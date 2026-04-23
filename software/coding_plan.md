# AI Coding Plan

## Coding Plan

### Kimi

[Kimi 登月计划](https://www.kimi.com/membership/pricing)

- Andante（49 RMB 每月）：每 5 小时的 Tokens 总量可支持约 300-1200 次 API 请求，最高并发上限达 30，确保复杂项目不间断
- Moderato（99 RMB 每月）：Kimi Code 4 倍额度
- Allegretto（199 RMB 每月）：Kimi Code 20 倍额度
- Allegro（699 RMB 每月）：Kimi Code 60 倍额度
- 通过实际测试，认为 Andante 是所有请求的 uncached input + output tokens 总和每 5 小时不超过 1M tokens，即不考虑命中缓存的输入 tokens；每周的限额是 4M uncached input + output tokens
- [K2.6 API 价格](https://platform.moonshot.cn/docs/pricing/chat)：
  - 输入命中缓存 1.1 RMB 每 1M tokens
  - 输入未命中缓存 6.5 RMB 每 1M tokens
  - 输出 27 RMB 每 1M tokens
  - 256K 上下文

### MiniMax

[MiniMax Token Plan](https://platform.minimaxi.com/docs/token-plan/intro) [产品定价](https://platform.minimaxi.com/docs/guides/pricing-token-plan)

- Starter（29 RMB 每月）: 600 请求 / 每 5 小时
- Plus（49 RMB 每月）: 1500 请求 / 每 5 小时
- Max（119 RMB 每月）: 4500 请求 / 每 5 小时
- Plus-极速版（98 RMB 每月）：1500 请求 / 每 5 小时
- Max-极速版（199 RMB 每月）：4500 请求 / 每 5 小时
- Ultra-极速版（899 RMB 每月）：30000 请求 / 每 5 小时
- Token Plan 的用量额度按模型分别计算：
  - M2.7 / M2.7-highspeed：按请求（request）计算，每 5 小时滚动重置。
  - 其他模型（语音、视频、音乐、图像）：按每日配额计算，每日重置。
- 所有方案均搭载最新 MiniMax M2.7 模型，并根据资源负载提供 M2.7-highspeed 使用。极速版订阅提供专属 M2.7-highspeed 支持，带来更快的推理速度。
- 周使用额度：当前每周可使用额度为「5 小时额度」的 10 倍（行业常见为 5–8 倍）
- [M2.7 API 价格](https://platform.minimaxi.com/docs/guides/pricing-paygo)：
  - 输入命中缓存 0.42 RMB 每 1M tokens
  - 输入未命中缓存 2.1 RMB 每 1M tokens
  - 输入写入缓存 2.625 RMB 每 1M tokens
  - 输出 8.4 RMB 每 1M tokens
  - 200K 上下文

[MiniMax 国际版 Coding Plan](https://platform.minimax.io/docs/token-plan/intro) [产品定价](https://platform.minimax.io/docs/guides/pricing-token-plan)

- Starter（10 USD 每月）: 1500 请求 / 每 5 小时
- Plus（20 USD 每月）: 4500 请求 / 每 5 小时
- Max（50 USD 每月）: 15000 请求 / 每 5 小时
- Plus-极速版（40 USD 每月）：4500 请求 / 每 5 小时
- Max-极速版（80 USD 每月）：15000 请求 / 每 5 小时
- Ultra-极速版（150 USD 每月）：30000 请求 / 每 5 小时

### 智谱

[智谱 GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite 套餐（49 RMB 每月）：每 5 小时最多约 80 次 prompts，每周最多约 400 次 prompts
- Pro 套餐（149 RMB 每月）：每 5 小时最多约 400 次 prompts，每周最多约 2000 次 prompts
- Max 套餐（469 RMB 每月）：每 5 小时最多约 1600 次 prompts，每周最多约 8000 次 prompts
- 一次 prompt 指一次提问，每次 prompt 预计可调用模型 15-20 次。每月可用额度按 API 定价折算，相当于月订阅费用的 15–30 倍（已计入周限额影响）。
- 注：上述次数为预估值，实际可用量会因项目复杂度、代码库大小以及是否启用自动接受等因素而有所不同。
- 注：所有套餐均支持 GLM-5.1、GLM-5-Turbo、GLM-4.7、GLM-4.5-Air。
- 注：GLM-5.1、GLM-5-Turbo 作为高阶模型，对标 Claude Opus，调用时将按照“高峰期 3 倍，非高峰期 2 倍”系数消耗额度；我们推荐您在复杂任务上切换至 GLM-5.1 处理，普通任务上继续使用 GLM-4.7，以避免套餐用量额度消耗过快。（作为限时福利，GLM-5.1、GLM-5-Turbo 将在非高峰期仅作为 1 倍抵扣，持续到 4 月底）注：高峰期为每日的 14:00～18:00（UTC+8）
- [GLM-5-Turbo API 价格](https://bigmodel.cn/pricing)：
  - 输入命中缓存 1.2/1.8 RMB 每 1M tokens
  - 输入未命中缓存 5/7 RMB 每 1M tokens
  - 输出 22/26 RMB 每 1M tokens
  - 200K 上下文
- [GLM-5.1 API 价格](https://bigmodel.cn/pricing)：
  - 输入命中缓存 1.3/2 RMB 每 1M tokens
  - 输入未命中缓存 6/8 RMB 每 1M tokens
  - 输出 24/28 RMB 每 1M tokens
  - 200K 上下文
- [GLM-4.7 API 价格](https://bigmodel.cn/pricing)：
  - 输入命中缓存 0.4/0.6/0.8 RMB 每 1M tokens
  - 输入未命中缓存 2/3/4 RMB 每 1M tokens
  - 输出 8/14/16 RMB 每 1M tokens
  - 200K 上下文

[智谱国际版 GLM Coding Plan](https://z.ai/subscribe)

### 云厂商

- [方舟 Coding Plan](https://www.volcengine.com/activity/codingplan)
  - Lite 套餐（40 RMB 每月）：每 5 小时：最多约 1,200 次请求。每周：最多约 9,000 次请求。每订阅月：最多约 18,000 次请求。
  - Pro 套餐（200 RMB 每月）：Lite 套餐的 5 倍用量
  - 支持模型：Doubao-Seed-2.0-Code、Doubao-Seed-2.0-pro、Doubao-Seed-2.0-lite、Doubao-Seed-Code、MiniMax-M2.7、MiniMax-2.5、Kimi-K2.6、Kimi-K2.5、GLM-5.1、GLM-4.7、DeepSeek-v3.2、Doubao-Embedding-Vision
- [阿里云百炼 Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
  - Pro 套餐（200 RMB 每月）：固定月费，每月 90000 次请求，每周 45000 次，每 5 小时 6000 次
  - Lite 基础套餐已于 2026 年 3 月 19 日停止新购，于 2026 年 4 月 13 日起停止续费和升级，已购用户可继续使用至服务到期，详见[公告](https://www.aliyun.com/notice/118175)
  - 一次用户提问可能触发多次模型调用，每次模型调用均计入一次额度消耗。典型场景下的额度消耗如下：
  - 简单问答或代码生成：通常触发 5-10 次模型调用
  - 代码重构或复杂任务：可能触发 10-30 次或更多模型调用
  - 实际额度消耗取决于任务的复杂度、上下文大小、工具调用次数等多种因素。具体消耗以实际使用情况为准，您可以在 Coding Plan 控制台查看套餐额度消耗情况。
  - 推荐模型：qwen3.6-plus、kimi-k2.5、glm-5、minimax-m2.5。更多模型：qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7
  - 注：qwen3.6-plus 为 Pro 套餐专属权益
  - [Qwen3.6-Plus API 价格](https://help.aliyun.com/zh/model-studio/models)：
    - 输入 2/8 RMB 每 1M tokens
    - 输出 12/48 RMB 每 1M tokens
    - 1M 上下文
  - [Qwen3-Max API 价格](https://help.aliyun.com/zh/model-studio/models)：
    - 输入 2.5/4/7 RMB 每 1M tokens
    - 输出 10/16/28 RMB 每 1M tokens
    - 256K 上下文
- [阿里云百炼 Token Plan（团队版）](https://help.aliyun.com/zh/model-studio/token-plan-overview)
  - 标准坐席（¥198/坐席/月）：25,000 Credits/坐席/月
  - 高级坐席（¥698/坐席/月）：100,000 Credits/坐席/月
  - 尊享坐席（¥1,398/坐席/月）：250,000 Credits/坐席/月
  - 共享用量包（¥5,000/个）：625,000 Credits/个
  - 单次消耗的 Credits 由模型类型、Token 用量、思考模式及工具调用等动态决定，实际消耗以账单为准。
  - 以 Qwen3.6-plus 为例，每 5000 输入未命中缓存 token、每 25000 输入命中缓存 token、每 5000/6 输出 token 为一个 Credit
  - 如果按 256K 以内的上下文算，一个 Credit 对应的 API 价格（隐式缓存）是 0.01 元，按 256K-1M 的上下文，一个 Credit 对应 0.04 元
  - 支持的模型：
    - 文本生成：qwen3.6-plus、glm-5、MiniMax-M2.5、deepseek-v3.2
    - 图像生成：qwen-image-2.0、qwen-image-2.0-pro、wan2.7-image、wan2.7-image-pro
- [腾讯云大模型 Coding Plan](https://cloud.tencent.com/act/pro/codingplan)
  - Lite 套餐（40 RMB 每月）：每 5 小时：最多约 1,200 次请求，每周：最多约 9,000 次请求，每订阅月：最多约 18,000 次请求
  - Pro 套餐（200 RMB 每月）：每 5 小时：最多约 6,000 次请求，每周：最多约 45,000 次请求，每订阅月：最多约 90,000 次请求
  - 支持模型：Tencent HY 2.0 Instruct、Tencent HY 2.0 Think、Hunyuan-T1、Hunyuan-TurboS、MiniMax-M2.5、Kimi-K2.5、GLM-5
- [腾讯云大模型 Token Plan](https://cloud.tencent.com/act/pro/tokenplan)
  - Lite 套餐（39 RMB 每月）：每订阅月 3500 万 Token
  - Standard 套餐（99 RMB 每月）：每订阅月 1 亿 Token
  - Pro 套餐（299 RMB 每月）：每订阅月 3.2 亿 Token
  - Max 套餐（599 RMB 每月）：每订阅月 6.5 亿 Token
  - 支持模型：Tencent HY 2.0 Instruct、Tencent HY 2.0 Think、Hunyuan-T1、Hunyuan-TurboS、MiniMax-M2.5、Kimi-K2.5、GLM-5
- [百度千帆 Coding Plan](https://cloud.baidu.com/product/codingplan.html)
  - Lite 套餐（40 RMB 每月）：每 5 小时：最多 1,200 次请求，每周：最多 9,000 次请求，每订阅月：最多 18,000 次请求
  - Pro 套餐（200 RMB 每月）：每 5 小时：最多 6,000 次请求，每周：最多 45,000 次请求，每订阅月：最多 90,000 次请求
  - 支持模型：Kimi-K2.5、DeepSeek-V3.2、GLM-5、MiniMax-M2.5、ERNIE-4.5-Turbo-20260402
- [京东云 Coding Plan](https://docs.jdcloud.com/cn/jdaip/PackageOverview)
  - Lite 套餐（新用户首月 7.9 RMB）：每 5 小时：最多 1,200 次请求，每周：最多 9,000 次请求，每订阅月：最多 18,000 次请求
  - Pro 套餐（新用户首月 39.9 RMB）：每 5 小时：最多 6,000 次请求，每周：最多 45,000 次请求，每订阅月：最多 90,000 次请求
  - 支持模型：DeepSeek-V3.2、GLM-5、GLM-4.7、MiniMax-M2.5、Kimi-K2.5、Kimi-K2-Turbo、Qwen3-Coder
- [讯飞星辰 Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html)
  - 首月版（2026 年 3 月 9 日上线，4 月 9 日起不再支持购买）：
    - 入门版（3.9 RMB 每月首购，19 RMB 每月叠加）：每日 2000 万 tokens，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash 模型，QPS=20
    - 专业版（7.9 RMB 每月首购，39 RMB 每月叠加）：每日 1000 万 tokens，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash、GLM-5、MiniMax-M2.5、Kimi-K2.5 模型，QPS=5
    - 高效版（39.9 RMB 每月首购，199 RMB 每月叠加）：每日 5000 万 tokens，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash、GLM-5、MiniMax-M2.5、Kimi-K2.5 模型，QPS=20
  - 焕新版（2026 年 4 月 9 日上线）
    - 无忧版（3.9 RMB 每月首购，19 RMB 每月重复购买）：请求次数不限，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash 模型
    - 专业版（39 RMB 每月）：每 5 小时：最多约 1,200 次请求；每周：最多约 9,000 次请求；每订阅月：最多约 18,000 次请求，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash、GLM-5、MiniMax-M2.5、Kimi-K2.5、Spark X2 模型
    - 高效版（199 RMB 每月）：每 5 小时：最多约 1,200 次请求；每周：最多约 9,000 次请求；每订阅月：最多约 18,000 次请求，支持 Qwen3.5-35B-A3B、DeepSeek-V3.2、GLM-4.7-Flash、GLM-5、MiniMax-M2.5、Kimi-K2.5、Spark X2 模型
- [天翼云 Coding Plan](https://www.ctyun.cn/document/11061839/11092368)
  - GLM Lite 套餐（49 RMB/月）：每 5 小时最多约 80 次 prompts，每周最多约 400 次 prompts，每月最多约 1,600 次 prompts，支持 GLM-5.1、GLM-5-Turbo、GLM-4.7、GLM-4.6、GLM-4.5、GLM-4.5-Air 模型
  - GLM Pro 套餐（149 RMB/月）：每 5 小时最多约 400 次 prompts，每周最多约 2,000 次 prompts，每月最多约 8,000 次 prompts，支持 GLM-5.1、GLM-5、GLM-5-Turbo、GLM-4.7、GLM-4.6、GLM-4.5、GLM-4.5-Air 模型
  - GLM Max 套餐（469 RMB/月）：每 5 小时最多约 1,600 次 prompts，每周最多约 8,000 次 prompts，每月最多约 32,000 次 prompts，支持 GLM-5.1、GLM-5、GLM-5-Turbo、GLM-4.7、GLM-4.6、GLM-4.5、GLM-4.5-Air 模型
  - GLM-5.1、GLM-5、GLM-5-Turbo 作为高阶模型，对标 Claude Opus，调用时将按照“高峰期 3 倍，非高峰期 2 倍”系数消耗额度；我们推荐您在复杂任务上切换至 GLM-5.1 处理，普通任务上继续使用 GLM-4.7，以避免套餐用量额度消耗过快。（作为限时福利，GLM-5.1、GLM-5-Turbo 将在非高峰期仅作为 1 倍抵扣，持续到 4 月底）注：高峰期为每日的 14:00～18:00

### 其他

- [无问芯穹 Infini Coding Plan](https://docs.infini-ai.com/gen-studio/coding-plan/)

  - Lite（40 RMB 每月）: 固定月费，每月 12000 次请求，每周 6000 次，每 5 小时 1000 次
  - Pro（200 RMB 每月）: 固定月费，每月 60000 次请求，每周 30000 次，每 5 小时 5000 次
  - 支持模型：DeepSeek-v3.2、Kimi-K2.5、MiniMax-M2.1、MiniMax-M2.5、MiniMax-M2.7、GLM-4.7、GLM-5、GLM-5.1

- [阶越星辰 Coding Plan](https://platform.stepfun.com/docs/zh/step-plan/overview)

  - Flash Mini（49 RMB 每月）：5 小时限额 100 次 Prompt（~1500 次模型调用），周限额 400 次 Prompt（~6000 次模型调用）
  - Flash Plus（99 RMB 每月）：5 小时限额 400 次 Prompt（~6000 次模型调用），周限额 1600 次 Prompt（~24000 次模型调用）
  - Flash Pro（199 RMB 每月）：5 小时限额 1500 次 Prompt（~22500 次模型调用），周限额 6000 次 Prompt（~90000 次模型调用）
  - Flash Max（699 RMB 每月）：5 小时限额 5000 次 Prompt（~75000 次模型调用），周限额 20000 次 Prompt（~300000 次模型调用）

- [小米 MiMo Token Plan](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription)

  - Lite（39 RMB 或 6 USD 每月）：6000 万 Credits 每月
  - Standard（99 RMB 或 16 USD 每月）：2 亿 Credits 每月
  - Pro（329 RMB 或 50 USD 每月）：7 亿 Credits 每月
  - Max（659 RMB 或 100 USD 每月）：16 亿 Credits 每月
  - 支持模型：各套餐均支持 MiMo-V2-Pro、MiMo-V2-Omni、MiMo-V2-TTS
  - 额度消耗：按 Token 数扣除 Credit 额度，Pro 和 Omni 的额度按 1:2 比例并行消耗，不是独立消耗。MiMo-V2-TTS 限时免费，不消耗套餐 Token。例如，您订购了 Standard 套餐，可单独或混合调用 MiMo-V2-Pro/Omni/TTS 模型，当您使用了 10M MiMo-V2-Pro 的 Token 额度后，相当于消耗了 20 M Credits，仍可享受 40M MiMo-V2-Omni 的 Token 额度（相当于 40 M Credits）。可在 订阅管理 查看当前套餐的额度及用量。
  - MiMo-V2-Omni 上下文 < 256k：1x（等同于原始 Token 消耗速度）
  - MiMo-V2-Pro 上下文 < 256k：2x（等同于 2 倍 Token 消耗速度）
  - MiMo-V2-Pro 上下文 256k~1M：4x（等同于 4 倍 token 消耗速度）
  - MiMo-V2-TTS：0x（限时免费，不消耗 Credit）

- [阶越星辰国际版 Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)

- [联通元景 GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)

- [摩尔线程 AI Coding Plan](https://code.mthreads.com/)

- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)

## prompt、请求和 token

- prompt：用户输入提示词到 CLI，按回车发出去，从请求来看，就是最后一个消息是来自用户的，而非 tool call result
- 请求：除了 prompt 本身会有一次请求以外，每轮 tool call 结束后，会把 tool call 结果带上上下文再发送请求，直到没有 tool call 为止
- token：每次请求都有一定量的 input 和 output tokens

一次 prompt 对应多次请求，每次请求都有很多的 input 和 output tokens。其中部分 input tokens 会命中缓存。实际测试下来，在 Vibe Coding 场景下，input + output tokens 当中：

- input tokens 占比 99.5%，因为多轮对话下来，input tokens 会不断累积变多，被重复计算
  - 其中 cached tokens 占 input + output tokens 约 90-95%
- output tokens 占比 0.5%

## 常见 API 定价方式

- OpenAI 模式：自动缓存，有输入未命中缓存价格、输入命中缓存价格和输出价格
  - OpenAI 有 Input，Cached Input 和 Output 三种价格，如果访问没有命中缓存，不命中的部分按 Input 收费，OpenAI 可能会进行缓存；如果访问命中缓存，命中的部分按 Cached Input 收费
  - 通常 Cached Input 是 0.1 倍的 Input 价格，也有 0.1-0.2 倍之间的
- Anthropic 模式：手动缓存，有输入未命中缓存价格、输入命中缓存价格、带缓存写入的输入价格（不同的 TTL 可能对应不同的价格）和输出价格
  - Claude 有 Base Input Tokens，5m Cache Writes，1h Cache Writes，Cache Hits & Refreshes 和 Output Tokens 五种价格，如果不使用缓存，那么每次输入都按 Base Input Tokens 收费；如果使用缓存，写入缓存部分的输入按 5m/1h Cache Writes 收费，之后命中缓存部分的输入按 Cache Hits & Refreshes 收费
  - 目前 5m Cache Writes 是 1.25 倍的 Base Input Tokens 价格，1h Cache Writes 是 2 倍的 Base Input Tokens 价格，Cache Hits & Refreshes 是 0.1 倍的 Base Input Tokens 价格

## 模型参数比较

| 模型名称                                                           | 参数量 | 激活量 | 视觉 |
| ------------------------------------------------------------------ | ------ | ------ | ---- |
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)           | 1T     | 32B    | 是   |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                  | 744B   | 40B    | 否   |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                  | 355B   | 32B    | 否   |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)      | 30B    | 3B     | 否   |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)      | 230B   | 10B    | 否   |
| [DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2)  | 671B   | 37B    | 否   |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | 397B   | 17B    | 是   |

## 更新历史

- 2026/04/23：GLM Coding Plan 将于 2026 年 4 月 30 日统一关闭老套餐（无周限额版本）的自动续订，当前已生效周期不受影响；同时，系统会自动为受影响用户赠送 2 个月同等级新套餐，在当前套餐到期后顺延生效，无需手动领取。详见[《老套餐迁移与补偿说明》](https://docs.bigmodel.cn/cn/coding-plan/transition)。

- 2026/04/22：方舟 Coding Plan 上线 MiniMax-M2.7、Kimi-K2.6、GLM-5.1

- 2026/04/21：阿里云百炼 Token Plan 团队版上线

- 2026/04/21：Kimi 正式发布 Kimi-K2.6 模型

- 2026/04/14：Kimi Code 上线 K2.6-code-preview 模型

- 2026/04/12：智谱国际版 GLM Coding Plan 起步价从 10 USD 每月涨至 18 USD 每月

- 2026/04/11：阿里云百炼 Coding Plan Lite 基础套餐于 2026 年 4 月 13 日起停止续费和升级，此前已于 2026 年 3 月 19 日停止新购

- 2026/04/11：添加了天翼云 Coding Plan

- 2026/04/09：无问芯穹 Infini Coding Plan 新增支持 glm-5.1 模型

- 2026/04/09：智谱 Coding Plan 下线了 GLM-5、GLM-4.6、GLM-4.5 模型

- 2026/04/08：讯飞 Astron Coding Plan 上线了新的焕新版套餐，旧首月版套餐下线

- 2026/04/08：阿里云百炼 Coding Plan 新增推荐模型 qwen3.6-plus（支持图片理解），仅 Pro 套餐可用，qwen3.5-plus 从推荐模型降级为更多模型

- 2026/04/07：百度千帆 Coding Plan 下线了 GLM-4.7 和 MiniMax-M2.1，新增 ERNIE-4.5-Turbo-20260402

- 2026/04/03：添加了小米 MiMo Token Plan

- 2026/04/03：添加了京东云 Coding Plan

- 2026/04/03：添加了阶跃星辰 Coding Plan

- 2026/03/27：GLM-5.1 上线 GLM Coding Plan

- 2026/03/27：添加了腾讯云大模型 Token Plan，相比 Coding Plan，用 Token 计限额而不是请求数

- 2026/03/26：GLM-5-Turbo 对所有 GLM Coding Plan 开放使用，之前仅对 Max 开放

- 2026/03/21：MiniMax Token Plan 把 Starter Plan 加了回来，价格和限额不变；此外还加入了每周限额，是每 5 小时限额的 10 倍

- 2026/03/19：阿里云百炼 Coding Plan 发布[公告](https://www.aliyun.com/notice/118094)，从北京时间 2026-03-20 00:00:00 停止新购 Coding Plan Lite 基础套餐

- 2026/03/19：无问芯穹 Infini Coding Plan 新增了第三方模型 minimax-m2.7 的支持

- 2026/03/18：MiniMax Token Plan 去掉了 MiniMax-M2.7-highspeed 版本消耗两倍请求的表述

- 2026/03/18：MiniMax-M2.7 上线，同时 MiniMax Coding Plan 改名为 MiniMax Token Plan，支持非文本的 LLM（如音频和视频）；Token Plan 去除了 Starter Plan，把表述从 Prompt 改成了请求，实际限额不变（之前也是按 1 prompt 等于 15 请求来限额）

- 2026/03/17：添加了讯飞星辰 MaaS Astron Coding Plan

- 2026/03/16：智谱上线了 GLM-5-Turbo 模型，描述如下：

  - 面向 OpenClaw 龙虾场景深度优化的基座模型
  - 强化了对外部工具与各类 Skills 的调用能力，在多步任务中更稳定、更可靠
  - 复杂指令拆解更强，能够精准识别目标、规划步骤，并支持多智能体之间的协同分工
  - 能够更好理解时间维度上的要求，在复杂长任务中保持执行连续性
  - 针对数据吞吐量大、逻辑链条长的龙虾任务，进一步提升了执行效率与响应稳定性
  - GLM-5-Turbo 套餐可用情况：Max 套餐已支持，Pro 预计 3 月底支持，Lite 预计 4 月内支持
  - GLM-5 套餐可用情况：Max 与 Pro 套餐均已支持，Lite 预计 3 月底支持
  - GLM-5、GLM-5-Turbo 作为高阶模型，对标 Claude Opus，调用时将按照“高峰期 3 倍，非高峰期 2 倍”系数消耗额度；我们推荐您在复杂任务上切换至 GLM-5 处理，普通任务上继续使用 GLM-4.7，以避免套餐用量额度消耗过快。（作为限时福利，GLM-5-Turbo 将在非高峰期仅作为 1 倍抵扣，持续到 4 月底）注：高峰期为每日的 14:00～18:00（UTC+8）

- 2026/03/08：腾讯云大模型 Coding Plan 上线

- 2026/03/07：智谱发放了 GLM Coding Plan 15 日补偿赠金，邮件全文如下：

  ```text
  亲爱的 GLM Coding Plan 用户，


  感谢您的继续支持与信任。


  针对近期部分用户在使用过程中遇到的体验问题，为表达我们的歉意与感谢您的理解，我们已为您发放 等值于您当前订阅套餐 15 天订阅费用的补偿赠金（无使用有效期限制）。该赠金已发放至您的账户，您可前往「智谱开放平台后台 - 财务 - 充值明细」查看到账详情，并在后续使用中进行抵扣。


  再次感谢您的理解与耐心，也感谢您一直以来对我们的包容与支持。我们会持续优化产品能力与服务质量，努力为您带来更加稳定、高效的开发体验。


  祝您使用愉快！


  智谱大模型开放平台

  2026 年 3 月 7 日
  ```

- 2026/03/06：方舟 Coding Plan 新增了第三方模型 MiniMax-M2.5 的支持

- 2026/02/25：阿里云百炼 Coding Plan 新增了第三方模型 minimax-m2.5 的支持

- 2026/02/24：阿里云百炼 Coding Plan 新增了第三方模型 glm-5 的支持

- 2026/02/21：观测到阿里云百炼 Coding Plan 新增了第三方模型 glm-4.7 和 kimi-k2.5 的支持，之前只有 qwen 自己的模型

- 2026/02/18：Kimi Code 的计费方式出现了新变化：

  - 此前是每周的限额从 50M input + output tokens 改成了 4M uncached input + output tokens，而每 5 小时的限额依然是 10M input + output tokens
  - 现在每 5 小时的限额改成了 1M uncached input + output tokens
  - 因此现在每 5 小时的限额与每周的限额有一个 4 倍的关系
  - 按 99.5% input（其中 95% cached, 5% uncached）+ 0.5% output 的比例的话，新旧算法的限额比较如下：
    - 旧每周限额 50M input + output tokens：`50M*0.5%=250K` output tokens
    - 新每周限额 4M uncached input + output tokens：`4M*0.5%/(0.5%+99.5%*5%)=365K` output tokens
    - 旧每 5 小时限额 10M input + output tokens：`10M*0.5%=50K` output tokens
    - 新每 5 小时限额 1M uncached input + output tokens：`1M*0.5%/(0.5%+99.5%*5%)=91K` output tokens
  - 按 99.5% input（其中 90% cached, 10% uncached）+ 0.5% output 的比例的话，新旧算法的限额比较如下：
    - 旧每周限额 50M input + output tokens：`50M*0.5%=250K` output tokens
    - 新每周限额 4M uncached input + output tokens：`4M*0.5%/(0.5%+99.5%*10%)=191K` output tokens
    - 旧每 5 小时限额 10M input + output tokens：`10M*0.5%=50K` output tokens
    - 新每 5 小时限额 1M uncached input + output tokens：`1M*0.5%/(0.5%+99.5%*10%)=48K` output tokens
  - 可见新旧限额下，哪个等效的限额更高，取决于缓存的命中率

- 2026/02/16：GLM Coding Plan 调高了每周限额，从每 5 小时限额的 4 倍（320/1600/6400 prompts）提高到了 5 倍（400/2000/8000 prompts），同时 GLM-5 对用量的消耗速度从 3 倍改成高峰期 3 倍，非高峰期 2 倍（高峰期为每日的 14:00～18:00（UTC+8））

- 2026/02/16：最近发现 Kimi Code 的计费方式有一些变化：

  - Andante 套餐每 5 小时的限额不变还是 10M input + output tokens，但每周的限额，表现为开一个新的 Code Session 时用的比较快，明显不是每 5 小时用量的 20%（之前的推算结果里，每周的限额是 5 倍的每 5 小时的限额），但慢慢用下来，比例还是在 20% 附近，按照之前的方法推算，每周的用量大概是 48M input + output tokens 而非原来的 50M，是个比较奇怪的数字
  - 这个疑问被 [LLM 推理系统、Code Agent 与电网 - 许欣然](https://zhuanlan.zhihu.com/p/2006506955775169424) 解释了：cached tokens 不计入用量
  - 如果按照 uncached input + output tokens 来推算，那么每周的用量就是 4M uncached input + output tokens；而 5 小时的限制应该还是老的算法，10M input + output tokens
  - 这样做的目的是，如果把 Kimi Code 用于一些 cache 比例很低的非 Vibe Coding 场景，那么每周的限额会消耗地很快
  - 扩展阅读：[suspiciously precise floats, or, how I got Claude's real limits](https://she-llac.com/claude-limits)

- 2026/02/15：MiniMax Coding Plan 添加了 Plus/Max/Ultra 极速版

- 2026/02/14: GLM Coding Plan 添加了每周的限额，是每 5 小时限额的 4 倍（Kimi 是 5 倍，方舟和阿里是 7.5 倍），同时 GLM-5 对限额的消耗速度是 GLM-4.7 的三倍

  - 不正经评语：看来在智谱，一周只用上四天班，每天工作 5 小时，而在 Moonshot 一周需要上五天班，在字节和阿里要每周上 7.5 天的班，哪个公司加班多一目了然，狗头（但字节和阿里一个月只用上两周，其他两周不上班，这就是“大小周”吗）
  - 正经评语：新 GLM Coding Plan 的性价比一下从夯降低到 NPC 的水平，那么 Kimi/MiniMax 的性价比就显现出来了，解决办法是继续续订老套餐，坚持 GLM-4.7 不动摇
  - 如果按照新套餐是原来的 2/3 限额折算，按 GLM-4.7 计算，那么 Lite 套餐每月（按 30 天算）可以用 `40M*2/3*4*30/7=457M` tokens；按 GLM-5 计算，则是 `40M*2/3*4*30/7/3=152M` tokens

- 2026/02/12：GLM Coding Plan 价格从 40/200/400 RMB 每月改成 49/149/469 RMB 每月；与此同时，用量额度减少了，变成了原来的 2/3：

  - Lite 套餐：每 5 小时最多约 80（原来是 120）次 prompts，相当于 Claude Pro 套餐用量的 3 倍
  - Pro 套餐：每 5 小时最多约 400（原来是 600）次 prompts，相当于 Lite 套餐用量的 5 倍
  - Max 套餐：每 5 小时最多约 1600（原来是 2400）次 prompts，相当于 Pro 套餐用量的 4 倍
  - 如果按照新是旧的 2/3 比例的话，那 Lite 套餐限额就是每 5 小时 `40/3*2=27M` tokens，另外新版还有每周的限额（2026/02/14 发布了具体规则见上）；待切换到新套餐后（不打算切了），再测试新版的用量限制对应多少 tokens（有读者感兴趣可以测完反馈一下）

- 2026/02/12：增加 Kimi Allegro 套餐的描述

- 2026/02/12：随着 GLM-5 的发布，GLM Coding Plan 的 quota/limit 接口不再返回具体的 token 数，应该是为了之后 GLM-5 与 GLM-4.7 以不同的速度消耗用量做准备（根据 API 价格猜测会有个 2 倍的系数？等待后续的测试），但目前测下来 GLM-4.7 的用量限制不变，Lite 套餐依然是输入加输出 40M tokens 每 5 小时；由于只有每 5 小时的限额，按每月 30 天算，理论上每月最多可以用到 `30*24/5*40=5760M` tokens

- 2026/01/30：通过实际测试，猜测 GLM Coding Plan 的 Lite 套餐用量限制是每 5 小时所有请求的 input + output tokens 总和不超过 40M tokens（意味着每次 prompt 对应 40M/120=333K tokens），这和 <https://open.bigmodel.cn/api/monitor/usage/quota/limit> 接口返回的结果一致（2026/02/12 后该接口只返回百分比，不返回 token 数）
