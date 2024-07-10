# 条件分支预测器

条件分支预测器负责预测条件分支的跳转方向：跳转（Taken）或者不跳转（Not Taken）。

## Static predictor

只根据指令本身的类型（或者 hint）进行分支预测。

## Bimodal predictor

对分支地址求 hash，得到的 hash 取模作为 index 去访问一个表，表的每一项是一个 2-bit saturating counter，0 和 1 预测 not taken，2 和 3 预测 taken。执行完分支后，如果 taken，则对应 counter 加一；否则对应 counter 减一。

## Two level predictor

记录最近若干个分支的跳转/不跳转历史，保存在 Global History Register 里面，再用 GHR 作为 index 去访问 Pattern History Table，PHT 的每一项也是一个 2 bit saturating counter，剩下的逻辑和 Bimodal 一样。

如果把 PC 和 GHR 异或后作为 index 访问 PHT，就是 Gshare 算法。如果把 PC 和 GHR 拼接起来作为 index 访问 PHT，就是 Gselect 算法。

## Local History

也可以记录每个分支自己的跳转/不跳转历史，保存在 Branch History Table 里面：根据 PC 从 Branch History Table 里找到该分支的 Local History，再用 Local History 访问 PHT。也可以把 Local History 和 PC 结合起来作为 index 访问 PHT。

## Path History

除了记录所有分支的 Taken/Not Taken 历史到 GHR 里，还可以只记录 Taken 分支的分支地址以及分支目的地址，保存到 Path History Register 里，代替 GHR 的作用。Intel 采用的是这个方案，每个 Taken 分支生成若干位的值，异或到 PHR 左移若干位的结果，成为新的 PHR。

## TAGE

流行的分支预测器，由一个 base predictor 以及若干个 PHT 组成。不同的 PHT 采用了不同的 GHR/PHR 位数，位数呈几何级数。预测时，base predictor 和所有 PHT 同时预测，最后采用给出预测里采用的历史位数最多的那一个。

PHT 的每个项记录了：

1. prediction saturating counter：用来预测 taken/not taken
2. useful saturating counter：表示该表项的重要性
3. tag：出现 index 冲突时判断预测的是否是正确的分支

useful 的维护方法：

1. 如果用该表项预测的正确，而用更短历史的 table 预测的错误，说明该表项很有用，useful 增加
2. 反之，如果用该表项预测的错误，而用更短历史的 table 预测的正确，说明该表项效果不好，useful 减少

出现分支预测错误时，认为当前所用的 PHT 的分支历史长度太段，不够预测当前的分支，因此在具有更长的历史的 PHT 里分配一条给预测错误的分支，找一个 useful 等于 0 的项替换。

为了避免一些表项很长时间都没有使用，但由于 useful 比较大而不会被替换，占用空间，需要定时减少 PHT 里所有表项的 useful 计数器，相当于 useful 计数器也有计时的功能，太久没用的表项会被替换。

在出现分支预测错误，创建了新的表项的时候，由于新表项记录的历史比较少，可能不够准确，此时可以临时用第二长的匹配的 PHT 里的表项做预测一段时间。
