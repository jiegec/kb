# Linux Kernel Memory Barriers

本文是对 [Linux Kernel Memory Barriers](https://www.kernel.org/doc/Documentation/memory-barriers.txt) 一文的总结。

## Abstract Memory Access Model

CPU 可以对 Load 和 Store 进行重排，但是有一些约束条件：

- 两个 load，如果后一个 load 的地址依赖前一个 load 的结果（`Q = LOAD P, D = LOAD *Q`），那么会按顺序执行（Alpha 除外，它允许 Split Cache）
- 地址重合的 load 和 store 会按顺序执行：`a = LOAD *X, STORE *X = b`
- 部分指令集架构会增加额外的限制，比如 x86 只允许 load 重排到 store 前面（Store Buffer）：`STORE *D = Z, X = LOAD *A` 实际的执行顺序可能是 `X = LOAD *A, STORE *D = Z`

## What are memory barriers?

Memory barrier 的类型：

- store barrier：barrier 之前的 store 会在 barrier 之后的 store 之前完成
- load barrier：barrier 之前的 load 会在 barrier 之后的 load 之前完成
- general barrier：barrier 之前的 load/store 会在 barrier 之后的 load/store 之前完成
- acquire: acquire 之后的 load/store 会在 acquire 之后完成，一般用于锁的 lock，保证对被保护的对象的访问在临界区内
- release: release 之前的 load/store 会在 release 之前完成，一般用于锁的 unlock，保证对被保护的对象的访问在临界区内

Control dependency：如果一个分支跳转与否，依赖某个 load 的结果，那么这个分支内的指令对这个 load 就有 Control dependency：

```cpp
q = READ_ONCE(a);
if (q) {
    p = READ_ONCE(b);
}
```

`READ_ONCE` 相当于 volatile read，避免编译器的优化。这里对 b 的读取和对 a 的读取有 Control dependency，但是它们依然可以重排。只有在分支内的写，因为有副作用，才不会被重排到 load 之前：

```cpp
q = READ_ONCE(a);
if (q) {
    WRITE_ONCE(b, 1);
}
```

但是 Control dependency 比较脆弱，容易因为编译器的优化把分支去掉，导致 dependency 失效，此时还是需要添加显式的 barrier。

## Explicit kernel barriers

内核提供了 Compiler barrier：`barrier()`，阻止编译器把 barrier 前的代码和 barrier 后的代码进行重排。定义如下：

```c
// in include/linux/compiler.h
# define barrier() __asm__ __volatile__("": : :"memory")
```

`READ_ONCE` 和 `WRITE_ONCE`：volatile read/write，阻止编译器优化。定义如下：

```c
// in include/asm-generic/rwonce.h
/*
 * Use __READ_ONCE() instead of READ_ONCE() if you do not require any
 * atomicity. Note that this may result in tears!
 */
#ifndef __READ_ONCE
#define __READ_ONCE(x)	(*(const volatile __unqual_scalar_typeof(x) *)&(x))
#endif

#define READ_ONCE(x)							\
({									\
	compiletime_assert_rwonce_type(x);				\
	__READ_ONCE(x);							\
})

#define __WRITE_ONCE(x, val)						\
do {									\
	*(volatile typeof(x) *)&(x) = (val);				\
} while (0)

#define WRITE_ONCE(x, val)						\
do {									\
	compiletime_assert_rwonce_type(x);				\
	__WRITE_ONCE(x, val);						\
} while (0)
```

特别地，在 Alpha 上，READ_ONCE 还会自带一个 barrier：

```c
// in arch/alpha/include/asm/rwonce.h
/*
 * Alpha is apparently daft enough to reorder address-dependent loads
 * on some CPU implementations. Knock some common sense into it with
 * a memory barrier in READ_ONCE().
 *
 * For the curious, more information about this unusual reordering is
 * available in chapter 15 of the "perfbook":
 *
 *  https://kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html
 *
 */
#define __READ_ONCE(x)							\
({									\
	__unqual_scalar_typeof(x) __x =					\
		(*(volatile typeof(__x) *)(&(x)));			\
	mb();								\
	(typeof(x))__x;							\
})
```

READ_ONCE/WRITE_ONCE 比较接近 C/C++ 的 atomic_load/atomic_store（指定 relaxed order）。
