# Dijkstra 算法

Dijkstra 解决的是图上的单源最短路径问题（Single Source Shortest Path，SSSP）。

实现大致代码如下：

```python
def dijkstra(graph, source):
    Q = priority_queue()

    # initialize dist and Q
    dist[source] = 0
    for v in graph.vertices:
        if v != source:
            dist[v] = INF

        Q.add_with_priority(v, dist[v])

    while not Q.empty:
        # find min dist and relax edge
        u = Q.extract_min()

        for v in u.neighbors():
            # relax
            new_dist = dist[u] + u.dist_to(v)
            if new_dist < dist[v]:
                dist[v] = new_dist
                Q.decrease_priority(v, new_dist)
```

Q 是一个优先队列，队列每个元素都有优先级，支持如下操作：

1. `add_with_priority(element, priority)`：插入新元素
2. `empty()`：判断队列是否为空
3. `extract_min()`：从队列中删除优先级最低的元素并返回该元素
4. `decrease_priority()`：修改队列中特定元素的优先级，保证队列中没有重复元素

算法的时间复杂度是 $O(|E|T_{dp}+|V|T_{em})$，其中 $E$ 是边的集合，$V$ 是顶点的集合，$T_{dp}$ 是 `decrease_priority()` 的时间复杂度，$T_{em}$ 是 `extract_min()` 的时间复杂度。

根据优先队列的不同实现，得到不同的时间复杂度：

1. 用数组实现优先队列，则 $T_{dp}=O(1), T_{em}=O(|V|)$，因此时间复杂度是 $O(|E|+|V|^2)=O(|V|^2)$
2. 用平衡树或者堆实现优先队列，则 $T_{dp}=O(\log{|V|}), T_{em}=O(\log{|V|})$，算法总时间复杂度为 $O((|E|+|V|)\log{|V|})$
3. 用 Fibonacci 堆实现优先队列，则 $T_{dp}=O(1), T_{em}=O(\log{|V|})$，算法总时间复杂度为 $O(|E|+|V|\log{|V|})$

最近一篇论文 [A Randomized Algorithm for Single-Source Shortest Path on Undirected Real-Weighted Graphs](https://arxiv.org/pdf/2307.04139.pdf) 提出了 $O(|E|\sqrt{\log{|V|}\log{\log{|V|}}})$ 的 Dijkstra 变种算法。

参考了 [Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)。
