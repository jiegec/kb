# Montgomery 模乘

## 背景

在密码学中，经常会涉及到模乘操作：$a * b \bmod N$。朴素的实现方法是，先求出 $a * b$，再对 N 进行除法，那么余数就是模乘的结果。

但由于此时的 $a$ $b$ $N$ 三个数都很大，在计算机上需要用大整数来表示，而大整数的乘法和除法都是需要耗比较多的时间的。如果用 Schönhage–Strassen 算法，计算两个 $n$ 位大整数的乘法需要的时间是 $O(n \log(n) \log(\log(n)))$。

## 定义

Montgomery 模乘是一种提高模乘的性能的方法。具体地，Montgomery 模乘需要一个参数 $R$ 满足 $R$ 和 $N$ 互质，且 $R > N$，那么 Montgomery 模乘实现的是如下计算：

$$
M(a, b) = a * b * R^{-1} \bmod N
$$

## 用途

这看起来很奇怪，为什么要在原来的 $a*b$ 上再多乘一项：这样可以把原来对 $N$ 的除法，转化为对 $R$ 的除法，而如果把 $R$ 选择为二的幂次，硬件上实现 $R$ 的除法就很简单，只需要位运算即可。这样就免去了原来很慢的除法操作。

但是，这种计算方法会引入额外的 $R^{-1}$ 系数，导致计算结果不是想要的 $a * b$。解决方法是，预先计算好 $R^2 \bmod N$，然后先用 Montgomery 模乘把要计算的数都乘以 $R$：

\begin{align}
M(a, R^2) \equiv a * R^2 * R^{-1} \equiv aR \pmod N \\
M(b, R^2) \equiv b * R^2 * R^{-1} \equiv bR \pmod N \\
\end{align}

此时所有数都自带一个 $R$ 的系数，此时再进行 Montgomery 乘，会发现：

$$
M(aR, bR) \equiv (aR) * (bR) * R^{-1} \equiv abR \pmod N
$$

得到的结果是 $ab$ 乘以 $R$ 的形式，那么这个结果可以继续和其他带有 $R$ 系数的值进行运算。当最后运算完成以后，要把结果恢复到原来的值的时候，再和 $1$ 进行 Montgomery 乘，即可得到最终结果

$$
M(abR, 1) \equiv abR * 1 * R^{-1} \equiv ab \bmod N
$$

因此，如果要用 Montgomery 模乘来进行加速，需要经过三个步骤：

1. 第一步，把所有数都进行 Montgomery 模乘，乘以 $R^2 \bmod N$，把所有数都添加上 $R$ 的系数
2. 第二步，按照正常的流程计算，所有值都带有 $R$ 系数，同时所有的模乘都被替换为了更加高效的 Montgomery 模乘
3. 第三步，把结果和 $1$ 进行 Montgomery 模乘，还原为真实值

因此，只要中间计算的过程是大头，初始化和最后的处理时间就可以忽略，可以享受到 Montgomery 模乘带来的性能提升。

## 算法

接下来介绍 Montgomery 的具体算法，看看它如何提高模乘性能。

首先介绍 Montogomery 的 REDC 算法，它的步骤是：

1. 预先计算 $N'$，满足 $NN' \equiv -1 \bmod R$
2. 计算 $T=a*b$
3. 计算 $m=((T \bmod R)N') \bmod R$
4. 计算 $t=(T + mN) / R$
5. 如果 $t \ge N$，那么 $a * b * R^{-1} \bmod N = t - N$
6. 否则 $a * b * R^{-1} \bmod N = t$

可以看到这个过程中只涉及到关于 $R$ 的除法，不涉及到关于 $N$ 的除法。下面推导一下为什么上面的公式是正确的：

首先计算过程中出现了 $t = (T+mN) / R$，为了保证 $t$ 是整数，需要证明 $T+mN$ 可以整除 $R$，也就是要求 $T + mN \equiv 0 \pmod R$：

\begin{align}
T + mN &\equiv T + (((T \bmod R)N') \bmod R)N \pmod R \\
&\equiv T + TN'N \pmod R \\
&\equiv T + T(-1) \pmod R \\
&\equiv 0 \pmod R
\end{align}

说明 $t$ 是整数。其次，需要证明 $a * b * R^{-1} \equiv t \pmod N$：

\begin{align}
t &= (T + mN) / R \\
&\equiv (T + mN) R^{-1} \pmod N \\
&\equiv TR^{-1} + mNR^{-1} \pmod N \\
&\equiv TR^{-1} + 0 \pmod N \\
&\equiv a * b * R^{-1} \pmod N
\end{align}

说明 $t$ 和答案 $a * b * R^{-1}$ 在模 $N$ 意义下相等。

根据 $m$ 的定义，$m$ 的范围是 $[0, R-1]$，同时 $a, b \in [0, N-1]$，且已知 $N < R$，计算 $t$ 的范围：

\begin{align}
t &= (T+mN) / R \\
&= (ab + mN) / R \\
&\le ((N-1)(N-1) + (R-1)N) / R \\
&< (RN + RN) / R \\
&= N + N \\
&= 2N
\end{align}

因此 $t \in [0, 2N-1]$。前面已经证明，$t$ 和答案 $a * b * R^{-1}$ 在模 $N$ 意义下相等。在 $[0, 2N-1]$ 范围内，模 $N$ 意义下相等只有两种可能：相等或者差一个 $N$。所以 REDC 算法的最后一步就是：如果 $t \ge N$，只可能 $t$ 和答案差一个 $N$，所以答案 $a * b * R^{-1} \bmod N = t - N$；否则 $t < N$，此时答案 $a * b * R^{-1} \bmod N = t$。

## 参考资料

- [Wikipedia](https://en.wikipedia.org/wiki/Montgomery_modular_multiplication)