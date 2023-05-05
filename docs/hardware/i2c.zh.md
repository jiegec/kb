# I2C

## 接口

I2C 协议涉及到两个信号：

- SCL: 时钟信号，Master -> Slave
- SDA：数据信号，Master <-> Slave

由于只有一个数据信号，所以 SDA 由 Master 和 Slave 轮流输出。一次请求的开始条件是，SDA 从 1 变成 0，之后 SCL 从 1 变成 0。开始请求以后，每次 SCL 上升沿采样一位的数据。请求结束时，SCL 从 0 变成 1，然后 SDA 从 0 变成 1。一次请求的波形如下：

```wavedrom
{
  signal:
    [
      { name: "scl", wave: "1.0101010|.101..."},
      { name: "sda", wave: "10....1..|0....1.", phase: -0.1},
      { name: "i2c", wave: "34.5.....|6.7....", data: ["idle", "start", "data", "ack", "stop"]},
    ]
}
```

1. idle 阶段，scl 和 sda 都是 1
2. start 阶段，首先是 sda 变成 0，之后是 scl 变成 0
3. data/ack 阶段，在 scl 上升沿采样数据，在 scl 下降沿（准确来说，负半周期）修改数据
4. stop 阶段，首先是 scl 变成 1，之后是 sda 变成 1

传输数据的时候，需要保证 sda 在 scl 正半周期的时候保持不变。如果变了，那就是 start 或者 stop。因此，在 data/ack 阶段，建议保证 sda 的变化相比 scl 下降沿有一个延迟（Hold Time，一般的要求是 Min 0us）。实现方法可能是在分频的时候，先拉低 scl，下一个周期再修改 sda。

这里的 data/ack 指的则是传输的具体内容：例如 master 要传输 7 位的地址和 1 位的读使能，响应地址的 slave 要返回 ack；之后，无论是 master 还是 slave 发送数据，接收的一方都要返回 ack。ack 是低有效，意味着 0 表示成功（ack），1 表示失败（nack）。

由于 sda 带有上拉电阻，所以如果没有 slave 响应，ack 阶段的 sda 就会变成 1，意味着失败（nack）。

在此基础上，可以设计上层协议，例如 [WM8731](http://cdn.sparkfun.com/datasheets/Dev/Arduino/Shields/WolfsonWM8731.pdf)，支持通过 I2C 写入内部寄存器，一次写操作分为以下步骤：

1. start
2. master 发送 7 位的设备地址和 0（表示写），slave 发送 ack
3. master 发送 7 位的寄存器地址 和 1 位的寄存器数据，slave 发送 ack
4. master 发送 8 位的寄存器数据，slave 发送 ack
5. stop

这里的第二步发送的 7 位地址 + 读/写位是标准的，I2C Slave 都会根据 7 位地址来决定是否由自己来响应。此后的数据的定义，则是各个芯片按照各自的协议来进行。

为了让多个同型号 I2C 芯片可以同时使用，通常芯片提供了一些引脚来配置它的地址，那么在设计的时候，给不同的芯片设置不同的地址，就解决了地址冲突的问题。

## I2C EEPROM

以 [AT24C32/AT24C64](https://ww1.microchip.com/downloads/en/devicedoc/doc0336.pdf) 为例，它提供了一个 I2C 接口的 EEPROM，支持如下操作：

写入数据：start，7 位设备地址，W，ACK；写入地址的高 8 位，ack；写入地址的低 8 位，ack；数据的每个字节，ack；最终 stop。

读取数据：start，7 位设备地址，W，ack；读取地址的高 8 位，ack；读取地址的低 8 位，ack；start，7 位设备地址，R，ack；数据的每个字节，ack；最终不想读的时候 nack，stop。

可以看到，这里设计成写操作的时候，只有 Master 到 Slave 的数据传输，反过来读操作的时候，只有 Slave 到 Master 的数据传输。因此，为了传输读取的地址，要首先“写入”读取的地址，再进行一次读操作，把数据读出来。

## I2C Audio Codec

上面的例子中的 [WM8731](http://cdn.sparkfun.com/datasheets/Dev/Arduino/Shields/WolfsonWM8731.pdf) 实际上就是一个 Audio Codec，可以通过 I2C 对其寄存器进行写入。WM8731 的寄存器地址有 9 位，每个寄存器有 8 位的数据，因此写入流程是：start，7 位设备地址，W，ack；7 位寄存器地址，1 位寄存器数据，ack；8 位寄存器数据，ack；stop。

## I2C Sensor

举一个传感器的例子：[PAJ7620U2: Integrated Gesture Recognition Sensor ](https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/unit/gesture/paj7620u2_datasheet.pdf)，它也提供了一个寄存器读写的接口，支持如下操作：

单次写入：start，7 位设备地址，W，ack；8 位地址，ack；8 位数据，ack；stop。

单次读取：start，7 位设备地址，W，ack；8 位地址，ack；stop；start，7 位设备地址，R，ack；8 位数据，nack；stop。这里的读取也拆成了两步：第一步“写入”读取的地址，第二步读取出数据。最后的 nack 表示 master 不需要读取更多的数据。

如果要批量读取的话，只要在单次读取的基础上，读取数据的时候发 ack，等到不需要继续读的时候再发 nack，就可以连续读取多个寄存器的数据。

这些命令格式和上面的 I2C EEPROM 基本是一样的。

颜色传感器 [TCS3472](https://cdn-shop.adafruit.com/datasheets/TCS34725.pdf) 的命令格式也是类似的。
