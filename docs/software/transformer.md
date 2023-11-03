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

## Llama 2 7B

以 Llama 2 7B 为例，下面分析 Transformer 推理的计算过程，它的参数如下：

- hidden size: 4096
- intermediate size（MLP 的中间层的维度）: 11008
- hidden layers: 32
- attention heads: 32
- key value heads: 32
- head dim: 4096 / 32 = 128
- vocab size: 32000

参考 [HuggingFace 源码](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py)。

Llama2 的主要计算过程是 32 层 LlamaDecoderLayer，每个 LlamaDecoderLayer 包括：

1. `hidden_states = self.input_layernorm(hidden_states)`: 见 LlamaRMSNorm
2. `hidden_states, self_attn_weights, present_key_value = self.self_attn()`：见 LlamaAttention
3. `hidden_states = residual + hidden_states`: `aten::add([1, 1, 4096], [1, 1, 4096]) = [1, 1, 4096]`
4. `hidden_states = self.post_attention_layernorm(hidden_states)`: 见 LlamaRMSNorm
5. `hidden_states = self.mlp(hidden_states)`：见 LlamaMLP
6. `hidden_states = residual + hidden_states`: `aten::add([1, 1, 4096], [1, 1, 4096]) = [1, 1, 4096]`

hidden_states 的规模是 `[1, 1, 4096]`。

LlamaRMSNorm 包括：

1. `hidden_states = hidden_states.to(torch.float32)`: `aten::to([1, 1, 4096]) = [1, 1, 4096]`
2. `v1 = hidden_states.pow(2)`: `aten::pow([1, 1, 4096]) = [1, 1, 4096]`
3. `variance = v2.mean(-1, keepdim=True)`: `aten::mean([1, 1, 4096]) = [1, 1, 1]`
4. `v3 = variance + self.variance_epsilon`: `aten::add([1, 1, 1]) = [1, 1, 1]`, 1 FLOP
5. `v4 = torch.rsqrt(v3)`: `aten::rsqrt([1, 1, 1]) = [1, 1, 1]`
6. `hidden_states = hidden_states * v4`: `aten::mul([1, 1, 4096], [1, 1, 1]) = [1, 1, 4096]`, 4096 FLOP
7. `v5 = hidden_states.to(input_dtype)`: `aten::to([1, 1, 4096]) = [1, 1, 4096]`
8. `return self.weight * v5`: `aten::mul([4096], [1, 1, 4096])`, 4096 FLOP

LlamaAttention 包括：

1. `query_states = self.q_proj(hidden_states)`: `aten::linear([1, 1, 4096], [4096, 4096]) = [1, 1, 4096]`, 33554432 FLOP
2. `key_states = self.k_proj(hidden_states)`: `aten::linear([1, 1, 4096], [4096, 4096]) = [1, 1, 4096]`, 33554432 FLOP
3. `value_states = self.v_proj(hidden_states)`: `aten::linear([1, 1, 4096], [4096, 4096]) = [1, 1, 4096]`, 33554432 FLOP
4. `v1 = query_states.view(bsz, q_len, self.num_heads, self.head_dim)`: `aten::view([1, 1, 4096]) = [1, 1, 32, 128]`
5. `query_states = v1.transpose(1, 2)`: `aten::transpose([1, 1, 32, 128]) = [1, 32, 1, 128]`
6. `v2 = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim)`: `aten::view([1, 1, 4096]) = [1, 1, 32, 128]`
7. `key_states = v2.transpose(1, 2)`: `aten::transpose([1, 1, 32, 128]) = [1, 32, 1, 128]`
8. `v3 = value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim)`: `aten::view([1, 1, 4096]) = [1, 1, 32, 128]`
9. `value_states = v3.transpose(1, 2)`: `aten::transpose([1, 1, 32, 128]) = [1, 32, 1, 128]`
10. `cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)`: 见 LlamaRotaryEmebdding
11. `query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, position_ids)`: 见 apply_rotary_pos_emb
12. `key_states = torch.cat([past_key_value[0], key_states], dim=2)`: `aten::cat([1, 32, C-1, 128], [1, 32, 1, 128]) = [1, 32, C, 128]`
13. `value_states = torch.cat([past_key_value[1], value_states], dim=2)`: `aten::cat([1, 32, C-1, 128], [1, 32, 1, 128]) = [1, 32, C, 128]`
14. `v4 = key_states.transpose(2, 3)`: `aten::transpose([1, 32, C, 128]) = [1, 32, 128, C]`
15. `v5 = torch.matmul(query_states, v4)`: `aten::matmul([1, 32, 1, 128], [1, 32, 128, C]) = [1, 32, 1, C]`, 8192*C FLOP
16. `attn_weights = v1 / math.sqrt(self.head_dim)`: `aten::div([1, 32, 1, C]) = [1, 32, 1, C]`
17. `attn_weights = attn_weights + attention_mask`: `aten::add([1, 32, 1, C], [1, 1, 1, C]) = [1, 32, 1, C]`, 32*C FLOP
18. `v6 = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)`: `aten::softmax([1, 32, 1, C]) = [1, 32, 1, C]`
19. `attn_weights = v6.to(query_states.dtype)`: `aten::to([1, 32, 1, C]) = [1, 32, 1, C]`
20. `attn_output = torch.matmul(attn_weights, value_states)`: `aten::matmul([1, 32, 1, C], [1, 32, C, 128]) = [1, 32, 1, 128]`: 8192*C FLOP
21. `attn_output = attn_output.transpose(1, 2).contiguous()`: `aten::transpose([1, 32, 1, 128]) = [1, 1, 32, 128]`
22. `attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)`: `aten::reshape([1, 1, 32, 128]) = [1, 1, 4096]`
23. `attn_output = self.o_proj(attn_output)`: `aten::linear([1, 1, 4096], [4096, 4096]) = [1, 1, 4096]`, 33554432 FLOP

