# 椭圆曲线

## Weierstrass 定义

椭圆曲线的一种定义是，在 $\mathbb{R}^2$ 上的曲线，曲线上每一点 $(x, y)$ 满足：

$$
y^2 = x^3 + ax + b
$$

要求 $4a^3 + 27b^2 \ne 0$，这种形式叫做 Weierstrass form。

## 运算

在椭圆曲线上，可以定义点之间的加法运算，满足：

- 单位元 $O$ 为无穷远点
- 对于曲线上两点 $P$ 和 $Q$，取经过 $P$ 和 $Q$ 的直线，这条直线与椭圆曲线相交于最多三个点（因为方程是三次的），其中两个点是 $P$ 和 $Q$，如果第三个点存在且不和 $P$、$Q$ 重合，记第三个点为 $R$，那么满足 $P + Q + R = O$，也就是 $P + Q = -R$
- 对一点 $R=(x_P, y_P)$，其相反数 $-R=(x_P, -y_P)$，也就是沿 X 轴对称的点

下面来推导一下 $P$ $Q$ $R$ 三点间的坐标关系。设 $P=(x_P, y_P), Q=(x_Q, y_Q), R=(x_R, y_R)$，首先假设 $x_P \ne x_Q$，那么经过 $P$ $Q$ 的直线的方程为

$$
y = kx + b
$$

带入椭圆曲线方程，得到

\begin{align}
(kx + b)^2 &= x^3 + ax + b \\
k^2x^2 + 2kbx + b^2 &= x^3 + ax + b \\
x^3 - k^2x^2 - 2kbx + ax + b - b^2 &= 0
\end{align}

因为 $P$ $Q$ $R$ 是曲线与直线相交的三点，上式等价于

$$
(x-x_P)(x-x_Q)(x-x_R) = x^3-(x_P+x_Q+x_R)x^2+(x_Px_Q+x_Qx_R+x_Rx_P)x-x_Px_Qx_R
$$

两个方程的系数相同，则

\begin{align}
k^2 &= x_P + x_Q + x_R \\
x_R &= k^2 - x_P - x_Q \\
k &= \frac{y_P - y_Q}{x_P - x_Q} \\
x_R &= (\frac{y_P - y_Q}{x_P - x_Q})^2 - x_P - x_Q \\
y_R &= y_P + k(x_R - x_P)
\end{align}

即 $R=((\frac{y_P - y_Q}{x_P - x_Q})^2 - x_P - x_Q, y_P + \frac{y_P - y_Q}{x_P - x_Q}((\frac{y_P - y_Q}{x_P - x_Q})^2 - x_P - x_Q - x_P))$。由于 $P + Q = -R$，所以椭圆曲线上点的加法在 $x_P \ne x_Q$ 时运算结果为

$$
(x_P, y_P) + (x_Q, y_Q) = ((\frac{y_P - y_Q}{x_P - x_Q})^2 - x_P - x_Q, - y_P - \frac{y_P - y_Q}{x_P - x_Q}((\frac{y_P - y_Q}{x_P - x_Q})^2 - x_P - x_Q - x_P))
$$

如果 $x_P = x_Q$，那么分情况讨论：

1. 如果 $y_P = y_Q$，也就是 $P + Q$，此时 $PQ$ 连的直线是椭圆曲线在 $P$ 点的切线，切线上的斜率的计算方法是，对椭圆曲线方程两侧对 $x$ 求导，得到 $2y \frac{\mathrm{d}y}{\mathrm{d}x} = 3x^2+a$，因此斜率 $k = \frac{3x_P^2+a}{2y_P}$，剩下的计算过程和上面一样。
2. 如果 $y_P \ne y_Q$，根据椭圆曲线的对称性，那么 $y_P = - y_Q$，此时 $P + Q = O$。

