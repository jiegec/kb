# CPU 漏洞和缓解措施

## Meltdown

- [论文 Meltdown: Reading Kernel Memory from User Space](https://meltdownattack.com/meltdown.pdf)
- [CVE-2017-5754](https://nvd.nist.gov/vuln/detail/cve-2017-5754)
- [Rogue Data Cache Load / CVE-2017-5754 / INTEL-SA-00088](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/rogue-data-cache-load.html)
- 允许用户态程序读取完整的内核态地址空间
- 原理：
	- 硬件为了性能，在验证 load 指令的权限是否正确之前，提前把 load 指令的结果传递给了后续的指令，后续发现 load 指令的的权限错误后，再进行回滚
	- 在用户态的时候，页表中内核态的地址也被映射了，只不过设置了权限位，禁止用户态访问
	- 在用户态访问内核态地址会触发异常，但如果 load 指令的结果通过某种方式带来了副作用，就可以知道 load 的结果是多少
	- 为了利用副作用来得到 load 指令的结果，首先把一个数组从缓存中清空，再把 load 指令的结果移位后作为下标去访问数组，那么副作用就是把对应位置的缓存行加载到缓存当中
	- 最后再测量缓存行的访问时间，从而知道之前哪个缓存行通过副作用被加载到缓存当中，从而得到 load 指令的结果，而这本来是只有在内核态才能访问的数据
	- 由于时间窗口比较小，如果访问的内核态的数据不在 L1 数据缓存中，可能会来不及产生副作用
- 代码：
	```asm
	; rcx = kernel address, rbx = probe array
	mov al, byte [rcx]         ; read one byte from kernel space
	shl rax, 0xc               ; multiply by 4096
	mov rbx, qword [rbx + rax] ; access probe array
	```
- 从内核地址 rcx 读取一个字节，左移 0xc，也就是乘以 4096，再去访问 rbx 指向的数组。那么每个可能的 al 放在不同的页上，避免预取器干扰后续的测量
- 缓解措施：Kernel Page Table Isolation/KPTI/PTI/KAISER([论文 KASLR is Dead: Long Live KASLR](https://gruss.cc/files/kaiser.pdf))，在用户态的页表里，不要映射整个内核态空间，只映射必须映射的部分，进入内核态后，再切换到具有完整的内核态地址空间的页表；那么在用户态尝试读取内核态地址的时候，由于地址不在 TLB 当中，也就无法读取内存，不会泄漏数据
- PoC：[paboldin/meltdown-exploit](https://github.com/paboldin/meltdown-exploit)
	- 这个 PoC 先用 root 权限读取 `/proc/kallsyms`，找到内核符号 `linux_proc_banner` 的地址，这主要是为了展示，方便拿到内核态地址，实际攻击者是没有 root 权限的
	- 访问 `/proc/version`，使得 `linux_proc_banner` 符号在缓存中
	- 在用户态用 Meltdown 读取内核态的 `linux_proc_banner` 的结果
	- 在 Intel Xeon E5-2603 v4 上关闭 KPTI（内核 cmdline 添加 `mitigations=off`）后成功复现，成功读出来 `%s version %s (d`：
		```
		cached = 30, uncached = 316, threshold 97
		read ffffffffa2400260 = 25 % (score=999/1000)
		read ffffffffa2400261 = 73 s (score=1000/1000)
		read ffffffffa2400262 = 20   (score=1000/1000)
		read ffffffffa2400263 = 76 v (score=1000/1000)
		read ffffffffa2400264 = 65 e (score=1000/1000)
		read ffffffffa2400265 = 72 r (score=1000/1000)
		read ffffffffa2400266 = 73 s (score=1000/1000)
		read ffffffffa2400267 = 69 i (score=1000/1000)
		read ffffffffa2400268 = 6f o (score=1000/1000)
		read ffffffffa2400269 = 6e n (score=1000/1000)
		read ffffffffa240026a = 20   (score=1000/1000)
		read ffffffffa240026b = 25 % (score=1000/1000)
		read ffffffffa240026c = 73 s (score=1000/1000)
		read ffffffffa240026d = 20   (score=1000/1000)
		read ffffffffa240026e = 28 ( (score=1000/1000)
		read ffffffffa240026f = 64 d (score=1000/1000)
		VULNERABLE
		```
	- 继续增加读取的字节数，可以得到完整的 `linux_proc_banner` 的内容：`%s version %s (debian-kernel@lists.debian.org) (gcc-12 (Debian 12.2.0-14) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40) %s`

## KASLR

- KASLR: Kernel Address Space Layout Randomization
- 随机化内核地址，避免攻击者猜测出内核地址

## TODO

- Gather data sampling
- Itlb multihit
- L1tf
- Mds
- Meltdown
- Mmio stable data
- Reg file data sampling
- Retbleed
- Spec rstack overflow
- Spec store bypass
- Spectre v1
- Spectre v2
- Srbds
- Tsx async abort
- __user pointer sanitization
- usercopy barrier
- swapgs barrier
- IBPB
- STIBP
- PBRSB-EIBRS
- BHI
- PTE Inversion
- Retpoline
- IBRS_FW
- RSB filling
- Zenbleed
- Safe RET
- untrained return thunk
