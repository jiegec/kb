# 近似公约数问题（Approximate Common Divisor Problem）

给定某个未知整数 $p$ 的整数倍数，要计算 $p$，只需要求这些整数倍数的最大公约数。但如果已知数并不是精确的 $p$ 的整数倍数，而是包含了一个较小的误差项，这个问题就称为近似公约数问题（Approximate Common Divisor Problem）。形式化地定义近似公约数问题：

- 已知 $t$ 个整数 $x_1, x_2, \ldots, x_t$ 满足 $x_i = pq_i + r_i$，其中 $q_i, r_i$ 是未知整数
- 其中 $q_i \ge 0$，$r_i$ 满足 $\mathrm{abs}(r_i) < 2^{\rho}$，$\rho$ 是一个已知参数

特别地，如果其中一个已知数是 $p$ 的精确整数倍，即 $r_1 = 0$，使得 $x_1 = pq_1$，这个问题就称为部分近似公约数问题（Partial Approximate Common Divisor Problem）。

下面介绍针对近似公约数问题的求解方法。以下方法有时候会求出来一些合法的近似解，例如求出来的 $p$ 实际上是 $p+1$、$2p$ 或者 $2p \pm 1$ 一类的。如果已知 $p$ 是素数或者知道 $p$ 的位数，可以对求出来的 $p$ 做一些后处理来提高准确率。

## 同时丢番图逼近方法（Simultaneous Diophantine Approximation，缩写 SDA）

同时丢番图逼近算法的思路是：既然 $r_i$ 是比较小的数，那么 $x_i/x_1 \approx q_i/q_1$ 成立。已知 $x_i$，可以计算出 $x_i/x_1$，通过丢番图逼近，可以找到两个整数 $q_i/q_1$ 使得 $x_i/x_1 \approx q_i/q_1$ 成立。但是，丢番图逼近有无穷多种解，我们希望找到一种丢番图逼近，使得求出来的 $q_i$ 就是原来用于计算 $x_i = pq_i + r_i$ 中所使用的 $q_i$。

为了实现这一点，同时对所有的 $t-1$ 个 $x_i/x_1, i \in {2, 3, \ldots, t}$ 同时进行丢番图逼近，并且要求它们的分母相等。具体做法是，构建以如下矩阵的行向量为基向量的格：

$$
B=\begin{pmatrix}
2^{\rho+1} & x_2 & x_3 & \cdots & x_t \\
& -x_1 & & & \\
& & -x_1 & & \\
& & & \ddots & \\
& & & & -x_1 \\
\end{pmatrix}
$$

以 $(q_1, q_2, \cdots, q_t)$ 为系数组合上述格中的基向量，可以得到向量 $v$：

$v = (q_1, q_2, \cdots, q_t)B = (q_12^{\rho+1}, q_1x_2-q_2x_2, \cdots, q_1x_t-q_tx_1)$

