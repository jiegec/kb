# SPI

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

想要读取数据的话，就要发送 READ_SINGLE_BLOCK 命令，参数就是要读取的 Block 地址。SD 卡回先回复一个字节的响应，然后开始发数据，数据从 Start Block Token 开始，然后是一个 Block 的数据（通常是 512 字节），最后再两个字节的 CRC16。

写数据则是发送 WRITE_BLOCK 命令，SD 卡回复一个字节的响应，然后控制器开始传输数据，数据从 Start Block Token 开始，接着是要写入的数据，最后是两个字节的 CRC16，然后 SD 卡回复一个字节的响应，标志着写入成功。

## SPI 以太网控制器

有一些以太网产品提供了 SPI 接口，例如 [KSZ8851SNL/SNLI](https://ww1.microchip.com/downloads/aemDocuments/documents/UNG/ProductDocuments/DataSheets/KSZ8851SNL-Single-Port-Ethernet-Controller-with-SPI-DS00002381C.pdf)，集成了 MAC 和 PHY，直接连接 MDI/MDI-X 接口，虽然最高只支持百兆网，但是接口上确实非常简单。

SPI 上发送的命令就两类：一类是读写寄存器，一类是读写 RX/TX FIFO。

## 键盘和触摸板

一些型号的苹果电脑的键盘和触摸板是通过 SPI 接口访问的，在 Linux 中有相应的 applespi 驱动。

## SPI vs I2C

SPI 和 I2C 的区别在于，前者信号更多，全双工传输；后者信号更少，半双工传输。SPI 通过 CS 信号选择 Slave 芯片，I2C 通过地址进行区分。此外 I2C 还需要 Pull up resistor，这样如果没有设备响应，就会 NACK。

一些芯片提供了 SPI 或 I2C 的选项：共用两个信号，允许用户选择用 I2C 还是 SPI。例如 [WM8731](http://cdn.sparkfun.com/datasheets/Dev/Arduino/Shields/WolfsonWM8731.pdf)，既支持 I2C（记为 2-wire mode），又支持 SPI（记为 3-wire mode）。一般这种时候，SPI 和 I2C 就是用来配置一些寄存器的，另外可能还有一些接口，例如 WM8731 负责声音数据传输的实际上是 I2S。
