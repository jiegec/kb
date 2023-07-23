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

### REDC

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

## 大整数 Montgomery 模乘

实际在计算机上运行 Montgomery 算法的时候，由于这些数都很大，因此为了表示大整数，需要用固定位数的整数数组来表示，例如用多个 64 位整数来表示一个大整数。此时，把大整数运算拆成多个 64 位整数的运算，然后把大整数的运算和 Montgomery 模乘结合在一起，得到更高性能的 Montgomery 模乘。

论文 [Analyzing and Comparing Montgomery Multiplication Algorithms](https://www.microsoft.com/en-us/research/wp-content/uploads/1996/01/j37acmon.pdf) 分析了几种混合了大整数运算和 Montgomery 模乘的算法。下面讲解论文中提到的部分算法。

在下面的讨论中，假设机器整数的宽度是 $w$ 位，例如 $w=64$ 表示用 64 位整数进行运算，此时 $R=2^{sw}$，也就是说，$R$ 等于 $s$ 个 $w$ 位整数可以表示的最大值加一，那么除以 $R$ 相当于舍弃最低的 $s$ 个 $w$ 位整数。同时也意味着，$a$ $b$ $N$ 都可以用 $s$ 个 $w$ 位整数表示。

### Separated Operand Scanning

第一种方法是 Separated Operand Scanning 方法（同时也是 [Wikipedia](https://en.wikipedia.org/wiki/Montgomery_modular_multiplication#Montgomery_arithmetic_on_multiprecision_integers) 中提到的 MultiPrecisionREDC 算法），它的步骤是：

第一步：按照传统方式进行大整数乘法，计算出 $T = a*b$：

```python
# t = a * b
for i=0 to s-1
    C := 0
    for j=0 to s-1
        (C, S) := t[i+j] + a[j]*b[i] + C
        t[i+j] := S
    t[i+s] := C
```

得到的结果放在 $t$ 数组中。

第二步，求 $t = (T + mN) / R$，此时 $T$ 已经计算出来，接下来首先要计算出 $m=((T \bmod R)N') \bmod R$，在这里 $\bmod R$ 就是取大数的最低 $s$ 个 $w$ 位整数，因此可以简化大整数乘法为：

```python
# m = ((T % R) * N') % R
for i=0 to s-1
    C := 0
    for j=0 to s-i-1
        (C, S) := m[i+j] + t[i]*n'[j] + C
        m[i+j] := S
```

接下来求大整数 $m$ 乘以大整数 $N$ 的积，求积的同时把结果累加到 $T$ 上。伪代码：


```python
# t += m * N
for i=0 to s-1
    C := 0
    for j=0 to s-1
        (C, S) := t[i+j] + m[i]*n[j] + C
        t[i+j] := S
    ADD (t[i+s], C)
```

这里的 ADD 函数指的是大整数加法运算里面，求和后不断进位直到不再进位为止的函数，这里就不展开了。

在这里有一个重要的优化：实际上，不需要把 $m$ 整个大整数计算出来，而是可以直接求 $T + mN$：回忆一下，最初计算 $T + mN$ 的目的是让结果整除 $R$，现在把 $T + mN$ 的计算拆成 $s$ 个小步：第 $i$ 步让结果整除 $2^{(i+1)w}$：

第一步：$T + m_1N \equiv 0 \pmod{2^w}$，此时 $m_1 = T * N' \bmod 2^w$，对应在代码上，就是 `m_1 = t[0] * n'[0]`，舍去溢出的部分。

第二步：$T + m_1N + m_22^wN \equiv 0 \pmod{2^{2w}}$，此时 $m_2 * 2^w = (T + m_1N) * N' \bmod 2^{2w}$，此时会惊喜地发现，由于 $T + m_1N$ 是 $2^w$ 的倍数，因此计算 $(T + m_1N) * N'$ 的时候，$T + m_1N$ 的低 $w$ 位全是 0，也意味着实际上 $(T + m_1N) * N'$ 就是拿 $(T + m_1N) \bmod 2^{2w}$ 的高 $w$ 位乘以 $N'$ 的低 $w$ 位，再左移 $w$ 位，结果等于 $m_2 * 2 ^ w$，所以 $m_2$ 就等于 $((T+m_1N) \bmod 2^{2w}) / 2^w * (N' \bmod 2^w)$，对应在代码上，就是 `m_2 = t[1] * n'[0]`。

这个过程可以一直继续下去，每一步的 `m_i` 都可以用 `m_i = t[i] * n'[0]` 计算。因此不再需要先求 $m$，再求 $T + mN$，而是可以同时计算：

```python
# t += m * N
for i=0 to s-1
    C := 0
    # W = 2^w
    m := t[i] * n'[0] mod W
    for j=0 to s-1
        (C, S) := t[i+j] + m*n[j] + C
        t[i+j] := S
    ADD (t[i+s], C)
```

计算出 $T + mN$ 以后，最后就是除以 $R$ 了，实际上也非常简单，直接去掉 `t` 数组的低 $s$ 项即可：

```python
# u = t / R
for i=0 to s
    u[j] := t[j+s]
```

最后再用大整数减法和比较，使得结果 $u$ 落在 $[0, N-1]$ 的范围内，这里就不单独列代码了。把上面的代码合在一起，就得到最终完整 Separated Operand Scanning 算法的伪代码：

```python
# t = a * b
for i=0 to s-1
    C := 0
    for j=0 to s-1
        (C, S) := t[i+j] + a[j]*b[i] + C
        t[i+j] := S
    t[i+s] := C

# t += m * N
for i=0 to s-1
    C := 0
    # W = 2^w
    m := t[i] * n'[0] mod W
    for j=0 to s-1
        (C, S) := t[i+j] + m*n[j] + C
        t[i+j] := S
    ADD (t[i+s], C)

# u = t / R
for i=0 to s
    u[j] := t[j+s]

# return u or u - N
B := 0
for i=0 to s-1
    (B,D) := u[i] - n[i] - B
    t[i] := D
(B,D) := u[s] - B
t[s] := D
if B=0 then
    return t[0], t[1], ... , t[s-1]
else
    return u[0], u[1], ... , u[s-1]
```

### Coarse Integrated Operand Scanning

第二种算法 Coarse Integrated Operand Scanning 是在 Separated Operand Scanning 的基础上，把 $a*b$ 和后面的计算过程交错进行，放在同一个大循环中，因为后面使用到 `t` 数组的时候，只会依赖已经计算出来的部分。同时，每次循环结束的时候就把整个 `t` 数组右移一次，因此原来的 `t[i]` 就会变成 `t[0]`，`t[i+j]` 变成 `t[j]`。

```python
for i=0 to s-1

    # t = a * b
    C := 0
    for j=0 to s-1
        (C, S) := t[j] + a[j]*b[i] + C
        t[j] := S
    (C, S) := t[s] + C
    t[s] := S
    t[s+1] := C

    # t += m * N
    C := 0
    # W = 2^w
    m := t[0] * n'[0] mod W
    for j=0 to s-1
        (C, S) := t[j] + m*n[j] + C
        t[j] := S
    (C, S) := t[s] + C
    t[s] := S
    t[s+1] := t[s+1] + C

    # t /= W
    for j=0 to s
        t[j] := t[j+1]

# return t or t - N
# save as above, omitted
```

每次循环都右移一次，那么循环 $s$ 次就是除以 $R$，因此原来的 $u = t / R$ 一步就不需要了。同时，$t$ 数组需要的存储空间也缩小了，因为不需要保存完整的 $a*b$ 的结果。更进一步，还可以把 `t += m * N` 和移位两步合并在一起进行：

```python
for i=0 to s-1

    # t = a * b
    C := 0
    for j=0 to s-1
        (C, S) := t[j] + a[j]*b[i] + C
        t[j] := S
    (C, S) := t[s] + C
    t[s] := S
    t[s+1] := C

    # t = (t + m * N) / W
    # W = 2^w
    m := t[0] * n'[0] mod W
    (C, S) := t[0] + m*n[0]
    for j=1 to s-1
        (C, S) := t[j] + m*n[j] + C
        t[j-1] := S
    (C, S) := t[s] + C
    t[s-1] := S
    t[s] := t[s+1] + C

# return t or t - N
# save as above, omitted
```

这样就得到了最终的 Coarse Integrated Operand Scanning 算法，下面是一段用 Rust 语言编写的实现：

```rust
// https://github.com/jiegec/rust-monty-comparison/blob/6c941d5c95d37dd9ee8f12aa57df577e0f2b623b/src/lib.rs#L89-L139
let mut res = [0u32; WORDS + 2];
// for i=0 to s-1
for i in 0..WORDS {
    // C := 0
    let mut c = 0;
    // for j = 0 to s-1
    for j in 0..WORDS {
        // (C, S) := t[j] + a[j] * b[i] + C
        let mut cs = res[j] as u64;
        cs += self.num[j] as u64 * other.num[i] as u64;
        cs += c as u64;
        c = (cs >> 32) as u32;
        // t[j] := S
        res[j] = cs as u32;
    }
    // (C, S) := t[s] + C
    let cs = res[WORDS] as u64 + c as u64;
    // t[s] := S
    res[WORDS] = cs as u32;
    // t[s+1] := C
    res[WORDS + 1] = (cs >> 32) as u32;

    // m := t[0]*n'[0] mod W
    let m: u32 = (res[0] as u64 * N_INV as u64) as u32;
    // (C, S) := t[0] + m*n[0]
    let mut cs = res[0] as u64 + m as u64 * N[0] as u64;
    c = (cs >> 32) as u32;
    // for j=1 to s-1
    for j in 1..WORDS {
        // (C, S) := t[j] + m*n[j] + C
        cs = res[j] as u64;
        cs += m as u64 * N[j] as u64;
        cs += c as u64;
        c = (cs >> 32) as u32;
        // t[j-1] := S
        res[j - 1] = cs as u32;
    }
    // (C, S) := t[s] + C
    cs = res[WORDS] as u64 + c as u64;
    // t[s-1] := S
    res[WORDS - 1] = cs as u32;
    // t[s] := t[s+1] + C
    res[WORDS] = res[WORDS + 1] + (cs >> 32) as u32;
}

let res_scalar = MontyBigNum::from_u32_slice(&res[0..WORDS]);
let mut res_scalar_sub = res_scalar;
let borrow = bignum_sub(&mut res_scalar_sub, &MODULO);
if res[WORDS] != 0 || borrow == 0 {
    res_scalar_sub
} else {
    res_scalar
}
```

OpenSSL 也在函数 [bn_mul_mont](https://github.com/openssl/openssl/blob/9c8d04dbec03172d6ffe4eaa38ea4b1ac2741f26/crypto/bn/bn_asm.c#L852) 中实现了这个算法。

## 常数时间

在 Montgomery 模乘的最后一步，需要把计算结果和 $N$ 比较，然后进行减法，这一步会出现一个条件分支，可能会导致运行时间和数据相关，成为一个潜在的测信道攻击的点。因此为了解决这个问题，可以有如下的解决方法（参考论文 [Montgomery Arithmetic from a Software Perspective](https://eprint.iacr.org/2017/1057.pdf)）：

既然条件分支是为了和 $N$ 比较，那如果去掉这个限制，也就是说让结果在 $[0, 2N-1]$ 的范围而不是 $[0, N-1]$，看看能否继续把结果传给下一次的 Montgomery 模乘。首先要求 $R > 2N$，因为输入参数的范围是模 $2N$，而不是模 $N$；其次，重新考虑 $t = (T+mN) / R$ 的放缩：

\begin{align}
t &= (T+mN) / R \\
&= (ab + mN) / R \\
&\le ((2N-1)(2N-1) + (R-1)N) / R
\end{align}

此时为了让 $t < 2N$ 成立，需要额外添加条件 $R > 4N$，此时：

\begin{align}
t &= (T+mN) / R \\
&= (ab + mN) / R \\
&\le ((2N-1)(2N-1) + (R-1)N) / R \\
&< ((\frac{1}{2}R)(2N) + RN) / R \\
&= N + N \\
&= 2N
\end{align}

也就是说，如果规定 $R > 4N$，那么最后一步可以不和 $N$ 比较，把结果保留在 $[0, 2N-1]$ 的范围，继续进行后续的 Montgomery 模乘。但是这样有一个问题，就是在 RSA 场景下，通常 $N$ 的位数就是二的幂次，例如 $N$ 是一个 2048 位的大整数，为了满足 $R > 4N$，不得不多存一个整数，相应地 Montgomery 模乘计算中的循环次数也要增加。

另一种思路是，既然和 $N$ 比较比较费时间，而且需要条件分支，那就改成和 $R$ 比较，让结果保持在 $[0, R-1]$ 的区间内，而不是原来的 $[0, N-1]$ 区间。此时重新考虑 $t = (T+mN) / R$ 的放缩：

\begin{align}
t &= (T+mN) / R \\
&= (ab + mN) / R \\
&\le ((R-1)(R-1) + (R-1)N) / R \\
&< (R^2 + RN) / R \\
&= R + N
\end{align}

也就是说，结果会在 $[0, R+N-1]$ 的范围内，此时最后一步变成和 $R$ 比较大小，如果比 $R$ 大，就减去 $N$。和 $R$ 比较大小很简单，直接看最高位是否为 $0$ 即可。这种方法并没有消除条件分支，但是把条件分支的开销降到了单次整数比较。如果要保证常数时间的话，可以在结果小于 $R$ 时，减去零。

## 逆推

下面尝试逆推出 Montgomery 是如何设计 Montgomery 模乘算法的。

首先目标是求 $t = a * b \bmod N$，也就是要找到一个 $m$ 满足 $t = a * b + mN \in [0, N-1]$，但是求 $m$ 的这一步需要计算除法。既然 $N$ 不方便计算除法，那就尝试换一个除数 $R$，把问题转化为求 $m$ 使得 $t = (a * b + mN) / R \in [0, N-1]$，此时 $t = a * b * R^{-1} \bmod N$，但是不要紧，只要能高效地计算 $a * b * R^{-1} \bmod N$，就可以高效地计算 $a * b \bmod N$。

于是下面的问题就来到了怎么找到 $m$ 使得 $t = (a * b + mN) / R \in [0, N-1]$。把 $R$ 挪到等式左边，得到

$$
t * R = a * b + m * N
$$

由于 $t$ 未知，所以等式左边的值未知，为了消除未知数，等式两边同时对 $R$ 取余：

$$
0 \equiv a * b + m * N \pmod R
$$

于是 $m \equiv - a * b * N^{-1} \pmod R$，其中 $-N^{-1} \bmod R$ 的部分可以预先计算好。但是这里依然是在模 $R$ 的意义下相等，$m$ 有多种可能。

很幸运的是，前面已经推导过，当 $m = ((a * b) \bmod R * -N^{-1}) \bmod R$ 时，恰好可以保证最终结果 $t \in [0, 2N-1]$，此时只需要简单判断一下 $t$ 和 $N$ 的大小关系，就可以求出答案。这样就把 Montgomery 模乘的流程逆推出来了。

所以两点观察很重要：一是换一个容易做除法的除数 $R$，想到要设 $t = (a * b + mN) / R$；二是即使让模乘加上一个系数 $R^{-1}$，也不妨碍它的使用。


## 参考资料

- [Wikipedia](https://en.wikipedia.org/wiki/Montgomery_modular_multiplication)
- [Analyzing and Comparing Montgomery Multiplication Algorithms](https://www.microsoft.com/en-us/research/wp-content/uploads/1996/01/j37acmon.pdf)
