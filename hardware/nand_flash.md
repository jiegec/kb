# NAND Flash

## 结构

NAND Flash 分如下层次：

- Package/Chip
- Die
- Plane
- Block：Erase 的粒度
- Page：Program/Read 的粒度

Erase：把整个 Block 的数据写成全 1

Program：把 Page 的某些 1 改写成 0，但不能把 0 改写成 1

物理上：Erase 把电压变成最低，对应 1，Program 把电压抬高，把 1 变成 0。

MLC：2 bit per cell，有四种电压。

TLC：3 bit per cell，有八种电压。

## 参考文献

- [Understanding Flash: Blocks, Pages and Program / Erases](https://flashdba.com/2014/06/20/understanding-flash-blocks-pages-and-program-erases/)
- [NAND Flash 101](https://www.simms.co.uk/Uploads/Resources/50/f4366381-b992-425a-bec4-cca409b51a6c.pdf)
