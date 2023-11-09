# ECDSA

<iframe src="https://player.bilibili.com/player.html?aid=573470219&bvid=BV16z4y177ym&cid=1197576892&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="100%" height="500"> </iframe>

ECDSA 是一个基于椭圆曲线的签名算法，使用时需要确定一个椭圆曲线，以及它的 base point $G$，且 $G$ 的阶是素数 $n$。

本文主要参考了 [ECDSA - Wikipedia](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)。

## 生成 key pair

生成 key pair 的时候，私钥是整数 $d_A \in [1, n-1]$，那么公钥就是圆锥曲线上一点 $Q_A = d_A \times G$，这里 $\times$ 表示整数与圆锥曲线上一点的乘法。

## 签名

签名的时候，对于给定的消息 $m$，签名流程如下：

1. 计算哈希：$e = \mathrm{HASH}(m)$，例如用 SHA 系列的哈希算法
2. 考虑到 $e$ 的位数可能比 $n$ 的位数更多，取 $e$ 的高位，使得位数和 $n$ 一致，得到的结果记为 $z$
3. 生成一个密码学安全的随机数 $k \in [1, n-1]$
4. 计算 $k \times G$，取它的 X 坐标为 $x_1$
5. 计算 $r = x_1 \bmod n$
6. 计算 $s = k^{-1}(z + r d_A) \bmod n$
7. 如果 $r$ 或者 $s$ 等于 0，取新的 $k$ 再重试
8. 得到的 ECDSA 签名就是 $(r, s)$ 两个数

## 验证

验证签名的时候，已知 $r, s, m, Q_A$，按照下面的流程进行：

1. 前两步和计算签名的算法一致，求哈希和截断后得到 $z$
2. 计算 $u_1 = zs^{-1} \bmod n, u_2 = rs^{-1} \bmod n$
3. 计算 $u_1 \times G + u_2 \times Q_A$，取它的 X 坐标为 $x_2$
4. 如果 $r \equiv x_2 \pmod n$，则签名合法

上面的过程忽略了一些边界情况的检查，详细版本见 Wikipedia。

下面进行验算：

\begin{align}
& u_1 \times G + u_2 \times Q_A \\
&= zs^{-1} \times G + rs^{-1} \times Q_A \\
&= zs^{-1} \times G + rs^{-1}d_A \times G \\
&= (zs^{-1} + rs^{-1}d_A) \times G \\
&= (z+rd_A)s^{-1} \times G \\
&= (z+rd_A)k(z+rd_A)^{-1} \times G \\
&= k \times G
\end{align}

等式左边的 X 坐标等于等式右边的 X 坐标，等价于 $r \equiv x_2 \pmod n$，验算没问题。

## 公钥恢复

ECDSA 支持公钥恢复算法，已知 $r, s, m$，恢复 $Q_A$。首先进行推导：

\begin{align}
Q_A &= d_A \times G \\
s &= k^{-1}(z + rd_A) \bmod n \\
sk &= z + rd_A \bmod n \\
sk \times G &= (z + rd_A) \times G \\
rd_A \times G &= (sk - z) \times G \\
Q_A &= d_A \times G = r^{-1}(sk-z) \times G \\
Q_A &= r^{-1}(s(k \times G) - z \times G)
\end{align}

上式中 $r, s$ 已知，$z$ 可以从 $m$ 通过哈希计算得出，$k \times G$ 的 X 坐标 $x_1$ 满足 $r = x_1 \bmod n$，因此恢复过程就是：

1. 在椭圆曲线上找到 X 坐标模 $n$ 等于 $r$ 的点，这个点就是 $k \times G$
2. 按照计算哈希的前两步，从 $m$ 计算出 $z$
3. 按照上述公式，计算出 $Q_A$

但是实际上第一步没有这么简单：首先同一个 X 坐标对应椭圆曲线上的两个点，其次 $r$ 和 $x_1$ 只是同余关系，可能二者之间差了一个倍数。因此实际在 BTC 或者 ETH 里使用的时候，还额外附加了一个参数 recid，范围是 0 到 3，对应 Y 坐标是正还是负，$r$ 和 $x_1$ 之间差 0 还是 $n$：

