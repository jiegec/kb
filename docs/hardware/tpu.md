# Google TPU

## TPU v1

论文：[In-Datacenter Performance Analysis of a Tensor Processing Unit ](https://arxiv.org/pdf/1704.04760)

Matrix Unit 采用 Weight Stationary Systolic Array：权重驻留在脉动阵列内部，即输入矩阵是 Bx256，权重是 256x256，输出矩阵是 Bx256。

脉动阵列是 256x256 个 PE，每个 PE 内部是 8 bit 的，占用芯片 24% 面积。每一拍流入 256x8b 等于 256B 的数据。内部是 256x256x8b 共 64KB 的权重。为了解决权重加载的 256 周期延迟，采用了 double buffering，实际上有两份权重。256 个周期的加载延迟，意味着它的权重加载也是每个周期从阵列上部传 256 个权重进去。

输入矩阵怎么来：TPU 通过 PCIe 访问内存，执行 Read_Host_Memory 指令把数据搬运到 Unified Buffer，然后执行 MatrixMultiply 指令的时候，会从 Unified Buffer 读取输入矩阵。Unified Buffer 是 96Kx256x8b，共 24MB，占用芯片 29% 面积。

权重矩阵怎么来：TPU 自己有一个 8GB 的 DDR3-2133 DRAM，里面保存的是权重，即 Weight Memory；权重读取时，先进入 Weight FIFO，再进入 Systolic Array。

输出矩阵怎么去：从 Systolic 流出，与 Accumulators 里的数据累加并保存到 Accumulators。Accumulators 大小是 4Kx256x32b，共 4MB。

支持的指令：

- Read_Host_Memory 从 CPU 侧内存读取数据到 Unified Buffer
- Read_Weights 从 Weight Memory（TPU 自带的 DDR3 DRAM）拷贝数据到 Weight FIFO，再输入到 Matrix Unit
- MatrixMultiply/Convolve 进行一个矩阵乘法，输入是 Unified Buffer，大小是 Bx256；输出是 Accumulators，大小是 Bx256，需要耗费 B 个流水线周期（实际上还有启动延迟）
- Activate 执行非线性激活函数，如 ReLU，Sigmoid，输入是 Accumulators，输出是 Unified Buffer
- Write_Host_Memory 把数据从 Unified Buffer 写回 CPU 侧内存

芯片规格：700 MHz，256x256 的阵列，可以达到 700MHzx256x256x2=91.8 INT8 TOPS。
