# SPI (Serial Peripheral Interface)

## 接口

SPI 协议涉及到四个信号：

- SCLK: 时钟信号，Master -> Slave
- MOSI：数据信号，Master -> Slave
- MISO：数据信号，Slave -> Master
- CS：芯片使能，一般是低有效

要通过 SPI 协议发送命令的时候，通常需要先拉低 CS，然后启动 SCLK 时钟，同时收发数据。注意 SPI 是全双工的，也就是发送的同时也在接收，只不过通常来说，外设等到主机发送了命令本身，才知道要回复什么，所以很多时候命令设计成了事实上的半双工：前半部分主机在发命令，外设发送无用的数据；后半部分外设在发送响应，主机发送无用的数据。

## 波形

SPI 有不同的类型，下面讲一种比较常见的配置（即 CPOL=0，CPHA=0），在这种模式下，Master 和 Slave 都是在时钟的下降沿修改输出的数据，然后在时钟（`sclk`）的上升沿对接收到的数据进行采样：

```wavedrom
{
  signal:
    [
      { name: "clk", wave: "p........"},
      { name: "sclk", wave: "0.101010."},
      { name: "mosi", wave: "03.4.5.x."},
      { name: "miso", wave: "06.7.8.x."},
      { name: "cs_n", wave: "10......1"},
    ]
}
```

波形图中，时钟（`sclk`）上升沿时，数据处于稳定的状态，所以此时 Master 对 MISO 采样，Slave 对 MOSI 采样，可以得到稳定的数据；时钟下降沿时，Master 和 Slave 修改输出的数据。

实际在 RTL 中实现的时候，Master 可以不写 negedge 逻辑，而是写一个分频器，在分频出来的负半周期里，实现数据的修改，如上图中的 `clk` 分频到 `sclk`。一般使用一个状态机来实现 SPI Master，记录当前传输到哪一个 bit，以及记录当前是 `sclk` 的正半周期还是负半周期。

SPI 本身很简单，所以核心不在 SPI，而是在 SPI 之上定义的各种协议。

## SPI Flash

SPI Flash 是一种很常见的 SPI 外设，可以用来访问 NAND/NOR Flash。

为了提升性能，很多 SPI Flash 还会提供 Dual SPI 和 Quad SPI 模式。标准的 SPI 中，Master 到 Slave 和 Slave 到 Master 分别是一根信号线，如果要继续提高性能，那就要引入更多的信号线来进行数据传输，所以 Dual SPI 就是让原来的 MISO 和 MOSI 都可以同时发送数据；Quad SPI 则是又额外添加了两个信号线来进行数据传输。

常见的 SPI Flash 厂家：

- Spansion -> Cypress -> Infineon
- Numonyx -> Micron
- Winbond
- GigaDevice
- Macronix

### SPI NAND Flash

