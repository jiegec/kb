# 傅立叶变换

## 傅立叶级数

以 $P$ 为周期的周期函数 $s(x)$ 可以分解为一系列三角函数之和：

$$
s(x) = A_0 + \Sigma_{n=1}^{\infty}(A_n \cos(\frac{2 \pi nx}{P}) + B_n \sin(\frac{2 \pi nx}{P}))
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
s(x) &= A_0 + \Sigma_{n=1}^{\infty}(A_n \cos(\frac{2 \pi nx}{P}) + B_n \sin(\frac{2 \pi nx}{P})) \\
&= A_0 + \Sigma_{n=1}^{\infty}(A_n \frac{e^{\frac{2 \pi nxi}{P}} + e^{\frac{-2 \pi nxi}{P}}}{2} + B_n \frac{e^{\frac{2 \pi nxi}{P}} - e^{\frac{-2 \pi nxi}{P}}}{2i}) \\
&= A_0 + \Sigma_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_n + B_n i}{2} e^{\frac{-2 \pi nxi}{P}})
\end{align}

记 $F_n = \frac{A_n - B_ni}{2}$，把 $A_n$ 和 $B_n$ 的定义延拓到 $n$ 为负数，发现：

\begin{align}
A_{-n} &= \frac{2}{P} \int_P s(x) \cos(\frac{-2 \pi nx}{P}) \mathrm{d} x = A_n \\
B_{-n} &= \frac{2}{P} \int_P s(x) \sin(\frac{-2 \pi nx}{P}) \mathrm{d} x = -B_n
\end{align}

再带入傅立叶展开式，得到

\begin{align}
s(x) &= A_0 + \Sigma_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_n + B_n i}{2} e^{\frac{-2 \pi nxi}{P}}) \\
&= A_0 + \Sigma_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}} + \frac{A_{-n} - B_{-n} i}{2} e^{\frac{2 \pi (-n)xi}{P}}) \\
&= A_0 + \Sigma_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}}) + \Sigma_{n=1}^{\infty}(\frac{A_{-n} - B_{-n} i}{2} e^{\frac{2 \pi (-n)xi}{P}}) \\
&= A_0 + \Sigma_{n=1}^{\infty}((\frac{A_n - B_n i}{2}) e^{\frac{2 \pi nxi}{P}}) + \Sigma_{n=-\infty}^{-1}(\frac{A_n - B_n i}{2} e^{\frac{2 \pi nxi}{P}}) \\
\end{align}

记 $F_0 = A_0$，那么上式可以写成：

$$
s(x) = \Sigma_{n=-\infty}^{\infty} F_n e^{\frac{2 \pi nxi}{P}}
$$

其中 $F_0 = A_0 = \frac{1}{P} \int_P s(x) \mathrm{d} x$，同时：

\begin{align}
F_n &= \frac{A_n - B_ni}{2} = \frac{1}{2}(\frac{2}{P} \int_P s(x) \cos(\frac{2 \pi nx}{P}) \mathrm{d} x - \frac{2}{P} \int_P s(x) \sin(\frac{2 \pi nx}{P})i \mathrm{d} x) \\
&= \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
\end{align}

这个通项公式对 $n=0$ 也成立。因此复指数形式的傅立叶系数为：

\begin{align}
s(x) &= \Sigma_{n=-\infty}^{\infty} F_n e^{\frac{2 \pi nxi}{P}} \\
F_n &= \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
\end{align}

## 傅立叶变换

傅立叶级数：对周期函数的分解。

非周期函数，可以看成是周期无穷大的周期函数，也就是 $P \to \infty$。但是这样计算出来的 $F_n$ 也趋向于零。如果去掉系数 $\frac{1}{P}$，把积分上下限替换为正负 $\infty$，进行代换 $\xi = \frac{n}{P}$，就可以把傅立叶级数变成傅立叶变换：

$$
F_n = \frac{1}{P} \int_P s(x) e^{\frac{-2 \pi nxi}{P}} \mathrm{d} x
$$

Fourier Transform：给定 $f(x)$，傅立叶变换得到 $\hat{f}(\xi)$

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


## 参考

- <https://en.wikipedia.org/wiki/Fourier_transform>
- <https://en.wikipedia.org/wiki/Fourier_series>