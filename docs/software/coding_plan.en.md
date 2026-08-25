# AI Coding Plan

## Coding Plan

### Kimi

[Kimi Membership](https://www.kimi.com/membership/pricing) [Kimi Code](https://www.kimi.com/code)

- Andante (49 RMB/month)
- Moderato (99 RMB/month)
- Allegretto (199 RMB/month)
- Allegro (699 RMB/month)
- Subscription renewal rule adjustment: Due to tight compute resources, priority will be given to ensuring the experience of currently subscribed users. You can renew before 2026-08-20 00:00; after that, direct purchase will no longer be available.
- [K3 API Pricing](https://platform.kimi.com/docs/pricing/chat-k3):
    - Cached input: 2 RMB per 1M tokens
    - Uncached input: 20 RMB per 1M tokens
    - Output: 100 RMB per 1M tokens
    - 1M context
- [K2.7-Code API Pricing](https://platform.kimi.com/docs/pricing/chat-k27-code):
    - Cached input: 1.3 RMB per 1M tokens
    - Uncached input: 6.5 RMB per 1M tokens
    - Output: 27 RMB per 1M tokens
    - 256K context
- [K2.7-Code-HighSpeed API Pricing](https://platform.kimi.com/docs/pricing/chat-k27-code):
    - Cached input: 2.6 RMB per 1M tokens
    - Uncached input: 13.0 RMB per 1M tokens
    - Output: 54 RMB per 1M tokens
    - 256K context

### MiniMax

[MiniMax Token Plan](https://platform.minimaxi.com/docs/token-plan/intro) [Pricing](https://platform.minimaxi.com/docs/guides/pricing-token-plan) [Subscription](https://platform.minimaxi.com/subscribe/token-plan)

- Token Plan coverage has been narrowed from "all models" to "flagship models"; music APIs (Music-3.0, Music-2.6, Lyrics Generation, etc.) have been discontinued and are no longer included in Token Plan quota
- Plus (49 RMB/month): Monthly M3 Token usage approx. 600M+
- Max (119 RMB/month): Monthly M3 Token usage approx. 1.8B+
- Ultra (469 RMB/month): Monthly M3 Token usage approx. 7.1B+
- [MiniMax M3 API Pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo):
    - `<=` 512K input tokens:
        - Cached input: 0.42 RMB per 1M tokens
        - Uncached input: 2.10 RMB per 1M tokens
        - Output: 8.40 RMB per 1M tokens
    - `>` 512K input tokens:
        - Cached input: 0.84 RMB per 1M tokens
        - Uncached input: 4.20 RMB per 1M tokens
        - Output: 16.80 RMB per 1M tokens
    - 1M context

[MiniMax International Token Plan](https://platform.minimax.io/docs/token-plan/intro) [Pricing](https://platform.minimax.io/docs/guides/pricing-token-plan)

### Zhipu (GLM, Z.ai)

[Zhipu GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite Plan (118 RMB/month): 2,000 points per 5 hours, 10,000 points per week
- Pro Plan (538 RMB/month): 12,000 points per 5 hours, 60,000 points per week
- Max Plan (1078 RMB/month): 28,000 points per 5 hours, 140,000 points per week
- Model points consumed = (input tokens × Input coefficient + cached input tokens × Cached Input coefficient + output tokens × Output coefficient) / 10,000
- MCP points consumed = number of calls × Output coefficient
- All plans support GLM-5.3, GLM-5-Turbo, GLM-4.7.
- Requests for previous models (GLM-5.2/GLM-5.1) will be automatically routed to GLM-5.3.
- During off-peak hours, model calls consume points at 50% of the base rate. Peak hours: 14:00–18:00 (UTC+8) on weekdays.
- GLM-5.3: Input coefficient 6.9, Cached Input coefficient 1.7, Output coefficient 24
- Using only GLM-5.3 as an example, the plan's token usage will vary depending on the cache hit rate, as shown below:

| Plan | 90.9% Cache Hit Rate | 95% Cache Hit Rate | 98% Cache Hit Rate |
| --- | --- | --- | --- |
| Lite | 43M–87M tokens/week | 48M–97M tokens/week | 52M–105M tokens/week |
| Pro | 263M–526M tokens/week | 290M–580M tokens/week | 313M–627M tokens/week |
| Max | 613M–1,226M tokens/week | 676M–1,352M tokens/week | 731M–1,463M tokens/week |
- Range explanation
    - Maximum tokens: all during off-peak hours, consuming points at 0.5×
    - Minimum tokens: all during peak hours, consuming points at 1×
- [GLM-5.3 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 2 RMB per 1M tokens
    - Uncached input: 8 RMB per 1M tokens
    - Output: 28 RMB per 1M tokens
    - 1M context
- [GLM-5.2 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 2 RMB per 1M tokens
    - Uncached input: 8 RMB per 1M tokens
    - Output: 28 RMB per 1M tokens
    - 1M context
- [GLM-5.1 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 1.3/2 RMB per 1M tokens
    - Uncached input: 6/8 RMB per 1M tokens
    - Output: 24/28 RMB per 1M tokens
    - 200K context
- [GLM-5-Turbo API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 1.2/1.8 RMB per 1M tokens
    - Uncached input: 5/7 RMB per 1M tokens
    - Output: 22/26 RMB per 1M tokens
    - 200K context
- [GLM-4.7 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 0.4/0.6/0.8 RMB per 1M tokens
    - Uncached input: 2/3/4 RMB per 1M tokens
    - Output: 8/14/16 RMB per 1M tokens
    - 200K context

[Zhipu GLM Coding Plan Team Edition](https://docs.bigmodel.cn/cn/coding-plan/team)

- Team Standard (598 RMB/month): Maximum 60M tokens per seat per 5 hours, maximum 300M tokens per seat per week
- Team Advanced (1198 RMB/month): Maximum 160M tokens per seat per 5 hours, maximum 800M tokens per seat per week
- "Maximum" refers to the total tokens that can be actually consumed at a 1× consumption coefficient. Current model consumption rules are as follows:
    - GLM-4.7, GLM-4.5-Air: Consume quota at 1× coefficient throughout the day
    - GLM-5.2, GLM-5-Turbo: As advanced models, consume quota at 3× during peak hours and 2× during off-peak hours. As a limited-time benefit, GLM-5.2 and GLM-5-Turbo will only consume 1× quota during off-peak hours, valid through the end of June.
    - Note: Peak hours are 14:00–18:00 (UTC+8) daily.

[Zhipu International GLM Coding Plan](https://z.ai/subscribe)

### Cloud Providers

- [Volcano Engine Coding Plan (Personal Edition)](https://www.volcengine.com/activity/codingplan) [Documentation](https://www.volcengine.com/docs/82379/1925114)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum ~1,200 requests. Per week: maximum ~9,000 requests. Per subscription month: maximum ~18,000 requests.
    - Pro Plan (200 RMB/month): 5x the Lite Plan quota
    - Supported models: Doubao-Seed-2.1-turbo, Doubao-Seed-Evolving (new), Doubao-Seed-2.0-lite, MiniMax-M3, Kimi-K2.7-Code, GLM-5.2 (phasing out), GLM-5.3, DeepSeek-V4-Flash, DeepSeek-V4-Pro
- [Volcano Engine Agent Plan (Personal Edition)](https://www.volcengine.com/docs/82379/2366394)
    - Agent Fuel Points (AFP) are the unified billing unit for Agent Plan subscriptions, used to quantify Agent resource consumption.
        - Text generation models, embedding models: (input token * input deduction coefficient + output token * output deduction coefficient) / 10,000
        - Video generation models: tokens consumed / 10,000 * deduction coefficient
        - Image generation models: number of successfully generated images * deduction coefficient
    - Small Plan (40 RMB/month): Per 5 hours: 2,000 AFP. Per week: 7,000 AFP. Per month: 20,000 AFP. Daily quota: 10,000 AFP.
    - Medium Plan (200 RMB/month): Per 5 hours: 10,000 AFP. Per week: 35,000 AFP. Per month: 100,000 AFP. Daily quota: 50,000 AFP.
    - Large Plan (500 RMB/month): Per 5 hours: 25,000 AFP. Per week: 87,500 AFP. Per month: 250,000 AFP. Daily quota: 125,000 AFP.
    - Max Plan (1000 RMB/month): Per 5 hours: 50,000 AFP. Per week: 175,000 AFP. Per month: 500,000 AFP. Daily quota: 250,000 AFP.
    - Image generation models, video generation models, voice models, and Harness have no 5-hour or weekly quota limits; they are only subject to daily quota and monthly plan quota. Daily quota is uniformly half of the monthly plan quota.
    - All plans support: doubao-seed-2.0-mini, doubao-seed-2.0-lite, deepseek-v4-flash, deepseek-v3.2, minimax-m3, glm-5.2 (phasing out), glm-5.3, kimi-k2.7-code, deepseek-v4-pro, doubao-embedding-vision, doubao-seedream-5.0-lite, doubao-seed-tts-2.0, doubao-seed-asr-2.0
    - Medium and above plans additionally support: doubao-seedance-1.5-pro, doubao-seedance-2.0, doubao-seedance-2.0-fast, doubao-seedance-2.0-mini
- [Alibaba Cloud Bailian Token Plan (Personal Edition)](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
    - Lite Plan (60 RMB/month): 2,500 Credits every 7 days
    - Standard Plan (180 RMB/month): 10,000 Credits every 7 days
    - Pro Plan (600 RMB/month): 40,000 Credits every 7 days
    - Usage Pack (100 RMB/month): 20,000 Credits
    - Supported models: qwen3.8-max, qwen3.7-max, qwen3.7-plus, qwen3.6-flash, qwen-image-3.0-pro, qwen-audio-3.0-tts-plus, qewn-audio-3.0-realtime-plus, qwen-audio-3.0-asr-flash, wan2.7-image, wan2.7-image-pro, deepseek-v4-pro, deepseek-v4-pro-0813, deepseek-v4-flash-0731, glm-5.2, happyhorse-1.1-i2v, happyhorse-1.1-t2v, happyhorse-1.1-r2v
- [Alibaba Cloud Bailian Token Plan (Team Edition)](https://help.aliyun.com/zh/model-studio/token-plan-overview)
    - Standard Seat (¥198/seat/month): 25,000 Credits/seat/month
    - Advanced Seat (¥698/seat/month): 100,000 Credits/seat/month
    - Premium Seat (¥1,398/seat/month): 250,000 Credits/seat/month
    - Shared Usage Pack (¥5,000/pack): 625,000 Credits/pack
    - Credits consumed per request are dynamically determined by model type, token usage, reasoning mode, and tool calls. Actual consumption is based on the bill.
    - For example, with Qwen3.6-plus, every 5,000 uncached input tokens, every 50,000 cached input tokens, or every 5,000/6 output tokens equals one Credit
    - For contexts within 256K, one Credit corresponds to an API price (implicit caching) of 0.01–0.02 RMB; for contexts between 256K–1M, one Credit corresponds to 0.04–0.08 RMB
    - Supported models: qwen3.8-max, qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.6-flash, qwen-image-2.0, qwen-image-2.0-pro, qwen-image-3.0-pro, qwen-audio-3.0-tts-plus, qwen-audio-3.0-realtime-plus, qwen-audio-3.0-asr-flash, wan2.7-image, wan2.7-image-pro, deepseek-v4-pro, deepseekv4-pro-0813, deepseek-v4-flash, deepseek-v4-flash-0731, deepseek-v3.2, kimi-k2.7-code, kimi-k2.6, kimi-k2.5, glm-5.2, glm-5.1, glm-5, minimax-m2.5, happyhorse-1.1-i2v, happyhorse-1.1-t2v, happyhorse-1.1-r2v
- [Tencent Cloud LLM Token Plan](https://cloud.tencent.com/act/pro/tokenplan)
    - Token Plan Enterprise Edition:
        - Professional Plan: 1 RMB/100 Credits per month, minimum purchase 50K Credits (500 RMB/month); supports DeepSeek-V4-Flash 0731 Official and DeepSeek-V4-Pro 0813 Official (peak-valley pricing, same rates as direct-supply versions)
        - Light Enjoyment Plan: 2 RMB/million tokens per month
    - Token Plan Personal Edition:
        - Hy Token Plan:
            - Lite Plan (28 RMB/month): 35M tokens per subscription month
            - Standard Plan (78 RMB/month): 100M tokens per subscription month
            - Pro Plan (238 RMB/month): 320M tokens per subscription month
            - Max Plan (468 RMB/month): 650M tokens per subscription month
            - Supported models: Hy3 preview
        - Universal Token Plan:
            - Lite Plan (39 RMB/month): 35M tokens per subscription month
            - Standard Plan (99 RMB/month): 100M tokens per subscription month
            - Pro Plan (299 RMB/month): 320M tokens per subscription month
            - Max Plan (599 RMB/month): 650M tokens per subscription month
            - Supported models (image, video, and other multimodal capabilities temporarily not supported): MiniMax-M2.7, Kimi-K2.5, GLM-5, GLM-5.1
            - Token Plan Enterprise Professional Plan has removed MiniMax-M2.5 model (discontinued on August 7, 2026)
- [Baidu Qianfan Token Plan (Personal Edition)](https://cloud.baidu.com/product/codingplan.html) [Personal Edition Documentation](https://cloud.baidu.com/doc/qianfan/s/Dmrabu8b6) [Enterprise Edition Documentation](https://cloud.baidu.com/doc/qianfan/s/ymq8wwch2)
    - Mini Plan (9.9 RMB/month): 10M tokens per month
    - Lite Plan (40 RMB/month): 42M tokens per month
    - Pro Plan (200 RMB/month): 230M tokens per month
    - Max Plan (600 RMB/month): 700M tokens per month
    - Supported models: DeepSeek-V4-Pro, DeepSeek-V4-Flash, GLM-5.2, GLM-5.1, Kimi-K2.6, ERNIE 5.1
- [JD Cloud Coding Plan](https://docs.jdcloud.com/cn/jdaip/PackageOverview)
    - Lite Plan (19.9 RMB first purchase/month, 40 RMB renewal/month): Per 5 hours: maximum 1,200 requests. Per week: maximum 9,000 requests. Per subscription month: maximum 18,000 requests
    - Pro Plan (99.9 RMB first purchase/month, 200 RMB renewal/month): Per 5 hours: maximum 6,000 requests. Per week: maximum 45,000 requests. Per subscription month: maximum 90,000 requests
    - Supported models: DeepSeek-V3.2, GLM-5, GLM-4.7, MiniMax-M2.5, Kimi-K2.5, Kimi-K2-Turbo, Qwen3-Coder
- [iFlytek Astron Token Plan Team Edition](https://www.xfyun.cn/doc/spark/TokenPlan.html) [Subscription](https://maas.xfyun.cn/tokenPlan/subscription)
    - Standard Member (200 RMB/seat/month): 20000 Credits, 2M TPM
    - Advanced Member (600 RMB/seat/month): 60000 Credits, 3M TPM
    - Premium Member (1200 RMB/seat/month): 200000 Credits, 5M TPM
    - Supported models: Spark-X2, Spark-X2-Flash, GLM-5.2, GLM-5.1, GLM-5, DeepSeek-V4-Pro, DeepSeek-V4-Flash, DeepSeek-V3.2, Kimi-K2.6, Kimi-K2.5, MiniMax-M2.5, Qwen3.5-397B-A17B, Qwen3.6-35B-A3B, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, GLM-4.7-Flash
- [iFlytek Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html) [Subscription](https://maas.xfyun.cn/packageSubscription)
    - Professional (39 RMB/month): Per 5 hours: maximum ~1,200 requests; per week: maximum ~9,000 requests; per subscription month: maximum ~18,000 requests. Supports Spark-X2-Agent, Spark-X2, Auto, GLM-5.1, GLM-5, MiniMax-M2.5, Kimi-K2.6, Kimi-K2.5, DeepSeek-V3.2, Spark-X2-Flash, Qwen3.6-35B-A3B, GLM-4.7-Flash, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, Qwen3.5-397B-A17B models
    - Efficient (199 RMB/month): Per 5 hours: maximum ~6,000 requests; per week: maximum ~45,000 requests; per subscription month: maximum ~90,000 requests. Supports Spark-X2-Agent, Spark-X2, Auto, GLM-5, GLM-5.2, DeepSeek-V4-Pro, DeepSeek-V4-Flash, MiniMax-M2.5, Kimi-K2.6, Kimi-K2.5, DeepSeek-V3.2, Spark-X2-Flash, Qwen3.6-35B-A3B, GLM-4.7-Flash, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, Qwen3.5-397B-A17B models
- [CTCloud Programming Token Plan](https://www.ctyun.cn/document/11061839/11092368)
    - 29 RMB/month: 25M tokens
    - 89 RMB/month: 80M tokens
    - 199 RMB/month: 180M tokens
    - 399 RMB/month: 380M tokens
    - 699 RMB/month: 680M tokens
    - Supported models: GLM-5.0 (Official), DeepSeek-V3.2 (Flagship), GLM-5.1, DeepSeek-V4-Flash-0731
- [Huawei Cloud MaaS Token Plan](https://support.huaweicloud.com/Token-plan-maas/tokenplan-maas-0001.html)
    - Lite (59 RMB/month): 50M tokens per subscription month
    - Standard (149 RMB/month): 130M tokens per subscription month
    - Pro (399 RMB/month): 380M tokens per subscription month
    - Max (799 RMB/month): 880M tokens per subscription month
    - Supported models: GLM-5, GLM-5.1, Kimi-K2.6, DeepSeek-V3.2, DeepSeek-V4-Flash

### Others

- [StepFun Step Plan](https://platform.stepfun.com/docs/zh/step-plan/overview)
    - Flash Mini (49 RMB/month): 400M Credits
    - Flash Plus (99 RMB/month): 1600M Credits
    - Flash Pro (199 RMB/month): 8000M Credits
    - Flash Max (699 RMB/month): 40000M Credits
    - Supported models: step-3.7-flash, step-3.5-flash-2603, step-3.5-flash, stepaudio-2.5-realtime, stepaudio-2.5-chat, stepaudio-2.5-tts, stepaudio-2.5-asr, step-router-v1 (intelligent routing between deepseek-v4-pro and step-3.5-flash), step-image-edit-2
- [Xiaomi MiMo Token Plan](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription)
    - Lite (39 RMB or 6 USD/month): 4.1B Credits per month
    - Standard (99 RMB or 16 USD/month): 11B Credits per month
    - Pro (329 RMB or 50 USD/month): 38B Credits per month
    - Max (659 RMB or 100 USD/month): 82B Credits per month
    - Supported models: All plans support MiMo-V2.5-Pro, MiMo-V2.5, MiMo-V2.5-ASR, MiMo-V2.5-TTS-VoiceClone, MiMo-V2.5-TTS-VoiceDesign, MiMo-V2.5-TTS, MiMo-V2-Pro, MiMo-V2-Omni, MiMo-V2-TTS (9 models total)
    - Credit consumption: Credits are deducted based on token count. Available models in the plan consume Credits at different ratios in parallel, not independently. TTS series models are free for a limited time and do not consume plan tokens.

- [OpenCode Go](https://opencode.ai/docs/zh-cn/go) (low-cost open-source coding model subscription for international users)
    - $10/month
    - Usage limits: $12 per 5 hours, $30 per week, $60 per month
    - Supported models: Grok 4.6, GLM-5.3/5.2/5.1, GPT 5.6 Luna, Kimi K3/K2.7 Code/K2.6, LongCat-2.0, MiMo-V2.5/V2.5-Pro, MiniMax M3/M2.7/M2.5, **Muse Spark 1.2 Contributor**, Qwen3.8 Max/Qwen3.7 Max/Qwen3.7 Plus/Qwen3.6 Plus, DeepSeek V4 Pro/V4 Flash/V4 Flash Vision Exp, Hy3, **Ox Alpha Free** (limited-time free)
    - Muse Spark 1.2 Contributor is a new model: allows Meta to use prompts and completions for training future models in exchange for heavily discounted token pricing (input $0.10/1M, output $0.20/1M, cache read $0.002/1M). Only available in regions permitted by Meta's [Geographic Use Policy](https://ai.developer.meta.com/legal/geographic-use-policy)
- [StepFun International Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)
- [UniAI GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)
- [Moorethreads AI Coding Plan](https://code.mthreads.com/)
- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)
- [DeepSeek API Pricing](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/):
    - Starting 2026-08-17 00:00, peak-valley pricing applies; off-peak price is half of peak price, with overall prices significantly increased compared to before
    - Peak hours: Monday to Friday 9:00-12:00, 14:00-18:00 Beijing time (the rest are off-peak hours)
    - deepseek-v4-flash (DeepSeek-V4-Flash-0731, 1M context):
        - Off-peak: cached input 0.05 RMB / uncached input 1.5 RMB / output 4.5 RMB per 1M tokens
        - Peak: cached input 0.10 RMB / uncached input 3.0 RMB / output 9.0 RMB per 1M tokens
    - deepseek-v4-pro (DeepSeek-V4-Pro-0813, 1M context):
        - Off-peak: cached input 0.15 RMB / uncached input 4.5 RMB / output 13.5 RMB per 1M tokens
        - Peak: cached input 0.30 RMB / uncached input 9.0 RMB / output 27.0 RMB per 1M tokens
    - deepseek-v4-flash-vision-exp (DeepSeek-V4-Flash-Vision-Exp, experimental vision model):
        - Pricing same as deepseek-v4-flash (off-peak / peak)
        - FIM completion not supported, concurrency limit 2500
        - Images are converted to tokens based on size and billed together with text tokens

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

| Name                                                                                | Parameters | Active | Vision |
|-------------------------------------------------------------------------------------|------------|--------|--------|
| [DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | 284B       | 13B    | N      |
| [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)           | 284B       | 13B    | N      |
| [DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)     | 1.6T       | 49B    | N      |
| [DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)               | 1.6T       | 49B    | N      |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)                       | 30B        | 3B     | N      |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                                   | 355B       | 32B    | N      |
| [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)                                   | 744B       | 40B    | N      |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                                   | 744B       | 40B    | N      |
| [Hy3-preview](https://huggingface.co/tencent/Hy3-preview)                           | 295B       | 21B    | N      |
| [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)                                | 2.8T       | 104B   | Y      |
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)                            | 1T         | 32B    | Y      |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)                           | 428B       | 23B    | Y      |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)                       | 230B       | 10B    | N      |
| [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)                  | 2.4T       | 95B    | Y      |
| [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)                              | 27B        | -      | Y      |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)                  | 397B       | 17B    | Y      |

## Update History

- 2026/08/26: OpenCode Go upgraded Grok model from 4.5 to 4.6: rate limits increased (169/5hr, 423/week, 845/month, previously 120/300/600), pricing changed to tiered (≤200K tokens: input $2.00, output $6.00, cache $0.50; >200K tokens: input $4.00, output $12.00, cache $1.00, previously flat $2.00/$6.00/$0.30), model ID changed from grok-4.5 to grok-4.6
- 2026/08/25: Tencent Cloud Token Plan Enterprise Professional Plan lowered minimum purchase from 100K to 50K Credits, added DeepSeek-V4-Flash 0731 Official and DeepSeek-V4-Pro 0813 Official models (peak-valley pricing, off-peak rates same as direct-supply versions)
- 2026/08/25: OpenCode Go added support for LongCat-2.0 model (input $0.30/1M, output $1.20/1M, cache read $0.006/1M)
- 2026/08/24: OpenCode Go removed first-month discount, pricing changed from "$5 first month, then $10/month" to a flat $10/month
- 2026/08/23: DeepSeek API peak-valley weekend rule now in effect: peak hours are explicitly Monday to Friday 9:00-12:00, 14:00-18:00 Beijing time; weekends are now charged at off-peak rates all day
- 2026/08/22: DeepSeek API peak-valley pricing rule adjustment: starting 2026-08-23 (Sunday) 00:00 Beijing time, weekends (Saturday and Sunday) will no longer distinguish peak/off-peak — all day will be charged at off-peak rates (previously weekends still followed peak/off-peak schedule)
- 2026/08/21: Volcano Engine Coding Plan (Personal Edition) added support for Doubao-Seed-Evolving model (for Coding & Agent scenarios, weekly upgrades, 1M context window, 256K max output); OpenCode Go added support for DeepSeek V4 Flash Vision Exp model (pricing Off-Peak $0.22/$0.66, Peak $0.44/$1.32 per 1M tokens, images converted to tokens based on size); Tencent Cloud Token Plan (Personal Edition) Universal Plan removed discontinued models (Tencent HY 2.0 Instruct, Tencent HY 2.0 Think, Hunyuan-T1, Hunyuan-TurboS, MiniMax-M2.5)
- 2026/08/21: DeepSeek added new vision model deepseek-v4-flash-vision-exp (experimental), priced same as deepseek-v4-flash, FIM completion not supported, concurrency limit 2500, images converted to tokens based on size; Tencent Cloud Token Plan Enterprise Professional Plan removed MiniMax-M2.5 model; Volcano Engine Agent Plan (Personal Edition) updated quota rules: image/video generation models, voice models, and Harness merged into a single daily quota category (no longer separated as "vision models" and "voice models"), daily quota uniformly set to half of monthly plan quota; OpenCode Go added Ox Alpha Free model (limited-time free)
- 2026/08/19: Alibaba Cloud Bailian added open-source model qwen3.8-27b, priced at Input 3 RMB / Output 12 RMB per 1M tokens (context cache discount available), international pricing Input 3.646 RMB / Output 21.875 RMB per 1M tokens; Tencent Cloud Token Plan (Personal Edition) and Enterprise Professional Plan renamed DeepSeek-V4-Pro 原厂直供 to DeepSeek-V4-Pro 正式版 原厂直供, added model IDs deepseek/deepseek-v4-pro-0813 and deepseek/deepseek-v4-pro; MiniMax Token Plan coverage narrowed from "all models" to "flagship models", music APIs (Music-3.0, Music-2.6, Lyrics Generation, etc.) discontinued and removed from Token Plan quota
- 2026/08/19: Zhipu released GLM-5.3 model with 50% coding improvement over GLM-5.2 and cybersecurity capabilities matching Mythos 5; GLM Coding Plan token allowance estimates updated to show multiple cache hit rates (90.9%, 95%, 98%); GLM-5.3 API pricing matches GLM-5.2
- 2026/08/18: Volcano Engine Coding Plan (Personal Edition) and Agent Plan removed MiniMax-M2.7 and Kimi-K2.6 models (previously marked as phasing out)
- 2026/08/17: Volcano Engine Coding Plan (Personal Edition) and Agent Plan removed Doubao-Seed-2.0-Code, Doubao-Seed-2.0-pro, Doubao-Seed-Code models (previously marked as phasing out); GLM-5.2 marked as phasing out; GLM-5.3 replaced GLM-5.2 as the default glm-latest target
- 2026/08/14: Volcano Engine Coding Plan (Personal Edition) and Agent Plan added support for the GLM-5.3 model (1M context window, 1024K context / 128K max output, thinking enabled by default and cannot be disabled, deduction coefficient same as GLM-5.2)
- 2026/08/14: Zhipu GLM Coding Plan flagship model upgraded from GLM-5.2 to GLM-5.3: all plans support GLM-5.3, GLM-5-Turbo and GLM-4.7; requests for previous models (GLM-5.2/GLM-5.1) are automatically routed to GLM-5.3; model deduction coefficients unchanged (Input 6.9 / Cached Input 1.7 / Output 24); the official docs also removed the "save up to 92%" claim; the international edition (Z.ai DevPack) was upgraded to GLM-5.3 accordingly
- 2026/08/13: DeepSeek API will adopt peak-valley pricing starting 2026-08-17 00:00: peak hours (9:00-12:00, 14:00-18:00 Beijing time) are charged at 2x the off-peak price, with overall prices significantly increased (e.g., deepseek-v4-pro output price rises from 6 RMB to 27 RMB peak / 13.5 RMB off-peak per 1M tokens)
- 2026/07/31: GLM Coding Plan switched to credit-based limits
- 2026/07/20: Kimi Code separated from Kimi membership, now available as a dedicated new Kimi Code subscription
- 2026/07/16: Kimi-K3 model released
- 2026/07/13: Baidu Qianfan Token Plan (Personal Edition) launched
- 2026/06/27: Infini Coding Plan discontinued
- 2026/06/13: GLM-5.2 model released
- 2026/06/12: Kimi K2.7-Code model released
- 2026/06/10: GLM Coding Plan Team Edition launched
- 2026/06/08: Volcano Engine Coding Plan and Agent Plan added MiniMax-M3
- 2026/06/08: MiniMax M3 API price permanently halved
- 2026/06/07: Alibaba Cloud Bailian Coding Plan added qwen3.7-plus model
- 2026/06/05: Huawei Cloud MaaS Token Plan launched
- 2026/06/01: MiniMax M3 released
- 2026/05/29: StepFun Coding Plan added support for step-3.7-flash model
- 2026/05/27: Xiaomi MiMo Token Plan quota massively increased
- 2026/05/22: Baidu Qianfan Coding Plan added support for DeepSeek-V4-Pro model
- 2026/05/22: Alibaba Cloud Token Plan added support for qwen3.7-max model
- 2026/05/08: Baidu Qianfan Coding Plan added support for DeepSeek-V4-Flash and GLM-5.1 models
- 2026/05/07: Volcano Engine Agent Plan (Personal Edition) launched
- 2026/04/30: Tencent Cloud Token Plan (Personal Edition) added support for GLM-5.1 and MiniMax-M2.7 models
- 2026/04/30: StepFun Coding Plan removed deepseek-v4-pro model, must access indirectly through step-router-v1 model
- 2026/04/28: StepFun Coding Plan added deepseek-v4-pro and step-router-v1 models
- 2026/04/27: GLM Coding Plan extended the limited-time discount benefit deadline from end of April to end of June
- 2026/04/24: Alibaba Cloud Bailian Token Plan halved the Credits required for cached input tokens
- 2026/04/23: MiMo-V2.5 series models launched
- 2026/04/23: StepFun Coding Plan added support for stepaudio-2.5-asr model
- 2026/04/23: GLM Coding Plan will uniformly disable auto-renewal for legacy plans (no weekly limit version) on April 30, 2026. Current active billing cycles are not affected. Meanwhile, the system will automatically gift affected users 2 months of equivalent new plan, which will take effect after the current plan expires, with no manual claim required. See [Legacy Plan Migration and Compensation Notice](https://docs.bigmodel.cn/cn/coding-plan/transition).
- 2026/04/22: Volcano Engine Coding Plan added MiniMax-M2.7, Kimi-K2.6, GLM-5.1
- 2026/04/21: Alibaba Cloud Bailian Token Plan (Team Edition) launched
- 2026/04/21: Kimi officially released Kimi-K2.6 model
- 2026/04/14: Kimi Code launched K2.6-code-preview model
- 2026/04/12: Zhipu International GLM Coding Plan starting price increased from 10 USD/month to 18 USD/month
- 2026/04/11: Alibaba Cloud Bailian Coding Plan Lite Plan will stop accepting renewals and upgrades from April 13, 2026. New purchases were already suspended on March 19, 2026
- 2026/04/11: Added CTCloud Coding Plan
- 2026/08/20: CTCloud Programming Token Plan updated supported models: added GLM-5.1, DeepSeek-V4-Flash-0731; renamed GLM-5 to GLM-5.0 (Official); DeepSeek-V3.2 labeled as Flagship
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
