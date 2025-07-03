# 缓存替换策略

## LRU(Least Recently Used)

每个元素维护一个最后一次访问的时间。每次访问一个元素，就更新它最后一次访问的时间。替换的时候，选择最后一次访问的时间最早的那一个元素去替换。

为了优先替换非法元素，非法元素的访问时间视为比合法元素的访问时间都更早。

## PLRU(Pseudo Least Recently Used)

用二叉树来维护状态，叶子结点对应各元素，非叶子结点记录零或一，对应左子数或右子树，指向的是访问时间更早的子树。当访问元素时，把从根结点到元素对应的叶子结点路径上的非叶子结点都指向不在路径的一侧。替换的时候，沿着非叶子结点上记录的方向，一路走到的叶子结点，该结点对应要替换的元素。

## MRU(Most Recently Used)

每个元素维护一个最后一次访问的时间。每次访问一个元素，就更新它最后一次访问的时间。替换的时候，选择最后一次访问的时间最晚的那一个元素去替换。

为了优先替换非法元素，特别地，如果有非法元素，那么就优先替换非法元素。

## LFU(Least Frequently Used)

每个元素维护一个访问次数。每次访问一个元素，就增加一次它的访问次数。替换的时候，选择最访问次数最小的那一个元素去替换。

为了优先替换非法元素，非法元素的访问次数视为零。

## Random

替换的时候，随机选择一个合法元素去替换。

为了优先替换非法元素，特别地，如果有非法元素，那么就优先替非法元素。

## RRIP(Re-Reference Interval Prediction)

论文：[High Performance Cache Replacement Using Re-Reference Interval Prediction (RRIP)](https://people.csail.mit.edu/emer/media/papers/2010.06.isca.rrip.pdf)

每个元素维护一个 RRPV（Re-Reference Prediction Value）值。当元素被换入时，它的 RRPV 设置为比较大的值。当元素被访问时，它的 RRPV 被设置为零（Hit Priority 方式）或者减去一（Frequency Priority 方式）。

替换的时候，给所有元素的 RRPV 值不断同时加一，直到有一个元素的 RRPV 值等于 maxRRPV（RRPV 可能设置的最大值），此时它就是被替换的元素。等价地说，RRPV 最大的元素就是要被替换的元素，同时增加其余元素的 RRPV 值，增加的值，等于 maxRRPV，减去被替换的元素的 RRPV 值。

为了优先替换非法元素，特别地，如果有非法元素，那么就优先替非法元素。

### SRRIP(Static RRIP)

RRIP 的一种特殊情况：当元素被换入时，它的 RRPV 值设置为 maxRRPV-1。

### BRRIP(Bimodel RRIP)

RRIP 的一种特殊情况：当元素被换入时，按照一定的概率，把它的 RRPV 值设置为 maxRRPV 或 maxRRPV-1。

### NRU(Not Recently Used)

SRRIP 的一种特殊情况：RRPV 只能设置为零或者一；当元素被换入时，RRPV 设置为零。

等价地说：当元素被换入时，RRPV 设置为零。当元素被访问时，RRPV 设置为零。在替换时，如果有 RRPV 等于一的元素，则替换它；如果所有元素的 RRPV 都等于零，则替换其中一个元素，并把剩下的元素的 RRPV 都设置为一。
