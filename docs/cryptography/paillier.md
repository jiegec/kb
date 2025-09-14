# Paillier 同态加密算法 

参考：[Paillier cryptosystem](https://en.wikipedia.org/wiki/Paillier_cryptosystem)

Paillier 是一种同态加密算法，它允许在不知道明文的情况下，通过密文，实现对明文的运算：

已知两个密文，可以对它们对应的明文求加法：

$D(E(m_1, r_1) \cdot E(m_2, r_2) \bmod n^2) = m_1 + m_2 \bmod n$

已知一个密文和一个明文，可以对密文对应的明文进行加法或者乘法：

$D(E(m_1, r_1) \cdot g^{m_2} \bmod n^2) = m_1 + m_2 \bmod n$

$D(E(m_1, r_1)^{m_2} \bmod n^2) = m_1m_2 \bmod n$

$D(E(m_2, r_1)^{m_1} \bmod n^2) = m_1m_2 \bmod n$
