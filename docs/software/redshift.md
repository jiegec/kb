# Amazon Redshift

本文基于 [Amazon Redshift Database Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html) 整理。

## 架构

文档：[Amazon Redshift System and architecture overview](https://docs.aws.amazon.com/redshift/latest/dg/c_redshift_system_overview.html)

Redshift 集群由若干个 compute node 组成，如果有两个或以上的 compute nodes，还有一个额外的 leader node。客户端和 leader node 通信，如果只有一个 compute node，那么它也会充当 leader node 的作用。

数据分布式地保存在 S3 和 compute node 的本地 SSD 存储上，通过 Redshift Managed Storage（RMS）自动管理，本地 SSD 存储相当于是 S3 的 cache。

为了并行性，数据会分布到各个 compute node 上，更进一步，每个 compute node 分为多个 slice，slice 会平分 compute node 的各种资源，所以实际上数据分发的粒度是 slice。每个 slice 内部进行计算，然后把结果发送到 leader node 上进行合并，最后发给客户端。

那么为了性能，最好是每个 slice 只用到本地的数据，尽量避免 slice 之间需要数据通信的情况。为了分发数据到各个 slice，Redshift 设计了 distribution key，用户可以指定 distribution key 以及 distribution style，决定数据如何分发到各个 slice 里，目的是后续查询的时候可以更快地找到要用到的数据。

Redshift 采用列式存储，同一列相邻行的数据是连续存放的，类似于 column major 的矩阵保存形式。由于每一列的大小一般比较小，并且很多时候是定长的，所以可以更加紧密地保存下来，也方便进行压缩。查询时，可以只访问要用到的列，不去读取没访问到的列的数据，省下来这部分 I/O 时间。Redshift 采用 1MB 大小的块，用来存储每一列的数据。

Redshift 支持请求缓存，在进行 SQL 查询的时候，如果曾经完成过同样的 SQL 查询，并且这段时间内数据没有变化，那么可以从请求缓存中直接把结果取出来，不用重新查询。

## 最佳实践

文档：[Amazon Redshift Best practices](https://docs.aws.amazon.com/redshift/latest/dg/best-practices.html)

### Distribution key

Distribution key 和 distribution style 决定了数据如何分布在各个 slice 中。如果预先设好的分布方案与实际查询时所期望的分布方案不同，就需要通信以重新分发数据，那么性能就会受到影响。除此之外，还尽量要保证不同 slice 比较均匀地分到数据，避免少数 slice 保存和处理大部分数据，影响并行性，同理，进行查询的时候，也要尽量保证每个 slice 都有自己的计算可以做。

[Distribution Style](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html) 有这么几种：

1. AUTO：由 Redshift 自动选择
2. EVEN：没有 Distribution key，插入数据时直接 Round-robin 式把数据分发到各个 slice 上
3. KEY：按照 Distribution key（某一个 column）进行分发，如果某两行在 Distribution key 下的值相同，那么这两行会被分到同一个 slice 上
4. ALL：把数据复制到所有的 node 上，每个 node 保存一份完整的数据，供所有 slice 读取

选择 Distribution style 的时候，要结合 workload 来进行分析。如果主要的查询是对两个表进行 join，把要 join 的 key 设为 Distribution key 是比较合理的方案，这样两个表的数据里的具有同一个 join key 的行会保存在同一个 slice 内部，那么每个 slice 内部就可以完成 join 操作，不需要在 slice 之间通信。

更详细的原则见 [Designating distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/t_designating_distribution_styles.html)，简单总结一下：

1. 经常 join 的 key，就设为对应 table 的 distribution key
2. 每个 table 的 distribution key 只能有一个，但是要 join 多个表，怎么办？选性能影响最大的那个，根据要 join 的表的大小来估计，估计大小时不要忘记考虑 filter
3. 实在不好设计 distribution key，又想提升查询性能，可以用 ALL distribution style，用空间换时间
4. 对于性能影响不大的表，可以让 Redshift 自动选择

为了确认分布方案是否合理，可以用 EXPLAIN 语句获取常用 SQL 查询的 Query Plan，可以看到 Redshift 是怎么执行这条 SQL 语句的，在里面就可以看到不同 Distribution key 的影响。

### Sort key

文档：[Choose the best sort key](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-sort-key.html) 和 [Working with sort keys](https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html)

除了 Distribution key 以外，还有一个很重要的概念，就是 Sort key。Sort key 对应数据库里的索引（Index），其实就是把数据按照什么顺序排序，方便查询。传统数据库每个表支持多个 Index，每个 Index 可以用不同的 Key，那么查询的时候，就可以利用这些 Index 来加速查询。Redshift 则不同，它每个表只有一个 Index，用 Sort key 排序，所以 Sort key 的选取对性能也是很重要的。

Distribution key 主要涉及到 slice 之间的数据分布方式，以及查询时 slice 之间需要多少的数据传输。而 Sort key 主要涉及的是 slice 内部实现查询时，能否高效地进行。

例如对两个表进行 join 的时候，如果两个表都按照 join key 排好了序，那就可以用类似归并排序的归并操作，双指针快速地同时遍历两边的表的同一个 join key。如果没排好序，那就要 fallback 到哈希表 join，从一个表构建哈希表，遍历另一个表，然后在哈希表里寻找 join key 匹配的行。再比如对某些列进行过滤的时候，如果已经按列排好序，那就可以很快地找到上下界，不用一个个去遍历。

相比 Distribution key 只能设置一个列，Sort key 则更加灵活，它支持如下模式：

1. COMPOUND：可以指定多个列，按多关键字排序，那么按照 Sort key 的前缀列进行查询的时候，就可以利用排好序的性质，提升查询性能
2. INTERLEAVED：可以指定多个列，但最多 8 列，它相比 COMPOUND 更复杂，加载数据时更慢，但是比较灵活，不一定要查询前缀列，可以任意组合

特别地，如果只有一个列需要排序，这个列的内容又有很多相同前缀的时候（例如大量 URL 开头都是 `https://www`），COMPOUND 模式下，它为了节省字符串比较时间，可能会只选取字符串的前若干个字节（从 `STV_BLOCKLIST` 的 `minvalue` 和 `maxvalue` 来推断，是前 8 个字节）来排序，这样排序的效果就变差了；而 INTERLEAVED 模式会做的更好。

### Fact Table 和 Dimension Table

在 Redshift 文档里会涉及到两个数据分析的概念：Fact Table 和 Dimension Table。Fact Table 一般是保记录某个事情的发生，这个事情涉及到了哪些人，哪些物品，发生在什么时间。这些涉及到的人和物品的信息都是用 ID 保存下来，然后用另一个 Dimension 表来具体保存每个人的信息，每个物品的信息，等等。

例如，对于一个网上购物系统，Fact Table 记录了所有订单，订单记录了买家的 ID，卖家的 ID，商品的 ID，商品的数量和价格，然后有多个 Dimension Table，所有买家是一个表，卖家是一个表，所有商品也是一个表。

这样，Fact Table 就是有大量的到 Dimension Table 的 Foreign Key。查询的时候，通常会把 Fact Table 和多个 Dimension Table join 起来。例如要找到所有卖家在每个商品卖出的总价格，那就把 Fact Table 和卖家表和商品表 join 起来，然后按卖家和商品进行 group by，对价格做求和。

如果要对这个例子优化，那么就要比较卖家表和商品表谁更大，一般来说，商品比卖家多，join 商品表花的时间更长，那就让订单列表（Fact Table）和商品表都设置商品 ID 为 Distribution key。此时卖家表没有商品 ID 这一列，没法按照商品 ID 来分发，如果设置卖家 ID 为 Distribution key，那卖家的分布和商品的分布不同，就会涉及到比较多的通信，但考虑到卖家比较少，性能影响可能比较小。如果要很好的性能，那么卖家表可以设置为 ALL distribution style，那么每个 node 都有一份卖家，每个 slice 可以从本地找到卖家的信息，不需要额外的通信。对于 Sort key，由于订单列表和商品表需要在商品 ID 上进行 join，很自然地可以把商品 ID 设置为 sort key。订单列表和卖家表需要在卖家 ID 上进行 join，于是卖家表可以把卖家 ID 设置为 sort key。

## 常用的系统表

- [SVL_QLOG](https://docs.aws.amazon.com/redshift/latest/dg/r_SVL_QLOG.html)：记录了 SQL 查询日志
- [STV_BLOCKLIST](https://docs.aws.amazon.com/redshift/latest/dg/r_STV_BLOCKLIST.html)：记录了每个 1MB block 的信息
