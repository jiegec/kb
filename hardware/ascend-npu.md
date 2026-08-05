# 华为昇腾 NPU

## 架构分析

基本架构：<https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/latest/programug/Ascendcopdevg/docs/guide/%E7%BC%96%E7%A8%8B%E6%8C%87%E5%8D%97/%E9%AB%98%E7%BA%A7%E7%BC%96%E7%A8%8B/%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0/%E5%9F%BA%E6%9C%AC%E6%9E%B6%E6%9E%84.md>

Atlas A2 训练系列产品/Atlas A2 推理系列产品的架构图，来自 cann/asc-devkit：

NPU 架构版本 3510(950) 的架构图，来自 cann/asc-devkit：

不同架构版本：

| 产品            | NPU  | DAV  |
| --------------- | ---- | ---- |
| Ascend 910      | 1001 | C100 |
| Ascend 910B     | 2201 | C220 |
| Ascend 950      | 3510 | C310 |
| Ascend 310P/610 | 2002 | M200 |
| Ascend 310B     | 3002 | M300 |
| Kirin X90       | 3003 | L300 |
| Kirin 9030      | 3113 | L311 |

## CANN 安装

<https://www.hiascend.com/cann/download>

CANN 9.1.0 下载：

```shell
wget https://ascend-cann-open.obs.cn-north-4.myhuaweicloud.com/CANN/CANN%209.1.0/Ascend-cann_9.1.0_linux-x86_64.run
wget https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/CANN/CANN%209.1.0/Ascend-cann-950-ops_9.1.0_linux-x86_64.run
```

