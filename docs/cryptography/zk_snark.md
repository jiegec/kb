# zk-SNARK

zk-SNARK 全名是 zero knowledge Succinct Non-interactive ARgument of Knowledge，是一种零知识证明的协议，其特点是简明（Succinct），也就是需要的信息量比较少；非交互式（Non-interactive），也就是不需要证明者和验证者之间进行多次的交互。

本文基本按照 [Why and How zk-SNARK Works: Definitive Explanation](https://arxiv.org/pdf/1906.07221.pdf) 的思路去探讨 zk-SNARK 的原理和实现，文中的例子也参考了该文章。

## 零知识证明

零知识证明的场景是，现在有一个 Prover 和一个 Verifier，Prover 可以向 Verifier 证明某件事情，但是又不能让 Verifier 知道隐藏的秘密。例如 Prover 要证明自己拥有超过一万块的存款，但是又不希望 Verifier 知道自己具体有多少存款，因此就需要零知识证明。

## 多项式零点证明

### 朴素证明

首先来看一个场景：Prover 知道一个多项式 $p(x)$，也知道它有哪些根，现在假设这些根都是整数，多项式的系数也都是整数。现在 Prover 想要向 Verifier 证明这个多项式有某几个根（不是全部），但又不想告诉 Verifier 这个多项式的所有系数是多少，怎么实现呢？

例如 $p(x)=x^3-3x^2+2x$，这个多项式的所有根是 $0, 1, 2$，想要向 Verifier 证明这个多项式有两个根 $0, 1$，怎么证明呢？

对于 Verifier 来说，公开信息是，有一个未知系数的多项式 $p(x)$，它有两个根 $0, 1$，那么这个多项式一定带有一个因式 $t(x)=(x-1)(x-2)$，也就是说，存在整系数多项式 $h(x)$ 满足：

$$
p(x)=t(x)h(x)=(x-1)(x-2)h(x)
$$

那么带入一个整数 $x$，得到的 $p(x)$ 和 $h(x)$ 都是整数。如果 Prover 想欺骗 Verifier，它的多项式 $p(x)$ 并没有所要证明的根，例如 $p(1) \ne 0$，那么 $x-1$ 就不是 $p(x)$ 的因式，也就没法整除得到一个 $h(x)$。所以就可以设计出这样的一个零知识证明协议：

1. Verifier 随机生成一个整数 $x_0$，发送给 Prover
2. Prover 计算 $p(x_0)$ 和 $h(x_0)$，发送给 Verifier
3. Verifier 计算，如果发现 $p(x_0)=(x_0-1)(x_0-2)h(x_0)$，并且 $p(x_0)$ 和 $h(x_0)$ 都是整数，那么说明没有出错

那么如果 Prover 欺骗了 Verifier，那么计算 $h(x_0)$ 一步的时候就会出问题，因为并不存在整除的 $h(x_0)$。例如 $p(x)=2x^3-3x^2+2x$，想要证明有因式 $t(x)=(x-1)(x-2)$，如果 Verifier 随机出一个 $x=4$，那么 $p(x)=88$，$t(x)=6$，此时就出现了不整除的情况，Prover 证明失败。

不过，还是有一定概率，虽然多项式不整除，但是算出来的数是可以整除的。解决方法就是多次进行上面的流程，每次用一个不同的随机数，随着随机次数增加，证明的可信度就越高，但是代价也就随之上升。

但是 Prover 还是有作弊的方法：随机一个值就当成 $h(x_0)$，然后计算 $p(x_0)=t(x_0)h(x_0)$，再发给 Verifier。此时 Prover 其实并没有一个整除 $t(x)$ 的多项式 $p(x)$。

### 同态加密

既然 Prover 可以伪造计算结果，那么是否可以使用同态加密的方法，让 Prover 可以进行多项式计算，又无法伪造计算结果？

答案是可以，参考 RSA 或者 Diffie-Hellman 的思路，如果想要对某个数做运算，但是又不暴露这个数，那就在素数域上进行指数运算：

$$
E(v) = g^v \pmod n
$$

其中 $v$ 是原始数据，$g$ 是密钥，那么 Verifier 计算出 $E(v)$ 以后，把 $E(v)$ 交给 Prover 去计算。Prover 不知道 $g$ 和 $v$，只能老老实实地去带入多项式进行计算。原来多项式中 $x$ 的加法，变成了 $E(x)$ 的乘法。原来多项式中 $x$ 的数乘，变成了 $E(x)$ 的幂运算。

但是这种方法有一个缺点，就是无法进行多项式的中 $x$ 的乘法：已知 $g^a$ 和 $g^b$，无法计算 $g^{ab}$。也就是说没办法从 $E(x)$ 计算出 $E(x^2)$，只能计算 $E(2x)=E(x)^2$。所以求 $E(x^i)$ 这一步需要由 Verifier 提前完成。

例如 $p(x)=x^3-3x^2+x$，就变成了：

\begin{align}
E(x^3)^1E(x^2)^{-3}E(x)^1 &= (g^{x^3})^1(g^{x^2})^{-3}(g^x)^1 \\
&= g^{x^3}g^{-3x^2}g^x \\
&= g^{x^2-3x^2+x}
\end{align}

可以看到整个过程就是把多项式的运算挪到了指数上面。但是 Prover 看到的只是 $E(x^3), E(x^2), E(x)$，并不知道实际的 $x$ 是多少。

此时的零知识证明协议变成了：

1. Verifier 生成随机数 $s$
2. Verifier 计算 $s$ 的幂次，再带入 $E(v)$：$E(s^i) = g^{s^i}$
3. Verifier 给 Prover 发送 $E(s^0), E(s^1), \ldots, E(s^d)$，其中 $d$ 是多项式 $p(x)$ 的阶数
4. Prover 已知 $p(s)=t(s)h(s)$，计算 $E(p(s)), E(h(s))$，发送给 Verifier
5. Verifier 计算 $E(p(s))$ 和 $E(h(s))^{t(s)}$，判断两者是否相等：$E(h(s))^{t(s)}=(g^{h(s)})^{t(s)}=g^{h(s)t(s)}=g^{p(s)}=E(p(s))$

注意计算 $s$ 的幂次这一步只有 Verifier 才能做，因为 Prover 并不知道 $s$ 的值。

但是这个协议不能保证 Prover 真的用了 $E(s^i)$ 计算出结果。所以接下来要考虑的是，如何保证 Prover 真的拿 $E(s^i)$ 去带入到 $E(p(s))$ 的计算中去，并且把结果发给 Verifier。

### Knowledge-of-Exponent Assumption

对于上面问题的一种解决方法是，让 Prover 可以证明它确实对一个数做了乘法（对应上面的模幂操作）。思路是这样的：

1. Verifier 有一个数 $a$，需要验证 Prover 对 $a$ 进行了模幂操作，并且只进行了模幂操作。
2. Verifier 生成一个随机数 $\alpha$，计算 $a' = a^{\alpha} \pmod n$，把 $a$ 和 $a'$ 发送给 Prover
3. Prover 要对 $a$ 进行模幂操作，次数是 $c$，那么需要计算 $b=a^c \pmod n$ 以及 $b' = (a')^c \pmod n$，把 $b$ 和 $b'$ 发送给 Verifier
4. Verifier 验证：$b^{\alpha} = b' \pmod n$

