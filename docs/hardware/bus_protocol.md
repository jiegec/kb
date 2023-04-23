# 总线协议

## 功能

总线通常用于连接 CPU 和外设（包括内存），为了更好的兼容性和可复用性，能否设计一个统一的协议，其中 CPU 实现的是发起请求的一方（又称为 master），外设实现的是接收请求的一方（又称为 slave），那么如果要添加外设、或者替换 CPU 实现，都会变得比较简单，减少了许多适配的工作量。

一个总线协议需要包括哪些内容？对于 CPU 来说，程序会读写内存，读写内存就需要将以下几个信号传输到内存：

1. 地址（`addr`）：例如 32 位地址
2. 数据（`w_data` 和 `r_data`）：分别是写数据和读数据，宽度通常为 32 位或 64 位，也就是一个时钟周期可以传输的数据量
3. 读还是写（`we`）：高表示写，低表示读
4. 字节有效（`be`）：例如为了实现单字节写，虽然 `w_data` 可能是 32 位宽，但是实际写入的是其中的一个字节

除了请求的内容以外，为了表示 CPU 想要发送请求，还需要添加 `valid` 信号：高表示发送请求，低表示不发送请求。很多时候，外设的速度比较慢，可能无法保证每个周期都可以处理请求，因此外设可以提供一个 `ready` 信号：当 `valid=1 && ready=1` 的时候，发送并处理请求；当 `valid=1 && ready=0` 的时候，表示外设还没有准备好，此时 CPU 需要一直保持 `valid=1` 不变，等到外设准备好后，`valid=1 && ready=1` 请求生效。

## 简易总线协议

结合上文，可以设计一个简易总线协议，分别得到 master 和 slave 端的信号列表。约定在命名的时候用 `_o` 表示输出、`_i` 表示输入，那么 master 端（CPU 端）的信号：

1. `clock_i`：时钟输入
2. `valid_o`：高表示 master 想要发送请求
3. `ready_i`：高表示 slave 准备好处理请求
4. `addr_o`：master 想要读写的地址
5. `we_o`：master 想要读还是写
6. `data_o`：master 想要写入的数据
7. `be_o`：master 读写的字节使能，用于实现单字节写等
8. `data_i`：slave 提供给 master 的读取的数据

除了时钟都是输入以外，把上面其余的信号输入、输出对称一下，就可以得到 slave 端（外设端）的信号：

1. `clock_i`：时钟输入
2. `valid_i`：高表示 master 想要发送请求
3. `ready_o`：高表示 slave 准备好处理请求
4. `addr_i`：master 想要读写的地址
5. `we_i`：master 想要读还是写
6. `data_i`：master 想要写入的数据
7. `be_i`：master 读写的字节使能，用于实现单字节写等
8. `data_o`：slave 提供给 master 的读取的数据

