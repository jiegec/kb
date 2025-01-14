# Linux 资源控制（Resource Control）

在 Linux 上运行的程序，共享了缓存和内存，那么它们之间是会互相影响性能的。如果想要给某些程序预留一定的资源，可以用 Linux resctrl(resource control) 机制来实现。

它背后依赖的是硬件的功能，比如 Intel 实现的 Resource Director Technology(RDT)，分为以下几个部分：

1. Monitoring：主要是监控缓存和内存的状态，包括：
	1. Cache Monitoring Technology (CMT)，监控程序的 L3 缓存占用
	2. Memory Bandwidth Monitoring (MBM)，监控程序的内存带宽使用
2. Allocation：主要是限制缓存和使用，包括：
	1. Cache Allocation Technology (CAT)，限制程序的 L2/L3 占用，把程序划分到若干个类（Class of Service，简称 COS 或者叫 CLOS）里面，每个类对应一个 bitmask
	2. Code and Data Prioritization (CDP)，在 CAT 的基础上，分别限制程序的指令和数据的 L2/L3 占用：每个 CAT 的类有从一个 bitmask 变成有两个 bitmask，一个用于数据，一个用于指令
	3. Memory Bandwidth Allocation (MBA)，限制程序的内存带宽使用
3. 针对 PCIe/CXL 外设访问 L3/内存的 Monitoring 和 Allocation

ARMv8-A 平台上类似的功能叫做 MPAM(Memory System Resource Partitioning and Monitoring)。

Linux 的 resctrl 功能通过 sysfs 挂载 resctrl 来暴露：

```shell
mount -t resctrl resctrl /sys/fs/resctrl
# create a new resource group called p0
mkdir /sys/fs/resctrl/p0
# add cpu 0-1 (bitmask 3) to p0
echo 3 > /sys/fs/resctrl/p0/cpus
# add tasks(processes/threads) to p0
echo pid0,pid1 > /sys/fs/resctrl/p0/tasks
# set L2 #0 bitmask to 0xffc00 for p0
# you can change global settings at /sys/fs/resctrl/schemata
echo "L2:0=ffc00;" > /sys/fs/resctrl/p0/schemata
```

这样处理完，在核心 0-1 上运行的程序，就只会用到 L2 的由 0xffc00 指定的那部分缓存容量。

参考：

- [Performance tuning at the edge using Cache Allocation Technology ](https://www.redhat.com/en/blog/performance-tuning-at-the-edge)
- [User Interface for Resource Control feature](https://docs.kernel.org/arch/x86/resctrl.html)
- [Configuring MPAM via resctrl file-system](https://developer.arm.com/documentation/108032/0100/A-closer-look-at-MPAM-software/Linux-MPAM-overview/Configuring-MPAM-via-resctrl-file-system)
- [Use Intel® Resource Director Technology to Allocate Last Level Cache (LLC)](https://www.intel.com/content/www/us/en/developer/articles/technical/use-intel-resource-director-technology-to-allocate-last-level-cache-llc.html)
- [resctrl](https://github.com/intel/intel-cmt-cat/wiki/resctrl)