如果验证正确，说明 Prover 对两个数 $a$ 和 $a'$ 求了同样次数的幂（对应多项式里，乘了同一个整系数）。如果对这两个数进行其他操作，那么就不能保证验证通过。回顾上一小节的最后一部分：Prover 想要作弊的话，需要构造一个 $E(h(s))$ 以及对应的 $E(p(s))$，如果对 $E(h(s))$ 或者 $E(p(s))$ 进行上述处理，那么 $E(h(s))$ 和 $E(p(s))$ 就只能是对 $E(s^i)$ 求 $c$ 次方计算出来的值，这正好就是一个多项式的求值过程。

换句话说，给定 $1, s, s^2, \ldots, s^d$ 这些值，要求只能用这些数进行加法和数乘操作，那么结果一定是某个多项式在 $s$ 处的取值。

因此此时的完整零知识证明协议变成了：

1. Verifier 生成随机数 $s$
2. Verifier 计算 $s$ 的幂次，再带入 $E(v)$：$E(s^i) = g^{s^i}$
3. Verifier 生成随机数 $\alpha$，带入 $E(s^i)^{\alpha} = g^{\alpha{}s^{i}}$
3. Verifier 给 Prover 发送 $E(s^0), E(s^1), \ldots, E(s^d)$ 和 $E(s^0)^{\alpha}, E(s^1)^{\alpha}, \ldots, E(s^d)^{\alpha}$，其中 $d$ 是多项式 $p(x)$ 的阶数
4. Prover 已知 $p(s)=t(s)h(s)$，计算 $E(p(s)), E(\alpha{}p(s)), E(h(s))$，发送给 Verifier
5. Verifier 判断 $E(p(s))=E(h(s))^{t(s)}$ 以及 $E(p(s))^{\alpha}=E(\alpha{}p(s))$

这样就证明了两点：

1. $E(p(s))=E(h(s))^{t(s)}$ 证明了 $t(x)$ 是 $p(x)$ 的因式
2. $E(p(s))^{\alpha}=E(\alpha{}p(s))$ 证明了 $p(x)$ 是一个多项式

需要注明的是，这里并没有保证 Prover 每次用同一个多项式 $p(x)$，只是证明了 Prover 知道一个整除 $t(x)$ 的多项式，并且次数不超过 $d$。

### 零知识

更进一步，如果想要让 Verifier 对多项式实现零知识，很简单：Prover 返回的三个值，再求一个随机数 $\delta$ 次方，相当于多项式的系数全部乘以 $\delta$，那么结果依然满足 Verifier 要判断的两个等式，但是 Verifier 就没办法推断多项式具体的系数了。

那么零知识证明协议变成了：

