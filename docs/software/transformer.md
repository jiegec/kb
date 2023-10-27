# Transformer

下面只考虑 Decoder-only 的 Transformer。

## 计算过程

输入 $n$ 个 Token，通过 Text 和 Position Embedding 后，得到一个尺寸为 $(n, d_{model})$ 的矩阵，其中 $d_{model}$ 为 Embedding 向量的长度。

接着，经过 $n_{layer}$ 个层，每层中要进行如下的计算：

1. 从上一层的输出 $(n, d_{model})$，每个 head 上乘以三个 $(d_{model}, d_{head})$ 的矩阵，得到 Q，K 和 V，尺寸为 $(n, d_{head})$
2. 按照 attention 激活公式，得到 Z，尺寸为 $(n, d_{head})$
3. 把所有 head 的 Z 矩阵拼起来，保证 $d_{model} = n_{head} * d_{head}$，那么所有的 Z 拼起来以后得到的矩阵的尺寸为 $(n, d_{head})$
4. 乘以一个尺寸为 $(d_{model}, d_{model})$ 的 Projection 矩阵，得到新矩阵 $(n, d_{model})$
5. 经过一个 MLP，MLP 第一层是 $(d_{model}, 4*d_{model})$，第二层是 $(4*d_{model}, d_{model})$
6. MLP 输出的矩阵尺寸为 $(n, d_{model})$

## KV cache

在推理的时候，是在已有的 context 的基础上，生成一个新 token，再把 token 加到 context，继续生成下一个 token。计算的时候，由于 Attention 会带 Mask，旧 token 不会依赖新 token，因此旧 token 的部分不会变，可以只考虑新引入的 token 带来的变化。

那么，计算新的 token 的 Q K V 以后，在进行 Attention 计算的时候，会发现先前的 token 的 K 和 V 部分不变，先前 token 的 Q 不影响当前 token 的结果。因此可以把之前 token 的 K 和 V 保存下来，不用重新计算，这就是 KV cache。

## 参数量和浮点计算量

考虑每层的参数量和浮点计算量：

1. 计算 Q，K 和 V：参数是三个 $(d_{model}, d_{model})$ 的矩阵，计算量是 $2 * 3 * n * d_{model}^2$
2. 乘以 Projection 矩阵：参数是 $(d_{model}, d_{model})$ 的矩阵，计算量是 $2 * n * d_{model}^2$
3. 乘以 MLP 第一层：参数是 $(d_{model}, 4*d_{model})$ 的矩阵，计算量是 $2 * 4 * n * d_{model}^2$
4. 乘以 MLP 第二层：参数是 $(4*d_{model}, d_{model})$ 的矩阵，计算量是 $2 * 4 * n * d_{model}^2$

其余部分的参数量和计算量可以忽略不计。

因此总参数量（不考虑 Embedding）为：

$$
12n_{layer}d_{model}^2
$$

每个 Token 的浮点计算量为：

$$
24n_{layer}d_{model}^2 \mathrm{FLOP}
$$

## 参考文献

- [Speeding up the GPT - KV cache](https://www.dipkumar.dev/becoming-the-unbeatable/posts/gpt-kvcache/)
- [最新最全 GPT-3 模型网络结构详细解析](https://zhuanlan.zhihu.com/p/174782647)
- [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/)
- [Understanding FLOPs-per-token estimates from OpenAI’s scaling laws](https://discuss.huggingface.co/t/understanding-flops-per-token-estimates-from-openais-scaling-laws/23133)
- [拆 Transformer 系列二：Multi-Head Attention 机制详解](https://zhuanlan.zhihu.com/p/109983672)
- [Past_key_values - why not past_key_values_queries?](https://discuss.huggingface.co/t/past-key-values-why-not-past-key-values-queries/31941/4)