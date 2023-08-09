# zk-SNARK

zk-SNARK 全名是 zero knowledge Succinct Non-interactive ARgument of Knowledge，是一种零知识证明的协议，其特点是简明（Succinct），也就是需要的信息量比较少；非交互式（Non-interactive），也就是不需要证明者和验证者之间进行多次的交互。

本文基本按照 [Why and How zk-SNARK Works: Definitive Explanation](https://arxiv.org/pdf/1906.07221.pdf) 的思路去探讨 zk-SNARK 的原理和实现。

## 零知识证明

零知识证明的场景是，现在有一个 Prover 和一个 Verifier，Prover 可以向 Verifier 证明某件事情，但是又不能让 Verifier 知道隐藏的秘密。例如 Prover 要证明自己拥有超过一万块的存款，但是又不希望 Verifier 知道自己具体有多少存款，因此就需要零知识证明。

## 参考资料

- [Why and How zk-SNARK Works: Definitive Explanation](https://arxiv.org/pdf/1906.07221.pdf)