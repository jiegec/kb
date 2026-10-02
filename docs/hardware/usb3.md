# USB 3.x

## USB 3.0

给 Type-A 加了额外的五个引脚，一对差分对用于传输，一对差分对用于接收。每个差分对的速率是 5 Gbps，所以每个方向都是 5 Gbps。采用 8b/10b 编码，理论有效数据传输是每个方向 4 Gbps。

## USB 3.1

原来 USB 3.0 是每个方向 5Gbps 速率，重命名为 USB 3.1 Gen 1，然后新增 USB 3.1 Gen 2，每个差分对的速率翻倍到 10 Gbps，采用 128b/132b 编码，理论有效数据传输是每个方向 9.70 Gbps。

## USB 3.2

USB 3.2 支持把 Type-C 里的四对差分对，都拿来传输数据，这样有两对差分对用于传输，两对差分对用于接收。USB 3.2 的各个版本：

- USB 3.2 Gen 1x1：收发都是一个差分对，每个差分对 5Gbps，8b/10b，每个方向都是 5Gbps，即 USB 3.0 也是 USB 3.1 Gen 1
- USB 3.2 Gen 2x1：收发都是一个差分对，每个差分对 10Gbps，128b/132b，每个方向都是 10 Gbps，即 USB 3.1 Gen 2
- USB 3.2 Gen 1x2：收发各有两个差分对，每个差分对 5Gbps，8b/10b，每个方向都是 10 Gbps
- USB 3.2 Gen 2x2：收发各有两个差分对，每个差分对 10Gbps，128b/132b，每个方向都是 20 Gbps

USB 3.2 Gen 1x2 和 USB 3.2 Gen 2x1 虽然每个方向都是 10Gbps，但因为编码的不同，USB 3.2 Gen 2x1 的理论有效数据传输速率更高。

如果只用两个差分对，那么 Type-A 和 Type-B 都可以支持；如果要用四个差分对，就必须 Type-C。

## DP Alternate Mode

把 Type-C 里的 1/2/4 对差分对拿来传 DP 信号，就是 DP Alternate Mode。其余的差分对（如有）还可以继续给 USB 3.x 用。

比较常见的是把两对差分对用于 DP，然后每对差分对用的是 HBR2 速率，两对 HBR2 差分对提供 10.8 Gbps 的速率，能支持 4K 30Hz，或者 4K 60Hz YCbCr 4:2:0。
