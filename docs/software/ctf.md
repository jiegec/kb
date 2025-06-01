# CTF

## general

### return oriented programming

利用 x86 的特性，可以找到一系列 gadget，几条简单的指令，其中最后一条指令是 ret。在栈溢出的时候，通过构造栈，把要执行的一系列的 gadget 的地址放在栈上，使得函数在返回了以后，会按照顺序执行各个 gadget。

### stack pivoting

如果栈溢出可以覆盖的部分比较少，无法放下完整的 return oriented programming 攻击，可以利用一个简单的 gadget，修改 rsp 到一个可控的可以放比较多数据的位置，再进行后续的攻击。

## glibc

### fake FILE

构建一个假的 `struct _IO_FILE_plus` 结构体，添加到 _IO_list_all 链表里，当 main 返回的时候，会 flush 它。通过构造特定的结构体内容，可以使得自定义的 `_IO_wdoallocbuf` 指针被调用，把它指向 system，第一个参数也可以被控制为 `/bin/sh` 字符串的指针，进而 get shell。

glibc 2.38+：[在 `_IO_cleanup` 中会调用 `_IO_flockfile` 获取锁](https://github.com/bminor/glibc/commit/af130d27099651e0d27b2cf2cfb44dafd6fe8a26)，所以 lock 字段也需要是合法的。

### malloc hook

把 `__malloc_hook` 指向 `system`，控制 size 参数为 `/bin/sh` 字符串的指针，从而实现 get shell。

glibc 2.34+：[移除了 __malloc_hook](https://github.com/bminor/glibc/commit/1e5a5866cb9541b5231dba3d86c8a1a35d516de9)，无法继续使用该办法。

### malloc got

覆盖 .got.plt 中 malloc@plt 的指针，指向 `system`，控制 size 参数为 `/bin/sh` 字符串的指针，从而实现 get shell。

要求可写的 `.got.plt`，即 `checksec` 报告 `No RELRO` 或 `Partial RELRO`。

### heap

glibc 2.32+：检查 chunk 的对齐，并且添加了 safe linking。

详见 [glibc 内存分配器](./glibc_allocator.md)。

## linux

### modprobe path

修改内核的 `modprobe_path` 内容，它指向 modprobe 路径，当内核遇到各种可能在尚未加载的内核模块中实现的功能时，会用 root 权限运行它去寻找合适的内核模块。把它指向攻击者控制的程序，然后用各种方法触发内核的自动 modprobe：

- 执行非法的可执行文件，Linux 6.14+ 删掉了这个功能：[exec: remove legacy custom binfmt modules autoloading](https://github.com/torvalds/linux/commit/fa1bdca98d74472dcdb79cb948b54f63b5886c04)
- 使用非常规的 socket 参数，例如 `socket(PF_MAX - 1, 0, 0)` 或 `socket(AF_INET, SOCK_STREAM, IPPROTO_MAX - 1)`

### override cred

`task_struct.cred` 字段记录了进程的权限（uid/gid 等），如果能覆盖 uid/gid 为 0，就得到了 root 权限。所以要做的是，找到当前进程的 cred 然后进行覆盖。方法：

- 在堆上寻找当前进程的名字（可以预先用 `prctl(PR_SET_NAME, name)` 设置），它保存在 `task_struct.comm` 字段，在它前面不远就是这个进程的 `task_struct.cred` 字段
- 在内核态运行 `commit_creds(prepare_kernel_cred(NULL))` 函数（在 Linux 6.2+，改为 `commit_creds(prepare_kernel_cred(&init_task))`，由于 [cred: Do not default to init_cred in prepare_kernel_cred()](https://github.com/torvalds/linux/commit/5a17f040fa332e71a45ca9ff02d6979d9176a423) 这一改动）

### return to user

在内核态进行 return oriented programming 比较困难，因此可以在用户态构造指令序列，然后在内核态下跳转到用户态地址上执行指令，首先利用内核态进行提权，然后用 `swapgs+iretq` 回到用户态，此时可以用 root 权限 get shell。这个方法会被如下的缓解措施阻止：

- Supervisor Mode Access Prevention：无法在内核态下读写用户态的地址
- Supervisor Mode Execute Prevention：无法在内核态下执行用户态的代码
- Kernel Page Table Isolation：Linux 的实现会让用户态的代码在内核态的页表中被标记为 Not Executable

