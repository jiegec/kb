# GCC Internals

本文是对 [GNU Compiler Collection Internals](https://gcc.gnu.org/onlinedocs/gccint.pdf) 文档的整理和总结。

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

表示这个指令的作用是，把 int32 类型的 a0 寄存器的值乘以 int32 类型的 a1 寄存器的值，结果符号扩展到 int64，写入到 a0 寄存器中。其中表示类型的是 DI/SI，下面是一个简单的名字和位数的对应关系：

- 整数：B(Bit)I=1, Q(Quarter)I=8, H(Half)I=16, S(Single)I=32, D(Double)I=64, T(Tetra)I=128
- 浮点：Q(Quarter)F=8, H(Half)F=16, S(Single)F=32, D(Double)F=64, T(Tetra)F=128
- 十进制浮点：*D
- 有理数：*Q
- 复数：*C

稍微和习惯不同的是 Q 表示 Quarter 而不是 Quad。

寄存器的表示方式是 `(reg:m n)`：

```lisp
(reg/i:DI 10 a0)
(reg:SI 10 a0 [77])
(reg:SI 11 a1 [78])
```

这里的 DI/SI 就是类型，10/11 是寄存器编号，后面的 a0/a1 是寄存器 10/11 在 RISC-V 架构里的 ABI 名称。`/i` 表示这个寄存器会保存函数的返回值（`REG_FUNCTION_VALUE_P(x)`）。

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

意思是可以匹配两个操作数，这两个操作数应当是寄存器操作数（`register_operand`），类型是 int32（`:SI`），操作数乘法后符号扩展到 int64（`:DI`），最后写入一个寄存器的目的操作数（`register_operand`，`:DI`）。满足这些要求，就匹配上了 `mulsi3_extended`。

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
