# 显示接口

## VGA

VGA 采用 15-pin 的连接器，包括 RGB 三种颜色，HSync 和 VSync 信号，还有可选的 DDC 接口。每种颜色对应一个 pin，采用模拟信号方式传输。VGA 有不同的分辨率和刷新率时序，对应不同的像素时钟频率，以及 HSync 和 VSync 的波形。

VGA 不支持传输音频。

参考：[Wikipedia](https://en.wikipedia.org/wiki/Video_Graphics_Array)

## DVI

DVI 有不同的版本，DVI-A 兼容 VGA 接口，只传输模拟信号；DVI-D 则是采用 TMDS 差分信号传输数字信号，兼容 HDMI；DVI-I 则兼容 DVI-A 和 DVI-D。

因此 DVI 转 VGA 或者 DVI 转 HDMI 的转换器内部不需要做数模转换，但是要求另一侧的设备支持相应的传输形式，例如 DVI 转 VGA 出来得到的还是模拟信号，如果另一侧的设备只支持在 DVI 上走数字信号，则无法正常工作。

DVI 在传输数字信号的时候，可以采用 3 对（Single link）或者 6 对（Dual link）TMDS 差分信号传输视频信号，此外还有一对 TMDS 差分时钟。其中 Single link 模式和 HDMI 是兼容的。

TMDS 每个时钟周期内，传输 8 bit 的数据，这 8 位的数据经过 8b/10b 编码在差分对上传输。因此对于 165 MHz 的 TMDS 时钟，传输视频数据的速率是 $165 \mathrm{MHz} * 3 * 8 = 3.96 \mathrm{Gbps}$。

DVI 不支持传输音频。

参考：[Wikipedia](https://en.wikipedia.org/wiki/Digital_Visual_Interface)

## HDMI

HDMI 在三对 TMDS 差分信号上传输数据，此外还有一对 TMDS 差分时钟和 DDC。常见的连接器是 Type A，有时候也能看到比较小的 Mini HDMI（Type C）和更小的 Micro HDMI（Type D）。

HDMI 除了传输视频，还支持传输音频。

HDMI 随着版本更新，逐渐提高了 TMDS 时钟频率。HDMI 1.0 版本和 DVI 一样，最高 TMDS 时钟是 165 MHz，不计入 8b/10b 编码损耗的话（下同），传输速率是 $165 \mathrm{MHz} * 3 * 10 = 4.95 \mathrm{Gbps}$；HDMI 1.3 版本把 TMDS 时钟提高到了 340 MHz，传输速率达到 $340 \mathrm{MHz} * 3 * 10 = 10.2 \mathrm{Gbps}$。HDMI 2.0 版本提高到了 600MHz，传输速率达到 $600 \mathrm{MHz} * 3 * 10 = 18 \mathrm{Gbps}$。

HDMI 2.1 不再使用单独的 TMDS 时钟差分对，把最后一对也用来传输数据，把数据编码从 8b/10b 改成了 16b/18b，传输速率达到 $4 * 12 \mathrm{Gbps} = 48 \mathrm{Gbps}$，相比 HDMI 2.0 有了巨大的提升。按照 16b/18b 算，数据速率是 42.7 Gbps，但 HDMI 2.1 还有额外的 FEC 开销（RS(255,251)），折算下来是 $48 \mathrm{Gbps} * 16 / 18 * 251 / 255 = 42.0 \mathrm{Gbps}$。

下面是这几代 HDMI 的对比，其中 HDMI 2.1 版本没考虑 FEC 开销：

|      | 1.0        | 1.3        | 2.0       | 2.1       |
| ---- | ---------- | ---------- | --------- | --------- |
| 传输速率 | 4.95 Gbps  | 10.2 Gbps  | 18 Gbps   | 48 Gbps   |
| 数据速率 | 3.96 Gbps  | 8.16 Gbps  | 14.4 Gbps | 42.0 Gbps |
| 编码方式 | 8b/10b     | 8b/10b     | 8b/10b    | 16b/18b   |
| 分辨率  | 1080p 60Hz | 1440p 75Hz | 4k 60Hz   | 8k 30Hz   |

HDMI 2.1 还支持 DSC 视频流压缩，可以支持更高的分辨率，如 8k 60Hz 甚至 8k 120Hz。

参考：[Wikipedia](https://en.wikipedia.org/wiki/HDMI) [HDMI 2.1 FEC RX IP Core](https://www.hardent.com/pdf/Rambus-Hardent_HDMI_2_1_FEC_RX_IP.pdf)

## DisplayPort

DisplayPort 采用四对差分对来传输数据，支持视频和音频等。

DisplayPort 1.0 版本支持 10.8 Gbps 的传输速率（编码方式 8b/10b，因此数据 8.64 Gbps）。DisplayPort 1.2 版本速率翻倍，达到了 21.6 Gbps（数据 17.28 Gbps）。DisplayPort 1.3 进一步提高到了 32.4 Gbps（数据 25.92 Gbps）。DisplayPort 2.0 进一步提高到 80 Gbps（编码方式 128b/132b），数据速率 77.37 Gbps（计算公式不明）。

参考：[Wikipedia](https://en.wikipedia.org/wiki/DisplayPort)

## SDI

SDI 全称 Serial Digital Interface，在同轴电缆上，串行传输视频数据。

参考：[Wikipedia](https://en.wikipedia.org/wiki/Serial_digital_interface)
