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

### tcache

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
2. 把它的 `key` 字段指向 tcache，用来表示这个空闲块当前在 `tcache` 当中
3. 以新的 `tcache_entry` 作为链表头，插入到 tcache 的对应的 bin 当中：`entries[tc_idx]`
4. 更新这个 bin 的空闲块个数到 `count[tc_idx]` 当中

反过来，`tcache_get` 则是从 tcache 中拿出一个空闲块：

1. 从链表头 `entries[tc_idx]` 取出一个空闲块，把它从链表中删除：`entries[tc_idx] = e->next`
2. 更新这个 bin 的空闲块个数到 `count[tc_idx]` 当中
3. 把它的 `key` 字段指向 NULL，用来表示这个空闲块当前不在 `tcache` 当中
4. 返回这个空闲块的地址

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

它实现的实际上是把用户请求的内存大小，加上 `SIZE_SZ`（即 `sizeof(size_t)`），向上取整到 `MALLOC_ALIGN_MASK` 对应的 alignment（`MALLOC_ALIGNMENT`，通常是 `2 * SIZE_SZ`）的整数倍数，再和 `MINSIZE` 取 max。接着，看它是如何计算出 tcache index 的：

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

可以看到，tcache 相当于是一个 per thread 的小缓存，记录了最近释放的内存块，可供 malloc 使用。由于 bin 的数量有限，所以比较大的内存分配不会经过 tcache。既然 malloc 用到了 tcache，自然 free 就要往里面放空闲块了，相关的代码在 `_int_free` 函数当中：

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
# define TCACHE_MAX_BINS		64
/* This is another arbitrary limit, which tunables can change.  Each
   tcache bin will hold at most this number of chunks.  */
# define TCACHE_FILL_COUNT 7
```

也就是说，它有 64 个 bin，每个 bin 的链表最多 7 个空闲块。

下面来写一段程序来观察 tcache 的行为，考虑到从链表头部插入和删除是先进后出（LIFO），相当于是一个栈，所以分配两个大小相同的块，释放后再分配相同大小的块，得到的指针应该是顺序是反过来的：

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

