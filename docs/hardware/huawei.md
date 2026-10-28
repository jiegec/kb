# 华为芯片

## 麒麟

注：以下的第几代是我自己按微架构划分，并非官方说法。

### 一代

#### 麒麟 9000S

- 搭载于：Mate 60
- 1x 大核（2.62 GHz, 带 SMT，0xd02），3x 中核（2.15 GHz, 带 SMT，0xd42），4x 小核 Cortex-A510（1.53 GHz, 无 SMT）
- 大核中核有超线程，共 8 核 12 线程
- Maleoon 910, 4CU, 1024 ALU
- 丝印 Hi36A0 GFCV120

来源：

- [麒麟 9000s 芯片性能详细解析——华为 mate60 系列！](https://www.zhihu.com/tardis/zm/art/659619471?source_id=1003)
- [Kirin 9000S Review: How Powerful is Huawei Mate60 Pro?](https://www.youtube.com/watch?v=SCRIFe0uaac)

### 二代

#### 麒麟 9010

- 搭载于：Pura 70 系列、MatePad Mini 典藏版
- 1x 大核（0xd03，最大 2.30 GHz，带 SMT），3x 中核（0xd42，最大 2.18 GHz，带 SMT），4x 小核 Cortex-A510（impl 0x41, part 0xd46，最大 1.55 GHz）
- 8 核，2+6+4=12 线程
- all CPU features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint svei8mm svebf16 i8mm bf16 bti
- 大核中核有超线程
- Maleoon 910, 4CU
- 丝印 Hi36A0 GFCV121

来源：

- [华为 Pura70 能效分析：架构进步很大！](https://www.bilibili.com/video/BV1az421D7Fk)
- [HiSilicon Kirin 9010](https://www.notebookcheck.net/HiSilicon-Kirin-9010-Processor-Benchmarks-and-Specs.855471.0.html)
- [Huawei’s Kirin 9010 Is a Reality Check for China’s Semiconductor Ambitions](https://zh.ifixit.com/News/95646/huaweis-kirin-9010-is-a-reality-check-for-chinas-semiconductor-ambitions)

#### 麒麟 9010B

- 搭载于：MatePad Mini、MatePad Mini 悦读版 鸿蒙焕新版
- 6 核 9 线程，1x 2.19（part 0xd03）+ 2x 2.18（part 0xd42）+ 3x 1.40 GHz（Cortex-A510）
- 麒麟 9010 降频，去掉一中一小
- GPU: Maleoon 910, 3CU

来源：

- [HUAWEI MLR-AL00 Geekbench 7](https://browser.geekbench.com/v7/cpu/613986)
- [HUAWEI MLR-AL00 Geekbench 7 Vulkan](https://browser.geekbench.com/v7/gpu/9477)
- [HUAWEI MLR-AL00 Geekbench 6 Compute（OpenCL：Maleoon 910，3CU）](https://browser.geekbench.com/v6/compute/6944237)
- [华为商城 MatePad Mini](https://www.vmall.com/product/10086287244006.html)


#### 麒麟 X90

- 搭载于：MatePad Edge 液冷版、MateBook Pro、MateBook Pro 24GB/512GB、MateBook 14 鸿蒙版、MateBook Fold 非凡大师（X90）
- 4+4+2, 20 threads
- part id 0xd03（8 threads，4 核，同麒麟 9010 大核，2.32 GHz）, 0xd43（8 threads，4 核，2.05 GHz）, 0xd42（4 threads，2 核，同麒麟 9010 中核，2.01 GHz），都带 SMT
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint svei8mm svebf16 i8mm bf16 dgh bti ecv
- Charlotte Pro
- Maleoon 916, 6CU @950MHz

来源：

- [【老戴】继续来折腾鸿蒙电脑！有你们最关心的 CPU 信息，设备树长啥样，包管理能不能用...](https://www.bilibili.com/video/BV1UY5VzMEj9/)
- [如何看待在 5 月 8 日鸿蒙电脑技术与生态沟通会上亮相的首款鸿蒙电脑，有哪些信息值得关注？ - 雷燚音的回答 - 知乎](https://www.zhihu.com/question/1903763170587304858/answer/1903943055951794515)
- [Huawei's Kirin X90 may be the company's 'Apple Silicon' moment — Matebook Pro 2025 features in-house hardware and software](https://www.tomshardware.com/pc-components/cpus/huaweis-kirin-x90-may-be-the-companys-apple-silicon-moment-matebook-pro-2025-features-in-house-hardware-and-software)
- [HUAWEI HPR-W72](https://browser.geekbench.com/v6/cpu/16545330)
- [Kirin X90/X90 Plus/XE90 参数实测（916 6CU、935 6CU）](https://www.sina.cn/news/detail/5328665761284126.html)

#### 麒麟 X90 Plus

- 搭载于：MateBook Pro 麒麟 X90 Plus、MateBook Fold 非凡大师（X90 Plus）
- 4(2.45 GHz, 0xd03)+4(2.05 GHz, 0xd43)+2(2.01 GHz, 0xd42), 20 threads
- 麒麟 X90 提频
- Maleoon 916, 6CU @950MHz

来源：

- [HUAWEI SLM-W24](https://browser.geekbench.com/v7/gpu/120510)
- [HUAWEI SLM-W24 Vulkan](https://browser.geekbench.com/v7/gpu/228311)
- [Kirin X90/X90 Plus/XE90 参数实测（X90 Plus 为 916 6CU）](https://www.sina.cn/news/detail/5328665761284126.html)

#### 麒麟 X90A

- 搭载于：MatePad Edge WiFi
- 8C16T，3+3+2：3x 2.07 GHz（0xd03，带 SMT），3x 1.85 GHz（0xd43，带 SMT），2x 1.81 GHz（0xd42，带 SMT）
- 麒麟 X90 降频，减一大一中核
- Maleoon 916B（CU 未知）

来源：

- [华为 MatePad Edge 芯片不是麒麟 X90，而是 X90A](https://www.sina.cn/news/detail/5235872261739929.html)
- [HUAWEI MatePad Edge 规格参数](https://consumer.huawei.com/cn/tablets/matepad-edge/specs/)
- [华为 MatePad Edge 首发猫头鹰散热架构 + 液冷技术](https://pad.zol.com.cn/1129/11294648_param.html)

### 三代

#### 麒麟 8000S

- 搭载于：畅享 100、畅享 100m
- 5 核 7 线程：2x 中核（0xd46，2.05 GHz，带 SMT），3x 小核（0xd23，1.31 GHz），无大核（0+2+3 两簇）
- 麒麟 9020 降频，砍一大核一中核一小核
- Maleoon 920C, 1CU

来源：

- [麒麟 8000S/8020A/9025 芯片参数对比](https://weibo.com/2/detail/5357226468049171)
- [麒麟 9020/8020 家族参数整理](https://www.sina.cn/news/detail/5357171013324123.html)
- [华为畅享 100 手机发布：搭载麒麟 8000S 芯片，1399 元起](https://m.ithome.com/html/1018922.htm)
- [华为畅享 100 系列发布 全系自研麒麟芯片 1399 元起步](https://phone.cnmo.com/news/821290.html)

#### 麒麟 8020

- 搭载于：nova 14 Pro、nova 14 Ultra、畅享 100 Pro Max 512GB、nova 15、nova 16 SE、nova 16z、MatePad 11.5 鸿蒙焕新版 全网通
- 1x 大核（0xd05，带 SMT，2.29 GHz），3x 中核（0xd46，带 SMT，2.05 GHz），4x 小核（0xd23，无 SMT，1.31 GHz）
- 麒麟 9020 降频
- 大核中核有超线程，共 12 线程
- Maleoon 920C, 2CU

来源：

- [华为 nova 14 Pro/Ultra 首销：3499 元起 首发麒麟 8020 芯片](https://m.mydrivers.com/newsview/1049373.html)
- [麒麟 8020 家族参数整理（含 8020/8020A/8000S）](https://www.sina.cn/news/detail/5357171013324123.html)

#### 麒麟 8020A

- 搭载于：畅享 100 Pro、畅享 100 Pro Max 128/256GB
- 6C9T：1x 大核（0xd05，带 SMT，2.29 GHz），2x 中核（0xd46，带 SMT，2.05 GHz），3x 小核（0xd23，1.31 GHz）
- 麒麟 9020 降频，砍一中核一小核
- Maleoon 920C, 2CU

来源：

- [麒麟 8000S/8020A/9025 芯片参数对比](https://weibo.com/2/detail/5357226468049171)
- [最高配麒麟 8020+8800mAh 大电池？华为畅享 100 系列定档 10.28](https://www.pcpop.com/article/6954648.shtml)
- [1999 元起！华为畅享 100 Pro Max 发布：麒麟 8020+鸿蒙 7](https://m.163.com/dy/article/LABD3H8T0511CPVM.html)

#### 麒麟 9010S

- 搭载于：Pura 80、Pura 90、nova 16、nova 16 Pro、nova 16 Ultra
- 1x 大核（0xd05，2.50 GHz），3x 中核（0xd46，2.05 GHz），4x 小核（0xd23，1.50 GHz，无 SMT）
- 8 核 12 线程
- Maleoon 920C, 2CU

来源：

- [Pura 80 数字版搭载 Kirin 9010S](https://www.coolapk.com/feed/66237183)
- [HUAWEI HED-LX9](https://browser.geekbench.com/v6/compute/6784045)

#### 麒麟 9020

- 搭载于：Mate 70 Pro+、Mate 80、Pura X、Pura X 典藏版
- 1x 大核（0xd05，带 SMT, 2.50 GHz），3x 中核（0xd46，带 SMT, 2.15 GHz），4x 小核（0xd23，无 SMT, 1.60 GHz）
- 大核中核有超线程，共 8 核 12 线程
- Maleoon 920, 4CU, 1024 ALU
- 丝印 Hi36C0 GFCV110

来源：

- [Huawei Mate 70 Pro+: Exploring the HiSilicon Kirin 9020 Processor](https://www.techinsights.com/blog/huawei-mate-70-pro-exploring-hisilicon-kirin-9020-processor)
- [Details on the new Kirin 9020 chipset surface, here's what is inside the new Mate 70 series](https://www.gsmarena.com/details_on_the_new_kirin_9020_chipset_surface_heres_what_is_inside_the_new_mate_70_series-news-65497.php)
- [HiSilicon Kirin 9020 from Mate 70 Pro Plus - Die Analysis](https://library.techinsights.com/public/hg-asset/e71466a2-64ef-410a-af5f-b3d001bd2318?utm_source=blog&utm_medium=website&utm_campaign=Huawei%20Mate%2070%20Pro%20Series#moduleName=Search&reportCode=FCT-2412-801&subscriptionId=null&channelId=null&reportName=HiSilicon+Kirin+9020+from+Mate+70+Pro+Plus+-+Die+Analysis)
- [华为 Mate70 Pro+ 性能分析：麒麟 9020 来啦！](https://www.bilibili.com/video/BV1j6iYYHEYG)
- [HUAWEI PLA-AL10](https://browser.geekbench.com/v6/cpu/9233574)
- [nova 14 ultra 的 cpu 信息](https://www.coolapk.com/feed/64975023)

Pura X 版本：丝印 Hi36C0 GFCV111

来源：

- [华为 Pura X 发售第一时间又消费了！今年最惊喜的拆解，全新的 9020 换封装工艺了，CPU 不一样了！](https://www.bilibili.com/video/BV1qAZzY4Eyj)
- [HUAWEI VDE-AL00（Pura X）Geekbench 7](https://browser.geekbench.com/v7/cpu/677065)

#### 麒麟 9020A

- 搭载于：Mate 70 Pro 优享版、Mate 70 Air 16GB
- 1x 大核（0xd05，带 SMT, 2.40 GHz），3x 中核（0xd46，带 SMT, 2.00 GHz），4x 小核（0xd23，无 SMT, 1.60 GHz）
- 麒麟 9020 降频
- 大核中核有超线程，共 8 核 12 线程
- Maleoon 920, 3CU

来源：

- [华为 Mate 70 Air 首次可选 CPU：麒麟 9020A、麒麟 9020B 有何区别 官方客服回应](https://m.mydrivers.com/newsview/1084793.html)
- [麒麟 9020 家族参数整理（含 9020A/9020B）](https://www.sina.cn/news/detail/5357171013324123.html)

#### 麒麟 9020B

- 搭载于：Mate 70 Air 12GB
- 6C9T：1x 2.40 GHz（0xd05，带 SMT），2x 2.00 GHz（0xd46，带 SMT），3x 1.60 GHz（0xd23）
- 麒麟 9020 降频，减一中核
- Maleoon 920R, 3CU

来源：

- [华为 Mate 70 Air 首次可选 CPU：麒麟 9020A、麒麟 9020B 有何区别 官方客服回应](https://m.mydrivers.com/newsview/1084793.html)
- [麒麟 9020 家族参数整理（含 9020A/9020B）](https://www.sina.cn/news/detail/5357171013324123.html)

#### 麒麟 9025

- 搭载于：Pura 90 Plus
- 麒麟 9020 提频
- 1x 大核（0xd05，带 SMT，2.60 GHz），3x 中核（0xd46，带 SMT，2.15 GHz），4x 小核（0xd23，无 SMT，1.60 GHz），共 8 核 12 线程
- Maleoon 920, 4CU

来源：

- [华为 Pura90 Plus 手机配置曝光：2.60GHz 麒麟 9025 芯片](https://www.ithome.com/1/017/425.htm)
- [麒麟 9025 下周登场：主频升至 2.60GHz 华为 Pura 90 Plus 首发搭载](https://news.17173.com/content/10242026/190105827.shtml)
- [华为 Pura 90 Plus 正式发布！搭载麒麟 9025 处理器](https://phone.cnmo.com/news/821293.html)
- [消息称华为 Pura 90 Plus 手机搭载麒麟 9025 处理器](https://www.163.com/dy/article/L9TPL4BC0511B8LM.html)
- [麒麟 8000S/8020A/9025 芯片参数对比](https://weibo.com/2/detail/5357226468049171)
- [麒麟 9020/8020 家族参数整理](https://www.sina.cn/news/detail/5357171013324123.html)

#### 麒麟 T82B

- 搭载于：MatePad 11.5 鸿蒙焕新版 WiFi
- 8 核 12 线程，1x 2.29（part 0xd05）+ 3x 2.05（part 0xd46）+ 4x 1.31 GHz（part 0xd23）
- 麒麟 9020 降频
- GPU: Maleoon 920C（CU 未知）

来源：

- [HUAWEI TXZ-W10 Geekbench 7](https://browser.geekbench.com/v7/cpu/46698)
- [HUAWEI TXZ-W10 Geekbench 7 Vulkan](https://browser.geekbench.com/v7/gpu/7691)
- [华为商城 MatePad 11.5 鸿蒙焕新版](https://www.vmall.com/product/10086070683245.html)

#### 麒麟 T82

- 搭载于：MatePad 11.5 鸿蒙焕新版 柔光版
- 1x 2.29（0xd05）+ 3x 2.05（0xd46）+ 4x 1.31 GHz（0xd23），8 核 12 线程
- GPU: Maleoon 920C（CU 未知）

来源：

- [HiSilicon Kirin T82](https://www.notebookcheck.net/HiSilicon-Kirin-T82-Processor-Benchmarks-and-Specs.1104372.0.html)
- [华为商城 MatePad 11.5 鸿蒙焕新版](https://www.vmall.com/product/10086070683245.html)

#### 麒麟 T92

- 搭载于：MatePad Pro 13.2" 2025、MatePad Pro 12.2" 2025
- 8C12T：1x 2.50 GHz（0xd05，带 SMT），3x 2.15 GHz（0xd46，带 SMT），4x 1.60 GHz（0xd23）
- Maleoon 920, 4CU
- 与麒麟 9020 规格一致

来源：

- [麒麟 9020 家族参数整理（含 T92/T92A/T92B/T92C/T92D）](https://www.sina.cn/news/detail/5357171013324123.html)
- [HUAWEI MatePad Pro 13.2-inch Specifications](https://download-c-retail.huawei.com/en/tablets/matepad-pro-13-2/specs/)


#### 麒麟 T92C

- 搭载于：MatePad 11.5 S 2025 灵动版、MatePad 11.5 S 鸿蒙焕新版 灵动款
- 6 核 9 线程，1x 2.30（part 0xd05）+ 2x 2.00（part 0xd46）+ 3x 1.60 GHz（part 0xd23）
- 麒麟 9020 降频，少一中一小核
- GPU: Maleoon 920A, 3CU（GB Compute 报 Maleoon 920）

来源：

- [HUAWEI SLG-W50 Geekbench 7](https://browser.geekbench.com/v7/cpu/532113)
- [HiSilicon Kirin T92C](https://www.notebookcheck.net/HiSilicon-Kirin-T92C-Processor-Benchmarks-and-Specs.1219777.0.html)
- [HUAWEI SLG-W50 Geekbench 6 Compute（OpenCL：3CU）](https://browser.geekbench.com/v6/compute/6926703)
- [华为商城 MatePad 11.5 S 鸿蒙焕新版](https://www.vmall.com/product/10086693978514.html)

#### 麒麟 T92D

- 搭载于：MatePad 11.5 S 2025 活力版、MatePad 11.5 S 鸿蒙焕新版 活力版
- 8 核，1x 2.40（part 0xd05）+ 3x 2.00（part 0xd46） + 4x 1.60 GHz（part 0xd23）
- 麒麟 9020 降频
- GPU: Maleoon 920（CU 未知）

来源：

- [HUAWEI SLG-W10 Geekbench 7](https://browser.geekbench.com/v7/cpu/597088)
- [HUAWEI SLG-W10 Geekbench 7 Vulkan](https://browser.geekbench.com/v7/gpu/273774)
- [华为商城 MatePad 11.5 S 鸿蒙焕新版](https://www.vmall.com/product/10086693978514.html)

### 四代

#### 麒麟 9030

- 搭载于：Mate 80 Pro 12GB、Mate 90
- 1x 大核（带 SMT，2.70 GHz，0xd06），3x 中核（带 SMT，2.27 GHz，0xd47），4x 小核（无 SMT，1.72 GHz，0xd24），共 8 核 12 线程
- Maleoon 935A, 5CU, 1800 ALU

来源：

- [Kirin 9030 vs Kirin 9030 Pro: Major differences between new chips](https://www.huaweicentral.com/kirin-9030-vs-kirin-9030-pro-major-differences-between-new-chips/)
- [酷安](https://www.coolapk.com/feed/68880017)
- [华为商城 Mate 80 Pro（12GB 为 9030）](https://www.vmall.com/product/10086476013098.html)

#### 麒麟 9030 Pro

- 搭载于：Mate 80 Pro 16GB、Mate 80 Pro Max 风驰版、Mate 80 RS 非凡大师
- 1x 大核（带 SMT，2.75 GHz，0xd06），4x 中核（带 SMT，2.27 GHz，0xd47），4x 小核（无 SMT，1.72 GHz，0xd24），共 9 核 14 线程
- Maleoon 935, 6CU, 2160 ALU

来源：

- [Kirin 9030 vs Kirin 9030 Pro: Major differences between new chips](https://www.huaweicentral.com/kirin-9030-vs-kirin-9030-pro-major-differences-between-new-chips/)
- [酷安](https://www.coolapk.com/feed/68880017)
- [华为商城 Mate 80 Pro（16GB 为 9030 Pro）](https://www.vmall.com/product/10086476013098.html)

#### 麒麟 9030S

- 搭载于：Pura X View、Pura 90 Pro、Pura 90 Pro Max
- 1x 大核（带 SMT，2.70 GHz，0xd06），3x 中核（带 SMT，2.15 GHz，0xd47），4x 小核（无 SMT，1.62 GHz，0xd24），共 8 核 12 线程
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint svei8mm svebf16 i8mm bf16 dgh bti
- GPU: Maleoon 935F, 3CU（T93S 为同规格平板版，3CU；T93SD 为 2CU）

来源：

- [华为 Pura 90 Pro / Pro Max 手机开售：首发麒麟 9030S 芯片，售价 5499 元起](https://m.ithome.com/html/0944744.htm)
- [HUAWEI Pura 90 Pro Max 规格参数](https://consumer.huawei.com/cn/phones/pura90-pro-max/specs/)
- [HUAWEI SCA-LX9 Geekbench 7](https://browser.geekbench.com/v7/cpu/722104)
- [HUAWEI VOL-AL00（Pura X View）Geekbench 7](https://browser.geekbench.com/v7/cpu/725112)

#### 麒麟 XE90

- 搭载于：MateBook Pro S
- 1+4+4，14 线程
- Maleoon 935, 6CU @933MHz
- 与麒麟 9030 Pro 规格一致

来源：

- [华为发布麒麟 X90 Plus 和麒麟 XE90 PC 芯片](https://www.c114.net.cn/industry/106756.html)
- [华为发布 MateBook Pro S 系列：798 克超轻薄 AI 笔记本，搭载麒麟 XE90 芯片](https://nb.zol.com.cn/1231/12318351.html)
- [华为 MateBook Pro S 麒麟 XE90 芯片评测](https://www.sina.cn/news/detail/5336851805638220.html)
- [Kirin X90/X90 Plus/XE90 参数实测（XE90 为 935 6CU）](https://www.sina.cn/news/detail/5328665761284126.html)

#### 麒麟 T93 Pro

- 搭载于：MatePad Pro Max
- 9C14T（1+4+4）
- Maleoon 935, 6CU @933MHz
- 与麒麟 9030 Pro 规格相同

来源：

- [华为最强平板来了！MatePad Pro Max 发布：首发麒麟 T93 Pro 6199 元起](https://m.mydrivers.com/newsview/1126433.html)
- [Huawei Kirin T93 Pro — Specs, Benchmarks](https://innoreviews.com/soc/huawei-kirin-t93-pro)
- [The world's thinnest tablet is a powerhouse — MatePad Pro Max review](https://www.notebookcheck.net/The-world-s-thinnest-tablet-is-a-powerhouse-Huawei-MatePad-Pro-Max-review.1381968.0.html)

#### 麒麟 T93

- 搭载于：MatePad Pro Max 悦享款、MatePad Pro 12
- 8 核，1x 2.69（part 0xd06）+ 3x 2.27（part 0xd47） + 4x 1.72 GHz（part 0xd24）
- 与麒麟 9030 规格相同

来源：

- [HUAWEI GEM-W40 Geekbench 7](https://browser.geekbench.com/v7/cpu/627090)
- [华为商城 MatePad Pro Max](https://www.vmall.com/product/10086127502687.html)
- [华为商城 MatePad Pro 12](https://www.vmall.com/product/10086473135606.html)

#### 麒麟 T93A

- 搭载于：MatePad Pro 12 悦享款
- 8 核，1x 2.69（part 0xd06）+ 3x 2.27（part 0xd47）+ 4x 1.72 GHz（part 0xd24）
- GPU: Maleoon 935A，5CU（T93B 为 4CU，T93A 多 1CU）

来源：

- [HUAWEI DAL-W20 Geekbench 7](https://browser.geekbench.com/v7/cpu/728863)
- [4499 元起！MatePad Air 2026 发布](https://www.vgover.com/news/234346)
- [华为商城 MatePad Pro 12](https://www.vmall.com/product/10086473135606.html)

#### 麒麟 T93B

- 搭载于：MatePad Air 12 三代
- 8 核 12 线程，1x 2.69（0xd06）+ 3x 2.27（0xd47）+ 4x 1.72 GHz（0xd24），CPU 与 T93A 相同
- GPU: Maleoon 935B，4CU @933 MHz（比 T93A 少 1 CU）

来源：

- [4499 元起！MatePad Air 2026 发布：柔光版为 T93B，GPU 比 T93A 少一核](https://www.vgover.com/news/234346)
- [酷安：麒麟 T93B 的 GPU 为 4CU Maleoon 935B @933MHz](https://www.coolapk.com/feed/73629560)
- [华为商城 MatePad Air 12 三代](https://www.vmall.com/product/10086662006762.html)

#### 麒麟 T93C

- 搭载于：MatePad Air 12 三代 悦享款
- 8 核，4x 2.27（part 0xd47）+ 4x 1.72（part 0xd24）GHz
- 比麒麟 9030 少了一个大核，多了一个中核
- GPU: Maleoon 935B, 4CU

来源：

- [HUAWEI WKI-W00 Geekbench 7](https://browser.geekbench.com/v7/cpu/537841)
- [HiSilicon Kirin T93C](https://www.notebookcheck.net/HiSilicon-Kirin-T93C-Processor-Benchmarks-and-Specs.1431009.0.html)
- [HUAWEI WKI-W00 Geekbench 6 Compute（OpenCL：Maleoon 935B，4CU）](https://browser.geekbench.com/v6/compute/6869609)
- [华为商城 MatePad Air 12 三代](https://www.vmall.com/product/10086662006762.html)

#### 麒麟 T93S

- 搭载于：MatePad Air Z 柔光版（AST-W10）
- 8 核，1x 2.70（0xd06）+ 3x 2.15（0xd47）+ 4x 1.62 GHz（0xd24），与麒麟 9030S 规格相同
- GPU: Maleoon 935F，3CU

来源：

- [HUAWEI AST-W10 Geekbench 6 Compute（OpenCL：Maleoon 935F，3CU）](https://browser.geekbench.com/v6/compute/6913440)
- [华为 MatePad Air Z 核心配置公布：柔光版为 T93S](https://news.17173.com/content/09242026/110415388.shtml)
- [华为商城 MatePad Air Z](https://www.vmall.com/product/10086966141469.html)

#### 麒麟 T93SD

- 搭载于：MatePad Air Z（标准版普通屏，AST-W00）、MatePad Air Z 悦享款（AST-W30）
- 与 T93S 的区别：MatePad Air Z 柔光版（AST-W10）用 T93S，普通屏/悦享款用 T93SD
- 8 核，1x 2.70（0xd06）+ 3x 2.15（0xd47）+ 4x 1.62 GHz（0xd24）
- GPU: Maleoon 935F，2CU

来源：

- [HUAWEI AST-W00 Geekbench 6 Compute（Vulkan：Maleoon 935F）](https://browser.geekbench.com/v6/compute/6910487)
- [微博：T93SD 为 1+3+4，GPU Maleoon 935F 2CU](https://weibo.com/2/detail/5346829106675961)
- [华为 MatePad Air Z 平板配置公布：麒麟 T93SD 处理器](https://www.ithome.com/0/100/6606.htm)
- [华为 MatePad Air Z 核心配置公布：柔光版为 T93S，普通屏/悦享款为 T93SD](https://news.17173.com/content/09242026/110415388.shtml)
- [华为商城 MatePad Air Z](https://www.vmall.com/product/10086966141469.html)

#### 麒麟 9035

- 搭载于：Mate 90 Pro
- 1x 大核（带 SMT，2.85 GHz，0xd06），4x 中核（带 SMT，2.35 GHz，0xd47），4x 小核（无 SMT，1.72 GHz，0xd24），共 9 核 14 线程
- Maleoon 935, 6CU, 2160 ALU
- 麒麟 9030 Pro 提频版

来源：

- [华为 Mate 90 Pro 首发麒麟 9035：CPU 主频提升至 2.85GHz](https://m.mydrivers.com/newsview/1154483.html)
- [麒麟 9035 跑分曝光，Mate90 全系智拍](https://www.sina.cn/news/detail/5348456299234883.html)
- [华为 Mate 90 系列十大黑科技公布 麒麟 9050 性能提升 23%](https://phone.cnmo.com/news/821286.html)
- [史上最强麒麟芯片！华为大大方方介绍 9050 Pro](https://www.eet-china.com/mp/a528616.html)

### 五代

#### 麒麟 9050

- 搭载于：Mate 90 Pro Max 12GB
- 1x 3.00 GHz（0xd47）+ 2x 2.70 GHz（0xd48）+ 3x 2.20 GHz（0xd48）+ 2x 1.75 GHz（0xd25），8 核 14 线程
- GPU: Maleoon 955A, 5CU

来源：

- [HUAWEI CMM-AL00 Geekbench 7](https://browser.geekbench.com/v7/cpu/550340)
- [HUAWEI CMM-AL00 Geekbench 7 Vulkan](https://browser.geekbench.com/v7/gpu/272285)
- [Mate 90 四款 τ 芯片规格（9050 为 955A 5CU）](https://www.vgover.com/news/238952)
- [9499 元起！华为 Mate 90 Pro Max/典藏版发布：麒麟 9050 系列](http://m.mydrivers.com/newsview/1155018.html)
- [华为 Mate 90 系列发布，全系搭载"韬芯片"](https://www.21jingji.com/article/20261001/herald/7d6a3b19765793c2e2df7a4187d5dc35.html)

#### 麒麟 9050 Pro

- 搭载于：Mate 90 Pro Max 16GB、Mate 90 RS 非凡大师、Mate XT2 ULTIMATE DESIGN
- 1(3.10 GHz, SMT, 0xd07)+2(2.70 GHz, SMT, 0xd48)+4(2.20 GHz, SMT, 0xd48)+2(1.75 GHz, 0xd25) 核，9 核 16 线程
- 比麒麟 9050 频率高，多一个 2.20 GHz 中核
- Maleoon 955 6CU, 1.05 GHz

来源：

- [HUAWEI LAP-AL10 Geekbench 6](https://browser.geekbench.com/v6/compute/6868350)
- [HUAWEI LAP-AL10 Geekbench 7](https://browser.geekbench.com/v7/cpu/291822)
- [酷安](https://www.coolapk.com/feed/73629560)
- [9499 元起！华为 Mate 90 Pro Max/典藏版发布：麒麟 9050 系列](http://m.mydrivers.com/newsview/1155018.html)
- [史上最强麒麟芯片！华为大大方方介绍 9050 Pro](https://www.eet-china.com/mp/a528616.html)
- [中國產晶片實力解密 華為 Mate 90 Pro Max 跑分曝光](https://www.eprice.com.tw/mobile/talk/102/5827128/1/m/5827140/)
- [韬定律表现如何！麒麟 9050 完整性能测试](https://m.mydrivers.com/newsview/1150918.html)
- [HUAWEI CMM-AL10 Geekbench 7](https://browser.geekbench.com/v7/cpu/734989)

### 麒麟芯片对比

| 时间 | 芯片          | 核心簇 1                | 核心簇 2                | 核心簇 3                 | 核心簇 4           | 核心线程数 | GPU               |
|------|---------------|-------------------------|-------------------------|--------------------------|--------------------|------------|-------------------|
| 2023 | 麒麟 9000S    | 1x 2.62 GHz, SMT, 0xd02 | 3x 2.15 GHz, SMT, 0xd42 | 4x 1.53 GHz, Cortex-A510 | N/A                | 8C12T      | Maleoon 910, 4CU  |
| 2024 | 麒麟 9010     | 1x 2.30 GHz, SMT, 0xd03 | 3x 2.18 GHz, SMT, 0xd42 | 4x 1.55 GHz, Cortex-A510 | N/A                | 8C12T      | Maleoon 910, 4CU  |
| 2025 | 麒麟 9010B    | 1x 2.19 GHz, SMT, 0xd03 | 2x 2.18 GHz, SMT, 0xd42 | 3x 1.40 GHz, Cortex-A510 | N/A                | 6C9T       | Maleoon 910, 3CU  |
| 2025 | 麒麟 X90      | 4x 2.32 GHz, SMT, 0xd03 | 4x 2.05 GHz, SMT, 0xd43 | 2x 2.01 GHz, SMT, 0xd42  | N/A                | 10C20T     | Maleoon 916, 6CU  |
| 2025 | 麒麟 X90A     | 3x 2.07 GHz, SMT, 0xd03 | 3x 1.85 GHz, SMT, 0xd43 | 2x 1.81 GHz, SMT, 0xd42  | N/A                | 8C16T      | Maleoon 916B, ?CU |
| 2026 | 麒麟 X90 Plus | 4x 2.45 GHz, SMT, 0xd03 | 4x 2.05 GHz, SMT, 0xd43 | 2x 2.01 GHz, SMT, 0xd42  | N/A                | 10C20T     | Maleoon 916, 6CU  |
| 2025 | 麒麟 9010S    | 1x 2.50 GHz, SMT, 0xd05 | 3x 2.05 GHz, SMT, 0xd46 | 4x 1.50 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920C, 2CU |
| 2024 | 麒麟 9020     | 1x 2.50 GHz, SMT, 0xd05 | 3x 2.15 GHz, SMT, 0xd46 | 4x 1.60 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920, 4CU  |
| 2026 | 麒麟 9025     | 1x 2.60 GHz, SMT, 0xd05 | 3x 2.15 GHz, SMT, 0xd46 | 4x 1.60 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920, 4CU  |
| 2025 | 麒麟 9020A    | 1x 2.40 GHz, SMT, 0xd05 | 3x 2.00 GHz, SMT, 0xd46 | 4x 1.60 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920, 3CU  |
| 2025 | 麒麟 9020B    | 1x 2.40 GHz, SMT, 0xd05 | 2x 2.00 GHz, SMT, 0xd46 | 3x 1.60 GHz, 0xd23       | N/A                | 6C9T       | Maleoon 920R, 3CU |
| 2024 | 麒麟 T92      | 1x 2.50 GHz, SMT, 0xd05 | 3x 2.15 GHz, SMT, 0xd46 | 4x 1.60 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920, 4CU  |
| 2025 | 麒麟 T92C     | 1x 2.30 GHz, SMT, 0xd05 | 2x 2.00 GHz, SMT, 0xd46 | 3x 1.60 GHz, 0xd23       | N/A                | 6C9T       | Maleoon 920A, 3CU |
| 2025 | 麒麟 T92D     | 1x 2.40 GHz, SMT, 0xd05 | 3x 2.00 GHz, SMT, 0xd46 | 4x 1.60 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920, ?CU  |
| 2025 | 麒麟 8020     | 1x 2.29 GHz, SMT, 0xd05 | 3x 2.05 GHz, SMT, 0xd46 | 4x 1.31 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920C, 2CU |
| 2026 | 麒麟 8020A    | 1x 2.29 GHz, SMT, 0xd05 | 2x 2.05 GHz, SMT, 0xd46 | 3x 1.31 GHz, 0xd23       | N/A                | 6C9T       | Maleoon 920C, 2CU |
| 2026 | 麒麟 8000S    | N/A                     | 2x 2.05 GHz, SMT, 0xd46 | 3x 1.31 GHz, 0xd23       | N/A                | 5C7T       | Maleoon 920C, 1CU |
| 2026 | 麒麟 T82B     | 1x 2.29 GHz, SMT, 0xd05 | 3x 2.05 GHz, SMT, 0xd46 | 4x 1.31 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920C, ?CU |
| 2025 | 麒麟 T82      | 1x 2.29 GHz, SMT, 0xd05 | 3x 2.05 GHz, SMT, 0xd46 | 4x 1.31 GHz, 0xd23       | N/A                | 8C12T      | Maleoon 920C, ?CU |
| 2025 | 麒麟 9030     | 1x 2.70 GHz, SMT, 0xd06 | 3x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935A, 5CU |
| 2025 | 麒麟 9030 Pro | 1x 2.75 GHz, SMT, 0xd06 | 4x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 9C14T      | Maleoon 935, 6CU  |
| 2026 | 麒麟 9030S    | 1x 2.70 GHz, SMT, 0xd06 | 3x 2.15 GHz, SMT, 0xd47 | 4x 1.62 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935F, 3CU |
| 2026 | 麒麟 9035     | 1x 2.85 GHz, SMT, 0xd06 | 4x 2.35 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 9C14T      | Maleoon 935, 6CU  |
| 2026 | 麒麟 T93 Pro  | 1x 2.75 GHz, SMT, 0xd06 | 4x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 9C14T      | Maleoon 935, 6CU  |
| 2026 | 麒麟 T93      | 1x 2.69 GHz, SMT, 0xd06 | 3x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935A, 5CU |
| 2026 | 麒麟 T93A     | 1x 2.69 GHz, SMT, 0xd06 | 3x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935A, 5CU |
| 2026 | 麒麟 T93B     | 1x 2.69 GHz, SMT, 0xd06 | 3x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935B, 4CU |
| 2026 | 麒麟 T93C     | N/A                     | 4x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935B, 4CU |
| 2026 | 麒麟 T93S     | 1x 2.70 GHz, SMT, 0xd06 | 3x 2.15 GHz, SMT, 0xd47 | 4x 1.62 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935F, 3CU |
| 2026 | 麒麟 T93SD    | 1x 2.70 GHz, SMT, 0xd06 | 3x 2.15 GHz, SMT, 0xd47 | 4x 1.62 GHz, 0xd24       | N/A                | 8C12T      | Maleoon 935F, 2CU |
| 2026 | 麒麟 XE90     | 1x 2.75 GHz, SMT, 0xd06 | 4x 2.27 GHz, SMT, 0xd47 | 4x 1.72 GHz, 0xd24       | N/A                | 9C14T      | Maleoon 935, 6CU  |
| 2026 | 麒麟 9050     | 1x 3.00 GHz, SMT, 0xd47 | 2x 2.70 GHz, SMT, 0xd48 | 3x 2.20 GHz, SMT, 0xd48  | 2x 1.75 GHz, 0xd25 | 8C14T      | Maleoon 955A, 5CU |
| 2026 | 麒麟 9050 Pro | 1x 3.10 GHz, SMT, 0xd07 | 2x 2.70 GHz, SMT, 0xd48 | 4x 2.20 GHz, SMT, 0xd48  | 2x 1.75 GHz, 0xd25 | 9C16T      | Maleoon 955, 6CU  |

## 产品型号

这里记录产品名与型号的对应关系。同一商品不同容量可能是不同型号、不同芯片（如 Mate 80 Pro 12GB 为 SGT-AL50/9030，16GB 为 SGT-AL00/9030 Pro）。

| 产品 | 型号 | 商城 CPU | 来源 |
|------|------|----------|------|
| Mate 70 Pro+ | PLA-AL10 | 麒麟 9020 | [华为商城](https://www.vmall.com/product/10086989076790.html) |
| Mate 70 Air 12GB | SUP-AL90 | 麒麟 9020B | [华为商城](https://www.vmall.com/product/10086384239615.html) |
| Mate 70 Air 16GB | SUP-AL90a | 麒麟 9020A | [华为商城](https://www.vmall.com/product/10086384239615.html) |
| Mate 80 | VYG-AL00 / VYG-AL30 | 麒麟 9020 | [华为商城](https://www.vmall.com/product/10086133363559.html) |
| Mate 80 Pro 12GB | SGT-AL50 | 麒麟 9030 | [华为商城](https://www.vmall.com/product/10086476013098.html) |
| Mate 80 Pro 16GB | SGT-AL00 | 麒麟 9030 Pro | [华为商城](https://www.vmall.com/product/10086476013098.html) |
| Mate 80 Pro Max 风驰版 | SGT-AL10 | 麒麟 9030 Pro | [华为商城](https://www.vmall.com/product/10086981094378.html) |
| Mate 80 RS 非凡大师 | SGU-AL10 | 麒麟 9030 Pro | [华为商城](https://www.vmall.com/product/10086511284892.html) |
| Mate 90 | HLS-AL00 | 麒麟 9030 | [华为商城](https://www.vmall.com/product/10086824447544.html) |
| Mate 90 Pro | CMS-AL20 | 麒麟 9035 | [华为商城](https://www.vmall.com/product/10086050799772.html) |
| Mate 90 Pro Max 12GB | CMM-AL00 | 麒麟 9050 | [华为商城](https://www.vmall.com/product/10086384648661.html) |
| Mate 90 Pro Max 16GB | CMM-AL10 | 麒麟 9050 Pro | [华为商城](https://www.vmall.com/product/10086384648661.html) |
| Mate 90 RS 非凡大师 | CMU-AL10 | 麒麟 9050 Pro | [华为商城](https://www.vmall.com/product/10086964819340.html) |
| Mate XT2 ULTIMATE DESIGN | LAP-AL10 | 麒麟 9050 Pro | [华为商城](https://www.vmall.com/product/10086839715516.html) |
| Pura X | VDE-AL00 | 麒麟 9020 | [华为商城](https://www.vmall.com/product/10086061975812.html) |
| Pura X 典藏版 | VDE-AL10 | 麒麟 9020 | [华为商城](https://www.vmall.com/product/10086061975812.html) |
| Pura X View | VOL-AL00 | 麒麟 9030S | [华为商城](https://www.vmall.com/product/10086683896486.html) |
| Pura 80 | HED-AL00 | 麒麟 9010S | [华为商城](https://www.vmall.com/product/10086364337052.html) |
| Pura 90 | KEE-AL00 | 麒麟 9010S | [华为商城](https://www.vmall.com/product/10086412214615.html) |
| Pura 90 Plus | LCI-AL00 | 麒麟 9025 | [华为商城](https://www.vmall.com/product/10086663062178.html) |
| Pura 90 Pro | MLN-AL00 | 麒麟 9030S | [华为商城](https://www.vmall.com/product/10086866372688.html) |
| Pura 90 Pro Max | SCA-AL00 | 麒麟 9030S | [华为商城](https://www.vmall.com/product/10086454848882.html) |
| 畅享 100 | JAL-AL90 | 麒麟 8000S | [华为商城](https://www.vmall.com/product/10086576131735.html) |
| 畅享 100m | JAL-AL90 | 麒麟 8000S | [华为商城](https://www.vmall.com/product/10086082763391.html) |
| 畅享 90 | JUY-AL80 | 麒麟 8000A | [华为商城](https://www.vmall.com/product/10086174757473.html) |
| 畅享 90 Plus | JUY-AL50 | 麒麟 8000 | [华为商城](https://www.vmall.com/product/10086756705081.html) |
| 畅享 90 Pro Max | CHZ-AL00 | 麒麟 8000 | [华为商城](https://www.vmall.com/product/10086270081540.html) |
| 畅享 100 Pro | CHZ-AL60 | 麒麟 8020A | [华为商城](https://www.vmall.com/product/10086591909517.html) |
| 畅享 100 Pro Max 128/256GB | YEW-AL80 | 麒麟 8020A | [华为商城](https://www.vmall.com/product/10086296035938.html) |
| 畅享 100 Pro Max 512GB | YEW-AL90 | 麒麟 8020 | [华为商城](https://www.vmall.com/product/10086296035938.html) |
| nova 15 | PSN-AL00 | 麒麟 8020 | [华为商城](https://www.vmall.com/product/10086352871370.html) |
| nova 16 | EMA-AL00 / EMA-AL00U | 麒麟 9010S | [华为商城](https://www.vmall.com/product/10086850799769.html) |
| nova 16 Pro | CRS-AL00 | 麒麟 9010S | [华为商城](https://www.vmall.com/product/10086941643085.html) |
| nova 16 Ultra | HIP-AL00 | 麒麟 9010S | [华为商城](https://www.vmall.com/product/10086524794571.html) |
| nova 16 SE | CAS-AL50 | 麒麟 8020 | [华为商城](https://www.vmall.com/product/10086562905319.html) |
| nova 16z | PKN-AL00 | 麒麟 8020 | [华为商城](https://www.vmall.com/product/10086658434293.html) |
| MatePad Edge WiFi | QXS-W00 / QXS-W10 | 麒麟 X90A | [华为商城](https://www.vmall.com/product/10086590821009.html) |
| MatePad Edge 液冷版 | QXS-W20 | 麒麟 X90 | [华为商城](https://www.vmall.com/product/10086590821009.html) |
| MatePad Pro Max 悦享款 | GEM-W40 | 麒麟 T93 | [华为商城](https://www.vmall.com/product/10086127502687.html) |
| MatePad Pro Max | GEM-W00 | 麒麟 T93 Pro | [华为商城](https://www.vmall.com/product/10086127502687.html) |
| MatePad Pro 12 悦享款 | DAL-W20 | 麒麟 T93A | [华为商城](https://www.vmall.com/product/10086473135606.html) |
| MatePad Pro 12 | DAL-W00 | 麒麟 T93 | [华为商城](https://www.vmall.com/product/10086473135606.html) |
| MatePad Air 12 三代 悦享款 | WKI-W00 | 麒麟 T93C | [华为商城](https://www.vmall.com/product/10086662006762.html) |
| MatePad Air 12 三代 | WKI-W10 | 麒麟 T93B | [华为商城](https://www.vmall.com/product/10086662006762.html) |
| MatePad Air Z | AST-W00 / AST-W30 | 麒麟 T93SD | [华为商城](https://www.vmall.com/product/10086966141469.html) |
| MatePad Air Z 柔光版 | AST-W10 | 麒麟 T93S | [华为商城](https://www.vmall.com/product/10086966141469.html) |
| MatePad 11.5 S 鸿蒙焕新版 灵动款 | SLG-W50 | 麒麟 T92C | [华为商城](https://www.vmall.com/product/10086693978514.html) |
| MatePad 11.5 S 鸿蒙焕新版 活力版 | SLG-W10 | 麒麟 T92D | [华为商城](https://www.vmall.com/product/10086693978514.html) |
| MatePad 11.5 鸿蒙焕新版 WiFi | TXZ-W10 | 麒麟 T82B | [华为商城](https://www.vmall.com/product/10086070683245.html) |
| MatePad 11.5 鸿蒙焕新版 柔光版 | TXZ-W20 | 麒麟 T82 | [华为商城](https://www.vmall.com/product/10086070683245.html) |
| MatePad 11.5 鸿蒙焕新版 全网通 | TXZ-AL10 | 麒麟 8020 | [华为商城](https://www.vmall.com/product/10086070683245.html) |
| MatePad SE 11 英寸 焕新版 | AGS6-W00 | 骁龙 685 | [华为商城](https://www.vmall.com/product/10086426290126.html) |
| MatePad Mini | MLR-AL00 | 麒麟 9010B | [华为商城](https://www.vmall.com/product/10086287244006.html) |
| MatePad Mini 典藏版 | MLR-AL10 | 麒麟 9010 | [华为商城](https://www.vmall.com/product/10086287244006.html) |
| MatePad Mini 悦读版 鸿蒙焕新版 | MLR-AL00 | 麒麟 9010B | [华为商城](https://www.vmall.com/product/10086204924439.html) |
| MateBook Pro | HAD-W32 | 麒麟 X90 | [华为商城](https://www.vmall.com/product/10086702263930.html) |
| MateBook Pro 24GB/512GB | HAD-W24 | 麒麟 X90 | [华为商城](https://www.vmall.com/product/10086702263930.html) |
| MateBook Pro 麒麟 X90 Plus | HAD-W24 / HAD-W32 | 麒麟 X90 Plus | [华为商城](https://www.vmall.com/product/10086008052699.html) |
| MateBook Pro S | MOR-M1 / MOR-M2 | 麒麟 XE90 | [华为商城](https://www.vmall.com/product/10086380895025.html) |
| MateBook 14 鸿蒙版 | MNTXM-24A / MNTXM-32A | 麒麟 X90 | [华为商城](https://www.vmall.com/product/10086097339191.html) |
| MateBook Fold 非凡大师（X90） | HPR-W72 | 麒麟 X90 | [华为商城](https://www.vmall.com/product/10086297718748.html) |
| MateBook Fold 非凡大师（X90 Plus） | SLM-W24 / SLM-W32 | 麒麟 X90 Plus | [华为商城](https://www.vmall.com/product/10086769820844.html) |

## hip

### hip07

- hip07 from DSDT oem table id
- hi1616
- kunpeng 916
- Cortex-A72

来源：

- [kernel/arch/arm64/kvm/hisilicon/hisi_virt.c](https://gitee.com/openeuler/kernel/blob/OLK-6.6/arch/arm64/kvm/hisilicon/hisi_virt.c)
- [A Quick Look at the Huawei HiSilicon Kunpeng 920 Arm Server CPU](https://www.servethehome.com/a-quick-look-huawei-hisilicon-kunpeng-920-arm-server-cpu/)
- [Kunpeng 916 (Hi1616) - HiSilicon](https://en.wikichip.org/wiki/hisilicon/kunpeng/hi1616)

### hip08

- tsv110
- part id 0xd01
- No SVE
- 华为云 kc1 实例
- hip08 from DSDT oem table id
- hi1620
- kunpeng 920
- 2.60 GHz
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma dcpop asimddp asimdfhm
- HIP08 appears in ACPI: `ACPI: XSDT 0x000000002F5DFE98 0000B4 (v01 HISI   HIP08    00000000 HISI 20151124)`

来源：

- [kernel/arch/arm64/kvm/hisilicon/hisi_virt.c](https://gitee.com/openeuler/kernel/blob/OLK-6.6/arch/arm64/kvm/hisilicon/hisi_virt.c)
- [A Quick Look at the Huawei HiSilicon Kunpeng 920 Arm Server CPU](https://www.servethehome.com/a-quick-look-huawei-hisilicon-kunpeng-920-arm-server-cpu/)
- [config/arm: add Hisilicon kunpeng](https://github.com/DPDK/dpdk/commit/7cf32a22b240f2db9e509ffe7b267673adbee35f)

### hip09

- ARMv8.5-A
- SVE (256 bits)
- part id 0xd02，和麒麟 9000s 大核一样
- 华为云 kc2 实例
- kunpeng 930
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb dcpodp flagm2 frint svei8mm svef32mm svef64mm svebf16 i8mm bf16 dgh rng bti ecv
- 64KB L1 Cache, 512KB L2 Cache
- 6-issue, 2 BR + 6 ALU + 4 FP + 2 LD + 2 ST from LLVM
- 88-entry reorder buffer from LLVM
- 16-entry instruction queue from LLVM

来源：

- [Add hip09 machine discribtion](https://github.com/openeuler-mirror/gcc/commit/d9131757175667d35e74d9ee84689039990af768)
- [config/arm: add Hisilicon kunpeng](https://github.com/DPDK/dpdk/commit/7cf32a22b240f2db9e509ffe7b267673adbee35f)
- [[SME] Recover hip09 and hip11 in aarch64-cores.def](https://github.com/openeuler-mirror/gcc/commit/239f0637307ff2f6afb1473e99d0bb0eaf8946b2)
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2174)
- [hip09_prefetch_tune](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L1746)
- [AArch64SchedHIP09.td](https://atomgit.com/openeuler/llvm-project/blob/dev_17.0.6/llvm/lib/Target/AArch64/AArch64SchedHIP09.td)

### hip09a

来源：

- [ACPI/IORT: Add PMCG platform information for HiSilicon HIP09A](https://github.com/torvalds/linux/commit/c2b46ae022704a2d845e59461fa24431ad627022)

### hip10

- ARMv8.5-A
- SVE
- part id 0xd03，和麒麟 9010 大核一样

来源：

- [kernel/arch/arm64/kvm/hisilicon/hisi_virt.c](https://gitee.com/openeuler/kernel/blob/OLK-6.6/arch/arm64/kvm/hisilicon/hisi_virt.c)
- [dpdk/config/arm/meson.build](https://github.com/DPDK/dpdk/blob/fd51012de5369679e807be1d6a81d63ef15015ce/config/arm/meson.build#L275)

### hip10a

- ARMv8.5-A
- SVE + SVE2 (256 bits)
- part id 0xd03，和麒麟 9010 大核一样
- 128KB L1 Cache, 1MB L2 Cache
- 疑似 hip10 和 hip10a 是同一个

来源：

- [Add hip10a machine discription](https://github.com/openeuler-mirror/gcc/commit/2eea7cfbd7128906034e3d3c5a0fe7d05860ba6b)
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2207)

### hip10c

- ARMv8.5-A
- SVE (256 bits)
- part id 0xd45
- 96KB L1 Cache, 1MB L2 Cache
- 12-issue, 2 BR + 6 ALU + 2 FP + 2 LD + 2 ST from LLVM
- 320-entry reorder buffer from LLVM
- 16-entry instruction queue from LLVM

来源：

- [Add hip10c machine discription](https://github.com/openeuler-mirror/gcc/commit/d3a8c59e7eaf99bff77447e08e15898530af8a9e) part id 0xddd
- [Add hip10a machine discription](https://github.com/openeuler-mirror/gcc/commit/2eea7cfbd7128906034e3d3c5a0fe7d05860ba6b) part id changes from 0xddd to 0xd45
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2240)
- [AArch64SchedHIP10C.td](https://atomgit.com/openeuler/llvm-project/blob/dev_17.0.6/llvm/lib/Target/AArch64/AArch64SchedHIP10C.td)

### hip11

- ARMv8.5-A
- SVE + SVE2 (512 bits)
- part id 0xd22
- 64KB L1 Cache, 512KB L2 Cache
- HasSMEI16I64 from LLVM
- 4-issue, 1 ALU + 2 (ALU + BR) + 1 MDU + 2 FP + 1 LDST + 1LD from LLVM
- 88-entry reorder buffer from LLVM
- 40-entry instruction queue from LLVM

来源：

- [Add hip11 CPU pipeline scheduling](https://github.com/openeuler-mirror/gcc/commit/824fccdab1d3c5e87fb88b31f0eeb7abd1b35c1f)
- [[SME] Recover hip09 and hip11 in aarch64-cores.def](https://github.com/openeuler-mirror/gcc/commit/239f0637307ff2f6afb1473e99d0bb0eaf8946b2)
- [SVE_512](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2274)
- [AArch64SchedHIP11.td](https://atomgit.com/openeuler/llvm-project/blob/dev_17.0.6/llvm/lib/Target/AArch64/AArch64SchedHIP11.td)

### hip12

- ARMv9.2-A
- SVE + SVE2 (256 bits)
- part id 0xd06，与 Kirin 9030 系列大核相同
- 128KB L1 Cache, 1MB L2 Cache
- kunpeng 950
- 16(?)/8-issue, 2 BR + 6 ALU + 4 FP + 3 LD + 2 ST from LLVM
- 128bit FP datapath from LLVM
- 320-entry reorder buffer from LLVM
- 16-entry instruction queue from LLVM

来源：

- [kernel/arch/arm64/kvm/hisilicon/hisi_virt.c](https://gitee.com/openeuler/kernel/blob/OLK-6.6/arch/arm64/kvm/hisilicon/hisi_virt.c)
- [Add hip12 core definition and cost model](https://github.com/openeuler-mirror/gcc/commit/c5970536c2caa3980bb1fded812ac0dc8ebf3681)
- [Add hip12 instructions pipeline](https://gitee.com/openeuler/gcc/commit/d63119daeb54cd0c387c1b24981c47d795e5a672)
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2308)
- [Add support for Hisilicon's hip12 core](https://patchwork.sourceware.org/project/gcc/patch/97a7d78ec85d4a05891366b3d39028ca@huawei.com/)
- [AArch64SchedHIP12.td](https://atomgit.com/openeuler/llvm-project/blob/dev_17.0.6/llvm/lib/Target/AArch64/AArch64SchedHIP12.td)
- [Add initial support for Hisilicon's hip12 core](https://github.com/llvm/llvm-project/pull/203446/changes)
- [Add hip12 to release notes](https://github.com/llvm/llvm-project/pull/205899/changes)
- [[AArch64] Add initial sched model for hip12 - #212935](https://github.com/llvm/llvm-project/pull/212935)

## Kunpeng 920B

- Kunpeng 920 V200 7270Z
- 64 cores/socket
- SVE
- SMT2
- 2.90 GHz
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt pacg dcpodp flagm2 frint svei8mm svef32mm svef64mm svebf16 i8mm bf16 dgh rng ecv
- 疑似等价于 hip09

来源：

- [鲲鹏 920B 8C8G 规格虚机跑 MySQL 绑核性能差，只有不绑核性能的 1/20](https://gitee.com/openeuler/community/issues/IAR1EG)
- [EulerOS V2.0SP11 支持的服务器类型](https://support.huawei.com/enterprise/zh/doc/EDOC1100346786/257a3292)

## Kunpeng 920C

- [Server Types Supported by EulerOS V2.0SP12](https://support.huawei.com/enterprise/en/doc/EDOC1100451965/257a3292/server-types-supported-by-euleros-v20sp12)

## Kunpeng 920E

- [Server Types Supported by EulerOS V2.0SP12](https://support.huawei.com/enterprise/en/doc/EDOC1100451965/257a3292/server-types-supported-by-euleros-v20sp12)

## Taishan V200M

- 昇腾 310P AI 处理器
- ARMv8.2-A
- SVE

来源：

- [Atlas 200I SoC A1 核心板 开发指南 01](https://www.hiascend.com/doc_center/source/zh/200I-SoC-A1/devguide/Atlas%20200I%20SoC%20A1%20%E6%A0%B8%E5%BF%83%E6%9D%BF%20%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%2001.pdf)
- <https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC1/pd/pd_0004.html>
- <https://www.hiascend.com/doc_center/source/zh/200I-SoC-A1/devguide/devguide_0012.html>
- [OrangePi AIpro (20T)](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-AIpro(20t).html)

## Roadmap

- 2024 Q1, Kunpeng 920, 64C, 80C/160T, w/ HCCS
- 2026 Q4, Kunpeng 950, 96C/192T, 192C/384T
- 2028 Q1, Kunpeng 960, 96C/192T, >= 256C/512T

## part id 列表

implementer 0x48

part id:

- 0xd01(3329): hip08
- 0xd02(3330): Kirin 9000S/hip09
- 0xd03(3331): Kirin 9010/hip10/hip10a/Kirin X90/Kirin 9010B
- 0xd05(3333): Kirin 9020/Kirin 9025/Kirin 9010S/Kirin 8020/Kirin 8020A/Kirin T92C/Kirin T92D/Kirin T82B
- 0xd06(3334): hip12/Kirin 9030/Kirin 9030Pro/Kirin 9030S/Kirin 9035/Kirin T93/Kirin T93A
- 0xd07(3335): Kirin 9050Pro
- 0xd22(3362): hip11
- 0xd23(3363): Kirin 9020/Kirin 9025/Kirin 9020A/Kirin 9020B/Kirin 9010S/Kirin 8020/Kirin 8020A/Kirin 8000S
- 0xd24(3364): Kirin 9030/Kirin 9030Pro/Kirin 9030S/Kirin 9035
- 0xd25(3365): Kirin 9050Pro
- 0xd42(3394): Kirin 9000S/Kirin 9010/Kirin X90
- 0xd43(3395): Kirin X90
- 0xd45(3397): hip10c
- 0xd46(3398): Kirin 9020/Kirin 9025/Kirin 9020A/Kirin 9020B/Kirin 9010S/Kirin 8020/Kirin 8020A/Kirin 8000S
- 0xd47(3399): Kirin 9030/Kirin 9030Pro/Kirin 9030S/Kirin 9035/Kirin T93C
- 0xd48(3400): Kirin 9050Pro

## LX2

- 每个节点是 2 socket
- 每个 socket 是 2 die，每个 die 上有 152 core，包括 4 cluster，每个 cluster 38 核
- 每个节点有 `2 * 2 * 4 * 38 = 608` 核
- 每个核有 32KB 的 L1I 和 L1D，每个 cluster 有 28.5MB L2，无 L3
- 每个 socket 有 32GB 容量 4TB/s 带宽 8-stack 的 HBM 和 256GB 的 DDR
- SDMA 引擎负责 HBM <-> DDR 传输
- 512-bit SVE+SME，每个 socket 是 60.3 TFLOP/s(FP64)，120.6 TFLOP/s(FP32), 240 TFLOP/s(BF16/FP16)，960 TOP/s(INT8)
- 1.55 GHz 主频
- 峰值性能验算：
    - 每核每周期 FP64 是 `60.3 TFLOP/s / 1.55 GHz / 304 = 128`，对应 8x8 的外积，和 512-bit SVE 的向量宽度吻合，每周期执行一条 FP64 1-way FMOPA 指令
    - 每核每周期执行一条 INT8 4-way SMOPA 指令，执行 16x4x16 的矩阵乘累加到 16x16 的 INT32，对应峰值算力 `16 * 4 * 16 * 2 * 304 * 1.55 GHz = 965 TOP/s`，是 FP64 的 16 倍
    - 每核每周期执行一条 FP16 2-way FMOPA 指令，执行 16x2x16 的矩阵乘累加到 16x16 的 FP32，对应峰值算力 `16 * 2 * 16 * 2 * 304 * 1.55 GHz = 483 TFOP/s`，实际只有 240 TFLOPS/s，意味着 IPC 只有 0.5
    - 每核每周期执行一条 FP32 1-way FMOPA 指令，执行 16x1x16 的矩阵乘累加到 16x16 的 FP32，对应峰值算力 `16 * 1 * 16 * 2 * 304 * 1.55 GHz = 241 TOP/s`，实际只有 120.6 TFLOPS，意味着 IPC 只有 0.5
    - 即：128 FP64 FLOP/cycle, 256 FP32 FLOP/cycle, 512 FP16 FLOP/cycle, 2048 INT8 OP/cycle
- 应该对应 hip11

来源：

- <https://arxiv.org/html/2604.15821>
- <https://arxiv.org/html/2605.08633>
- <https://arxiv.org/html/2605.24896>
- <https://arxiv.org/html/2606.14073>
- <https://www.top500.org/system/180490/>
