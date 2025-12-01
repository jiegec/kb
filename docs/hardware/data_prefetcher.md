# 数据预取器

## Offset Prefetcher

Offset Prefetcher 是一类预取器，它的行为是，当访问地址为 X 的 cacheline 时，预取地址为 X + O 的 cacheline，其中 O 就是 Offset，可以是固定的，或者是动态学习出来的。

如果采用一个 Offset 去预取 `X + O`, `X + O * 2`, ...，那么这种 Offset Prefetcher 也叫 Stride Prefetcher，针对的是数组的访存模式，由于数组的元素大小是固定的，那么访存地址通常满足 `X`, `X+Stride`, `X+2*Stride`, ... 的规律。

### Next Line Prefetcher

Next Line Prefetch 就是 O 恒等于 1 的 Offset Prefetcher，即总是预取下一个 cacheline。

代码参考 [ChampSim 实现](https://github.com/ChampSim/ChampSim/blob/master/prefetcher/next_line/next_line.cc)：

```c
champsim::block_number pf_addr{addr};
prefetch_line(champsim::address{pf_addr + 1}, true, metadata_in);
```

### IP Stride Prefetcher

[IP Stride Prefetcher](https://dl.acm.org/doi/10.1145/358923.358939) 是一种根据 Load 指令的地址进行跟踪的 Stride Prefetcher：它维护了一个 Reference Prediction Table，使用 Load 指令的地址进行索引，表项维护两个信息：最后一次访问的 cacheline 地址和当前的 stride。其工作过程如下：

- 当 Load 指令第一次访问的时候，在 Reference Prediction Table 中分别新的表项，记录它的访问地址，stride 还没有学习到，置为 0
- 当 Load 指令第二次访问的时候，计算访问地址和记录在 Reference Prediction Table 中上一次访问地址的差值，写入到 stride 当中，同时更新访问地址
- 当 Load 指令第三次访问的时候，再次计算访问地址和上一次访问地址的差值，如果差值等于记录的 stride，就启动 stride prefetcher

代码实现可参考 [ChampSim](https://github.com/ChampSim/ChampSim/blob/master/prefetcher/ip_stride/ip_stride.cc)：

检查当前 Load 指令的 PC 是否已经在 Reference Prediction Table 当中：

```c
champsim::block_number cl_addr{addr};
champsim::block_number::difference_type stride = 0;

auto found = table.check_hit({ip, cl_addr, stride});
```

如果在，计算一下访问地址减去上一次访问地址的差值，和已有的 stride 比对，如果相等且不为 0，启动预取：

```c
// if we found a matching entry
if (found.has_value()) {
    stride = champsim::offset(found->last_cl_addr, cl_addr);

    // Initialize prefetch state unless we somehow saw the same address twice in
    // a row or if this is the first time we've seen this stride
    if (stride != 0 && stride == found->last_stride)
        active_lookahead = {champsim::address{cl_addr}, stride, PREFETCH_DEGREE};
}

// update tracking set
table.fill({ip, cl_addr, stride});
```

另一方面，启动预取，把 `Y+Stride*i` 的数据预取进来：

```c

void ip_stride::prefetcher_cycle_operate()
{
    // If a lookahead is active
    if (active_lookahead.has_value()) {
        auto [old_pf_address, stride, degree] = active_lookahead.value();
        assert(degree > 0);

        champsim::address pf_address{champsim::block_number{old_pf_address} + stride};

        // If the next step would exceed the degree or run off the page, stop
        if (intern_->virtual_prefetch || champsim::page_number{pf_address} == champsim::page_number{old_pf_address}) {
            // check the MSHR occupancy to decide if we're going to prefetch to this level or not
            const bool mshr_under_light_load = intern_->get_mshr_occupancy_ratio() < 0.5;
            const bool success = prefetch_line(pf_address, mshr_under_light_load, 0);
            if (success)
                active_lookahead = {pf_address, stride, degree - 1};
            // If we fail, try again next cycle

            if (active_lookahead->degree == 0) {
                active_lookahead.reset();
            }
        } else {
            active_lookahead.reset();
        }
    }
}
```

### Best Offset Prefetcher

Code: <https://github.com/gem5/gem5/blob/stable/src/mem/cache/prefetch/bop.cc>

[Best Offset Prefetcher (BOP, DPC-2)](https://www.irisa.fr/alf/downloads/michaud/dpc2_michaud.pdf) 的思路是，在不同程序下，最优的 Offset 可能不一样，所以动态地计算出最佳的 Offset。思路如下：

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

然后用这个 Offset 去进行预取，在这里 Gem5 允许预取 X + O * I 的多个地址，但通常 degree 就是 1：

```c
if (issuePrefetchRequests) {
    for (int i = 1; i <= degree; i++) {
        Addr prefetch_addr = addr + ((i * bestOffset) << lBlkSize);
        addresses.push_back(AddrPriority(prefetch_addr, 0));
    }
}
```

### Multi-Lookahead Offset Prefetching

[Multi-Lookahead Offset Prefetching (MLOP, DPC-3)](https://dpc3.compas.cs.stonybrook.edu/pdfs/Multi_lookahead.pdf) 是一种在 Best Offset Prefetcher 的基础上的改进：Best Offset Prefetcher 会按照固定的 Offset 序列，给 Offset 打分：访问 Y 的时候，如果 Y-Offset 在最近的访问序列中，就给 Offset 加分。然后用最高分的 Offset 去进行预取。Multi-Lookahead Offset Prefetching 的思路是，有时候单独一个最佳的 Offset 不够，而是设置不同的 Lookahead 等级：Lookahead 等级为几，就代表跳过了最近的几个访问序列；然后对每个 Lookahead 等级都去计算一个最佳的 Offset，用这些 Offset 去预取。其实就相当于，Best Offset Prefetcher 用完整的最近访问序列去计算分数，而在这里，会按照 Lookahead 等级来忽略最后几次访问，再去计算最佳的 Offset，这样算出来的 Offset 它预取的时间距离更远

### Berti (MICRO 版本)

[Berti: an Accurate Local-Delta Data Prefetcher (MICRO-55)](https://ieeexplore.ieee.org/document/9923806) 在 Best Offset Prefetcher 的基础上更进一步：Best Offset Prefetcher 认为不同程序的最佳 Offset 不同，所以要动态地寻找最佳的 Offset；而 Berti 认为，程序里不同 Load 指令的最佳 Offset 不同，所以要给不同的 Load 指令使用不同的最佳的 Offset。

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

代码参考 [官方实现](https://github.com/agusnt/Berti-Artifact)，在实现上述 History Table 和 Tables of delta 以外，为了记录 L1D miss latency，还实现了 Latency Table 和 Shadow Cache，但在硬件中不需要这么麻烦，只需要在 L1D 中额外记录 miss 的时间戳，等 refill 的时候求差即可知道延迟。

### Berti (DPC-3 版本)

[Berti: A Per-Page Best-Request-Time Delta Prefetcher (DPC-3)](https://dpc3.compas.cs.stonybrook.edu/pdfs/Berti.pdf) 在 DPC-3 比赛中的设计，与后来在 MICRO 上发表的设计不同，这里的 Berti 同时作为 L1D 和 L2 级别的 Prefetcher 出现，采用的是物理地址，因此相比使用虚拟地址的在 MICRO 上的 Berti 设计，DPC-3 版本的 Berti 额外引入了 Burst 机制，用来解决每个页开头的若干个 cacheline 无法找到更早的 cacheline 来触发 Offset Prefetch 的问题。

那么 DPC-3 版本的 Berti 记录了哪些信息呢：

1. 首先是一个 current pages 的表，记录了有哪些活跃的 page，对于每个 page，记录内部有哪些 cacheline 被访问过（类似 Spatial Memory Streaming 的做法），有哪些 delta 以及每个 delta 的分数（和 MICRO 版本的 Berti 一样），第一次访问该 page 的 PC 以及 offset（类似 Spatial Memory Streaming 的做法）
2. 然后是 recorded pages 表，当 current pages 的表项完成了学习，就会把表项移动到 recorded pages 当中
3. 此外还有一个 IP table，记录了对 page 产生第一次访问的 Load 指令的地址
4. 为了记录访存的延迟，维护 previous demand requests 表和 previous prefetch requests 表

实际预取的时候，就是两种模式：Burst 模式类似 Spatial Memory Streaming，但只把那些距离小于 delta 且之前访问过的 cacheline 取进来；Berti 模式类似 MICRO 版本，根据学习到的最佳 delta 来进行 Offset Prefetch。

### Signature Path Prefetcher

[Path Confidence based Lookahead Prefetching (MICRO-49)](https://ieeexplore.ieee.org/document/7783763) 提出了一种 Signature Path Prefetcher（SPP），其借用了分支预测的思路，把访存的地址进行差分，得到一个 delta 序列，然后对 delta 序列进行预测：把 delta 的序列折叠成一个 signature，然后用 signature 去访问 Pattern Table，提供下一个 delta 是多少的预测。其思路和后面的 Variable Length Delta Predictor 类似。

它包括一个 Signature Table，它根据 Page 进行索引，维护在同一个 Page 内的访问的 signature 和最后一次访问的 offset：当对这个 Page 进行一次新的访问时，用当前访问的 offset 减去最后一次的 offset，然后哈希到 signature 当中，同时更新最后一次访问的 offset。

它还包括一个 Pattern Table，它针对 Signature 和下一次访问的 delta，维护 confidence 信息。在预取的时候，根据 Signature，找到 confidence 最高的那个 delta，计算出新的 Signature，再去查询 Pattern Table，循环若干次，直到 confidence 足够低或者达到一定的预取深度。

代码实现可参考 [ChampSim](https://github.com/ChampSim/ChampSim/blob/master/prefetcher/spp_dev/spp_dev.cc)。

### Pythia

[Pythia](https://dl.acm.org/doi/10.1145/3466752.3480114) 是一种基于 Reinforcement Learning 的 Offset Prefetcher。强化学习（Reinforcement Learning）的概念是，智能体 Agent 感知状态 State，输出动作 Action，得到奖励 Reward，目标是长期的奖励最大。在这里，Action 就是决定 Offset Prefetcher 预取所采用的 Offset。Q 函数输入是 State 和 Action，输出预测的 Reward 值，所以强化学习要做的事情就是找到一个很精确的 Q 函数的近似，然后根据学习到的 Q 函数来选择 Action。Reward 则是根据预取器的效果来取值：

1. Accurate and timely：预取进到缓存的数据被访问了
2. Accurate but late：预取的数据在还没预取完成的时候就被访问了，这意味着预取准确，但是不够早
3. Loss of coverage：预取的地址超出了页边界，因为采用的是物理地址，所以预取失败
4. Inaccurate：预取的数据没有被访问过，说明预取了错误的数据
5. No-prefetch：不进行预取

在论文中，Accurate and timely 会给 20 的 Reward，Accurate but late 给 12 的 Reward，这两种是希望发生的；Loss of coverage 给 -12 的 Reward，Incorrect 给 -8 或 -14（内存带宽占用率高）的 Reward，No-prefetch 给 -4 或 -2（内存带宽占用率高）的 Reward。优化目标就是要找到 Action（即 Offset）实现最高的 Reward。可以看到，当内存带宽占用率高的时候，给错误的预取更大的惩罚，也允许不做预取。

[论文](https://arxiv.org/pdf/2109.12021)中的伪代码如下：

![](./data_prefetcher_pythia.png)

1. 用 EQ（Evaluation Queue）维护 Prefetch 历史
2. 当 LSU 读取某个 Cacheline 的时候，查询它的地址是否在 EQ 当中，如果是，且这个 Cacheline 命中，给一个 Accurate and timely 的 Reward；如果在 EQ 当中但 Cacheline 缺失，给一个 Accurate but late 的 Reward
3. 预取的时候，根据当前的 State，找到最好的 Action 使得对应的 Q 值最大（小的概率选择随机 Action），用这个 Action 作为 Offset 来进行预取；然后把这次预取的信息插入到 EQ 当中
4. 如果 Action 等于 0，即没有要预取的数据，给一个 No prefetch 的 Reward；如果要预取的地址超出物理页边界，给一个 Loss of coverage 的 Reward
5. 按照 SARSA 方式更新从 EQ evict 出来的 entry 的 Q 值

代码实现可参考 [CMU-SAFARI/Pythia](https://github.com/CMU-SAFARI/Pythia/)。

## Spatial Prefetcher

Spatial Prefetcher 利用的是程序的访存模式在空间上的相似性，即程序对这一段内存的访存模式，可能会在另外很多段内存里以相同的模式重现。

### Spatial Memory Streaming

[Spatial Memory Streaming (SMS, ISCA '06)](https://ieeexplore.ieee.org/document/1635957/) 的做法是，把内存分成很多个相同大小的 Region（通常一个 Region 是多个连续 Cacheline，例如 32 或 64 个 Cacheline），在第一次访问某个 Region 时，维护当前 Region 的信息，记录这次访存指令的 PC 以及访存的地址相对 Region 的偏移，然后开始跟踪这个 Region 内哪些数据被读取了，直到这个 Region 的数据被换出 Cache，就结束记录，把信息保存下来。当同一条访存指令访问到了任何一个 Region 内和之前一样的偏移时，根据之前保存的信息，把 Region 里曾经读过的地址预取一遍。这里的核心是只匹配偏移而不是完整的地址，忽略了地址的高位，最后预取的时候，也是拿新的 Region 的地址去加偏移，自然而然实现了空间上的平移。

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

### Bingo

[Bingo Spatial Prefetcher](https://ieeexplore.ieee.org/document/8675188/) 在 Spatial Memory Streaming 的基础上做了改进：Spatial Memory Streaming 用的是 Load 指令的地址和 Region 内的 Offset 作为索引，去访问 Bitmap 信息，然后用 Bitmap 去预取 Region 内的被访问过的 cacheline。Bingo 的思路是，有些时候用 Load 指令的地址和 Region 内 Offset 作为索引不够精确，而如果用 Load 指令的地址和完整的 Load 地址作为索引会更加精确。

因此 Bingo 的思路是，先用 Load 指令的地址加完整的 Load 地址去查询，如果有匹配的，就直接预取；如果没有匹配的，再用 Load 指令的地址加 Load 地址在 Region 内的 Offset 去查询，此时就和 Spatial Memory Streaming 一致了。为了在不增加太多开销的前提下实现这个查询，它把 Region 内的 Offset 作为 index，Region 外的 Load 地址部分参与到 tag 当中，那么要做的事情就变成，访问同一个 set 内的多个 way，如果有某个 way 的 tag 匹配，则优先用匹配的（相当于 Load 指令的地址加完整的 Load 地址去查询），否则就可以用其他的（相当于用 Load 指令的地址加 Region 内的 Offset 去查询）。

这个匹配逻辑见 [Bingo 在 DPC-3 上的源码](https://dpc3.compas.cs.stonybrook.edu/src/Accurately.zip)：

```cpp
/**
 * First searches for a PC+Address match. If no match is found, returns all PC+Offset matches.
 * @return All un-rotated patterns if matches were found, returns an empty vector otherwise
 */
vector<vector<bool>> find(uint64_t pc, uint64_t address) {
    if (this->debug_level >= 2)
        cerr << "PatternHistoryTable::find(pc=0x" << hex << pc << ", address=0x" << address << ")" << dec << endl;
    uint64_t key = this->build_key(pc, address);
    uint64_t index = key % this->num_sets;
    uint64_t tag = key / this->num_sets;
    auto &set = this->entries[index];
    uint64_t min_tag_mask = (1 << (this->pc_width + this->min_addr_width - this->index_len)) - 1;
    uint64_t max_tag_mask = (1 << (this->pc_width + this->max_addr_width - this->index_len)) - 1;
    vector<vector<bool>> matches;
    this->last_event = MISS;
    for (int i = 0; i < this->num_ways; i += 1) {
        if (!set[i].valid)
            continue;
        bool min_match = ((set[i].tag & min_tag_mask) == (tag & min_tag_mask));
        bool max_match = ((set[i].tag & max_tag_mask) == (tag & max_tag_mask));
        vector<bool> &cur_pattern = set[i].data.pattern;
        if (max_match) {
            this->last_event = PC_ADDRESS;
            Super::set_mru(set[i].key);
            matches.clear();
            matches.push_back(cur_pattern);
            break;
        }
        if (min_match) {
            this->last_event = PC_OFFSET;
            matches.push_back(cur_pattern);
        }
    }
    int offset = address % this->pattern_len;
    for (int i = 0; i < (int)matches.size(); i += 1)
        matches[i] = my_rotate(matches[i], +offset);
    return matches;
}
```

### Pattern Merging Prefetcher

[Pattern Merging Perfetcher (PMP, MICRO-55)](https://ieeexplore.ieee.org/document/9923831) 也是一个 Spatial Prefetcher，它的思路是，很多 Spatial Pattern 是类似的，但保存了很多份，所以它希望通过合并 Pattern（类似 SMS 里面的那个 Bitmap）来节省空间。合并思路是这样的：

1. 把 Bitmap 进行旋转移位，使得 Trigger Access 对应的 Bit 挪到开头
2. 用 Counter Vector 代替 Bitmap，每一个位置记录一个数而不再是 0/1，合并 Bitmap 时，将旋转移位后的 Bitmap 求和到 Counter Vector 当中
3. 根据 Counter Vector 的值：计算 Counter 除以 Trigger Access 的 Counter，即这一个 Cacheline 的出现频率，根据频率决定哪些 Cacheline 预取到 L1 或 L2

实现参考它的[代码](https://github.com/zeal4u/PMP/blob/main/prefetcher/pmp.l1d_pref)：

```c++
// step 1: rotate
int offset = __coarse_offset(__fine_offset(address));
offset = is_degrade ? offset / PATTERN_DEGRADE_LEVEL : offset;
pattern = my_rotate(pattern, -offset);

if (entry)
{
    // step 2: added to stored pattern
    int max_value = 0;
    auto &stored_pattern = entry->data.pattern; 
    for (int i = 0; i < this->pattern_len; i++)
    {
        pattern[i] ? ADD(stored_pattern[i], max_conf) : 0;
        if (i > 0 && max_value < stored_pattern[i]) {
            max_value = stored_pattern[i];
        }
    }

    // handle overflow
    if (entry->data.pattern[0] == max_conf) {
        if (max_value < (1 << BACKOFF_TIMES)) {
            entry->data.pattern[0] = max_value;
        }
        else 
            for (auto &e : stored_pattern) {
                e >>= BACKOFF_TIMES;
            }
    }
    Super::rp_promote(key);
}

// step 3: prefetch based on frequency
int cnt = 0;
for (int j = 0; j < n; j += 1)
{
    cnt += x[j].pattern[i];
}
double p = 1.0 * cnt / x[0].pattern[0];
if (p > 1) {
    cout << "cnt:" << cnt << ",total:" << x[0].pattern[0] << endl;
    assert(p <= 1);
}

if (x[0].pattern[0] <= START_CONF) {
    break;
}

if (p >= PC_L1D_THRESH)
    res[i] = FILL_L1;
else if (p >= PC_L2C_THRESH)
    res[i] = FILL_L2;
else if (p >= PC_LLC_THRESH)
    res[i] = FILL_LLC;
else
    res[i] = 0;
```

此外，它根据 Offset 和 PC 分别进行预测，对应 Offset Pattern Table 和 PC Pattern Table。

### Variable Length Delta Prefetcher

[Variable Length Delta Prefetcher (VLDP, MICRO-48)](https://ieeexplore.ieee.org/document/7856594) 是一种基于 delta 预测的 Spatial Prefetcher，具体地，它对访存序列求差分，即用第 k 次访存地址减去第 k-1 次访存地址，得到 Delta 序列，然后对当前的 Delta 序列，预测下一个 Delta，那么预取的地址，就是 Delta 加上最后一次访存的地址。它的实现思路是：

- 在 Delta History Buffer 中对每个物理页分别保存物理页号，最后一次访问地址的偏移，最近的最多四个 Delta 值，最近一次用了哪个表来做预测，这个页面被访问多少次，以及最近四次预取的 offset
- 当程序第一次访问某个物理页时，在 Delta History Buffer 中创建表项，同时根据访问的页内偏移，查询 Offset Prediction Table，得到预取的距离，进行预取
- 当程序第二次访问某个物理页时，根据 Delta History Buffer 中保存的信息，得到这两次访问的偏移的差值 Delta，然后用这个 Delta 去访问第一个 Delta Prediction Table，即用一个 Delta 预测下一个 Delta
- 当程序第三次访问时，用前两个 Delta 访问第二个 Delta Prediction Table，预测第三个 Delta；第四次访问时，用前三个 Delta 访问第三个 Delta Prediction Table，预测第四个 Delta；依此类推

与 Signature Path Prefetcher 把 Delta 序列压缩为 Signature 不同，Variable Length Delta Prefetcher 用的是完整的最多四个 Delta 序列来进行预测。

## Temporal Prefetcher

### Irregular Stream Buffer

[Irregular Stream Buffer (ISB, MICRO-46)](https://dl.acm.org/doi/10.1145/2540708.2540730) 是一种 Temporal Prefetcher，它可以把时间上连续的若干个地址联系起来，实现一些不规则访问的预取。它的思路是，把不连续的物理地址，映射到一个连续的地址空间（称其中的地址为 Structural Address），那么预取的时候，就可以在这个连续的地址空间内连续地取地址，再反查对应的物理地址。其原理如下：

1. 维护一个 Training Unit，记录每个 Load PC 最后一次 Load 的物理地址
2. 维护一个 Physical to Structural Address Mapping Cache（PS-AMC），记录物理地址到 Structural Address 的映射；具体地，当执行 Load 指令时：
    1. 检查 Training Unit，如果没有表项，则初始化，记录第一次 Load 的物理地址
    2. 如果已有表项，查询最后一次 Load 的物理地址，记为 A；当前 Load 指令访问的物理地址，记为 B；在 PS-AMC 中分别查询 A 和 B
    3. 如果 A 和 B 都不在 PS-AMC 中，则给它们分配两个连续的 Structural Address，记录在 PS-AMC 当中
    4. 如果 A 在 PS-AMC 当中而 B 不在，给 B 的 Structural Address 设置为 A 的 Structural Address 加一
    5. 如果 A 和 B 都在 PS-AMC 当中，如果它们的 Structural Address 已经是连续的，就增加 Confidence，否则减少 Confidence；如果 Confidence 减到了 0，则给 B 的 Structural Address 设置为 A 的 Structural Address 加一
3. 同时维护一个 Structural to Physical Address Mapping Cache（SP-AMC），记录 Structural Address 到物理地址的映射

要预取的时候，根据物理地址，查询 PS-AMC，找到它的 Structural Address，计算它的后续 Structural Address，然后反查 SP-AMC 从而得到要预取的物理地址。

由于片上空间有限，它设计了一个基于 TLB 的换入换出机制，同时利用 TLB 来节省物理地址的存储。

### Managed Irregular Stream Buffer

[Managed Irregular Stream Buffer (MISB, ISCA '19)](https://dl.acm.org/doi/10.1145/3307650.3322225) 是针对 Irregular Stream Buffer (ISB) 的改进：

1. 管理 Structural Address 和 Physical Address 之间映射的粒度从页缩小到了缓存行
2. 实现 Metadata Prefetching，根据 Structural Address 的连续性提前把 off chip 当中的信息预取到 on chip
3. 通过 Bloom Filter 减少无用的 Metadata 内存请求

## Other Prefetcher

有的 Prefetcher 集合了多种 Prefetcher 于一体，可以支持多种不同的访存模式。

### Instruction Pointer Classifier based Prefetching

[Instruction Pointer Classifier based Prefetching (IPCP, DPC-3)](https://dpc3.compas.cs.stonybrook.edu/pdfs/Bouquet.pdf) 在 IP-stride Prefetch 的基础上，支持了更多的访存模式：

- IP Constant Stride(CS)，和前面提到的 IP-stride Prefetch 一样，从某个地址开始，按照固定的 stride 进行访问
- IP Complex Stride(CPLX)，思路是根据 stride 历史来预测下一个 stride 是多少，可以支持不固定但有规律的 stride，类似前面提到的 Signature Path Prefetching
- IP Global Stream(GS)，就是和 Load 指令无关，但是从全局来看，是访问连续的 cacheline，对应 Stream Prefetcher

具体来说，维护了一个 IP table，使用 Load 指令的地址来索引，它的表项包括：

- 6-bit 的 tag
- 1-bit 的 valid
- 针对 IP Constant Stride，记录：
    - 52-bit 的 page 地址
    - 6-bit 的 page 内 cacheline offset
    - 7-bit 的 last stride，记录最后两次访存地址的差值
    - 2-bit 的 confidence
- 针对 IP Complex Stride，记录：
    - 12-bit 的 signature，是最近若干次 stride 经过哈希的结果
- 针对 IP Global Stream，记录：
    - 1-bit 的 stream valid，表示是否为合法的 Stream
    - 1-bit 的 stream direction，表示向地址更高的方向还是向地址更低的方向
    - 1-bit 的 strength

下面来结合[代码](https://dpc3.compas.cs.stonybrook.edu/src/Bouquet.zip) 来分析一下：

首先是 IP Constant Stride 的部分，计算和上一次访存地址的差值：

```c
// calculate the stride between the current address and the last address
int64_t stride = 0;
if (cl_offset > trackers_l1[cpu][index].last_cl_offset)
    stride = cl_offset - trackers_l1[cpu][index].last_cl_offset;
else {
    stride = trackers_l1[cpu][index].last_cl_offset - cl_offset;
    stride *= -1;
}

// don't do anything if same address is seen twice in a row
if (stride == 0)
    return;
```

如果和之前的结果一致，就增加 confidence，反之减少：

```c
int update_conf(int stride, int pred_stride, int conf){
    if(stride == pred_stride){             // use 2-bit saturating counter for confidence
        conf++;
        if(conf > 3)
            conf = 3;
    } else {
        conf--;
        if(conf < 0)
            conf = 0;
    }

    return conf;
}

// update constant stride(CS) confidence
trackers_l1[cpu][index].conf = update_conf(stride, trackers_l1[cpu][index].last_stride, trackers_l1[cpu][index].conf);

// update CS only if confidence is zero
if(trackers_l1[cpu][index].conf == 0)                      
    trackers_l1[cpu][index].last_stride = stride;
```

如果 confidence 大于 1 且 stride 不等于 0，则继续往后预取：

```c
if(trackers_l1[cpu][index].conf > 1 && trackers_l1[cpu][index].last_stride != 0){            // CS IP  
    for (int i=0; i<prefetch_degree; i++) {
        uint64_t pf_address = (cl_addr + (trackers_l1[cpu][index].last_stride*(i+1))) << LOG2_BLOCK_SIZE;

        // Check if prefetch address is in same 4 KB page
        if ((pf_address >> LOG2_PAGE_SIZE) != (addr >> LOG2_PAGE_SIZE)){
            break;
        }

        metadata = encode_metadata(trackers_l1[cpu][index].last_stride, CS_TYPE, spec_nl[cpu]);
        prefetch_line(ip, addr, pf_address, FILL_L1, metadata);
        num_prefs++;
        SIG_DP(cout << trackers_l1[cpu][index].last_stride << ", ");
    }
}
```

接下来看 IP Complex Stride。它的思路是，计算 stride 序列，通过哈希得到一个 signature，然后用 signature 去预测下一个 delta 是多少，和分支预测是类似的。首先是 signature 的计算：

```c
uint16_t update_sig_l1(uint16_t old_sig, int delta){                           
    uint16_t new_sig = 0;
    int sig_delta = 0;

    // 7-bit sign magnitude form, since we need to track deltas from +63 to -63
    sig_delta = (delta < 0) ? (((-1) * delta) + (1 << 6)) : delta;
    new_sig = ((old_sig << 1) ^ sig_delta) & 0xFFF;                     // 12-bit signature

    return new_sig;
}

// calculate and update new signature in IP table
signature = update_sig_l1(last_signature, stride);
trackers_l1[cpu][index].signature = signature;
```

使用 signature 去访问 Delta Prediction Table，它的表项是 delta 和 confidence：

```cpp
class DELTA_PRED_TABLE {
public:
    int delta;
    int conf;

    DELTA_PRED_TABLE () {
        delta = 0;
        conf = 0;
    };        
};
```

如果 confidence 非负，就用它预测的 delta 来进行预取：

```c
if(DPT_l1[cpu][signature].conf >= 0 && DPT_l1[cpu][signature].delta != 0) {  // if conf>=0, continue looking for delta
    int pref_offset = 0,i=0;                                                        // CPLX IP
    for (i=0; i<prefetch_degree; i++) {
        pref_offset += DPT_l1[cpu][signature].delta;
        uint64_t pf_address = ((cl_addr + pref_offset) << LOG2_BLOCK_SIZE);

        // Check if prefetch address is in same 4 KB page
        if (((pf_address >> LOG2_PAGE_SIZE) != (addr >> LOG2_PAGE_SIZE)) || 
                (DPT_l1[cpu][signature].conf == -1) ||
                (DPT_l1[cpu][signature].delta == 0)){
            // if new entry in DPT or delta is zero, break
            break;
        }

        // we are not prefetching at L2 for CPLX type, so encode delta as 0
        metadata = encode_metadata(0, CPLX_TYPE, spec_nl[cpu]);
        if(DPT_l1[cpu][signature].conf > 0){                                 // prefetch only when conf>0 for CPLX
            prefetch_line(ip, addr, pf_address, FILL_L1, metadata);
            num_prefs++;
            SIG_DP(cout << pref_offset << ", ");
        }
        signature = update_sig_l1(signature, DPT_l1[cpu][signature].delta);
    }
} 
```

根据 signature 和当前的 delta，更新 Delta Prediction Table：

```c
// update complex stride(CPLX) confidence
DPT_l1[cpu][last_signature].conf = update_conf(stride, DPT_l1[cpu][last_signature].delta, DPT_l1[cpu][last_signature].conf);

// update CPLX only if confidence is zero
if(DPT_l1[cpu][last_signature].conf == 0)
    DPT_l1[cpu][last_signature].delta = stride;
```

最后是 IP Global Stream，它使用 Global History Buffer 记录了全局的若干次 cacheline 访问：

```c
// update GHB
// search for matching cl addr
int ghb_index=0;
for(ghb_index = 0; ghb_index < NUM_GHB_ENTRIES; ghb_index++)
    if(cl_addr == ghb_l1[cpu][ghb_index])
        break;
// only update the GHB upon finding a new cl address
if(ghb_index == NUM_GHB_ENTRIES){
    for(ghb_index=NUM_GHB_ENTRIES-1; ghb_index>0; ghb_index--)
        ghb_l1[cpu][ghb_index] = ghb_l1[cpu][ghb_index-1];
    ghb_l1[cpu][0] = cl_addr;
}
```

检测当前访问往低地址或者高地址的连续若干个 cacheline 是不是都在 GHB 当中，是的话激活 IP Global Stream 模式：

```c
void check_for_stream_l1(int index, uint64_t cl_addr, uint8_t cpu){
    int pos_count=0, neg_count=0, count=0;
    uint64_t check_addr = cl_addr;

    // check for +ve stream
    for(int i=0; i<NUM_GHB_ENTRIES; i++){
        check_addr--;
        for(int j=0; j<NUM_GHB_ENTRIES; j++)
            if(check_addr == ghb_l1[cpu][j]){
                pos_count++;
                break;
            }
    }

    check_addr = cl_addr;
    // check for -ve stream
    for(int i=0; i<NUM_GHB_ENTRIES; i++){
        check_addr++;
        for(int j=0; j<NUM_GHB_ENTRIES; j++)
            if(check_addr == ghb_l1[cpu][j]){
                neg_count++;
                break;
            }
    }

    if(pos_count > neg_count){                                // stream direction is +ve
        trackers_l1[cpu][index].str_dir = 1;
        count = pos_count;
    }
    else{                                                     // stream direction is -ve
        trackers_l1[cpu][index].str_dir = 0;
        count = neg_count;
    }

    if(count > NUM_GHB_ENTRIES/2){                                // stream is detected
        trackers_l1[cpu][index].str_valid = 1;
        if(count >= (NUM_GHB_ENTRIES*3)/4)                        // stream is classified as strong if more than 3/4th entries belong to stream
            trackers_l1[cpu][index].str_strength = 1;
    }
    else{
        if(trackers_l1[cpu][index].str_strength == 0)             // if identified as weak stream, we need to reset
            trackers_l1[cpu][index].str_valid = 0;
    }

}
```

在 IP Global Stream 模式下的预取：

```c
if(trackers_l1[cpu][index].str_valid == 1){                         // stream IP
    // for stream, prefetch with twice the usual degree
    prefetch_degree = prefetch_degree*2;
    for (int i=0; i<prefetch_degree; i++) {
        uint64_t pf_address = 0;

        if(trackers_l1[cpu][index].str_dir == 1){                   // +ve stream
            pf_address = (cl_addr + i + 1) << LOG2_BLOCK_SIZE;
            metadata = encode_metadata(1, S_TYPE, spec_nl[cpu]);    // stride is 1
        }
        else{                                                       // -ve stream
            pf_address = (cl_addr - i - 1) << LOG2_BLOCK_SIZE;
            metadata = encode_metadata(-1, S_TYPE, spec_nl[cpu]);   // stride is -1
        }

        // Check if prefetch address is in same 4 KB page
        if ((pf_address >> LOG2_PAGE_SIZE) != (addr >> LOG2_PAGE_SIZE)){
            break;
        }

        prefetch_line(ip, addr, pf_address, FILL_L1, metadata);
        num_prefs++;
        SIG_DP(cout << "1, ");
        }
}
```

最后，如果这几种模式都没有匹配，就采用 Next Line Prefetcher：

```cpp
// if no prefetches are issued till now, speculatively issue a next_line prefetch
if(num_prefs == 0 && spec_nl[cpu] == 1){                                        // NL IP
    uint64_t pf_address = ((addr>>LOG2_BLOCK_SIZE)+1) << LOG2_BLOCK_SIZE;  
    metadata = encode_metadata(1, NL_TYPE, spec_nl[cpu]);
    prefetch_line(ip, addr, pf_address, FILL_L1, metadata);
    SIG_DP(cout << "1, ");
}
```

### Micro Armed Bandit

[Micro Armed Bandit (MICRO-56)](https://dl.acm.org/doi/10.1145/3613424.3623780) 把强化学习的 Multi-Armed Bandit 算法用于预取器的设计当中。首先介绍一下 Multi-Armed Bandit，它的意思是一个多臂的老虎机，模拟的是一个玩家，面前有多个不同的老虎机，每个老虎机可能带来不同的收益，但收益是未知的，那么 Multi-Armed Bandit 算法就是要寻找一种方法去选择玩哪些老虎机、玩多少次以最大化收益。它会给每个老虎机维护从这个老虎机上获取的 Reward 有多少，以及游玩的次数；在开始的 Round Robin 阶段，先轮流尝试各个老虎机，收集对应的 Reward，之后再根据启发式的算法，寻找一个 Reward 较高的老虎机或者选择一个随机老虎机，然后根据 Reward 来不断调整后续的选择。

在这里，老虎机就是选择哪些预取器，例如在 Next-Line、Stride 还是 Stream 当中选择，然后预取深度是多少。Reward 就是 IPC，因此会根据 IPC 的变化来选择更优的预取器。
