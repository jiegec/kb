# AI Coding Plan

- [Kimi 登月计划 49/99/199/699 RMB 每月](https://www.kimi.com/membership/pricing)
    - Andante：每 5 小时的 Tokens 总量可支持约 300-1200 次 API 请求，确保复杂项目不间断。（通过实际测试，猜测是所有请求的 input + output token 总和每 5 小时不超过 10M token，每周的限额是每 5 小时的 5 倍，即 50M token）
    - Moderato：Kimi Code 4 倍额度
    - Allegretto：Kimi Code 20 倍额度
    - Allegro：Kimi Code 60 倍额度
    - [K2.5 API 价格](https://platform.moonshot.cn/docs/pricing/chat)：
        - 输入命中缓存 0.7 RMB 每 1M token
        - 输入未命中缓存 4 RMB 每 1M token
        - 输出 21 RMB 每 1M token
        - 256K 上下文
- [MiniMax Coding Plan 29/49/119 RMB 每月](https://platform.minimaxi.com/docs/coding-plan/intro)
    - Starter: 40 prompts / 每 5 小时
    - Plus: 100 prompts / 每 5 小时
    - Max: 300 prompts / 每 5 小时
    - Q: 为什么“一个 prompt 约等于 15 次模型调用”？A: 在 AI 编程工具中，您的一次操作（例如请求代码补全或解释代码）在工具后台可能会被拆分为多次与 AI 模型的连续交互（例如：获取上下文、生成建议、修正建议等）。为了简化计费，我们将这些后台的连续调用打包为一次“prompt”计数。这意味着您在套餐内的一次“prompt”实际上包含了多次模型的复杂调用。
    - [M2.1 API 价格](https://platform.minimaxi.com/docs/guides/pricing-paygo)：
        - 输入命中缓存 0.21 RMB 每 1M token
        - 输入未命中缓存 2.1 RMB 每 1M token
        - 输入写入缓存 2.625 RMB 每 1M token
        - 输出 8.4 RMB 每 1M token
        - 200K 上下文
- [MiniMax 国际版 Coding Plan 10/20/50 USD 每月](https://platform.minimax.io/docs/coding-plan/intro)
    - Starter: 100 prompts / 每 5 小时
    - Plus: 300 prompts / 每 5 小时
    - Max: 1000 prompts / 每 5 小时
- [方舟 Coding Plan 40/200 RMB 每月](https://www.volcengine.com/activity/codingplan)
    - Lite 套餐：每 5 小时：最多约 1,200 次请求。每周：最多约 9,000 次请求。每订阅月：最多约 18,000 次请求。
    - Pro 套餐：Lite 套餐的 5 倍用量
- [智谱 GLM Coding Plan 40/200/400 RMB 每月](https://docs.bigmodel.cn/cn/coding-plan/overview)
    - Lite 套餐：每 5 小时最多约 120 次 prompts，相当于 Claude Pro 套餐用量的 3 倍（通过实际测试，猜测用量限制是每 5 小时所有 GLM-4.7 请求的 input + output token 总和不超过 40M token，这和在 2026.2.12 之前通过 <https://open.bigmodel.cn/api/monitor/usage/quota/limit> 接口返回的结果一致，目前该接口只返回百分比，不再返回 token 数）
    - Pro 套餐：每 5 小时最多约 600 次 prompts，相当于 Claude Max(5x) 套餐用量的 3 倍
    - Max 套餐：每 5 小时最多约 2400 次 prompts，相当于 Claude Max(20x) 套餐用量的 3 倍
    - 从可消耗 tokens 量来看，每次 prompt 预计可调用模型 15-20 次，每月总计可用总量高达几十亿到数百亿 tokens，折算下来仅为 API 价格的 0.1 折，极具性价比。
    - 注：上述次数为预估值，实际可用量会因项目复杂度、代码库大小以及是否启用自动接受等因素而有所不同。
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
- [智谱国际版 GLM Coding Plan](https://z.ai/subscribe)
- [阿里云百炼 Coding Plan 40/200 RMB 每月](https://help.aliyun.com/zh/model-studio/coding-plan)
    - Lite: 固定月费，每月 1.8 万次请求，其中每 5 小时限额 1200 次
    - Pro: 固定月费，每月 9 万次请求，其中每 5 小时限额 6000 次

常见 API 定价方式：

- OpenAI 模式：自动缓存，有输入未命中缓存价格、输入命中缓存价格和输出价格
    - OpenAI 有 Input，Cached Input 和 Output 三种价格，如果访问没有命中缓存，不命中的部分按 Input 收费，OpenAI 可能会进行缓存；如果访问命中缓存，命中的部分按 Cached Input 收费
    - 通常 Cached Input 是 0.1 倍的 Input 价格，也有 0.1-0.2 倍之间的
- Anthropic 模式：手动缓存，有输入未命中缓存价格、输入命中缓存价格、带缓存写入的输入价格（不同的 TTL 可能对应不同的价格）和输出价格
    - Claude 有 Base Input Tokens，5m Cache Writes，1h Cache Writes，Cache Hits & Refreshes 和 Output Tokens 五种价格，如果不使用缓存，那么每次输入都按 Base Input Tokens 收费；如果使用缓存，写入缓存部分的输入按 5m/1h Cache Writes 收费，之后命中缓存部分的输入按 Cache Hits & Refreshes 收费
    - 目前 5m Cache Writes 是 1.25 倍的 Base Input Tokens 价格，1h Cache Writes 是 2 倍的 Base Input Tokens 价格，Cache Hits & Refreshes 是 0.1 倍的 Base Input Tokens 价格

更新历史：

- 2026/02/12：增加 Kimi Allegro 套餐的描述
- 2026/02/12：随着 GLM-5 的发布，GLM Coding Plan 的 quota/limit 接口不再返回具体的 token 数，应该是为了之后 GLM-5 与 GLM-4.7 以不同的速度消耗用量做准备（根据 API 价格猜测会有个 2 倍的系数？等待后续的测试），但目前测下来 GLM-4.7 的用量限制不变，Lite 套餐依然是输入加输出 40M token 每 5 小时