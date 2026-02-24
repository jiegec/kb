# 原子指令

现在的处理器，一般会提供如下几种形式的原子指令：

1. LL(Load-Linked)/SC(Store-Conditional)
2. CAS(Compare And Swap)
3. AMO(Atomic Memory Operation)
4. HTM(Hardware Transactional Memory)

它们在软件的使用方式和硬件实现上有所区别，下面来讨论这些原子指令。

## 背景

首先讨论一下为什么需要有原子指令。假设现在有一个多线程程序在多核处理器上运行，每个线程都需要对内存中同一个地址的数据进行加一的操作。在处理器中，加一的操作实际上分为三步：

1. 从内存中读取当前的值
2. 求值加一的结果
3. 把加一的结果写入到内存中

但是这三个操作是分别进行的，可能会出现这么一种情况：

1. 线程一读取内存中的值等于 0
2. 线程二读取内存中的值等于 0
3. 线程一计算 0 加 1 等于 1
4. 线程二计算 0 加 1 等于 1
5. 线程一把 1 写入内存
6. 线程二把 1 写入内存

于是加法的结果就被丢弃了。下面用 OpenMP 给出了一个例子：

```cpp
#include <stdio.h>
int count = 0;
int main() {
#pragma omp parallel for
  for (int i = 0; i < 100000; i++) {
    count++;
  }

  printf("%d\n", count);
  return 0;
}
```

如果用多核执行，得到的结果会是一个远小于 100000 的结果。如果把程序绑定到一个核心上（`numactl -C 0`），就会得到正确的 100000 的结果。因此需要用原子指令来保证更新的原子性。

在讨论原子指令的硬件实现时，会涉及到缓存一致性协议的内容。如果对这方面还缺乏了解，可以参考 [缓存一致性](../hardware/cache_coherence_protocol.md) 的内容。

## LL/SC

### 定义

