# NVIDIA Tensor Core

## Volta

Volta 的每个 Tensor Core 每周期（吞吐）能做一个 $4\times4\times4$ 的矩阵乘加：

$$
D_{4\times4} = A_{4\times4}\,B_{4\times4} + C_{4\times4}
$$

$A$、$B$ 是 $4\times4$ 的 FP16 矩阵，$C$、$D$ 是 $4\times4$ 的矩阵，元素为 FP32 或 FP16：

| 矩阵 | 大小 | 格式 |
| --- | --- | --- |
| $A$ | $4\times4$ | FP16（1-5-10） |
| $B$ | $4\times4$ | FP16（1-5-10） |
| $C$ | $4\times4$ | FP32（1-8-23）或 FP16 |
| $D$ | $4\times4$ | 同 $C$ |

每个输出元素取 $A$ 的一行和 $B$ 的一列做 4 项点积，再加上 $C$ 的对应元素，即 $d_{ij}=\sum_{k=0}^{3}a_{ik}b_{kj}+c_{ij}$，共 64 次 FMA。

硬件上它是一个 $4\times4$ 的 dot4 阵列：**16 个 dot4 单元**，每个单元有 4 个 11×11 乘法器，负责输出矩阵的一个元素。

每个 SM 有 8 个 TC（每个 Processing Block 2 个），合计 512 FMA/周期。按 V100 的 80 个 SM、1.53 GHz 计算，FP16 峰值约为 125 TFLOPS。

### dot4 单元

dot4 单元的工作方式：4 个乘积和第 5 个加数 $c$ 一起对齐到最大指数，截断后做一次定点求和，最后才归一化并舍入到输出格式（FP32 用 RZ，FP16 用 RNE）。伪代码如下：

```text
dot4(A, B, C, i, j):             # A,B: 4×4 FP16；C: 4×4（FP32/FP16）；(i,j) 指明算哪个输出
    for k in 0..3:
        p_k = A[i][k] * B[k][j]  # 11×11 乘法器，精确，不规格化
        e_k = exp(A[i][k]) + exp(B[k][j])
    e_max = max(e_0, e_1, e_2, e_3, exp(C[i][j]))

    S = 0
    for k in 0..3:
        S += trunc(p_k * 2^(e_k - e_max + 23))        # 对齐到 e_max，右移截断
    S += trunc(C[i][j] * 2^(exp(C[i][j]) - e_max + 23))

    if D 是 FP32:
        return RZ_FP32(S * 2^(e_max - 23))            # 归一化后向零截断
    else:
        return RNE_FP16(S * 2^(e_max - 23))           # 归一化后 RNE 到 FP16

mma4x4(A, B, C):                 # 一个 TC 每周期吞吐一个 4×4×4
    D = 4×4 矩阵
    for i in 0..3, j in 0..3:    # 16 个 dot4 同时进行
        D[i][j] = dot4(A, B, C, i, j)
    return D
```

输出为 FP16 时，5 项的对齐、截断和定点求和都不变，只有最后一步从 RZ 到 FP32 换成 RNE 到 FP16。

### 模拟器

下面是一个可交互的 $4\times4\times4$ 模拟器：A、B、C 可以自由修改，输出格式可选 FP32（RZ）或 FP16（RNE）；点击 D 的任意元素，左侧会显示该元素的 dot4 逐步计算。

<style>
.tc-sim { width: 100%; height: 880px; border: 0; }
@media (max-width: 760px) { .tc-sim { height: 1280px; } }
</style>
<iframe class="tc-sim" src="nvidia_tensor_core_sim.html" title="Volta Tensor Core 4×4×4 模拟器" loading="lazy"></iframe>

## 引用

- NVIDIA, *NVIDIA Tesla V100 GPU Architecture* (whitepaper), 2017. <https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf>
- B. R. Boswell et al., *Generalized acceleration of matrix multiply accumulate operations*, US Patent 10,884,734 B2, 2021. <https://patents.google.com/patent/US10884734B2/en>
- M. Fasi et al., *Numerical behavior of NVIDIA tensor cores*, PeerJ Comput. Sci. 7:e330, 2021. <https://doi.org/10.7717/peerj-cs.330>
- P. Xie et al., *Bit-Accurate Modeling of GPU Matrix Multiply-Accumulate Units: Demystifying Numerical Discrepancy and Accuracy*, MICRO 2026 / arXiv:2511.10909. <https://arxiv.org/abs/2511.10909>，代码：<https://github.com/microsoft/MMA-Sim>
- Z. Jia et al., *Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking*, arXiv:1804.06826. <https://arxiv.org/abs/1804.06826>