这部分推导参考了 [Wikipedia](https://en.wikipedia.org/wiki/Elliptic_curve)。

除了加法以外，还可以定义数乘：整数 $n$ 乘以点 $P$，实际上就是求 $n$ 个 $P$ 的和。

由于运算过程只用到了加减法、乘法和除法，所以坐标也可以扩展到其他的域上。

## 齐次坐标

上面的计算过程会涉及到除法，为了避免除法运算，可以使用齐次坐标来表示：`[X : Y : Z]` 对应的点就是 `(X/Z, Y/Z)`。有了齐次坐标以后，就可以把计算过程中的除法变成对 Z 的乘法，从而避免了除法运算。

## 有限域上的椭圆曲线

从上面的观察可以发现，在计算两点间的加法运算的时候，对 X Y 坐标的计算只涉及到了加减乘除。因此，可以把椭圆曲线的坐标换到其他域上，而不局限于上面使用的 $\mathbb{R}$。例如在密码学中，通常会使用 $F_p$ 素数域或者 $GF(2^m)$。例如取素数域 $F_p$ 上的椭圆曲线，那么点的坐标满足

$$
y^2 \equiv x^3 + ax + b \pmod p
$$

例如在椭圆曲线密码学中常用的 secp192r1 曲线，就是在素数域上定义的椭圆曲线：

\begin{align}
p &= 6277101735386680763835789423207666416083908700390324961279 \\
a &= p - 3 \\
b &= 2455155546008943817740293915197451784769108058161191238065
\end{align}

此时除法运算定义为在素数域上乘以乘法逆元的运算。

## Montgomery curve

在椭圆曲线密码学中，有时候会用 Montgomery curve 来描述椭圆曲线，而不是上面的 Weierstrass form。它的形式如下：

$$
By^2 = x^3 + Ax^2 + x
$$

满足 $B(A^2-4) \ne 0$。

例如 [Curve25519](https://en.wikipedia.org/wiki/Curve25519) 就是一个在素数域上的 Montgomery curve：

\begin{align}
y^2 &\equiv x^3 + 486662 x^2 + x \pmod p \\
p &= 2^{255} - 19
\end{align}

使用 Montgomery curve 的好处是能够实现更快的运算。

Montgomery 曲线可以转换为 Weierstrass 曲线，下面给出转换过程：

考虑到 Montgomery 相比 Weierstrass 左侧多了一个 $B$ 的因子，采用变量代换把它消除，

\begin{align}
By^2 &= x^3 + Ax^2 + x \\
u &= \frac{x}{B} \\
v &= \frac{y}{B} \\
B(vB)^2 &= (uB)^3 + A(uB)^2 + uB \\
v^2 &= u^3 + \frac{A}{B}u^2 + \frac{1}{B^2}u
\end{align}

此时距离 Weierstrass form 就差等式右边的 $u$ 的次数，目标是 $x^3 + ax + b$，现在是 $x^3 + ax^2 + x$，因此要把 $x^2$ 项消掉，设 $u = t - \frac{A}{3B}$，则

\begin{align}
v^2 &= u^3 + \frac{A}{B}u^2 + \frac{1}{B^2}u \\
u &= t - \frac{A}{3B} \\
v^2 &= (t - \frac{A}{3B})^3 + \frac{A}{B}(t - \frac{A}{3B})^2 + \frac{1}{B^2}(t - \frac{A}{3B}) \\
v^2 &= t^3 + \frac{3-A^2}{3B^2}t + \frac{2A^3-9A}{27B^3}
\end{align}

此时 $(v, t)$ 就是符合 Weierstrass form 椭圆曲线上的一点。

这部分推导参考了 [Wikipedia](https://en.wikipedia.org/wiki/Montgomery_curve#Equivalence_with_Weierstrass_curves)。

## Twisted Edwards curve

第三种椭圆曲线的描述方法是 Twisted Edwards curve，定义如下：

$$
ax^2 + y^2 = 1 + dx^2y^2
$$

Twisted Edwards curve 的点的加法如下：

$$
(x_1, y_1) + (x_2, y_2) = (\frac{x_1y_2+y_1x_2}{1+dx_1x_2y_1y_2},\frac{y_1y_2-ax_1x_2}{1-dx_1x_2y_1y_2})
$$

点可以用齐次坐标表示：$(X, Y, Z, T)$ 对应 $(x,y)$ 满足 $x=X/Z, y=Y/Z, x*y=T/Z$。

Twisted Edwards curve 可以用在 [EdDSA](https://en.wikipedia.org/wiki/EdDSA) 签名算法中。
