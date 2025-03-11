# 垃圾回收 Garbage Collection

## 基本概念

- mutator: 指用户程序，因修改 GC 状态而得名
- collector：指垃圾回收程序
- mark-sweep：mark 阶段标记所有活跃的对象，sweep 阶段回收不活跃的对象
- mark-compact：mark 阶段标记所有活跃的对象，compact 阶段丢弃不活跃的对象，把活跃的对象放在连续的内存
- copying collection：把活跃的对象复制到新的堆，然后回收旧的堆
- reference counting：引用计数，计数降到 0 的时候释放
- stop the world：把 mutator 都停下来以后，启动垃圾回收，回收完成再继续 mutator 的执行
- GC root: 用于寻找活跃对象的根结点，通常包括寄存器，调用栈和全局变量，通过这些结点可以找到所有的活跃对象；无法通过根结点访问的对象，则是不活跃的对象

## Mark-Sweep

Mark-Sweep 垃圾回收分为两个阶段：

- Mark 阶段：从 GC root 开始，找到所有的活跃对象并标记
- Sweep 阶段：扫描堆中的对象，把没有被标记为活跃的对象释放掉

对象是否活跃的标记可以和对象放在一起，也可以单独以类似 bitmap 的方式保存。Sweep 阶段也未必要每次 Mark 完就去做，可以做得更 Lazy。

### 三色标记 Tri-colour

三色标记（tri-colour）是记录对象在 Mark 阶段的三种状态：

- 黑色：活跃对象，并且已经 Mark 完成
- 灰色：活跃对象，但还没 Mark 完成，还需要遍历
- 白色：还没 Mark 到，或者是非活跃对象

在 Mark 的时候，首先把 GC root 里面的对象标记为黑色，把它们引用的对象标记为灰色，接着去搜索这些灰色的对象引用的其他对象。在遍历灰色对象完成的时候，把它标记为黑色；当所有灰色都转化为黑色时，Mark 结束。这里的灰色就相当于搜索的 frontier。

## 参考

- [The Garbage Collection Handbook - The art of automatic memory management](http://gchandbook.org/)