以上面的总线协议为例，绘制出一个可能的波形图（以 master 的信号为例）：

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "clock", wave: "p.........", node: ".abcdefgh"},
      { name: "valid_o", wave: "0101.01..0"},
      { name: "ready_i", wave: "010.101..0"},
      { name: "addr_o", wave: "x=x=.x===x", data: ["0x01", "0x02", "0x03", "0x01", "0x02"]},
      { name: "we_o", wave: "x1x0.x101x"},
      { name: "data_o", wave: "x=xxxx=x=x", data: ["0x12", "0x56", "0x9a"]},
      { name: "be_o", wave: "x=x=.x=x=x", data: ["0x1", "0x1", "0x1", "0x1"]},
      { name: "data_i", wave: "xxxx=xx=xx", data: ["0x34", "0x12"]},
    ]
}
```
<figcaption>简易总线协议的波形图</caption>
</figure>

- `a` 周期：此时 `valid_o=1 && ready_i=1` 说明有请求发生，此时 `we_o=1` 说明是一个写操作，并且写入地址是 `addr_o=0x01`，写入的数据是 `data_o=0x12`
- `b` 周期：此时 `valid_o=0 && ready_i=0` 说明无事发生
- `c` 周期：此时 `valid_o=1 && ready_i=0` 说明 master 想要从地址 0x02（`addr_o=0x02`）读取数据（`we_o=0`），但是 slave 没有接受（`ready_i=0`）
- `d` 周期：此时 `valid_o=1 && ready_i=1` 说明有请求发生，master 从地址 0x02（`addr_o=0x02`）读取数据（`we_o=0`），读取的数据为 0x34（`data_i=0x34`）
- `e` 周期：此时 `valid_o=0 && ready_i=0` 说明无事发生
- `f` 周期：此时 `valid_o=1 && ready_i=1` 说明有请求发生，master 向地址 0x03（`addr_o=0x03`）写入数据（`we_o=1`），写入的数据为 0x56（`data_i=0x56`）
- `g` 周期：此时 `valid_o=1 && ready_i=1` 说明有请求发生，master 从地址 0x01（`addr_o=0x01`）读取数据（`we_o=0`），读取的数据为 0x12（`data_i=0x12`）
- `h` 周期：此时 `valid_o=1 && ready_i=1` 说明有请求发生，master 向地址 0x02（`addr_o=0x02`）写入数据（`we_o=1`），写入的数据为 0x9a（`data_i=0x9a`）

观察上面的波形，得到如下几条规律：

1. master 想要发起请求的时候，就设置 `valid_o=1`；当 slave 可以接受请求的时候，就设置 `ready_i=1`；在 `valid_o=1 && ready_i=1` 时视为一次请求
2. 如果 master 发起请求，同时 slave 不能接收请求，即 `valid_o=1 && ready_i=0`，此时 master 要保持 `addr_o` `we_o` `data_o` 和 `be_o` 不变，直到请求结束，这一点非常重要
3. 当 master 不发起请求的时候，即 `valid_o=0`，此时总线上的信号都视为无效数据，不应该进行处理；对于读操作，只有在 `valid_o=1 && ready_i=1` 时 `data_i` 上的数据是有效的
4. 可以连续多个周期发生请求，即 `valid_o=1 && ready_i=1` 连续多个周期等于一，此时是理想情况，可以达到总线最高的传输速度

这样就实现了一个简易的总线协议。

## Wishbone

Wishbone 是一个在开源社区广泛使用的总线协议，其分为多个版本，下面介绍其中的 Wishbone Classic Standard 和 Wishbone Classic Pipelined。

### Wishbone Classic Standard

最简单的 Wishbone 版本叫做 Wishbone Classic Standard，其设计思路和上面的简易总线协议非常相似，下面将两者进行一个对比。Wishbone Classic Standard 协议的 master 端（CPU 端）的信号：

1. `CLK_I`: 时钟输入，即简易总线协议中的 `clock_i`
2. `STB_O`：高表示 master 要发送请求，即简易总线协议中的 `valid_o`
3. `ACK_I`：高表示 slave 处理请求，即简易总线协议中的 `ready_i`
4. `ADR_O`：master 想要读写的地址，即简易总线协议中的 `addr_o`
5. `WE_O`：master 想要读还是写，即简易总线协议中的 `we_o`
6. `DAT_O`：master 想要写入的数据，即简易总线协议中的 `data_o`
7. `SEL_O`：master 读写的字节使能，即简易总线协议中的 `be_o`
8. `DAT_I`：master 从 slave 读取的数据，即简易总线协议中的 `data_i`
9. `CYC_O`：总线的使能信号，无对应的简易总线协议信号

此处忽略了一些可选信号。除了最后一个 `CYC_O`，其他的信号其实就是上文的简易总线协议。`CYC_O` 的可以认为是 master 想要占用 slave 的总线接口，在常见的使用场景下，直接认为 `CYC_O=STB_O`。它的用途是：

1. 占用 slave 的总线接口，不允许其他 master 访问
2. 简化 interconnect 的实现

把上面简易总线协议的波形图改成 Wishbone Classic Standard，就可以得到：

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "CLK_I", wave: "p.........", node: ".abcdefgh"},
      { name: "CYC_O", wave: "0101.01..0"},
      { name: "STB_O", wave: "0101.01..0"},
      { name: "ACK_I", wave: "010.101..0"},
      { name: "ADR_O", wave: "x=x=.x===x", data: ["0x01", "0x02", "0x03", "0x01", "0x02"]},
      { name: "WE_O", wave: "x1x0.x101x"},
      { name: "DAT_O", wave: "x=xxxx=x=x", data: ["0x12", "0x56", "0x9a"]},
      { name: "SEL_O", wave: "x=x=.x=x=x", data: ["0x1", "0x1", "0x1", "0x1"]},
      { name: "DAT_I", wave: "xxxx=xx=xx", data: ["0x34", "0x12"]},
    ]
}
```
<figcaption>Wishbone Classic Standard 的波形图</caption>
</figure>

