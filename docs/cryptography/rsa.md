# RSA 非对称加密

- 大素数 $p$ 和 $q$
- 计算 $n = pq$
- 选定一个公开的 $e$，一般是 65537
- 计算 $e$ 关于模 $(p-1)(q-1)$ 的逆元 $d$
- 那么 $ed \equiv 1 \pmod {(p-1)(q-1)}$
- 根据欧拉定理，$a^{(p-1)(q-1)} \equiv 1 \pmod n$
- 因此 $(x^e)^d \equiv x \pmod n$
- 加密过程：$c \equiv m^e \pmod n$
- 解密过程：$c^d \equiv m \pmod n$
- 公钥：$n$ 和 $e$
- 私钥：$p$、$q$ 和 $d$
