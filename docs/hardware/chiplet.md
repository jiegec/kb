# Chiplet Interface

## ACC RV (Road vehicles - Advanced Cost-driven Chiplet Interface) 车规级芯粒互联接口标准

车规级芯粒互联接口标准 – 草案

Road vehicles - Advanced Cost-driven Chiplet Interface (ACC_RV 1.0)

标准链接：<http://www.iiisct.com/smart/upload/CMS1/202303/ACC_RV%201.0.pdf>

ACC RV 1.0 包括如下层次：

1. 协议层 Protocol Layer：支持 CXL 3.0（Standard 256B Flit），AXI 4.0 或者自定义的 Stream 协议
2. 链路层 Link Layer：可靠传输，链路适配
3. 数字物理层 Digital Physical Layer
4. 电气物理层 Electrical Physical Layer

## BoW (Bunch of Wires)

Specification: <https://opencomputeproject.github.io/ODSA-BoW/bow_specification.html> <https://www.opencompute.org/documents/bow-specification-v2-0d-1-pdf> <https://www.opencompute.org/documents/bunch-of-wires-phy-specification-pdf>

## UCIe (Universal Chiplet Interconnect Express)

UCIe 的标准可以在官网上申请，申请后过几天会在邮箱里收到 UCIe 的标准 PDF。下文参考的是 UCIe 1.1（2023 年 7 月 10 日 版本）。按照 UCIe 标准要求，这里列出 UCIe 标准的版权信息： `© 2022–2023 UNIVERSAL CHIPLET INTERCONNECT EXPRESS, INC. ALL RIGHTS RESERVED`。

### 介绍

UCIe 是一个用于 Chiplet 的互联协议，把一个 package 上的多个 die 连接起来。它支持不同的协议：标准的 PCIe 和 CXL，通用的 Streaming 协议，或者自定义的协议。

它的主要目的是，采用一个标准的物理层和链路层，把 die 间的通信协议“标准化”，但是在 UCIe 上层，具体用什么协议，就不一定那么标准了。

UCIe 从高到低分为三层：

1. 上层的 Protocol Layer：支持 PCIe，CXL，或者通用的 Streaming 协议
2. 中间的 Die-to-Die Adapter
3. 底层的 Physical Layer

### Protocol Layer & Die-to-Die Adapter

Protocol Layer 支持 PCIe、CXL 或者通用的 Streaming 协议。

PCIe 从 6.0 开始，引入了 256B 的 FLIT，因此如果要在 UCIe 上跑 PCIe 6.0，那就把 PCIe 6.0 的 FLIT 作为 UCIe 的 Protocol Layer。

类似地，CXL 支持 68B 和 256B 两种大小的 FLIT，UCIe 也把 CXL 的两种 FLIT 大小引入了进来，作为 Protocol Layer。

对于 Streaming 协议，它可以借用 PCIe 或者 CXL 的 FLIT 格式来传输。

无论哪种格式，最后到物理层都是以 64B 为一组的形式发送出去。

综合以上需求，UCIe 一共支持如下的格式：

1. Format 1: Raw `Protocol Layer populates all the bytes on FDI. Adapter passes to RDI without modifications or additions.` 对数据不做任何处理，直接传给物理层
2. Format 2: 68B Flit `Protocol Layer transmits 64B per Flit on FDI. Adapter inserts two bytes of Flit header and two bytes of CRC and performs the required barrel shifting of bytes before transmitting on RDI. On the RX, Adapter strips out the Flit header and CRC only sending the 64B per Flit to the Protocol Layer on FDI.` 在 64B 的 Flit 前面插入两个字节的头部，在后面插入两个字节的 CRC，以 68B 为单位，连续地放在多个 64B 中发送出去
3. Format 3: Standard 256B End Header Flit `Protocol Layer transmits 256B of Flit on FDI, while driving 0b on the bits reserved for the Adapter. Adapter fills in the relevant Flit header and CRC information before transmitting on RDI. On the Rx, Adapter forwards the Flit received from the Link to the Protocol Layer without modifying any bits applicable to the Protocol Layer, and the Protocol Layer must ignore any bits not applicable for it. Flit Header is located on Byte 236 and Byte 237 of the Flit.` 在 Flit 尾部插入头部等信息
4. Format 4: Standard 256B Start Header Flit `Protocol Layer transmits 256B of Flit on FDI, while driving 0b on the bits reserved for the Adapter. Adapter fills in the relevant Flit header and CRC information before transmitting on RDI. On the Rx, Adapter forwards the Flit received from the Link to the Protocol Layer without modifying any bits applicable to the Protocol Layer, and the Protocol Layer must ignore any bits not applicable for it. Flit Header is located on Byte 0 and Byte 1 of the Flit.` 在 Flit 头部插入两字节的头部，在尾部插入其余信息
5. Format 5: Latency-Optimized 256B without Optional Bytes Flit `Protocol Layer transmits 256B of Flit on FDI, while driving 0b on the bits reserved for the Adapter. Adapter fills in the relevant Flit header and CRC information before transmitting on RDI. On the Rx, Adapter forwards the Flit received from the Link to the Protocol Layer without modifying any bits applicable to the Protocol Layer, and the Protocol Layer must ignore any bits not applicable for it. CRC bytes sent with each 128B of the Flit. The optional Protocol Layer bytes are reserved in this format and not used by the Protocol Layer.` 在数据的中间和尾部都插入较短的 CRC，从而实现更短的延迟
6. Format 6: Latency-Optimized 256B with Optional Bytes Flit `Protocol Layer transmits 256B of Flit on FDI, while driving 0b on the bits reserved for the Adapter. Adapter fills in the relevant Flit header and CRC information before transmitting on RDI. On the Rx, Adapter forwards the Flit received from the Link to the Protocol Layer without modifying any bits applicable to the Protocol Layer, and the Protocol Layer must ignore any bits not applicable for it. CRC bytes sent with each 128B of the Flit, and optional bytes are used by the Protocol Layer.`

上文的 FDI 意思是 Flit-aware D2D Interface，是 Protocol Layer 和 D2D Adapter 之间的接口；RDi 的意思是 Raw D2D Interface，是 D2D Adapter 和 Physical Layer 之间的接口。

### Physical Layer

物理层拿到的就是一系列的 64B 数据，根据链路的宽度，分布到不同的 Lane 上。

## AIB (Advanced Interface Bus)

Specification: <https://github.com/chipsalliance/AIB-specification>

Whitepaper: <https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/accelerating-innovation-through-aib-whitepaper.pdf>

RTL Example: <https://github.com/chipsalliance/aib-protocols> <https://github.com/chipsalliance/aib-phy-hardware>