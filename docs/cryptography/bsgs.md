# Baby-step Giant-step 算法

参考： [Baby-step Giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step) 方法

为了找到 $x$ 满足 $a^x = b \pmod p$，设 $m = \lceil \sqrt{p-1} \rceil$，那么一定可以找到 $i, j \in [0, m)$ 使得 $x = i + mj$，那就枚举所有的 $i \in [0, m)$，计算出 $a^i \bmod p$ 并保存下来，放到一个集合当中，然后枚举 $b$，计算 $b(a^{-m})^j \bmod p$ 是否出现在前述集合中，如果有，那么就有 $i, j$ 使得 $a^i = b(a^{-m})^j \pmod p$ 即 $a^{i+mj}=a^x=b \pmod p$。

代码样例：

```python
def bsgs(unit, base, target, order):
    """Find x < order satisfying power(base, x) = target"""
    m = int(math.sqrt(order)) + 1

    baby = {}
    current = unit
    for j in range(m):
        baby[current] = j
        current = mul(current, base)

    base_m = pow(base, m)
    giant = inv(base_m)
    current = target
    for i in range(m):
        if current in baby:
            return i * m + baby[current]
        current = mul(current, giant)
    return None
```