```c
// Source: https://github.com/ethereum/go-ethereum/blob/e1fe6bc8469c626afaa86b1dfb819737e980a574/crypto/secp256k1/libsecp256k1/src/modules/recovery/main_impl.h#L104-L112
if (recid & 2) {
    if (secp256k1_fe_cmp_var(&fx, &secp256k1_ecdsa_const_p_minus_order) >= 0) {
        return 0;
    }
    secp256k1_fe_add(&fx, &secp256k1_ecdsa_const_order_as_fe);
}
if (!secp256k1_ge_set_xo_var(&x, &fx, recid & 1)) {
    return 0;
}
```

参考：[Crypto Magic: Recovering Alice’s Public Key From An ECDSA Signature](https://medium.com/asecuritysite-when-bob-met-alice/crypto-magic-recovering-alices-public-key-from-an-ecdsa-signature-e7193df8df6e) 和 [Can We Recover The Public Key from an ECDSA Signature?](https://medium.com/asecuritysite-when-bob-met-alice/can-we-recover-the-public-key-from-an-ecdsa-signature-7af4b56a8a0f)

## DSA 公钥恢复

如果在 DSA 算法上尝试上面的公钥恢复流程，就会遇到困难：

\begin{align}
g &= h^{(p-1)/q} \bmod p \\
y &= g^x \bmod p \\
r &= (g ^ k \bmod p) \bmod q \\
s &= (k^{-1}(H(m) + xr)) \bmod q \\
sk &\equiv H(m) + xr \bmod q \\
xr &\equiv sk - H(m) \bmod q \\
x &\equiv r^{-1}(sk - H(m)) \bmod q \\
y &= g^x \bmod p = g^{r^{-1}(sk - H(m))+nq} \bmod p, n \in Z \\
y &= g^{r^{-1}sk}g^{-r^{-1}H(m)+nq} \bmod p
\end{align}

此时会发现无法从 $r$ 推断出 $g^k \bmod p$ 的值，中间差了 $q$ 的整数倍。后面的 $g^{nq} \bmod p$ 也无法计算。

更加完整的讨论可以见 [Can we recover public key from DSA signatures as we can from ECDSA?](https://crypto.stackexchange.com/questions/107260/can-we-recover-public-key-from-dsa-signatures-as-we-can-from-ecdsa)。

## Nonce Reuse Attack

在生成 ECDSA 签名的时候，注意不能用固定的 nonce（$k$），否则会被攻击。假如攻击者用一对 ECDSA key pair 对不同的两个消息 $m_1$ 和 $m_2$ 分别做了一次签名，并且采用了相同的 nonce，那么：

两次签名的 nonce $k$ 相等，因此 $x_1$ 相等，$r$ 也相等，只有 $s$ 不同：

\begin{align}
s_1 &= k^{-1}(z_1 + rd_A) \bmod n \\
s_2 &= k^{-1}(z_2 + rd_A) \bmod n
\end{align}

签名是公开信息，也就是说 $r$、$s_1$ 和 $s_2$ 是攻击者已知的。此外消息 $m_1$ 和 $m_2$ 也是已知的，所以攻击者可以求出 $z_1$ 和 $z_2$。现在尝试求解 $d_A$：

\begin{align}
s_1 &= k^{-1}(z_1 + rd_A) \bmod n \\
s_2 &= k^{-1}(z_2 + rd_A) \bmod n \\
k &= s_1^{-1}(z_1 + rd_A) \bmod n \\
k &= s_2^{-1}(z_2 + rd_A) \bmod n \\
s_1^{-1}(z_1 + rd_A) &= s_2^{-1}(z_2 + rd_A) \bmod n \\
(s_1^{-1} - s_2^{-1})rd_A &= s_2^{-1}z_2 - s_1^{-1}z_1 \bmod n \\
d_A &= r^{-1}(s_1^{-1} - s_2^{-1})^{-1}(s_2^{-1}z_2 - s_1^{-1}z_1) \bmod n
\end{align}

这样就把私钥 $d_A$ 求了出来。
