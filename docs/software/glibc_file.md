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
