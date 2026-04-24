# AI Coding Plan

## Coding Plan

### Kimi

[Kimi Membership](https://www.kimi.com/membership/pricing)

- Andante (49 RMB/month): A 5-hour token quota supports approximately 300–1,200 API calls, with a maximum concurrency of 30, ensuring uninterrupted operation for complex workloads
- Moderato (99 RMB/month): 4x Kimi Code quota
- Allegretto (199 RMB/month): 20x Kimi Code quota
- Allegro (699 RMB/month): 60x Kimi Code quota
- Based on actual testing, Andante limits total uncached input + output tokens to 1M per 5 hours (i.e. not counting cached input tokens), 4M per week
- [K2.6 API Pricing](https://platform.moonshot.cn/docs/pricing/chat):
    - Cached input: 1.1 RMB per 1M tokens
    - Uncached input: 6.5 RMB per 1M tokens
    - Output: 27 RMB per 1M tokens
    - 256K context

### MiniMax

[MiniMax Token Plan](https://platform.minimaxi.com/docs/token-plan/intro) [Pricing](https://platform.minimaxi.com/docs/guides/pricing-token-plan)

- Starter (29 RMB/month): 600 requests / per 5 hours
- Plus (49 RMB/month): 1,500 requests / per 5 hours
- Max (119 RMB/month): 4,500 requests / per 5 hours
- Plus-Highspeed (98 RMB/month): 1,500 requests / per 5 hours
- Max-Highspeed (199 RMB/month): 4,500 requests / per 5 hours
- Ultra-Highspeed (899 RMB/month): 30,000 requests / per 5 hours
- The Token Plan usage quota is calculated per model:
    - M2.7 / M2.7-highspeed: Measured by requests, with a 5-hour rolling reset.
    - Other models (speech, video, music, image): Measured by daily quotas, resetting daily.
- All plans include the latest MiniMax M2.7 model, with M2.7-highspeed availability based on resource load. High-Speed subscriptions offer dedicated M2.7-highspeed support for even faster inference.
- Weekly Usage Quota: The current weekly usage quota is 10 times the “5-hour quota” (industry common range is 5–8 times)
- [M2.7 API Pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo):
    - Cached input: 0.42 RMB per 1M tokens
    - Uncached input: 2.1 RMB per 1M tokens
    - Cache write input: 2.625 RMB per 1M tokens
    - Output: 8.4 RMB per 1M tokens
    - 200K context

[MiniMax International Token Plan](https://platform.minimax.io/docs/token-plan/intro) [Pricing](https://platform.minimax.io/docs/guides/pricing-token-plan)

- Starter (10 USD/month): 1,500 requests / per 5 hours
- Plus (20 USD/month): 4,500 requests / per 5 hours
- Max (50 USD/month): 15,000 requests / per 5 hours
- Plus-High-Speed (40 USD/month): 4,500 requests / per 5 hours
- Max-High-Speed (80 USD/month): 15,000 requests / per 5 hours
- Ultra-High-Speed (150 USD/month): 30,000 requests / per 5 hours

### Zhipu (GLM, Z.ai)

[Zhipu GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite Plan (49 RMB/month): Maximum ~80 prompts per 5 hours, maximum ~400 prompts per week
- Pro Plan (149 RMB/month): Maximum ~400 prompts per 5 hours, maximum ~2000 prompts per week
- Max Plan (469 RMB/month): Maximum ~1600 prompts per 5 hours, maximum ~8000 prompts per week
- One prompt refers to one query. Each prompt is estimated to invoke the model 15–20 times. The monthly available quota is converted based on API pricing, equivalent to approximately 15–30× the monthly subscription fee (weekly caps already factored in).
- Note: The above figures are estimates. Actual available usage may vary depending on project complexity, repository size, and whether auto-accept is enabled.
- Note: All plans support GLM-5.1, GLM-5-Turbo, GLM-4.7 and GLM-4.5-Air.
- Note: GLM-5.1 and GLM-5-Turbo are advanced models designed to rival Claude Opus model. Its usage will be deducted at 3 × during peak hours and 2 × during off-peak hours. We recommend switching to GLM-5.1 for complex tasks and continuing to use GLM-4.7 for routine tasks to avoid rapid quota consumption. As a limited-time benefit, GLM-5.1 and GLM-5-Turbo will only consume 1× quota during off-peak hours, valid through the end of April.
- [GLM-5-Turbo API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 1.2/1.8 RMB per 1M tokens
    - Uncached input: 5/7 RMB per 1M tokens
    - Output: 22/26 RMB per 1M tokens
    - 200K context
- [GLM-5.1 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 1.3/1.2 RMB per 1M tokens
    - Uncached input: 6/8 RMB per 1M tokens
    - Output: 24/28 RMB per 1M tokens
    - 200K context
- [GLM-4.7 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 0.4/0.6/0.8 RMB per 1M tokens
    - Uncached input: 2/3/4 RMB per 1M tokens
    - Output: 8/14/16 RMB per 1M tokens
    - 200K context

[Zhipu International GLM Coding Plan](https://z.ai/subscribe)

### Cloud Providers

- [Volcano Engine Coding Plan](https://www.volcengine.com/activity/codingplan)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum ~1,200 requests. Per week: maximum ~9,000 requests. Per subscription month: maximum ~18,000 requests.
    - Pro Plan (200 RMB/month): 5x the Lite Plan quota
    - Supported models: Doubao-Seed-2.0-Code, Doubao-Seed-2.0-pro, Doubao-Seed-2.0-lite, Doubao-Seed-Code, MiniMax-M2.7, MiniMax-2.5, Kimi-K2.6, Kimi-K2.5, GLM-5.1, GLM-4.7, DeepSeek-v3.2, Doubao-Embedding-Vision
- [Alibaba Bailian Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
    - Pro Plan (200 RMB/month): Fixed monthly fee, 90,000 requests per month, 45,000 per week, 6,000 per 5 hours
    - Lite Plan was suspended from new purchases on March 19, 2026, and will stop accepting renewals and upgrades from April 13, 2026. Existing users can continue using it until expiration. See [announcement](https://www.aliyun.com/notice/118175)
    - One user question may trigger multiple model calls; each model call counts as one quota consumption. Typical quota consumption scenarios:
    - Simple Q&A or code generation: usually triggers 5-10 model calls
    - Code refactoring or complex tasks: may trigger 10-30 or more model calls
    - Actual quota consumption depends on task complexity, context size, number of tool calls, and other factors. Specific consumption is based on actual usage; you can view plan quota consumption in the Coding Plan console.
    - Recommended models: qwen3.6-plus, kimi-k2.5, glm-5, minimax-m2.5. More models: qwen3.5-plus, qwen3-max-2026-01-23, qwen3-coder-next, qwen3-coder-plus, glm-4.7
    - [Qwen3.6-Plus API Pricing](https://help.aliyun.com/zh/model-studio/models)：
        - Input: 2/8 RMB per 1M tokens
        - Output: 12/48 RMB per 1M tokens
        - 1M context
    - [Qwen3-Max API Pricing](https://help.aliyun.com/zh/model-studio/models)：
        - Input: 2.5/4/7 RMB per 1M tokens
        - Output: 10/16/28 RMB per 1M tokens
        - 256K context
- [Alibaba Cloud Bailian Token Plan (Team Edition)](https://help.aliyun.com/zh/model-studio/token-plan-overview)
    - Standard Seat (¥198/seat/month): 25,000 Credits/seat/month
    - Advanced Seat (¥698/seat/month): 100,000 Credits/seat/month
    - Premium Seat (¥1,398/seat/month): 250,000 Credits/seat/month
    - Shared Usage Pack (¥5,000/pack): 625,000 Credits/pack
    - Credits consumed per request are dynamically determined by model type, token usage, reasoning mode, and tool calls. Actual consumption is based on the bill.
    - For example, with Qwen3.6-plus, every 5,000 uncached input tokens, every 25,000 cached input tokens, or every 5,000/6 output tokens equals one Credit
    - For contexts within 256K, one Credit corresponds to an API price (implicit caching) of 0.01 RMB; for contexts between 256K–1M, one Credit corresponds to 0.04 RMB
    - Supported models:
        - Text generation: qwen3.6-plus, glm-5, MiniMax-M2.5, deepseek-v3.2
        - Image generation: qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro
- [Tencent Cloud LLM Coding Plan](https://cloud.tencent.com/act/pro/codingplan)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum ~1,200 requests. Per week: maximum ~9,000 requests. Per subscription month: maximum ~18,000 requests
    - Pro Plan (200 RMB/month): Per 5 hours: maximum ~6,000 requests. Per week: maximum ~45,000 requests. Per subscription month: maximum ~90,000 requests
    - Supported models: Tencent HY 2.0 Instruct, Tencent HY 2.0 Think, Hunyuan-T1, Hunyuan-TurboS, MiniMax-M2.5, Kimi-K2.5, GLM-5
- [Tencent Cloud LLM Token Plan](https://cloud.tencent.com/act/pro/tokenplan)
    - Lite Plan (39 RMB/month): 35M tokens per subscription month
    - Standard Plan (99 RMB/month): 100M tokens per subscription month
    - Pro Plan (299 RMB/month): 320M tokens per subscription month
    - Max Plan (599 RMB/month): 650M tokens per subscription month
    - Supported models: Tencent HY 2.0 Instruct, Tencent HY 2.0 Think, Hunyuan-T1, Hunyuan-TurboS, MiniMax-M2.5, Kimi-K2.5, GLM-5
- [Baidu Qianfan Coding Plan](https://cloud.baidu.com/product/codingplan.html)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum 1,200 requests. Per week: maximum 9,000 requests. Per subscription month: maximum 18,000 requests
    - Pro Plan (200 RMB/month): Per 5 hours: maximum 6,000 requests. Per week: maximum 45,000 requests. Per subscription month: maximum 90,000 requests
    - Supported models: Kimi-K2.5, DeepSeek-V3.2, GLM-5, MiniMax-M2.5, ERNIE-4.5-Turbo-20260402
- [JD Cloud Coding Plan](https://docs.jdcloud.com/cn/jdaip/PackageOverview)
    - Lite Plan (7.9 RMB first month for new users): Per 5 hours: maximum 1,200 requests. Per week: maximum 9,000 requests. Per subscription month: maximum 18,000 requests
    - Pro Plan (39.9 RMB first month for new users): Per 5 hours: maximum 6,000 requests. Per week: maximum 45,000 requests. Per subscription month: maximum 90,000 requests
    - Supported models: DeepSeek-V3.2, GLM-5, GLM-4.7, MiniMax-M2.5, Kimi-K2.5, Kimi-K2-Turbo, Qwen3-Coder
- [iFlytek Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html)
    - First Month Edition (launched March 9, 2026, no longer available for purchase from April 9):
        - Starter (3.9 RMB first purchase/month, 19 RMB add-on/month): 20M tokens daily, supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash models, QPS=20
        - Professional (7.9 RMB first purchase/month, 39 RMB add-on/month): 10M tokens daily, supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash, GLM-5, MiniMax-M2.5, Kimi-K2.5 models, QPS=5
        - Efficient (39.9 RMB first purchase/month, 199 RMB add-on/month): 50M tokens daily, supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash, GLM-5, MiniMax-M2.5, Kimi-K2.5 models, QPS=20
    - Updated Edition (launched April 9, 2026):
        - Worry-Free (3.9 RMB first purchase/month, 19 RMB repeat purchase/month): Unlimited requests, supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash models
        - Professional (39 RMB/month): Per 5 hours: maximum ~1,200 requests; per week: maximum ~9,000 requests; per subscription month: maximum ~18,000 requests. Supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash, GLM-5, MiniMax-M2.5, Kimi-K2.5, Spark X2 models
        - Efficient (199 RMB/month): Per 5 hours: maximum ~1,200 requests; per week: maximum ~9,000 requests; per subscription month: maximum ~18,000 requests. Supports Qwen3.5-35B-A3B, DeepSeek-V3.2, GLM-4.7-Flash, GLM-5, MiniMax-M2.5, Kimi-K2.5, Spark X2 models
- [CTCloud Coding Plan](https://www.ctyun.cn/document/11061839/11092368)
    - GLM Lite Plan (49 RMB/month): Maximum ~80 prompts per 5 hours, maximum ~400 prompts per week, maximum ~1,600 prompts per subscription month. Supports GLM-5.1, GLM-5-Turbo, GLM-4.7, GLM-4.6, GLM-4.5, GLM-4.5-Air models
    - GLM Pro Plan (149 RMB/month): Maximum ~400 prompts per 5 hours, maximum ~2,000 prompts per week, maximum ~8,000 prompts per subscription month. Supports GLM-5.1, GLM-5, GLM-5-Turbo, GLM-4.7, GLM-4.6, GLM-4.5, GLM-4.5-Air models
    - GLM Max Plan (469 RMB/month): Maximum ~1,600 prompts per 5 hours, maximum ~8,000 prompts per week, maximum ~32,000 prompts per subscription month. Supports GLM-5.1, GLM-5, GLM-5-Turbo, GLM-4.7, GLM-4.6, GLM-4.5, GLM-4.5-Air models
    - Note: GLM-5.1, GLM-5, and GLM-5-Turbo are advanced models designed to rival Claude Opus. Their usage will be deducted at 3× during peak hours and 2× during off-peak hours. We recommend switching to GLM-5.1 for complex tasks and continuing to use GLM-4.7 for routine tasks to avoid rapid quota consumption. As a limited-time benefit, GLM-5.1 and GLM-5-Turbo will only consume 1× quota during off-peak hours, valid through the end of April. Peak hours are 14:00–18:00 (UTC+8).

### Others

- [Infini-AI Coding Plan](https://docs.infini-ai.com/gen-studio/coding-plan/)
    - Lite (40 RMB/month): Fixed monthly fee, 12,000 requests per month, 6,000 per week, 1,000 per 5 hours
    - Pro (200 RMB/month): Fixed monthly fee, 60,000 requests per month, 30,000 per week, 5,000 per 5 hours
    - Supported models: DeepSeek-v3.2, Kimi-K2.5, MiniMax-M2.1, MiniMax-M2.5, MiniMax-M2.7, GLM-4.7, GLM-5, GLM-5.1
- [StepFun Coding Plan](https://platform.stepfun.com/docs/zh/step-plan/overview)
    - Flash Mini (49 RMB/month): 100 prompts per 5 hours (~1,500 model calls), 400 prompts per week (~6,000 model calls)
    - Flash Plus (99 RMB/month): 400 prompts per 5 hours (~6,000 model calls), 1,600 prompts per week (~24,000 model calls)
    - Flash Pro (199 RMB/month): 1,500 prompts per 5 hours (~22,500 model calls), 6,000 prompts per week (~90,000 model calls)
    - Flash Max (699 RMB/month): 5,000 prompts per 5 hours (~75,000 model calls), 20,000 prompts per week (~300,000 model calls)
    - Supported models: step-3.5-flash-2603, step-3.5-flash, stepaudio-2.5-tts, stepaudio-2.5-asr
- [Xiaomi MiMo Token Plan](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription)
    - Lite (39 RMB or 6 USD/month): 60M Credits per month
    - Standard (99 RMB or 16 USD/month): 200M Credits per month
    - Pro (329 RMB or 50 USD/month): 700M Credits per month
    - Max (659 RMB or 100 USD/month): 1.6B Credits per month
    - Supported models: All plans support MiMo-V2-Pro, MiMo-V2-Omni, MiMo-V2-TTS
    - Credit consumption: Credits are deducted based on token count. Pro and Omni quotas are consumed in parallel at a 1:2 ratio, not independently. MiMo-V2-TTS is free for a limited time and does not consume plan tokens. For example, if you subscribe to the Standard plan and use 10M MiMo-V2-Pro tokens, that consumes 20M Credits, and you can still enjoy 40M MiMo-V2-Omni tokens (equivalent to 40M Credits). You can check your current plan's quota and usage in Subscription Management.
    - MiMo-V2-Omni context < 256k: 1x (equivalent to base token consumption rate)
    - MiMo-V2-Pro context < 256k: 2x (equivalent to 2x token consumption rate)
    - MiMo-V2-Pro context 256k–1M: 4x (equivalent to 4x token consumption rate)
    - MiMo-V2-TTS: 0x (free for a limited time, no Credit consumption)

- [StepFun International Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)
- [UniAI GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)
- [Moorethreads AI Coding Plan](https://code.mthreads.com/)
- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)

## Prompts, Requests, and Tokens

- Prompt: User inputs a prompt into the CLI and presses Enter to send it. From the request perspective, it's when the last message is from the user, not from a tool call result.
- Request: In addition to the prompt itself generating one request, after each round of tool calls, the tool call results are sent along with the context until there are no more tool calls.
- Token: Each request has a certain amount of input and output tokens.

One prompt corresponds to multiple requests, and each request has many input and output tokens. Some input tokens will hit the cache. In actual testing in Vibe Coding scenarios, among input + output tokens:

- Input tokens account for 99.5%, because with multi-turn conversations, input tokens accumulate and are repeatedly counted
    - Among which cached tokens account for approximately 90-95% of input + output tokens
- Output tokens account for 0.5%

## Common API Pricing Models

- OpenAI Model: Automatic caching, with uncached input price, cached input price, and output price
    - OpenAI has three prices: Input, Cached Input, and Output. If the access doesn't hit the cache, the uncached portion is charged at the Input rate; OpenAI may perform caching; if the access hits the cache, the cached portion is charged at the Cached Input rate.
    - Typically Cached Input is 0.1x the Input price, sometimes between 0.1-0.2x.
- Anthropic Model: Manual caching, with uncached input price, cached input price, input price with cache write (different TTLs may correspond to different prices), and output price
    - Claude has five prices: Base Input Tokens, 5m Cache Writes, 1h Cache Writes, Cache Hits & Refreshes, and Output Tokens. If caching is not used, each input is charged at the Base Input Tokens rate; if caching is used, the portion written to cache is charged at the 5m/1h Cache Writes rate, and subsequent cache hits are charged at the Cache Hits & Refreshes rate.
    - Currently 5m Cache Writes are 1.25x the Base Input Tokens price, 1h Cache Writes are 2x the Base Input Tokens price, and Cache Hits & Refreshes are 0.1x the Base Input Tokens price.

## Model Parameters Comparison

| Name                                                               | Parameters | Active | Vision |
|--------------------------------------------------------------------|------------|--------|--------|
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)           | 1T         | 32B    | Y      |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                  | 744B       | 40B    | N      |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                  | 355B       | 32B    | N      |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)      | 30B        | 3B     | N      |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)      | 230B       | 10B    | N      |
| [DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2)  | 671B       | 37B    | N      |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | 397B       | 17B    | Y      |

## Update History

- 2026/04/23: StepFun Coding Plan added support for stepaudio-2.5-asr model
- 2026/04/23: GLM Coding Plan will uniformly disable auto-renewal for legacy plans (no weekly limit version) on April 30, 2026. Current active billing cycles are not affected. Meanwhile, the system will automatically gift affected users 2 months of equivalent new plan, which will take effect after the current plan expires, with no manual claim required. See [Legacy Plan Migration and Compensation Notice](https://docs.bigmodel.cn/cn/coding-plan/transition).
- 2026/04/22: Volcano Engine Coding Plan added MiniMax-M2.7, Kimi-K2.6, GLM-5.1
- 2026/04/21: Alibaba Cloud Bailian Token Plan (Team Edition) launched
- 2026/04/21: Kimi officially released Kimi-K2.6 model
- 2026/04/14: Kimi Code launched K2.6-code-preview model
- 2026/04/12: Zhipu International GLM Coding Plan starting price increased from 10 USD/month to 18 USD/month
- 2026/04/11: Alibaba Cloud Bailian Coding Plan Lite Plan will stop accepting renewals and upgrades from April 13, 2026. New purchases were already suspended on March 19, 2026
- 2026/04/11: Added CTCloud Coding Plan
- 2026/04/09: Infini-AI Coding Plan added support for glm-5.1 model
- 2026/04/09: Zhipu Coding Plan removed GLM-5, GLM-4.6, GLM-4.5 models
- 2026/04/08: iFlytek Astron Coding Plan launched new Updated Edition plans; old First Month Edition plans retired
- 2026/04/08: Alibaba Cloud Bailian Coding Plan added recommended model qwen3.6-plus (with image understanding), available only on the Pro plan. qwen3.5-plus was moved from recommended to more models
- 2026/04/07: Baidu Qianfan Coding Plan removed GLM-4.7 and MiniMax-M2.1, added ERNIE-4.5-Turbo-20260402
- 2026/04/03: Added Xiaomi MiMo Token Plan
- 2026/04/03: Added JD Cloud Coding Plan
- 2026/04/03: Added StepFun Coding Plan
- 2026/03/27: GLM-5.1 launched in GLM Coding Plan
- 2026/03/27: Added Tencent Cloud LLM Token Plan, which uses token-based limits instead of request counts compared to the Coding Plan
- 2026/03/26: GLM-5-Turbo is now available on all GLM Coding Plan tiers; previously only available on Max
- 2026/03/21: MiniMax Token Plan has brought back the Starter Plan, with the same pricing and limits. Additionally, a weekly limit has been introduced, which is 10 times the limit per 5 hours.
- 2026/03/19: Alibaba Cloud Bailian Coding Plan Release [Announcement](https://www.aliyun.com/notice/118094), new purchases of the Coding Plan Lite will be suspended from 2026-03-20 00:00:00 Beijing Time.
- 2026/03/19: Infini-AI Coding Plan added support for third-party model minimax-m2.7
- 2026/03/18: MiniMax Token Plan removed the statement that the MiniMax-M2.7-highspeed version consumes double the requests.
- 2026/03/18: MiniMax-M2.7 launched; meanwhile, MiniMax Coding Plan was renamed to MiniMax Token Plan, supporting non-text LLMs (e.g., audio and video). The Token Plan removed the Starter Plan and changed the description from "prompts" to "requests" though the actual limits remain unchanged (previously, the limit was also calculated as 1 prompt equaling 15 requests)
- 2026/03/17: Added iFlytek MaaS Astron Coding Plan
- 2026/03/18: Z.ai released GLM-5-Turbo model:
    - Designed for high-throughput OpenClaw lobster workloads, GLM-5-Turbo focuses on improving stability and efficiency in long-chain Agent tasks, enabling smoother execution for complex, multi-step workflows.
    - It strengthens tool and Skills integration and enhances complex instruction decomposition, allowing the model to better identify task goals, plan execution steps, coordinate across multiple agents, and maintain temporal consistency in extended tasks.
    - GLM-5 support in Coding Plan: Supported on both Max and Pro plans; expected to be available on the Lite plan by the end of March
    - GLM-5-Turbo support in Coding Plan: Supported on the Max plan; expected to be available on the Pro plan by the end of March and on the Lite plan sometime in April
    - GLM-5 and GLM-5-Turbo are advanced models designed to rival Claude Opus model. Its usage will be deducted at 3 × during peak hours and 2 × during off-peak hours. We recommend switching to GLM-5 for complex tasks and continuing to use GLM-4.7 for routine tasks to avoid rapid quota consumption. As a limited-time benefit, GLM-5-Turbo will only consume 1× quota during off-peak hours, valid through the end of April. Peak hours are 14:00–18:00 (UTC+8).
- 2026/03/08: Tencent Cloud LLM Coding Plan launched
- 2026/03/07: Zhipu issued a 15-day compensation credit for GLM Coding Plan. The translated email text is as follows (original was in Chinese):
    ```
    Dear GLM Coding Plan User,


    Thank you for your continued support and trust.


    To address the recent service issues some users experienced and to express our sincere apologies, we have credited your account with compensation equivalent to 15 days of your current subscription fee (with no expiration). You can view the credit details in your account dashboard under "Zhipu Open Platform Console - Billing - Transaction History", and it will be automatically applied to your future usage.


    Thank you again for your understanding and patience, as well as your ongoing support. We remain committed to improving our product capabilities and service quality to deliver a more stable and efficient development experience.


    Best regards,


    Zhipu AI Platform Team

    March 7, 2026
    ```
- 2026/03/06: Volcano Engine Coding Plan added support for third-party model MiniMax-M2.5
- 2026/02/25: Alibaba Bailian Coding Plan added support for third-party model minimax-m2.5
- 2026/02/24: Alibaba Bailian Coding Plan added support for third-party model glm-5
- 2026/02/21: Observed that Alibaba Bailian Coding Plan added support for third-party models glm-4.7 and kimi-k2.5; previously only Qwen's own models were available
- 2026/02/18: Kimi Code billing has changed:
    - Previously, the weekly limit was changed from 50M input + output tokens to 4M uncached input + output tokens, while the per-5-hour limit remained 10M input + output tokens
    - Now the per-5-hour limit has been changed to 1M uncached input + output tokens
    - Therefore, there is now a 4x relationship between the per-5-hour limit and the weekly limit
    - Assuming 99.5% input (95% cached, 5% uncached) + 0.5% output ratio, old vs new limit comparison:
        - Old weekly limit 50M input + output tokens: `50M*0.5%=250K` output tokens
        - New weekly limit 4M uncached input + output tokens: `4M*0.5%/(0.5%+99.5%*5%)=365K` output tokens
        - Old per-5-hour limit 10M input + output tokens: `10M*0.5%=50K` output tokens
        - New per-5-hour limit 1M uncached input + output tokens: `1M*0.5%/(0.5%+99.5%*5%)=91K` output tokens
    - Assuming 99.5% input (90% cached, 10% uncached) + 0.5% output ratio, old vs new limit comparison:
        - Old weekly limit 50M input + output tokens: `50M*0.5%=250K` output tokens
        - New weekly limit 4M uncached input + output tokens: `4M*0.5%/(0.5%+99.5%*10%)=191K` output tokens
        - Old per-5-hour limit 10M input + output tokens: `10M*0.5%=50K` output tokens
        - New per-5-hour limit 1M uncached input + output tokens: `1M*0.5%/(0.5%+99.5%*10%)=48K` output tokens
    - As can be seen, whether the new or old limit is more restrictive depends on the cache hit rate
- 2026/02/16: GLM Coding Plan increased weekly limits from 4x the per-5-hour limit (320/1600/6400 prompts) to 5x (400/2000/8000 prompts). Meanwhile, GLM-5 consumption rate changed from 3x to 3x during peak hours and 2x during off-peak hours (peak hours: 14:00-18:00 UTC+8 daily).
- 2026/02/16: Recently discovered some changes in Kimi Code billing:
    - The Andante plan's per-5-hour limit remains unchanged at 10M input + output tokens, but the weekly limit observed when opening a new Code Session depletes faster, clearly not being 20% of the per-5-hour usage (previous calculation showed weekly limit was 5x the per-5-hour limit). However, with continued use, the ratio stays around 20%. Calculated using the previous method, weekly usage is approximately 48M input + output tokens rather than the original 50M—a rather odd number.
    - This question was explained by [LLM Inference Systems, Code Agents, and Power Grids - Xu Xinran](https://zhuanlan.zhihu.com/p/2006506955775169424): cached tokens are not counted in usage.
    - If calculated by uncached input + output tokens, then weekly usage is 4M uncached input + output tokens; the 5-hour limit should still use the old calculation of 10M input + output tokens.
    - The purpose is that if Kimi Code is used for non-Vibe Coding scenarios with low cache hit rates, the weekly limit will be consumed quickly.
    - Further reading: [suspiciously precise floats, or, how I got Claude's real limits](https://she-llac.com/claude-limits)
- 2026/02/15: MiniMax Coding Plan added Plus/Max/Ultra High Speed versions
- 2026/02/14: GLM Coding Plan added weekly limits at 4x the per-5-hour limit (Kimi is 5x, Volcano and Alibaba are 7.5x). Meanwhile, GLM-5 consumes quota at 3x the rate of GLM-4.7.
    - Unserious comment: Looks like at Zhipu, you only work 4 days a week, 5 hours a day, while at Moonshot you work 5 days a week, and at ByteDance and Alibaba you work 7.5 days a week. Which company has more overtime is clear at a glance, lol. (But ByteDance and Alibaba only work for two weeks a month; the other two weeks are off, this is the "big week small weeks" system?)
    - Serious comment: The new GLM Coding Plan's cost-effectiveness dropped from "夯"(S-level) to "NPC"(C-level), making Kimi/MiniMax's value stand out. The solution is to continue renewing the old plan and stick with GLM-4.7.
    - If calculated using the new plan at 2/3 of the old quota limit, using GLM-4.7, the Lite plan can use `40M*2/3*4*30/7=457M` tokens per month (30 days); using GLM-5, it would be `40M*2/3*4*30/7/3=152M` tokens.
- 2026/02/12: GLM Coding Plan prices changed from 40/200/400 RMB/month to 49/149/469 RMB/month; meanwhile, usage quotas were reduced to 2/3 of the original:
    - Lite Plan: Maximum ~80 prompts per 5 hours (was 120), equivalent to 3x Claude Pro plan usage
    - Pro Plan: Maximum ~400 prompts per 5 hours (was 600), equivalent to 5x Lite plan usage
    - Max Plan: Maximum ~1600 prompts per 5 hours (was 2400), equivalent to 4x Pro plan usage
    - If using the 2/3 ratio, the Lite plan limit would be `40/3*2=27M` tokens per 5 hours. The new version also has weekly limits (specific rules published on 2026/02/14, see above). After switching to the new plan (I am not planning to), need to test what the new usage limits correspond to in tokens (interested readers can test and provide feedback).
- 2026/02/12: Added description for Kimi Allegro plan
- 2026/02/12: With the release of GLM-5, GLM Coding Plan's quota/limit API no longer returns specific token counts—presumably preparing for GLM-5 and GLM-4.7 to consume usage at different rates (based on API pricing, guessing there might be a 2x coefficient? Awaiting further testing). However, current testing shows GLM-4.7 usage limits remain unchanged; Lite plan is still 40M input + output tokens per 5 hours. Since there's only a per-5-hour limit, calculated at 30 days per month, theoretically maximum monthly usage could be `30*24/5*40=5760M` tokens.
- 2026/01/30: Through actual testing, speculated that GLM Coding Plan's Lite plan usage limit is that the sum of all requests' input + output tokens does not exceed 40M per 5 hours (meaning each prompt corresponds to 40M/120=333K tokens), which is consistent with the results returned by the `https://open.bigmodel.cn/api/monitor/usage/quota/limit` API (after 2026/02/12, this API only returns percentages, not token counts).
