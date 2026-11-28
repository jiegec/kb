// probe_sm103_fp64.cu — 在 B300（sm_103a）上确认 FP64 张量路径（DMMA）是否还存在。
//
// 编译：
//   nvcc -arch=sm_103a -O3 -o probe scripts/probe_sm103_fp64.cu
// 反汇编（看指令是否还在）：
//   cuobjdump -sass probe | grep -E '\bDMMA\b|\bDFMA\b' | sort | uniq -c
// 运行（看是否有实际加速）：
//   ./probe
//
// 判读：
//   k_mma  里出现 DMMA.8x8x4  -> sm_103 仍有该指令
//   k_mma  里只有 DFMA         -> mma.sync.f64 被编译成 CUDA core 序列
//   k_mma 吞吐 ≈ k_dfma 吞吐   -> 即使指令还在，FP64 数据通路也只剩矢量速率

#include <cstdio>
#include <cuda_runtime.h>

__device__ __forceinline__ void mma_f64(double &d0, double &d1,
                                        double a0, double b0) {
#if defined(__CUDA_ARCH__) && (__CUDA_ARCH__ >= 800)
  asm volatile(
      "mma.sync.aligned.m8n8k4.row.col.f64.f64.f64.f64 "
      "{%0,%1}, {%2}, {%3}, {%0,%1};\n"
      : "+d"(d0), "+d"(d1)
      : "d"(a0), "d"(b0));
#endif
}

// 依赖链形式的 m8n8k4：每次把上一次的累加器当前馈入，防止乱序折叠
__global__ void k_mma(double *out, int iters) {
  double d0 = threadIdx.x * 1e-9;
  double d1 = blockIdx.x * 1e-9;
  double a0 = 1.0 + threadIdx.x * 1e-12;
  double b0 = 1.0 + blockIdx.x * 1e-12;
  for (int i = 0; i < iters; ++i) mma_f64(d0, d1, a0, b0);
  // 不可达分支：保证 d0/d1 不会被当成死代码消掉
  if (d0 == 12345.6789 && d1 == 0.5) out[0] = d0 + d1;
}

// 参考：纯 DFMA 依赖链，测 FP64 CUDA core 的矢量速率
__global__ void k_dfma(double *out, int iters) {
  double d0 = threadIdx.x * 1e-9;
  double d1 = blockIdx.x * 1e-9;
  double a0 = 1.0 + threadIdx.x * 1e-12;
  double a1 = 1.0 + blockIdx.x * 1e-12;
  for (int i = 0; i < iters; ++i) {
    d0 = __fma_rn(a0, a1, d0);
    d1 = __fma_rn(a1, d0, d1);
  }
  if (d0 == 12345.6789 && d1 == 0.5) out[0] = d0 + d1;
}

static double time_kernel(void (*k)(double *, int), double *buf, int grid,
                         int block, int iters, int reps) {
  cudaEvent_t s, e;
  cudaEventCreate(&s);
  cudaEventCreate(&e);
  k<<<grid, block>>>(buf, iters);  // warmup
  cudaEventRecord(s);
  for (int r = 0; r < reps; ++r) k<<<grid, block>>>(buf, iters);
  cudaEventRecord(e);
  cudaEventSynchronize(e);
  float ms = 0;
  cudaEventElapsedTime(&ms, s, e);
  cudaEventDestroy(s);
  cudaEventDestroy(e);
  return ms / reps;
}

int main() {
  int dev = 0;
  cudaDeviceProp p{};
  cudaGetDeviceProperties(&p, dev);
  printf("device      : %s\n", p.name);
  printf("compute cap : %d.%d\n", p.major, p.minor);
  printf("SMs         : %d\n", p.multiProcessorCount);
  printf("clock (max) : %.0f MHz\n", p.clockRate / 1000.0);
  if (p.major != 10 || p.minor != 3)
    printf("WARNING: 这不是 sm_103 设备，结论不能套到 GB110 上\n");

  double *buf;
  cudaMalloc(&buf, sizeof(double));

  const int block = 128, grid = p.multiProcessorCount * 8, iters = 20000;
  const long threads = (long)grid * block;

  // m8n8k4 = 8*8*4 MAC = 512 FLOP / warp-instruction = 16 FLOP / thread
  double ms_mma = time_kernel(k_mma, buf, grid, block, iters, 20);
  double flops_mma = (double)threads * iters * 16.0;
  double tflops_mma = flops_mma / (ms_mma * 1e-3) / 1e12;

  // 2 条独立 DFMA / 线程 / 迭代 = 4 FLOP
  double ms_dfma = time_kernel(k_dfma, buf, grid, block, iters, 20);
  double flops_dfma = (double)threads * iters * 4.0;
  double tflops_dfma = flops_dfma / (ms_dfma * 1e-3) / 1e12;

  printf("\nmma.sync m8n8k4.f64 : %.3f TFLOPS (%.3f ms)\n", tflops_mma, ms_mma);
  printf("DFMA  reference     : %.3f TFLOPS (%.3f ms)\n", tflops_dfma, ms_dfma);
  printf("ratio mma/dfma      : %.2fx\n", tflops_mma / tflops_dfma);
  printf("\n(参考：B300 的 FP64 规格是 1.2-1.3 TFLOPS，"
         "若 mma 也只有这个量级，说明没有可用的张量加速)\n");

  cudaFree(buf);
  return 0;
}
