# SGEMM on CUDA

使用 CUDA 实现 SGEMM（准确地说，实现了矩阵乘法 $C=A*B$，而不是完整的 GEMM 计算 $C = \alpha A*B + \beta C$）。

参考了如下的资料：

- [[施工中] CUDA GEMM 理论性能分析与 kernel 优化](https://zhuanlan.zhihu.com/p/441146275)
- [CUDA SGEMM矩阵乘法优化笔记——从入门到cublas](https://zhuanlan.zhihu.com/p/518857175)

## SGEMM 定义

SGEMM 指的是单精度浮点矩阵乘法，它的完整性形式是 $C = \alpha A*B + \beta C$，在本文中，实现的是基础的 $C = A * B$，相当于设定了 $\alpha = 1, \beta = 0$。本文约定用 row major 的保存方式，默认情况下所有尺寸都是先行后列。

矩阵乘法按照定义，是这样的过程：

```c
// Input
float a[m][k];
float b[k][n];

// Output
float c[m][n];

for (int i = 0;i < m;i++) {
    for (int j = 0;j < n;j++) {
        c[i][j] = 0;
        for (int l = 0;l < k;l++) {
            c[i][j] += a[i][l] * b[l][j];
        }
    }
}
```

也就是循环 C 矩阵的每个元素，然后计算 A 矩阵一行和 B 矩阵一列的内积，结果就是 C 矩阵该元素的值。约定 A 矩阵的大小是 $m*k$，B 矩阵大小是 $k*n$，C 矩阵大小是 $m*n$。

## SGEMM v1

接下来思考如何用 CUDA 实现。在 CUDA 中，启动 kernel 的单位是 grid，一个 grid 有若干个 block，每个 block 有若干个 thread。因此需要想好每个 thread 负责什么任务，再去思考 block 的大小以及 grid 的大小。

首先比较简单的思路是，既然要枚举 C 矩阵的 $m*n$ 个元素，那就让每个线程对应一个 C 矩阵的元素，线程内要做的事情就是，对 K 循环，计算两个向量的内积，最后写入 C 矩阵：

```c
// x, y: the x and y index of the current thread
float sum = 0.0;
for (int i = 0; i < k; i++) {
    // sum += a[x][i] * b[i][y];
    sum += a[IDX2C(x, i, k)] * b[IDX2C(i, y, n)];
}

// c[x][y] = sum;
c[IDX2C(x, y, n)] = sum;
```

这里的 `IDX2C` 指的是计算二维矩阵下标对应的一维下标：

```c
#define IDX2C(i, j, ld) (((i) * (ld)) + (j))
```

因为是 row major，所以 i 是行下标，j 是列下标，ld 就是一行的元素个数，同时也是矩阵的列数。因此 `a[x][i]` 就变成了 `a[IDX2C(x, i, k)]`，k 就是 a 矩阵的列数，同理 `b[i][y]` 变成了 `b[IDX2C(i, y, n)]`。

那么每个线程就实现了 C 矩阵中单个元素的计算，接下来就需要思考 grid 有多少个 block，block 有多少个 thread 了。由于 C 矩阵一共是 $m*n$ 个元素，所以最终是希望有 $m*n$ 个 thread。CUDA 限制每个 block 最多有 1024 个 thread，为了方便，就让每个 block 包括 $32*32$ 个 thread，每个 block 负责 $32*32$ 的矩阵：

```c
//            n
//
//    +-------+-------+
//    |       |       |
//    | 32x32 | 32x32 |
//    |       |       |
// m  +-------+-------+
//    |       |       |
//    | 32x32 | 32x32 |
//    |       |       |
//    +-------+-------+
//
//            C
#define BLOCK_SIZE_PER_THREAD_BLOCK 32
blockDim->x = BLOCK_SIZE_PER_THREAD_BLOCK;
blockDim->y = BLOCK_SIZE_PER_THREAD_BLOCK;
blockDim->z = 1;
```

这样的话，就是把 C 矩阵分成了若干个 $32*32$ 的子矩阵，每个子矩阵交给一个 thread block 去执行。子矩阵的个数，那就看 m 和 n 除以 32 是多少，如果不能整除，那就向上取整：

```c
#define BLOCK_SIZE_PER_THREAD_BLOCK 32
gridDim.x =
    (m + (BLOCK_SIZE_PER_THREAD_BLOCK - 1)) / BLOCK_SIZE_PER_THREAD_BLOCK;
gridDim.y =
    (n + (BLOCK_SIZE_PER_THREAD_BLOCK - 1)) / BLOCK_SIZE_PER_THREAD_BLOCK;
gridDim.z = 1;
```

在这样的设定下，就可以比较容易地计算出每个 thread 负责的 C 矩阵的元素的行列下标：

```c
// each thread handles one element in C matrix
//          n=3
//     +---+---+---+
//     |t00|t01|t02|
//     +---+---+---+
//     |t10|t11|t12|
// m=4 +---+---+---+
//     |t20|t21|t22|
//     +---+---+---+
//     |t30|t31|t32|
//     +---+---+---+
//
//           C
int x = blockDim.x * blockIdx.x + threadIdx.x;
int y = blockDim.y * blockIdx.y + threadIdx.y;
```

结合这些代码，就可以实现出一个基础的 SGEMM 代码。