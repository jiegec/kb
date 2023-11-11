# SGEMM on CUDA

使用 CUDA 实现 SGEMM（准确地说，实现了矩阵乘法 $C=A*B$，而不是完整的 GEMM 计算 $C = \alpha A*B + \beta C$）。

参考了如下的资料：

- [CUDA 矩阵乘法终极优化指南](https://zhuanlan.zhihu.com/p/410278370)
- [[施工中] CUDA GEMM 理论性能分析与 kernel 优化](https://zhuanlan.zhihu.com/p/441146275)
- [CUDA SGEMM 矩阵乘法优化笔记——从入门到 cublas](https://zhuanlan.zhihu.com/p/518857175)
- [CUDA Ampere Tensor Core HGEMM 矩阵乘法优化笔记 —— Up To 131 TFLOPS!](https://zhuanlan.zhihu.com/p/555339335)

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

## SGEMM v2

接下来第二个版本，在第一个版本的基础上，把 shared memory 使用上。Shared memory 是 CUDA 每个 SM 内部的存储，可供同一个 Block 内的 thread 共享，比访问 Global memory 性能更好。

首先要思考如何使用 shared memory。目前的设定是，每个线程负责 1 个 C 矩阵的元素，每个 thread block 负责 $32*32$ 的 C 矩阵的子矩阵。这个 thread block 涉及到的 A 矩阵的部分是一个长条形的子矩阵 $32 * k$，涉及到 B 矩阵的部分是 $k * 32$。由于 $k$ 的大小取决于用户输入，它可能很大，所以没法把整个 $32 * k$ 或者 $k * 32$ 的长条形矩阵放进 shared memory。那就只取一部分：先从 A 矩阵和 B 矩阵取 $32 * 32$ 的子矩阵到 shared memory，进行一番计算，再取 $32 * 32$ 的子矩阵，直到整个 $32 * k$ 和 $k * 32$ 取完为止。

那么就需要用 shared memory 保存两个 $32 * 32$ 的矩阵：

```c
__shared__ float aTile[BLOCK_SIZE_PER_THREAD_BLOCK]
                      [BLOCK_SIZE_PER_THREAD_BLOCK];
__shared__ float bTile[BLOCK_SIZE_PER_THREAD_BLOCK]
                      [BLOCK_SIZE_PER_THREAD_BLOCK];
```

接下来问题来了，怎么从 A 和 B 矩阵分别复制 $32*32$ 个元素？每个 thread block 正好有 $32*32$ 个线程，那就每个线程负责复制一个元素。正好 blockDim 设置的是 x 和 y 方向上各 32 个线程，那就每个线程负责写入 `aTile[threadIdx.x][threadIdx.y]` 和 `bTile[threadIdx.x][threadIdx.y]`。那么从 A 和 B 矩阵的哪里读取数据呢？

首先考虑 A 矩阵，第一次要取的 $32*32$ 矩阵，应该是当前 thread block 对应的同一行里，最左边的 $32*32$ 矩阵。这个矩阵左上角元素的下标应该是 $x=32 * blockIdx.x, y=0$，右下角元素的下标应该是 $x=32 * blockIdx.x + 31, y=31$。因此第一次循环的时候，第一个线程 $threadIdx.x=0, threadIdx.y=0$ 应该从 a 矩阵的 `a[32 * blockIdx.x][0]` 读取，最后一个线程 $threadIdx.x=15, threadIdx.y=15$ 应该从 a 矩阵的 `a[32 * blockIdx.x + 15][15]` 读取，正好每个线程对应一个 a 矩阵的元素，只是 X 方向上整体偏移了 $32 * blockIdx.x$，所以：

```c
aTile[threadIdx.x][threadIdx.y] = a[IDX2C(32 * blockIdx.x + threadIdx.x, threadIdx.y, k)];
```

类似地，b 矩阵会从 y 方向上读取，整体偏移了 $32 * blockIdx.y$，所以：

```c
bTile[threadIdx.x][threadIdx.y] = b[IDX2C(threadIdx.x, 32 * blockIdx.y + threadIdx.y, n)];
```

这是第一次循环的情况，下一次循环，从 A 矩阵读取时，y 方向要移动 32 项；从 B 矩阵读取时，x 方向要移动 32 项，把这个偏移 i 放进来：

```c
int x = 32 * blockIdx.x + threadIdx.x;
int y = 32 * blockIdx.y + threadIdx.y;
for (int i = 0; i < k; i += BLOCK_SIZE_PER_THREAD_BLOCK) {
    // 1. read data to aTile and bTile
    // each thread is responsible to copy one element from global memory
    aTile[threadIdx.x][threadIdx.y] = a[IDX2C(x, i + threadIdx.y, k)];
    bTile[threadIdx.x][threadIdx.y] = b[IDX2C(i + threadIdx.x, y, n)];
}
```

这样就完成了 $32*32$ 子矩阵的读取，并且会循环直到 $32*k$ 整个长条形的子矩阵都读取完成。接下来，就是边读边算，只不过把原来从 global memory 读取数据，改成从 shared memory 读取数据：

```c
__syncthreads();
for (int ii = i; ii < k && ii < i + BLOCK_SIZE_PER_THREAD_BLOCK; ii++) {
    // sum += a[x][i] * b[i][y];
    sum += aTile[threadIdx.x][ii - i] * bTile[ii - i][threadIdx.y];
}
```

注意全局的偏移和 shared memory 中偏移的关系。不要忘记在读取 shared memory 和计算之间插入 `__syncthreads()`，保证 thread block 中所有线程完成写入。

这个版本依然是每个线程负责 1 个 C 矩阵的元素，因此性能并没有什么变化，但是为后面的版本打下了基础。

## SGEMM v3

前面的两个版本性能不好，是因为大部分时间都拿来读取内存，实际计算的时间很少。如果要增加计算的比例，就需要把更多矩阵的元素放在寄存器中。因此，这个版本里，每个线程负责 $8*8$ 的矩阵，每个 thread block 缩小到 $16*16$ 个 thread，因为每个线程负责 $8*8$，所以一个 thread block 就负责了 $128*128$ 的 C 矩阵的子矩阵。因此，可以按如下方法计算 gridDim 和 blockDim：

```c
// each thread block handles 128*128 submatrix of C
// each thread handles 8*8 submatrix of C
//              n
//
//    +---------+---------+
//    |         |         |
//    | 128x128 | 128x128 |
//    |         |         |
// m  +---------+---------+
//    |         |         |
//    | 128x128 | 128x128 |
//    |         |         |
//    +---------+---------+
//
//              C
#define BLOCK_SIZE_PER_THREAD_BLOCK 128
#define BLOCK_SIZE_PER_THREAD 8
blockDim.x = BLOCK_SIZE_PER_THREAD_BLOCK / BLOCK_SIZE_PER_THREAD;
blockDim.y = BLOCK_SIZE_PER_THREAD_BLOCK / BLOCK_SIZE_PER_THREAD;
blockDim.z = 1;

// compute number of blocks
// round up
gridDim.x =
    (m + (BLOCK_SIZE_PER_THREAD_BLOCK - 1)) / BLOCK_SIZE_PER_THREAD_BLOCK;
gridDim.y =
    (n + (BLOCK_SIZE_PER_THREAD_BLOCK - 1)) / BLOCK_SIZE_PER_THREAD_BLOCK;
gridDim.z = 1;
```

此时如果想如法炮制 v2，在 shared memory 中保存 $128*128$ 矩阵的数据，会发现 CUDA 报错，表示没有这么多的 shared memory 可以使用。因此，不得不在 K 方向上，减少 shared memory 矩阵的规模，这里选择的是 $128*8$，也就是说，从 A 矩阵取出 $128*8$ 的子矩阵，从 B 矩阵取出 $8*128$ 的子矩阵，保存在 shared memory 中：

```c
// 128x128 is too large to save in shared memory,
// so we reduce k dimension to 8.
// save 128x8 tile from A, 8x128 tile from B
#define SHARED_K_DIMENSION 8
__shared__ float aTile[BLOCK_SIZE_PER_THREAD_BLOCK][SHARED_K_DIMENSION];
__shared__ float bTile[SHARED_K_DIMENSION][BLOCK_SIZE_PER_THREAD_BLOCK];
```

v2 版本中，读取数据到 shared memory 比较容易，因为每个线程只需要负责一个元素。但在 v3 中，shared memory 要保存 $128*8=1024$ 个元素，每个 thread block 只有 $16*16=256$ 个线程，意味着每个线程需要负责 4 个元素的读取。既然如此，就按照顺序，给每个线程分配四个连续的元素：

第一个线程负责 `aTile[0][0..=3]`，第二个线程负责 `aTile[0][4..=7]`，第三个线程负责 `aTile[1][0..=3]`，依次类推，寻找规律：

```c
// thread (0, 0), tid=0: aTile[0][0..=3]
// thread (0, 1), tid=1: aTile[0][4..=7]
// thread (0, 2), tid=2: aTile[1][0..=3]
// ...
// thread (0, 15), tid=15: aTile[7][4..=7]
// thread (1, 0), tid=16: aTile[8][0..=3]
// ...
// thread (15, 15), tid=255: aTile[127][4..=7]
```

可以发现，首先把 `threadIdx.x` 和 `threadIdx.y` 合并成连续的 tid：`tid = threadIdx.x * 16 + threadIdx.y`，之后就可以得到 aTile 的两个维度的起始下标：

```c
int tid = threadIdx.x * 16 + threadIdx.y;
// aTile[local_x][local_y..=(local_y+3)]
int local_x = tid / 2;
int local_y = 4 * (tid % 2);
```

接着，计算出当前 A 子矩阵的起始下标，就像 v2 中那样，只不过此时每个 block 对应的是 128 个元素，不再等于 blockDim.x，i 的含义和 v2 一样，也是 K 方向上的偏移：

```c
int block_x = BLOCK_SIZE_PER_THREAD_BLOCK * blockIdx.x;
int block_y = i;
```

最后用循环从 A 复制四个元素到 shared memory：

```c
for (int j = 0; j < 4; j++) {
    aTile[local_x][local_y + j] =
        a[IDX2C(block_x + local_x, block_y + local_y + j, k)];
}
```

类似地，循环从 B 复制四个元素到 shared memory，只不过这次子矩阵变成了 $128*8$，计算公式略有不同，但很容易找到规律：

```c
// thread (0, 0), tid=0: bTile[0][0..=3]
// thread (0, 1), tid=1: bTile[0][4..=7]
// ...
// thread (0, 15), tid=15: bTile[0][60..=63]
// thread (1, 0), tid=16: bTile[0][64..=67]
// ...
// thread (1, 15), tid=31: bTile[0][124..=127]
// ...
// thread (15, 15), tid=255: bTile[7][124..=127]
block_x = i;
block_y = BLOCK_SIZE_PER_THREAD_BLOCK * blockIdx.y;
local_x = tid / 32;
local_y = 4 * (tid % 32);
for (int j = 0; j < 4; j++) {
    bTile[local_x][local_y + j] =
        b[IDX2C(block_x + local_x, block_y + local_y + j, n)];
}
```

完成读取以后，每个线程负责 $8*8$ 矩阵的计算，因此需要多加两层循环：

```c
// each thread handles 8x8 elements in C
float sum[BLOCK_SIZE_PER_THREAD][BLOCK_SIZE_PER_THREAD] = {};

for (int i = 0; i < k; i += SHARED_K_DIMENSION) {
    // read aTile and bTile
    // ...

    __syncthreads();
    for (int ii = i; ii < k && ii < i + SHARED_K_DIMENSION; ii++) {
        for (int xx = 0; xx < BLOCK_SIZE_PER_THREAD; xx++) {
            for (int yy = 0; yy < BLOCK_SIZE_PER_THREAD; yy++) {
                sum[xx][yy] +=
                    aTile[threadIdx.x * BLOCK_SIZE_PER_THREAD + xx][ii - i] *
                    bTile[ii - i][threadIdx.y * BLOCK_SIZE_PER_THREAD + yy];
            }
        }
    }
}
```

最后写回 C 矩阵的时候，也是每个线程负责把自己的 $8*8$ 矩阵写回内存：

```c
for (int xx = 0; xx < BLOCK_SIZE_PER_THREAD && x + xx < m; xx++) {
    for (int yy = 0; yy < BLOCK_SIZE_PER_THREAD && y + yy < n; yy++) {
        c[IDX2C(x + xx, y + yy, n)] = sum[xx][yy];
    }
}
```

v3 版本相比 v2 和 v1 就有了明显的性能提升，因为读取数据到 shared memory 以后，后面的大量计算都在寄存器和 shared memory 上进行，并且由于 $8*8$ 矩阵保存在寄存器中，编译后会出现连续的 FMA 指令，达到比较高的浮点性能。NVCC 编译器也会对 `sum[xx][yy]` 计算的外积进行优化，先从 shared memory 读取 aTile 和 bTile 的向量，然后计算外积，计算外积的时候就只会涉及到寄存器了。

## SGEMM v4

v3 实现的时候，会出现一个性能瓶颈：Shared Memory Bank Conflict。问题出在外积的循环当中，它对 aTile 的读取是不连续的：

```c
for (int ii = i; ii < k && ii < i + SHARED_K_DIMENSION; ii++) {
    for (int xx = 0; xx < BLOCK_SIZE_PER_THREAD; xx++) {
        for (int yy = 0; yy < BLOCK_SIZE_PER_THREAD; yy++) {
            sum[xx][yy] +=
                aTile[threadIdx.x * BLOCK_SIZE_PER_THREAD + xx][ii - i] *
                bTile[ii - i][threadIdx.y * BLOCK_SIZE_PER_THREAD + yy];
        }
    }
}
```

在计算 `sum[xx][yy]` 的时候，同一个 warp 内相邻线程的 `threadIdx.x` 不同，它们访问 aTile 的地址差，等于 `8(BLOCK_SIZE_PER_THREAD) * 8(SHARED_K_DIMENSION) * 4(sizeof(float)) = 256` 字节，而 Shared Memory 组织方式是 32 个 Bank，每个 Bank 32 位，也就是说，如果访问 32 位数据时，两次访问的地址差是 128 字节的倍数，两次访问就由同一个 Bank 负责，而单个 Bank 处理请求只能串行，此时就出现了 Shared Memory Bank Conflict。bTile 不会遇到 Bank Conflict 的问题，因为如果 `threadIdx.y` 差一，那么地址差等于 `8(BLOCK_SIZE_PER_THREAD) * 4(sizeof(float)) = 32`，小于 128 字节。下面给出了 `blockDim.x=16, blockDim.y=16` 情况下，一个 warp 内的 `threadIdx` 情况：

```c
warp thread 0: threadIdx.x=0, threadIdx.y=0
// ...
warp thread 15: threadIdx.x=15, threadIdx.y=0
warp thread 16: threadIdx.x=0, threadIdx.y=1
// ...
warp thread 31: threadIdx.x=15, threadIdx.y=1
```

因此读取 aTile 会出现大量的 Bank Conflict，每个线程都读取同一个 Shared Memory Bank。所以解决办法是，把 threadIdx.x 变化时的地址差变成不是 128 的倍数，就可以避免 Bank Conflict。一个简单的办法是，交换 aTile 的行和列的保存方式，这样地址差就变成了 `8(BLOCK_SIZE_PER_THREAD) * 4(sizeof(float)) = 32`，大大减少了 Bank Conflict 的情况：

```c
// the two dimensions of aTile are swapped to reduce bank conflict
__shared__ float aTile[SHARED_K_DIMENSION][BLOCK_SIZE_PER_THREAD_BLOCK];

// thread (0, 0), tid=0: aTile[0..=3][0]
// thread (0, 1), tid=1: aTile[4..=7][0]
// thread (0, 2), tid=2: aTile[0..=3][1]
// ...
// thread (0, 15), tid=15: aTile[4..=7][7]
// thread (1, 0), tid=16: aTile[0..=3][8]
// ...
// thread (15, 15), tid=255: aTile[4..=7][127]
int block_x = BLOCK_SIZE_PER_THREAD_BLOCK * blockIdx.x;
int block_y = i;
int local_x = tid / 2;
int local_y = 4 * (tid % 2);
for (int j = 0; j < 4; j++) {
    // swap aTile dimensions to reduce bank conflict
    aTile[local_y + j][local_x] =
        a[IDX2C(block_x + local_x, block_y + local_y + j, k)];
}

// ...
// swap aTile dimensions to reduce bank conflict
sum[xx][yy] +=
    aTile[ii - i][threadIdx.x * BLOCK_SIZE_PER_THREAD + xx] *
    bTile[ii - i][threadIdx.y * BLOCK_SIZE_PER_THREAD + yy];
```

不过 Bank Conflict 依然是存在的：对于 threadIdx.x=0 和 threadIdx.x=4 的两个线程，它们的地址差是 `4 * 8(BLOCK_SIZE_PER_THREAD) * 4(sizeof(float)) = 128`，就会出现 Bank Conflict。但发生 Bank Conflict 的情况降低到了四分之一。如果想要更进一步，还可以调整 x 和 y 的比例，进一步减少 Bank Conflict，使得每个周期都可以打满 Shared memory 带宽。

这样写还有一个附带的好处：由于 xx 和 yy 都在内层循环，ii 是外层循环，把内存循环的循环变量参与到最后一维的下标中，可以改善内存局部性，并且也方便 NVCC 去优化，例如使用 LDS.128 指令，一条指令从 shared memory 读取 128 位的连续数据。

## SGEMM v5

v5 相比 v4 的改进在于 Double Buffering：现在的流程是每轮先读取数据到 shared memory，再从 shared memory 中读取数据来计算。但实际上，计算的时候访存单元是空闲的，可以让访存单元去读取下一轮的 shared memory 所要的数据，然后为了减少存储空间，把 Buffer 空间复制两份，一份用来给当前轮做计算，同时去读取数据到另一份，再把两份交换一下，这就是 Double Buffering。

首先是在 Shared Memory 上分配两倍的 Buffer 空间：

```c
// double buffering
__shared__ float aTile[2][SHARED_K_DIMENSION][BLOCK_SIZE_PER_THREAD_BLOCK];
__shared__ float bTile[2][SHARED_K_DIMENSION][BLOCK_SIZE_PER_THREAD_BLOCK];
```

接着思考：每一轮循环需要做的事情，包括计算当前轮的数据，以及读取下一轮的 shared memory，那么多次循环的效果是：

1. 计算第一轮的数据，读取第二轮的数据
2. 计算第二轮的数据，读取第三轮的数据
3. 等等
4. 计算倒数第二轮的数据，读取最后一轮的数据

这时候你会发现：缺少了读取第一轮的数据和计算最后一轮的数据，这两个步骤放在循环外，那就是：

1. 读取第一轮的数据
2. 在 K 维度上循环：计算第 i 轮的数据，读取第 i+1 轮的数据
3. 计算最后一轮的数据

同时用 `buffer_index` 维护当前轮的数据在 Double Buffer 的哪一个 Buffer 上，那么要计算的时候，用 `buffer_index` 作为下标，表示这一轮在用的 Buffer；写入数据的时候，就用 `buffer_index ^ 1` 作为下标，表示下一轮要用到的 Buffer；一轮完成后，交换两个 Buffer，只需要 `buffer_index ^= 1`。

读取第一轮数据到 Shared Memory：

```c
int buffer_index = 0;
// ...
aTile[buffer_index][local_y + j][local_x] =
    a[IDX2C(block_x + local_x, block_y + local_y + j, k)];
// ...
bTile[buffer_index][local_x][local_y + j] =
        b[IDX2C(block_x + local_x, block_y + local_y + j, n)];
```

循环中，读取下一轮的数据到 Shared Memory：

```c
// ...
aTile[buffer_index ^ 1][local_y + j][local_x] =
    a[IDX2C(block_x + local_x, block_y + local_y + j, k)];
// ...
bTile[buffer_index ^ 1][local_x][local_y + j] =
    b[IDX2C(block_x + local_x, block_y + local_y + j, n)];
```

计算时，用当前轮的 Buffer：

```c
sum[xx][yy] += aTile[buffer_index][ii - real_i]
                    [threadIdx.x * BLOCK_SIZE_PER_THREAD + xx] *
                bTile[buffer_index][ii - real_i]
                    [threadIdx.y * BLOCK_SIZE_PER_THREAD + yy];
```

一轮结束后，更新 `buffer_index`：

```c
buffer_index ^= 1;
```

最后一轮计算也是用 `buffer_index` 做下标，和上面一样，这里就不重复了。
