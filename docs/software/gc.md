# 垃圾回收 Garbage Collection

本文是对 [The Garbage Collection Handbook - The art of automatic memory management](http://gchandbook.org/) 一书的学习笔记。

## 基本概念

- mutator: 指用户程序，因修改 GC 状态而得名
- collector：指垃圾回收程序
- mark-sweep：mark 阶段标记所有活跃的对象，sweep 阶段回收不活跃的对象
- mark-compact：mark 阶段标记所有活跃的对象，compact 阶段丢弃不活跃的对象，把活跃的对象放在连续的内存
- copying collection：把活跃的对象复制到新的堆，然后回收旧的堆
- reference counting：引用计数，计数降到 0 的时候释放
- stop the world：把 mutator 都停下来以后，启动垃圾回收，回收完成再继续 mutator 的执行
- GC root: 用于寻找活跃对象的根结点，通常包括寄存器，调用栈和全局变量，通过这些结点可以找到所有的活跃对象；无法通过根结点访问的对象，则是不活跃的对象
- interior pointer: 指针指向某个对象的中间位置，而不是对象开头

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

## Mark-Compact

Mark-Compact 垃圾回收分为两个阶段：

- Mark 阶段：从 GC root 开始，找到所有的活跃对象并标记
- Compact 阶段：扫描并移动堆中的对象，使得它们紧凑地保存在一起

### Two-Finger Compaction

Two-Finger Compaction 是一种 Mark-Compact 的 Compact 阶段的实现，它需要维护两个指针：一个指针 `free` 一开始指向堆的开头，从前往后去寻找下一个可以存放对象的空闲的空间；另一个指针 `scan` 一开始指向堆的结尾，从后往前去寻找需要被挪到前面的对象。这个算法分为两轮，第一轮是移动对象：

1. 递增 `free` 指针，直到找到一个可以存放对象的空闲的空间
2. 递减 `scan` 指针，直到找到一个需要被挪到前面的对象（要求 `scan > free`）
3. 把处于 `scan` 指针的对象移动到 `free` 指向的位置
4. 因为可能有其他对象拥有对 `scan` 指向的对象的指针，为了保证后续指针可以被正确地更新，在 `scan` 指针的位置，留下一个指向 `free` 的信息，表示之前在 `scan` 指针的位置这里有个对象，现在被挪到了 `free` 这个位置
5. 循环以上过程，直到所有对象都被紧密地保存，此时 `free >= scan`

这个过程有点像快速排序里的 partition：快速排序里，partition 就是把左边小于 pivot 的元素和右边大于 pivot 的元素交换；在这里，相当于是把左边的空位和右边的对象交换。最后两边指针汇合了，就意味着交换结束了。

此时对象已经被 Compact 了，但是很多对象的指针还指向了旧的地址，因此需要进行第二轮，即更新指针：遍历各个对象，如果它的字段指向了一个被挪走的对象，就需要把地址改成它的新位置：根据上面第四步留下的信息，把指针改为它目前所在的新的地址即可。

这个算法在对象大小都一样的时候比较好用，不然可能会出现 `scan` 指向的对象太大，放不进 `free` 指向的空隙中的情况。

### Lisp 2

Lisp 2 是另一种 Compact 算法，它和 Two-Finger Compaction 有一些像，但它分为三个步骤：

1. 第一个步骤是 computeLocations，地址从低往高遍历，给每个活跃的对象，按地址从低往高顺序分配 compact 后的位置，也就是计算出它 compact 后的地址，这个地址会保存在对象的 forwardingAddress 字段中，即这个对象的新地址
2. 第二个步骤是 updateReferences，更新对象的字段，把各字段的指针改成对应对象的 forwardingAddress，也就是去指向新的 compact 后的地址
3. 第三个步骤是 relocate，即按照地址从低往高的顺序，把各对象挪到第一步已经计算好的位置上；地址的分配和移动顺序，保证了移动的时候不会覆盖掉不该覆盖的对象

这样做的好处是，对象在堆中的相对顺序被保留了下来，因此缓存局部性会好一些，代价是每个对象要多保存一个 forwardingAddress 指针；而 Two-Finger Compaction 算法会打乱对象之间的顺序，可能会导致缓存局部性不好。

### Jonkers’s threaded compactor

Threaded compactor 的思路是，复用已有的对象的字段的空间，去维护 forwardingAddress 信息，从而避免了 Lisp 2 算法的额外的空间，同时可以保证对象之间的顺序。这个复用的思路是这样的：

1. 初始状态下，A B C 三个对象分别有字段指向了 N，此时无法从 N 知道有哪些字段引用了它
2. 通过遍历，构造出一个链表：N -> C -> B -> A，也就是说把引用了 N 这个对象的字段都放到一个链表里面，这个时候就可以从 N 知道有哪些字段引用了 N
3. 那么在要移动 N 的时候，就可以在知道 N 的新地址的同时，遍历这个链表，恢复出原来的连接关系（即 A B C 三个对象分别有字段指向了 N），并修正 A B C 三个对象的字段的指针，让它们指向 N 的新地址

这个思路有点像 Morris Traversal，一种在二叉树上 O(1) 空间开销的中序遍历方法，它利用已有的树的指针，去构建一条回溯的路径，从而避免了栈的内存开销。

在这个思路的基础上，就得到了这个算法的三轮遍历：

1. 第一轮，遍历对象，把指针改写成上面所述的形式；这一轮过后，每个对象都能找到自己被引用的所有字段
2. 第二轮，再次遍历对象，给对象分配 compact 后的地址，此时通过链表，可以找到所有引用当前对象的字段，把指针改写回正确的连接关系，并改成 compact 后的地址；这一轮过后，每个对象的字段都指向了对应对象的新地址
3. 第三轮，再次遍历对象，把对象挪到正确的位置

实际上，这三轮遍历可以简化为两轮遍历。首先来分析一下这三轮为啥不能同时进行：如果同时进行第一轮和第二轮，那么在遍历对象的时候，假设依然是按照地址从低到高遍历，那么只有地址比它低的对象的字段引用它，才会出现在链表当中，而地址比它高的对象的字段引用它就不在链表当中，因为还没有被遍历到；如果同时进行第二轮和第三轮，因为第二轮需要改写对象的字段的指针，这意味着这些对象本身不能被挪走，但是第三轮在移动对象，会改变地址比当前对象小的对象的位置。

结合这个分析，可以改进，得到一个两轮遍历的方法：

1. 第一轮，地址从低往高遍历，计算每个对象被 compact 后的地址，首先根据当前对象的链表去恢复引用当前对象的字段，由于遍历的顺序，只有地址低引用地址高的字段会被修正（称为“前向”引用）；然后，也以当前对象的字段去构造链表，最终地址高引用地址低的字段（称为“后向”引用）会留下来，用于第二轮
2. 第二轮，地址从低往高遍历，此时前向的引用都被修正了，可以移动对象到被 compact 后的地址，不用担心出错；而此时第一轮也把后向的引用都加入了链表当中，此时再修正后向的引用，由于地址比当前地址大的对象都没有被移动，所以修改不会出现问题

这里利用遍历的顺序，把引用分为了前向和后向，巧妙地把三轮改成了两轮，并且保证了正确性。由于遍历的顺序相同，两轮计算出来的对象被 compact 后的地址也是相同的，也就不需要保存下来，节省了内存。这里还有一个巧妙的节省空间的设计，就是把原来对象头部的空间拿来存指针，然后把头部空间原来的内容放到链表的末尾，最后再恢复回来，当然了，需要能够区分指针和对象头部的数据。

这个算法在 [Algorithms for Dynamic Memory Management (236780) Lecture 2 by Erez Petrank](https://csaws.cs.technion.ac.il/~erez/courses/gc/lectures/02-compaction.pdf) 中有详细的 step by step 图示，建议读者阅读。

### One Pass Compaction

还有一种 Compaction 的优化，叫做 One Pass Compaction。在前面的几种 Compact 算法中，都需要扫描堆中的活跃对象，从而计算出它们被 compact 后的新地址。而 One Pass Compaction 不是扫描堆中的活跃对象，而是扫描 bitmap，bitmap 记录了堆中哪些部分保存了活跃对象，哪些部分没有。根据这个信息，它进行如下的预处理操作：

1. 把堆分成若干个固定大小的块，比如每个块 256 字节
2. 虽然不知道这个块内有多少个对象，但是通过 bitmap，可以知道这个块内分配了多少字节的数据用于保存对象
3. 以块的粒度，按照顺序给每个块分配空间，得到每个块在 compact 后的地址

有了这个信息以后，再遍历堆里的活跃对象，此时，可以利用预处理好的信息，计算出每个对象在 compact 后的地址：

1. 首先根据对象的地址，找到它属于哪个块，并处于块内的第几个对象，它前面要保存多少字节的数据
2. 找到对应块 compact 后的地址，加上块内的偏移，就得到了这个对象 compact 后的地址

有了这个对应关系了以后，就可以把对象和各个字段中的指针按照同样的方法映射到 compact 后的地址，在移动对象的同时，也把指针更新好了。这个思路事实上就是通过分块，加速了地址计算，减少了地址计算的开销，从而避免了两轮遍历。严格来说，遍历 bitmap 也要一轮，但是因为它比较小（若干个字节对应 bitmap 的一个 bit），所以就不算成一轮了。

## Copying Collection

Copying Collection 的方法是，把堆分成两个区域，分别叫做 fromspace 和 tospace。一开始，所有的对象保存在 fromspace 中，要进行垃圾回收的时候，把活跃的对象从 fromspace 拷贝到 tospace 的连续空间中。当所有对象拷贝完成的时候，fromspace 可以直接清空。之后 tospace 和 fromspace 的角色互换，就像 double buffer 那样。

在拷贝的时候，和之前的 Compact 算法类似，也需要记录对象的 forwardingAddress：当对象从 fromspace 迁移到 tospace 的时候，在 fromspace 的那一份对象的 forwardingAddress 记录的是它在 tospace 里的新地址。当然了，可以直接利用 fromspace 里的空间，原地保存 forwardingAddress。

### Cheney Scanning

在遍历 fromspace 的对象用于复制的算法中，Cheney Scanning 算法是一种经典的实现，相当于用 tospace 来维护 BFS 的队列：

1. 首先把 GC root 引用的对象复制到 tospace 空间
2. 维护两个指针：`scan` 一开始指向 tospce 空间的最开头，`free` 指向 tospace 中空闲的空间的开头
3. 从 `scan` 指针开始，扫描 tospace 已有的对象，找到它所引用的在 fromspace 中还没复制到 tospace 的对象，把 fromspace 中的对象复制到 tospace 中 `free` 指向的空闲空间，更新 forwardingAddress，然后更新 `free` 指向剩余的空闲空间
4. 当 `scan` 等于 `free` 的时候，所有的 fromspace 活跃对象都已经复制完毕

## 参考

- [The Garbage Collection Handbook - The art of automatic memory management](http://gchandbook.org/)
- [Algorithms for Dynamic Memory Management (236780) Lecture 2 by Erez Petrank](https://csaws.cs.technion.ac.il/~erez/courses/gc/lectures/02-compaction.pdf)
