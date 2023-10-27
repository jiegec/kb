# 原子指令

现在的处理器，一般会提供如下几种形式的原子指令：

1. LL(Load-Linked)/SC(Store-Conditional)
2. CAS(Compare And Swap)
3. AMO(Atomic Memory Operation)

它们在软件的使用方式和硬件实现上有所区别。

## LL/SC

### 定义

[LL/SC](https://en.wikipedia.org/wiki/Load-link/store-conditional) 是一对指令，其中 LL 指令从内存中读取数据到寄存器，SC 指令执行时，如果地址和 LL 指令相同，并且在 LL 指令后，被 LL 访问的内存（粒度可能更粗，例如一个缓存行）没有被修改，那么写入寄存器的值到同样的地址；否则就不写入。SC 指令的写入是否成功，会通过向目的寄存器写入不同的值来区分。也就是说，SC 如果写入成功，保证了 LL 到 SC 这段时间内，这段内存没有被改变。

### 常见用法

LL/SC 的通常用法是，实现一个读 - 改 - 写（read-modify-write）操作：首先用 LL 指令读取内存，然后对寄存器进行计算，再把结果用 SC 指令写入内存：如果中途内存结果被其他处理器核心修改了，那么用 LL 指令读取的结果就是错的，这次计算结果就不会被 SC 写进去；否则，说明 LL 指令读取的值是正确的，然后把更新后的结果写入到内存中。

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

代码利用 LL/SC 指令，把 a1 和 a0 指向的内存的值比较，如果相等，就把 a2 写到 a0 指向的内存，返回成功；如果不相等，则不修改内存的值，返回错误。

除了内存被其他处理器核心写入会导致 SC 失败以外，一些指令集架构允许程序手动让 SC 失败，以 LoongArch 为例，标准要求：

LL.{W/D} 执行时记录下访问地址并置上一个标记（LLbit 置为 1），SC.{W/D} 指令执行时会查看 LLbit，仅当 LLbit 为 1 时才真正产生写动作，否则不写。在配对的 LL-SC 执行期间，下列事件会让 LLbit 清 0:

- 执行了 ERTN 指令且执行时 CSR.LLBCTL 中的 KLO 位不等于 1;
- 其它处理器核或 Cache Coherent master 对该 LLbit 对应的地址所在的 Cache 行执行完成了一个 store 操作。

这样做的目的是，如果在 LL 和 SC 之间触发了上下文切换，操作系统可以把 SC 自动取消掉，详情可以看 LoongArch 的 CSR.LLBCTL 的定义。

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

对于返回内存中旧值的 CAS 指令，可以把 dest 和 old_data 进行比较来判断 CAS 是否成功。有的 CAS 指令既返回了 CAS 是否成功的信息，又返回了内存中的旧值。

这个过程看起来和 LL/SC 很像，但是有如下的不同：

1. LL/SC 需要两条原子指令，分别在开头的读和最后的写；CAS 只有一条原子指令，在最后实现写入
2. LL/SC 需要的操作数比较少：LL 是一个源操作数，也就是要读取的内存地址，一个目的操作数，用来保存读取的值；SC 是两个源操作数，包括要写入的内存地址和数据，一个目的操作数，用来保存 SC 是否成功的结果；CAS 需要的操作数比较多：三个源操作数，包括内存地址、比较数据和新数据，一个目的操作数，用来保存 CAS 是否成功或者内存旧值。
3. CAS 可能会遇到 ABA 问题：在 Read-Modify-CAS 过程中，如果内存中的值从 A 变成了 B，又从 B 变回了 A，CAS 依然会成功，因为它写入与否，仅取决于比较是否相等；而 LL/SC 会由硬件监测中途的内存访问，只要内存中的值被写入过，无论最后的值是否回到了 LL 读取的值，都会让 SC 失败

### ABA 问题

ABA 问题就是指的在 Read-Modify-Write 循环中，如果内存中的值从 A 变成了 B，又从 B 变成了 A，是否会影响写入是否成功的问题。LL/SC 的答案是，如果出现了 ABA 的情况，会使得写入失败；CAS 的答案是，ABA 情况下写入依然成功。

为什么要讨论 ABA 问题呢？这是因为一些无锁数据结构的实现，是不允许 ABA 情况的出现的。这个时候，就需要用 LL/SC，或者用下面要介绍的 DWCAS（Double Width Compare And Swap）指令，而不是 CAS 指令。

### DWCAS

DWCAS（Double Width Compare And Swap）指令其实也是 CAS 指令，只不过它的内存操作的粒度是处理器位数的两倍：例如 32 位处理器，DWCAS 的操作宽度就是 64 位；64 位处理器，DWCAS 的操作宽度就是 128 位。

引入 DWCAS 可以解决 ABA 的问题：既然问题出在值会从 A 到 B 再回到 A，那就让值不回到 A，不就好了？每次更新的时候，除了原本要更新的值，同时更新一个 counter，这个 counter 每次更新都加一。counter 溢出需要很多很多次 CAS，因此可以认为不会出现 ABA 的情况，这时候就解决了 ABA 问题。

但是，通常处理器都只会提供和处理器位数相同位数的内存指令，例如 32 位处理器提供 32 位 CAS，那要是需要更新的值已经占了 32 位，怎么同时更新 counter 呢？所以就不得不引入了 DWCAS，在 32 位处理器上提供 64 位 CAS，多的那 32 位就是拿来更新 counter 的。

但是 DWCAS 实现起来也会比较复杂：每个操作数的位宽都翻倍了，原来的一个通用寄存器放不下了，怎么办？一个朴素的办法是，传更多的操作数，两个操作数拼起来合成一个两倍位宽的值，但是这样在指令编码中，操作数占用的位数太多：

```asm
cas dest_hi, dest_lo, addr, old_data_hi, old_data_lo, new_data_hi, new_data_lo
```

一个解决方法是，一个操作数对应两个连续的通用寄存器，例如某个操作数是 2 号寄存器，代表的就是 2 号和 3 号寄存器拼接起来的两倍位宽的值。如果平台有更宽的向量寄存器，也可以把操作数放到向量寄存器上传入。但无论如何，单条指令涉及到的操作数和宽度都比较大，给处理器的设计带来了一定的挑战。

除了 DWCAS 以外，还有一种 CAS 变体：[DCAS（Double Compare and Swap）](https://en.wikipedia.org/wiki/Double_compare-and-swap)。和 DWCAS 不同的是，DCAS 实现的原子的两个 CAS 操作，这两个 CAS 可以操作不连续的内存。换句话说，DWCAS 可以认为是 DCAS 的一个特殊情况，特殊在于两个 CAS 操作的是连续的内存。


### 指令集架构支持

x86_64 指令集提供了 CAS 指令，并且提供了 DWCAS 两倍位宽版本：[cmpxchg16b 指令](https://www.felixcloutier.com/x86/cmpxchg8b:cmpxchg16b)，它把内存中的值和 RDX:RAX 比较，如果相等，就设置 ZF，并往内存写入 RCX:RBX；如果不相等，清空 ZF 并把内存中的值写入到 RDX:RAX。可以看到，这条指令采用的是多个源寄存器的方案：RDX、RAX、RCX、RBX 一共四个源 64 位通用寄存器，并且通过定死寄存器编号，解决了指令编码的问题。同时，一条指令也要写入两个通用寄存器 RDX 和 RAX，外加 FLAGS 寄存器的 ZF。

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

### 硬件实现

AMO 指令的硬件实现和 CAS 类似，也是把原子操作下放到缓存中去执行。但由于 AMO 指令需要涉及少量的更新操作，例如位操作和整数运算，因此缓存内部也需要引入一个 ALU 用于实现 AMO 指令的计算。

## 不同原子指令间的关系

不同原子指令之间，虽然语义不同，但是可以一定程度上互相实现。

用 LL/SC 实现 CAS：首先用 LL 读取旧值，和预期值进行比较，如果相等，则用 SC 写入新值，如果 SC 写入失败，则循环。

用 CAS 实现 AMO：首先读取旧值，用指令实现 AMO 要做的更新操作后，用 CAS 尝试写入，如果内存中的值等于旧值，就把更新后的新值写入，如果写入失败，则循环。

用 CAS 实现 LL/SC：不完美，可能有 ABA 问题。用正常的指令读取内存以代替 LL，记录下访问的内存地址和读取的值；在原来 SC 的地方，判断 SC 的地址是否和之前 LL 的相同，如果地址相同，则用 CAS 尝试写入，如果内存中的值等于之前读取的值，就写入 SC 要写入的值。

关于 LL/SC 和 CAS 在 Linux 中使用的讨论，推荐阅读：[cmpxchg ll/sc portability](https://yarchive.net/comp/linux/cmpxchg_ll_sc_portability.html)。

事实上，QEMU 为了性能，会用 CAS 实现 LL/SC。虽然它会有 ABA 问题，但实际上利用 LL/SC 来避免 ABA 问题的代码比较少。如果不这么做，就需要比较复杂的方法来实现精确的 LL/SC 模拟，这方面的论文也不少，例如：

- Kristien, Martin, et al. "Fast and correct load-link/store-conditional instruction handling in DBT systems." IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 39.11 (2020): 3544-3554.

但很遗憾的是，这些工作的性能都没有达到 CAS 模拟那么好，所以还是没有被 QEMU 采用。关于 QEMU 为什么要采用 CAS 来模拟 LL/SC 的讨论，可以见 [cmpxchg-based emulation of atomics](https://lists.gnu.org/archive/html/qemu-devel/2016-06/msg07754.html)。
