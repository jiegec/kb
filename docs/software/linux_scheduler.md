# Linux Scheduler 分析

## CFS Completely Fair Scheduler

文档：[CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html)

设计目标：建模一个理想的多任务 CPU，它以相同的速度并行运行多个任务，每个任务运行的时间一样长。

但是这样的 CPU 不存在，不同的任务需要分时执行。因此需要记录每个任务执行的时间，让不同任务可以得到相同的 CPU 时间。CFS 要做的是，让可以运行的任务尽量得到相同的 CPU 时间。那就要找到那些没有得到足够 CPU 时间的任务，去调度它们。

为了记录进程的 CPU 时间任务，CFS 给每个 Task 记录了一个 virtual runtime，那么如果一个任务的 virtual runtime 比别人都少，那就说明它得到的 CPU 时间不够，要调度它。

因此，调度实际上就是要找到当前 virtual runtime 最小的任务。CFS 用平衡树来维护这个信息，调度 virtual runtime 最小的任务，从平衡树中删除，当任务运行了一段时间后，回到调度器，它的 virtual runtime 增加，再插入平衡树。

virtual runtime 和实际 runtime 的区别是，它考虑了优先级：通过 nice 可以设置任务的权重，权重大的，相同运行时间，virtual runtime 增加的少，那么就会被分到更多的 CPU 时间。

注意 CFS 考虑的是某个核上的进程的调度，它不管进程被调度到哪个核上。

## EEVDF Earliest Eligible Virtual Deadline First

文档：[EEVDF Scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html)

EEVDF 是在 CFS 基础上的改进。CFS 主要考虑的是公平性，讲究的是所有任务得到一样多的 CPU 时间。EEVDF 除了考虑公平性，还要考虑及时性，改进 Latency。

它的思路是，统计每个任务的实际运行时间和预期运行时间，如果实际运行的比预期的少，才会被考虑去调度（Eligible）：实际比预期少的时间叫做 lag，那么 Eligible 意味着 lag 非负。Eligible 的任务可能有多个，此时选取它们 virtual deadline 最小的那个任务去调度。virtual deadline 怎么计算的呢？论文[Earliest Eligible Virtual Deadline First: A Flexible and Accurate Mechanism for Proportional Share Resource Allocation](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=805acf7726282721504c8f00575d91ebfd750564) 中是这么分析的：

考虑一个实时系统，有一个需要定期进行的任务，例如视频解码，在时间 t 收到了一帧的数据，需要解码并显示到屏幕上，那么为了显示的流畅，肯定要在下一帧之前完成。假设每 T 时间会收到一帧，需要 r 时间完成解码，那么这个任务每 T 时间就要获得 r 的 CPU 时间。用 CFS 的话来说，它的权重占所有任务的 $r/T$，记为 f。

那么反过来，假如我知道一个任务的权重占比是 f，我希望它在什么时刻之前完成呢？假如我在 t 时刻收到一帧，我希望任务在下一帧之前完成，也就是要在 $t+T$ 时刻前完成。而 $f=r/T$，那么 $T=r/f$，带入 $t+T$，得到 $t+\frac{r}{f}$。它计算的是：假如这是一个定期执行的实时任务，它应该在什么时刻之前完成？这个式子已经很接近最终的 virtual deadline 计算方法。

## runqueue

runqueue 是 Linux 的 per cpu 数据结构，维护了在这个核上要运行的任务。为了负载均衡，把机器的不同核心用起来，需要在不同 cpu 的 runqueue 之间迁移任务。为了实现合理的负载均衡，调度器需要知道处理器的拓扑，这是通过 [Sched Domain](https://docs.kernel.org/scheduler/sched-domains.html) 来表示的。

Domain 呈一个树型结构，每个结点是 CPU 核的一个划分，父结点是子结点的超集，比如 SMT 同一个物理核的两个逻辑核，同一个 NUMA Node，整个 Socket，所有核。通过这个树型结构，内核调度器就可以知道 CPU 核心的拓扑。

接着是在这棵树上进行负载均衡。每个 Domain 可以有若干个 Group，每个 Group 记录了若干个 CPU 核心，那么负载均衡的粒度就是 Group，保证同一个 Domain 下，不同 Group 的负载是差不多的。Group 的负载，就是这个 Group 内所有核的负载之和。

Linux 内核会定期进行负载均衡，检查 Domain 里面，有没有哪个 Group 负载最高，如果有，尝试把任务挪到其他的 Group 的 runqueue 内部。

那么，对于 SMT 来说，每个物理核成为一个 Group，Group 内就是两个逻辑核。通过负载均衡，先给每个 Group 的其中一个核分配任务，如果所有 Group 都有任务了，再向 SMT 的第二个逻辑核上分配任务。

## 参考

- [Linux CFS 调度器：原理、设计与内核实现（2023）](http://arthurchiao.art/blog/linux-cfs-design-and-implementation-zh/)
- [EEVDF Patch Notes](https://hackmd.io/@Kuanch/eevdf)
- [Linux 内核：EEVDF 调度器详解](https://zhuanlan.zhihu.com/p/704413081)
- [CFS 的覆灭，Linux 新调度器 EEVDF 详解](https://zhuanlan.zhihu.com/p/683775984)