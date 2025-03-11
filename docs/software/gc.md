# 垃圾回收 Garbage Collection

## 基本概念

- mutator: 指用户程序，因修改 GC 状态而得名
- collector：指垃圾回收程序
- mark-sweep：mark 阶段标记所有活跃的对象，sweep 阶段回收不活跃的对象
- mark-compact：mark 阶段标记所有活跃的对象，compact 阶段丢弃不活跃的对象，把活跃的对象放在连续的内存
- copying collection：把活跃的对象复制到新的堆，然后回收旧的堆
- reference counting：引用计数，计数降到 0 的时候释放

## 参考

- [The Garbage Collection Handbook - The art of automatic memory management](http://gchandbook.org/)
