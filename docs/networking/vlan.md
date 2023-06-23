# VLAN

VLAN 定义在 802.1Q 标准中，它的目的是把局域网切分成多个隔离的网络，通过 VLAN ID 来区分。VLAN ID 有 12 位，可以选取的区间通常是 1-4094 或者 1-4093，其中 1 一般是特殊的。

为了给以太网帧打上 VLAN ID，会在以太网帧头部的源地址后面插入四字节的信息。定义带有 VLAN 头部的以太网帧，称为 tagged；如果没有 VLAN 头部，则称为 untagged。

启用 VLAN 以后，交换机内部所有的包都会有 VLAN ID（也就是 tagged），此时同一个 VLAN 内的可以互通，不同 VLAN 则被隔离开。

交换机的端口可以配置成如下几种模式：

1. Access：只接收 untagged 以太网帧，进入交换机时，根据预先设定的 Port VLAN ID 打上 VLAN 头部；发送时，只允许发送 Port VLAN ID 对应的 VLAN 内的流量，并且离开交换机时，会去掉 VLAN 头部，成为 untagged。有的交换机也允许接收 tagged 以太网帧，要求 VLAN ID 等于 Port VLAN ID。
2. Trunk：只接收 tagged 以太网帧，不做修改；发送时也只发送 tagged 以太网帧，不做修改。
2. Hybrid（有的交换机称这个模式为 Trunk，取代上面的纯粹 Trunk）：对于预先设定的 Port VLAN ID，行为是 Access；其他的 VLAN，行为是 Trunk：
    - 接收 tagged 和 untagged，其中 untagged 会被认为是属于 Port VLAN ID 对应的 VLAN，变成 tagged。
    - 发送时，如果 VLAN ID 等于 Port VLAN ID，则去掉 VLAN 头部，变成 untagged；否则不做修改，发送 tagged。

不同交换机对于 Trunk 和 Hybrid 的定义有所不同，需要根据文档来确认具体行为。
