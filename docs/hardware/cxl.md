# CXL

CXL 的标准是公开下载的：https://www.computeexpresslink.org/download-the-specification，下文参考的是 2022 年 8 月 1 日的 CXL 3.0 版本。

## CXL 设备类型

CXL 对 PCIe 的重要的扩展，一是在于让设备可以和 CPU 实现缓存一致性（CXL.cache），二是可以做远程的内存（CXL.mem）。

具体下来，CXL 标准主要定义了三类设备：

- CXL Type 1: 设备带有与 CPU 一致的缓存，实现 CXL.io 和 CXL.cache
- CXL Type 2: 设备带有自己的内存和与 CPU 一致的缓存，实现 CXL.io，CXL.cache 和 CXL.mem
- CXL Type 3: 设备带有自己的内存，实现 CXL.io 和 CXL.mem

## CXL 传输层

### CXL.io

CXL.io 基本上就是 PCIe 协议：

    CXL.io provides a non-coherent load/store interface for I/O devices. Figure
    3-1 shows where the CXL.io transaction layer exists in the Flex Bus layered
    hierarchy. Transaction types, transaction packet formatting, credit-based
    flow control, virtual channel management, and transaction ordering rules
    follow the PCIe* definition; please refer to the “Transaction Layer
    Specification” chapter of PCIe Base Specification for details. This chapter
    highlights notable PCIe operational modes or features that are used for
    CXL.io.

CXL 3.0 速度是 64.0 GT/s，使用 PAM4 编码，对应的是 PCIe 6.0。

### CXL.cache

CXL.cache 每个方向上有三个 channel：请求，响应和数据。考虑到 Host 和 Device 的传输方向，就是六个 channel：D2H Req，D2H Resp，D2H Data，H2D Req，H2D Resp，H2D Data。在 Data channel 上传输的缓存行大小是 64 字节。

CXL.cache 的缓存行状态采用的是 MESI。

CXL.cache 传输有三种模式：68B Flit，256B Flit 和 PBR Flit。

H2D Request 的字段：

- Valid
- Opcode
- `Address[51:6]`: 物理地址
- UQID: Unique Queue ID
- CacheID: Only in 256B Flit
- SPID/DPID: Only in PBR Flit

D2H Response 的字段：

- Valid
- Opcode
- UQID: Unique Queue ID
- DPID: Only in PBR Flit

D2H Data 的字段：

- Valid
- UQID: Unique Queue ID
- ChunkValid: Only in 68B Flit
- Bogus
- Poison: data is corrupted
- BEP: Only in 256B Flit & PBR Flit
- DPID: Only in PBR Flit

D2H Request 的字段：

- Valid
- Opcode
- CQID: Command Queue ID
- NT: Non Temporal
- CacheID: Only in 256B Flit
- Address: 46 位物理地址
- SPID/DPID: Only in PBR Flit

H2D Response 的字段：

- Valid
- Opcode
- RspData
- RSP_PRE
- CQID: Command Queue ID
- CacheID: Only in 256B Flit
- DPID: Only in PBR Flit

H2D Data 的字段：

- Valid
- CQID: Command Queue ID
- ChunkValid: Only in 68B Flit
- Bogus
- GO-Err
- CacheID: Only in 256B Flit
- DPID: Only in PBR Flit

#### 请求类型

首先考虑 Host 会发送的请求。

第一种是 SnpData，例如在 Host 在读取的时候出现缺失，此时需要向 Device 发送 Snoop，获取最新的 Dirty 的 Data，或者让 Device 的缓存行降级为 Shared 状态。

Device 收到 SnpData 后，如果发现缓存行不在缓存中（状态是 I），会回复一个 RspIHitI；如果缓存行在缓存中且数据没有修改（状态是 S 或者 E），降级到 S，会回复一个 RspSHitSE；如果缓存行是 dirty（状态是 M），可以选择降级到 S，然后回复 RspSFwdM 以及缓存行的数据，也可以选择变成 Invalid，回复 RspIFwdM 以及缓存行的数据。

