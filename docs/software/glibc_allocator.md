# glibc 内存分配器

## glibc 2.31

glibc 2.31 是 ubuntu 20.04 所使用的 libc 版本，首先来分析它的实现，源码可以从 [glibc-2.31 tag](https://github.com/bminor/glibc/tree/glibc-2.31) 中找到。

首先来看 malloc 函数，它实现在 `malloc/malloc.c` 的 [`__libc_malloc`](https://github.com/bminor/glibc/blob/glibc-2.31/malloc/malloc.c#L3022) 函数当中，忽略 `__malloc_hook` 和一些检查，首先可以看到它有一段代码，使用了一个叫做 tcache 的数据结构：

```c
/* int_free also calls request2size, be careful to not pad twice.  */
size_t tbytes;
if (!checked_request2size (bytes, &tbytes))
  {
    __set_errno (ENOMEM);
    return NULL;
  }
size_t tc_idx = csize2tidx (tbytes);

MAYBE_INIT_TCACHE ();

DIAG_PUSH_NEEDS_COMMENT;
if (tc_idx < mp_.tcache_bins
    && tcache
    && tcache->counts[tc_idx] > 0)
  {
    return tcache_get (tc_idx);
  }
DIAG_POP_NEEDS_COMMENT;
```

### tcache (Thread Local Cache)

接下来仔细地研究 tcache 的结构。首先，它是一个 per-thread 的数据结构，意味着每个线程都有自己的一份 tcache，不需要上锁就可以访问：

```c
static __thread tcache_perthread_struct *tcache = NULL;
```

接下来看它具体保存了什么：

```c
/* We overlay this structure on the user-data portion of a chunk when
   the chunk is stored in the per-thread cache.  */
typedef struct tcache_entry
{
  struct tcache_entry *next;
  /* This field exists to detect double frees.  */
  struct tcache_perthread_struct *key;
} tcache_entry;

/* There is one of these for each thread, which contains the
   per-thread cache (hence "tcache_perthread_struct").  Keeping
   overall size low is mildly important.  Note that COUNTS and ENTRIES
   are redundant (we could have just counted the linked list each
   time), this is for performance reasons.  */
typedef struct tcache_perthread_struct
{
  uint16_t counts[TCACHE_MAX_BINS];
  tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;

/* Caller must ensure that we know tc_idx is valid and there's room
   for more chunks.  */
static __always_inline void
tcache_put (mchunkptr chunk, size_t tc_idx)
{
  tcache_entry *e = (tcache_entry *) chunk2mem (chunk);

  /* Mark this chunk as "in the tcache" so the test in _int_free will
     detect a double free.  */
  e->key = tcache;

  e->next = tcache->entries[tc_idx];
  tcache->entries[tc_idx] = e;
  ++(tcache->counts[tc_idx]);
}

/* Caller must ensure that we know tc_idx is valid and there's
   available chunks to remove.  */
static __always_inline void *
tcache_get (size_t tc_idx)
{
  tcache_entry *e = tcache->entries[tc_idx];
  tcache->entries[tc_idx] = e->next;
  --(tcache->counts[tc_idx]);
  e->key = NULL;
  return (void *) e;
}
```

可以看到它有两个成员，把 tcache 分为 `TCACHE_MAX_BINS` 这么多个 bin，每个 bin 分别有一个：

1. `counts[bin]`：记录了这个 bin 中空闲块的数量，`tcache_put` 的时候加一，`tcache_get` 的时候减一
2. `entries[bin]`: 每个 bin 用一个链表保存了空闲块，链表的节点类型是 `tcache_entry`，那么 `entries[bin]` 保存了链表头的指针

bin 是内存分配器的一个常见做法，把要分配的块的大小分 bin，从而保证拿到的空闲块足够大。接下来看 `tcache_put` 是如何把空闲块放到 tcache 中的：

1. 把空闲块强制转换为 `tcache_entry` 结构体类型
2. 把它的 `key` 字段指向 tcache，用来表示这个空闲块当前在 `tcache` 当中，后续用它来检测 double free
3. 以新的 `tcache_entry` 作为链表头，插入到 tcache 的对应的 bin 当中：`entries[tc_idx]`
4. 更新这个 bin 的空闲块个数到 `count[tc_idx]` 当中

反过来，`tcache_get` 则是从 tcache 中拿出一个空闲块：

1. 从链表头 `entries[tc_idx]` 取出一个空闲块，把它从链表中删除：`entries[tc_idx] = e->next`
2. 更新这个 bin 的空闲块个数到 `count[tc_idx]` 当中
3. 把它的 `key` 字段指向 NULL，用来表示这个空闲块当前不在 `tcache` 当中
4. 返回这个空闲块的地址

#### malloc

接下来回到 `malloc` 的实现，它首先根据用户要分配的空间大小（`bytes`），计算出实际需要分配的大小（`tbytes`），和对应的 bin（`tc_idx`）：

```c
/* int_free also calls request2size, be careful to not pad twice.  */
size_t tbytes;
if (!checked_request2size (bytes, &tbytes))
  {
    __set_errno (ENOMEM);
    return NULL;
  }
size_t tc_idx = csize2tidx (tbytes);
```

其中 `checked_request2size` 实现如下：

```c
#define request2size(req)                                         \
  (((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)  ?             \
   MINSIZE :                                                      \
   ((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK)

/* Check if REQ overflows when padded and aligned and if the resulting value
   is less than PTRDIFF_T.  Returns TRUE and the requested size or MINSIZE in
   case the value is less than MINSIZE on SZ or false if any of the previous
   check fail.  */
static inline bool
checked_request2size (size_t req, size_t *sz) __nonnull (1)
{
  if (__glibc_unlikely (req > PTRDIFF_MAX))
    return false;
  *sz = request2size (req);
  return true;
}
```

它实现的实际上是把用户请求的内存大小，加上 `SIZE_SZ`（即 `sizeof(size_t)`），向上取整到 `MALLOC_ALIGN_MASK` 对应的 alignment（`MALLOC_ALIGNMENT`，通常是 `2 * SIZE_SZ`）的整数倍数，再和 `MINSIZE` 取 max。这里要加 `SIZE_SZ`，是因为 malloc 会维护被分配的块的一些信息，包括块的大小和一些 flag，后续会详细讨论，简单来说就是分配的实际空间会比用户请求的空间要更大。

接着，看它是如何计算出 tcache index 的：

```c
/* When "x" is from chunksize().  */
# define csize2tidx(x) (((x) - MINSIZE + MALLOC_ALIGNMENT - 1) / MALLOC_ALIGNMENT)
```

可以看到，从 MINSIZE 开始，以 MALLOC_ALIGNMENT 为单位，每个 bin 对应一个经过 align 以后的可能的内存块大小。得到 tcache index 后，检查对应的 bin 是否有空闲块，如果有，则直接分配：

```c
if (tc_idx < mp_.tcache_bins
    && tcache
    && tcache->counts[tc_idx] > 0)
  {
    return tcache_get (tc_idx);
  }
```

可以看到，tcache 相当于是一个 per thread 的小缓存，记录了最近释放的内存块，可供 malloc 使用。由于 bin 的数量有限，所以比较大的内存分配不会经过 tcache。

P.S. `calloc` 不会使用 tcache，而是用后面提到的 `_int_malloc` 进行各种分配。

#### free

既然 malloc 用到了 tcache，自然 free 就要往里面放空闲块了，相关的代码在 `_int_free` 函数当中：

```c
size_t tc_idx = csize2tidx (size);
if (tcache != NULL && tc_idx < mp_.tcache_bins)
  {
    /* Check to see if it's already in the tcache.  */
    tcache_entry *e = (tcache_entry *) chunk2mem (p);

    /* This test succeeds on double free.  However, we don't 100%
       trust it (it also matches random payload data at a 1 in
       2^<size_t> chance), so verify it's not an unlikely
       coincidence before aborting.  */
    if (__glibc_unlikely (e->key == tcache))
      {
        tcache_entry *tmp;
        LIBC_PROBE (memory_tcache_double_free, 2, e, tc_idx);
        for (tmp = tcache->entries[tc_idx];
             tmp;
             tmp = tmp->next)
          if (tmp == e)
            malloc_printerr ("free(): double free detected in tcache 2");
            /* If we get here, it was a coincidence.  We've wasted a
               few cycles, but don't abort.  */
      }

    if (tcache->counts[tc_idx] < mp_.tcache_count)
      {
        tcache_put (p, tc_idx);
        return;
      }
  }
```

它的逻辑也不复杂：

1. 计算 tcache index，找到对应的 bin
2. 检查它是不是已经被 free 过了，即 double free：free 过的指针，它的 key 字段应当指向 tcache，如果实际检测到是这样，那就去 tcache 里遍历链表，检查是不是真的在里面，如果是，说明 double free 了，报错
3. 如果对应的 bin 的链表长度不是很长（阈值是 `mp_.tcache_count`，取值见后），则添加到链表头部，完成 free 的过程

那么 tcache 默认情况下有多大呢：

```c
/* We want 64 entries.  This is an arbitrary limit, which tunables can reduce.  */
# define TCACHE_MAX_BINS  64
/* This is another arbitrary limit, which tunables can change.  Each
   tcache bin will hold at most this number of chunks.  */
# define TCACHE_FILL_COUNT 7
```

也就是说，它有 64 个 bin，每个 bin 的链表最多 7 个空闲块。

在 64 位下，这 64 个 bin 对应的块大小是从 32 字节到 1040 字节，每 16 字节一个 bin（`(1040 - 32) / 16 + 1 = 64`）。那么，`malloc(1032)` 或更小的分配会经过 tcache，而 `malloc(1033)` 或更大的分配则不会。

#### 实验

下面来写一段程序来观察 tcache 的行为，考虑到从链表头部插入和删除是后进先出（LIFO），相当于是一个栈，所以分配两个大小相同的块，释放后再分配相同大小的块，得到的指针的顺序应该是反过来的：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
  void *p1 = malloc(32);
  void *p2 = malloc(32);
  free(p1);
  free(p2);
  void *p3 = malloc(32);
  void *p4 = malloc(32);
  printf("p1=%p p2=%p p3=%p p4=%p\n", p1, p2, p3, p4);
}
```

输出如下：

```c
p1=0x55fb2f9732a0 p2=0x55fb2f9732d0 p3=0x55fb2f9732d0 p4=0x55fb2f9732a0
```

结果符合预期，tcache 的内部状态变化过程如下：

1. `free(p1)`：p1 变成链表的头部
2. `free(p2)`：p2 变成链表的头部，next 指针指向 p1
3. `p3 = malloc(32)`: p2 是链表的头部，所以被分配给 p3，之后 p1 成为链表的头部
3. `p4 = malloc(32)`: p1 是链表的头部，所以被分配给 p4

如果修改分配的大小，让它们被放到不同的 bin，就不会出现顺序颠倒的情况：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
  void *p1 = malloc(32);
  void *p2 = malloc(48);
  free(p1);
  free(p2);
  void *p3 = malloc(32);
  void *p4 = malloc(48);
  printf("p1=%p p2=%p p3=%p p4=%p\n", p1, p2, p3, p4);
}
```

输出如下：

```c
p1=0x5638e68db2a0 p2=0x5638e68db2d0 p3=0x5638e68db2a0 p4=0x5638e68db2d0
```

可以看到 p3 等于 p1，p4 等于 p2。此时 p1 和 p3 属于同一个 bin，而 p2 和 p4 属于另一个 bin。

既然我们知道了 tcache 的内部构造，我们可以写一个程序，首先得到 tcache 的地址，再打印出每次 malloc/free 之后的状态：

```c
// see also: https://github.com/shellphish/how2heap/blob/master/glibc_2.31/tcache_poisoning.c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TCACHE_MAX_BINS 64

typedef struct tcache_entry {
  struct tcache_entry *next;
  struct tcache_perthread_struct *key;
} tcache_entry;

typedef struct tcache_perthread_struct {
  uint16_t counts[TCACHE_MAX_BINS];
  tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;

void dump_tcache(tcache_perthread_struct *tcache) {
  for (int i = 0; i < TCACHE_MAX_BINS; i++) {
    if (tcache->counts[i]) {
      tcache_entry *p = tcache->entries[i];
      printf("tcache bin #%d: %p", i, p);
      p = p->next;
      while (p) {
        printf(" -> %p", p);
        p = p->next;
      }
      printf("\n");
    }
  }
}

int main() {
  // leak tcache address
  void *p0 = malloc(128);
  free(p0);
  tcache_entry *entry = p0;
  tcache_perthread_struct *tcache = entry->key;
  printf("tcache is at %p\n", tcache);
  // clear tcache
  p0 = malloc(128);

  void *p1 = malloc(32);
  void *p2 = malloc(32);
  free(p1);
  printf("after free(p1):\n");
  dump_tcache(tcache);
  free(p2);
  printf("after free(p2):\n");
  dump_tcache(tcache);
  void *p3 = malloc(32);
  printf("after malloc(p3):\n");
  dump_tcache(tcache);
  void *p4 = malloc(32);
  printf("after malloc(p4):\n");
  dump_tcache(tcache);
  printf("p1=%p p2=%p p3=%p p4=%p\n", p1, p2, p3, p4);
}
```

运行结果如下：

```c
tcache is at 0x558f39310010
after free(p1):
tcache bin #1: 0x558f39310740
after free(p2):
tcache bin #1: 0x558f39310770 -> 0x558f39310740
after malloc(p3):
tcache bin #1: 0x558f39310740
after malloc(p4):
p1=0x558f39310740 p2=0x558f39310770 p3=0x558f39310770 p4=0x558f39310740
```

打印出来的结果和预期一致。

接下来继续分析 malloc 的后续代码。

### 回到 `__libc_malloc`

如果 malloc 没有命中 tcache，或者 free 没有把空闲块放到 tcache 当中，会发生什么事情呢？接下来往后看，首先是 `__libc_malloc` 的后续实现：

```c
if (SINGLE_THREAD_P)
  {
    victim = _int_malloc (&main_arena, bytes);
    // omitted
    return victim;
  }

arena_get (ar_ptr, bytes);

victim = _int_malloc (ar_ptr, bytes);
```

这里出现了 arena 的概念：多线程情况下，为了提升性能，同时用多个 arena，每个 arena 用一把锁来保证多线程安全，从而使得多个线程可以同时从不同的 arena 中分配内存。这里先不讨论多线程的情况，先假设在单线程程序下，全局只用一个 arena：`main_arena`，然后从里面分配内存。接下来看 `_int_malloc` 的内部实现，可以看到它根据要分配的块的大小进入了不同的处理：

```c
// in _int_malloc
if ((unsigned long) (nb) <= (unsigned long) (get_max_fast ()))
  {
    // fast bin handling
  }

if (in_smallbin_range (nb))
  {
    // small bin handling
  }
else
  {
    // consolidate fast bins to unsorted bins
  }

for (;; )
  {
    // process unsorted bins
  }
```

malloc 把空闲的块分成四种类型来保存：

1. fast bin: 类似前面的 tcache bin，把大小相同的空闲块放到链表中，再维护多个对应不同大小的空闲块的链表头指针，采用单向链表维护
2. small bin：small bin 也会把相同的空闲块放在链表中，但相邻的空闲块会被合并为更大的空闲块，采用双向链表维护
3. large bin：large bin 可能保存不同大小的空闲块，采用双向链表维护
4. unsorted bin：近期被 free 的空闲块，如果没有保存到 tcache，会被放到 unsorted bin 当中，留待后续的处理

在讨论这些 bin 的维护方式之前，首先要知道 glibc 是怎么维护块的：空闲的时候是什么布局，被分配的时候又是什么布局？

### 块布局

glibc 每个空闲块（chunk）对应了下面的结构体 `malloc_chunk`：

```c
struct malloc_chunk {
  INTERNAL_SIZE_T      mchunk_prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */

  struct malloc_chunk* fd;         /* double links -- used only if free. */
  struct malloc_chunk* bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};
```

它的字段如下：

1. 相邻的前一个空闲块的大小 `mchunk_prev_size`，记录它是为了方便找到前一个空闲块的开头，这样合并相邻的空闲块就很简单
2. 当前空闲块的大小 `mchunk_size`，由于块的大小是对齐的，所以它的低位被用来记录 flag
3. `fd` 和 `bk`：small bin 和 large bin 需要用双向链表维护空闲块，指针就保存在这里
4. `fd_nextsize` 和 `bk_next_size`：large bin 需要用双向链表维护不同大小的空闲块，方便找到合适大小的空闲块

这是空闲块的内存布局，那么被分配的内存呢？被分配的内存，相当于是如下的结构：

```c
struct {
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */
  char payload[];                         /* malloc() returns pointer to payload */
};
```

也就是说，`malloc()` 返回的地址，等于空闲块里 `fd` 所在的位置。被分配的块，除了用户请求的空间以外，只有前面的 `sizeof(size_t)` 大小的空间是内存分配器带来的空间开销。块被释放以后，它被重新解释成 `malloc_chunk` 结构体（注意它们的起始地址不同，`malloc_chunk` 的地址是 malloc 返回的 `payload` 地址减去 `2 * sizeof(size_t)`，对应 `mchunk_prev_size` 和 `mchunk_size` 两个字段）。事实上，`mchunk_prev_size` 保存在用户请求的空间的最后几个字节。内存布局如下：

```
 in-use chunk         free chunk
+-------------+      +------------------+
| mchunk_size |      | mchunk_size      |
+-------------+      +------------------+
| payload     |      | fd               |
|             |      +------------------+
|             |      | bk               |
|             |      +------------------+
|             |      | fd_nextsize      |
|             | ---> +------------------+
|             |      | bk_nextsize      |
|             |      +------------------+
|             |      | unused           |
|             |      |                  |
|             |      |                  |
|             |      |                  |
|             |      +------------------+
|             |      | mchunk_prev_size |
+-------------+      +------------------+
```

因此为了在 payload 和 `malloc_chunk` 指针之间转换，代码中设计了两个宏来简化指针运算：

```c
/* conversion from malloc headers to user pointers, and back */

#define chunk2mem(p)   ((void*)((char*)(p) + 2*SIZE_SZ))
#define mem2chunk(mem) ((mchunkptr)((char*)(mem) - 2*SIZE_SZ))
```

知道了空闲块的维护方式，由于各个 bin 维护的就是这些空闲块，所以接下来分别看这几种 bin 的维护方式。

### fast bin

fast bin 的维护方式和 tcache 类似，它把不同大小的空闲块按照大小分成多个 bin，每个 bin 记录在一个单向链表当中，然后用一个数组记录各种 bin 大小的链表头，这里直接用的就是 `malloc_chunk` 指针数组：

```c
typedef struct malloc_chunk *mfastbinptr;
struct malloc_state
{
  /* other fields are omitted */
  /* Fastbins */
  mfastbinptr fastbinsY[NFASTBINS];
}
```

在 64 位下，默认 `NFASTBINS` 等于 10，计算方式如下：

1. 最大的由 fast bin 管理的块大小等于 `80 * sizeof(size_t) / 4 + sizeof(size_t)` 向上取整到 16 的倍数，在 64 位机器上等于 176 字节
2. 分配粒度从最小的 32 字节到最大的 176 字节，每 16 字节一个 bin，一共有 10 个 bin（`(176 - 32) / 16 + 1 = 10`）

不过默认情况下，fast bin 管理的块大小通过 `set_max_fast(DEFAULT_MXFAST)` 被限制在 `DEFAULT_MXFAST` 附近，这个值等于 `64 * sizeof(size_t) / 4`，加上 `sizeof(size_t)` 再向下取整到 16 的倍数，就是 128 字节。此时，只有前 7 个 bin 可以被用到（32 字节到 128 字节，每 16 字节一个 bin，`(128 - 32) / 16 + 1 = 7`），即 `malloc(120)` 或更小的分配会保存到 fast bin 中，`malloc(121)` 或更大的分配则不会。

#### malloc

分配的时候，和 tcache 类似，也是计算出 fastbin 的 index，然后去找对应的链表，如果链表非空，则从链表头取出空闲块用于分配：

```c
#define fastbin(ar_ptr, idx) ((ar_ptr)->fastbinsY[idx])

/* offset 2 to use otherwise unindexable first 2 bins */
#define fastbin_index(sz) \
  ((((unsigned int) (sz)) >> (SIZE_SZ == 8 ? 4 : 3)) - 2)

// in _int_malloc, allocate using fastbin
idx = fastbin_index (nb);
mfastbinptr *fb = &fastbin (av, idx);
mchunkptr pp;
victim = *fb;

if (victim != NULL)
  {
    if (SINGLE_THREAD_P)
      *fb = victim->fd;
    else
      REMOVE_FB (fb, pp, victim);
    if (__glibc_likely (victim != NULL))
      {
        size_t victim_idx = fastbin_index (chunksize (victim));
        if (__builtin_expect (victim_idx != idx, 0))
          malloc_printerr ("malloc(): memory corruption (fast)");
        check_remalloced_chunk (av, victim, nb);
#if USE_TCACHE
        /* While we're here, if we see other chunks of the same size,
          stash them in the tcache.  */
        size_t tc_idx = csize2tidx (nb);
        if (tcache && tc_idx < mp_.tcache_bins)
          {
            mchunkptr tc_victim;

            /* While bin not empty and tcache not full, copy chunks.  */
            while (tcache->counts[tc_idx] < mp_.tcache_count
                  && (tc_victim = *fb) != NULL)
              {
                if (SINGLE_THREAD_P)
                  *fb = tc_victim->fd;
                else
                  {
                    REMOVE_FB (fb, pp, tc_victim);
                    if (__glibc_unlikely (tc_victim == NULL))
                      break;
                  }
                tcache_put (tc_victim, tc_idx);
              }
          }
#endif
        void *p = chunk2mem (victim);
        alloc_perturb (p, bytes);
        return p;
      }
  }
```

它的过程如下：

1. 使用 `fastbin_index (nb)` 根据块的大小计算出 fast bin 的 index，然后 `fastbin (av, idx)` 对应 fast bin 的链表头指针
2. 如果链表非空，说明可以从 fast bin 分配空闲块，此时就把链表头的结点弹出：`*fb = victim->fd`（单线程）或 `REMOVE_FB (fb, pp, victim)`（多线程）；只用到了单向链表的 `fd` 指针，其余的字段没有用到
3. 进行一系列的安全检查：`__builtin_expect` 和 `check_remalloced_chunk`
4. 检查 tcache 对应的 bin，如果它还没有满，就把 fast bin 链表中的元素挪到 tcache 当中
5. 把 payload 地址通过 `chunk2mem` 计算出来，返回给 malloc 调用者
6. 调用 `alloc_perturb` 往新分配的空间内写入垃圾数据（可选），避免泄露之前的数据

可以看到，这个过程比较简单，和 tcache 类似，只不过它从 thread local 的 tcache 改成了支持多线程的版本，同时为了支持多线程访问，使用 CAS 原子指令来更新链表头部：

```c
#define REMOVE_FB(fb, victim, pp) \
  do                              \
    {                             \
      victim = pp;                \
      if (victim == NULL)         \
        break;                    \
    }                             \
  while ((pp = catomic_compare_and_exchange_val_acq (fb, victim->fd, victim)) != victim);
```

正因如此，这个分配过程才能做到比较快，所以这样的分配方法叫做 fast bin。

#### free

接下来分析一下 free 的时候，空闲块是如何进入 fast bin 的：

```c
// in _int_free, after tcache handling
if ((unsigned long)(size) <= (unsigned long)(get_max_fast ()))
  {
    /* check omitted */
    free_perturb (chunk2mem(p), size - 2 * SIZE_SZ);

    atomic_store_relaxed (&av->have_fastchunks, true);
    unsigned int idx = fastbin_index(size);
    fb = &fastbin (av, idx);

    /* Atomically link P to its fastbin: P->FD = *FB; *FB = P;  */
    mchunkptr old = *fb, old2;

    if (SINGLE_THREAD_P)
      {
        /* Check that the top of the bin is not the record we are going to
          add (i.e., double free).  */
        if (__builtin_expect (old == p, 0))
          malloc_printerr ("double free or corruption (fasttop)");
        p->fd = old;
        *fb = p;
      }
    else
      do
        {
          /* Check that the top of the bin is not the record we are going to
            add (i.e., double free).  */
          if (__builtin_expect (old == p, 0))
            malloc_printerr ("double free or corruption (fasttop)");
          p->fd = old2 = old;
        }
      while ((old = catomic_compare_and_exchange_val_rel (fb, p, old2))
              != old2);

    /* check omitted */
  }
```

可以看到，它的逻辑很简单：如果大小合适，就直接添加到 fast bin 的链表头里，没有 tcache 那样的长度限制，多线程场景下依然是用 CAS 来实现原子的链表插入。

相比 tcache，fast bin 的 double free 检查更加简陋：它只能防护连续两次 free 同一个块，只判断了要插入链表的块是否在链表头，而不会检查是否在链表中间。

#### 实验

接下来写一段代码来观察 fast bin 的更新过程：

1. 由于 fastbin 保存在 `main_arena` 中，所以我们需要找到 `main_arena` 的运行时地址
2. `main_arena` 不在符号表中，不能直接找到它的地址，此时可以请出 Ghidra 逆向 `__libc_malloc` 或者 `malloc_trim` 函数，结合代码找到它的地址是 `DAT_002ecb80`，它相对 image base 的 offset 是 `0x1ecb80`
3. 再找一个在符号表中的符号 `_IO_2_1_stdout_`，在 Ghidra 中找到它的地址是 `0x2ed6a0`，相对 image base 的 offset 是 `0x1ed6a0`
4. 根据以上信息，就可以在运行时找到 libc 的 image base 地址，从而推断 `main_arena` 的地址，进而找到所有的 fast bin
5. 下面写一段代码，观察空闲块进入 fast bin 的过程

```c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct malloc_chunk {
  size_t mchunk_prev_size; /* Size of previous chunk (if free).  */
  size_t mchunk_size;      /* Size in bytes, including overhead. */

  struct malloc_chunk *fd; /* double links -- used only if free. */
  struct malloc_chunk *bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk *fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk *bk_nextsize;
};

/* offset 2 to use otherwise unindexable first 2 bins */
#define fastbin_index(sz) ((((unsigned int)(sz)) >> (SIZE_SZ == 8 ? 4 : 3)) - 2)

#define INTERNAL_SIZE_T size_t

/* MALLOC_ALIGNMENT equals to 16 on 64-bit */
#define MALLOC_ALIGNMENT                                                       \
  (2 * SIZE_SZ < __alignof__(long double) ? __alignof__(long double)           \
                                          : 2 * SIZE_SZ)

/* The corresponding word size.  */
/* SIZE_SZ equals to 8 on 64-bit */
#define SIZE_SZ (sizeof(INTERNAL_SIZE_T))

/* The corresponding bit mask value.  */
/* MALLOC_ALIGN_MASK equals to 15 on 64-bit */
#define MALLOC_ALIGN_MASK (MALLOC_ALIGNMENT - 1)

/* The smallest possible chunk */
/* MIN_CHUNK_SIZE equals to 32 on 64-bit */
#define MIN_CHUNK_SIZE (offsetof(struct malloc_chunk, fd_nextsize))

/* The smallest size we can malloc is an aligned minimal chunk */
/* MINSIZE equals to 32 on 64-bit */
#define MINSIZE                                                                \
  (unsigned long)(((MIN_CHUNK_SIZE + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK))

/* equivalent to max(alignUp(req + SIZE_SZ, MALLOC_ALIGNMENT), MINSIZE) */
#define request2size(req)                                                      \
  (((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)                             \
       ? MINSIZE                                                               \
       : ((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK)

/* MAX_FAST_SIZE equals to 160 on 64-bit */
#define MAX_FAST_SIZE (80 * SIZE_SZ / 4)

/* NFASTBINS equals to 10 on 64-bit */
#define NFASTBINS (fastbin_index(request2size(MAX_FAST_SIZE)) + 1)

struct malloc_state {
  /* Serialize access.  */
  int mutex;
  /* Flags (formerly in max_fast).  */
  int flags;
  /* Set if the fastbin chunks contain recently inserted free blocks.  */
  /* Note this is a bool but not all targets support atomics on booleans.  */
  int have_fastchunks;
  /* Fastbins */
  struct malloc_chunk *fastbinsY[NFASTBINS];
};

void dump_fastbin() {
  void *libc_base = (char *)stdout - 0x1ed6a0; // offset of _IO_2_1_stdout_
  struct malloc_state *main_arena =
      libc_base +
      0x1ecb80; // offset of main_arena, found by decompiling malloc_trim
  for (int i = 0; i < NFASTBINS; i++) {
    if (main_arena->fastbinsY[i]) {
      struct malloc_chunk *p = main_arena->fastbinsY[i];
      printf("fastbin #%d: %p", i, p);
      p = p->fd;
      while (p) {
        printf(" -> %p", p);
        p = p->fd;
      }
      printf("\n");
    }
  }
}

int main() {
  // use 10 malloc + free, the first 7 blocks will be saved in tcache, the rest
  // ones will go to fastbin
  void *ptrs[10];
  printf("allocate 10 pointers:");
  for (int i = 0; i < 10; i++) {
    ptrs[i] = malloc(32);
    printf(" %p", ptrs[i]);
  }
  printf("\n");

  // now one ptr goes to fastbin
  for (int i = 0; i < 8; i++) {
    free(ptrs[i]);
  }

  printf("fastbins after 8 pointers freed:\n");
  dump_fastbin();

  // free the 9th one
  free(ptrs[8]);

  // two pointers in the fastbin
  printf("fastbins after 9 pointers freed:\n");
  dump_fastbin();

  // free the 10th one
  free(ptrs[9]);

  // three pointers in the fastbin
  printf("fastbins after 10 pointers freed:\n");
  dump_fastbin();
  return 0;
}
```

输出如下：

```c
allocate 10 pointers: 0x563bd918d6b0 0x563bd918d6e0 0x563bd918d710 0x563bd918d740 0x563bd918d770 0x563bd918d7a0 0x563bd918d7d0 0x563bd918d800 0x563bd918d830 0x563bd918d860
fastbins after 8 pointers freed:
fastbin #1: 0x563bd918d7f0
fastbins after 9 pointers freed:
fastbin #1: 0x563bd918d820 -> 0x563bd918d7f0
fastbins after 10 pointers freed:
fastbin #1: 0x563bd918d850 -> 0x563bd918d820 -> 0x563bd918d7f0
```

可以看到，代码先分配了十个块，再按顺序释放，那么前七个块会进入 tcache，剩下的三个块则进入了同一个 fast bin，并且后释放的会在链表的开头。注意 fast bin 链表里的地址打印的是 chunk 地址，而用 `malloc` 分配的地址指向的是 payload 部分，二者差了 16 字节，最终 fast bin 就是把十个块里最后三个块用链表串起来。

前面分析过，fast bin 对 double free 的检测比较弱，如果构造一种情况，让它无法被检测到，就会导致一个空闲块被插入 fast bin 两次，此后就会被分配两次：

```c
// see also: https://github.com/shellphish/how2heap/blob/master/glibc_2.31/fastbin_dup.c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct malloc_chunk {
  size_t mchunk_prev_size; /* Size of previous chunk (if free).  */
  size_t mchunk_size;      /* Size in bytes, including overhead. */

  struct malloc_chunk *fd; /* double links -- used only if free. */
  struct malloc_chunk *bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk *fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk *bk_nextsize;
};

/* offset 2 to use otherwise unindexable first 2 bins */
#define fastbin_index(sz) ((((unsigned int)(sz)) >> (SIZE_SZ == 8 ? 4 : 3)) - 2)

#define INTERNAL_SIZE_T size_t

#define MALLOC_ALIGNMENT                                                       \
  (2 * SIZE_SZ < __alignof__(long double) ? __alignof__(long double)           \
                                          : 2 * SIZE_SZ)

/* The corresponding word size.  */
#define SIZE_SZ (sizeof(INTERNAL_SIZE_T))

/* The corresponding bit mask value.  */
#define MALLOC_ALIGN_MASK (MALLOC_ALIGNMENT - 1)

/* The smallest possible chunk */
#define MIN_CHUNK_SIZE (offsetof(struct malloc_chunk, fd_nextsize))

/* The smallest size we can malloc is an aligned minimal chunk */
#define MINSIZE                                                                \
  (unsigned long)(((MIN_CHUNK_SIZE + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK))

#define request2size(req)                                                      \
  (((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)                             \
       ? MINSIZE                                                               \
       : ((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK)

#define MAX_FAST_SIZE (80 * SIZE_SZ / 4)

#define NFASTBINS (fastbin_index(request2size(MAX_FAST_SIZE)) + 1)

struct malloc_state {
  /* Serialize access.  */
  int mutex;
  /* Flags (formerly in max_fast).  */
  int flags;
  /* Set if the fastbin chunks contain recently inserted free blocks.  */
  /* Note this is a bool but not all targets support atomics on booleans.  */
  int have_fastchunks;
  /* Fastbins */
  struct malloc_chunk *fastbinsY[NFASTBINS];
};

void dump_fastbin() {
  void *libc_base = (char *)stdout - 0x1ed6a0; // offset of _IO_2_1_stdout_
  struct malloc_state *main_arena =
      libc_base +
      0x1ecb80; // offset of main_arena, found by decompiling malloc_trim
  for (int i = 0; i < NFASTBINS; i++) {
    if (main_arena->fastbinsY[i]) {
      struct malloc_chunk *p = main_arena->fastbinsY[i];
      struct malloc_chunk *init_p = p;
      printf("fastbin #%d: %p", i, p);
      p = p->fd;
      while (p) {
        printf(" -> %p", p);
        if (p == init_p) {
          printf(" (cycle detected)");
          break;
        }
        p = p->fd;
      }
      printf("\n");
    }
  }
}

int main() {
  // use 7 malloc + free to fill the tcache
  void *ptrs[7];
  printf("allocate 7 pointers:");
  for (int i = 0; i < 7; i++) {
    ptrs[i] = malloc(32);
    printf(" %p", ptrs[i]);
  }
  printf("\n");

  void *p1 = malloc(32);
  void *p2 = malloc(32);
  printf("allocate p1=%p p2=%p\n", p1, p2);

  for (int i = 0; i < 7; i++) {
    free(ptrs[i]);
  }

  // now p1 goes to fastbin
  free(p1);

  printf("fastbins after p1 freed:\n");
  dump_fastbin();

  // now p2 goes to fastbin
  free(p2);

  // two pointers in the fastbin
  printf("fastbins after p1 & p2 freed:\n");

  dump_fastbin();

  // free p1 again
  free(p1);

  // three pointers in the fastbin
  printf("fastbins after p1, p2 & p1 freed:\n");
  dump_fastbin();

  // allocate 7 pointers to clear tcache
  printf("allocate 7 pointers\n");
  for (int i = 0; i < 7; i++) {
    ptrs[i] = malloc(32);
  }

  p1 = malloc(32);
  p2 = malloc(32);
  void *p3 = malloc(32);
  printf("allocate p1=%p p2=%p p3=%p\n", p1, p2, p3);
  return 0;
}
```

由于 fast bin 的 double free 检查只检查链表头，所以按照 `p1, p2, p1` 的顺序释放，就不会被检查到，并且此时链表中出现了两次 `p1`，那么后续再分配内存时，就会把同一个地址分配了两次。上述代码的输出如下，符合预期：

```c
allocate 7 pointers: 0x5633121676b0 0x5633121676e0 0x563312167710 0x563312167740 0x563312167770 0x5633121677a0 0x5633121677d0
allocate p1=0x563312167800 p2=0x563312167830
fastbins after p1 freed:
fastbin #1: 0x5633121677f0
fastbins after p1 & p2 freed:
fastbin #1: 0x563312167820 -> 0x5633121677f0
fastbins after p1, p2 & p1 freed:
fastbin #1: 0x5633121677f0 -> 0x563312167820 -> 0x5633121677f0 (cycle detected)
allocate 7 pointers
allocate p1=0x563312167800 p2=0x563312167830 p3=0x563312167800
```

可见 double free 不一定能被检测到，并且可能带来危险的后果。

### small bin

分析完 fast bin，接下来来看 small bin。small bin 每个 bin 内空闲块的大小是相同的，并且也是以链表的方式组织，只不过用的是双向链表。

#### malloc

接下来观察 `_int_malloc` 是怎么使用 small bin 的。前面提到，`_int_malloc` 首先会尝试在 fast bin 中分配，如果分配失败，或者大小超出了 fast bin 的范围，接下来会尝试在 small bin 中分配：

```c
// in _int_malloc
if (in_smallbin_range (nb))
  {
    idx = smallbin_index (nb);
    bin = bin_at (av, idx);

    if ((victim = last (bin)) != bin)
      {
        bck = victim->bk;
        if (__glibc_unlikely (bck->fd != victim))
          malloc_printerr ("malloc(): smallbin double linked list corrupted");
        set_inuse_bit_at_offset (victim, nb);
        bin->bk = bck;
        bck->fd = bin;

        if (av != &main_arena)
          set_non_main_arena (victim);
        check_malloced_chunk (av, victim, nb);
#if USE_TCACHE
        /* While we're here, if we see other chunks of the same size,
           stash them in the tcache.  */
        size_t tc_idx = csize2tidx (nb);
        if (tcache && tc_idx < mp_.tcache_bins)
          {
            mchunkptr tc_victim;

            /* While bin not empty and tcache not full, copy chunks over.  */
            while (tcache->counts[tc_idx] < mp_.tcache_count
                   && (tc_victim = last (bin)) != bin)
              {
                if (tc_victim != 0)
                  {
                    bck = tc_victim->bk;
                    set_inuse_bit_at_offset (tc_victim, nb);
                    if (av != &main_arena)
                      set_non_main_arena (tc_victim);
                    bin->bk = bck;
                    bck->fd = bin;

                    tcache_put (tc_victim, tc_idx);
                  }
              }
          }
#endif
        void *p = chunk2mem (victim);
        alloc_perturb (p, bytes);
        return p;
      }
  }
```

它的过程如下：

1. 使用 `in_smallbin_range (nb)` 检查块的大小是否应该放到 small bin 当中
2. 使用 `smallbin_index (nb)` 根据块的大小计算出 small bin 的 index，然后 `bin_at (av, idx)` 对应 small bin 的链表尾部的哨兵，这个双向链表有且只有一个哨兵，这个哨兵就放在 small bin 数组当中
3. 找到哨兵结点的前驱结点 `last (bin)`，如果链表为空，那么哨兵的前驱结点就是它自己；如果链表非空，那么哨兵的前驱结点就是链表里的最后一个结点，把它赋值给 `victim`
4. 把这个空闲块标记为正在使用：`set_inuse_bit_at_offset (victim, nb)`
5. 把 `victim` 从链表里删除：`bck = victim->bk; bin->bk = bck; bck->fd = bin;`，典型的双向链表的结点删除过程，维护 `victim` 前驱结点的后继指针，维护哨兵 `bin` 的前驱指针
6. 进行一系列的安全检查：`check_malloced_chunk`
7. 检查 tcache 对应的 bin，如果它还没有满，就把 small bin 链表中的元素挪到 tcache 当中
8. 把 payload 地址通过 `chunk2mem` 计算出来，返回给 malloc 调用者
9. 调用 `alloc_perturb` 往新分配的空间内写入垃圾数据（可选），避免泄露之前的数据

其实现过程和 fast bin 很类似，只不过把单向链表改成了双向，并且引入了哨兵结点，这个哨兵结点保存在 `malloc_state` 结构的 bins 数组当中：

```c
#define NSMALLBINS         64
/* SMALLBIN_WIDTH equals to 16 on 64-bit */
#define SMALLBIN_WIDTH    MALLOC_ALIGNMENT
/* SMALLBIN_CORRECTION equals to 0 on 64-bit */
#define SMALLBIN_CORRECTION (MALLOC_ALIGNMENT > 2 * SIZE_SZ)

/* MIN_LARGE_SIZE equals to 1024 on 64-bit */
#define MIN_LARGE_SIZE    ((NSMALLBINS - SMALLBIN_CORRECTION) * SMALLBIN_WIDTH)

/* equivalent to (sz < 1024) on 64-bit */
#define in_smallbin_range(sz)  \
  ((unsigned long) (sz) < (unsigned long) MIN_LARGE_SIZE)

/* equivalent to (sz >> 4) on 64-bit */
#define smallbin_index(sz) \
  ((SMALLBIN_WIDTH == 16 ? (((unsigned) (sz)) >> 4) : (((unsigned) (sz)) >> 3))\
   + SMALLBIN_CORRECTION)

typedef struct malloc_chunk* mchunkptr;

/* addressing -- note that bin_at(0) does not exist */
#define bin_at(m, i) \
  (mbinptr) (((char *) &((m)->bins[((i) - 1) * 2]))			      \
             - offsetof (struct malloc_chunk, fd))
      
#define NBINS             128
struct malloc_state
{
  /* omitted */
  /* Normal bins packed as described above */
  mchunkptr bins[NBINS * 2 - 2];
}
```

乍一看会觉得很奇怪，这里 `NBINS * 2 - 2` 是什么意思？`mchunkptr` 是个指针类型，那它指向的数据存在哪？其实这里用了一个小的 trick：

1. 不去看 bins 元素的类型，只考虑它的元素的大小，每个元素大小是 `sizeof(size_t)`，一共有 `NBINS * 2 - 2` 个元素
2. 而每个 bin 对应一个链表的哨兵结点，由于是双向链表，哨兵结点也没有数据，只需要保存前驱和后继两个指针，即每个 bin 只需要存两个指针的空间，也就是 `2 * sizeof(size_t)`
3. 正好 `bins` 数组给每个 bin 留出了 `2 * sizeof(size_t)` 的空间（bin 0 除外，这个 bin 不存在），所以实际上这些哨兵结点的前驱和后继指针就保存在 `bins` 数组里，按顺序保存，首先是 bin 1 的前驱，然后是 bin 1 的后继，接着是 bin 2 的前驱，依此类推
4. 虽然空间对上了，但是为了方便使用，代码里用 `bin_at` 宏来计算出一个 `malloc_chunk` 结构体的指针，而已知 bins 数组只保存了 `fd` 和 `bk` 两个指针，并且 bin 的下标从 1 开始，所以 bin i 的 `fd` 指针地址就是 `(char *) &((m)->bins[((i) - 1) * 2])`，再减去 `malloc_chunk` 结构体中 `fd` 成员的偏移，就得到了一个 `malloc_chunk` 结构体的指针，当然了，这个结构体只有 `fd` 和 `bk` 两个字段是合法的，其他字段如果访问了，就会访问到其他 bin 那里去

抛开这些 trick，其实就等价于用一个数组保存了每个 bin 的 `fd` 和 `bk` 指针，至于为什么要强行转换成 `malloc_chunk` 类型的指针，可能是为了方便代码的编写，不需要区分空闲块的结点和哨兵结点。

此外，small bin 的处理里还多了一次 `set_inuse_bit_at_offset (victim, nb)`，它的定义如下：

```c
#define set_inuse_bit_at_offset(p, s)					      \
  (((mchunkptr) (((char *) (p)) + (s)))->mchunk_size |= PREV_INUSE)
```

乍一看会觉得很奇怪，这个访问不是越界了吗？其实这个就是跨过当前的 chunk，访问相邻的下一个 chunk，在它的 `mchunk_size` 字段上打标记，表示它的前一个 chunk 已经被占用。前面提到过，`mchunk_size` 同时保存了 chunk 的大小和一些 flag，由于 chunk 的大小至少是 8 字节对齐的（32 位系统上），所以最低的 3 位就被拿来保存如下的 flag：

1. `PREV_INUSE(0x1)`: 前一个 chunk 已经被分配
2. `IS_MAPPED(0x2)`：当前 chunk 的内存来自于 mmap
3. `NON_MAIN_ARENA(0x4)`：当前 chunk 来自于 main arena 以外的其他 arena

在这里，就是设置了 `PREV_INUSE` flag，方便后续的相邻块的合并。

可以注意到，small bin 的分配范围是 `nb < MIN_LARGE_SIZE`，因此在 64 位上，`malloc(1000)` 或更小的分配会被 small bin 分配，而 `malloc(1001)` 或更大的分配则不可以。

#### free

在讲述 small bin 在 free 中的实现之前，先讨论 `_int_malloc` 的后续逻辑，最后再回过头来看 free 的部分。

### consolidate

当要分配的块经过 fast bin 和 small bin 两段逻辑都没能分配成功，并且要分配的块比较大的时候（`!in_small_range (nb)`），会进行一次 `malloc_consolidate` 调用，这个函数会尝试对 fast bin 中的空闲块进行合并，然后把新的块插入到 unsorted bin 当中。它的实现如下：

```c
unsorted_bin = unsorted_chunks(av);
maxfb = &fastbin (av, NFASTBINS - 1);
fb = &fastbin (av, 0);
do {
  p = atomic_exchange_acq (fb, NULL);
  if (p != 0) {
    do {
      /* malloc check omitted */

      check_inuse_chunk(av, p);
      nextp = p->fd;

      /* Slightly streamlined version of consolidation code in free() */
      size = chunksize (p);
      nextchunk = chunk_at_offset(p, size);
      nextsize = chunksize(nextchunk);

      if (!prev_inuse(p)) {
        prevsize = prev_size (p);
        size += prevsize;
        p = chunk_at_offset(p, -((long) prevsize));
        /* malloc check omitted */
        unlink_chunk (av, p);
      }

      if (nextchunk != av->top) {
        nextinuse = inuse_bit_at_offset(nextchunk, nextsize);

        if (!nextinuse) {
          size += nextsize;
          unlink_chunk (av, nextchunk);
        } else
          clear_inuse_bit_at_offset(nextchunk, 0);

        first_unsorted = unsorted_bin->fd;
        unsorted_bin->fd = p;
        first_unsorted->bk = p;

        if (!in_smallbin_range (size)) {
          p->fd_nextsize = NULL;
          p->bk_nextsize = NULL;
        }

        set_head(p, size | PREV_INUSE);
        p->bk = unsorted_bin;
        p->fd = first_unsorted;
        set_foot(p, size);
      }

      else {
        size += nextsize;
        set_head(p, size | PREV_INUSE);
        av->top = p;
      }

    } while ( (p = nextp) != 0);

  }
} while (fb++ != maxfb);
```

1. 第一层循环，遍历每个非空的 fast bin，进行下列操作
2. 第二层循环，每个非空的 fast bin 有一个单向链表，沿着链表进行迭代，遍历链表上的每个空闲块，进行下列操作
3. 循环内部，检查当前空闲块能否和前后的空闲块合并
4. 首先检查在它前面（地址更低的）相邻的块是否空闲：如果 `PREV_INUSE` 没有被设置，可以通过 `mchunk_prev_size` 找到前面相邻的块的开头，然后把两个块合并起来；如果前面相邻的块已经在某个双向链表当中（例如 small bin），把它从双向链表中删除：`unlink_chunk (av, p);`；为什么前面要用双向链表，也是为了在这里可以直接从链表中间删除一个结点
5. 接着检查在它后面（地址更高的）相邻的块是否空闲：根据自己的 size，计算出下一个块的地址，得到下一个块的大小，再读取下一个块的下一个块，根据它的 `PREV_INUSE`，判断下一个块是否空闲；如果空闲，那就把下一个块也合并进来，同理也要把它从双向链表中删除：`unlink_chunk (av, nextchunk);`；代码中还有对 top chunk 的特殊处理，这里先略过
6. 合并完成以后，把当前的空闲块放到 unsorted bin 当中，也是一个简单的双向链表向链表头的插入算法：`first_unsorted = unsorted_bin->fd; unsorted_bin->fd = p; first_unsorted->bk = p; p->bk = unsorted_bin; p->fd = first_unsorted;`

`unlink_chunk` 的实现就是经典的双向链表删除结点的算法：

```c
/* Take a chunk off a bin list.  */
static void
unlink_chunk (mstate av, mchunkptr p)
{
  /* malloc check omitted */

  mchunkptr fd = p->fd;
  mchunkptr bk = p->bk;

  /* malloc check omitted */

  fd->bk = bk;
  bk->fd = fd;
  if (!in_smallbin_range (chunksize_nomask (p)) && p->fd_nextsize != NULL)
    {
      /* malloc check omitted */

      if (fd->fd_nextsize == NULL)
        {
          if (p->fd_nextsize == p)
            fd->fd_nextsize = fd->bk_nextsize = fd;
          else
            {
              fd->fd_nextsize = p->fd_nextsize;
              fd->bk_nextsize = p->bk_nextsize;
              p->fd_nextsize->bk_nextsize = fd;
              p->bk_nextsize->fd_nextsize = fd;
            }
        }
      else
        {
          p->fd_nextsize->bk_nextsize = p->bk_nextsize;
          p->bk_nextsize->fd_nextsize = p->fd_nextsize;
        }
    }
}
```

这里的 `fd_nextsize` 和 `bk_nextsize` 字段适用于 large bin，后面会讨论这个双向链表的细节。

因此 unsorted bin 保存了一些从 fast bin 合并而来的一些块，由于 unsorted bin 只有一个，所以它里面会保存各种大小的空闲块。实际上，unsorted bin 占用的就是 `malloc_state` 结构中的 bin 1，因为我们已经知道，块的大小至少是 32，而大小为 32 的块，对应的 small bin index 是 2，说明 1 没有被用到，其实就是留给 unsorted bin 用的。在 64 位系统下，`malloc_state` 的 127 个 bin 分配如下：

1. bin 1 是 unsorted bin
2. bin 2 到 bin 63 是 small bin
3. bin 64 到 bin 126 是 large bin

bin 127 没有用到。

经过这次合并之后，接下来 `_int_malloc` 尝试从 unsorted bin 和 large bin 中分配空闲块。

### 再次回到 `__libc_malloc`

接下来，`_int_malloc` 有一大段代码来进行后续的内存分配，大概步骤包括：

1. 把 unsorted bin 中的空闲块的处理，放到 small bin 或者 large bin 中，同时如果有合适的块，就分配给 malloc 的调用者
2. 如果还是没有找到合适大小的块，就在 large bin 里寻找空闲块来分配；如果找不到合适大小的块，进行 consolidate，尝试更多的合并，得到更大的块；重复这个过程多次
3. 如果还是找不到合适的块，就从堆顶分配新的块，如果堆已经满了，还需要去扩大堆，或者直接用 mmap 分配一片内存

现在分步骤观察这个过程，首先观察 unsorted bin 的处理。

### unsorted bin

首先是 unsorted bin 的空闲块的处理：

```c
int iters = 0;
while ((victim = unsorted_chunks (av)->bk) != unsorted_chunks (av))
  {
    bck = victim->bk;
    size = chunksize (victim);
    mchunkptr next = chunk_at_offset (victim, size);

    /* malloc checks omitted */

    /*
       If a small request, try to use last remainder if it is the
       only chunk in unsorted bin.  This helps promote locality for
       runs of consecutive small requests. This is the only
       exception to best-fit, and applies only when there is
       no exact fit for a small chunk.
     */

    if (in_smallbin_range (nb) &&
        bck == unsorted_chunks (av) &&
        victim == av->last_remainder &&
        (unsigned long) (size) > (unsigned long) (nb + MINSIZE))
      {
        /* split and reattach remainder */
        remainder_size = size - nb;
        remainder = chunk_at_offset (victim, nb);
        unsorted_chunks (av)->bk = unsorted_chunks (av)->fd = remainder;
        av->last_remainder = remainder;
        remainder->bk = remainder->fd = unsorted_chunks (av);
        if (!in_smallbin_range (remainder_size))
          {
            remainder->fd_nextsize = NULL;
            remainder->bk_nextsize = NULL;
          }

        set_head (victim, nb | PREV_INUSE |
                  (av != &main_arena ? NON_MAIN_ARENA : 0));
        set_head (remainder, remainder_size | PREV_INUSE);
        set_foot (remainder, remainder_size);

        check_malloced_chunk (av, victim, nb);
        void *p = chunk2mem (victim);
        alloc_perturb (p, bytes);
        return p;
      }

    /* remove from unsorted list */
    /* malloc checks omitted */
    unsorted_chunks (av)->bk = bck;
    bck->fd = unsorted_chunks (av);

    /* Take now instead of binning if exact fit */

    if (size == nb)
      {
        set_inuse_bit_at_offset (victim, size);
        if (av != &main_arena)
          set_non_main_arena (victim);
#if USE_TCACHE
        /* Fill cache first, return to user only if cache fills.
           We may return one of these chunks later.  */
        if (tcache_nb
            && tcache->counts[tc_idx] < mp_.tcache_count)
          {
            tcache_put (victim, tc_idx);
            return_cached = 1;
            continue;
          }
        else
          {
#endif
        check_malloced_chunk (av, victim, nb);
        void *p = chunk2mem (victim);
        alloc_perturb (p, bytes);
        return p;
#if USE_TCACHE
          }
#endif
      }

    /* place chunk in bin */

    if (in_smallbin_range (size))
      {
        victim_index = smallbin_index (size);
        bck = bin_at (av, victim_index);
        fwd = bck->fd;
      }
    else
      {
        victim_index = largebin_index (size);
        bck = bin_at (av, victim_index);
        fwd = bck->fd;

        /* maintain large bins in sorted order */
        if (fwd != bck)
          {
            /* Or with inuse bit to speed comparisons */
            size |= PREV_INUSE;
            /* if smaller than smallest, bypass loop below */
            assert (chunk_main_arena (bck->bk));
            if ((unsigned long) (size)
                < (unsigned long) chunksize_nomask (bck->bk))
              {
                fwd = bck;
                bck = bck->bk;

                victim->fd_nextsize = fwd->fd;
                victim->bk_nextsize = fwd->fd->bk_nextsize;
                fwd->fd->bk_nextsize = victim->bk_nextsize->fd_nextsize = victim;
              }
            else
              {
                assert (chunk_main_arena (fwd));
                while ((unsigned long) size < chunksize_nomask (fwd))
                  {
                    fwd = fwd->fd_nextsize;
                    assert (chunk_main_arena (fwd));
                  }

                if ((unsigned long) size
                    == (unsigned long) chunksize_nomask (fwd))
                  /* Always insert in the second position.  */
                  fwd = fwd->fd;
                else
                  {
                    victim->fd_nextsize = fwd;
                    victim->bk_nextsize = fwd->bk_nextsize;
                    /* malloc checks omitted */
                    fwd->bk_nextsize = victim;
                    victim->bk_nextsize->fd_nextsize = victim;
                  }
                bck = fwd->bk;
                /* malloc checks omitted */
              }
          }
        else
          victim->fd_nextsize = victim->bk_nextsize = victim;
      }

    mark_bin (av, victim_index);
    victim->bk = bck;
    victim->fd = fwd;
    fwd->bk = victim;
    bck->fd = victim;

#if USE_TCACHE
    /* If we've processed as many chunks as we're allowed while
       filling the cache, return one of the cached ones.  */
    ++tcache_unsorted_count;
    if (return_cached
        && mp_.tcache_unsorted_limit > 0
        && tcache_unsorted_count > mp_.tcache_unsorted_limit)
      {
        return tcache_get (tc_idx);
      }
#endif

#define MAX_ITERS       10000
    if (++iters >= MAX_ITERS)
      break;
  }
```

它的流程如下：

1. 遍历 unsorted bin 双向链表，从哨兵结点开始，从后往前遍历空闲块
2. fast path 逻辑：如果要申请的块比当前空闲块小，并且当前空闲块可以拆分，那就拆分当前的空闲块，然后直接分配拆分后的空闲块
3. 如果要申请的块的大小和当前空闲块的大小相同，把空闲块放到 tcache，或者直接分配这个空闲块
4. 把当前空闲块根据大小，分发到 small bin 或者 large bin
5. 如果 tcache 中有合适的空闲块，就分配它

由此可见，unsorted bin 中的空闲块在 malloc 的时候会被分派到对应的 small bin 或者 large bin 当中。small bin 的处理比较简单，因为每个 bin 的块大小都相同，直接加入到双向链表即可。large bin 的处理则比较复杂，下面主要来分析 large bin 的结构。

### large bin

large bin 和其他 bin 的不同的地方在于，它每个 bin 的大小不是一个固定的值，而是一个范围。在 64 位下，bin 64 到 bin 127 对应的块大小范围：

1. bin 64 到 bin 96: 从 1024 字节开始，每个 bin 覆盖 64 字节的长度范围，例如 bin 64 对应 1024-1087 字节范围，bin 96 对应 3072-3135 字节范围
2. bin 97 到 bin 111: 从 3136 字节开始，每个 bin 覆盖 512 字节的长度范围，例如 bin 97 对应 3136-3583 字节范围（没有涵盖 512 字节是因为对齐问题，其他的都是涵盖 512 字节），bin 111 对应 10240-10751 字节范围
3. bin 112 到 bin 119: 从 10752 字节开始，每个 bin 覆盖 4096 字节的长度范围，例如 bin 112 对应 10752-12287 字节范围（没有涵盖 4096 字节是因为对齐问题，其他的都是涵盖 4096 字节），bin 119 对应 36864-40959 字节范围
4. bin 120 到 bin 123: 从 40960 字节开始，每个 bin 覆盖 32768 字节的长度范围，例如 bin 120 对应 40960-65535 字节范围（没有涵盖 32768 字节是因为对齐问题，其他的都是涵盖 32768 字节），bin 123 对应 131072-163839 字节范围
5. bin 124: 163840-262143 共 98304 个字节的范围
6. bin 125: 262144-524287 共 262144 个字节的范围
7. bin 126: 524288 或更长

可以看到，比较短的长度范围给的 bin 也比较多，后面则更加稀疏。上述各个 bin 的大小范围可以通过以下代码打印：

```c
#include <stdio.h>
#define largebin_index_64(sz)                                                  \
  (((((unsigned long)(sz)) >> 6) <= 48)                                        \
       ? 48 + (((unsigned long)(sz)) >> 6)                                     \
       : ((((unsigned long)(sz)) >> 9) <= 20)                                  \
             ? 91 + (((unsigned long)(sz)) >> 9)                               \
             : ((((unsigned long)(sz)) >> 12) <= 10)                           \
                   ? 110 + (((unsigned long)(sz)) >> 12)                       \
                   : ((((unsigned long)(sz)) >> 15) <= 4)                      \
                         ? 119 + (((unsigned long)(sz)) >> 15)                 \
                         : ((((unsigned long)(sz)) >> 18) <= 2)                \
                               ? 124 + (((unsigned long)(sz)) >> 18)           \
                               : 126)

int main() {
  int last_bin = largebin_index_64(1024);
  int last_i = 1024;
  for (int i = 1024; i < 1000000; i++) {
    if (largebin_index_64(i) != last_bin) {
      printf("%d-%d: %d, length %d\n", last_i, i - 1, last_bin, i - last_i);
      last_i = i;
      last_bin = largebin_index_64(i);
    }
  }
  printf("%d-inf: %d\n", last_i, last_bin);
  return 0;
}
```

因此 large bin 里面会有不同 chunk 大小的空闲块。为了快速地寻找想要的大小的空闲块，large bin 中空闲块按照从大到小的顺序组成链表，同时通过 `fd_nextsize` 和 `bk_nextsize` 把每种大小出现的第一个块组成双向链表。大致的连接方式如下，参考了 [Malloc Internals](https://sourceware.org/glibc/wiki/MallocInternals) 给的示例：

```
  bins[id]      chunk A              chunk B              chunk C
+----------+  +-----------------+  +-----------------+  +-----------------+
| fd = A   |  | size = 1072     |  | size = 1072     |  | size = 1040     |
+----------+  +-----------------+  +-----------------+  +-----------------+
| bk = C   |  | fd = B          |  | fd = C          |  | fd = bins[id]   |
+----------+  +-----------------+  +-----------------+  +-----------------+
              | bk = bins[id]   |  | bk = A          |  | bk = B          |
              +-----------------+  +-----------------+  +-----------------+
              | fd_nextsize = C |                       | fd_nextsize = A |
              +-----------------+                       +-----------------+
              | bk_nextsize = C |                       | bk_nextsize = A |
              +-----------------+                       +-----------------+
```

即所有的空闲块加哨兵组成一个双向链表，从大到小按照 `A -> B -> C` 的顺序连接；然后每种大小的第一个块 `A` 和 `C` 单独在一个 nextsize 链表当中。

因此在插入 large bin 的时候，分如下几种情况：

第一种情况，如果新插入的空闲块的大小比目前已有空闲块都小，则直接插入到空闲块和 nextsize 链表的尾部。例如要插入一个 `size = 1024` 的空闲块 D，插入后状态为：

```
  bins[id]      chunk A              chunk B              chunk C              chunk D          
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| fd = A   |  | size = 1072     |  | size = 1072     |  | size = 1040     |  | size = 1024     |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| bk = D   |  | fd = B          |  | fd = C          |  | fd = D          |  | fd = bins[id]   |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | bk = bins[id]   |  | bk = A          |  | bk = B          |  | bk = C          |
              +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | fd_nextsize = C |                       | fd_nextsize = D |  | fd_nextsize = A |
              +-----------------+                       +-----------------+  +-----------------+
              | bk_nextsize = D |                       | bk_nextsize = A |  | bk_nextsize = C |
              +-----------------+                       +-----------------+  +-----------------+
```

第二种情况，在遍历 nextsize 链表过程中，发现已经有大小相同的块，那就把新的块插入到它的后面。例如要插入一个 `size = 1072` 的空闲块 D，通过遍历 nextsize 链表找到了 A，插入之后的状态为：

```
  bins[id]      chunk A              chunk D              chunk B              chunk C          
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| fd = A   |  | size = 1072     |  | size = 1072     |  | size = 1072     |  | size = 1040     |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| bk = C   |  | fd = D          |  | fd = B          |  | fd = C          |  | fd = bins[id]   |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | bk = bins[id]   |  | bk = A          |  | bk = D          |  | bk = C          |
              +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | fd_nextsize = C |                                            | fd_nextsize = A |
              +-----------------+                                            +-----------------+
              | bk_nextsize = C |                                            | bk_nextsize = A |
              +-----------------+                                            +-----------------+
```

第三种情况，在遍历 nextsize 链表过程中，没有大小相同的块，那就按照从大到小的顺序插入到合适的位置。例如要插入一个 `size = 1056` 的空闲块 D，通过遍历 nextsize 链表找到了 A 和 C，插入之后的状态为：

```
  bins[id]      chunk A              chunk B              chunk D              chunk C          
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| fd = A   |  | size = 1072     |  | size = 1072     |  | size = 1056     |  | size = 1040     |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
| bk = D   |  | fd = B          |  | fd = D          |  | fd = C          |  | fd = bins[id]   |
+----------+  +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | bk = bins[id]   |  | bk = A          |  | bk = B          |  | bk = D          |
              +-----------------+  +-----------------+  +-----------------+  +-----------------+
              | fd_nextsize = D |                       | fd_nextsize = C |  | fd_nextsize = A |
              +-----------------+                       +-----------------+  +-----------------+
              | bk_nextsize = C |                       | bk_nextsize = A |  | bk_nextsize = D |
              +-----------------+                       +-----------------+  +-----------------+
```

这样就保证了插入以后的 large bin，依然满足从大到小排序，并且每种大小的第一个块组成 nextsize 链表的性质。

## 参考

- [Malloc Internals](https://sourceware.org/glibc/wiki/MallocInternals)
