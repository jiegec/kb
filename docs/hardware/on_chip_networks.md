# 片上网络

## 背景

随着芯片内的核心数量增多，在实现互联的时候，传统的 Crossbar 遇到了扩展性的瓶颈，因此需要用片上网络来替代 Crossbar。

下面主要按照 [On-Chip Networks, Second Edition](https://link.springer.com/book/10.1007/978-3-031-01755-1) 以及《计算机系统结构》课程课件的顺序进行讲解。

## 拓扑

拓扑讲的就是结点间的连接方式。比较常见的拓扑有：

1. Ring：每个结点连接到环上相邻的两个结点
2. Mesh：以 2D Mesh 为例，把结点放在一个网格里，每个结点最多连接四个相邻结点：在内部的连接四个相邻结点，在边上的只连接三个相邻结点，在角上的只连接两个结点
3. Torus：在 Mesh 的基础上，让边和角上的结点也连接四个结点：边上的结点连到对侧最远的结点，角上的结点连到另外两个角

<figure markdown>
  ![Ring, Mesh and Torus](on_chip_networks_example.png){ width="600" }
  <figcaption>Ring，Mesh 和 Torus（图源 <a href="https://link.springer.com/book/10.1007/978-3-031-01755-1">On Chip Networks, Second Edition</a>）</figcaption>
</figure>

其中 Mesh 和 Torus 还可以扩展到高阶情况，例如 3D 的立方体。

可以从以下几个方面评估一个拓扑的属性：

1. 结点的度：连接的结点数
2. 直径：结点间距离的最大值
3. 等分宽度：网络被切成两半（或者几乎两半）的时候，切割的最小边数

在这三种拓扑中，结点既是流量的起点和终点，又负责了流量的转发。

另一类拓扑中，有部分结点只负责转发流量，不作为流量的起点和终点，例如 Butterfly 网络，Clos 网络，Fat Tree。

但由于片上网络是要实现在芯片上的，而芯片是 2D 的，所以片上网络一般会用可以放在平面上的拓扑，比较常见的就是 Mesh 和 Ring。

## 路由

确定好网络拓扑后，在实际传输之前，由于两个结点间路径不唯一，所以需要考虑如何把请求从起点路由到终点。这里主要考虑的是 Mesh 拓扑的路由算法。

首先容易想到的是选择最短路径，但在 Mesh 拓扑中，最短路径也是不唯一的，因此还是需要更加具体的算法来做出选择。

路由在选取的时候还需要考虑死锁的问题：由于通常片上网络是不允许丢包的，因此如果发送数据时，接收方的缓冲区已经满了，就不能继续发送了。那么这个时候就会出现一个依赖关系：A 要发给 B，但同时 B 也要发给 C，现在 B 和 C 的缓冲区满了，那么只有等 C 的缓冲区释放空间，B 才能发给 C，然后 B 的缓冲区才得以释放，A 才能发给 B。换句话说，A 到 B 的传输只有等 B 到 C 的传输完成才可以继续。

那么，假如此时 A 到 B 要等待 B 到 C 传输完成，B 到 C 要等待 C 到 D 传输完成，C 到 D 要等待 D 到 A 传输完成，D 到 A 要等待 A 到 B 传输完成，此时就出现了死锁：互相依赖，出现了环，并且没有办法从环中退出，那就死锁了。

<figure markdown>
  ![Deadlock in NoC](on_chip_networks_deadlock.png){ width="300" }
  <figcaption>路由协议死锁的情况（图源 <a href="https://link.springer.com/book/10.1007/978-3-031-01755-1">On Chip Networks, Second Edition</a>）</figcaption>
</figure>

一个经典的路由算法是维序路由（Dimension Ordering Routing，简称 DOR），意思就是按照维度的顺序去路由，只有前一个维度走到和终点相同，才会在下一个维度继续走。例如在二维场景下，X-Y 路由就是先走 X 轴，走完 X 轴以后再走 Y 轴。反过来 Y-X 路由则是先走 Y 轴，再走 X 轴。

维序路由十分简单，容易实现，并且不会出现死锁。维序路由不会出现死锁的原因是，它的依赖不会出现环：以 X-Y 路由为例，所有 X 方向上的传输可能依赖 Y 方向上的传输，但 Y 方向上的传输不会依赖 X 方向上的传输。还是以上图为例子：A 到 B 的传输依赖 B 到 C 的传输，但是 B 到 C 的传输不会依赖 C 到 D 的传输，因为这不符合 X-Y 路由的规则。

但是维序路由的缺点也很明显：浪费了很多可能的路径，例如 A 和 B 同时要向 C 传输，就会在 B 到 C 的边上拥挤，无法利用剩下的路径。

接下来介绍路由算法的两个分类：一类是 Oblivious 路由算法，另一类是 Adaptive 路由算法。顾名思义，Oblivious 不考虑网络当前的拥塞状态，直接按照自己的算法来发；Adaptive 会根据网络当前的拥塞状态，期望找到一个不那么拥挤的路径。

显然，维序路由没有考虑网络是否拥塞，属于 Oblivious 路由算法。另一个典型的 Oblivious 路由是 Valiant 随机路由算法：随机选择一个中间结点，先从起点路由到中间结点，再从中间结点路由到终点。还有一种典型的 Oblivious 路由，就是随机选择 X-Y 路由或 Y-X 路由的一种，但是可能会出现死锁。

Adaptive 路由算法的目的是，根据网络的拥塞情况，找到一个更优的路由，绕过拥塞的部分，实现更高的带宽利用率。例如如果最短路径上出现了拥塞，可以尝试绕路，在一条不拥塞的最短路径上传输。但是绕路的时候，需要防止活锁：一直在绕路，从来没到达目的地。

设计 Adaptive 路由的时候，也要考虑如何避免死锁。维序路由保证了不会出现死锁，但也唯一确定了路由，无法支持 Adaptive 路由。但实际上，为了避免死锁，不需要像维序路由那么严格。

回顾一下维序路由中的 X-Y 路由：它要求先走 X 轴，再走 Y 轴，那么从 X 轴拐到 Y 轴的时候，有四种情况，见下图 (b)：

<figure markdown>
  ![Turns in 2-D Mesh](on_chip_networks_turn.png){ width="500" }
  <figcaption>Mesh 的转向（(a) 是所有可能，(b) 是 X-Y 路由）（图源 <a href="https://link.springer.com/book/10.1007/978-3-031-01755-1">On Chip Networks, Second Edition</a>）</figcaption>
</figure>

这种拐法可以保证不出现死锁，但是有更加宽松的转向方式，也可以保证不出现死锁，例如下面的三种：

<figure markdown>
  ![Turn models in 2-D Mesh](on_chip_networks_adaptive_turn.png){ width="500" }
  <figcaption>Mesh 的三种转向模型（图源 <a href="https://link.springer.com/book/10.1007/978-3-031-01755-1">On Chip Networks, Second Edition</a>）</figcaption>
</figure>

每种转向模型都在八种转向中去掉了两种，这样就实现了无死锁。West First Turns 的意思是先往西走，转向后不再往西走；North Last Turns 的意思是往北走只能出现在最后阶段，往北走以后就不再转向；Negative First Turns 的意思是先往西（X 轴负方向）或者南（Y 轴负方向）走，之后再往东（X 轴正方向）或者北（Y 轴正方向）走。

还有一种 Odd-even 方法：在偶数列的时候，禁止东转北和北转西；在奇数列的时候，禁止东转南和南转西。

有了更多转向方向后，就允许出现多种可能的路径，意味着 Adaptive 路由算法可以在保证不死锁的前提下，找出一条比较优的路径。

## 流控

## 参考资料

- [On-Chip Networks, Second Edition](https://link.springer.com/book/10.1007/978-3-031-01755-1)