### Wishbone Classic Pipelined

Wishbone Classic Standard 协议非常简单，但是会遇到一个问题：假设实现的是一个 SRAM 控制器，它的读操作有一个周期的延迟，也就是说，在这个周期给出地址，需要在下一个周期才可以得到结果。在 Wishbone Classic Standard 中，就会出现下面的波形：

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "CLK_I", wave: "p.....", node: ".abcd"},
      { name: "CYC_O", wave: "01...0"},
      { name: "STB_O", wave: "01...0"},
      { name: "ACK_I", wave: "0.1010"},
      { name: "ADR_O", wave: "x=.=.x", data: ["0x01", "0x02"]},
      { name: "WE_O", wave: "x0...x"},
      { name: "DAT_O", wave: "xxxxxx"},
      { name: "SEL_O", wave: "x=...x", data: ["0x1"]},
      { name: "DAT_I", wave: "xx=x=x", data: ["0x12", "0x34"]},
    ]
}
```
<figcaption>Wishbone Classic Standard 实现 SRAM 控制器的波形图</caption>
</figure>

- `a` 周期：master 给出读地址 0x01，此时 SRAM 控制器开始读取，但是此时数据还没有读取回来，所以 `ACK_I=0`
- `b` 周期：此时 SRAM 完成了读取，把读取的数据 0x12 放在 `DAT_I` 并设置 `ACK_I=1`
- `c` 周期：master 给出下一个读地址 0x02，SRAM 要重新开始读取
- `d` 周期：此时 SRAM 完成了第二次读取，把读取的数据 0x34 放在 `DAT_I` 并设置 `ACK_I=1`

从波形来看，功能没有问题，但是每两个周期才能进行一次读操作，发挥不了最高的性能。在 `a` 周期给出第一个地址，在 `b` 周期得到第一个数据，那么如果能在 `b` 周期的时候给出第二个地址，就可以在 `c` 周期得到第二个数据，这样就可以实现流水线式的每个周期进行一次读操作。但是，Wishbone Classic Standard 要求 `b` 周期时第一次请求还没有结束，因此需要修改协议，来实现流水线式的请求。

实现思路也很简单：既然 Wishbone Classic Standard 认为 `b` 周期时，第一次请求还没有结束，那就让第一次请求提前在 `a` 周期完成，只不过它的数据要等到 `b` 周期才能给出。实际上，这个时候的一次读操作，可以认为分成了两部分：首先是 master 向 slave 发送读请求，这个请求在 `a` 周期完成；然后是 slave 向 master 发送读的结果，这个结果在 `b` 周期完成。为了实现这个功能，进行如下修改：

- 添加 `STALL_I` 信号：`CYC_O=1 && STB_O=1 && STALL_I=0` 表示进行一次读请求
- 修改 `ACK_I` 信号含义：`CYC_O=1 && STB_O=1 && ACK_I=1` 表示一次读响应

进行如上修改，就得到了 Wishbone Classic Pipelined 总线协议。上面的两次连续读操作波形如下：

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "CLK_I", wave: "p....", node: ".abcd"},
      { name: "CYC_O", wave: "01..0"},
      { name: "STB_O", wave: "01.0."},
      { name: "STALL_I", wave: "0...."},
      { name: "ACK_I", wave: "0.1.0"},
      { name: "ADR_O", wave: "x==xx", data: ["0x01", "0x02"]},
      { name: "WE_O", wave: "x0.xx"},
      { name: "DAT_O", wave: "xxxxx"},
      { name: "SEL_O", wave: "x=.xx", data: ["0x1"]},
      { name: "DAT_I", wave: "xx==x", data: ["0x12", "0x34"]},
    ]
}
```
<figcaption>Wishbone Classic Pipelined 实现 SRAM 控制器的波形图</caption>
</figure>

- `a` 周期：master 请求读地址 0x01，slave 接收读请求（`STALL_O=0`）
- `b` 周期：slave 返回读请求结果 0x12，并设置 `ACK_I=1`；同时 master 请求读地址 0x02，slave 接收读请求（`STALL_O=0`）
- `c` 周期：slave 返回读请求结果 0x34，并设置 `ACK_I=1`；master 不再发起请求，设置 `STB_O=0`
- `d` 周期：所有请求完成，master 设置 `CYC_O=0`

这样就利用 Wishbone Classic Pipelined 协议实现了一个每周期进行一次读操作的 slave。

## AXI