[LL/SC](https://en.wikipedia.org/wiki/Load-link/store-conditional) 是一对指令，其中 LL 指令从内存地址 read_addr 中读取数据到寄存器 read_data；SC 指令执行时，如果要写入的内存地址 write_addr 和之前用 LL 指令读取的内存地址 read_addr 相同，并且在 LL 指令后，被 LL 访问的内存区域（粒度可能是 32 位，也可能更粗，例如一个缓存行）没有被修改，那么写入寄存器 write_data 的值到同样的地址 write_addr；否则就不写入。SC 指令的写入是否成功，会通过向目的寄存器 dest 写入不同的值来区分。也就是说，如果 SC 写入成功，就保证了从 LL 到 SC 这段时间内，这段内存没有被改变。

### 常见用法

LL/SC 的通常用法是，实现一个读 - 改 - 写（read-modify-write）操作：首先用 LL 指令读取内存，然后对寄存器进行计算，再用 SC 指令把结果写入内存：如果中途内存的值被其他处理器核心修改了，那么用 LL 指令读取的结果是旧的，用的也是旧的值做计算，计算结果就不会被 SC 写进去；否则，说明 LL 指令读取的值和内存中的值是相同的，SC 指令把更新后的结果写入到内存中。

因此 LL/SC 在使用的时候，通常会和循环放在一起用：如果 SC 失败，就重新开始读 - 改 - 写操作，直到 SC 成功。用 LL/SC 实现对内存进行原子加一操作（Atomic Add One）的伪代码如下：

```asm
loop:
    # Read
    ll data, addr
    # Modify
    add data, data, 1
    # Write
    sc result, data, addr
    # Try again if SC failed
    goto loop if failed
```

### 指令集架构支持

在 RISC-V 的 A 扩展中，LL 指令叫做 LR（Load-Reserved），SC 指令还是叫做 SC。下面是 RISC-V 指令集手册中给出的一段用 LL/SC 实现原子比较和写入（Atomic Compare And Set）操作的[代码](https://github.com/riscv/riscv-isa-manual/blob/cd30ad51f1b282a3b409bd803bc02a0e03afbbf2/src/a-st-ext.adoc?plain=1#L227)：

```asm
    # a0 holds address of memory location
    # a1 holds expected value
    # a2 holds desired value
    # a0 holds return value, 0 if successful, !0 otherwise
cas:
    lr.w t0, (a0)        # Load original value.
    bne t0, a1, fail     # Doesn't match, so fail.
    sc.w t0, a2, (a0)    # Try to update.
    bnez t0, cas         # Retry if store-conditional failed.
    li a0, 0             # Set return to success.
    jr ra                # Return.
fail:
    li a0, 1             # Set return to failure.
    jr ra                # Return.
```

代码利用 LL/SC 指令，把 a0 指向的内存的值和 a1 的值比较，如果相等，就把 a2 写到 a0 指向的内存，返回成功；如果不相等，则不修改内存的值，返回错误。

除了内存被其他处理器核心写入会导致 SC 失败以外，一些指令集架构允许程序手动让 SC 失败，以 LoongArch 为例，标准要求：

LL.{W/D} 执行时记录下访问地址并置上一个标记（LLbit 置为 1），SC.{W/D} 指令执行时会查看 LLbit，仅当 LLbit 为 1 时才真正产生写动作，否则不写。在配对的 LL-SC 执行期间，下列事件会让 LLbit 清 0:

- 执行了 ERTN 指令且执行时 CSR.LLBCTL 中的 KLO 位不等于 1;
- 其它处理器核或 Cache Coherent master 对该 LLbit 对应的地址所在的 Cache 行执行完成了一个 store 操作。

这样做的目的是，如果在 LL 和 SC 之间触发了上下文切换，操作系统可以把 SC 自动取消掉，详情可以看 LoongArch 的 CSR.LLBCTL 的定义。

[其他实现了 LL/SC 的指令集架构](https://en.wikipedia.org/wiki/Load-link/store-conditional#Implementations)：

- Alpha: ldl_l/stl_c, ldq_l/stq_c
- PowerPC/Power ISA: lwarx/stwcx, ldarx/stdcx
- MIPS: ll/sc, llwp/scwp(Double Width)
- ARM: ldrex/strex(ARMv6 & ARMv7), ldxr/stxr(ARMv8), ldxp/stxp(Double Width, ARMv8)
- ARC: llock/scond

实际实现时，根据处理器实现不同，检测内存访问的粒度可能不同。

### 硬件实现

在处理器中，LL/SC 的实现并不复杂：缓存一致性协议下，保证了当一个缓存行被更新的时，所有拥有该缓存行的核心都会被通知到。因此，LL 指令只需要在读取缓存的基础上，在缓存上打一个标记；通过缓存一致性协议，如果发现有其他核心要写入 LL 指令读取的缓存行，或者该缓存行要被 Evict，那就记录一个 SC 失败标记，使得下一次 SC 指令失败。实现 SC 指令时，首先检查它的地址是否和 LL 指令相同，如果相同，并且没有触发 SC 失败标记，那就进行实际的写入。伪代码如下：

```c
Init() {
    LLvalid = 0;
    LLaddr = 0;
}

LL(addr) {
    data = memory[addr];
    LLaddr = addr;
    LLvalid = 1;
    return data;
}

SC(addr, data) {
    if (LLaddr == addr && LLvalid) {
        memory[addr] = data;
        return SUCCESS;
    } else {
        return FAIL;
    }
}

Invalidate(addr) {
    if (addr == LLaddr) {
        LLvalid = 0;
    }
}
```

### 活锁

LL/SC 在使用的时候，潜在的一个问题是，可能会出现活锁：当 LL 和 SC 之间执行的指令比较多，花费的时间比较长，可能使得 LL/SC 一直被其他核心打断，没有办法实现进展。

此外，编写 LL/SC 程序的时候也需要小心，避免在中间进行一些比较复杂的操作，因为这些操作可能导致 SC 的时候总是失败：例如在 LL/SC 中途访问其他内存，可能会导致 SC 要写入的的缓存行被 Evict。

因为这个问题，RISC-V 在标准中定义了一些[条件](https://github.com/riscv/riscv-isa-manual/blob/cd30ad51f1b282a3b409bd803bc02a0e03afbbf2/src/a-st-ext.adoc?plain=1#L255)，如果满足了这些条件，就可以避免活锁的发生：

- The loop comprises only an LR/SC sequence and code to retry the sequence in the case of failure, and must comprise at most 16 instructions placed sequentially in memory.
- An LR/SC sequence begins with an LR instruction and ends with an SC instruction. The dynamic code executed between the LR and SC instructions can only contain instructions from the base “I” instruction set, excluding loads, stores, backward jumps, taken backward branches, JALR, FENCE, and SYSTEM instructions. If the “C” extension is supported, then compressed forms of the aforementioned “I” instructions are also permitted.
- The code to retry a failing LR/SC sequence can contain backwards jumps and/or branches to repeat the LR/SC sequence, but otherwise has the same constraint as the code between the LR and SC.
- The LR and SC addresses must lie within a memory region with the LR/SC eventuality property. The execution environment is responsible for communicating which regions have this property.
- The SC must be to the same effective address and of the same data size as the latest LR executed by the same hart.

因为 LL/SC 的局限性，现在很多算法会用下面讲到的 CAS 或者 AMO 指令来实现。

## CAS

### 定义

CAS（Compare-And-Swap）指令做的事情是，把内存中的值和给定的值进行比较，如果相同，那么写入一个新的值；把写入是否成功写入目的寄存器中，或者把旧值写入到目的寄存器中：

```asm
cas dest, addr, compare, new
```

相当于原子地完成了如下操作：

```c
if (memory[addr] == compare) {
    memory[addr] = new;
    dest = 1;
} else {
    dest = 0;
}
```

或者返回内存中的旧值：

```c
dest = memory[addr];
if (memory[addr] == compare) {
    memory[addr] = new;
}
```

### 常见用法

CAS 指令的常见用法是，放在循环中，首先读取内存中的值，进行一系列计算，用 CAS 指令进行对内存的原子更新：如果内存的值没有变，那就把新的值写入；如果内存的值变了，那就循环重新尝试：

```asm
loop:
    # Read
    load old_data, addr
    # Modify
    add new_data, old_data, 1
    # Compare-And-Swap
    cas dest, addr, old_data, new_data
    # Try again if CAS failed
    goto loop if failed
```

这样就实现了原子加一操作。和 LL/SC 一样，也需要在循环中不断尝试更新，直到更新成功为止。

对于返回内存中旧值的 CAS 指令，可以把 dest 和 old_data 进行比较来判断 CAS 是否成功。有的 CAS 指令既返回了 CAS 是否成功的信息，又返回了内存中的旧值。

这个过程看起来和 LL/SC 很像，但是有如下的不同：

1. LL/SC 需要两条原子指令，分别在开头的读和最后的写；CAS 只有一条原子指令，在最后实现写入。
2. LL/SC 需要的操作数比较少：LL 是一个源操作数，也就是要读取的内存地址，一个目的操作数，用来保存读取的值；SC 是两个源操作数，包括要写入的内存地址和数据，一个目的操作数，用来保存 SC 是否成功的结果；CAS 需要的操作数比较多：三个源操作数，包括内存地址、比较数据和新数据，一个目的操作数，用来保存 CAS 是否成功或者内存旧值。
3. CAS 可能会遇到 ABA 问题：在 Read-Modify-CAS 过程中，如果内存中的值从 A 变成了 B，又从 B 变回了 A，CAS 依然会成功，因为它写入与否，仅取决于比较是否相等；而 LL/SC 会由硬件监测中途的内存访问，只要内存中的值被写入过，无论最后的值是否回到了 LL 读取的值，都会让 SC 失败。下面来讨论 ABA 问题。

### ABA 问题

ABA 问题就是指的在 Read-Modify-Write 循环中，如果内存中的值从 A 变成了 B，又从 B 变成了 A，是否会影响写入是否成功的问题。LL/SC 的答案是，如果出现了 ABA 的情况，会使得写入失败；CAS 的答案是，ABA 情况下写入依然成功。

为什么要讨论 ABA 问题呢？这是因为一些无锁数据结构的实现，是不允许 ABA 情况的出现的。这个时候，就需要用 LL/SC，或者用下面要介绍的 DWCAS（Double Width Compare And Swap）指令，而不是 CAS 指令。

### DWCAS

DWCAS（Double Width Compare And Swap）指令其实也是 CAS 指令，只不过它的内存操作的粒度是处理器位数的两倍：例如 32 位处理器，DWCAS 的操作宽度就是 64 位；64 位处理器，DWCAS 的操作宽度就是 128 位。

引入 DWCAS 可以解决 ABA 的问题：既然问题出在值会从 A 到 B 再回到 A，那就让值“不回到”A，不就好了？每次更新的时候，除了原本要更新的值，同时更新一个 counter，这个 counter 每次更新都加一。counter 溢出需要很多很多次 CAS，因此可以认为不会出现 ABA 的情况，这时候就解决了 ABA 问题。

但是，通常处理器都只会提供不超过处理器位数的内存指令，例如 32 位处理器提供 8 位、16 位和 32 位 CAS，那要是需要更新的值已经占了 32 位，怎么同时更新 counter 呢？所以就不得不引入了 DWCAS，在 32 位处理器上提供 64 位 CAS，多的那 32 位就可以拿来更新 counter。

但是 DWCAS 实现起来也会比较复杂：每个操作数的位宽都翻倍了，原来的一个通用寄存器放不下了，怎么办？一个朴素的办法是，传更多的操作数，两个操作数拼起来合成一个两倍位宽的值，但是这样在指令编码中，操作数占用的位数太多：

```asm
cas dest_hi, dest_lo, addr, old_data_hi, old_data_lo, new_data_hi, new_data_lo
```

一个解决方法是，一个操作数对应两个连续的通用寄存器，例如某个操作数是 2 号寄存器，代表的就是 2 号和 3 号寄存器拼接起来的两倍位宽的值。如果平台有更宽的向量寄存器，也可以把操作数放到向量寄存器上传入。但无论如何，单条指令涉及到的操作数和宽度都比较大，给处理器的设计带来了一定的挑战。

除了 DWCAS 以外，还有一种 CAS 变体：[DCAS（Double Compare and Swap）](https://en.wikipedia.org/wiki/Double_compare-and-swap)。和 DWCAS 不同的是，DCAS 实现的原子的两个 CAS 操作，这两个 CAS 可以操作不连续的内存。换句话说，DWCAS 可以认为是 DCAS 的一个特殊情况，特殊在于两个 CAS 操作的是连续的内存。


### 指令集架构支持

x86_64 指令集提供了 CAS 指令，并且提供了 DWCAS 两倍位宽版本：[cmpxchg16b 指令](https://www.felixcloutier.com/x86/cmpxchg8b:cmpxchg16b)，它把内存中的值和 RDX:RAX 比较，如果相等，就设置 ZF，并往内存写入 RCX:RBX；如果不相等，清空 ZF 并把内存中的值写入到 RDX:RAX。可以看到，这条指令采用的是多个源寄存器的方案：RDX、RAX、RCX、RBX 一共四个源 64 位通用寄存器，并且通过定死寄存器编号，解决了指令编码的问题。同时，一条指令也要写入两个通用寄存器 RDX 和 RAX，外加 FLAGS 寄存器的 ZF。

ARM64 也提供了 CAS 指令，通过 CASP 指令实现了 DWCAS：`CASP <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{,#0}]`，可以把连续两个 64 位通用寄存器拼起来，作为一个 128 位的整体来进行 CAS。

LoongArch 从 V1.1 版本开始，支持了 AMCAS 指令。RISC-V 也有可选的 [Zacas](https://github.com/riscv/riscv-zacas) 扩展。

### 硬件实现

CAS 的硬件实现也比较简单：在缓存一致性协议下，当一个缓存可以写缓存行的时候，它拥有了这个缓存行的所有权限，因此只需要在缓存里实现 CAS 即可，其他缓存无法打断这个原子的操作。

## AMO

### 定义

AMO（Atomic Memory Operations）指的是对内存中的值进行原子更新：读取内存中的值，写入到目的寄存器，同时对值进行一些更新操作，再写入内存。这个更新操作是预设的，例如位运算（AND、OR、XOR 和 SWAP）或者整数运算（ADD、MIN 和 MAX）等等。它用一条指令完成了前面 LL/SC 或者 CAS 指令的读 - 改 - 写循环做的功能，但是限制了允许的修改操作：

```asm
# Use AMO
    amoadd dest, addr, 1

# Use CAS
loop:
    # Read
    load old_data, addr
    # Modify
    add new_data, old_data, 1
    # Compare-And-Swap
    cas dest, addr, old_data, new_data
    # Try again if CAS failed
    goto loop if failed
```

### 常见用法

AMO 指令相当于是把一些常见的读 - 改 - 写循环固化成了指令，因此原来用 LL/SC 或 CAS 实现的一些原子操作，如果有对应的 AMO 指令，可以直接用 AMO 指令实现。

### 指令集架构支持

RISC-V 和 LoongArch 都提供了 AMO 指令，它们可以完成内存的原子更新，同时得到更新前的旧值。x86 指令集下，通过给 [add 指令添加 lock 前缀](https://en.wikipedia.org/wiki/Fetch-and-add#x86_implementation)，也可以实现原子更新的效果，如果要得到更新前的旧值，可以用 xadd 指令。

AArch64 提供了 AMO 指令：LDADD、LDCLR、LDEOR、LDSET、LDSMAX、LDSMIN、LDUMAX、LDUMIN、STADD、STCLR、STEOR、STSET、STSMAX、STSMIN、STUMAX、STUMIN、SWP 等等。此外，在实现了 LSFE 扩展的 AArch64 处理器上，还支持浮点的 AMO 指令：LDFADD、LDFMAX、LDFMIN、LDBFADD、LDBFMAX、LDBFMIN、STFADD、STFMAX、STFMIN、STBFADD、STBFMAX、STBFMIN。

### 硬件实现

AMO 指令的硬件实现和 CAS 类似，也是把原子操作下放到缓存中去执行。但由于 AMO 指令需要涉及少量的更新操作，例如位运算和整数运算，因此缓存内部也需要引入一个 ALU 用于实现 AMO 指令的计算。因此，目前 AMO 指令仅限于硬件开销比较小的位运算和整数运算，没有整数乘除法，也没有浮点运算。

例如 Rocket Chip 设计了一个 [AMOALU](https://github.com/chipsalliance/rocket-chip/blob/e3773366a5c473b6b45107f037e3130f4d667238/src/main/scala/rocket/AMOALU.scala#L53)，用于在 DCache 中实现 AMO 指令的计算。

## HTM

### 定义

HTM 是硬件提供的在内存上的事务。事务这个概念在数据库上比较常见，把多个对数据库的操作放到一个事务中，可以保证整个事务的原子性。HTM 也是类似的，只不过是在 CPU 上，可以保证一系列的指令对内存的操作是原子的。

### 常见用法

通常，它需要用特定的 begin 指令开始一段事务，执行一系列指令后，再用特定的 end 指令结束事务。如果在事务中途，事务被打断，例如程序主动用指令打断，或者涉及到的内存被其他处理器核心修改，那么事务就会被回滚，同时程序转移到指定的 fallback 地址继续执行，这个 fallback 地址会在 begin 指令中给出。下面是一段用硬件内存事务实现的原子加一：

```asm
retry:
    # begin transaction
    # set fallback address to fail label
    begin fail

    # do computation
    load data, addr
    add data, data, 1
    store data, addr

    # end transaction
    end

fail:
    # retry if transaction failed
    goto retry
```

实际上，HTM 支持嵌套，也就是说可以在一次事务中途，再开另一个事务。但只有最外层的事务的 end 指令会提交事务，如果需要回滚事务，也会回滚到最外层事务，再跳转到最外层事务的 fallback 地址。

### 指令集架构支持

x86_64 指令集提供了 Transactional Synchronization Extensions (TSX) 扩展，它有两种使用方法：Hardware Lock Elision 和 Restricted Transactional Memory。它的文档在 Intel 64 and IA-32 Architectures Software Developer's Manual 的 Volume 1 Chapter 16 Programming with Intel Transaction Synchronization Extensions。

Hardware Lock Elision 的应用场景是，程序编写了 critical section，并且用锁来保护它，保证同时只有一个核心在执行这个 critical section。但锁会带来额外的开销。既然有了硬件内存事务，就可以先跳过加锁这一步，在事务里执行一次 critical section，在原来释放锁的地方结束事务。如果事务成功提交，说明没有其他核心要进入 critical section，那就省下了锁的开销；如果事务没有成功提交，就会回滚，再正常执行带锁的 critical section。

具体地，它在加锁的指令上添加一个 XACQUIRE 前缀，并在释放锁的指令上添加一个 XRELEASE 前缀。那么在支持 TSX 的硬件上，处理器就可以用硬件事务来尝试绕过锁。如果处理器不支持 TSX，就会忽略掉 XACQUIRE 和 XRELEASE 前缀，正常上锁、执行代码再释放锁。

Restricted Transactional Memory 就是完整的硬件内存事务支持：用 XBEGIN 指令开始事务，用 XEND 指令结束事务，用 XABORT 指令打断当前事务。

AArch64 从 ARMv9-A 开始，也引入了硬件内存事务支持：[Transactional Memory Extension (TME)](https://documentation-service.arm.com/static/62ff4dcbc3b04f2bd53e21d5?token=)。它引入了如下的新指令：

- TCANCEL imm: 对应 x86 的 XABORT，取消事务，从 TSTART 下一条指令开始继续执行，imm 会被写入到 TSTART 指令的目的寄存器
- TCOMMIT: 对应 x86 的 XEND
- TSTART Xd: 对应 x86 的 XBEGIN，如果事务成功开始，那么目的寄存器被写入 0；如果事务失败，那么目的寄存器会被写入为事务失败原因
- TTEST Xd: 把目前的事务嵌套层级写到目的寄存器

因此 TME 的预期使用方法是（例子来自 ARM DDI0617 C1.1 Conventions）：

```asm
loop
    tstart x12     # attempt to start a new transaction
    cbnz x12, loop # retry forever

    <code>

    tcommit
```

此外，TME 扩展也可以用来实现类似 x86 的 HLE 特性：Transactional Lock Elision。但是，与 x86 的实现方法不同，AArch64 的 TME 扩展还是需要用上述的 TSTART 等指令来实现 Transactional Lock Elision，下面是一个例子（来自 ARM DDI0617 C2.3 Acquiring a lock）：

获得锁：

```asm
loop:
    TSTART X5         # attempt to start a new transaction
    CBNZ X5, fallback # check if start succeeded

    # CHECK_ACQ(X1)
    # add the fallback lock to the transactional read set ; and set W5 to 0 if the fallback lock is free.
    LDAR W5, [X1]

    CBZ W5, enter     # if the fallback lock is free enter the critical region
    TCANCEL #0xFFFF   # otherwise cancel the transaction with RTRY set to 1

fallback:
    TBZ X5, #15, lock # if RTRY is 0 take the fallback lock
    SUB W6, W6, #1    # decrement the retry count
    CBZ W6, lock      # take the lock if 0

    # WAIT_ACQ(X1==0)
    # wait until the lock is free
loop_wait:
    LDAR W5, [X1]     # load acquire ensures it is ordered before subsequent loads/stores
    CBNZ W5, loop_wait

    B loop            # retry the transaction

lock:
    # LOCK(X1)
    # elision failed, acquire the fallback lock

    PRFM PSTL1KEEP, [X1] # preload into cache in unique state
loop_lock:
    LDAXR W5, [X1]       # read lock with acquire
    CBNZ W5, loop_lock   # check if 0
    STXR W5, W0, [X1]    # attempt to store new value
    CBNZ W5, loop_lock   # test if store succeeded and retry if not

    DMB ISH           # block loads/stores from the critical region

enter:
```

代码首先开始一次事务，如果发现锁没有被其他线程获得，那就直接跳转到 enter 进行 critical section 的执行；如果发现锁已经被其他线程获得，就取消事务，再次循环，如果循环多次还是失败，那就用传统的锁。

在 critical section 最后释放锁：

```asm
    # CHECK(X1)
    # set W5 to 0 if the fallback lock is free
    LDR W5, [Xx] ; read lock

    CBNZ W5, unlock   # check if 0
    TCOMMIT           # the lock was elided, exit the transaction
    B exit

unlock:
    # UNLOCK(X1)
    # elision failed, release the fallback lock exit:
    STLR WZR, [X1]    # clear the lock with release semantics

exit:
```

首先检查之前是采用的哪种方法“获得”了锁，如果是事务，那就提交事务；如果是传统的锁，那就释放掉锁。可以看到，相比 x86 的方案，ARM 的 TME 在实现 Lock Elision 时，指令上会比较冗余，但好处是微架构的实现会比较容易。

## 不同原子指令间的关系

不同原子指令之间，虽然语义不同，但是可以一定程度上互相实现。

用 LL/SC 实现 CAS：首先用 LL 读取旧值，和预期值进行比较，如果相等，则用 SC 写入新值，如果 SC 写入失败，则循环。

用 CAS 实现 AMO：首先读取旧值，用指令实现 AMO 要做的更新操作后，用 CAS 尝试写入，如果内存中的值等于旧值，就把更新后的新值写入，如果写入失败，则循环。

用 CAS 实现 LL/SC：不完美，可能有 ABA 问题。用正常的指令读取内存以代替 LL，记录下访问的内存地址和读取的值；在原来 SC 的地方，判断 SC 的地址是否和之前 LL 的相同，如果地址相同，则用 CAS 尝试写入，如果内存中的值等于之前读取的值，就写入 SC 要写入的值。

关于 LL/SC 和 CAS 在 Linux 中使用的讨论，推荐阅读：[cmpxchg ll/sc portability](https://yarchive.net/comp/linux/cmpxchg_ll_sc_portability.html)。

事实上，QEMU 为了性能，会用 CAS 实现 LL/SC。虽然它会有 ABA 问题，但实际上利用 LL/SC 来避免 ABA 问题的代码比较少。如果不这么做，就需要比较复杂的方法来实现精确的 LL/SC 模拟，这方面的论文也不少，例如：

- Kristien, Martin, et al. "Fast and correct load-link/store-conditional instruction handling in DBT systems." IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 39.11 (2020): 3544-3554.
- Z. Zhao, Z. Jiang, Y. Chen, X. Gong, W. Wang and P. -C. Yew, "Enhancing Atomic Instruction Emulation for Cross-ISA Dynamic Binary Translation," 2021 IEEE/ACM International Symposium on Code Generation and Optimization (CGO), Seoul, Korea (South), 2021, pp. 351-362, doi: 10.1109/CGO51591.2021.9370312.

但很遗憾的是，这些工作的性能都没有达到 CAS 模拟那么好，所以还是没有被 QEMU 采用。关于 QEMU 为什么要采用 CAS 来模拟 LL/SC 的讨论，可以见 [cmpxchg-based emulation of atomics](https://lists.gnu.org/archive/html/qemu-devel/2016-06/msg07754.html)。

## 编程语言支持

目前很多编程语言都内置了对原子指令的支持，例如：

- C: C11 引入了 stdatomic.h 头文件
- C++: C++11 引入了 atomic 头文件
- Rust：提供了 std::sync::atomic

根据指令集架构支持的原子指令类型，这些编程语言的原子操作会被翻译成对应的汇编代码。

## 其他原子指令


一些指令集架构还提供了其他类型的原子指令，例如：

- AArch64 提供了 64 字节粒度的原子读或写：LD64B 从内存原子读取连续 64 字节的数据到 8 个通用寄存器中；ST64B 把连续 8 个通用寄存器的值原子写入到内存中

## 不同指令集架构对原子指令支持的对比

| ISA       | LL/SC                  | CAS                           | AMO    | HTM |
|-----------|------------------------|-------------------------------|--------|-----|
| RISC-V    | A 扩展                 | Zacas 扩展，并且支持双倍宽度   | A 扩展 | 无  |
| LoongArch | 有，V1.1 支持了双倍宽度 | 需要 V1.1 版本，不支持双倍宽度 | 有     | 无  |
| x86_64    | 无                     | 有，并且支持双倍宽度           | 有     | TSX |
| AArch64   | 有                     | 有，并且支持双倍宽度           | 有     | TME |
| MIPS      | 有，也支持双倍宽度      | 有，并且支持双倍宽度           | 有     | 无  |
