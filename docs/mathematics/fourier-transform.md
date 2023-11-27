# 傅立叶变换

## 傅立叶级数

以 $P$ 为周期的周期函数 $s(x)$ 可以分解为一系列三角函数之和：

$$
s(x) = A_0 + \sum_{n=1}^{\infty}(A_n \cos(\frac{2 \pi nx}{P}) + B_n \sin(\frac{2 \pi nx}{P}))
$$

为了计算系数 $A_n$ 和 $B_n$，在一个周期上计算如下积分：

\begin{align}
A_0 &= \frac{1}{P} \int_P s(x) \mathrm{d} x \\
A_n &= \frac{2}{P} \int_P s(x) \cos(\frac{2 \pi nx}{P}) \mathrm{d} x \\
B_n &= \frac{2}{P} \int_P s(x) \sin(\frac{2 \pi nx}{P}) \mathrm{d} x
\end{align}

实际上是在计算 $s(x)$ 在由 $\cos(\frac{2 \pi nx}{P})$ 和 $\sin(\frac{2 \pi nx}{P})$ 组成的正交函数集上的分解，两个函数的内积定义为在一个周期上两个函数的乘积的积分。

需要注意 $A_0$ 项的系数中分子是 1，而不是 2。这个系数可以用内积来计算出来。

根据欧拉公式：

$$
e^{ix} = \cos(x) + i \sin(x)
$$

可得

\begin{align}
\cos(x) &= \frac{e^{ix} + e^{-ix}}{2} \\
\sin(x) &= \frac{e^{ix} - e^{-ix}}{2i} \\
\end{align}

带入到傅立叶级数展开式：

\begin{align}
s(x) &= A_0 + \sum_{n=1}^{\infty}(A_n \cos(\frac{2 \pi nx}{P}) + B_n \sin(\frac{2 \pi nx}{P})) \\
&= A_0 + \sum_{n=1}^{\infty}(A_n \frac{e^{\frac{2 \pi nxi}{P}} + e^{\frac{-2 \pi nxi}{P}}}{2} + B_n \frac{e^{\frac{2 \pi nxi}{P}} - e^{\frac{-2 \pi nxi}{P}}}{2i}) \\
&= A_0 + \sum_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_n + B_n i}{2} e^{\frac{-2 \pi nxi}{P}})
\end{align}

记 $F_n = \frac{A_n - B_ni}{2}$，把 $A_n$ 和 $B_n$ 的定义延拓到 $n$ 为负数，发现：

\begin{align}
A_{-n} &= \frac{2}{P} \int_P s(x) \cos(\frac{-2 \pi nx}{P}) \mathrm{d} x = A_n \\
B_{-n} &= \frac{2}{P} \int_P s(x) \sin(\frac{-2 \pi nx}{P}) \mathrm{d} x = -B_n
\end{align}

再带入傅立叶展开式，得到

\begin{align}
s(x) &= A_0 + \sum_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_n + B_n i}{2} e^{\frac{-2 \pi nxi}{P}}) \\
&= A_0 + \sum_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_{-n} - B_{-n} i}{2} e^{\frac{2 \pi (-n)xi}{P}}) \\
&= A_0 + \sum_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}}) + \sum_{n=1}^{\infty}(\frac{A_{-n} - B_{-n} i}{2} e^{\frac{2 \pi (-n)xi}{P}}) \\
&= A_0 + \sum_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}}) + \sum_{n=-\infty}^{-1}(\frac{A_n - B_n i}{2} e^{\frac{2 \pi nxi}{P}}) \\
\end{align}

记 $F_0 = A_0$，那么上式可以写成：

$$
s(x) = \sum_{n=-\infty}^{\infty} F_n e^{\frac{2 \pi nxi}{P}}
$$

其中 $F_0 = A_0 = \frac{1}{P} \int_P s(x) \mathrm{d} x$，同时：

\begin{align}
F_n &= \frac{A_n - B_ni}{2} = \frac{1}{2}(\frac{2}{P} \int_P s(x) \cos(\frac{2 \pi nx}{P}) \mathrm{d} x - \frac{2}{P} \int_P s(x) \sin(\frac{2 \pi nx}{P})i \mathrm{d} x) \\
&= \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
\end{align}

这个通项公式对 $n=0$ 也成立。因此复指数形式的傅立叶系数为：

\begin{align}
s(x) &= \sum_{n=-\infty}^{\infty} F_n e^{\frac{2 \pi nxi}{P}} \\
F_n &= \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
\end{align}

## 傅立叶变换

傅立叶级数：对周期函数的分解。

非周期函数，可以看成是周期无穷大的周期函数，也就是 $P \to \infty$。但是这样计算出来的 $F_n$ 也趋向于零。如果去掉系数 $\frac{1}{P}$，把积分上下限替换为正负 $\infty$，进行代换 $\xi = \frac{n}{P}$，就可以把傅立叶级数：

