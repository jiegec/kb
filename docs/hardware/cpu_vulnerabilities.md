# CPU 漏洞和缓解措施

## 漏洞 Vulnerabilities

### Spectre

- [论文 Spectre Attacks: Exploiting Speculative Execution](https://spectreattack.com/spectre.pdf)
- [Reading privileged memory with a side-channel](https://googleprojectzero.blogspot.com/2018/01/reading-privileged-memory-with-side.html)
- [Spectre Side Channels](https://docs.kernel.org/admin-guide/hw-vuln/spectre.html)
- 有两个变种：Variant 1 和 Variant 2（Variant 3 是 Meltdown）
- Variant 1: Bounds Check Bypass
	- [CVE-2017-5753](https://nvd.nist.gov/vuln/detail/cve-2017-5753)
	- 原理：访问数组的时候，通常会有边界检查，这个边界检查是通过条件分支实现的；即使边界检查失败，如果分支预测器预测它会检查成功，就会导致错误路径上的代码被执行，进而产生可以被观察到的副作用
	- 攻击方法：非 root 用户利用 eBPF 在内核态中运行自定义代码，虽然 eBPF 强制做了边界检查，但处理器会执行错误路径，从而泄漏内核态的信息
	- 具体到 Linux 内核中，有一个场景是 swapgs：在切换上下文的时候，需要切换 gs 段的基地址，那么这个基地址应该用内核态的还是用户态的，就要根据具体情况来判断，而这就会引入条件分支：
		```asm
		if (coming from user space)
			swapgs
		mov %gs:<percpu_offset>, %reg
		mov (%reg), %reg1
		```
	- 如果在内核态在分支预测的错误路径上，跳过了 swapgs，直接用用户态的基地址去访问内存，就产生了安全问题
	- 类似的问题还出现在从用户态复制数据的时候：需要调用 `access_ok` 函数来判断指针是否合法，但这个判断也需要分支预测，可能会在错误路径上产生问题
	- 缓解措施：
		- Bounds Clipping
		- 特定场景下（例如 usercopy 和 swapgs）加入 lfence 指令阻止错误路径上的 load 指令被执行
		- Supervisor-Mode Access Prevention (SMAP)
		- __user pointer sanitization
- Variant 2: Branch Target Injection (BTI)
	- [CVE-2017-5715](https://nvd.nist.gov/vuln/detail/cve-2017-5715)
	- 原理：CPU 的分支预测器的状态是全局共享的，因此可以在虚拟机内控制分支预测器的状态，当 CPU 控制权回到宿主机时（比如进行一次 hypercall），CPU 会使用虚拟机准备好的分支预测器的状态来进行分支预测，从而推测执行了原本宿主机不会执行的代码，具体方法是欺骗 BTB 或间接分支预测器，注入攻击者指定的分支目的地址，使得 CPU 在预测错误路径上预测执行攻击者指定的代码；类似的方法也可以用于从用户态攻击内核态
	- 用类似的方法，还可以注入 Return Stack Buffer，也就是对 return 返回地址的预测
	- 缓解措施：
		- Retpoline
		- Indirect Branch Restricted Speculation (IBRS)
		- Enhanced Indirect Branch Restricted Speculation (Enhanced IBRS)
		- Single Threaded Indirect Branch Predictors (STIBP)
		- Indirect Branch Prediction Barrier (IBPB)
		- Supervisor-Mode Execution Prevention (SMEP)

### Meltdown (Rouge Data Cache Load)

- [论文 Meltdown: Reading Kernel Memory from User Space](https://meltdownattack.com/meltdown.pdf)
- [Reading privileged memory with a side-channel](https://googleprojectzero.blogspot.com/2018/01/reading-privileged-memory-with-side.html)
- [CVE-2017-5754](https://nvd.nist.gov/vuln/detail/cve-2017-5754)
- [Rogue Data Cache Load / CVE-2017-5754 / INTEL-SA-00088](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/rogue-data-cache-load.html)
- Meltdown 和 Spectre 一起被提出，其中 Variant 1 和 2 属于 Spectre，Variant 3 就是 Meltdown
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
- 缓解措施：
	- 软件上：Kernel Page Table Isolation
	- 硬件上：提早对权限的检查，避免以错误权限读出来的数据被用于后续的指令
- PoC：[IAIK/meltdown](https://github.com/IAIK/meltdown) [paboldin/meltdown-exploit](https://github.com/paboldin/meltdown-exploit)，下面分析后一个 PoC：
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
- Meltdown 的变种：Meltdown variant 3a, Meltdown-CPL-REG, Rogue System Register Read, [CVE-2018-3640](https://nvd.nist.gov/vuln/detail/cve-2018-3640), [lgeek/spec_poc_arm](https://github.com/lgeek/spec_poc_arm) 把 Meltdown 中读取内核态地址改成在用户态读取 System Register，而这本来是在内核态才能读取的

### Retbleed (Return Stack Buffer Underflow)

- [Retbleed](https://comsec.ethz.ch/research/microarch/retbleed/)
- [CVE-2022-29900](https://nvd.nist.gov/vuln/detail/CVE-2022-29900)
- [CVE-2022-29901](https://nvd.nist.gov/vuln/detail/CVE-2022-29901)
- [Return Stack Buffer Underflow](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/return-stack-buffer-underflow.html)
- 顾名思义，针对的是 Return Stack Buffer，它是一个栈，call 的时候压栈，ret 的时候弹栈，那么如果 ret 的时候，栈已经空了，也就是所谓的 Underflow，此时会有什么样的行为？
- 在部分处理器上，当 Return Stack Buffer 为空的时候，ret 的预测会交给间接分支预测器去预测，而间接分支预测器在之前 Spectre Variant 2 Branch Target Injection 的时候，就被攻击过了
- Intel 处理器对 Return Stack Buffer Underflow 的处理方式有如下几种类型：
	- RSB Alternate (RSBA)：RSB 为空时，用间接分支预测器预测 ret，会受到其他特权级的影响，此时会有安全问题
	- Restricted RSB Alternate (RRSBA): RSB 为空时，用间接分支预测器预测 ret，如果打开了 eIBRS，则在一个特权级下的预测不会受到其他特权级的影响（例如用户态无法影响到内核态）
	- RRSBA_DIS_S: 可以通过配置 `IA32_SPEC_CTRL.RRSBA_DIS_S = 1`，使得在 RSB 为空时，不去预测 ret 的目的地址
- 缓解措施：
	- RSB stuffing/filling
	- RRSBA_DIS_S
	- untrained return thunk

### Speculative Return Stack Overflow (SRSO/Spec rstack overflow/INCEPTION)

- [Speculative Return Stack Overflow (SRSO)](https://docs.kernel.org/admin-guide/hw-vuln/srso.html)
- [Inception: how a simple XOR can cause a Microarchitectural Stack Overflow](https://comsec.ethz.ch/inception)
- [TECHNICAL UPDATE REGARDING SPECULATIVE RETURN STACK OVERFLOW](https://www.amd.com/content/dam/amd/en/documents/corporate/cr/speculative-return-stack-overflow-whitepaper.pdf)
- [CVE-2023-20569](https://www.cve.org/CVERecord?id=CVE-2023-20569)
- 原理：
	- ret 的目的地址由 Return Stack Buffer 来预测，预测的前提是有一个匹配的 call
	- 正常情况下，call 和 ret 是可以配对的，那么 ret 会被预测到 call 的下一条指令的地址上
	- 在 AMD 的一些处理器上，BTB 是可能出现 alias 的，也就是不同的地址会被映射到同一个 BTB Entry 上，并且无法区分
	- 如果两段代码，被映射到同一个 BTB Entry 上，第一段代码有 call，第二段代码没有，假如通过执行第一段代码，让 BTB 记录下第一段代码的 call 指令信息，那么 BTB 在预测第二段代码的时候，会认为第二段代码也有 call，即使实际上并没有
	- 在 BTB 预测第二段代码有 call 的时候，会更新 Return Stack Buffer 的状态，进而影响了后续 ret 指令的预测，即使第二段代码实际上并没有 call 指令
- 缓解措施：
	- 硬件上，BTB 也要用 full tag 比较，不允许 alias
	- Safe RET
	- Indirect Branch Prediction Barrier (IBPB)

### Gather Data Sampling (DOWNFALL)

- [Downfall Attacks](https://downfall.page/)
- [论文 Downfall: Exploiting Speculative Data Gathering](https://downfall.page/media/downfall.pdf)
- [Gather Data Sampling](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/gather-data-sampling.html)
- [CVE-2022-40982](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40982)
- 原理：
	- Intel 处理器在实现 SIMD Gather 指令的时候，为了提升性能，会把 Gather 读取的缓存行的数据放在一个临时的 Buffer 当中，而这个 Buffer 是没有隔离的，同一个物理核的两个逻辑核会用同一个
	- 在一个物理核的第一个逻辑核上进行正常的 SIMD Gather 指令，在同一个物理核的第二个逻辑核上也进行一个 SIMD Gather 指令，由于 Buffer 的共享，可能会导致在预测执行路径上，第一个逻辑核的 SIMD Gather 读出来的数据被转发到第二个逻辑核的 SIMD Gather 结果
	- 这个被转发的数据是错误的，之后会被回滚并纠正为正确的数据；但是回滚前，被转发的数据已经传播出去了
	- 于是在第二个逻辑核上通过缓存的侧信道，就可以推测出第一个逻辑核使用 SIMD Gather 读取了什么数据：
		```asm
		// Step (i): Increase the transient window
		lea addresses_normal, %rdi
		clflush (%rdi)
		mov (%rdi), %rax

		// Step (ii): Gather uncacheable memory
		lea addresses_uncacheable, %rsi
		mov $0b1, %rdi
		kmovq %rdi, %k1
		vpxord %zmm1, %zmm1, %zmm1
		vpgatherdd 0(%rsi, %zmm1, 1), %zmm5{%k1}

		// Step (iii): Encode (transient) data to cache
		movq %xmm5, %rax
		encode_eax

		// Step (iv): Scan the cache
		scan_flush_reload
		```
	- 为了扩大预测执行的窗口，使得信息能够通过缓存侧信道传递出来，在上述第二个逻辑核上首先访问不在缓存中的缓存行，再使用 SIMD Gather 访问无法缓存的内存
	- 进一步测试，发现不仅能够泄露第一个逻辑核上使用 SIMD Gather 指令读取的数据，用其他很多 SIMD Load 指令读出来的数据也可以通过在第二个逻辑核上用 SIMD Gather 泄露出来
	- 进一步测试，发现不仅能够泄露同一个物理核的另一个逻辑核的数据，同一个逻辑核内的数据也可以从内核态泄露到用户态
- 缓解措施：
	- 硬件 Microcode 修复

### Branch History Injection/Intra-mode BTI (IMBTI)

- [Branch History Injection/Intra-mode BTI](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/branch-history-injection.html)
- [CVE-2022-0001](https://nvd.nist.gov/vuln/detail/cve-2022-0001)
- [CVE-2022-0002](https://nvd.nist.gov/vuln/detail/cve-2022-0002)
- 原理：
	- 用于记录分支历史的 Branch History Buffer（BHB，实际上就是 Path History Register）没有在特权态之间隔离
	- IBRS/eIBRS 隔离了间接分支预测器的状态，但没有隔离 BHB，用户态程序可以向 BHB 注入分支历史来操控内核态的间接分支预测
- 缓解措施：
	- Retpoline
	- Enhanced Indirect Branch Restricted Speculation (Enhanced IBRS)
	- Supervisor-Mode Execution Prevention (SMEP)
	- BHI_DIS_S
	- IPRED_DIS_S
	- Software BHB Clearing

### ITLB Multihit

- [iTLB multihit](https://www.tacitosecurity.com/multihit.html)
- [CVE-2018-12207](https://nvd.nist.gov/vuln/detail/cve-2018-12207)
- [INTEL-SA-00210 Intel® Processor Machine Check Error Advisory](https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00210.html)
- [iTLB multihit from linux docs](https://docs.kernel.org/admin-guide/hw-vuln/multihit.html)
- 原理：
	- ITLB Multihit 是一个 DoS 漏洞，在虚拟机内可以让宿主机死机
	- 在虚拟机内的内核，通过修改页表的大小，使得同一个地址出现在不同大小页表对应的 ITLB 表项时，会导致宿主机出现 Machine Check Error，无法继续工作
- 缓解措施：
	- 宿主机观测虚拟机的页表，如果虚拟机分配了可执行的大页，则宿主机把它拆分成多个 4K 大小的页，避免了问题

### L1 Terminal Fault (L1TF, Foreshadow)

- [L1TF - L1 Terminal Fault from linux docs](https://www.kernel.org/doc/html/next/admin-guide/hw-vuln/l1tf.html)
- 原理：
	- 处理器在推测执行的时候，有时候会无视掉页表项的 Present bit，即使它最终会导致 page fault，但还是会执行/读取它指向的物理地址的指令/数据
- 环节措施：
	- PTE inversion：避免 Present bit 设为 0 的页表项的物理地址指向一个合法的可以被缓存的物理地址，从而避免内存中数据的泄漏

### Microarchitectural Data Sampling (MDS)

- [MDS - Microarchitectural Data Sampling](https://www.kernel.org/doc/html/next/admin-guide/hw-vuln/mds.html)
- [Microarchitectural Data Sampling (MDS) mitigation](https://www.kernel.org/doc/html/next/arch/x86/mds.html)
- 原理：
	- 处理器为了提升性能，load 指令可以从一些先前指令或者缓存 refill 获取结果
	- 获取到的结果可能来自错误的指令，从而泄露了信息，即使这条 load 指令最终会被回滚，但可能把数据通过侧信道泄露出去
- 缓解措施：
	- 切换特权级或在宿主机和虚拟机之间切换时，清空微架构上的状态以避免数据泄露

### Register File Data Sampling

- [Register File Data Sampling / CVE-2023-28746 / INTEL-SA-00898](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/register-file-data-sampling.html)
- 原理：
	- 在部分 Atom 处理器上，`VERW` 指令可能会泄漏浮点寄存器的旧值，这个旧值可能来自其他进程或者其他特权态
- 缓解措施：
	- 升级 Microcode
	- 主动执行 `VERW` 指令来避免旧值被后续代码泄漏

### Speculative Store Bypass (SSB)

- [Speculative Store Bypass / CVE-2018-3639 / INTEL-SA-00115](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/speculative-store-bypass.html)
- 又称 Spectre Variant 4
- 原理：
	- 处理器为了提升 load 指令性能，会预测 load 指令的数据可以从哪条 store 指令获取
	- 如果欺骗这个预测器，让它预测 load（下面的 `Y = ...`）从错误的 store 指令处（下面的 `X = &K`）获取数据，可以在一个推测执行窗口中操控 load 读取的数据，进而泄露数据：

	```c
	X = &K;    // Attacker manages to get variable with address of K stored into pointer X
	<at some later point>
	X = &M;      // Does a store of address of M to pointer X
	Y = Array[*X & 0xFFFF]; // Dereferences address of M which is in pointer X in order to
          // load from array at index specified by M[15:0]
	```
- 缓解措施：
	- 添加 LFENCE 以阻止推测执行
	- 设置 Speculative Store Bypass Disable (SSBD)

### Zenbleed

- [Zenbleed](https://lock.cmpxchg8b.com/zenbleed.html)
- 原理：
	- 部分 AMD 处理器在处理向量处理器和分支预测错误恢复时有 BUG，导致可能会泄露向量寄存器的旧值
- 缓解措施：
	- 升级 Microcode

### TSX Asynchronous Abort

- [TAA - TSX Asynchronous Abort](https://docs.kernel.org/admin-guide/hw-vuln/tsx_async_abort.html)
- [Intel® Transactional Synchronization Extensions (Intel® TSX) Asynchronous Abort / CVE-2019-11135 / INTEL-SA-00270](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/intel-tsx-asynchronous-abort.html)
- Intel Transactional Synchronization Extensions (TSX) 是 Intel 的 Transactional Memory 的实现，可以把一系列的指令当成一个事务原子地完成
- 原理：
	- 攻击者启动一个 TSX Transaction，当它被异步地打断时，一些指令会在推测执行路径上读取到处理器内部结构的值，进而泄露信息

### Special Register Buffer Data Sampling (SRBDS)

- [SRBDS - Special Register Buffer Data Sampling](https://docs.kernel.org/admin-guide/hw-vuln/special-register-buffer-data-sampling.html)
- 原理：
	- RDRAND 和 RDSEED 指令的结果会保存在 Special Register Buffer 当中
	- 通过 Microarchitectural Data Sampling (MDS) 的方法，可以泄露出 Special Register Buffer 的内容，从而嗅探到随机数生成指令的结果

### MMIO Stale Data

- [Processor MMIO Stale Data Vulnerabilities](https://docs.kernel.org/admin-guide/hw-vuln/processor_mmio_stale_data.html)
- 原理：
	- 在虚拟机中的攻击者，可以对外设进行 MMIO，MMIO 的不当实现可能会泄露核上宿主机或其他虚拟机的数据

### Indirect Target Selection

- CVE-2024-28956
- [Indirect Target Selection / INTEL-SA-01153](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/indirect-target-selection.html)
- [Training Solo](https://www.vusec.net/projects/training-solo/)
- 原理：
	- 部分 Intel 的 CPU 有 BUG，使得在缓存行前半部分（根据分支的最后一个字节的位置判断）的间接分支，它的目的地址可以被预测为缓存行后半部分的分支的目的地址
- 缓解措施：
	- 微码更新
	- 把间接分支放到缓存行的后半部分

### Branch Privilege Injection

- CVE-2024-45332
- [Branch Privilege Injection](https://comsec.ethz.ch/research/microarch/branch-privilege-injection/)
- 原理：
	- 分支预测器的更新是异步的，从一个分支的正确结果出来，到把结果用于分支预测器的训练，需要若干个周期
	- 切换特权态或者进行 IBPB（Indirect Branch Prediction Barrier）的时候，异步的更新依然在进行，导致有一些分支预测器的更新从一个特权态泄露到了另一个特权态
- 缓解措施：
	- 微码更新

## 缓解措施 Mitigations

### KASLR

- KASLR: Kernel Address Space Layout Randomization
- 随机化内核地址，避免攻击者猜测出内核地址

### Kernel Page Table Isolation (KPTI/PTI/KAISER)

- 又称 KAISER：[论文 KASLR is Dead: Long Live KASLR](https://gruss.cc/files/kaiser.pdf)
- 在用户态的页表里，不要映射整个内核态空间，只映射必须映射的部分，进入内核态后，再切换到具有完整的内核态地址空间的页表
- 那么在用户态尝试读取内核态地址的时候，由于地址不在 TLB 当中，也就无法读取内存，不会泄漏数据
- 修复 Meltdown 漏洞


### Retpoline

- [Retpoline](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/retpoline-branch-target-injection-mitigation.html)
- 把间接分支替换为 call/ret 对，同时把栈上的地址改成实际的目的地址，强迫硬件用 Return Stack Buffer 做预测，但由于覆盖了返回地址，Return Stack Buffer 总是会预测错误，在错误路径上循环执行 pause-lfence-jmp 三条指令，不会被攻击者控制，但会损失性能
- 针对间接跳转：
	```asm
	# for indirect jmp:
	# before:
	jmp *%rax

	# after:
	call load_label # push the address of capture_ret_spec to the stack

	capture_ret_spec:
	pause
	lfence
	jmp capture_ret_spec

	load_label:
	mov %rax, (%rsp) # override the return address on the top of the stack
	ret # the return stack buffer predicts to jump to capture_ret_spec
	```
- 针对间接调用：
	```asm
	# for indirect call:
	# before:
	call *%rax

	# after:
	jmp label2
	label0:
		call label1 # push the address of capture_ret_spec to the stack

	capture_ret_spec:
		pause
		lfence
		jmp capture_ret_spec

	label1:
		mov %rax, (%rsp) # override the return address
		ret

	label2:
		call label0 # use extra call to maintain real return address
		# continue execution
	```
- 修复基于间接分支的漏洞：Spectre Variant 2 Branch Target Injection

### Supervisor-Mode Execution Prevention (SMEP)

- [Supervisor-Mode Execution Prevention (SMEP)](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/related-intel-security-features-technologies.html) 在内核态下，禁止运行（包括推测运行）用户态地址空间内的代码，这样就缩小了攻击者可利用的代码范围
- 又称 Intel® OS Guard
- SMEP 本身不能修复漏洞，但可以给攻击者创造更多限制

### Supervisor-Mode Access Prevention (SMAP)

- [Supervisor-Mode Access Prevention (SMAP)](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/related-intel-security-features-technologies.html) 在内核态下，禁止访问（包括推测访问）用户态空间的内存，缩小攻击者可以利用的内存范围；代价是在需要访问用户态空间的内存时，内核需要临时关闭 SMAP
- SMAP 相当于是把 SMEP 的限制从执行权限扩展到了读写权限
- SMAP 本身不能修复漏洞，但可以给攻击者创造更多限制
- x86 上，首先在 CR4 寄存器中启用 SMAP，此时默认情况下内核不能访问用户态的数据，只有在 `stac` 指令之后且在 `clac` 指令之前的区间内可以访问用户态数据：

	```asm
	# cannot access user pointers
	stac
	# can access user pointers
	clac
	# cannot access user pointers
	```
- ARMv8 上，这个功能通过 [PAN(Privileged Acess Never)](https://developer.arm.com/documentation/ddi0601/2025-03/AArch64-Registers/PAN--Privileged-Access-Never) 实现
- 虽然内核不能用用户态的指针访问用户态的数据，但由于 Linux 下所有的物理地址都被映射到了内核的地址空间，所以如果可以获取到用户态的指针对应的物理地址在内核态中被映射的地址，也可以在内核态访问它

### Bounds Clipping

- 边界检查如果用条件分支实现，可能会在分支预测的错误路径上访问边界外的内存
- Bounds Clipping 以性能损失为代价，把边界检查的条件分支变成计算，从而避免了错误路径的预测执行
- Linux 的实现： [`array_index_nospec`](https://www.kernel.org/doc/Documentation/speculation.txt) 宏
- 修复 Spectre Variant 1 即 Bounds Check Bypass 漏洞

### Indirect Branch Restricted Speculation (IBRS)

- [Indirect Branch Restricted Speculation (IBRS)](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/indirect-branch-restricted-speculation.html)
- [AMD64 TECHNOLOGY INDIRECT BRANCH CONTROL EXTENSION](https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/white-papers/111006-architecture-guidelines-update-amd64-technology-indirect-branch-control-extension.pdf)
- 从用户态切换到内核态后，在内核态设置 `IA32_SPEC_CTRL.IBRS = 1` 可以保证内核态后续间接分支的预测不会被用户态影响
- 只保护了间接分支的预测，不保护 Return Stack Buffer
- 只避免了用户态对内核态的间接预测器的影响，但不同用户态进程间（包括虚拟机之间）还是会互相影响
- IBRS 包括了 STIBP 的功能：如果开启了 IBRS，那么同一个物理核的两个逻辑核之间的间接分支预测器也会被隔离
- 此外 IBRS 还会保证内核态和 Enclave 以及 SMM（System Management Mode）之间的隔离，在 Linux 里称这个功能为 IBRS_FW，表示对固件的保护
- 修复基于间接分支的漏洞：Spectre Variant 2 Branch Target Injection

### Enhanced Indirect Branch Restricted Speculation (Enhanced IBRS/eIBRS)

- [Indirect Branch Restricted Speculation (IBRS)](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/indirect-branch-restricted-speculation.html) 每次从用户态切换到内核态都要写入一次 `IA32_SPEC_CTRL.IBRS`，降低性能
- [AMD64 TECHNOLOGY INDIRECT BRANCH CONTROL EXTENSION](https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/white-papers/111006-architecture-guidelines-update-amd64-technology-indirect-branch-control-extension.pdf)
- Enhanced IBRS：打开一次以后，总是启用 IBRS
- 不再需要每次从用户态切换到内核态去写入 `IA32_SPEC_CTRL.IBRS`
- 修复基于间接分支的漏洞：Spectre Variant 2 Branch Target Injection
- Post-barrier Return Stack Buffer with eIBRS enabled (PBRSB-eIBRS)：即使打开了 eIBRS，由于 IBRS 主要针对的是间接分支预测，对于 ret 的保护是不足的，所以需要额外的针对 Return Stack Buffer 的防护

### Single Threaded Indirect Branch Predictors (STIBP)

- [Single Thread Indirect Branch Predictors](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/single-thread-indirect-branch-predictors.html)
- [AMD64 TECHNOLOGY INDIRECT BRANCH CONTROL EXTENSION](https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/white-papers/111006-architecture-guidelines-update-amd64-technology-indirect-branch-control-extension.pdf)
- SMT 场景下，同一个物理核的两个逻辑核共享间接分支预测器，因此可以从一个逻辑核操控另一个逻辑核的间接分支预测器
- STIBP 设置启用后（`IA32_SPEC_CTRL.STIBP = 1`），保证了逻辑核之间的间接分支预测器的隔离
- 修复基于间接分支的漏洞：Spectre Variant 2 Branch Target Injection

### Indirect Branch Prediction Barrier (IBPB)

- [Indirect Branch Predictor Barrier](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/indirect-branch-predictor-barrier.html)
- [AMD64 TECHNOLOGY INDIRECT BRANCH CONTROL EXTENSION](https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/white-papers/111006-architecture-guidelines-update-amd64-technology-indirect-branch-control-extension.pdf)
- IBPB 是一个预测器的 Barrier，保证 Barrier 之前的指令不会影响 Barrier 之后的指令的间接分支预测
- 这个 Barrier 通过写入 MSR `IA32_PRED_CMD.IBPB = 0` 实现，没有引入新的指令
- 前面提到，IBRS 只考虑了用户态对内核态的影响，没有考虑用户态之间的影响，这可以由 IBPB 来补足
- 修复基于间接分支的漏洞：Spectre Variant 2 Branch Target Injection

### RSB filling/stuffing

- [Retpoline](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/retpoline-branch-target-injection-mitigation.html)
- 由于 Return Stack Buffer 在空的时候，会使用被攻击者控制的间接分支预测器来预测目的地址
- 为了缓解这个问题，提前向 Return Stack Buffer 填充一些地址，避免出现 Underflow 的问题，这就叫 RSB filling/stuffing：
	```asm
	.rept 16
		call 1f
		pause
		lfence

		1:
	.endr
	addq $(8 * 16), %rsp
	```

### Safe RET

- Safe RET 和 Retpoline 类似，也是要强迫 ret 被预测到指定的错误路径上，避免被攻击者控制预测的地址
- 但 Safe RET 要解决的是 Speculative Return Stack Overflow 漏洞中，BTB 出现 alias 的问题
- 因此 Safe RET 的解决办法是，主动构造 BTB alias，先把攻击者从 BTB 中刷掉，再去进行实际的 ret

### Software BHB Clearing

- Software BHB（Branch History Buffer）Clearing 的目的是防止用用户态控制的 BHB 来进行内核态的间接分支的预测
- 因此实现上就是在用户态切换到内核态的时候，首先调用足够次数的分支，使得 BHB 中由用户态设置的部分被刷掉，保证用于内核态间接分支预测的 BHB 是安全的

### Intel MSR

- Intel 处理器上很多缓解措施的控制都和两个 MSR 有关：IA32_SPEC_CTRL 和 IA32_PRED_CMD，这里总结一下它们的各个字段：
- IA32_SPEC_CTRL:
	- [0]: IBRS, Indirect Branch Restricted Speculation，隔离用户态和内核态的间接分支预测
	- [1]: STIBP, Single Thread Indirect Branch Predictor，隔离同一个物理核的两个逻辑核的间接分支预测
	- [2]: SSBD，Speculative Store Bypass Disable，等先前的所有的 store 地址已知后，再预测执行 load
	- [3]: IPRED_DIS_U，Indirect Predictor Disable User，用户态下，等到间接分支的目的地址被实际计算出来后才进行后续的执行
	- [4]: IPRED_DIS_S，Indirect Predictor Disable Supervisor，内核态下，等到间接分支的目的地址被实际计算出来后才进行后续的执行
	- [5]: RRSBA_DIS_U，Restricted Return Stack Buffer Alternate User，用户态下，当 Return Stack Buffer 为空的时候，禁止预测
	- [6]: RRSBA_DIS_S，Restricted Return Stack Buffer Alternate Supervisor，内核态下，当 Return Stack Buffer 为空的时候，禁止预测
	- [7]: PSFD，禁止 Fast Store Forwarding Predictor
	- [8]: DDPD_U，用户态下禁止 Data Dependent Prefetcher
	- [10]: BHI_DIS_S，Branch History Injection Disable Supervisor，隔离用户态和内核态用于分支预测的分支历史
- IA32_PRED_CMD:
	- [0]: IPBP，Indirect Branch Prediction Barrier，阻止 Barrier 前面的指令影响 Barrier 后面的指令的间接分支预测

### __user pointer sanitization

- [[PATCH v6 13/13] x86/spectre: report get_user mitigation for spectre_v1](https://lore.kernel.org/all/151727420158.33451.11658324346540434635.stgit@dwillia2-desk3.amr.corp.intel.com/T/#u)
- 内核在访问用户态的地址的时候，添加 barrier 以避免推测执行

### untrained return thunk

- 为了避免 ret 被预测，利用 x86 指令集编码的特性，使得 ret 指令被解释为非 ret 指令的一部分，再去执行这条 ret 指令，此时它就不会被预测，这个特别的指令序列如下（对应 Linux 的 [`retbleed_untrain_ret` 函数](https://github.com/torvalds/linux/blob/2df0c02dab829dd89360d98a8a1abaa026ef5798/arch/x86/lib/retpoline.S#L272)）：

	```asm
	1:
	.byte 0xf6
	2:
	ret
	int 3
	lfence
	jmp 2b
	int 3
	```

- 这段代码从 `1:` 处开始执行，由于 `test $0xcc, %bl` 的编码和 `.byte 0xf6; ret; int3` 指令相同，所以它的语义相当于是 `test $0xcc, %bl; lfence; jmp 2b`；然后跳转到 `2:` 处的 ret 指令
- 在执行 `test $0xcc, %bl` 的时候，就会把 `ret` 指令标记为非分支指令，之后再去执行它的时候，预测器就不会工作，从而避免了漏洞的利用