AXI 总线协议是 ARM 公司提出的总线协议，在 ARM 处理器以及 Xilinx FPGA 内使用的比较广泛。

AXI 的信号分成五个 Channel：

1. AW（Address Write）：写请求的地址会通过 AW Channel 发送给 Slave
2. W（Write）：写请求的数据会通过 W Channel 发送给 Slave
3. B：写响应会通过 B Channel 发送给 Master
4. AR（Address Read）：读请求的地址会通过 AR Channel 发送给 Slave
5. R（Read）：读响应会通过 R Channel 发送给 Slave

每个 Channel 都包括 `valid-ready` 式的握手信号，对于 AW、W 和 AR Channel，Master 是发送方，Slave 是接收方；对于 R 和 B Channel，Slave 是发送方，Master 是接收方。

可见 AXI 的设计把请求和响应的过程拆开，并且允许总线上同时有多个正在进行的请求：不用等待响应回来，就可以发送新的请求。因此 AXI 可以更好地利用内存的并行度，达到更高的性能，代价就是设计更加复杂。

为了完成一次写请求，Master 需要：

1. 通过 AW Channel 发送要写入的地址、写入的长度等信息给 Slave
2. 通过 W Channel 发送要写入的数据，支持 Burst，也就是使用多个周期完成一个写请求的数据传输
3. 在 B Channel 上等待 Slave 回复写入完成的响应

为了完成一次读请求，Master 需要：

1. 通过 AR Channel 发送要读取的地址、读取的长度等信息给 Slave
2. 在 R Channel 上等待 Slave 回复读取的数据，支持 Burst，也就是使用多个周期完成一个读响应的数据传输

由于 AXI 上可以同时进行多个请求，为了让 Master 可以区分出 B 和 R Channel 上的响应与请求的对应关系，每个请求和响应都附带了一个 ID，那么 Master 在请求中附带了什么 ID，Slave 在响应的时候，也要附带相同的 ID。对于同一个 ID 的请求，其顺序是受保证的。

AXI 有支持缓存一致性协议的扩展：ACE，其内容在 [一致性协议](cache_coherence_protocol.md) 中介绍。

## TileLink