$$
F_n = \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
$$

变成傅立叶变换 Fourier Transform：给定 $f(x)$，傅立叶变换得到 $\hat{f}(\xi)$

$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i \xi x} \mathrm{d}x
$$

Inverse Fourier Transform：给定 $\hat{f}(\xi)$，傅立叶逆变换得到 $f(x)$

$$
f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{2\pi i \xi x} \mathrm{d}\xi
$$

另一种傅立叶变换的表示形式，把 $2 \pi \xi$ 换元为 $\omega$：

$$
\hat{f}(\omega) = \int_{-\infty}^{\infty} f(x) e^{- i \omega x} \mathrm{d}x
$$

$$
f(x) = \frac{1}{2\pi} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i \omega x} \mathrm{d}\omega
$$

注意逆变换多了一个系数 $\frac{1}{2\pi}$。如果希望保持对称性，可以在正变换的时候也乘一个系数 $\frac{1}{\sqrt{2\pi}}$：

$$
\hat{f}(\omega) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} f(x) e^{- i \omega x} \mathrm{d}x
$$

$$
f(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i \omega x} \mathrm{d}\omega
$$

## 傅立叶级数和傅立叶变换的对比

傅立叶级数：

- 针对周期函数
- 离散的频率
- 得到频率分量上的数值

傅立叶变换：

- 针对非周期函数
- 连续的频率
- 得到频率分量上的密度

## 采样

理想采样是在时域上，以固定的采样间隔 $T$ 对信号进行采样，相当于是给信号乘以一个[冲激串函数（Dirac comb）](https://en.wikipedia.org/wiki/Dirac_comb) $p(t)$。在时域上乘法，等价于频域上做卷积。冲激串函数 $p(t)$ 在频域上是 $P(\omega)$，它依然是一个冲激串：

$$
p(t) = \sum_{n = -\infty}^{\infty} \delta(t - nT)
$$

$$
P(\omega) = \frac{2 \pi}{T} \sum_{n = -\infty}^{\infty} \delta(\omega - \frac{2 \pi}{T} n)
$$

注：根据傅立叶变换的形式不同，这里的系数可能不完全一样，例如可能没有 $2 \pi$ 的因子。

因此理想采样在频域上相当于是对信号的频域以 $2 \pi / T$ 为周期进行周期性延拓。

周期性延拓的时候，可能会出现频谱的混叠现象。如果发生了混叠，那么就无法从采样后的信号恢复出原始信号。为了不发生混叠，需要保证采样间隔满足 Nyquist 采样定理。

如果没有发生混叠，可以采用理想低通滤波器，去掉周期性延拓出来的多余频谱，恢复出采样前的原始信号。

## 离散时间傅立叶变换

离散时间傅立叶变换（DTFT）是傅立叶变换的离散时间版本：时域上是离散的。频域依然是连续的。离散时间傅立叶变换是傅立叶变换的特殊形式，它把一个离散的无限长序列 $x[n]$，对应到单位时间周期的冲激串函数的幅度上，得到 $f(t) = \sum_{n=-\infty}^{\infty} x[n] \delta(t-n)$，再进行傅立叶变换：

\begin{align}
\hat{f}(\omega) &= \int_{-\infty}^{\infty} f(t) e^{- i \omega t} \mathrm{d}t \\
&= \int_{-\infty}^{\infty} (\sum_{n=-\infty}^{\infty} x[n] \delta(t-n)) e^{- i \omega t} \mathrm{d}t \\
&= \sum_{n = - \infty}^{\infty} x[n] e^{-i \omega n}
\end{align}

为了简化，直接要求冲激串函数的周期为 1，这样就把采样率归一化了。

如果限定离散序列 $x[n]$ 为有限长度，那么相当于对时域乘以一个矩形窗。假设有限的长度为 $L$，也就是 $n$ 的取值范围从所有整数缩小到 $\{0, 1, \cdots, L-1\}$，那么有限长度离散序列的离散时间傅立叶变换为：

$$
X_{2 \pi}(\omega) = \sum_{n = 0}^{L-1} x[n]e^{-i \omega n}
$$

## 离散傅立叶变换

离散傅立叶变换（DFT）是在离散时间傅立叶变换的基础上，在频谱上 $[0, 2 \pi)$ 频率范围内均匀地取 $N$ 个点的值。也就是说，把上式的 $\omega$ 替换为 $\frac{2 \pi k}{N}$，就得到了离散傅立叶变换的公式：

$$
X_k = \sum_{n = 0}^{L-1} x_ne^{-i \frac{2 \pi k}{N} n}
$$

通常会让 $N$（频域上点的个数）等于 $L$（时域上点的个数）。


## 参考

- <https://en.wikipedia.org/wiki/Fourier_transform>
- <https://en.wikipedia.org/wiki/Fourier_series>
- <https://en.wikipedia.org/wiki/Sampling_(signal_processing)>
- <https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem>