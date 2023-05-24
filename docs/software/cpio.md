# cpio 文件格式

cpio 文件有多种不同的格式，其中被 POSIX 标准化的是 odc 格式。

## odc

cpio 的 odc 文件格式比较简单，就是一系列的 File Entry。每个 File Entry 由头部，文件名和数据组成，其头部格式是：

```c
struct cpio_entry_header {
  char magic[6];
  char dev[6];
  char ino[6];
  char mode[6];
  char uid[6];
  char gid[6];
  char nlink[6];
  char rdev[6];
  char mtime[11];
  char namesize[6];
  char filesize[11];
};
```

magic 字段恒为 `070707`。其他字段都保存的是数字，用八进制数转成 ASCII 码保存。例如文件名长度是 28，转成八进展是 034，`namesize` 字段是 6 个字节，所以添加前置 0，得到 `000034`，用 ASCII 保存在 `namesize` 字段。

读取 Entry 头部以后，把其中的 `namesize` 和 `filesize` 字段转换成整数，就知道文件名（包括末尾 0）和数据的长度。头部后面紧接着就是文件名，然后是数据。所有 Entry 拼接在一起，就是完整的 cpio 文件。没有额外的 padding。

为了表示 cpio 文件的结束，最后一个文件的文件名是 `TRAILER!!!`。

cpio 的设计非常简单，被用于 initramfs 等场合。相比 Tar，cpio 没有把结构体对齐到 512 字节的边界，并且文件名也采用了动态长度的方法。

总结一下，cpio 文件的格式就是：`(头部，文件名，数据)*`。为了表示结束，最后一个文件的文件名是固定的 `TRAILER!!!`。

## 常用命令

创建 cpio：`find . | cpio -ov > archive.cpio`

展开 cpio：`cpio -idv < archive.cpio`