LlamaRotaryEmbedding 包括：

1. `self.cos_cached[:, :, :seq_len, ...].to(dtype=x.dtype),`: `aten::slice([1, 1, 4096, 128])`
2. `self.sin_cached[:, :, :seq_len, ...].to(dtype=x.dtype),`: `aten::slice([1, 1, 4096, 128])`

apply_rotary_pos_emb 包括：

1. `v1 = cos.squeeze(1)`: `aten::squeeze([1, 1, 10, 128])`
2. `cos = v1.squeeze(0)`: `aten::squeeze([1, 10, 128])`
3. `v2 = cos.squeeze(1)`: `aten::squeeze([1, 1, 10, 128])`
4. `sin = v2.squeeze(0)`: `aten::squeeze([1, 10, 128])`
5. `v3 = cos[position_ids]`: `aten::index([10, 128])`
6. `cos = v3.unsqueeze(1)`: `aten::unsqueeze([1, 1, 128]) = [1, 1, 1, 128]`
7. `v4 = sin[position_ids]`: `aten::index([10, 128])`
8. `sin = v4.unsqueeze(1)`: `aten::unsqueeze([1, 1, 128]) = [1, 1, 1, 128]`
9. `v5 = q * cos`: `aten::mul([1, 32, 1, 128], [1, 1, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP
10. `v6 = rotate_half(q)`: 见 rotate_half
11. `v7 = v6 * sin`: `aten::mul([1, 32, 1, 128], [1, 1, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP
12. `q_embed = v5 + v7`: `aten::add([1, 32, 1, 128], [1, 32, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP
13. `v8 = k * cos`: `aten::mul([1, 32, 1, 128], [1, 1, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP
14. `v9 = rotate_half(k)`: 见 rotate_half
15. `v10 = v9 * sin`: `aten::mul([1, 32, 1, 128], [1, 1, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP
16. `k_embed = v8 + v10`: `aten::add([1, 32, 1, 128], [1, 32, 1, 128]) = [1, 32, 1, 128]`, 4096 FLOP

rotate_half 包括：

1. `x1 = x[..., : x.shape[-1] // 2]`: `aten::slice([1, 3, 1, 128])`
2. `x2 = x[..., x.shape[-1] // 2 :]`: `aten::slice([1, 3, 1, 128])`
1. `v1 = -x2`: `aten::neg([1, 3, 1, 64])`
2. `return torch.cat((v1, x1), dim=-1)`: `aten::cat([1, 3, 1, 64], [1, 3, 1, 64]) = [1, 3, 1, 128]`

LlamaMLP 包括：

1. `v1 = self.gate_proj(x)`: `aten::linear([1, 1, 4096], [11008, 4096]) = [1, 1, 11008]`, 90177536 FLOP
2. `v2 = self.act_fn(v1)`: `aten::silu([1, 1, 11008]) = [1, 1, 11008]`
3. `v3 = self.up_proj(x)`: `aten::linear([1, 1, 4096], [11008, 4096]) = [1, 1, 11008]`, 90177536 FLOP
4. `v4 = v2 * v3`: `aten::mul([1, 1, 11008], [1, 1, 11008]) = [1, 1, 11008]`, 11008 FLOP
5. `v5 = self.down_proj(v4)`: `aten::linear([1, 1, 11008], [4096, 11008]) = [1, 1, 4096]`, 90177536 FLOP

所有 aten 算子：

- aten::add
- aten::cat
- aten::div
- aten::index
- aten::linear
- aten::matmul
- aten::mean
- aten::mul
- aten::neg
- aten::pow
- aten::reshape
- aten::rsqrt
- aten::sequeeze
- aten::silu
- aten::slice
- aten::softmax
- aten::to
- aten::transpose
- aten::unsqueeze
- aten::view


## 参考文献

- [Speeding up the GPT - KV cache](https://www.dipkumar.dev/becoming-the-unbeatable/posts/gpt-kvcache/)
- [最新最全 GPT-3 模型网络结构详细解析](https://zhuanlan.zhihu.com/p/174782647)
- [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/)
- [Understanding FLOPs-per-token estimates from OpenAI’s scaling laws](https://discuss.huggingface.co/t/understanding-flops-per-token-estimates-from-openais-scaling-laws/23133)
- [拆 Transformer 系列二：Multi-Head Attention 机制详解](https://zhuanlan.zhihu.com/p/109983672)
- [Past_key_values - why not past_key_values_queries?](https://discuss.huggingface.co/t/past-key-values-why-not-past-key-values-queries/31941/4)