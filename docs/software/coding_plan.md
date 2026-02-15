# AI Coding Plan

## Coding Plan

### Kimi

[Kimi 登月计划](https://www.kimi.com/membership/pricing)

- Andante（49 RMB 每月）：每 5 小时的 Tokens 总量可支持约 300-1200 次 API 请求，确保复杂项目不间断。
- Moderato（99 RMB 每月）：Kimi Code 4 倍额度
- Allegretto（199 RMB 每月）：Kimi Code 20 倍额度
- Allegro（699 RMB 每月）：Kimi Code 60 倍额度
- 通过实际测试，认为 Andante 是所有请求的 input + output token 总和每 5 小时不超过 10M token；每周的限额是 4M uncached input + output token，即不考虑命中缓存的输入 token
- 宣传的是请求而非 token 数，根据 10M token 对应 300-1200 的请求次数，估计每次 API 请求的平均 input + output token 数量在 8K-33K 之间，本地用一段时间实测来看是 31K
- [K2.5 API 价格](https://platform.moonshot.cn/docs/pricing/chat)：
    - 输入命中缓存 0.7 RMB 每 1M token
    - 输入未命中缓存 4 RMB 每 1M token
    - 输出 21 RMB 每 1M token
    - 256K 上下文

### MiniMax

[MiniMax Coding Plan](https://platform.minimaxi.com/docs/coding-plan/intro)

- Starter（29 RMB 每月）: 40 prompts / 每 5 小时
- Plus（49 RMB 每月）: 100 prompts / 每 5 小时
- Max（119 RMB 每月）: 300 prompts / 每 5 小时
- Plus-极速版（98 RMB 每月）：100 prompts / 每 5 小时
- Max-极速版（199 RMB 每月）：300 prompts / 每 5 小时
- Ultra-极速版（899 RMB 每月）：2000 prompts / 每 5 小时
- Q: 为什么“一个 prompt 约等于 15 次模型调用”？A: 在 AI 编程工具中，您的一次操作（例如请求代码补全或解释代码）在工具后台可能会被拆分为多次与 AI 模型的连续交互（例如：获取上下文、生成建议、修正建议等）。为了简化计费，我们将这些后台的连续调用打包为一次“prompt”计数。这意味着您在套餐内的一次“prompt”实际上包含了多次模型的复杂调用。
- [M2.5 API 价格](https://platform.minimaxi.com/docs/guides/pricing-paygo)：
    - 输入命中缓存 0.21 RMB 每 1M token
    - 输入未命中缓存 2.1 RMB 每 1M token
    - 输入写入缓存 2.625 RMB 每 1M token
    - 输出 8.4 RMB 每 1M token
    - 200K 上下文

[MiniMax 国际版 Coding Plan](https://platform.minimax.io/docs/coding-plan/intro)

- Starter（10 USD 每月）: 100 prompts / 每 5 小时
- Plus（20 USD 每月）: 300 prompts / 每 5 小时
- Max（50 USD 每月）: 1000 prompts / 每 5 小时

### 智谱

[智谱 GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite 套餐（49 RMB 每月）：每 5 小时最多约 80 次 prompts，每周最多约 320 次 prompts
- Pro 套餐（149 RMB 每月）：每 5 小时最多约 400 次 prompts，每周最多约 1600 次 prompts
- Max 套餐（469 RMB 每月）：每 5 小时最多约 1600 次 prompts，每周最多约 6400 次 prompts
- 一次 prompt 指一次提问，每次 prompt 预计可调用模型 15-20 次。每周额度价值约为同等 API 费用的 13-23 倍。
- 调用 GLM-5 会 3 倍速率（和其他历史模型相比）消耗套餐额度
- 注：上述次数为预估值，实际可用量会因项目复杂度、代码库大小以及是否启用自动接受等因素而有所不同。
- 注：对于在 2 月 12 日之前订阅的用户，在您当前订阅套餐的有效期内，套餐的用量额度不变，仍按您订阅时页面显示执行。
- 注：对于在 2 月 12 日之前开启续订的用户，续费价格及套餐的用量额度不变，仍按您订阅时页面显示执行。
- 为了管理资源并确保所有用户的公平访问，我们增加了每周使用额度限制。该限额自您下单时开启计时，以 7 天为一个周期额度刷新重置。您可以在 用量统计 中查看您的额度消耗进展。2 月 12 日前订阅及开启自动续费的用户，在订阅有效期内，不受周使用额度限制。
- [GLM-5 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 1/1.5 RMB 每 1M token
    - 输入未命中缓存 4/6 RMB 每 1M token
    - 输出 18/22 RMB 每 1M token
    - 200K 上下文
- [GLM-4.7 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 0.4/0.6/0.8 RMB 每 1M token
    - 输入未命中缓存 2/3/4 RMB 每 1M token
    - 输出 8/14/16 RMB 每 1M token
    - 200K 上下文

[智谱国际版 GLM Coding Plan](https://z.ai/subscribe)

### 其他

- [方舟 Coding Plan](https://www.volcengine.com/activity/codingplan)
    - Lite 套餐（40 RMB 每月）：每 5 小时：最多约 1,200 次请求。每周：最多约 9,000 次请求。每订阅月：最多约 18,000 次请求。
    - Pro 套餐（200 RMB 每月）：Lite 套餐的 5 倍用量
- [阿里云百炼 Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
    - Lite（40 RMB 每月）: 固定月费，每月 18000 次请求，每周 9000 次，每 5 小时 1200 次
    - Pro（200 RMB 每月）: 固定月费，每月 90000 次请求，每周 45000 次，每 5 小时 6000 次
    - 一次用户提问可能触发多次模型调用，每次模型调用均计入一次额度消耗。典型场景下的额度消耗如下：
    - 简单问答或代码生成：通常触发 5-10 次模型调用
    - 代码重构或复杂任务：可能触发 10-30 次或更多模型调用
    - 实际额度消耗取决于任务的复杂度、上下文大小、工具调用次数等多种因素。具体消耗以实际使用情况为准，您可以在 Coding Plan 控制台查看套餐额度消耗情况。

## prompt、请求和 token

- prompt：用户输入提示词到 CLI，按回车发出去，从请求来看，就是最后一个消息是来自用户的，而非 tool call result
- 请求：除了 prompt 本身会有一次请求以外，每轮 tool call 结束后，会把 tool call 结果带上上下文再发送请求，直到没有 tool call 为止
- token：每次请求都有一定量的 input 和 output token

一次 prompt 对应多次请求，每次请求都有很多的 input 和 output token。其中部分 input token 会命中缓存。实际测试下来，在 Vibe Coding 场景下，input + output token 当中：

- input token 占比 99.5%，因为多轮对话下来，input token 会不断累积变多，被重复计算
    - 其中 cached token 占 input + output token 约 90-95%
- output token 占比 0.5%

## 常见 API 定价方式

- OpenAI 模式：自动缓存，有输入未命中缓存价格、输入命中缓存价格和输出价格
    - OpenAI 有 Input，Cached Input 和 Output 三种价格，如果访问没有命中缓存，不命中的部分按 Input 收费，OpenAI 可能会进行缓存；如果访问命中缓存，命中的部分按 Cached Input 收费
    - 通常 Cached Input 是 0.1 倍的 Input 价格，也有 0.1-0.2 倍之间的
- Anthropic 模式：手动缓存，有输入未命中缓存价格、输入命中缓存价格、带缓存写入的输入价格（不同的 TTL 可能对应不同的价格）和输出价格
    - Claude 有 Base Input Tokens，5m Cache Writes，1h Cache Writes，Cache Hits & Refreshes 和 Output Tokens 五种价格，如果不使用缓存，那么每次输入都按 Base Input Tokens 收费；如果使用缓存，写入缓存部分的输入按 5m/1h Cache Writes 收费，之后命中缓存部分的输入按 Cache Hits & Refreshes 收费
    - 目前 5m Cache Writes 是 1.25 倍的 Base Input Tokens 价格，1h Cache Writes 是 2 倍的 Base Input Tokens 价格，Cache Hits & Refreshes 是 0.1 倍的 Base Input Tokens 价格

## 模型参数比较

- [Kimi-K2.5](https://huggingface.co/moonshotai/Kimi-K2.5): 1T parameters (32B active)
- [GLM-5](https://huggingface.co/zai-org/GLM-5): 744B parameters (40B active) 
- [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7): 355B parameters (32B active) 
- [MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5): 230B parameters (10B active)

## 更新历史

- 2026/02/16：最近发现 Kimi Code 的计费方式有一些不同：
    - Andante 套餐每 5 小时的限额不变还是 10M input + output token，但每周的限额，表现为开一个新的 Code Session 时用的比较快，明显不是每 5 小时用量的 20%（之前的推算结果里，每周的限额是 5 倍的每 5 小时的限额），但慢慢用下来，比例还是在 20% 附近，按照之前的方法推算，每周的用量大概是 48M input + output token 而非原来的 50M，是个比较奇怪的数字
    - 这个疑问被 [LLM 推理系统、Code Agent 与电网 - 许欣然](https://zhuanlan.zhihu.com/p/2006506955775169424) 解释了：cached token 不收钱
    - 如果按照 uncached input + output token 来计算，那么每周的用量就是 4M uncached input + output token；而 5 小时的限制应该还是老的算法
    - 这样做的目的是，如果把 Kimi Code 用于一些 cache 比例很低的非 Vibe Coding 场景，那么每周的限额会消耗地很快
- 2026/02/15：MiniMax Coding Plan 添加了 Plus/Max/Ultra 极速版
- 2026/02/14: GLM Coding Plan 添加了每周的限额，是每 5 小时限额的 4 倍（Kimi 是 5 倍，方舟和阿里是 7.5 倍），同时 GLM-5 对限额的消耗速度是 GLM-4.7 的三倍
    - 不正经评语：看来在智谱，一周只用上四天班，每天工作 5 小时，而在 Moonshot 一周需要上五天班，在字节和阿里要每周上 7.5 天的班，哪个公司加班多一目了然，狗头（但字节和阿里一个月只用上两周，其他两周不上班，这就是“大小周”吗）
    - 正经评语：新 GLM Coding Plan 的性价比一下从夯降低到 NPC 的水平，那么 Kimi/MiniMax 的性价比就显现出来了，解决办法是继续续订老套餐，坚持 GLM-4.7 不动摇
    - 如果按照新套餐是原来的 2/3 限额折算，按 GLM-4.7 计算，那么 Lite 套餐每月（按 30 天算）可以用 `40M*2/3*4*30/7=457M` token；按 GLM-5 计算，则是 `40M*2/3*4*30/7/3=152M` token
- 2026/02/12：GLM Coding Plan 价格从 40/200/400 RMB 每月改成 49/149/469 RMB 每月；与此同时，用量额度减少了，变成了原来的 2/3：
    - Lite 套餐：每 5 小时最多约 80（原来是 120）次 prompts，相当于 Claude Pro 套餐用量的 3 倍
    - Pro 套餐：每 5 小时最多约 400（原来是 600）次 prompts，相当于 Lite 套餐用量的 5 倍
    - Max 套餐：每 5 小时最多约 1600（原来是 2400）次 prompts，相当于 Pro 套餐用量的 4 倍
    - 如果按照新是旧的 2/3 比例的话，那 Lite 套餐限额就是每 5 小时 `40/3*2=27M` token，另外新版还有每周的限额（2026/02/14 发布了具体规则见上）；待切换到新套餐后（不打算切了），再测试新版的用量限制对应多少 token（有读者感兴趣可以测完反馈一下）
- 2026/02/12：增加 Kimi Allegro 套餐的描述
- 2026/02/12：随着 GLM-5 的发布，GLM Coding Plan 的 quota/limit 接口不再返回具体的 token 数，应该是为了之后 GLM-5 与 GLM-4.7 以不同的速度消耗用量做准备（根据 API 价格猜测会有个 2 倍的系数？等待后续的测试），但目前测下来 GLM-4.7 的用量限制不变，Lite 套餐依然是输入加输出 40M token 每 5 小时；由于只有每 5 小时的限额，按每月 30 天算，理论上每月最多可以用到 `30*24/5*40=5760M` token
- 2026/01/30：通过实际测试，猜测 GLM Coding Plan 的 Lite 套餐用量限制是每 5 小时所有请求的 input + output token 总和不超过 40M token（意味着每次 prompt 对应 40M/120=333K token），这和 <https://open.bigmodel.cn/api/monitor/usage/quota/limit> 接口返回的结果一致（2026/02/12 后该接口只返回百分比，不返回 token 数）
