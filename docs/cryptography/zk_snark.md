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

但是 Prover 还是有作弊的方法：它可以不用固定的多项式 $p(x)$ 来计算，而是每次 Verifier 给出一个 $x_0$，就构造出一个新的满足要求的 $p(x)$，不再是原来要证明的那个多项式了。

### 同态加密

既然 Prover 可以伪造计算结果，那么是否可以使用同态加密的方法，让 Prover 可以进行多项式计算，又无法伪造计算结果？

答案是可以，参考 RSA 或者 Diffie-Hellman 的思路，如果想要对某个数做运算，但是又不暴露这个数，那就在素数域上进行指数运算：

$$
E(v) = g^v \pmod n
$$

其中 $v$ 是原始数据，$g$ 是密钥，那么 Verifier 计算出 $E(v)$ 以后，把 $E(v)$ 交给 Prover 去计算。Prover 不知道 $g$ 和 $v$，只能老老实实地去带入多项式进行计算。原来多项式中 $x$ 的加法，变成了 $E(x)$ 的乘法。原来多项式中 $x$ 的数乘，变成了 $E(x)$ 的幂运算。例如 $p(x)=x^3-3x^2+x$，就变成了：

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

但是 Prover 还是有作弊的可能性，例如告诉 Verifier $E(p(s))=E(h(s))=1$，那么无论 $s$ 是什么，都会验证通过。或者取一个整数 $r$，告诉 Verifier $E(p(s))=(g^{t(s)})^r$（$t(x)$ 多项式是公开信息，并且知道 $E(s^i)$），$E(h(s))=g^r$，那么 Verifier 验证的时候，会发现验证通过。

这个作弊的方法核心的点就是，虽然 Prover 并不知道 $s$ 是什么，但是它可以拿 $E(s^i)$ 去做别的计算，而不是按照多项式 $p(x)$ 去计算。所以接下来要考虑的是，如何保证 Prover 真的拿 $E(s^i)$ 去带入到 $E(p(s))$ 的计算中去，并且把结果发给 Verifier。

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

## 参考资料

- [Why and How zk-SNARK Works: Definitive Explanation](https://arxiv.org/pdf/1906.07221.pdf)