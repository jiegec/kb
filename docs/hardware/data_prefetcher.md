# 数据预取器

## Offset Prefetcher

Offset Prefetch 是一类预取器，它的行为是，当访问地址为 X 的 cacheline 时，预取地址为 X + O 的 cacheline，其中 O 就是 Offset，可以是固定的，或者是动态学习出来的。

### Next Line Prefetcher

Next Line Prefetch 就是 O 恒等于 1 的 Offset Prefetcher，即总是预取下一个 cacheline。

代码参考 [ChampSim 实现](https://github.com/ChampSim/ChampSim/blob/master/prefetcher/next_line/next_line.cc)：

```c
champsim::block_number pf_addr{addr};
prefetch_line(champsim::address{pf_addr + 1}, true, metadata_in);
```

### Best Offset Prefetcher

Code: <https://github.com/gem5/gem5/blob/stable/src/mem/cache/prefetch/bop.cc>

[Best Offset Prefetcher](https://www.irisa.fr/alf/downloads/michaud/dpc2_michaud.pdf) 的思路是，在不同程序下，最优的 Offset 可能不一样，所以动态地计算出最佳的 Offset。思路如下：

1. 记录最近访问的若干个 cacheline 的地址 X 到 Recent Requests 表中
2. 当地址为 Y 的 cacheline 进入到缓存时，根据预先设好的若干个 Offset：O1、O2、...、On，计算 Y - Oi，判断它是不是在 Recent Requests 表中，如果在，就增加 Oi 的分数
3. 当某个 Offset 分数达到上限，或者到达一定的时间上限，就用当前学习到的分数最高的 Offset 去进行预取，然后分数清零，重新学习

相比固定 Offset 的 Offset Prefetcher，Best Offset Prefetcher 可以动态地找到该应用最适合的 Offset。

代码参考 [Gem5 实现](https://github.com/gem5/gem5/blob/stable/src/mem/cache/prefetch/bop.cc)：

记录访问历史到 Recent Requests 表：

```c
Addr addr = pfi.getAddr();
Addr tag_x = tag(addr);
insertIntoRR(addr, tag_x, RRWay::Left);
```

遍历预先设好的 Offset 列表，计算 Y - Oi 是否在 Recent Requests 表当中，是则增加对应 Oi 的分数：

```c
Addr offset_tag = (*offsetsListIterator).first;
Addr lookup_tag = tag((addr) - (offset_tag << lBlkSize));

if (testRR(lookup_tag)) {
    (*offsetsListIterator).second++;
    if ((*offsetsListIterator).second > bestScore) {
        bestScore = (*offsetsListIterator).second;
        phaseBestOffset = (*offsetsListIterator).first;
    }
}

offsetsListIterator++;
```

当某个 Offset 分数达到上限，或达到一定的时间上限，则选取此时分数最高的 Offset：

```c
if ((bestScore >= scoreMax) || (round >= roundMax)) {
    round = 0;

    if (bestScore > badScore) {
        bestOffset = phaseBestOffset;
        round = 0;
        issuePrefetchRequests = true;
    } else {
        issuePrefetchRequests = false;
    }

    resetScores();
    bestScore = 0;
    phaseBestOffset = 0;
}
```

然后用这个 Offset 去进行预取，在这里 Gem5 允许预取 X + O * I 的多个地址：

```c
if (issuePrefetchRequests) {
    for (int i = 1; i <= degree; i++) {
        Addr prefetch_addr = addr + ((i * bestOffset) << lBlkSize);
        addresses.push_back(AddrPriority(prefetch_addr, 0));
    }
}
```

### Berti (MICRO 版本)

[Berti: an Accurate Local-Delta Data Prefetcher](https://ieeexplore.ieee.org/document/9923806) 在 Best Offset Prefetcher 的基础上更进一步：Best Offset Prefetcher 认为不同程序的最佳 Offset 不同，所以要动态地寻找最佳的 Offset；而 Berti 认为，程序里不同 Load 指令的最佳 Offset 不同，所以要给不同的 Load 指令使用不同的最佳的 Offset。

此外，和 Best Offset Prefetcher 不同的是，Berti 没有一个预设的 Offset 列表，而是根据实际的 cacheline 地址去找到合适的 Offset。下面来看它具体是怎么做的。

首先，Berti 会给不同的 Load 指令的 PC 分别维护访问历史，也就是说，Best Offset Prefetcher 中的 Recent Requests 表在 Berti 这里就不是全局的了，而是需要给不同的 PC 维护不同的历史，在这里这个信息记录在 History Table 当中。

接着，Berti 会测量 L1D 缓存缺失的延迟，也就是从产生缺失到数据取回来花费的时间。那么，为了能够及时地预取数据，就需要保证预取的时刻，加上缓存缺失的延迟，还要早于在实际使用的时刻。由于 Berti 是一个 Offset Prefetcher，为了预取由某个 Load 指令访问的地址为 Y 的 cacheline，我们就需要找到由同一个 Load 指令在更早的时候访问地址为 X 的 cacheline，使得在访问 X 时预取 Y 是及时的。然后计算 Y - X 的差值，作为一个合适的 Offset。那么我们就知道，用这个 Offset 做预取是合理的，增加这个 Offset 对应的分数。最后，使用分数高的 Offset 来进行预取。

下面来看具体设计，Berti 采用 History Table 来记录访问历史，它是一个 16 路组相连的结构，但允许 tag 出现冲突，从而可以记录同一个 PC 对应的多个历史。每个 History Table 的表项记录由 Load 指令的 PC 哈希得到的 7-bit tag，某次访问的 24-bit cacheline 地址，以及一个 16-bit 时间戳。查询的时候，根据当前时间戳，减去缓存缺失延迟得到差值，找到时间戳小于差值的表项对应的 cacheline 地址，用于后续的 Offset 计算。

接着，是一个 16 路全相连的 Table of deltas 结构，它记录了不同 Load 指令，其最优的 16 种 Offset 的状态。具体地，Table of deltas 的表项包括：

- 10-bit 根据 Load 指令地址的 PC 哈希得到的 tag
- 4-bit 的 counter，记录该表项的更新次数
- 16 个 delta，每个 delta 包括：
    - 13-bit 的 delta 本身，就是 Offset
    - 4-bit 的 coverage，代表当前 Offset 能够覆盖多少比例的预取
    - 2-bit 的 status，代表当前 Offest 的状态，是否启动预取

当地址为 Y 的 cacheline 进入缓存时，往回找历史，从 History Table 中找到匹配的表项且时间戳足够早，计算地址的距离记为 delta，然后更新到 Table of deltas 当中：给 counter 加一，然后对于每个表项中记录的 delta，如果有匹配的 delta，则给它 coverage 加一。

当表项的更新次数累积达到 16 次，也就是 counter 字段溢出时，遍历 16 个 delta，如果它的 coverage 足够高，达到了 10，就标记它为可以预取，并且预取到 L1D 缓存；如果只有 5，就还是预取，但是只预取到 L2，因为不够精确；更低的话就不预取了。然后 counter 和 coverage 清零，进入新的一轮学习。

有了这些信息以后，就可以根据上述 Tables of delta 中学习到的状态，按照不同的 Offset 来进行预取了。

代码参考 [官方实现](https://github.com/gem5/gem5/blob/stable/src/mem/cache/prefetch/bop.cc)，在实现上述 History Table 和 Tables of delta 以外，为了记录L1D miss latency，还实现了 Latency Table 和 Shadow Cache，但在硬件中不需要这么麻烦，只需要在 L1D 中额外记录 miss 的时间戳，等 refill 的时候求差即可知道延迟。

### Berti (DPC-3 版本)

[Berti: A Per-Page Best-Request-Time Delta Prefetcher](https://dpc3.compas.cs.stonybrook.edu/pdfs/Berti.pdf) 在 DPC-3 比赛中的设计，与后来在 MICRO 上发表的设计不同，这里的 Berti 同时作为 L1D 和 L2 级别的 Prefetcher 出现，采用的是物理地址，因此相比使用虚拟地址的在 MICRO 上的 Berti 设计，DPC-3 版本的 Berti 额外引入了 Burst 机制，用来解决每个页开头的若干个 cacheline 无法找到更早的 cacheline 来触发 Offset Prefetch 的问题。

那么 DPC-3 版本的 Berti 记录了哪些信息呢：

1. 首先是一个 current pages 的表，记录了有哪些活跃的 page，对于每个 page，记录内部有哪些 cacheline 被访问过（类似 Spatial Memory Streaming 的做法），有哪些 delta 以及每个 delta 的分数（和 MICRO 版本的 Berti 一样），第一次访问该 page 的 PC 以及 offset（类似 Spatial Memory Streaming 的做法）
2. 然后是 recorded pages 表，当 current pages 的表项完成了学习，就会把表项移动到 recorded pages 当中
3. 此外还有一个 IP table，记录了对 page 产生第一次访问的 Load 指令的地址
4. 为了记录访存的延迟，维护 previous demand requests 表和 previous prefetch requests 表

实际预取的时候，就是两种模式：Burst 模式类似 Spatial Memory Streaming，但只把那些距离小于 delta 且之前访问过的 cacheline 取进来；Berti 模式类似 MICRO 版本，根据学习到的最佳 delta 来进行 Offset Prefetch。

## Spatial Prefetcher

Spatial Prefetcher 利用的是程序的访存模式在空间上的相似性，即程序对这一段内存的访存模式，可能会在另外很多段内存里以相同的模式重现。

### Spatial Memory Streaming

[Spatial Memory Streaming (SMS)](https://ieeexplore.ieee.org/document/1635957/) 的做法是，把内存分成很多个相同大小的 Region（通常一个 Region 是多个连续 Cacheline，例如 32 或 64 个 Cacheline），在第一次访问某个 Region 时，维护当前 Region 的信息，记录这次访存指令的 PC 以及访存的地址相对 Region 的偏移，然后开始跟踪这个 Region 内哪些数据被读取了，直到这个 Region 的数据被换出 Cache，就结束记录，把信息保存下来。当同一条访存指令访问到了任何一个 Region 内和之前一样的偏移时，根据之前保存的信息，把 Region 里曾经读过的地址预取一遍。这里的核心是只匹配偏移而不是完整的地址，忽略了地址的高位，最后预取的时候，也是拿新的 Region 的地址去加偏移，自然而然实现了空间上的平移。

具体来说，Spatial Memory Streaming 维护了一个 Active Generation Table（缩写 AGT）来记录上面所述的 Region 内哪些数据被读取的信息，当这个 Region 里的数据被换出 Cache，对应的信息就会被保存到 Pattern History Table（缩写 PHT）当中，后续会根据 PHT 来预测预取的地址。其中 Active Generation Table 又包括了 Accumulation Table 和 Filter Table，这样做是为了减少不必要的分配，只有当一个 Region 出现至少两次访问才会被分配到 Accmuluation Table 当中。具体步骤：

1. 当一个 Region 第一次被访问的时候，此时 Accumuation Table 还没有对应的表项，把访存的 PC 和 Region 内 offset 记录到 Filter Table 当中
2. 当一个 Region 第二次被访问的时候，此时 Filter Table 中应当有对应的表项，把表项挪到 Accumulation Table 当中，用 Bitmap 维护这个 Region 内哪些 Cacheline 被访问过的信息
3. 当一个 Region 内第三次或更多次被访问的时候，继续更新 Region 内哪些 Cacheline 被访问过的 Bitmap
4. 当 Region 内缓存被换出 Cache 时，认为这个 Region 已经学习完毕，把对应的信息移动到 Pattern History Table 中，注意此时 Region 地址信息不会被记录在 Pattern History Table 上，这样它就可以被用来预测多个 Region
5. 与此同时，查询 Pattern History Table，如果有 PC 和 offset 匹配的 entry，就按照 Bitmap 把 Region 内被访问过的 Cacheline 预取进来

Gem5 实现了 [Spartial Memory Stream 预取器](https://github.com/gem5/gem5/blob/stable/src/mem/cache/prefetch/sms.cc)，基本就是按照上面的思路实现的：

首先是计算出 Region 的地址以及 Region 内的 offset：

```c
Addr blk_addr = blockAddress(pfi.getAddr());
Addr pc = pfi.getPC();
Addr region_base = roundDown(blk_addr, Region_Size);
Addr offset = blk_addr - region_base;
```

接着，判断它是否在 Allocation Table 当中，如果是，说明已经访问了第三次或更多，把这次访问记录到 Bitmap 当中：

```c
if (AGT.find(region_base) != AGT.end()) {
    assert (FT.find(region_base) == FT.end());
    // Record Pattern
    AGT[region_base].insert(offset);
    // LRU omitted
}
```

如果不在 Allocation Table 当中，但是在 Filter Table 当中，说明这是 Region 内的第二次访问，把它从 Filter Table 挪到 Allocation Table，并更新 Bitmap：

```c
} else if (FT.find(region_base) != FT.end()) {
    //move entry from FT to AGT
    AGT[region_base].insert(FT[region_base].second);
    AGTPC[region_base] = FT[region_base];
    lruAGT.push_front(region_base);
    //Record latest offset
    AGT[region_base].insert(offset);
    //Recycle FT entry
    FT.erase(region_base);
    //Make space for next entry
    while (AGT.size() > Max_Contexts) {
        AGT.erase(lruAGT.back());
        AGTPC.erase(lruAGT.back());
        lruAGT.pop_back();
    }
}
```

如果在 Allocation Table 和 Filter Table 中都没有找到，那就在 Filter Table 中创建一个新的表项：

```c
} else {
    // Trigger Access
    FT[region_base] = std::make_pair (pc,offset);
    fifoFT.push_front(region_base);
    while (FT.size() > Max_Contexts) {
        FT.erase(fifoFT.back());
        fifoFT.pop_back();
    }
}
```

与此同时，检查 Pattern History Table 中有没有和当前访问匹配的表现，如果有，按照 Bitmap 来进行预取：

```c
//Prediction
std::pair <Addr, Addr> pc_offset = std::make_pair(pc,offset);
if (PHT.find(pc_offset) != PHT.end()) {
    for (std::set<Addr>::iterator it = PHT[pc_offset].begin();
        it != PHT[pc_offset].end(); it ++) {
        Addr pref_addr = blockAddress(region_base + (*it));
        addresses.push_back(AddrPriority(pref_addr,0));
    }
    // LRU omitted
}
```

另一方面，当缓存行从缓存中被 Evict 时，认为 Allocation Table 中对应的 Region 学习完成，移动到 Pattern History Table 当中：

```c
void
Sms::notifyEvict(const EvictionInfo &info)
{
    //Check if any active generation has ended
    Addr region_base = roundDown(info.addr, Region_Size);
    std::pair <Addr,Addr> pc_offset = AGTPC[region_base];
    if (AGT.find(region_base) != AGT.end()) {
        //remove old recording
        if (PHT.find(pc_offset) != PHT.end()) {
            PHT[pc_offset].clear();
        }
        //Move from AGT to PHT
        for (std::set<Addr>::iterator it = AGT[region_base].begin();
         it != AGT[region_base].end(); it ++) {
            PHT[pc_offset].insert(*it);
        }
        lruPHT.push_front(pc_offset);
    }

    while (PHT.size() > MAX_PHTSize) {
        PHT.erase(lruPHT.back());
        lruPHT.pop_back();
    }

    AGTPC.erase(region_base);
    AGT.erase(region_base);
}
```

