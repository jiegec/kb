# Many Facet Rasch Model

定义：

$$
\log(\frac{P_{nijk}}{P_{nij(k-1)}}) = B_n - D_i - C_j - F_k
$$

- $P_{nijk}$ 是考官 j 针对题目 i 给考生 n 打 k 分的概率
- $P_{nij(k-1)}$ 是考官 j 针对题目 i 给考生 n 打 k-1 分的概率
- $B_n$ 是考生 n 的能力
- $D_i$ 是题目 i 的难度
- $C_j$ 是考官 j 的严格程度
- $F_k$ 是评分从 k-1 增加到 k 的难度

完全交叉：J 个考官，对 N 个考生做的 I 个题目，给出了 $J*N*I$ 个打分，打分范围是 0 到 K。目标：求解上述各数。

## JMLE

JMLE 求解算法：初始化各参数，得到一系列的 $P_{nijk}$，根据实际的打分，计算出似然概率，然后优化参数，使得似然概率极大化。

先考虑简单情形：K=1，此时打分只有 0 和 1 两种情况。此时：

$$
\begin{align}
\log(\frac{P_{nij1}}{P_{nij0}}) &= B_n - D_i - C_j - F_1 \\
P_{nij0} + P_{nij1} &= 1
\end{align}
$$

所以：

$$
\begin{align}
P_{nij1} &= P_{nij0}e^{B_n - D_i - C_j - F_1} \\
P_{nij0} &= \frac{1}{1+e^{B_n - D_i - C_j - F_1}} \\
P_{nij1} &= \frac{e^{B_n - D_i - C_j - F_1}}{1+e^{B_n - D_i - C_j - F_1}} \\
\end{align}
$$

假如实际上有两个考生，两个考官，两个题目，已知得分情况如下：

| 考生 | 题目 | 考官 | 得分 |
|------|------|------|------|
| 0    | 0    | 0    | 1    |
| 0    | 0    | 1    | 1    |
| 0    | 1    | 0    | 0    |
| 0    | 1    | 1    | 0    |
| 1    | 0    | 0    | 1    |
| 1    | 0    | 1    | 0    |
| 1    | 1    | 0    | 0    |
| 1    | 1    | 1    | 1    |

那么目标就是最大化 $P_{0001}P_{0011}P_{0100}P_{0110}P_{1001}P_{1010}P_{1100}P_{1111}$。

因为 $K=1$，只有一种 $F_k$，所以 $F_1$ 是常数项，直接让它等于 0。

如果所有 $B_n$ 同时增加一个数 $c$，同时 $D_i$ 或 $C_j$ 增加同一个数 $c$，概率不变。所以为了避免无穷多组解，添加约束：$\Sigma_n{B_n} = 0, \Sigma_j{C_j} = 0$。

因为最大化目标是个乘积，不方便计算，对它求对数，就得到了 $\log P_{0001}+\log P_{0011}+\log P_{0100}+\log P_{0110}+\log P_{1001}+\log P_{1010}+\log P_{1100}+\log P_{1111}$，成为新的最大化目标。

已知：

$$
\begin{align}
P_{nij0} &= \frac{1}{1+e^{B_n - D_i - C_j - F_1}} \\
P_{nij1} &= \frac{e^{B_n - D_i - C_j - F_1}}{1+e^{B_n - D_i - C_j - F_1}} \\
\end{align}
$$

设 $L_{nij}=B_n - D_i - C_j - F_1 = B_n - D_i - C_j$，那么：

$$
\begin{align}
P_{nij0} &= \frac{1}{1+e^{L_{nij}}} \\
P_{nij1} &= \frac{e^{L_{nij}}}{1+e^{L_{nij}}} \\
\end{align}
$$

设 $s_{nij} \in \{0,1\}$ 即考生 n 在题目 i 被考官 j 打的实际得分，那么极大化目标里，每一项的表达式就是：

$$
s_{nij}\log(P_{nij1}) + (1-s_{nij})\log(P_{nij0})
$$

即 $s_{nij}=0$ 时等于 $\log(P_{nij0})$，$s_{nij}=1$ 时等于 $\log(P_{nij1})$。上式可以化简：

$$
\begin{align}
s_{nij}\log(P_{nij1}) + (1-s_{nij})\log(P_{nij0}) \\
&= s_{nij}\log(e^{L_{nij}}P_{nij0}) + (1-s_{nij})\log(P_{nij0}) \\
&= s_{nij}(L_{nij}+\log(P_{nij0})) + (1-s_{nij})\log(P_{nij0}) \\
&= s_{nij}L_{nij}+\log(P_{nij0}) \\
&= s_{nij}L_{nij}-\log(1+e^{L_{nij}}) \\
\end{align}
$$

有了这个优化目标以后，就可以对 $B_n, D_i, C_j$ 求偏导，通过多次迭代来最大化对数极大似然。

比如每一项对 $B_n$ 求导：

$$
\begin{align}
\frac{\partial(s_{nij}L_{nij}-\log(1+e^{L_{nij}}))}{\partial B_n} \\
&= s_{nij}-\frac{e^{L_{nij}}}{1+e^{L_{nij}}} \\
&= s_{nij}-P_{nij1}
\end{align}
$$

类似地，每一项对 $D_i$ 或 $C_j$ 求导：

$$
\begin{align}
\frac{\partial(s_{nij}L_{nij}-\log(1+e^{L_{nij}}))}{\partial D_i} \\
&= \frac{\partial(s_{nij}L_{nij}-\log(1+e^{L_{nij}}))}{\partial C_j} \\
&= -(s_{nij}-P_{nij1})
\end{align}
$$

上述数据，迭代出来的结果是：

- 考生能力 B：$B_0=0.00000, B_1=0.00000$
- 题目难度 D：$D_0=-1.09861, D_1=1.09861$，这个数刚好等于 $\ln(3)$
- 考官严厉度 C：$C_0=0.00000, C_1=-0.00000$

得到的结论就是，两个考生的能力相同，考官的严厉程度相同，但题目难度不同，题目 1 比题目 0 更难。
