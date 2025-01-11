# ABI (Application Binary Interface)

## Data Model

- LP64: long & pointer are 64 bit, int is 32 bit
- ILP32: long, pointer & int are 32 bit

## MIPS

MIPS 有多种 ABI：

1. O32 ABI: original/old 32 位 ILP32 ABI，32 位 MIPS 用的多，`mips*-linux-gnu` target
	1. `$4-$7($a0-$a3)` 传整数参数
	2. `$f12-$f15` 传浮点参数
	3. `$2-$3($v0-$v1)` 传返回数据
	4. 16 个浮点寄存器
2. N64 ABI: new 64 位 LP64 ABI，64 位 MIPS 用的多，`mips*64*-linux-gnuabi64` target
	1. `$4-$11($a0-$a7)` 传整数参数
	2. `$f12-$f19` 传浮点参数
	3. `$2-$3($v0-$v1)` 传返回数据
	4. 32 个浮点寄存器
3. N32 ABI：把 N64 从 LP64 移植 ILP32，即只用 32 位地址，但寄存器还是 64 位，`mips*64*-linux-gnuabin32` target
4. O64 ABI: 把 O32 移植到 64 位，64 位寄存器
5. EABI: 有 32 位和 64 位版本：eabi32/eabi64

参考：

- [MIPS N32/N64 ABI](https://math-atlas.sourceforge.net/devel/assembly/mipsabi64.pdf)
- [MIPS N32 ABI](https://web.archive.org/web/20160121005457/http://techpubs.sgi.com/library/manuals/2000/007-2816-005/pdf/007-2816-005.pdf)
- [MIPS O64 ABI](https://gcc.gnu.org/projects/mipso64-abi.html)
- [MIPS EABI](https://sourceware.org/legacy-ml/binutils/2003-06/msg00436.html)
- [MIPS ABI History](https://web.archive.org/web/20180826012735/https://www.linux-mips.org/wiki/MIPS_ABI_History)
- [Debian Multiarch triples](https://wiki.debian.org/Multiarch/Tuples)

## x86

- [i386 abi](https://gitlab.com/x86-psABIs/i386-ABI): i*86-linux-gnu
- [amd64 abi](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf): x86_64-linux-gnu
- [x32 abi](https://sites.google.com/site/x32abi/): AMD64 上的 ILP32 ABI，32 位指针，x86_64-linux-gnux32 target

## ILP32 on 64-bit

- [MIPS N32](https://web.archive.org/web/20160121005457/http://techpubs.sgi.com/library/manuals/2000/007-2816-005/pdf/007-2816-005.pdf)
- [ARM64 ILP32](https://wiki.debian.org/Arm64ilp32Port)
- [AMD64 X32 ABI](https://sites.google.com/site/x32abi/)
- [RISC-V 64 ILP32 ABI](https://lwn.net/Articles/951187/)
