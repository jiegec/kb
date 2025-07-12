# 华为芯片

## 麒麟

### 麒麟 9000s

- 首发：Mate 60
- 1x 大核（0xd02），3x 中核（0xd42），4x 小核 Cortex-A510
- 大核中核有超线程
- 马良 910
- 丝印 Hi36A0 GFCV120

来源：

- [麒麟 9000s 芯片性能详细解析——华为 mate60 系列！](https://www.zhihu.com/tardis/zm/art/659619471?source_id=1003)
- [Kirin 9000S Review: How Powerful is Huawei Mate60 Pro?](https://www.youtube.com/watch?v=SCRIFe0uaac)

### 麒麟 9010

- 首发：Pura 70
- 1x 大核（0xd03，最大 2.3 GHz），3x 中核（0xd42，最大 2.18 GHz），4x 小核 Cortex-A510（impl 0x41, part 0xd46，最大 1.55 GHz）
- 2+6+4=12 线程
- all CPU features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint svei8mm svebf16 i8mm bf16 bti
- 大核中核有超线程
- 马良 910
- 丝印 Hi36A0 GFCV121

来源：

- [华为 Pura70 能效分析：架构进步很大！](https://www.bilibili.com/video/BV1az421D7Fk)
- [HiSilicon Kirin 9010](https://www.notebookcheck.net/HiSilicon-Kirin-9010-Processor-Benchmarks-and-Specs.855471.0.html)
- [Huawei’s Kirin 9010 Is a Reality Check for China’s Semiconductor Ambitions](https://zh.ifixit.com/News/95646/huaweis-kirin-9010-is-a-reality-check-for-chinas-semiconductor-ambitions)

### 麒麟 9020

- 首发：Mate 70
- 1x 大核（0xd05），3x 中核，4x 小核
- 大核中核有超线程
- 马良 920
- 丝印 Hi36C0 GFCV110

来源：

- [Huawei Mate 70 Pro+: Exploring the HiSilicon Kirin 9020 Processor](https://www.techinsights.com/blog/huawei-mate-70-pro-exploring-hisilicon-kirin-9020-processor)
- [Details on the new Kirin 9020 chipset surface, here's what is inside the new Mate 70 series](https://www.gsmarena.com/details_on_the_new_kirin_9020_chipset_surface_heres_what_is_inside_the_new_mate_70_series-news-65497.php)
- [HiSilicon Kirin 9020 from Mate 70 Pro Plus - Die Analysis](https://library.techinsights.com/public/hg-asset/e71466a2-64ef-410a-af5f-b3d001bd2318?utm_source=blog&utm_medium=website&utm_campaign=Huawei%20Mate%2070%20Pro%20Series#moduleName=Search&reportCode=FCT-2412-801&subscriptionId=null&channelId=null&reportName=HiSilicon+Kirin+9020+from+Mate+70+Pro+Plus+-+Die+Analysis)
- [华为 Mate70 Pro+ 性能分析：麒麟 9020 来啦！](https://www.bilibili.com/video/BV1j6iYYHEYG)
- [HUAWEI PLA-AL10](https://browser.geekbench.com/v6/cpu/9233574)

### 麒麟 9020 on Pura X

- 丝印 Hi36C0 GFCV111

来源：

- [华为 Pura X 发售第一时间又消费了！今年最惊喜的拆解，全新的 9020 换封装工艺了，CPU 不一样了！](https://www.bilibili.com/video/BV1qAZzY4Eyj)

### 麒麟 X90 on MateBook Pro

- 20 threads
- part id 0xd03（8 threads，可能是 4 核，同麒麟 9010 大核）, 0xd43（8 threads，可能是 4 核）, 0xd42（4 threads，可能是 2 核，同麒麟 9010 中核）
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint svei8mm svebf16 i8mm bf16 dgh bti ecv

来源：

- [【老戴】继续来折腾鸿蒙电脑！有你们最关心的 CPU 信息，设备树长啥样，包管理能不能用...](https://www.bilibili.com/video/BV1UY5VzMEj9/)
- [如何看待在 5 月 8 日鸿蒙电脑技术与生态沟通会上亮相的首款鸿蒙电脑，有哪些信息值得关注？ - 雷燚音的回答 - 知乎](https://www.zhihu.com/question/1903763170587304858/answer/1903943055951794515)

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
- 2.6 GHz
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

来源：

- [Add hip09 machine discribtion](https://github.com/openeuler-mirror/gcc/commit/d9131757175667d35e74d9ee84689039990af768)
- [config/arm: add Hisilicon kunpeng](https://github.com/DPDK/dpdk/commit/7cf32a22b240f2db9e509ffe7b267673adbee35f)
- [[SME] Recover hip09 and hip11 in aarch64-cores.def](https://github.com/openeuler-mirror/gcc/commit/239f0637307ff2f6afb1473e99d0bb0eaf8946b2)
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2174)
- [hip09_prefetch_tune](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L1746)

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

来源：

- [Add hip10c machine discription](https://github.com/openeuler-mirror/gcc/commit/d3a8c59e7eaf99bff77447e08e15898530af8a9e) part id 0xddd
- [Add hip10a machine discription](https://github.com/openeuler-mirror/gcc/commit/2eea7cfbd7128906034e3d3c5a0fe7d05860ba6b) part id changes from 0xddd to 0xd45
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2240)

### hip11

- ARMv8.5-A
- SVE + SVE2 (512 bits)
- part id 0xd22
- 64KB L1 Cache, 512KB L2 Cache

来源：

- [Add hip11 CPU pipeline scheduling](https://github.com/openeuler-mirror/gcc/commit/824fccdab1d3c5e87fb88b31f0eeb7abd1b35c1f)
- [[SME] Recover hip09 and hip11 in aarch64-cores.def](https://github.com/openeuler-mirror/gcc/commit/239f0637307ff2f6afb1473e99d0bb0eaf8946b2)
- [SVE_512](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2274)

### hip12

- ARMv9.2-A
- SVE + SVE2 (256 bits)
- part id 0xd06
- 128KB L1 Cache, 1MB L2 Cache

来源：

- [kernel/arch/arm64/kvm/hisilicon/hisi_virt.c](https://gitee.com/openeuler/kernel/blob/OLK-6.6/arch/arm64/kvm/hisilicon/hisi_virt.c)
- [Add hip12 core definition and cost model](https://github.com/openeuler-mirror/gcc/commit/c5970536c2caa3980bb1fded812ac0dc8ebf3681)
- [Add hip12 instructions pipeline](https://gitee.com/openeuler/gcc/commit/d63119daeb54cd0c387c1b24981c47d795e5a672)
- [SVE_256](https://github.com/openeuler-mirror/gcc/blob/966b156d8eadd564d65e1f0185bf589d2e1fe0d4/gcc/config/aarch64/aarch64.cc#L2308)

## Kunpeng 920B

- Kunpeng 920 V200 7270Z
- 64 cores/socket
- SVE
- SMT2
- 2.9 GHz
- Features: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt pacg dcpodp flagm2 frint svei8mm svef32mm svef64mm svebf16 i8mm bf16 dgh rng ecv
- 疑似等价于 hip09

来源：

- [鲲鹏 920B 8C8G 规格虚机跑 MySQL 绑核性能差，只有不绑核性能的 1/20](https://gitee.com/openeuler/community/issues/IAR1EG)
- [EulerOS V2.0SP11 支持的服务器类型](https://support.huawei.com/enterprise/zh/doc/EDOC1100346786/257a3292)

## part id 列表

implementer 0x48

part id:

- 0xd01: hip08
- 0xd02: Kirin 9000s/hip09
- 0xd03: Kirin 9010/hip10/hip10a/Kirin x90
- 0xd05: Kirin 9020
- 0xd06: hip12
- 0xd22: hip11
- 0xd42: Kirin 9000s/Kirin 9010/Kirin x90
- 0xd43: Kirin x90
- 0xd45: hip10c