在 Docker 里安装：

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i \
        's@//archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g; \
         s@//security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' \
        /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-dev \
        build-essential gcc g++ make cmake git wget curl \
        libssl-dev zlib1g-dev libffi-dev libgmp-dev \
        numactl libnuma1 kmod unzip tar bc \
        file vim less \
    && rm -rf /var/lib/apt/lists/*

COPY Ascend-cann_9.1.0_linux-x86_64.run /tmp/Ascend-cann_9.1.0_linux-x86_64.run
COPY Ascend-cann-950-ops_9.1.0_linux-x86_64.run /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run

RUN chmod +x /tmp/Ascend-cann_9.1.0_linux-x86_64.run \
    && /tmp/Ascend-cann_9.1.0_linux-x86_64.run --quiet --install \
        --install-for-all

RUN chmod +x /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run \
    && /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run --quiet --install --install-for-all
```

## CANN 样例代码分析

### vector_add 样例

vector_add 样例来自 [`cann/cann-samples`](https://gitcode.com/cann/cann-samples) 的 [`Samples/0_Introduction/vector_add`](https://gitcode.com/cann/cann-samples/blob/master/Samples/0_Introduction/vector_add/README.md) 路径，核心代码：

```c++
template <typename T>
__global__ __aicore__ __vector__ void add_kernel(
    GM_ADDR x, GM_ADDR y, GM_ADDR z, int64_t totalLength, int64_t blockLength, uint32_t tileSize)
{
    // setup double buffering omitted
    // loop over tiles
    for (int64_t i = 0; i < tileNum; ++i) {
        // copy from gm to ub omitted
        // compute
        xLocal = inQueueX.DeQue<T>();
        yLocal = inQueueY.DeQue<T>();
        AscendC::LocalTensor<T> zLocal = outQueueZ.AllocTensor<T>();
        AscendC::Add(zLocal, xLocal, yLocal, tileElementNum);
        outQueueZ.EnQue(zLocal);
        inQueueX.FreeTensor(xLocal);
        inQueueY.FreeTensor(yLocal);
        // copy from ub to gm omitted
    }
}
```

下面构建并用 cannsim 跑样例：

```shell
source /usr/local/Ascend/cann-9.1.0/set_env.sh
# Setup CANN-Samples
git clone https://gitcode.com/cann/cann-samples
cd cann-samples
cmake -S . -B build -DNPU_ARCH=dav-3510
# Compile vector_add example
cmake --build build --target vector_add
# Run vector_add example in cannsim
cannsim record ./build/Samples/0_Introduction/vector_add/vector_add -s Ascend950 -o ./sim_out
# Generate report
cannsim report -e ./sim_out/npusim_TIMESTAMP_vector_add
```

在 `./sim_out/npusim_TIMESTAMP_vector_add` 目录下得到结果：

- `record/instr.bin`：执行的指令历史，二进制格式，可以用 cannsim 解析，源码在 `/usr/local/Ascend/cann-9.1.0/python/site-packages/cannsim/prof/src/backend/calog_handlers/instr_calog_bin_reader_simple.py`，内部是多个 `<QIIQ200s200s` 结构体，对应的字段是 tick、core、sub、pc、dec、exe；日志样例：`(PC: 0x9000d0d000) SCALAR : (Binary: 0x02004880) (ID: 000000) MOV_XD_SPR`，猜测是从特殊寄存器（SPR）移动（MOV）数据到通用寄存器（XD）
- `report/results/kernel_0_reports/core_0/trace_core0.json`：Chrome trace 格式，可以看到 NPU 各部分在做什么事情，可以在 `chrome://tracing` 页面里加载

这个样例主要做的事情是，从 GM (Global Memory) 拷贝数据到 UB (Unified Buffer)，在 UB 上读取数据，向量求和后，写入 UB，再从 UB 拷贝数据到 GM，类似 CUDA 上，先把数据从 GM 拷贝到 Shared Memory，在 Shared Memory 上进行向量求和，写入 Shared Memory 后，再从 Shared Memory 拷贝数据到 GM。不过这里实际上是有多个单元在协作，从 Chrome tracing 来看：

1. 标量单元 AIV0_SCALAR 执行一些未知的初始化指令
1. AIV0_MTE2 执行两个 MOV_SRC_TO_DST_ALIGNv2 指令，从 GM 拷贝两个向量的数据到 UB 上
1. AIV0_RVECLD 执行 RV_VLD 指令，应该是把 UB 的数据读取到寄存器里；AIV0_RVECEX 单元执行 RV_PLT 和 RV_VADD，PLT 应该是 predicate less than 的意思，根据循环的进展计算 mask，VADD 进行的是实际的向量求和；最后 AIV0_RVECST 单元执行 RV_VST 指令把数据从寄存器写到 UB 里
1. 最后 AIV0_MTE3 执行 MOV_SRC_TO_DST_ALIGNv2 指令，从 UB 拷贝输出向量的值到 GM

### custom_kernel_launch 样例

在 [`cann/runtime`](https://gitcode.com/cann/runtime) 的 `example/0_quickstart/4_custom_kernel_launch` 下面，也有一个 [`vector_add_kernel.cpp`](https://gitcode.com/cann/runtime/blob/master/example/0_quickstart/4_custom_kernel_launch/vector_add_kernel.cpp) 样例，但它其实采用的是标量单元实现向量乘加，看到的计算都是在 AIV0_SCALAR 里进行的：先是 `LD_XD_XN_IMM` 指令，应该是从 GM 读取数据到寄存器，然后用 `MADD` 指令计算向量乘加 `srcA[idx] + alpha * srcB[idx]`，最后用 `ST_XD_XN_IMM` 指令把数据写到 GM。代码：

```c++
extern "C" __global__ __aicore__ void VectorAddKernel(
    __gm__ float* srcA, __gm__ float* srcB, __gm__ float* dst, float alpha, uint32_t elementCount)
{
    for (uint32_t idx = 0; idx < elementCount; ++idx) {
        dst[idx] = srcA[idx] + alpha * srcB[idx];
    }

    // A5 编译时，生成器会在 kernel tail 中追加 dci()。关闭自动 DCCI 后，scalar store 产生的脏数据
    // 尚未回写到 GM 就被 dci() 失效，导致输出全为 0，因此需要显式调用 dcci() 将数据回写到 GM。
#if __NPU_ARCH__ == 3510
    dcci(reinterpret_cast<__gm__ int64_t*>(dst),
        cache_line_t::ENTIRE_DATA_CACHE,
        dcci_dst_t::CACHELINE_OUT);
#endif
}
```

这一点和 NVIDIA 就很不一样：NVIDIA 是 SIMT，写标量代码，实际上也是向量化执行。而 NPU 就要像前一个例子那样，调用 `AscendC::Add` 来主动让 Vector 单元进行向量计算。这可能就是为啥大家觉得 NPU 编程比较复杂？涉及到向量计算的时候，写起来就是很多的函数调用，比较麻烦。

只保留 kernel 部分，生成 LLVM IR：

```shell
$ cat kernel.cpp
extern "C" __global__ __aicore__ void VectorAddKernel(
    __gm__ float* srcA, __gm__ float* srcB, __gm__ float* dst, float alpha, uint32_t elementCount)
{
    for (uint32_t idx = 0; idx < elementCount; ++idx) {
        dst[idx] = srcA[idx] + alpha * srcB[idx];
    }
}
$ ccec -O3 -std=c++17 --cce-aicore-lang --cce-aicore-arch=dav-c310-vec --cce-aicore-only -c -emit-llvm
$ llvm-dis vector_add_kernel-cce-hiipu64-hisilicon-cce-dav-c310-vec.bc
```

在生成的 `vector_add_kernel-cce-hiipu64-hisilicon-cce-dav-c310-vec.ll` 里可以看到熟悉的 LLVM IR：

```text
; Function Attrs: nofree nosync nounwind memory(argmem: readwrite)
define dso_local cc73 void @VectorAddKernel(ptr addrspace(1) nocapture noundef readonly %0, ptr addrspace(1) nocapture noundef readonly %1, ptr addrspace(1) nocapture noundef writeonly %2, float noundef %3, i32 noundef %4) local_unnamed_addr #0 !dbg !7 {
  %6 = zext i32 %4 to i64, !dbg !10
  %7 = icmp eq i32 %4, 0, !dbg !10, !loop.guard !11
  br i1 %7, label %20, label %8, !dbg !12, !loop.guard !11

8:                                                ; preds = %5
  br label %9, !dbg !12

9:                                                ; preds = %8, %9
  %10 = phi i64 [ %17, %9 ], [ 0, %8 ]
  %11 = getelementptr inbounds float, ptr addrspace(1) %0, i64 %10, !dbg !13
  %12 = load float, ptr addrspace(1) %11, align 4, !dbg !13, !tbaa !14
  %13 = getelementptr inbounds float, ptr addrspace(1) %1, i64 %10, !dbg !18
  %14 = load float, ptr addrspace(1) %13, align 4, !dbg !18, !tbaa !14
  %15 = tail call float @llvm.fmuladd.f32(float %3, float %14, float %12), !dbg !19
  %16 = getelementptr inbounds float, ptr addrspace(1) %2, i64 %10, !dbg !20
  store float %15, ptr addrspace(1) %16, align 4, !dbg !21, !tbaa !14
  %17 = add nuw nsw i64 %10, 1, !dbg !22
  %18 = icmp eq i64 %17, %6, !dbg !10
  br i1 %18, label %19, label %9, !dbg !12, !llvm.loop !23

19:                                               ; preds = %9
  br label %20, !dbg !26

20:                                               ; preds = %19, %5
  ret void, !dbg !26
}
```

### vector_function_add 样例

cann-samples 里还有一个 [`vector_function_add`](https://gitcode.com/cann/cann-samples/blob/master/Samples/0_Introduction/vector_function_add/README.md) 样例，换了一种方式来表达向量计算，写法上就非常接近 SIMD Intrinsics 的写法：

```c++
template <typename T>
__simd_vf__ inline void VectorFunctionAdd(
    __ubuf__ T* xAddr, __ubuf__ T* yAddr, __ubuf__ T* zAddr, uint32_t total, uint16_t loopNum)
{
    constexpr uint32_t vectorLength = AscendC::VECTOR_REG_WIDTH / sizeof(T);
    AscendC::Reg::RegTensor<T> xReg, yReg, zReg;
    AscendC::Reg::MaskReg mask;
    uint32_t remain = total;

    for (uint16_t i = 0; i < loopNum; ++i) {
        mask = AscendC::Reg::UpdateMask<T>(remain);
        AscendC::Reg::LoadAlign<T, AscendC::Reg::LoadDist::DIST_NORM>(
            xReg, xAddr + i * vectorLength);
        AscendC::Reg::LoadAlign<T, AscendC::Reg::LoadDist::DIST_NORM>(
            yReg, yAddr + i * vectorLength);
        AscendC::Reg::Add(zReg, xReg, yReg, mask);
        AscendC::Reg::StoreAlign<T, AscendC::Reg::StoreDist::DIST_NORM>(
            zAddr + i * vectorLength, zReg, mask);
    }
}
```

取 mask，load，add 再 store，这和写 RVV/SVE 的 intrinsics 也没什么区别。这种写法叫 RegBase，中间计算结果可以保留在向量寄存器里，不用频繁读写 UB。不过，vector function 还是只能访问 UB，外面的 scalar 部分还是要负责 GM 和 UB 之间的数据搬运。与之相对的老 API 叫 MemBase，就是上面那种 `AscendC::Mul`，参数都是 `AscendC::LocalTensor` 类型，对应的是 UB 上保存的数据，输入和输出都在 UB 上。

循环体对应的 LLVM IR：

```llvm
7:                                                ; preds = %5, %7
  %8 = phi i16 [ %22, %7 ], [ 0, %5 ]
  %9 = phi i32 [ %13, %7 ], [ %3, %5 ]
  %10 = zext i16 %8 to i64, !dbg !294
  %11 = tail call { <256 x i1>, i32 } @llvm.hivm.plt.b32.v300(i32 %9), !dbg !295
  %12 = extractvalue { <256 x i1>, i32 } %11, 0, !dbg !295
  %13 = extractvalue { <256 x i1>, i32 } %11, 1, !dbg !295
  %14 = shl nuw nsw i64 %10, 6, !dbg !305
  %15 = getelementptr inbounds float, ptr addrspace(6) %0, i64 %14, !dbg !306
  %16 = tail call <64 x float> @llvm.hivm.vldsx1.v64f32(ptr addrspace(6) %15, i32 0, i32 0, i32 0), !dbg !307
  %17 = getelementptr inbounds float, ptr addrspace(6) %1, i64 %14, !dbg !316
  %18 = tail call <64 x float> @llvm.hivm.vldsx1.v64f32(ptr addrspace(6) %17, i32 0, i32 0, i32 0), !dbg !317
  %19 = tail call <64 x float> @llvm.hivm.vadd.s.x.v64f32(<64 x float> %16, <64 x float> %18, <256 x i1> %12), !dbg !321
  %20 = bitcast <64 x float> %19 to <64 x i32>, !dbg !321
  %21 = getelementptr inbounds float, ptr addrspace(6) %2, i64 %14, !dbg !332
  tail call void @llvm.hivm.vstsx1.v64i32(<64 x i32> %20, ptr addrspace(6) %21, i32 0, i32 2, i32 0, <256 x i1> %12), !dbg !333
  %22 = add nuw i16 %8, 1, !dbg !341
  %23 = icmp eq i16 %22, %4, !dbg !292
  br i1 %23, label %24, label %7, !dbg !293, !llvm.loop !342
```

这里出现的 llvm.hivm 的 intrinsic 应该就对应到指令上了。

### simt 样例

`cann/cann-samples/Samples/1_Features/hardware_features/simt` 下面有 SIMT 的样例，其编程模型就和 NVIDIA 十分接近了，很多概念也直接映射过去。UB 就变成了 Shared Memory，然后 UB 还划分出了一部分空间用于 SIMD DCache，这和 NVIDIA 的 L1 和 Shared Memory 共享一篇空间，大小可调是类似的。SIMT 模式下还能访问 GM，比上面的向量编程会方便很多，不用强制走一遍 UB。样例代码：

```c++
template <uint32_t MAX_THREADNUM, typename DATA_TYPE, typename INDICES_TYPE, typename INDEX_SIZE_TYPE>
inline __simt_vf__ __aicore__ __launch_bounds__(MAX_THREADNUM) void gather_function(__gm__ DATA_TYPE *x, __gm__ INDICES_TYPE *indices, __gm__ DATA_TYPE *y, 
    INDEX_SIZE_TYPE gatherDimSize, INDEX_SIZE_TYPE indicesDimSize, INDEX_SIZE_TYPE innerDimSize, INDEX_SIZE_TYPE outNum) {
    for (INDEX_SIZE_TYPE idx = threadIdx.x + blockIdx.x * blockDim.x; idx < outNum; 
        idx += block_num * blockDim.x) {
        INDEX_SIZE_TYPE outerI = idx / (gatherDimSize * innerDimSize);
        INDEX_SIZE_TYPE tmpI = idx - outerI * (gatherDimSize * innerDimSize);
        INDEX_SIZE_TYPE gatherI = tmpI / innerDimSize;
        INDEX_SIZE_TYPE innerI = tmpI - gatherI * innerDimSize;
        INDICES_TYPE indicesValue = indices[gatherI];
        INDEX_SIZE_TYPE indicesValueI = static_cast<INDEX_SIZE_TYPE>(indicesValue);
        INDEX_SIZE_TYPE xIndex = outerI * gatherDimSize * innerDimSize + indicesValueI * innerDimSize + innerI;
        // indices overflow
        bool indexOutOfBound = indicesValue < 0 || indicesValue >= gatherDimSize;
        y[idx] = indexOutOfBound ? 0 : x[xIndex];
    }
}
```

这个时候的编程就和 NVIDIA 没啥区别了。可以当 GPGPU 来编程？不过目前还是主推 SIMD，SIMT 还是辅助，填补一些可编程性以及 SIMD 用 Mask 处理起来比较麻烦的运算。

### 小结

NPU 的编程模式，虽然也是用 C 代码，但确实和 NVIDIA 很不一样。NVIDIA 的 SIMT 可以把看起来是标量的代码向量化执行，不过 NPU 上，目前还是需要显式地通过特定的 Ascend 函数来执行向量指令，更类似 CPU，就是默认写的都是标量代码，需要向量的时候再用 intrinsics。SIMD 的部分，就和 SVE/RVV 类似，循环里面，计算 mask，然后一系列的向量 intrinsics。

矩阵部分，也是用 MTE 做异步数据传输，从 GM 到 L1，再从 L1 到 L0A 和 L0B，矩阵运算从 L0A 和 L0B 取数据，结果保存在 L0C 里面，最后再把数据从 L0C 拷贝到 GM。

但是 NPU 比较麻烦的是，它的向量部分，不能直接访问 GM，只能访问 UB，其实就相当于在 NVIDIA 上只能访问 Shared Memory。所以要向量加速，得先通过 MTE2 从 GM 搬数据到 UB，向量计算完以后，再通过 MTE3 把数据从 UB 搬到 GM。矩阵那边，还有 L0A、L0B 和 L0C，矩阵乘法的输入输出也必须在特定的片上存储里，这一点比较像 NVIDIA 的 [`tcgen05`](https://gau-nernst.github.io/tcgen05/)，额外搞了一个 Tensor Memory，即矩阵乘法的输入在 Shared Memory，输出在 Tensor Memory，再配合 Tensor Memory Accelerator 来负责从 GM 搬运数据到 Shared Memory。总之在矩阵运算来看，NVIDIA 和华为的设计是趋同了，主要还是向量的部分不一样。

有了 SIMT 模式以后，在 SIMT 模式下的编程就和 NVIDIA 基本一样了，从样例代码能看出来，很多语法也是复用了。编程易用性上肯定有一定的提升，但性能就不好说了。
