# RISC-V Vector (RVV) Extension

规范：[riscvarchive/riscv-v-spec](https://github.com/riscvarchive/riscv-v-spec)

## 概念

- VLEN: 每个向量寄存器的宽度，单位是 bit
- SEW(Selected Element Width): 当前的元素宽度，单位是 bit，取值 8/16/32/64
- ELEN: 支持的 SEW 的最大值
- LMUL: Vector register group multiplier，把一到多个的向量寄存器绑在一起当成一个向量寄存器来用，可以是整数，也可以是分数，取值 1/8, 1/4, 1/2, 1, 2, 4, 8
- VLMAX: 最大的元素个数：`LMUL*VLEN/SEW`
- EEW: effective element width，默认是 SEW，但如果指令自带了宽度，EEW 可能和 SEW 不同
- EMUL: effective LMUL，默认是 LMUL，但如果 EEW 和 SEW 不同，那么可以通过 EEW/EMUL=SEW/LMUL 得到 EMUL 的值，这样保证了元素个数是不变的

## CSR

- mstatus/vsstatus: 和浮点类似，用来启用/关闭 RVV，方便上下文切换
- vtype: 最主要的 rvv 状态，通过 `vset{i}vl{i}` 指令设置，包括如下字段：
	- vill: illegal，用来检测不合法的 vtype
	- vma: 设置没有被 mask enable 的部分怎么处理：undisturbed（不变）或 agnostic（硬件决定不变或者写为全 1）
	- vta：设置没有被 vl 覆盖的部分怎么处理，也是 undisturbed 或 agnostic
	- vsew：设置 SEW
	- vlmul：设置 LMUL
- vl: 当前的向量寄存器长度，单位是元素个数，最大值是 VLMAX
- vlenb: 保存了 VLEN/8
- vstart：执行时跳过开头的一些元素，用于异常恢复
- vxrm: rounding mode
- vxsat: saturation flag
- vcsr: vxrm + vxsat
