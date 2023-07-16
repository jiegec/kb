# LLL 格基规约算法

LLL（Lenstra–Lenstra–Lovász）格基规约算法实现了格（lattice）的一组基（basis）的规约，规约后得到了新的一组基，并且这些基向量的大小满足不等式。

## 格

首先定义什么是格（lattice）：

给定 $\mathbb{R}^n$ 上的 $n$ 个向量 $\{b_1, b_2, \cdots b_n\}$：

\begin{align}
b_1 &= (a_{11}, a_{12}, \cdots, a_{1n}) \\
b_2 &= (a_{21}, a_{22}, \cdots, a_{2n}) \\
&\vdots \\
b_n &= (a_{n1}, a_{n2}, \cdots, a_{nn}) \\
\end{align}

将这些基向量 以**整系数**线性组合得到的空间，就是格：

$$
L = \{\sum_i^d r_ib_i \vert r_i \in \mathbb{Z}\}
$$

例如 $\mathbb{Z}^2$ 就可以认为是以 $(1, 0), (0, 1)$ 为基构成的格。

## 格基规约

格规约要实现的事情是，对于给定的格 L，即已知：

$$
L = \{\sum_i^d r_ib_i \vert r_i \in \mathbb{Z}\}
$$

计算出一组新的一组基 $\{b_1', b_2', \cdots, b_n'\}$，满足：

$$
L = \{\sum_i^d r_ib_i' \vert r_i \in \mathbb{Z}\}
$$

也就是两组基在构成格 L 上是等价的。

但是规约的同时，也会给新的一组基添加约束，从而得到“更好”的一组基。

## LLL 格基规约算法

LLL 就是一个格基规约算法，对于 $L \subset \mathbb{Z}^n$ 的一组基，进行规约后得到的基 $\{b_1, b_2, \cdots b_n\}$ 满足以下的性质：

$$
|b_1| \le 2^{(n-1)/4} |\mathrm{det}(L)|^{1/n}
$$

这意味着规约后得到的第一个基的大小是有界的，公式中 $\mathrm{det}(L)$ 指的是把基向量拼接成的矩形的特征值。

## 应用

### 已知整数多项式的根，求多项式

应用 LLL 可以求解这样一个问题：已知有一个 $n$ 次整数多项式以及它的零点 $r$，现在要求整数多项式的各项系数的多少。

例子：已知 $r=1.6180339$ 是一个 2 次整数多项式 $ax^2 + bx + c$ 的零点，即 $ar^2 + br + c=0$，求 $a$ $b$ $c$。

为了利用 LLL 格基规约算法，需要根据题目条件构造出一组基 $\{b_1, b_2, b_3\}$：

\begin{align}
b_1 &= (1, 0, Xr^2) \\
b_2 &= (0, 1, Xr) \\
b_3 &= (0, 0, X) \\
\end{align}

其中 $X$ 是一个整数，因为 LLL 算法要求 $L \subset \mathbb{Z}^n$，所以上式中的 $Xr^2$ 和 $Xr$ 两项都需要取整，这里为了下面公式推导的方便，暂时省略了。

假如对上面的基进行 LLL 格基规约算法，应该会得到一组新的基 $\{b_1', b_2', b_3'\}$，满足：

$$
|b_1'| \le 2^{(n-1)/4} |\mathrm{det}(L)|^{1/n}
$$

其中：

$$
L = (b_1^T b_2^T b_3^T) = \begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
Xr^2 & Xr & X
\end{pmatrix}
$$

计算行列式可得 $\mathrm{det}(L)=X$，代入 $n=3$ 到上式，可得 $|b_1'| \le 2^{1/2} |X|^{1/3}$。

又因为两组基是等价的，因此 $b_1'$ 也可以用 $\{b_1, b_2, b_3\}$ 线性组合得到，且系数 $A$ $B$ $C$ 是整数：

\begin{align}
b_1' &= Ab_1 + Bb_2 + Cb_3 \\
&= (A, 0, AXr^2) + (0, B, BXr) + (0, 0, CX) \\
&= (A, 0, XAr^2) + (0, B, XBr) + (0, 0, XC) \\
&= (A, B, X(Ar^2 + Br + C))
\end{align}

因此 $|b_1'| = \sqrt{A^2+B^2+(X(Ar^2+Br+C))^2} \le 2^{1/2} X^{1/3}$，由于 $X$ 是自己选定的任意整数，当 X 取足够大时，只有当 $Ar^2+Br+C \approx 0$ 时，上式才能满足。这样就找到了以 $r$ 为零点的整系数多项式。

此时 $A$ 和 $B$ 可以直接从得到的 $b_1'$ 基向量中取出，$C$ 可以通过 $C=-Ar^2-Br$ 计算得出。

实际上使用 LLL 算法的时候，基的个数可以少于维数，因此对于上面的问题，可以构造出如下一组基：

\begin{align}
b_1 &= (1, 0, 0, Xr^2) \\
b_2 &= (0, 1, 0, Xr) \\
b_3 &= (0, 0, 1, X) \\
\end{align}

此时经过 LLL 规约后得到的 $b_1=(A, B, C)$，也就是直接得到了多项式的所有系数。

用 sage 实现上面的算法：

```sage
# parameters
r = 1.618
degree = 2
X = 10000

# build lattice matrix
matrix = []

for i in range(degree + 1):
    matrix.append(
        [int(i == j) for j in range(degree + 1)] + [round(X * (r ** (degree - i)))]
    )

# compute first basis vector after LLL reduction
m = Matrix(ZZ, matrix)
ans = m.LLL()[0]

# recover polynomial
expr = 0
x = var("x")
for i in range(degree + 1):
    expr = expr + ans[i] * (x ** (degree - i))

# prints "-x^2 + x + 1"
print(expr)
```
