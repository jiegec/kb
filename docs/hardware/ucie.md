# UCIe

UCIe 的标准可以在官网上申请，申请后过几天会在邮箱里收到 UCIe 的标准 PDF。下文参考的是 UCIe 1.1（2023 年 7 月 10 日 版本）。按照 UCIe 标准要求，这里列出 UCIe 标准的版权信息： `© 2022–2023 UNIVERSAL CHIPLET INTERCONNECT EXPRESS, INC. ALL RIGHTS RESERVED`。

## 介绍

UCIe 是一个用于 Chiplet 的互联协议，把一个 package 上的多个 die 连接起来。它支持不同的协议：标准的 PCIe 和 CXL，通用的 Streaming 协议，或者自定义的协议。

它的主要目的是，采用一个标准的物理层和链路层，把 die 间的通信协议“标准化”，但是在 UCIe 上层，具体用什么协议，就不一定那么标准了。

UCIe 从高到低分为三层：

1. 上层的 Protocol Layer：支持 PCIe，CXL，或者通用的 Streaming 协议
2. 中间的 Die-to-Die Adapter
3. 底层的 Physical Layer
