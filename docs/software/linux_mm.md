# Linux 内存管理（Memory Management）

## Transparent Huge Page (THP)

文档：[Transparent Hugepage Support](https://docs.kernel.org/admin-guide/mm/transhuge.html)

自动合并多个连续的虚拟地址-物理地址映射，到粒度更粗的一级页，比如 512 个 4KB 合并到一个 2MB 页，当然物理地址也要连续。合并的粒度受限于页表的设计，只能一级一级的合并。

mTHP(multi size THP)：更细粒度的合并，不节省内存，但是告诉硬件，有若干个 PTE 的映射是连续的（Contiguous PTE），节省 TLB。需要硬件支持：

- RISC-V：Svnapot，N=1 表示 16 个连续的 4KB page，一共 64KB 对应一个 TLB entry
- ARMv8: Contiguous bit，设置后，连续若干个 page 对应一个 TLB entry，例如 16 个连续的 4KB page 对应一个 TLB entry

## Same Page Merging

文档：[Kernel Samepage Merging](https://docs.kernel.org/admin-guide/mm/ksm.html)

节省内存，多个虚拟页映射到一个物理页
