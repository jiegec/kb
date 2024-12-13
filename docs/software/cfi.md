# 控制流完整性 Control Flow Integrity

## 目的地址检查

一类常见的 CFI 机制是检查间接分支（call/jmp reg）的目的地址，是否落到预期的位置上，比如函数的开头。这个机制主要防止的是 ROP gadget，即从现有指令的中间某个位置开始执行一段代码，从而实现攻击者想要的效果。引入目的地址检查后，不再能从间接分支跳转到任意位置开始执行一段代码。这个预期的位置，一般是用指令来标识的。

[Intel CET(Control-flow Enforcement Technology)](https://www.intel.com/content/www/us/en/developer/articles/technical/technical-look-control-flow-enforcement-technology.html) 包括 IBT(Indirect Branch Tracking) 机制，要求 call/jmp 指令跳转到 endbr32/endbr64 指令。编译时，可以用 `-fcf-protection` 来启用 IBT。可以用 `readelf -n $BINARY` 来查看它是否启用了 IBT：`Properties: x86 feature: IBT, SHSTK`。

[ARM BTI(Branch Target Identification)](https://developer.arm.com/documentation/109576/0100/Branch-Target-Identification) 实现了这种机制。它的做法是，通过页表给页打上 Guarded Page 标记，被保护的页内 BTI 机制生效，此时间接分支的目的地址必须是一条 BTI 类的指令，否则就会触发异常。在不支持 BTI 的处理器上，BTI 会被当成 NOP 指令，因为 BTI 定义在了原来的 NOP 指令空间中。编译时，可以用 `-mbranch-protection=bti` 来启用 BTI，或者进一步用 `-mbranch-protection=standard` 来同时使用 BTI 和 PAC 两个保护机制。可以用 `readelf -n $BINARY` 来查看它是否启用了这些保护机制：`Properties: AArch64 feature: BTI, PAC`。

[RISC-V Zicfilp](https://github.com/riscv/riscv-isa-manual/blob/main/src/unpriv-cfi.adoc) 扩展的实现方法很类似，也是在间接分支的预期目的地址上放一条 LPAD 指令，如果间接分支没跳到 LPAD 上，触发异常。LPAD 也是复用了已有的 NOP 指令空间（AUIPC 的 rd=x0），所以在没有实现这个扩展的处理器上会被当成 NOP 指令。

## 影子栈

另一类常见的 CFI 检查针对的是 call/ret 指令，通常情况下，ret 会返回到对应的 call 的下一条指令的地址，但攻击者会希望通过控制返回地址来挟持控制流。为了避免控制流挟持，于是就有了影子栈（Shadow Stack），它以栈的形式存储 call stack 信息，除了 call 会 push，ret 会 pop 以外，它的内容要用特定的指令去修改，从而避免了攻击者篡改返回地址，进而在 ret 时，通过 Shadow Stack 检查 ret 指令是否跳转到了正确的位置。

[Intel CET(Control-flow Enforcement Technology)](https://www.intel.com/content/www/us/en/developer/articles/technical/technical-look-control-flow-enforcement-technology.html) 除了 IBT 以外，还有 SHSTK(shadow stack) 机制。它对现有指令的修改以及引入的新指令包括：

1. call 指令除了现有的把返回地址 push 到内存里 rsp 指向的栈上，还会把返回地址 push 到 shadow stack 上
2. ret 指令除了从内存里 rsp 指向的栈上 pop 返回地址，还会从 shadow stack 上 pop 返回地址，如果两个返回地址不同，则抛出异常
3. shadow stack 实际上也保存在内存里，但是和 rsp 指向的栈放在不同的地方：shadow stack 所在的页会通过页表打上 shadow stack 的标记，使得这个页不允许通过 mov 指令写入，只能用 call 指令或特定的指令来修改页内的返回地址
4. 增加一个寄存器：shadow stack pointer(SSP)，它不是通用寄存器，功能类似于 rsp，指向 shadow stack 的栈顶
5. 为了支持上下文切换，新增 saveprevssp 和 rstorssp 指令，供内核使用
6. 针对一些特殊的程序，它的 call/ret 可能不配对，此时可以用 incssp 来手动增加 ssp，等价于 pop 了若干个元素

编译时，可以用 `-fcf-protection` 来启用 SHSTK。可以用 `readelf -n $BINARY` 来查看它是否启用了 IBT：`Properties: x86 feature: IBT, SHSTK`。

ARM GCS(Guarded Control Stack) 也是类似的技术，用一个单独的栈来保存调用栈。编译时，可以用 `-mbranch-protection=gcs` 来启用 GCS。

[RISC-V Zicfiss](https://github.com/riscv/riscv-isa-manual/blob/main/src/unpriv-cfi.adoc) 扩展也是类似的技术。

## 地址签名和验证

此外还有一种防止攻击的技术，就是对地址进行签名和验证。它的思想是，攻击者想要挟持控制流，那就需要把正常的地址覆盖掉，变成攻击者控制的地址。如果处理器能够区分正常的地址和攻击者构造的地址，那就实现了防护。地址签名和验证就是这样的技术，它使用签名和验证算法，使用处理器内部的密钥，对正常地址进行签名，签名会放在地址高位上：由于目前虚拟地址空间没有用完，所以高位地址可以用来存储签名的信息。那么使用地址的时候，会去验证这个地址是否是合法的，由硬件生成的。攻击者不知道处理器内部的密钥，想要篡改地址时，无法给出正确的签名，于是无法通过检验。

ARM PAC(Pointer Authentication Code) 就是这样的技术。编译时，可以用 `-mbranch-protection=pac-ret` 来启用 PAC，或者进一步用 `-mbranch-protection=standard` 来同时使用 BTI 和 PAC 两个保护机制。可以用 `readelf -n $BINARY` 来查看它是否启用了这些保护机制：`Properties: AArch64 feature: BTI, PAC`。

除了签名和认证以外，还有一个很类似的技术，但它主要不是用于安全，而是用于检测内存访问溢出：Memory Tagging。它也是在地址高位添加一些信息，去标识这个指针应该范围的内存范围，但是这个信息没有密码学的保护，允许篡改。这个技术主要是用来加速 Address Sanitizer 一类的技术，给地址和内存上色，只有颜色相同的情况下才允许访问。不过由于颜色数量有限，它是可能漏掉一些错误的访问的。在没有 Memory Tagging 之前，Address Sanitizer 为了检查每次访存是否越界，开销会比较大。编译时，用 `-fsanitize=address` 启用 Address Sanitizer，用 `-fsanitize=hwaddress` 启用基于上述硬件加速的 Hardware Address Sanitizer。

无论是 PAC 还是 Memory Tagging，都需要硬件在访存时，忽略地址的高位，这个特性一般叫 Top Byte Ignore 或者 Linear Address Masking。这些多出来的位数，可以归软件来自由发挥，也可以启用 PAC 或 Memory Tagging 来让硬件参与使用。
