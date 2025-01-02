# GCC Internals

本文是对 [GNU Compiler Collection Internals](https://gcc.gnu.org/onlinedocs/gccint.pdf) 文档的整理和总结。文章引用了部分 GCC 源码。

## RTL

### 查看 RTL

GCC 的 RTL 是采用 Lisp 语言描述的低层次的中间语言，是转换为机器指令前的最后一个表示。在生成汇编的时候，添加参数 `-dP` 就可以看到最后的 RTL 和汇编的对应关系：

```asm
#(insn 13 8 14 (set (reg/i:DI 10 a0)
#        (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
#                (reg:SI 11 a1 [78])))) "kb.c":3:1 21 {*mulsi3_extended}
#     (expr_list:REG_DEAD (reg:SI 11 a1 [78])
#        (nil)))
        mulw    a0,a0,a1        # 13    [c=20 l=4]  *mulsi3_extended
#(jump_insn 21 20 22 (simple_return) "kb.c":3:1 246 {simple_return}
#     (nil)
# -> simple_return)
        ret             # 21    [c=0 l=4]  simple_return

```

如果想要 dump 出每个 RTL pass 后的结果，可以添加参数：`-fdump-rtl-all`，可以看到形如下面的 RTL 代码：

```lisp
;; Function mul (mul, funcdef_no=0, decl_uid=1488, cgraph_uid=1, symbol_order=0)

(note 1 0 5 NOTE_INSN_DELETED)
(note 5 1 19 [bb 2] NOTE_INSN_BASIC_BLOCK)
(note 19 5 2 NOTE_INSN_PROLOGUE_END)
(note 2 19 3 NOTE_INSN_DELETED)
(note 3 2 4 NOTE_INSN_DELETED)
(note 4 3 7 NOTE_INSN_FUNCTION_BEG)
(note 7 4 8 NOTE_INSN_DELETED)
(note 8 7 13 NOTE_INSN_DELETED)
(insn 13 8 14 (set (reg/i:DI 10 a0)
        (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
                (reg:SI 11 a1 [78])))) "kb.c":3:1 21 {*mulsi3_extended}
     (expr_list:REG_DEAD (reg:SI 11 a1 [78])
        (nil)))
(insn 14 13 20 (use (reg/i:DI 10 a0)) "kb.c":3:1 -1
     (nil))
(note 20 14 21 NOTE_INSN_EPILOGUE_BEG)
(jump_insn 21 20 22 (simple_return) "kb.c":3:1 246 {simple_return}
     (nil)
 -> simple_return)
(barrier 22 21 18)
(note 18 22 0 NOTE_INSN_DELETED)
```

### 阅读 RTL

可以看到 RTL 是一系列的 S-exp，每个 S-exp 的前三个整数参数分别是 id，prev 和 next，表示一个双向链表。核心是要看 (insn) 的第四个参数，例如：

```lisp
(set (reg/i:DI 10 a0)
        (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
                (reg:SI 11 a1 [78]))))
```

表示这个指令的作用是，把 int32 类型的 a0 寄存器的值乘以 int32 类型的 a1 寄存器的值，结果符号扩展到 int64，写入到 a0 寄存器中。其中表示类型的是 [DI/SI](https://gcc.gnu.org/onlinedocs/gccint/Machine-Modes.html)，下面是一个简单的名字和位数的对应关系：

- 整数：B(Bit)I=1, Q(Quarter)I=8, H(Half)I=16, S(Single)I=32, D(Double)I=64, T(Tetra)I=128
- 浮点：Q(Quarter)F=8, H(Half)F=16, S(Single)F=32, D(Double)F=64, T(Tetra)F=128
- 十进制浮点：*D
- 定点数（_Fract）：*Q，无符号在开头加 U
- 累加器（_Accum）：*A，无符号在开头加 U
- 复数：*C

稍微和习惯不同的是 Q 表示 Quarter 而不是 Quad。

寄存器的表示方式是 `(reg:m n)`：

```lisp
(reg/i:DI 10 a0)
(reg:SI 10 a0 [77])
(reg:SI 11 a1 [78])
```

这里的 DI/SI 就是类型，10/11 是寄存器编号，后面的 a0/a1 是寄存器 10/11 在 RISC-V 架构里的 ABI 名称。`/i` 表示这个寄存器会保存函数的返回值（`REG_FUNCTION_VALUE_P(x)`）。

### 指令模板

同一行最后还有一个 `{*mulsi3_extended}`，这表示的是这一个 insn 对应了哪一个规则，这可以在 [riscv.md](https://github.com/gcc-mirror/gcc/blob/63663e4e69527b308687c63bacb0cc038b386593/gcc/config/riscv/riscv.md#L1048-L1056) 中找到：

```lisp
(define_insn "mulsi3_extended"
  [(set (match_operand:DI              0 "register_operand" "=r")
	(sign_extend:DI
	    (mult:SI (match_operand:SI 1 "register_operand" " r")
		     (match_operand:SI 2 "register_operand" " r"))))]
  "(TARGET_ZMMUL || TARGET_MUL) && TARGET_64BIT"
  "mulw\t%0,%1,%2"
  [(set_attr "type" "imul")
   (set_attr "mode" "SI")])
```

这表示一个模式匹配的规则，构成了从 RTL 到指令的映射关系。模式匹配的部分是：

```
  [(set (match_operand:DI              0 "register_operand" "=r")
	(sign_extend:DI
	    (mult:SI (match_operand:SI 1 "register_operand" " r")
		     (match_operand:SI 2 "register_operand" " r"))))]
```

意思是可以匹配两个操作数，这两个操作数应当是寄存器操作数（`register_operand`，`r` 表示通用寄存器），类型是 int32（`:SI`），操作数乘法后符号扩展到 int64（`:DI`），最后写入一个寄存器的目的操作数（`register_operand`，类型是 int64 `:DI`，保存在通用寄存器 `r`，`=` 表示写入，旧数据丢弃）。满足这些要求，就匹配上了 `mulsi3_extended`。

下一行：

```lisp
  "(TARGET_ZMMUL || TARGET_MUL) && TARGET_64BIT"
```

指的是额外的条件，用 C 代码编写。比如这里要用到 mulw 指令，但是如果当前的 target 不支持这个指令，那就不要生成 mulw 指令，所以这里就要制定限制条件：实现了乘法，并且是 64 位。

再下一行就是输出的指令：

```lisp
  "mulw\t%0,%1,%2"
```

这里的 `%0` `%1` `%2` 就会替换为前面匹配得到的操作数，注意前面 `match_operand` 后的整数，这就是对应的编号。可以看到这里和 GCC 内联汇编的语法特别相似，包括前面 `match_operand` 的最后一个参数：`=r` 和 ` r`，其实和内联汇编里对操作数的 specifier 也是非常像的。

```lisp
  [(set_attr "type" "imul")
   (set_attr "mode" "SI")])
```

最后是一些额外的属性，这个是用来给运算标记类型的，例如要针对处理器流水线进行优化，那就需要知道每个指令会被分到哪个流水线里面。

[完整的格式](https://gcc.gnu.org/onlinedocs/gccint/Patterns.html)如下：

```lisp
(define_insn
  [insn-pattern]
  "condition"
  "output-template"
  [insn-attribute])
```

忽略了可选的命名。

### 例子回顾

回顾一下开头的例子：

```asm
#(insn 13 8 14 (set (reg/i:DI 10 a0)
#        (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
#                (reg:SI 11 a1 [78])))) "kb.c":3:1 21 {*mulsi3_extended}
#     (expr_list:REG_DEAD (reg:SI 11 a1 [78])
#        (nil)))
        mulw    a0,a0,a1        # 13    [c=20 l=4]  *mulsi3_extended
```

这一个 insn 与 mulsi3_extended 相匹配，操作数 0 匹配到了 `(reg/i:DI 10 a0)`，操作数 1 匹配到了 `(reg:SI 10 a0 [77])`，操作数 2 匹配到了 `(reg:SI 11 a1 [78])`，所以最后生成指令的时候，把对应的寄存器名字填进去，就得到了 `mulw a0,a0,a1`。

有时候，比较复杂的指令会在 C 代码中生成，例如 `simple_return`：

```lisp
(define_insn "simple_return"
  [(simple_return)]
  ""
{
  return riscv_output_return ();
}
  [(set_attr "type"	"jump")
   (set_attr "mode"	"none")])
```

那么匹配以后，会调用 `riscv_output_return` 函数：

```c
const char *
riscv_output_return ()
{
  if (cfun->machine->naked_p)
    return "";

  return "ret";
}
```

实现也很简单，除了 naked 函数以外，都是一条 ret 指令。

### 原理探究

具体地，在 `riscv.md` 中写模式匹配的时候：

```lisp
  [(set (match_operand:DI              0 "register_operand" "=r")
	(sign_extend:DI
	    (mult:SI (match_operand:SI 1 "register_operand" " r")
		     (match_operand:SI 2 "register_operand" " r"))))]
```

会在 `gcc/insn-recog.cc` 生成如下的代码：

```c
// x1 = (set (reg/i:DI 10 a0)
//           (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
//                   (reg:SI 11 a1 [78]))))
static int
recog_7 (rtx x1 ATTRIBUTE_UNUSED,
	rtx_insn *insn ATTRIBUTE_UNUSED,
	int *pnum_clobbers ATTRIBUTE_UNUSED)
{
  rtx * const operands ATTRIBUTE_UNUSED = &recog_data.operand[0];
  rtx x2, x3, x4, x5, x6;
  int res ATTRIBUTE_UNUSED;
  // x2 = (reg/i:DI 10 a0)
  x2 = XEXP (x1, 0);
  // operands[0] = (reg/i:DI 10 a0)
  operands[0] = x2;
  // x3 = (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
  //                      (reg:SI 11 a1 [78])))
  x3 = XEXP (x1, 1);
  // x4 = (mult:SI (reg:SI 10 a0 [77])
  //               (reg:SI 11 a1 [78]))
  x4 = XEXP (x3, 0);
  switch (GET_CODE (x4))
    {
    case MULT:
      if (pattern14 (x3, E_SImode) != 0
          || !
#line 869 "/home/jiegec/ct-ng/.build/riscv64-unknown-linux-gnu/src/gcc/gcc/config/riscv/riscv.md"
(TARGET_MUL && TARGET_64BIT))
        return -1;
      return 21; /* *mulsi3_extended */
    }
}
```

```c
// x1 = (sign_extend:DI (mult:SI (reg:SI 10 a0 [77])
//                      (reg:SI 11 a1 [78])))
static int
pattern14 (rtx x1, machine_mode i1)
{
  rtx * const operands ATTRIBUTE_UNUSED = &recog_data.operand[0];
  rtx x2, x3, x4;
  int res ATTRIBUTE_UNUSED;
  // x2 = (mult:SI (reg:SI 10 a0 [77])
  //               (reg:SI 11 a1 [78]))
  // operands[0] = (reg/i:DI 10 a0)
  x2 = XEXP (x1, 0);
  if (GET_MODE (x2) != E_SImode
      || !register_operand (operands[0], E_DImode)
      || GET_MODE (x1) != E_DImode)
    return -1;
  // x3 = (reg:SI 10 a0 [77])
  x3 = XEXP (x2, 0);
  // operands[1] = (reg:SI 10 a0 [77])
  operands[1] = x3;
  if (!register_operand (operands[1], E_SImode))
    return -1;
  // x4 = (reg:SI 11 a1 [78])
  x4 = XEXP (x2, 1);
  // operands[2] = (reg:SI 11 a1 [78])
  operands[2] = x4;
  if (!register_operand (operands[2], i1))
    return -1;
  return 0;
}
```

代码中用注释标注了每一步匹配的内容，可见代码在匹配的同时，也把操作数保存了下来。

### 指令拆分

有些时候，RTL 层次上的指令可能对应多条实际的机器指令。例如在 32 位 target 上，拷贝一个 64 位整数，这意味着需要把一个 DI 类型的 move，拆成两个 SI 类型的 move，分别处理高位和低位。下面来看一个 rv32 的例子：

```lisp
;; 64-bit modes for which we provide move patterns.
(define_mode_iterator MOVE64 [DI DF])

(define_split
  [(set (match_operand:MOVE64 0 "nonimmediate_operand")
	(match_operand:MOVE64 1 "move_operand"))]
  "reload_completed
   && riscv_split_64bit_move_p (operands[0], operands[1])"
  [(const_int 0)]
{
  riscv_split_doubleword_move (operands[0], operands[1]);
  DONE;
})
```

可以看到，它会尝试匹配从一个 64 位整数（DI）或浮点数（DF）到另一个 64 位整数（DI）或浮点数（DF）的 set，也就是 move 操作。匹配上以后，判断条件：

```c
  "reload_completed
   && riscv_split_64bit_move_p (operands[0], operands[1])"
```

是否成立。这里 `reload_completed == true` 表示已经完成寄存器分配。

如果成立，就认为可以拆分 64 位的 move 为两个 32 位的 move，就生成下列 RTL：

```lisp
  [(const_int 0)]
```

但是实际上不会生成这个，而是调用后面的代码来生成新的 RTL 代码：

```c
{
  riscv_split_doubleword_move (operands[0], operands[1]);
  DONE;
})
```

完整的 [`define_split`](https://gcc.gnu.org/onlinedocs/gccint/Insn-Splitting.html) 定义如下：

```lisp
(define-split
  [insn-pattern]
  "condition"
  [new-insn-pattern-1
   new-insn-pattern-2
   ...]
  "preparation-statements")
```

忽略了可选的命名。

下面来看一个具体的例子，这一段是在 split 之前的 RTL 代码：

```lisp
(insn 6 3 13 (set (reg:DI 14 a4 [orig:72 _2 ] [72])
        (mem/c:DI (plus:SI (reg/f:SI 8 s0)
                (const_int -24 [0xffffffffffffffe8])) [1 a+0 S8 A64])) "kb.c":1:38 134 {*movdi_32bit}
     (nil))
```

它做的事情是，从内存地址 `$s0-24` 读取读取 8 个字节，写入到 a4 寄存器当中，由于 RV32 寄存器宽度只有 32 位，所以需要拆成两个读取：

```lisp
Splitting with gen_split_14 (riscv.md:1510)
deleting insn with uid = 6.
deleting insn with uid = 6.

(insn 30 3 31 (set (reg:SI 14 a4 [orig:72 _2 ] [72])
        (mem/c:SI (plus:SI (reg/f:SI 8 s0)
                (const_int -24 [0xffffffffffffffe8])) [1 a+0 S4 A64])) "kb.c":1:38 136 {*movsi_internal}
     (nil))
(insn 31 30 32 (set (reg:SI 15 a5 [ _2+4 ])
        (mem/c:SI (plus:SI (reg/f:SI 8 s0)
                (const_int -20 [0xffffffffffffffec])) [1 a+4 S4 A32])) "kb.c":1:38 136 {*movsi_internal}
     (nil))
```

可以看到，64 位的目的寄存器被拆成了两个 32 位寄存器，分别是 a4 和 a5；内存读取指令也拆分成了两个 SI 类型的读取，栈上的偏移也做了相应的调整。

有时候还可以见到 `define_insn_and_split`：

```lisp
(define_insn_and_split
  [insn-pattern]
  "condition"
  "output-template"
  "split-condition"
  [new-insn-pattern-1
   new-insn-pattern-2
   ...]
  "preparation-statements"
  [insn-attribute])
```

这实际上就是一个 `define_insn` 加一个 `define_split`，二者的 `insn-pattern` 一致：

```lisp
(define_insn
  [insn-pattern]
  "condition"
  "output-template"
  [insn-attribute])

(define_split
  [insn-pattern]
  "split-condition"
  [new-insn-pattern-1
   new-insn-pattern-2
   ...]
  "preparation-statements")
```

## 构建用于开发的 GCC

完整的 GCC 需要经过 bootstrap，但是为了开发，可以简化：

```shell
mkdir gcc-build
cd gcc-build
../gcc/configure --prefix=$PREFIX --enable-languages=c,c++ --disable-bootstrap CFLAGS="-g -O0" CXXFLAGS="-g -O0"
make -j8
make install -j8
```

交叉编译：给 configure 添加参数 `--target=loongarch64-unknown-linux-gnu`，但是有一些组件可能会因为缺少交叉编译环境而无法编译，可以只编译和安装 gcc：`make all-gcc && make install-gcc`。

交叉编译时，由于 libgcc 会依赖 libc，但构建 libc 又需要连接 libgcc，所以实际的构建顺序是这样的：

1. 构建 binutils
2. 构建一个不依赖 libc 的 gcc+libgcc，编译的时候设置：
    1. --without-headers：没有 C 头文件
    2. --disable-threads：没有 pthread
    3. --disable-shared：动态链接依赖 libc
3. 构建 libc，如果 libc 需要 linux 头文件，则还需要在 linux 源码中进行 headers_install
4. 再构建一个依赖 libc 的 gcc+libgcc

还有一种办法，是用 newlib 来做一个简单的空壳 libc 实现，这样可以直接一步到位。

## 调试 GCC

给 GCC 传递编译选项，可以让 GCC 打印中间结果，见 [GCC Developer Options](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html)：`-fdump-tree-all -fdump-rtl-all -dP`。想要更加详细的日志，可以用 `-fdump-tree-all-details` 甚至 `-fdump-tree-all-all`。

为了给 GCC 打断点，可以添加 `-v` 参数，找到实际的 `cc1` 命令行调用，再用调试器调试 cc1。GCC 提供了 gdbinit 配置：`gcc/gdbinit.in`。

## 测试 GCC

参考：[Installing GCC: Testing](https://gcc.gnu.org/install/test.html) [Working with the testsuite](https://dmalcolm.fedorapeople.org/gcc/newbies-guide/working-with-the-testsuite.html)

运行所有 gcc 测试：`make check-gcc`。针对测试类型进行过滤：

```shell
# test according to all files named execute.exp
make check-gcc RUNTESTFLAGS="execute.exp"
# test according to all files named execute.exp
# ./gcc/testsuite/g++.target/loongarch/loongarch.exp
# ./gcc/testsuite/gcc.target/loongarch/loongarch.exp
make check-gcc RUNTESTFLAGS="loongarch.exp"
```

进一步，限制到某个测例，例如要测试 `gcc.target/loongarch/cas-acquire.c`：

```shell
make check-gcc RUNTESTFLAGS="loongarch.exp='cas-acquire.c'"
```