1. Verifier 生成随机数 $s$ 和 $\alpha$
2. Verifier 计算 $s$ 的幂次，再带入 $E(v)$：$E(s^i) = g^{s^i}$
3. Verifier 计算 $E(s^i)^{\alpha} = g^{\alpha{}s^{i}}$
3. Verifier 给 Prover 发送 $E(s^0), E(s^1), \ldots, E(s^d)$ 和 $E(s^0)^{\alpha}, E(s^1)^{\alpha}, \ldots, E(s^d)^{\alpha}$，其中 $d$ 是多项式 $p(x)$ 的阶数
4. Prover 已知 $p(s)=t(s)h(s)$，计算 $E(p(s)), E(\alpha{}p(s)), E(h(s))$
5. Prover 生成随机数 $\delta$，计算 $E(\delta{}p(s)), E(\delta{}\alpha{}p(s)), E(\delta{}h(s))$，发送给 Verifier
5. Verifier 判断 $E(\delta{}p(s))=E(\delta{}h(s))^{t(s)}$ 以及 $E(\delta{}p(s))^{\alpha}=E(\delta{}\alpha{}p(s))$

### 非交互式

上面的零知识证明协议是交互式的，需要 Verifier 发送一些数据，Prover 再回复一些数据。更理想的是非交互式的证明，Prover 直接生成一个证明，Verifier 随时可以验证，不需要交互。

为了解决交互的问题，可以让 Prover 做自己的 Verifier，生成一个证明，然后把证明的结果公开。那么这时候需要有两点性质：Prover 自己做自己的 Verifier 的时候，不能作弊；实际的 Verifier 看到证明的结果的时候，可以验证这个证明是合法的。

为了保证第一点，需要保证 Prover 不能操纵 Verifier 的随机参数 $s$ 和 $\alpha$。一个思路是让多个潜在的 Verifier 共同给出一组随机参数，另一个思路是使用一些不可逆的函数，例如密码学哈希函数，输入多项式的一些信息，把输出的哈希视为随机数，这样保证了随机性，又无法指定随机参数。

为了保证第二点，需要保证所有人都可以完成验证的那一步，回顾前面的协议，最后需要验证的是：

1. $E(\delta{}p(s))=E(\delta{}h(s))^{t(s)}$
2. $E(\delta{}p(s))^{\alpha}=E(\delta{}\alpha{}p(s))$

但是这个验证过程需要知道 $t(s)$ 和 $\alpha$ 的值，但如果是采用前面所说的随机生成的方法，那么这两个值是不能公开的，否则 Prover 就可以针对它去生成数据。解决方法是，设计一个 “乘法”（下面用 $\times$ 表示），使得验证过程不需要原始的 $t(s)$ 和 $\alpha$，而是需要 $E(t(s))$ 和 $E(\alpha)$：

1. $E(\delta{}p(s))=E(\delta{}h(s))^{t(s)}$ 对应 $g^{\delta{}p(s)} \times g = g^{t(s)} \times g^{\delta{}h(s)}$
2. $E(\delta{}p(s))^{\alpha}=E(\delta{}\alpha{}p(s))$ 对应 $g^{\delta{}p(s)} \times g^{\alpha} = g^{\delta{}\alpha{}p(s)} \times g$

那么验证的时候，只需要 $E(t(s))=g^{t(s)}$，$E(\alpha)=g^{\alpha}$ 和 $g$，就可以验证结果是否正确，不需要知道 $s$ 和 $\alpha$ 的具体值。

这个乘法是一个双线性的映射，叫做 pairing。

那么到这里就可以给出一个完整的非交互式的多项式零点证明：

1. 已知多项式 $t(x)$ 和次数 $d$
2. 初始化阶段
    1. 生成随机数 $s$ 和 $\alpha$
    2. 计算 $g^{s^i}, g^{\alpha{}s^i}, g^{\alpha}, g^{t(s)}$
    3. 记其中的 $g^{s^i}, g^{\alpha{}s^i}$ 为 Proving Key，用于 Prover 生成 Proof
    4. 记其中的 $g^{\alpha}, g^{t(s)}$ 为 Verification Key，用于 Verifier 验证 Proof
3. 证明阶段
    1. 计算 $h(x) = p(x) / t(x)$
    2. 用 $g^{s^i}$ 计算 $g^{p(s)}$ 和 $g^{h(s)}$
    3. 用 $g^{\alpha{}s^i}$ 计算 $g^{\alpha{}p(s)}$
    4. 生成随机数 $\delta$
    5. 计算 $g^{\delta{}p(s)}, g^{\delta{}h(s)}, g^{\delta{}\alpha{}p(s)}$
4. 验证阶段
    1. 检查 $g^{\delta{}\alpha{}p(s)} \times g = g^{\delta{}p(s)} \times g^{\alpha}$
    2. 检查 $g^{\delta{}p(s)} \times g = g^{t(s)} \times g^{\delta{}h(s)}$

## 通用零知识证明

上面的零知识证明只适用于多项式的零点问题，那么对于更广泛的场景，例如前面提到的银行存款的问题，如何实现呢？

思路是把问题转化为前面的多项式零点问题，具体内容 TODO。

## 参考资料

- [Why and How zk-SNARK Works: Definitive Explanation](https://arxiv.org/pdf/1906.07221.pdf)