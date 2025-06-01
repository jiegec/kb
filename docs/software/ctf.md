# CTF

## Fake FILE

构建一个假的 `struct _IO_FILE_plus` 结构体，添加到 _IO_list_all 链表里，当 main 返回的时候，会 flush 它。通过构造特定的结构体内容，可以使得自定义的 `_IO_wdoallocbuf` 指针被调用，把它指向 system，第一个参数也可以被控制为 `/bin/sh` 字符串的指针，进而 get shell。

glibc 2.38+：[在 `_IO_cleanup` 中会调用 `_IO_flockfile` 获取锁](https://github.com/bminor/glibc/commit/af130d27099651e0d27b2cf2cfb44dafd6fe8a26)，所以 lock 字段也需要是合法的。

## malloc hook

把 `__malloc_hook` 指向 `system`，控制 size 参数为 `/bin/sh` 字符串的指针，从而实现 get shell。

glibc 2.34+：[移除了 __malloc_hook](https://github.com/bminor/glibc/commit/1e5a5866cb9541b5231dba3d86c8a1a35d516de9)，无法继续使用该办法。

## malloc got

覆盖 .got.plt 中 malloc@plt 的指针，指向 `system`，控制 size 参数为 `/bin/sh` 字符串的指针，从而实现 get shell。

要求可写的 `.got.plt`，即 `checksec` 报告 `No RELRO` 或 `Partial RELRO`。

## glibc heap

glibc 2.32+：检查 chunk 的对齐，并且添加了 safe linking。

详见 [glibc 内存分配器](./glibc_allocator.md)。