可以看到，这些 D2H Response 的 Opcode 的名字格式很有规律，`Rsp+A+Hit/Fwd+B`，A 表示新的缓存行状态，B 是原来的缓存行状态，Hit 不附带数据，Fwd 附带数据。

第二种是 SnpInv，例如 Host 要写入缓存，就要 invalidate 其他缓存。Device 收到以后，可能返回 RspIHitI、RspIHitSE 和 RspIFwdM，分别对应不同的初始状态，最终都是 Invalid 态。

第三种是 SnpCur，获取当前的缓存行状态。Device 可以修改缓存行状态，但是不建议。可能的返回有 RspIHitI，RspVHitV，RspSHitSE，RspSFwdM，RspIFwdM 和 RspVFwdV。这里的 V 表示 Valid，对应 MESI 中的 MES 三种状态。所以如果缓存行状态不变的话，就是 RspIHitI，RspVHitV 和 RspVFwdV 三种响应。

再考虑 Device 会发送的请求。首先，请求可以分为四类：

1. Read：发送 D2H Request，接收 H2D Response 和 H2D Data
2. Read0：发送 D2H Request，接收 H2D Response
3. Write：发送 D2H Request，接收 H2D Response，发送 D2H Data，可选接收 H2D Response
4. Read0-Write：发送 D2H Request，接收 H2D Response，发送 D2H Data

- RdCurr(Read)，Device 读取 Host 的缓存行，不造成任何的缓存状态的修改。Device 缓存还是处于 Invalid 状态。
- RdOwn(Read)，Device 读取 Host 的缓存行，可以进入 E 态或者 M 态。Host 响应 GO-Err/GO-I/GO-E/GO-M。
- RdShared(Read)，Device 读取 Host 的缓存行，进入 S 态。Host 响应 GO-Err/GO-I/GO-S。
- RdAny(Read)，Device 读取 Host 的缓存行，进入 M 态，E 态或 S 态。Host 响应 GO-Err/GO-I/GO-S/GO-E/GO-M。
- RdOwnNoData(Read0)，Device 不读取现在缓存行的数据，进入 E 态。一般用于整个缓存行的数据都要更新的情况，所以不需要或许当前缓存行的数据。
- ItoMWr(Read0-Write)，Device 写入新的完整缓存行到 Host 中，并且进入 M 态。Host 响应 GO_WritePull/GO_ERR_WritePull。
- WrCur(Read0-Write)，和 ItoMWr 基本一样，区别在于，如果缓存行命中了，就写入到缓存中；如果缺失了，就写入到内存中。Host 响应 GO_WritePull/GO_ERR_WritePull。
- CLFlush(Read0)，要求 Host Invalidate 一个缓存行。Host 响应 GO-Err/GO-I。
- CleanEvict(Write)，Device 要 Evict 一个 Exclusive 的缓存行。Host 响应 GO_WritePull/GO_WritePull_Drop。
- DirtyEvict(Write)，Device 要 Evict 一个 Modified 的缓存行。Host 响应 GO_WritePull/GO_ERR_WritePull。
- CleanEvictNoData(Write)，Device 要 Evict 一个 Exclusive 的缓存行，但是不传输数据，只用于更新 Snoop Filter。Host 响应 GO-I。
- WrInv(Write)，Write Invalidate Line，向 Host 写入 0-64 字节的数据，并且 Invalidate 缓存。Host 响应 WritePull/GO-Err/GO-I。
- WOWrInv(Write)，Weakly Ordered 版本的 WrInV，写入 0-63 字节的数据。Host 响应 ExtCmp/FastGO_WritePull/GO_ERR_WritePull。
- WOWrInvF(Write)，Weakly Ordered 版本的 WrInv，写入 64 字节的数据。Host 响应 ExtCmp/FastGO_WritePull/GO_ERR_WritePull。
- CacheFlushed(Read0)，告诉 Host 自己的缓存都被清空了，所有缓存行都在 I 状态。Host 响应 GO-I。

