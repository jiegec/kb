# 模逆隐藏数问题（Modular Inverse Hidden Number Problem）

隐藏数问题是一类问题，有一个隐藏数，已知基于这个隐藏数计算出来的一系列数字，反推隐藏数的过程，就是隐藏数问题。

模逆隐藏数问题是一种隐藏数问题，定义如下：

- $p$ 是一个已知素数
- $\alpha$ 是一个需要求解的模 $p$ 的未知整数
- 已知 $n$ 个整数 $x_0, x_2, \cdots, x_{n-1}$，以及对应的 $\mathrm{MSB}_k((\alpha+x_i)^{-1} \bmod p)$，即 $\alpha+x_i$ 在模 $p$ 意义下的逆元的高 $k$ 位

下面介绍针对模逆隐藏数问题的一些解法。

## A Linear Approach

下面介绍论文 [The Modular Inversion Hidden Number Problem](https://www.iacr.org/archive/asiacrypt2001/22480036.pdf) 介绍的一种比较简单的求解方法。

首先，根据已知的信息，可以列出如下的公式：

$b_i = \mathrm{MSB}_k((\alpha+x_i)^{-1} \bmod p) * 2^{l - k}$

其中 $l$ 是素数 $p$ 的位数，此时 $b_i$ 与 $1/(\alpha+x_i)$ 在高 $k$ 位上相等，其余的低位部分不相等，设低位的差值为 $e_i$：

$e_i = ((\alpha+x_i)^{-1} \bmod p) - b_i$

那么 $e_i$ 是有界的：$0 \le e_i < 2^k$。

根据上述定义，可以得到：

$(b_i + e_i)(\alpha + x_i) = 1 \pmod p$

代入 $i=0$，得到

$(b_0 + e_0)(\alpha + x_0) = 1 \pmod p$

为了对 $\alpha$ 消元，两式分别乘上一个系数：

$(b_0 + e_0)(b_i + e_i)(\alpha + x_i) = b_0 + e_0 \pmod p$

$(b_0 + e_0)(b_i + e_i)(\alpha + x_0) = b_i + e_i \pmod p$

两式相减，得到：

$(b_0 + e_0)(b_i + e_i)(x_i - x_0) = b_0 + e_0 - b_i - e_i \pmod p$

展开后，得到：

$(x_i - x_0)e_0e_i + (b_0x_i - b_0x_0 + 0)e_i + (b_ix_i - b_ix_0 - 0)e_0 + b_0b_i(x_0 - x_0) + b_i - b_0 = 0 \pmod p$

于是我们得到了一个针对未知数 $e_0, e_1, \cdots, e_{n-1}$ 的同余方程组，且这里的未知数都比较小：$0 \le e_i < 2^k$。为了方便后面的表示，把上述公式中的系数拆分出来：

$A_i = x_i - x_1$

$B_i = b_1 * x_i - b_1 * x_1 + 1$

$C_i = b_i * x_i - b_i * x_1 - 1$

$D_i = b_1 * b_i * (x_i - x_1) + b_i - b_1$

那么

$A_ie_0e_i + B_ie_i + C_ie_0 + D_i = 0 \pmod p$

接下来，为了求解这些未知数，构建一个格，把上面的 $n-1$ 个同余不等式转化为行向量的整系数线性组合，设

$v=(1, e_0, e_1, \cdots, e_{n-1}, e_0e_1, e_0e_2, \cdots, e_0e_{n-1}, k_1, k_2, \cdots, k_{n-1})$

$$
M=\begin{pmatrix}
D_1 & D_2 & \cdots & D_{n-1} \\
C_1 & C_2 & \cdots & C_{n-1} \\
B_1 & \\
& B_2 \\
& & \ddots \\
& & & B_{n-1} \\
A_1 & \\
& A_2 \\
& & \ddots \\
& & & A_{n-1} \\
p & \\
& p \\
& & \ddots \\
& & & p \\
\end{pmatrix}
$$

那么以 $v$ 为系数组合 $M$ 中的行向量：

$vM=(D_1+e_0C_1+e_1B_1+e_0e_1A_1+k_1p, \cdots, D_{n-1}+e_0C_{n-1}+e_{n-1}B_{n-1}+e_0e_{n-1}A_{n-1}+k_{n-1}p)$

根据已知条件，$A_ie_1e_i + B_ie_i + C_ie_1 + D_i = 0 \pmod p$，可见存在一组 $k_i$ 使得 $vM$ 为零向量。那么如果找到了向量 $v$，就找到了满足要求的 $e_i$。

但是满足要求的 $v$ 很多，怎么求解呢？还是要利用 $e_i$ 是小数的限制，把 $e_i < 2^k$ 的条件，转化为在格中寻找短向量的问题，此时的矩阵变为：

$$
M=\begin{pmatrix}
1 & & & & & & & & D_1 & \cdots & D_{n-1} \\
& 2^{-k} & & & & & & & C_1 & \cdots & C_{n-1} \\
& & 2^{-k} & & & & & & B_1 \\
& & & \ddots & & & & & & \ddots \\
& & & & 2^{-k} & & & & & & B_{n-1} \\
& & & & & 2^{-2k} & & & A_1 \\
& & & & & & 2^{-2k} & & & \ddots \\
& & & & & & & 2^{-2k} & & &A_{n-1} \\
& & & & & & & & p \\
& & & & & & & & & \ddots \\
& & & & & & & & & & p \\
\end{pmatrix}
$$

此时继续用向量 $v$ 对 $M$ 中的行向量进行线性组合：

$vM=(1, 2^{-k}e_0, 2^{-k}e_1, \cdots, 2^{-k}e_{n-1}, 2^{-2k}e_0e_1, \cdots, 2^{-2k}e_0e_{n-1}, D_{n-1}+e_0C_{n-1}+e_{n-1}B_{n-1}+e_0e_{n-1}A_{n-1}+k_{n-1}p)$

同理，存在一组 $k_i$ 使得 $vM$ 的后面 $n-1$ 项全部等于 0，前面的 $2n$ 项都是不大于 $1$ 的数，因此它是一个短向量，可以通过对 $M$ 矩阵进行 [LLL](./lll.md) 格基规约算法求解。

代码实现（代码中按照原论文约定，已知 $n+1$ 个 $x_i$ 包括 $x_0, x_1, \cdots, x_n$）：

```python
from Crypto.Util.number import getPrime
import random


def linear(x: list[int], m: list[int], k: int, p: int) -> int | None:
    """
    Solve MIHNP problem using Linear Approach from
    [The Modular Inversion Hidden Number Problem](https://www.iacr.org/archive/asiacrypt2001/22480036.pdf)

    Args:
        x (list[int]): an array of known x_i
        m (list[int]): an array of known m_i = MSB_k((alpha + x_i)^{-1} mod p)
        k (int): the number of known MSB bits
        p (int): the prime modulo

    Returns:
        the recovered alpha, or None for failure
    """

    # solve MIHNP problem
    # b_i = MSB_k((alpha + x_i)^{-1} \bmod p)
    # e_i = ((alpha + x_i)^{-1} \bmod p) - b_i
    # (b_i + e_i) * (alpha + x_i) = 1 \pmod p
    # (b_0 + e_0) * (alpha + x_0) = 1 \pmod p
    # eliminate alpha:
    # (b_0 + e_0) * (b_i + e_i) * (alpha + x_i) = b_0 + e_0 \pmod p
    # (b_0 + e_0) * (b_i + e_i) * (alpha + x_0) = b_i + e_i \pmod p
    # subtract:
    # (b_0 + e_0) * (b_i + e_i) * (x_i - x_0) = b_0 + e_0 - b_i - e_i \pmod p
    # (x_i - x_0) * e_0 * e_i + (b_0 * x_i - b_0 * x_0 + 1) * e_i +
    #   (b_i * x_i - b_i * x_0 - 1) * e_0 + b_0 * b_i * (x_1 - x_0) + b_i - b_0 = 0 \pmod p
    # e_i are small: less than p >> shift
    # A_i = x_i - x_0
    # B_i = b_0 * x_i - b_0 * x_0 + 1
    # C_i = b_i * x_i - b_i * x_0 - 1
    # D_i = b_0 * b_i * (x_i - x_0) + b_i - b_0
    # then
    # A_i * e_0 * e_i + B_i * e_i + C_i * e_0 + D_i = 0 \pmod p
    # construct lattice for solving bounded coefficients:
    # 1, e_0, e_1, ..., e_n, e_0e_1, e_0e_2, ..., e_0e_n

    try:
        from flint import fmpq_mat, fmpq as Rational

        use_flint = True
    except ImportError:
        from sage.all import Matrix, Rational

        use_flint = False

    # step 1:
    # compute b_i = MSB_k((alpha + x_i)^{-1} mod p) << (n - k)
    # the known MSB bits shifted
    b = [m_i << (p.bit_length() - k) for m_i in m]

    # step 2:
    # compute A_i, B_i, C_i, and D_i
    n = len(x) - 1
    assert len(x) == len(b)
    A = []
    B = []
    C = []
    D = []
    for i in range(1, n + 1):
        A.append(x[i] - x[0])
        B.append(b[0] * x[i] - b[0] * x[0] + 1)
        C.append(b[i] * x[i] - b[i] * x[0] - 1)
        D.append(b[0] * b[i] * (x[i] - x[0]) + b[i] - b[0])

    # step 3:
    # bound for e_i
    bound = p >> k
    # construct lattice
    M: list[list[int | Rational]] = [[0] * (3 * n + 2) for _ in range(3 * n + 2)]
    # row corresponds to 1
    M[0][0] = 1
    # D_1 to D_n
    for i in range(n):
        M[0][2 * n + 2 + i] = D[i]

    # rows correspond to e_i
    for i in range(n + 1):
        M[i + 1][i + 1] = Rational(1) / bound
        if i == 0:
            # C_1 to C_n for e_0
            for j in range(n):
                M[i + 1][2 * n + 2 + j] = C[j]
        else:
            # B_1 to B_n
            M[i + 1][2 * n + 2 + i - 1] = B[i - 1]

    # rows correspond to e_0 * e_i
    for i in range(n):
        M[n + 2 + i][n + 2 + i] = Rational(1) / bound / bound
        # A_1 to A_n
        M[n + 2 + i][2 * n + 2 + i] = A[i]

    # rows for the p term
    for i in range(n):
        M[2 * n + 2 + i][2 * n + 2 + i] = p

    # step 4:
    # use lll to find a small solution
    # the matrix is rational, convert to integer first
    # Q = M * d
    if use_flint:
        Q, d = fmpq_mat(M).numer_denom()
        reduced = Q.lll()
    else:
        Q, d = Matrix(M)._clear_denom()
        reduced = Q.LLL()

    # step 5:
    # find a row that satisfy:
    # v = (1, e_0 / bound, \cdots, e_n / bound, e_0 * e_1 / bound, \cdots, e_0 * e_n / bound, 0, \cdots, 0)
    for i in range(3 * n + 2):
        # convert to actual rational number
        v = [Rational(reduced[i, j]) / d for j in range(3 * n + 2)]
        if (v[0] == 1 or v[0] == -1) and all(
            v[j] == 0 for j in range(2 * n + 2, 3 * n + 2)
        ):
            e_0 = v[0] * v[1] * bound
            # (b_0 + e_0) * (alpha + x_0) = 1 \pmod p
            alpha = (pow(int(b[0] + e_0), -1, p) - x[0]) % p
            # the answer may be incorrect...
            return alpha
    return None


# Modular Inversion Hidden Number Problem
p = getPrime(512)
k = 400
alpha = random.randrange(1, p)
x = []
m = []
for i in range(3):
    # (x_i, MSB_k((alpha + x_i)^{-1} \bmod p))
    x_i = random.randrange(1, p)
    m_i = pow(alpha + x_i, -1, p) >> (p.bit_length() - k)
    x.append(x_i)
    m.append(m_i)
assert linear(x, m, k, p) == alpha
```