TileLink 总线协议是 SiFive 公司提出的总线协议，在 Rocket Chip 相关的项目中使用比较广泛。根据 [TileLink Spec 1.8.0](https://github.com/chipsalliance/omnixtend/blob/master/OmniXtend-1.0.3/spec/TileLink-1.8.0.pdf)，TileLink 分为以下三种：

- TL-UL: 只支持读写，不支持 burst，类比 AXI-Lite
- TL-UH：支持读写，原子指令，预取，支持 burst，类比 AXI+ATOP（AXI5 引入的原子操作）
- TL-C：在 TL-UH 基础上支持缓存一致性协议，类比 AXI+ACE/CHI

本文主要讨论前两种，TL-C 的内容在 [一致性协议](cache_coherence_protocol.md) 中介绍。

### 接口

TileLink Uncached(TL-UL 和 TL-UH) 包括了两个 channel：

- A channel: M->S 发送请求，类比 AXI 的 AR/AW/W
- D channel: S->M 发送响应，类比 AXI 的 R/W

因此 TileLink 每个周期只能发送读或者写的请求，而 AXI 可以同时在 AR 和 AW channel 上发送请求。

一些请求的例子：

- 读：M->S 在 A channel 上发送 Get，S->M 在 D channel 上发送 AccessAckData
- 写：M->S 在 A channel 上发送 PutFullData/PutPartialData，S->M 在 D channel 是发送 AccessAck
- 原子操作：M->S 在 A channel 上发送 ArithmeticData/LogicalData，S->M 在 D channel 上发送 AccessAckData
- 预取操作：M->S 在 A channel 上发送 Intent，S->M 在 D channel 上发送 AccessAck

### 和 AXI 的对比

和 AXI 对比，TileLink 把读和写进行了合并，所有的读写请求都通过 A channel 发送，所有的响应都通过 D channel 回复。这样做简化了硬件的实现，但如果 CPU 希望同时进行大量的读写，可能 AXI 可以实现更高的性能。

下面分析 TileLink 和 AXI 协议的桥接模块的实现方法。

首先针对 [AXI4ToTL](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/amba/axi4/ToTL.scala#L59) 模块的例子，来分析一下如何把一个 AXI4 Master 转换为 TileLink。

针对 AXI4 和 TileLink 的区别进行设计：一个是读写 channel 合并了，所以这里需要一个 Arbiter；其次 AXI4 中 AW 和 W 是分开的，这里也需要进行合并。这个模块并不考虑 Burst 的情况，而是由 [AXI4Fragmenter](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/amba/axi4/Fragmenter.scala#L14=) 来进行拆分，即添加若干个 AW beat，和 W 进行配对。

具体到代码实现上，首先把 AR channel [对应到](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/amba/axi4/ToTL.scala#L86=) 到 A channel 上：

```scala
val r_out = Wire(out.a)
r_out.valid := in.ar.valid
r_out.bits :<= edgeOut.Get(r_id, r_addr, r_size)._2
```

然后 AW+W channel 也[连接](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/amba/axi4/ToTL.scala#L119=) 到 A channel，由于不用考虑 burst 的情况，这里在 aw 和 w 同时 valid 的时候才认为有请求。

```scala
val w_out = Wire(out.a)
in.aw.ready := w_out.ready && in.w.valid && in.w.bits.last
in.w.ready  := w_out.ready && in.aw.valid
w_out.valid := in.aw.valid && in.w.valid
w_out.bits :<= edgeOut.Put(w_id, w_addr, w_size, in.w.bits.data, in.w.bits.strb)._2
```

为了区分请求的类型，读写的 id 增加了若干位，最低位 0 表示读，1 表示写，剩下几位是请求编号，这样发出去的是不同 id 的多个请求。

然后，把读和写的 A channel [连接](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/amba/axi4/ToTL.scala#L155=)到 Arbiter 上：

```scala
TLArbiter(TLArbiter.roundRobin)(out.a, (UInt(0), r_out), (in.aw.bits.len, w_out))
```

其余的部分则是对 D channel 进行判断，有数据的转给 R channel，没有数据的转给 B channel：

```scala
out.d.ready := Mux(d_hasData, ok_r.ready, ok_b.ready)
ok_r.valid := out.d.valid && d_hasData
ok_b.valid := out.d.valid && !d_hasData
```

最后处理了一下 TileLink 和 AXI4 对写请求返回确认的区别：TileLink 中，可以在第一个 burst beat 就返回确认，而 AXI4 需要在最后一个 burst beat 之后返回确认。

再来看一下反过来的转换，即从 TileLink Master 到 AXI。由于 TileLink 同时只能进行读或者写，所以它首先做了一个虚构的 arw channel，可以理解为合并了 ar 和 aw channel 的 AXI4，这个设计在 SpinalHDL 的代码中也能看到。然后再根据是否是写入，分别[连接](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/tilelink/ToAXI4.scala#L153=)到 ar 和 aw channel：

```scala
val queue_arw = Queue.irrevocable(out_arw, entries=depth, flow=combinational)
out.ar.bits := queue_arw.bits
out.aw.bits := queue_arw.bits
out.ar.valid := queue_arw.valid && !queue_arw.bits.wen
out.aw.valid := queue_arw.valid &&  queue_arw.bits.wen
queue_arw.ready := Mux(queue_arw.bits.wen, out.aw.ready, out.ar.ready)
```

[这里](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/tilelink/ToAXI4.scala#L197=)处理了 aw 和 w 的 valid 信号：

```scala
in.a.ready := !stall && Mux(a_isPut, (doneAW || out_arw.ready) && out_w.ready, out_arw.ready)
out_arw.valid := !stall && in.a.valid && Mux(a_isPut, !doneAW && out_w.ready, Bool(true))
out_w.valid := !stall && in.a.valid && a_isPut && (doneAW || out_arw.ready)
```

这样做的原因是，在 TileLink 中，每个 burst 都是一个 a channel 上的请求，而 AXI4 中，只有第一个 burst 有 aw 请求，所有 burst 都有 w 请求，因此这里用 doneAW 信号来进行区分。

接着，要把 b 和 r channel 上的结果连接到 d channel，根据上面的经验，[这里](https://github.com/chipsalliance/rocket-chip/blob/850e1d5d56989f031fe3e7939a15afa1ec165d64/src/main/scala/tilelink/ToAXI4.scala#L205=) 又是一个 arbitration：

```scala
val r_wins = (out.r.valid && b_delay =/= UInt(7)) || r_holds_d
out.r.ready := in.d.ready && r_wins
out.b.ready := in.d.ready && !r_wins
in.d.valid := Mux(r_wins, out.r.valid, out.b.valid)
```

最后还处理了一下请求和结果顺序的问题。