#### 和其他协议的对比

在 [缓存一致性协议](cache_coherence_protocol.md) 中分析过 TileLink 的缓存一致性实现方法，如果某一个缓存（Master A）出现了缺失，需要经过如下的过程：

- Master A -> Slave: Acquire
- Slave -> Master B: Probe
- Master B -> Slave: ProbeAck
- Slave -> Master A: Grant
- Master A -> Slave: GrantAck

在 TileLink Cached 里面，所有的 Master 都是平等的。而在 CXL 中，需要维护缓存一致性的，有 CPU 内部的各个缓存之间，还有 CPU 和设备之间。而 CXL.cache 主要负责的是与设备的缓存一致性部分，维护缓存一致性的核心是在 CPU 一侧，Host 相当于 TileLink 的 Slave，Device 相当于 TileLink 的 Master A。可以说 CXL.cache 是不对称的缓存一致性协议。

例如 CXL 中设备读取缓存的时候，出现了缺失，那么需要经过如下的过程：

- Device -> Host: RdShared/RdOwn
- Host -> CPU Caches: Custom Snoop Messages
- Host -> Other CXL Device: SnpData
- Other CXL Device -> Host: RspSHitSE/RspSFwdM
- Host -> Device: GO-S

可以看到，整体的流程也是差不多的。

### CXL.mem

CXL.mem 用于扩展内存，根据类型的不同，它可能单独使用，也可能和 CXL.cache 配合使用。具体来说，有三种一致性模型：

1. HDM-H(Host-only Coherent)：仅 Type 3 设备，也就是无 CXL.cache
2. HDM-D(Device Coherent)：仅 Legacy Type 2 设备，也就是有 CXL.cache
3. HDM-DB(Device Coherent using Back-Invalidation)：Type 2 或 Type 3 设备

在 CXL.cache 中，两端是 Host 和 Device；而 CXL.mem，两端是 Master 和 Subordinate。

从 Master 到 Subordinate 的消息（M2S）有三类：

1. Request(Req)
2. Request with Data(RwD)
3. Back-Invalidation Response(BIRsp)

从 Subordinate 到 Master 的消息（S2M）有三类：

1. Response without data(NDR, No Data Response)
2. Response with Data(DRS, Data Response)
3. Back-Invalidation Snoop(BiSnp)

其中比较特别的是 Back-Invalidation，这个的目的是让 Device 可以通过 Snoop 修改 Host 中缓存了 Device 内存中的数据的缓存行。

对于 Type 3 的设备（无 CXL.cache）来说，Device 就是一个扩展的内存，比较简单，只需要支持读写内存就可以了。Host 发送 `MemRd*`，Device 响应 MemData；Host 发送 `MemWr*`，Device 响应 Cmp。

对于 Type 2 的设备（有 CXL.cache）来说，Device 既有自己的缓存，又有自己的内存，所以这时候就比较复杂了。例如 Host 在读取数据的时候（MemRd，SnpData/SnpInv/SnpCur），还需要对 Device Cache 进行 Snoop（SnpData/SnpInv/SnpCur），保证缓存的一致性。Host 想要写入数据到 Device Memory 的时候，如果此时 Device Cache 中有 Dirty 数据，需要进行写合并，再把合并后的数据写入到 Device Memory。当 Device 想要从自己的缓存读取数据，又缺失的时候，首先需要判断数据在 Host 端的缓存中，还是在 Device Memory 中，不同的偏置（Bias）模式决定了数据应该放在 Host 还是 Device 的缓存上。Device 要写入数据的时候，如果 Host 中缓存了该缓存行，则需要 Back-Invalidation。为了支持这些场景，CXL.cache 和 CXL.mem 会比较复杂。