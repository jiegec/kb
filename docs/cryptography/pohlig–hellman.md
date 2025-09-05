# Pohlig-Hellman 算法

参考：[Wikipedi](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)

Pohlig-Hellman 算法是一种在有限交换群中高效实现离散对数的方法。例如，要求解 $x$ 使得：$2^x = 22 \pmod{43}$，如何高效地进行计算？

方法一：枚举 $x$，找到满足要求的值为止，可以得到 $x=13$

方法二：用 [Baby-step Giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step) 方法，为了找到 $x$ 满足 $a^x = b \pmod p$，设 $m = \lceil \sqrt{p-1} \rceil$，那么一定可以找到 $i, j \in [0, m)$ 使得 $x = i + mj$，那就枚举所有的 $i \in [0, m)$，计算出 $a^i \pmod p$ 并保存下来，放到一个集合当中，然后枚举 $b$，计算 $b(a^{-m})^j \pmod p$ 是否出现在前述集合中，如果有，那么就有 $i, j$ 使得 $a^i = b(a^{-m})^j \pmod p$ 即 $a^{i+mj}=a^x=b \pmod p$

方法三：使用 Pohlig-Hellman 算法，它的思路是，把问题分解成子群上的问题，例如上述 $2^x = 22 \pmod {43}$ 可以分解，这个群的阶是 $42 = 2 * 3 * 7$，可以拆出来阶为 2、3 和 7 的子群。

具体地说，如果 $2^x = 22 \pmod {43}$ 成立，那么一定有 $(2^{21})^x = 22^{21} \pmod {43}$，此时 $2^{21}$ 的阶是 2，意味着 $x_1 = x \bmod 2$ 的值决定了这个等式是否成立；类似地，$x_2 = x \bmod 3$ 的值决定了 $(2^{14})^x = 22^{14} \pmod {43}$ 是否成立，$x_3 = x \bmod 7$ 的值决定了 $(2^{6}) ^ x = 22^{6} \pmod {43}$ 是否成立。那么 $x_1, x_2, x_3$ 就可以用前面的方法二l来解，把一个阶很大的群中的离散对数问题，变成多个阶比较小的群的离散对数问题。

求解 $(2^{21})^x = 22^{21} \pmod {43}$ 可得 $x_1 = x \bmod 2 = 1$，类似可得 $x_2 = x \bmod 3 = 1, x_3 = x \bmod 7 = 6$，那么为了求 $x$，最后用中国剩余定理即可。