下面以 [Alliance Memory SPI NAND Flash Datasheet](https://www.alliancememory.com/wp-content/uploads/pdf/flash/AllianceMemory_SPI_NAND_Flash_July2020_Rev1.0.pdf) 为例子，看看通常 SPI Flash 都支持哪些命令，都是如何传输数据的。

这款 SPI NAND Flash 的内部存储分为三层：

1. Block：数量不定
2. Page：每个 Block 包括 64 个 Page
3. Byte：每个 Page 包括一定数量的 Byte，常见的有 2112(2048+64)、2176(2048+128)、4352(4096+256)

NAND Flash 的读取粒度是 Page，这就是为什么 NAND Flash 更像块设备。一次读取过程分为三个步骤：

1. 发送 13H(Page Read to Cache) 命令，把一个 Page 的数据读取到 NAND Flash 内部的 Cache 中
2. 不断发送 0FH(Get Feature) 命令，直到 NAND Flash 表示 Page Read to Cache 命令完成
3. 发送 Read from Cache 命令，考虑到传输的方式不同，有以下几种：
    1. Read from Cache x1 IO(03H/0BH): Master 给出 1 字节命令，2 字节地址和 1 字节 dummy 数据，共 8(COMMAND)+16(ADDR)+8(DUMMY) 个周期，之后 Slave 从 MISO 给出数据
    2. Read from Cache x2 IO(3BH): Slave 同时通过 MISO 和 MOSI 给出数据
    3. Read from Cache x4 IO(6BH): Slave 同时通过 MISO、MOSI、WP# 和 HOLD# 给出数据
    4. Read from Cache Dual IO(BBH): 在 3BH 的基础上，Master 也同时通过 MISO 和 MOSI 给出地址和 dummy 字节，所以 Master 只占用 8(COMMAND)+8(ADDR)+4(DUMMY) 个周期的时间发送
    5. Read from Cache Quad IO(EBH): 在 6BH 的基础上，Master 也同时通过四个数据信号给出地址和 dummy 字节，所以 Master 只占用 8(COMMAND)+4(ADDR)+2(DUMMY) 个周期的时间发送

写入的时候，由于 NAND Flash 的特性，首先需要擦除，把一个 Block 的内容全部擦除，需要注意每个 Block 包括多个 Page，所以擦除的粒度是很粗的。擦除过的 Page 才可以进行写入，具体步骤是：

1. 发送 06H(Write Enable) 允许写入
2. 发送 02H(Program Load) 或 32H(Program Load x4) 把要写入的数据传输给 NAND Flash 中的 Cache；02H 和 32H 的区别就是后者同时在四个信号线上传输数据
3. 发送 10H(Program Execute) 进行实际的写入操作，从 Cache 到 Flash 存储
4. 不断发送 0FH(Get Feature) 命令，直到 Program Execute 操作完成

### SPI NOR Flash

NOR Flash 和 NAND Flash 的区别在于，NOR Flash 可以随机访问，可以提供 XIP 支持。下面以 [128Mb, 3V, Multiple I/O Serial Flash Memory](https://www.micron.com/-/media/client/global/documents/products/data-sheet/nor-flash/serial-nor/n25q/n25q_128mb_3v_65nm.pdf) 为例子看看它是如何读写的。

SPI NOR Flash 读取的时候，只需要一条命令就可以了：READ/FAST READ。其中 READ 命令比较简单：发送 Command，发送地址，然后 Slave 紧接着就会发送数据；FAST READ 可以达到更高的频率，但是为了让 NOR Flash 有时间读取数据，在 Master 发送 Command 和地址后，还需要发送 Dummy cycles，然后 Slave 才会发送数据。和前面一样，FAST READ 也支持不同的 IO 类型，例如 Dual Output，Dual Input/Output，Quad Output，Quad Input/Output。一些比较高端的 SPI NOR Flash 还支持 DTR（Double Transfer Rate），实际上就是 DDR，在时钟上升沿和下降沿都采样数据。

写入的时候，和 NAND Flash 一样，也需要先擦除，再写入。SPI Flash 的存储层级是：

1. Sector
2. Subsector
3. Page
4. Byte

擦除的粒度是 Sector 或者 Subsector，写入的粒度是 Page。写入的时候，也需要首先发送 WRITE ENABLE 命令，再发送 PAGE PROGRAM 命令。NOR Flash 在 Program 上也比较简化，直接 Program 即可，不需要先写入到 Cache，再进行 Program。

NOR Flash 还提供了 XIP Mode 来加快随机访问：启用 XIP 模式后，给出一个地址，等待 Dummy cycles 后，就可以读出数据，不需要像前面那样发送 COMMAND，减少了延迟。当然了，即使不打开 NOR Flash 的 XIP Mode，也可以在 SPI 控制器里实现 XIP，只不过每次读取都要发一次 READ 命令。

## SPI EEPROM

SPI EEPROM 和 SPI NOR Flash 比较类似，但是 EEPROM 更小，也更加简单，例如写入的时候，不需要擦除。感兴趣的可以在 [SPI 串行 EEPROM 系列数据手册](http://ww1.microchip.com/downloads/en/DeviceDoc/22040c_cn.pdf) 中查看命令列表，这里就不赘述了。

## SD 卡

SD 卡除了 SD Bus 以外，还支持 SPI 模式（最新的 SDUC 不支持 SPI 模式），所以也可以用 SPI 来读写 SD 卡。

SD 卡比较特别的一点是，它需要比较复杂的初始化流程：

1. 首先要发送 CMD0 命令，同时 CS 拉低，使得 SD 卡进入 SPI 模式
2. 对于 SDHC SD 卡，需要发送 CMD8 来协商工作电压范围
3. 重复发送 ACMD41 命令（CMD55 + CMD41 = ACMD41）进行初始化，直到 SD 卡回复初始化完成
4. 发送 CMD58 命令以读取 OCR 寄存器的值

比较有意思的是命令的传输方式。每个命令有一个 6 位的命令编号，例如 CMD0 的编号就是 0，CMD55 的编号就是 55；还带有四字节的参数。每个命令会组装成一个 48 位的分组：

1. bit[47]=0: Start Bit
2. bit[46]=1: Transmission Bit
3. bit[45:40]: Command Index
4. bit[39:8]: Argument
5. bit[7:1]: CRC7
6. bit[0]=1: End Bit

可见额外多了一个 CRC7 的校验和。

SD 卡规定，SPI 模式下，所有的数据传输都是对齐到 8 位，也就是从 CS 拉低开始算，每 8 个时钟上升沿是一个字节，无论命令还是响应，都在 8 位的边界上传输。

想要读取数据的话，就要发送 READ_SINGLE_BLOCK 命令，参数就是要读取的 Block 地址，Block 地址的单位在 SDSC 上是字节，在 SDHC 和 SDXC 上是 512 字节。SD 卡回先回复一个字节的响应，然后开始发数据，数据从 Start Block Token 开始，然后是一个 Block 的数据（通常是 512 字节），最后再两个字节的 CRC16。

写数据则是发送 WRITE_BLOCK 命令，SD 卡回复一个字节的响应，然后控制器开始传输数据，数据从 Start Block Token 开始，接着是要写入的数据，最后是两个字节的 CRC16，然后 SD 卡回复一个字节的响应，标志着写入成功。

## SPI 以太网控制器

有一些以太网产品提供了 SPI 接口，例如 [KSZ8851SNL/SNLI](https://ww1.microchip.com/downloads/aemDocuments/documents/UNG/ProductDocuments/DataSheets/KSZ8851SNL-Single-Port-Ethernet-Controller-with-SPI-DS00002381C.pdf)，集成了 MAC 和 PHY，直接连接 MDI/MDI-X 接口，虽然最高只支持百兆网，但是接口上确实非常简单。

SPI 上发送的命令就两类：一类是读写寄存器，一类是读写 RX/TX FIFO。

## 键盘和触摸板

一些型号的苹果电脑的键盘和触摸板是通过 SPI 接口访问的，在 Linux 中有相应的 applespi 驱动。

## SPI vs I2C

SPI 和 I2C 的区别在于，前者信号更多，全双工传输；后者信号更少，半双工传输。SPI 通过 CS 信号选择 Slave 芯片，I2C 通过地址进行区分。此外 I2C 还需要 Pull up resistor，这样如果没有设备响应，就会 NACK。

一些芯片提供了 SPI 或 I2C 的选项：共用两个信号，允许用户选择用 I2C 还是 SPI。例如 [WM8731](http://cdn.sparkfun.com/datasheets/Dev/Arduino/Shields/WolfsonWM8731.pdf)，既支持 I2C（记为 2-wire mode），又支持 SPI（记为 3-wire mode）。一般这种时候，SPI 和 I2C 就是用来配置一些寄存器的，另外可能还有一些接口，例如 WM8731 负责声音数据传输的实际上是 I2S。

## AXI Quad SPI

AXI Quad SPI 是一个 SPI 协议的控制器，它支持 XIP（eXecute In Place）模式，即可以暴露一个只读 AXI Slave 接口，当接收到读请求的时候，就发送 SPI NOR Flash 命令去对应的地址进行读取，然后返回结果。由于不同厂家的 SPI NOR Flash 支持有所不同，所以 IP 上的设置可以看到厂家的选择。

特别地，一个常见的需求是希望访问 Cfg（Configuration）Flash，亦即用来保存 Bitstream 的 Flash。当 FPGA 上电的时候，如果启动模式设置为 SPI Flash，FPGA 就会向 Cfg Flash 读取 Bitstream，Cfg Flash 需要连接到 FPGA 的指定引脚上，当 FPGA 初始化的时候由内部逻辑驱动，初始化完成后又要转交给用户逻辑。转交的方式就是通过 STARTUP 系列的 primitive。

通常，如果要连接外部的 SPI Flash，需要连接几条信号线到顶层，然后通过 xdc 把信号绑定到引脚上，然后引脚连接了一个外部的 SPI Flash。但由于 Cfg Flash 比较特殊，所以信号从 AXI Quad SPI 直接连到 STARTUP 系列的 primitive 上。如果是采用 STARTUPE2 原语的 7 系列的 FPGA，那么只有时钟会通过 STARTUPE2 pritimive 连接到 SPI Flash 上，其他数据信号还是正常通过顶层绑定；如果是采用 STARTUPE3 原语的 UltraScale 系列的 FPGA，那么时钟和数据都通过 STARTUPE3 primitive 连接到 SPI Flash。

### Virtex UltraScale+ 时序

把信号连好了只是第一步，因为外设对时序要求比较复杂，如果用一个比较高直接跑，很大可能就读取到错误的数据了。AXI Quad SPI 已经在生成的文件里提供了一个样例的 xdc，在文档里也有体现。对于 Virtex Ultrascale+ 系列的 FPGA，它内容如下：

```tcl
#### All the delay numbers have to be provided by the user

#### Following are the SPI device parameters
#### Max Tco
set tco_max 7
#### Min Tco
set tco_min 1
#### Setup time requirement
set tsu 2
#### Hold time requirement
set th 3
#####################################################################################################
# STARTUPE3 primitive included inside IP for US+                                                             #
#####################################################################################################
set tdata_trace_delay_max 0.25
set tdata_trace_delay_min 0.25
set tclk_trace_delay_max 0.2
set tclk_trace_delay_min 0.2

create_generated_clock -name clk_sck -source [get_pins -hierarchical *axi_quad_spi_0/ext_spi_clk] [get_pins -hierarchical */CCLK] -edges {3 5 7}
set_input_delay -clock clk_sck -max [expr $tco_max + $tdata_trace_delay_max + $tclk_trace_delay_max] [get_pins -hierarchical *STARTUP*/DATA_IN[*]] -clock_fall;
set_input_delay -clock clk_sck -min [expr $tco_min + $tdata_trace_delay_min + $tclk_trace_delay_min] [get_pins -hierarchical *STARTUP*/DATA_IN[*]] -clock_fall;
set_multicycle_path 2 -setup -from clk_sck -to [get_clocks -of_objects [get_pins -hierarchical */ext_spi_clk]]
set_multicycle_path 1 -hold -end -from clk_sck -to [get_clocks -of_objects [get_pins -hierarchical */ext_spi_clk]]
set_output_delay -clock clk_sck -max [expr $tsu + $tdata_trace_delay_max - $tclk_trace_delay_min] [get_pins -hierarchical *STARTUP*/DATA_OUT[*]];
set_output_delay -clock clk_sck -min [expr $tdata_trace_delay_min - $th - $tclk_trace_delay_max] [get_pins -hierarchical *STARTUP*/DATA_OUT[*]];
set_multicycle_path 2 -setup -start -from [get_clocks -of_objects [get_pins -hierarchical */ext_spi_clk]] -to clk_sck
set_multicycle_path 1 -hold -from [get_clocks -of_objects [get_pins -hierarchical */ext_spi_clk]] -to clk_sck
```

分段来看这个 xdc 都做了什么：

```tcl
create_generated_clock -name clk_sck -source [get_pins -hierarchical *axi_quad_spi_0/ext_spi_clk] [get_pins -hierarchical */CCLK] -edges {3 5 7}
```

首先，它创建了一个时钟 `clk_sck`。CCLK 是 STARTUP 输出的实际时钟，会连接到 Cfg Flash 的时钟信号上。而 AXI Quad SPI 的 ext_spi_clk 会输出到 CCLK 上，因此这里是一个生成的时钟，并且指定上下边沿的位置。`edges` 参数有三个，分别表示上升、下降和上升沿分别的位置。1 表示源时钟的第一个上升沿，2 表示源时钟的第一个下降沿，以此类推，所以 {3, 5, 7} 的意思就是频率减半，相位差半个周期。

接着最主要的就是，怎么设置延迟。可以看到，代码中首先定义了一些参数：

```tcl
#### Max Tco
set tco_max 7
#### Min Tco
set tco_min 1
#### Setup time requirement
set tsu 2
#### Hold time requirement
set th 3

#### Trace delay
set tdata_trace_delay_max 0.25
set tdata_trace_delay_min 0.25
set tclk_trace_delay_max 0.2
set tclk_trace_delay_min 0.2
```

首先是 $t_{co}$，表示的是 SPI Flash 的时钟到输出的延迟。以 SPI Flash 型号 Micron MT25QU02GCBB8E12-0SIT 为例子，可以从它的 [Datasheet](https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/nor-flash/serial-nor/mt25q/die-rev-b/mt25q_qlkt_u_02g_cbb_0.pdf) 看到，时钟到输出的延迟应该是 Max 7ns：

```
Clock LOW to output valid under 30pF Max 7ns
Clock LOW to output valid under 10pF Max 6ns
```

因此 `tco_max` 设为 7，`tco_min` 默认即可，因为 Datasheet 中没有做要求。

然后 $t_{su}$ 和 $t_h$ 则是输入的 setup 和 hold time。类似的，可以查到 SPI Flash 的参数：

```
Data in setup time Min 2.5ns
Data in hold time Min 2ns
```

所以 `tsu` 设为 2.5，`th` 设为 2。

接下来则是 tdata 和 tclk 的 trace delay。这指的是从 FPGA 引脚到 SPI Flash 引脚的信号传输延迟。这个延迟可以从板子的布线上测量长度来估计出来，一个简单的估算方法：光速 $3*10^8 \mathrm{m/s}$，假设电信号传播速度是光速的一半，可以得到延迟和长度的比值： $0.06 \mathrm{ns/cm} = 0.15 \mathrm{ns/inch}$。

下面讨论这些变量如何参与到 input/output delay 的计算中。

首先考虑 input delay。它指的是，从 SPI Flash 到 FPGA 的数据，相对于时钟的延迟。这个延迟由三部分组成：

1. 从 FPGA 输出的时钟 CCLK 到 SPI Flash 的时钟有延迟 $t_{clk}$，下图 `a -> b`
2. 从 SPI Flash 的时钟到数据输出有延迟 $t_{co}$，下图 `b -> c`
3. 从 SPI Flash 的数据到 FPGA 的数据输入有延迟 $t_{data}$，下图 `c -> d`

```wavedrom
{
  signal:
    [
      { name: "clk_fpga", wave: "p..", node: ".a" },
      { name: "clk_flash", wave: "p...", node: "..b", phase: 2.7 },
      { name: "data_flash", wave: "3456", node: "..c", phase: 2.5 },
      { name: "data_fpga", wave: "3456", node: "..d", phase: 2.3 },
    ],
  config: { hscale: 3 },
}
```

因此总延迟就是 $t_{clk}+t_{co}+t_{data}$，就可以得到对应的设置：

```tcl
set_input_delay -clock clk_sck -max [expr $tco_max + $tdata_trace_delay_max + $tclk_trace_delay_max] [get_pins -hierarchical *STARTUP*/DATA_IN[*]] -clock_fall;
set_input_delay -clock clk_sck -min [expr $tco_min + $tdata_trace_delay_min + $tclk_trace_delay_min] [get_pins -hierarchical *STARTUP*/DATA_IN[*]] -clock_fall;
```

接下来要考虑 output delay。虽然 output delay 也有 min 和 max，但其含义有所区别，需要分别考虑。

首先是 max，它对应的是 setup time。如果定义时间 0 为时钟的上升沿，沿更早的时间为正的时间轴，沿更晚的时间为负的时间轴。期望目标是，数据到达寄存器输入的时间大于 setup time，此时可以满足 setup 条件。为了计算 max output delay，需要考虑的是从 FPGA 数据输出到 SPI Flash 上时钟的延迟。

假设 FPGA CCLK 时钟上升沿在 $0$ 时刻（下图的 `a`），那么 SPI Flash 时钟上升沿在 $-t_{clk}$ 时刻（下图的 `b`）。假设 FPGA 数据输出时刻为 $t_0$（通常为正，下图的 `c`），那么 FPGA 数据输出到达 SPI Flash 在 $t_0-t_{data}$ 时刻（下图的 `d`），为了保证 $t_0-t_{data}$ 在 $-t_{clk}$ 时刻之前（下图的 `d -> b`）至少 $t_{su}$ 时间到达，可以得到表达式：

```wavedrom
{
  signal:
    [
      { name: "clk_fpga", wave: "p..", node: ".a" },
      { name: "clk_flash", wave: "p...", node: "..b", phase: 2.7 },
      { name: "data_fpga", wave: "3456", node: "..c", phase: 3.6 },
      { name: "data_flash", wave: "3456", node: "..d", phase: 3.4 }
    ],
  config: { hscale: 3 },
}
```

$$
t_0 - t_{data} > -t_{clk} + t_{su}
$$


化简一下，就可以得到 $t_0 > t_{data} + t_{su} - t_{clk}$，如果考虑极端情况，右侧 $t_{data}$ 取最大值，$t_{clk}$ 取最小值，就可以得到约束：

```tcl
set_output_delay -clock clk_sck -max [expr $tsu + $tdata_trace_delay_max - $tclk_trace_delay_min] [get_pins -hierarchical *STARTUP*/DATA_OUT[*]];
```

接下来考虑 output delay 的 min，这对应的是 hold time。此时的目标是数据到达 SPI Flash 寄存器的时候，距离上升沿时间超过了 $t_h$。按照同样的假设，如果 FPGA CCLK 时钟上升沿在 0 时刻（下图的 `a`），那么 SPI Flash 时钟上升沿在 $-t_{clk}$ 时刻（下图的 `b`）。假设 FPGA 数据输出时刻为 $t_0$（下图的 `c`），那么 FPGA 数据输出到达 SPI Flash 在 $t_0-t_{data}$ 时刻（下图的 `d`），为了满足 hold 条件，可以得到：

```wavedrom
{
  signal:
    [
      { name: "clk_fpga", wave: "p..", node: ".a" },
      { name: "data_fpga", wave: "3456", node: "..c", phase: 2.6 },
      { name: "clk_flash", wave: "p...", node: "..b", phase: 2.3 },
      { name: "data_flash", wave: "3456", node: "..d", phase: 2.2 },
    ],
  config: { hscale: 3 },
}
```

$$
t_0 - t_{data} < -t_{clk} - t_h
$$

化简以后，可以得到 $t_0 < t_{data} - t_{clk} - t_h$，按照极限来取，$t_{data}$ 取最小值，$t_{clk}$ 取最大值，就得到了最终的时序约束：

```tcl
set_output_delay -clock clk_sck -min [expr $tdata_trace_delay_min - $th - $tclk_trace_delay_max] [get_pins -hierarchical *STARTUP*/DATA_OUT[*]];
```

这样就可以实现 FPGA 和 SPI Flash 之间的正常通讯了。这里比较绕的就是时间轴的定义，和平常思考的方向是反过来的。而且，这里的 min 和 max 并不是指 $[\min, \max]$，而是 $(-\inf, \min] \cup [\max, \inf)$。代入上面的数据，可以得到 $\max=2.05, \min=-2.95, t_0 \in (\inf, -2.95] \cup [2.05, \inf)$。如果变化的时刻距离时钟上升沿太接近，就会导致在 SPI Flash 侧出现不满足 setup 或者 hold 约束的情况。

也可以换个角度来理解 min 和 max：对于同一个周期的时钟和数据来说，数据相对时钟有一个延迟，这个延迟不能太小，至少要满足 hold，所以这是一个最小的延迟；同时这个延迟不能太大，最多需要满足下一个时钟上升沿的 setup，所以这是一个最大的延迟。如果从这个角度来看，那就是延迟在一个 $[\min, \max]$ 的范围内。但是，这样在计算的时候就需要把时钟周期纳入到 $\max$ 的计算中，比如 $\max=t_c-t_{su}$。如果把坐标轴修改一下，原点变成原来的下一个时钟周期的上升沿，x 的正方向变成反向，此时公式里不会出现时钟周期，就可以得到上面的形式了。

### Artix 7 时序

对于更常见的 7 Series FPGA，比如 Artix 7，它采用的是 STARTUPE2 原语，只有时钟是通过 STARTUPE2 原语的 USRCCLKO 信号传递到 CCLK 引脚上的，其他数据信号都是需要在顶层信号绑定对应的引脚。在 AXI Quad SPI 文档中，描述了 STARTUPE2 所需要的时序约束：

```tcl
# You must provide all the delay numbers
# CCLK delay is 0.5, 6.7 ns min/max for K7-2; refer Data sheet
# Consider the max delay for worst case analysis
set cclk_delay 6.7
# Following are the SPI device parameters
# Max Tco
set tco_max 7
# Min Tco
set tco_min 1
# Setup time requirement
set tsu 2
# Hold time requirement
set th 3
# Following are the board/trace delay numbers
# Assumption is that all Data lines are matched
set tdata_trace_delay_max 0.25
set tdata_trace_delay_min 0.25
set tclk_trace_delay_max 0.2
set tclk_trace_delay_min 0.2
### End of user provided delay numbers
```

可以看到，这一部分和上面 UltraScale+ 部分差不多，只是多一个 `cclk_delay` 变量，这是因为 Artix 7 中，时钟只能创建到 USRCCLKO 引脚上。但是实际 SPI Flash 接收到的时钟，首先从 USRCCLKO 到 CCLK 引脚，然后再通过 PCB 上的线传播到 SPI Flash，所以需要手动添加一个偏移，这个偏移就是 USRCCLKO 到 CCLK 的延迟，可以在 [Artix 7 Data Sheet](https://www.xilinx.com/support/documentation/data_sheets/ds181_Artix_7_Data_Sheet.pdf) 里面看到：对于 1.0V，-2 速度的 FPGA，这个延迟最小值为 0.50ns，最大值为 6.70ns，这里采用了最大值。

剩下的约束，除了时钟部分以外，和上面分析的 UltraScale+ 时序约束计算方法是相同的。不同点在于，这里约束了从 AXI Quad SPI 到 STARTUPE2 的路由时延，从 0.1ns 到 1.5ns，然后又从 USRCCLKO 创建了一个分频 + 延迟 `cclk_delay` 纳秒的时钟，作为 SPI Flash 上 SCK 引脚的时钟。

```tcl
# this is to ensure min routing delay from SCK generation to STARTUP input
# User should change this value based on the results
# having more delay on this net reduces the Fmax
set_max_delay 1.5 -from [get_pins -hier *SCK_O_reg_reg/C] -to [get_pins -hier
*USRCCLKO] -datapath_only
set_min_delay 0.1 -from [get_pins -hier *SCK_O_reg_reg/C] -to [get_pins -hier
*USRCCLKO]
# Following command creates a divide by 2 clock
# It also takes into account the delay added by STARTUP block to route the CCLK
create_generated_clock -name clk_sck -source [get_pins -hierarchical
*axi_quad_spi_1/ext_spi_clk] [get_pins -hierarchical *USRCCLKO] -edges {3 5 7}
-edge_shift [list $cclk_delay $cclk_delay $cclk_delay]
# Data is captured into FPGA on the second rising edge of ext_spi_clk after the SCK
falling edge

# Data is driven by the FPGA on every alternate rising_edge of ext_spi_clk
set_input_delay -clock clk_sck -max [expr $tco_max + $tdata_trace_delay_max +
$tclk_trace_delay_max] [get_ports IO*_IO] -clock_fall;
set_input_delay -clock clk_sck -min [expr $tco_min + $tdata_trace_delay_min +
$tclk_trace_delay_min] [get_ports IO*_IO] -clock_fall;
set_multicycle_path 2 -setup -from clk_sck -to [get_clocks -of_objects [get_pins
-hierarchical */ext_spi_clk]]
set_multicycle_path 1 -hold -end -from clk_sck -to [get_clocks -of_objects [get_pins
-hierarchical */ext_spi_clk]]
# Data is captured into SPI on the following rising edge of SCK
# Data is driven by the IP on alternate rising_edge of the ext_spi_clk
set_output_delay -clock clk_sck -max [expr $tsu + $tdata_trace_delay_max -
$tclk_trace_delay_min] [get_ports IO*_IO];
set_output_delay -clock clk_sck -min [expr $tdata_trace_delay_min - $th -
$tclk_trace_delay_max] [get_ports IO*_IO];
set_multicycle_path 2 -setup -start -from [get_clocks -of_objects [get_pins
-hierarchical */ext_spi_clk]] -to clk_sck
set_multicycle_path 1 -hold -from [get_clocks -of_objects [get_pins -hierarchical */
ext_spi_clk]] -to clk_sck
```

一个 Artix 7 上配置 STARTUP SPI Flash 的例子 [io_timings.xdc](https://github.com/trivialmips/nontrivial-mips/blob/master/vivado/NonTrivialMIPS.srcs/constrs_1/new/io_timings.xdc) 可供参考。