因为 $x_i/x_1 \approx q_i/q_1$ 成立，所以 $q_1x_i - q_ix_1 \approx 0$，因此 $v$ 是一个比较短的向量。通过 [LLL 格基规约算法](./lll.md)，我们可以找到 $B$ 对应的格中比较短的一个向量，那么在满足一定条件的情况下（详细推导见[论文](https://eprint.iacr.org/2016/215.pdf)），通过 LLL 得到的最短的向量，可能就是上面的 $v$。通过 $v$，可以求出 $q_1$，进而 $r_1 = x_1 \bmod q_1$, $p = (x_1 - r_1) / q_1$。

代码实现：

```python
from sage.all import *
from Crypto.Util.number import *
import random

p = getPrime(512)
rho = 50
x = [random.randrange(0, p) * p + random.randrange(0, 2**rho) for i in range(5)]


def sda_attack(x, rho):
    # Simultaneous Diophantine approximation approach (SDA)

    # create matrix
    # 2^{rho+1},  x_2,  x_3, ...,  x_t
    #         0, -x_1, ...
    #         0,    0, -x_1, ...
    #         ...
    #         0,    0,       ..., -x_1
    t = len(x)
    matrix = [[0] * t for _ in range(t)]
    matrix[0][0] = 2 ** (rho + 1)
    for i in range(t - 1):
        matrix[0][i + 1] = x[i + 1]
        matrix[i + 1][i + 1] = -x[0]

    B = Matrix(matrix)
    reduced = B.LLL()
    v = reduced[0]

    # recover q_1
    q_1 = v[0] // (2 ** (rho + 1))
    r_1 = x[0] % q_1

    p = abs((x[0] - r_1) // q_1)
    return p


# It may fail sometimes
res = sda_attack(x, rho)
print(f"Got result:", res != None)
print(f"Result correct:", res == p)
```

## 正交方法（Orthogonal，缩写 OL）

另一种求解近似公约数问题的方法是正交方法，它的思路是：找到 $t-1$ 个线性无关且与 $(q_1, q_2, \ldots, q_t)$ 正交的向量，那么 $(q_1, q_2, \ldots, q_t)$ 就是以这 $t-1$ 个线性无关的向量组成的线性子空间的核空间中的一个基向量。

为了找到这样一组向量，构建以如下矩阵的行向量为基向量的格：

$$
B=\begin{pmatrix}
x_1 & 2^{\rho} & & & & \\
x_2 & & 2^{\rho} & & & \\
x_3 & & & 2^{\rho} & & \\
\vdots & & & & \ddots & \\
x_t & & & & & 2^{\rho} \\
\end{pmatrix}
$$

在格中的向量 $v=(v_1, v_2, \ldots, v_{t+1})$ 是由一系列整系数 $(u_1, u_2, \ldots, u_t)$ 线性组合基向量而来：

$v = (u_1, u_2, \ldots, u_t)B = (\Sigma_{i=1}^{i=t} u_ix_i, u_1 2^{\rho}, u_2 2^{\rho}, \ldots, u_t 2^{\rho})$

如果你注意力惊人，可以观察到下列等式：

$v_1 - \Sigma_{i=1}^{i=t} v_{i+1}r_i/2^{\rho} = \Sigma_{i=1}^{i=t} u_ix_i - \Sigma_{i=1}^{i=t} u_ir_i = \Sigma_{i=1}^{i=t}u_i(x_i-r_i)$

由于 $x_i = pq_i + r_i$，所以 $x_i - r_i = 0 \pmod p$ 成立，同理 $\Sigma_{i=1}^{i=t}u_i(x_i-r_i) = 0 \pmod p$。而如果你注意力特别惊人，还可以发现当 $v$ 向量比较短的时候，$\mathrm{abs}(v_1 - \Sigma_{i=1}^{i=t} v_{i+1}r_i/2^{\rho}) < p/2$。

那么此时只有一个解：$\Sigma_{i=1}^{i=t}u_i(x_i-r_i) = 0$，那么 $\Sigma_{i=1}^{i=t}u_ipq_i = 0$，由于 $p \ne 0$，所以 $\Sigma_{i=1}^{i=t}u_iq_i = 0$。也就是说，向量 $(u_1, u_2, \ldots, u_t)$ 和向量 $(q_1, q_2, \ldots, q_t)$ 是正交的。

每当我们找到一个比较短的向量 $v$，就找到了一组向量 $(u_1, u_2, \ldots, u_t)$ 和 $(q_1, q_2, \ldots, q_t)$ 是正交的。

而对矩阵 $B$ 进行 [LLL 格基规约算法](./lll.md)，满足一定条件下（详细推导见[论文](https://eprint.iacr.org/2016/215.pdf)）是可以找到 $t-1$ 个这样的满足要求的短向量 $v$，也就找到了 $t-1$ 个和 $(q_1, q_2, \ldots, q_t)$ 正交的向量，并且 LLL 保证了这些向量还是线性无关的。在核空间中找到一组整系数的基，就得到了 $q_i$，剩下就是 $r_i = x_i \bmod q_i, p = (x_i - r_i) / q_i$，完成求解。

代码实现：

```python
from sage.all import *
from Crypto.Util.number import *
import random

p = getPrime(512)
rho = 50
x = [random.randrange(0, p) * p + random.randrange(0, 2**rho) for i in range(5)]


def ol_attack(x, rho):
    # Orthogonal based approach

    # create matrix
    # R = 2^rho
    # x_1, R, 0, ..., 0
    # x_2, 0, R, ..., 0
    # ...
    # x_t, 0, 0, ..., R
    R = 2**rho
    size = len(x)
    matrix = [[0] * (size + 1) for _ in range(size)]
    for i in range(size):
        matrix[i][0] = x[i]
        matrix[i][i + 1] = R

    B = Matrix(matrix)
    # transform * B == reduced
    reduced, transform = B.LLL(transformation=True)
    assert transform * B == reduced

    # now sum(u_i * q_i) == 0 for short enough vector
    # the u_i vectors are saved in the transformation matrix

    # find kernel of the space spanned by t-1 u-vectors
    M = transform[: size - 1][:]
    # q is the basis of the kernel
    q = M.right_kernel()
    q_1 = q.basis()[0][0]

    # r_1 = x_1 mod q_1
    r_1 = x[0] % q_1
    # p = (x_1 - r_1) / q_1
    p = (x[0] - r_1) // q_1

    return p


res = ol_attack(x, rho)
print(f"Got result:", res != None)
print(f"Result correct:", res == p)
```

## 参考文献

- [Algorithms for the Approximate Common Divisor Problem](https://eprint.iacr.org/2016/215.pdf)
