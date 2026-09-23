# AI Coding Plan

## Coding Plan

### Kimi

[Kimi Membership](https://www.kimi.com/membership/pricing) [Kimi Code](https://www.kimi.com/code)

- Andante (49 RMB/month)
- Moderato (99 RMB/month)
- Allegretto (199 RMB/month)
- Allegro (699 RMB/month)
- Subscription renewal rule adjustment: Due to tight compute resources, priority will be given to ensuring the experience of currently subscribed users. You can renew before 2026-08-20 00:00; after that, direct purchase will no longer be available.
- Kimi Code is now powered by the flagship K3 model (~2.8 trillion parameters), available with the K2.8 Preview in two modes (standard / K2.7 Code HighSpeed), with a maximum inference speed of 260 Tokens/s and a 1M Token context window; it is fully compatible with mainstream agent tools including Kimi Code CLI, Claude Code, and VS Code
- Per-model ID membership tier requirements (added to the docs on 2026-09-18): `k3` and `k3-256k` require Moderato / Plus or above, with the 1M context requiring Allegretto / Pro or above; `kimi-for-coding` (K2.8 Preview) requires Andante / Plus or above (previously described as "available to all members"); `kimi-for-coding-highspeed` requires Allegretto / Pro or above. This is the first appearance of the Plus / Pro tier names (Kimi's membership pricing page is not crawled, so the mapping between Plus / Pro and the domestic tiers is unconfirmed)
- API endpoints are now split into domestic and overseas: OpenAI-compatible — domestic `https://api.kimi.com/coding/v1`, overseas `https://api.kimi.ai/coding/v1`; Anthropic-compatible — domestic `https://api.kimi.com/coding/`, overseas `https://api.kimi.ai/coding/`; Kimi Open Platform — domestic `https://api.moonshot.cn/v1`, overseas `https://api.moonshot.ai/v1`
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

[MiniMax Token Plan](https://platform.minimaxi.com/docs/token-plan/intro) [Pricing](https://platform.minimaxi.com/docs/guides/pricing-token-plan) [Subscription](https://platform.minimax.cn/subscribe/token-plan)

- Token Plan coverage has been narrowed from "all models" to "flagship models"; music APIs (Music-3.0, Music-2.6, Lyrics Generation, etc.) have been discontinued and are no longer included in Token Plan quota
- Plus (49 RMB/month): Monthly M3 Token usage approx. 600M+
- Max (119 RMB/month): Monthly M3 Token usage approx. 1.8B+
- Ultra (469 RMB/month): Monthly M3 Token usage approx. 7.1B+
- Prepaid credits packages: ¥30 for 4,489 credits, ¥150 for 22,460 credits, ¥500 for 74,900 credits, valid for 365 days
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

- Plus ($22/month): Personal projects and prototyping
- Max ($55/month): Daily coding with agents and multimodal work
- Ultra ($132/month): Heavy Agent workflows and extended sessions

### Zhipu (GLM, Z.ai)

[Zhipu GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite Plan (118 RMB/month): 2,000 points per 5 hours, 10,000 points per week
- Pro Plan (538 RMB/month): 12,000 points per 5 hours, 60,000 points per week
- Max Plan (1078 RMB/month): 28,000 points per 5 hours, 140,000 points per week
- Model points consumed = (input tokens × Input coefficient + cached input tokens × Cached Input coefficient + output tokens × Output coefficient) / 10,000
- MCP points consumed = number of calls × Output coefficient
- All plans support **GLM-5.3**, **GLM-5.3-Flash**.
- Requests for previous models (GLM-5.2/GLM-5.1) will be automatically routed to GLM-5.3, requests for GLM-5-Turbo/GLM-4.7 will automatically be routed to GLM-5.3-Flash.
- During off-peak hours, model calls consume points at 50% of the base rate. Peak hours: 14:00–18:00 (UTC+8) on weekdays.
    - "GLM-5.3-Flash Usage Campaign" (2026-09-03 to 2026-10-07, daily 23:00–09:00): plan users get unlimited GLM-5.3-Flash usage via [ZCode](https://zcode.z.ai/cn) and doubled quota on other agents
    - "Double Festival" campaign (2026-09-25 to 2026-10-07): all-day usage is charged at the off-peak rate, i.e. 50% points consumption around the clock
- GLM-5.3: Input coefficient 6.9, Cached Input coefficient 1.7, Output coefficient 24
- GLM-5.3-Flash (Including MCP for visual understanding): Input coefficient 2.3, Cached Input coefficient 0.56, Output coefficient 8
- Token usage varies depending on the cache hit rate, as shown below:

| Cache Hit Rate | Model | Lite (M Tokens/week) | Pro (M Tokens/week) | Max (M Tokens/week) |
| --- | --- | --- | --- | --- |
| 95% | GLM-5.3 | 0.48～0.97 | 2.90～5.80 | 6.76～13.52 |
| 95% | GLM-5.3-Flash | 1.46～2.92 | 8.77～17.55 | 20.47～40.95 |
| 96% | GLM-5.3 | 0.50～0.99 | 2.97～5.95 | 6.94～13.87 |
| 96% | GLM-5.3-Flash | 1.50～3.00 | 9.00～18.01 | 21.01～42.02 |
| 98% | GLM-5.3 | 0.52～1.04 | 3.13～6.27 | 7.31～14.63 |
| 98% | GLM-5.3-Flash | 1.58～3.17 | 9.50～19.00 | 22.17～44.33 |


- Range explanation
    - Maximum tokens: all during off-peak hours, consuming points at 0.5×
    - Minimum tokens: all during peak hours, consuming points at 1×
- By fully utilizing the off-peak discounts, you can save up to 92% compared with pay-as-you-go calls to the GLM-5.3 standard API
- [GLM-5.3 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 2 RMB per 1M tokens
    - Uncached input: 8 RMB per 1M tokens
    - Output: 28 RMB per 1M tokens
    - 1M context
- [GLM-5.3-Flash API Pricing](https://bigmodel.cn/pricing):
    - Cached input 0.23, uncached input 0.8, output 2.8 RMB per 1M tokens
    - 1M context (the limited-time 50% off promotion has ended; billed at the standard price above)
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

[Zhipu International GLM Coding Plan](https://z.ai/subscribe): all plans support GLM-5.3 and GLM-5.3-Flash; requests for GLM-5.2/GLM-5.1 auto-route to GLM-5.3, GLM-4.7 auto-routes to GLM-5.3-Flash

### Cloud Providers

- [Volcano Engine Coding Plan (Personal Edition)](https://www.volcengine.com/activity/codingplan) [Documentation](https://www.volcengine.com/docs/82379/1925114)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum ~1,200 requests. Per week: maximum ~9,000 requests. Per subscription month: maximum ~18,000 requests.
    - Pro Plan (200 RMB/month): 5x the Lite Plan quota
    - Supported models: Doubao-Seed-2.1-pro, Doubao-Seed-2.1-lite, Doubao-Seed-2.0-mini, Doubao-Seed-2.1-turbo (being retired), Doubao-Seed-Evolving, Doubao-Seed-2.0-lite (being retired), MiniMax-M3, Kimi-K2.7-Code, Kimi-K2.8-Preview, Kimi-K3 (high deduction coefficient, recommended only for Pro plan users), GLM-5.3, GLM-5.3-Flash, DeepSeek-V4-Flash, DeepSeek-V4-Pro, DeepSeek-V4.1-Flash
    - 2026-09-23 model library update: added doubao-seed-2.1-pro (new-generation flagship model with all-round capability gains, 1024k context window / 256k output, suited to complex reasoning, in-depth analysis and long-chain task execution), doubao-seed-2.1-lite (lightweight and efficient, 1024k context window / 256k output, suited to everyday coding and routine development tasks), doubao-seed-2.0-mini (ultra-fast responses, 256k context window / 128k output, suited to simple coding tasks and code completion) and deepseek-v4.1-flash (the lightweight flagship of DeepSeek's new-architecture series, 552B total-parameter MoE, natively capable of multimodal vision understanding, 1024k context window / 384k max output); doubao-seed-2.1-turbo and doubao-seed-2.0-lite are marked "being retired"
    - 1M-context supported list (2026-09-23): doubao-seed-evolving, glm-5.3, glm-5.3-flash, kimi-k3, kimi-k2.8-preview, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro
    - New Kimi-K2.8-Preview model: overall performance close to K3 with higher thinking efficiency, strong at code completion and routine development tasks, supports text and image input; 1M context window / 1M max output. During the promotion from 2026-09-18 00:00 to 2026-09-30 23:59, the available quota of Kimi-K2.8-Preview in the Coding Plan is comparable to that during the Agent Plan 40%-off deduction promotion
    - GLM-5.3-Flash is a new model: Zhipu's first natively multimodal model, 320B total params / 18B active, supports image input, 1M context / 128K max output; first two weeks deduction coefficient at 50% off, promotion ends 2026-09-11 23:59:59
    - DeepSeek-V4-Pro is now officially released (was an early-access preview), with significantly enhanced Agent capabilities, accessible via model name and console selection
- [Volcano Engine Agent Plan (Personal Edition)](https://www.volcengine.com/docs/82379/2366394)
    - Agent Fuel Points (AFP) are the unified billing unit for Agent Plan subscriptions, used to quantify Agent resource consumption.
        - Text generation models, embedding models: (input token * input deduction coefficient + output token * output deduction coefficient) / 10,000
        - Video generation models: tokens consumed / 10,000 * deduction coefficient
        - Image generation models: number of successfully generated images * deduction coefficient
        - The input and output deduction coefficients for text-generation/embedding models are now determined solely by the model and no longer vary with input length (previously input coefficient = model coefficient × input segment factor: ×0.67 for ≤32k, ×1 for 32k–128k, ×2 for >128k; the length segmentation has been removed)
        - Deduction coefficients per model (input/output identical):
            - doubao-seed-2.0-mini: 0.25 (without audio input) / 2.5 (with audio input)
            - doubao-seed-2.0-lite (being retired), deepseek-v4-flash: 0.5
            - doubao-seed-2.1-lite: 0.5 (without audio input) / 4.5 (with audio input)
            - glm-5.3-flash: 0.5 (0.25 for the first two weeks at 50% off)
            - doubao-seed-2.1-turbo (being retired), doubao-seed-evolving, minimax-m3: 2.5
            - doubao-seed-2.1-pro: 2.5
            - deepseek-v4.1-flash: 2.5 (1.25 during the limited-time 50% off, 2026-09-15 00:00 to 2026-09-28 23:59)
            - kimi-k2.7-code: 4.5
            - kimi-k2.8-preview: 8 (4.8 during the limited-time 40% off, 2026-09-17 00:00 to 2026-09-30 23:59)
            - glm-5.3 (glm-latest): 4.5
            - deepseek-v4-pro: 5.5
            - kimi-k3: 10
            - doubao-embedding-vision: 0.5
    - Small Plan (40 RMB/month): Per 5 hours: 2,000 AFP. Per week: 7,000 AFP. Per month: 20,000 AFP. Daily quota: 10,000 AFP.
    - Medium Plan (200 RMB/month): Per 5 hours: 10,000 AFP. Per week: 35,000 AFP. Per month: 100,000 AFP. Daily quota: 50,000 AFP.
    - Large Plan (500 RMB/month): Per 5 hours: 25,000 AFP. Per week: 87,500 AFP. Per month: 250,000 AFP. Daily quota: 125,000 AFP.
    - Max Plan (1000 RMB/month): Per 5 hours: 50,000 AFP. Per week: 175,000 AFP. Per month: 500,000 AFP. Daily quota: 250,000 AFP.
    - Image generation models, video generation models, voice models, and Harness have no 5-hour or weekly quota limits; they are only subject to daily quota and monthly plan quota. Daily quota is uniformly half of the monthly plan quota.
    - All plans support: doubao-seed-2.1-pro, doubao-seed-2.1-lite, doubao-seed-2.0-mini, doubao-seed-2.0-lite (being retired), deepseek-v4-flash, deepseek-v3.2, minimax-m3, glm-5.3, glm-5.3-flash, kimi-k2.7-code, kimi-k2.8-preview, deepseek-v4-pro, deepseek-v4.1-flash, doubao-embedding-vision, doubao-seedream-5.0-lite, doubao-seedream-5-0-pro, doubao-seed-tts-2.0, doubao-seed-asr-2.0
    - Agent Evolution: first 50 files free (previously limited/charged)
    - Medium and above plans additionally support: doubao-seedance-2.0, doubao-seedance-2.0-fast, doubao-seedance-2.0-mini, doubao-seedance-2.5
    - 2026-09-23 model library update: added doubao-seed-2.1-pro (text generation (advanced), new-generation flagship model with all-round capability gains, 1024k context window / 256k output, deduction coefficient 2.5), doubao-seed-2.1-lite (text generation (standard), lightweight and efficient, 1024k context window / 256k output, deduction coefficient 0.5 / 4.5 with audio input) and doubao-seed-2.0-mini (text generation (fast), 256k context window / 128k output, deduction coefficient refined to 0.25 without audio input / 2.5 with audio input); doubao-seed-2.1-turbo and doubao-seed-2.0-lite are marked "being retired"; doubao-seedance-1.5-pro has been removed from the model table
    - New doubao-seedream-5-0-pro (image generation, all plans): input-image deduction coefficient is free for the first image and 10 AFP per image from the second onward; output images cost 150 AFP (single-image generation, ≤2.61M pixels) or 300 AFP (>2.61M pixels), and 75 / 150 AFP for the layer-separation scenario
    - New doubao-seedance-2.5 (video generation, Large/Max): deduction coefficient per token is 210 when the input contains video and 350 when it does not (480p/720p output), and 230 / 385 for 1080p output
    - New deepseek-v4.1-flash (text generation (advanced), all plans): 1M context window / 384K max output, natively capable of multimodal vision understanding; deduction coefficient 2.5, at 50% off (1.25) from 2026-09-15 00:00 to 2026-09-28 23:59. The model also joins the 1M-context supported list (glm-5.3, glm-5.3-flash, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro, kimi-k3)
    - New kimi-k2.8-preview (text generation (advanced), all plans): 1M context window / 1M max output, supports text and image input, overall performance close to K3 with higher thinking efficiency and strong at code completion and routine development tasks; deduction coefficient 8, at 40% off (4.8) from 2026-09-17 00:00 to 2026-09-30 23:59. The model also joins the 1M-context supported list (glm-5.3, glm-5.3-flash, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro, kimi-k3, kimi-k2.8-preview)
- [Alibaba Cloud Bailian Token Plan (Personal Edition)](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
    - Lite Plan (60 RMB/month, 39 RMB/month for a limited time): 11,500 Credits per month
    - Essential Plan (120 RMB/month, 79 RMB/month for a limited time): 25,500 Credits per month
    - Standard Plan (180 RMB/month, 139 RMB/month for a limited time): 45,000 Credits per month
    - Pro Plan (600 RMB/month, 499 RMB/month for a limited time): 180,000 Credits per month
    - Usage Pack (100 RMB/month): 20,000 Credits
    - Since 2026-09-22 the Personal Edition has abolished the fixed 7-day window quota and switched to a monthly quota: each subscription month runs 30 days from the subscription date, and once cumulative consumption within the subscription month reaches the plan quota, service is paused until the quota resets at the start of the next subscription month (auto-refreshed based on the subscription date, not a fixed calendar date); unused quota does not roll over. For existing subscriptions, the remaining quota was reset once to the full monthly quota of the corresponding plan on 2026-09-22, with the subscription cycle and expiry date unchanged; the previous "reset card / quota reset entitlement" was removed along with the weekly limit
    - Deduction order: each request is first deducted from the current subscription month's plan quota; once that is exhausted, Usage Pack quota is deducted automatically (Usage Pack quota neither occupies nor counts toward the plan monthly quota); when both are exhausted, or no Usage Pack is held, service is paused. You can upgrade the plan or wait for the next subscription month's reset
    - Upgrades (the current subscription cycle is not reset): the price difference is paid for the remaining days — upgrade price difference = (new plan price − old plan price) × remaining days ÷ 30, and the new quota granted for the current cycle = remaining days ÷ 30 × (new monthly quota − old monthly quota), with partial days counted as a full day and the quota result rounded up; from the next subscription month the new plan's monthly quota applies
    - Essential is a newly added tier: supports 2-3 concurrent Agents, and its benefits are all Lite benefits plus 2.25x the Lite plan quota
    - Device usage note: The Token Plan Personal Edition is for use by the subscriber on a single device only. (The official guide was tightened from "you may configure the same API Key on multiple of your own devices (e.g., home and office computers)" to "for the subscriber's own use on a single device.")
    - Supported models: auto (a platform-provided smart model that automatically matches the underlying model to the request), qwen3.8-max, qwen3.8-flash, qwen3.7-max, qwen3.7-plus, qwen3.6-flash, qwen-image-3.0-pro, qwen-audio-3.0-tts-plus, qewn-audio-3.0-realtime-plus, qwen-audio-3.0-asr-flash, wan2.7-image, wan2.7-image-pro, deepseek-v4.1-flash (capability label now includes "vision understanding"), deepseek-v4-pro, deepseek-v4-pro-0813, deepseek-v4-flash-0731, glm-5.3, glm-5.2, happyhorse-1.1-i2v, happyhorse-1.1-t2v, happyhorse-1.1-r2v
    - Limited-time night discount (every night 22:00 to 08:00): Credits consumption is 40% off for qwen3.8-max and qwen3.8-flash, and 50% off for deepseek-v4-pro-0813, deepseek-v4-flash-0731 and deepseek-v4.1-flash (page updated 2026-09-22: qwen3.8-max went from 50% off to 40% off, and qwen3.8-flash was added at 40% off)
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
        - Professional Plan: 1 RMB/100 Credits per month, minimum purchase 50K Credits (500 RMB/month); available model library (varies slightly by region, Guangzhou more complete, Singapore fewer): Auto, GLM-5.3, GLM-5.3-Flash, GLM-5.2, GLM-5 (discontinued 2026-10-09), GLM-5.1 (discontinued 2026-10-09), GLM-5-Turbo (discontinued 2026-10-09), Kimi K2.7 Code, Kimi K2.7 Code HighSpeed, Kimi K3, Kimi-K2.6, MiniMax-M2.7, MiniMax-M3, DeepSeek-V4-Flash, DeepSeek-V4-Pro, DeepSeek-V4-Flash 0731 Official, DeepSeek-V4-Pro 0813 Official, DeepSeek-V4.1-Flash Official direct-supply (model ID `deepseek/deepseek-flash`), DeepSeek-V4-Flash Official direct-supply, DeepSeek-V4-Pro Official direct-supply, DeepSeek-V4-Flash-Vision-Exp Official direct-supply (text capability on par with V4-Flash Official, with greatly enhanced visual understanding, multimodal Agent performance approaching Claude Opus-4.8; Kimi-K2.5 discontinued 2026-08-31)
        - Peak-valley billing (adjusted from 2026-08-29): DeepSeek V4 [Official direct-supply] continues peak-valley on weekdays (Mon-Fri, peak hours 9:00–12:00 and 14:00–18:00); weekends (Sat-Sun) are all billed at off-peak rates. DeepSeek V4 Official: peak hours are Mon–Sun 9:00–12:00 and 14:00–18:00. The billing window is determined by when the platform server receives the request (Beijing time)
        - DeepSeek [Official direct-supply] Flash-series credit prices lowered (2026-09-14): DeepSeek-V4-Flash 0731 Official direct-supply (previously ~39 off-peak / ~77 peak credits per 1M tokens) and DeepSeek-V4-Flash-Vision-Exp Official direct-supply (previously ~35 / ~70) both dropped to match the newly added DeepSeek-V4.1-Flash — cached input 2 / uncached input 100 / output 400 (off-peak), 4 / 200 / 800 (peak) credits per 1M tokens, i.e. an estimated blended price of ~26 / ~51 credits per 1M tokens; this follows DeepSeek's upstream move of routing the legacy model names to V4.1-Flash billing
        - Light Enjoyment Plan: 2 RMB/million tokens per month
    - Token Plan Personal Edition (switched to credit-based deduction effective 2026-08-31 17:00):
        - Hy Token Plan:
            - Lite Plan (28 RMB/month): 560 credits per subscription month
            - Standard Plan (78 RMB/month): 1,560 credits per subscription month
            - Pro Plan (238 RMB/month): 4,760 credits per subscription month (238 RMB × 20 = 4,760, consistent with the other tiers; the source page previously mislabeled this as 1,560 credits, now corrected)
            - Max Plan (468 RMB/month): 9,360 credits per subscription month
            - Supported models (image, video, and other multimodal capabilities temporarily not supported): Hy3, Hy4 preview (Hy3 preview calls auto-route to Hy3)
        - Universal Token Plan:
            - Lite Plan (39 RMB/month): 780 credits per subscription month
            - Standard Plan (99 RMB/month): 1,980 credits per subscription month
            - Pro Plan (299 RMB/month): 5,980 credits per subscription month
            - Max Plan (599 RMB/month): 11,980 credits per subscription month
            - Supported models: Auto, DeepSeek-V4-Flash Official direct-supply, DeepSeek-V4-Pro Official direct-supply, MiniMax-M2.7, MiniMax-M3, GLM-5, GLM-5.1, GLM-5.2, GLM-5.3, GLM-5.3-Flash, Kimi K2.7 Code, Kimi K3, Hy4 preview (Kimi-K2.5 discontinued)
            - DeepSeek-V4-Flash/DeepSeek-V4-Pro Official direct-supply model aliases deepseek/deepseek-v4-flash-0731, deepseek/deepseek-v4-flash, deepseek/deepseek-v4-pro-0813, deepseek/deepseek-v4-pro
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
    - Supported models: Spark-X2.5, Spark-X2-Flash, GLM-5.2, GLM-5.1, GLM-5, DeepSeek-V4-Pro, DeepSeek-V4-Flash, DeepSeek-V3.2, Kimi-K2.6, Kimi-K2.5, MiniMax-M2.5, Qwen3.5-397B-A17B, Qwen3.6-35B-A3B, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, GLM-4.7-Flash
- [iFlytek Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html) [Subscription](https://maas.xfyun.cn/packageSubscription)
    - Professional (39 RMB/month): Per 5 hours: maximum ~1,200 requests; per week: maximum ~9,000 requests; per subscription month: maximum ~18,000 requests. Supports Spark-X2-Agent, Spark-X2, Auto, GLM-5.1, GLM-5, MiniMax-M2.5, Kimi-K2.6, Kimi-K2.5, DeepSeek-V3.2, Spark-X2-Flash, Qwen3.6-35B-A3B, GLM-4.7-Flash, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, Qwen3.5-397B-A17B models
    - Efficient (199 RMB/month): Per 5 hours: maximum ~6,000 requests; per week: maximum ~45,000 requests; per subscription month: maximum ~90,000 requests. Supports Spark-X2-Agent, Spark-X2, Auto, GLM-5, GLM-5.2, DeepSeek-V4-Pro, DeepSeek-V4-Flash, MiniMax-M2.5, Kimi-K2.6, Kimi-K2.5, DeepSeek-V3.2, Spark-X2-Flash, Qwen3.6-35B-A3B, GLM-4.7-Flash, Qwen3.5-35B-A3B, Qwen3-Coder-Next-FP8, Qwen3.5-397B-A17B models
- [CTCloud Programming Token Plan](https://www.ctyun.cn/document/11061839/11092368): billing switched from a fixed token allowance to credits ("Programming Token Plan (Credits Edition)", page updated 2026-09-23)
    - 29 RMB/month: 3,000 credits
    - 89 RMB/month: 10,000 credits
    - 199 RMB/month: 25,000 credits
    - 399 RMB/month: 50,000 credits
    - 699 RMB/month: 100,000 credits
    - Supported models (credits edition): DeepSeek-V4-Pro, DeepSeek-V4-Flash-0731, GLM-5.2, GLM-5.1, Kimi-K2.6, MiniMax-M3
    - Credit-to-token conversion (tokens per credit, input/output): DeepSeek-V4-Pro 1,111/370; DeepSeek-V4-Flash 3,333/1,111; GLM-5.2 1,250/357; GLM-5.1 input [0,32k] 1,667 (output 417) and input (32k,200k] 1,250 (output 357); Kimi-K2.6 1,538/370; MiniMax-M3 input [0,512k] 4,762 (output 1,190) and input (512k,1M] 2,381 (output 595)
    - Official note: the plan model library is updated dynamically — models may be added, replaced, upgraded, re-scoped or retired according to model performance, stability and supply, and the plan only grants access to the models adapted for the current period with no guarantee of permanently providing any given model
    - The previous token-metered plans are being retired: only existing subscribers may renew and new purchases are not supported; their supported models are now DeepSeek-V4-Flash-0731, GLM-5.1, GLM-5.0 (retiring 2026-10-10) and DeepSeek-V3.2 (written "DeepSeeV3.2" on the page, retiring 2026-10-10)
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
    - Supported models: step-5-preview (next-generation flagship base model), step-3.7-flash, step-3.5-flash-2603, step-3.5-flash, stepaudio-2.5-realtime, stepaudio-2.5-chat, stepaudio-2.5-tts, stepaudio-2.5-asr, step-router-v1 (intelligent routing between deepseek-v4-pro and step-3.5-flash)
    - step-image-edit-2 (text-to-image and image editing model, originally scheduled for retirement on 2026-10-10) has been removed from the supported model list and the official page also deleted the image model retirement notice; the page after the switch to Credit monthly-pool billing no longer includes any image generation/editing model
- [Xiaomi MiMo Token Plan (Personal Edition)](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription) (the official page title changed from "Subscription" to "Personal Edition", and the plan purchase note now reads "only one Personal Edition plan can be held at a time")
    - Lite (39 RMB or 6 USD/month): 4.1B Credits per month
    - Standard (99 RMB or 16 USD/month): 11B Credits per month
    - Pro (329 RMB or 50 USD/month): 38B Credits per month
    - Max (659 RMB or 100 USD/month): 82B Credits per month
    - Supported models: All plans support MiMo-V2.6-Pro, MiMo-V2.6-Flash, MiMo-V2.5-Pro, MiMo-V2.5, MiMo-V2.5-ASR, MiMo-V2.5-TTS-VoiceClone, MiMo-V2.5-TTS-VoiceDesign, MiMo-V2.5-TTS (8 models total; MiMo-V2-Pro, MiMo-V2-Omni and MiMo-V2-TTS were removed from the list and the Credit table)
    - MiMo-V2.6-Pro and MiMo-V2.6-Flash are new models whose Credit conversion matches the previous generation: V2.6-Pro is 2.5 cached input / 300 uncached input / 600 output Credits per token, V2.6-Flash is 2 / 100 / 200 Credits per token (identical to V2.5-Pro / V2.5; ASR remains 30M Credits per hour)
    - **mimo-v2.5-pro and mimo-v2.5 will be retired at 10:00 Beijing time on 2026-10-21; the official page advises switching to the new models as soon as possible.**
    - Credit consumption: language models deduct Credits by token count, ASR deducts by input audio duration, and the TTS series is free for a limited time and does not consume plan Credits
    - The discounts are now only "88% off first purchase, 88% off annual auto-renewal, 0.8x consumption at night (0:00-8:00)"; the Token Plan upgrade "Credits usage reset" campaign (effective 2026-05-27) has been removed from the page

- [OpenCode Go](https://opencode.ai/docs/zh-cn/go) (low-cost open-source coding model subscription for international users)
    - $10/month
    - Usage limits: defined per model as a monthly amount; 5 hours = 20% of the monthly limit, week = 50%, month = 100% (monthly limits differ per model, e.g. GLM-5.3 $15, GLM-5.3-Flash $60)
    - Supported models: Grok 4.7, Grok 4.6, GLM-5.3/5.3-Flash/5.2/5.1, GPT 5.6 Luna, Kimi K3/K2.7 Code/K2.6, LongCat-2.0, MiMo-V2.6-Flash/V2.6-Pro/V2.5/V2.5-Pro, MiniMax M3/M2.7/M2.5, **Muse Spark 1.3 Contributor**, **Muse Spark 1.2 Contributor**, Qwen3.8 Max/Qwen3.8 Flash/Qwen3.7 Max/Qwen3.7 Plus/Qwen3.6 Plus, DeepSeek V4 Pro/V4 Flash/V4 Flash Vision Exp, Hy4 preview, Hy3, **Omen Alpha**
    - Grok 4.7 is a new model: pricing and request limits are the same as Grok 4.6 (≤200K tokens: input $2.00 / output $6.00 / cache read $0.50; >200K tokens: input $4.00 / output $12.00 / cache read $1.00 per 1M tokens; monthly usage allowance $15; request limits 169 per 5 hours, 423 per week, 845 per month); model ID grok-4.7, endpoint https://opencode.ai/zen/go/v1/responses
    - MiMo-V2.6-Flash and MiMo-V2.6-Pro are new models: pricing and request limits are identical to the previous generations they replace — V2.6-Flash input $0.14 / output $0.28 / cache read $0.0028 (allowance $60, request limits 30,100 per 5 hours, 75,200 per week, 150,400 per month, model ID mimo-v2.6-flash); V2.6-Pro input $0.435 / output $0.87 / cache read $0.003625 (allowance $15, request limits 3,250 per 5 hours, 8,150 per week, 16,300 per month, model ID mimo-v2.6-pro)
    - The DeepSeek V4.1 Flash model ID was renamed from deepseek-flash to deepseek-v4.1-flash (endpoint https://opencode.ai/zen/go/v1/chat/completions)
    - Hy4 preview is a new model: input $0.834/1M, output $2.501/1M, cache read $0.042/1M (usage allowance $30); request limits 1,350 per 5 hours, 3,380 per week, 6,770 per month; model ID hy4-preview
    - Omen Alpha is a new model: input $0.20/1M, output $0.66/1M, cache read $0.04/1M (usage allowance $100/month); request limits 11,600 per 5 hours, 29,000 per week, 57,900 per month; model ID omen-alpha
    - Muse Spark 1.3 Contributor is a new model: allows Meta to use prompts and completions for training future models in exchange for heavily discounted token pricing (input $0.10/1M, output $0.20/1M, cache read $0.002/1M, usage allowance $60); request limits 45,300 per 5 hours, 113,300 per week, 226,600 per month; model ID muse-spark-1.3-contributor. Only available in regions permitted by Meta's [Geographic Use Policy](https://ai.developer.meta.com/legal/geographic-use-policy)
    - Muse Spark 1.2 Contributor is a new model: allows Meta to use prompts and completions for training future models in exchange for heavily discounted token pricing (input $0.10/1M, output $0.20/1M, cache read $0.002/1M). Only available in regions permitted by Meta's [Geographic Use Policy](https://ai.developer.meta.com/legal/geographic-use-policy)
    - Qwen3.8 Flash is a new model: input $0.15/1M, output $0.47/1M, cache read $0.016/1M, cache write $0.20/1M (usage limit $30); request limits 5,400 per 5 hours, 13,500 per week, 27,000 per month; model ID qwen3.8-flash
    - Qwen3.7 Max: request limits 170 per 5 hours, 420 per week, 840 per month, usage allowance $30/month; pricing input $2.50/1M, output $7.50/1M, cache read $0.50/1M, cache write $3.125/1M (from 2026-09-01 the request limits were halved from 340/840/1,690 and the monthly usage allowance was reduced from $60 to $30)
    - DeepSeek V4.1 Flash limits temporarily boosted 4x: monthly usage allowance raised from $15 to $60 (limited-time promotion, end date extended from 2026-09-20 to 2026-09-27), with request limits raised to 26,000 per 5 hours, 65,000 per week, 130,000 per month (previously 6,500/16,250/32,500); token pricing unchanged (off-peak input $0.15/1M, output $0.60/1M, cache read $0.003/1M; peak pricing is double)
- [StepFun International Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)
- [UniAI GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)
- [Moorethreads AI Coding Plan](https://code.mthreads.com/)
- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)
- [DeepSeek API Pricing](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/):
    - Peak-valley pricing: off-peak price is half of peak; peak hours are Monday to Friday 9:00-12:00, 14:00-18:00 Beijing time (the rest are off-peak)
    - deepseek-flash (DeepSeek-V4.1-Flash, 1M context, supports image understanding; the official model name to use):
        - Off-peak: cached input 0.02 RMB / uncached input 1 RMB / output 4 RMB per 1M tokens
        - Peak: cached input 0.04 RMB / uncached input 2 RMB / output 8 RMB per 1M tokens
        - Old model names deepseek-v4-flash and deepseek-v4-flash-vision-exp are discontinued; calls still work but are served by DeepSeek-V4.1-Flash and billed at Flash pricing
    - deepseek-v4-pro (DeepSeek-V4-Pro-0813, 1M context, no image understanding):
        - Off-peak: cached input 0.15 RMB / uncached input 4.5 RMB / output 13.5 RMB per 1M tokens
        - Peak: cached input 0.30 RMB / uncached input 9.0 RMB / output 27.0 RMB per 1M tokens
        - V4 Pro retirement was announced but has been reversed: DeepSeek will keep serving the DeepSeek V4 Pro API after 2026-09-14 with unchanged billing (the earlier notice said all requests would be routed to V4.1 Flash and billed at Flash pricing)

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

| Name                                                                                | Parameters | Active                | Vision |
|-------------------------------------------------------------------------------------|------------|-----------------------|--------|
| [DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | 284B       | 13B                   | N      |
| [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)           | 284B       | 13B                   | N      |
| [DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)     | 1.6T       | 49B                   | N      |
| [DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)               | 1.6T       | 49B                   | N      |
| [DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)       | 552B       | 8B input / 16B output | Y      |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)                       | 30B        | 3B                    | N      |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                                   | 355B       | 32B                   | N      |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                                   | 744B       | 40B                   | N      |
| [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)                                   | 744B       | 40B                   | N      |
| [GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash)                       | 320B       | 18B                   | Y      |
| [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3)                                   | 744B       | 40B                   | N      |
| [Hy3-preview](https://huggingface.co/tencent/Hy3-preview)                           | 295B       | 21B                   | N      |
| [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)                                | 2.8T       | 104B                  | Y      |
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)                            | 1T         | 32B                   | Y      |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)                           | 428B       | 23B                   | Y      |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)                       | 230B       | 10B                   | N      |
| [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)                  | 2.4T       | 95B                   | Y      |
| [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)                              | 27B        | -                     | Y      |
| [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)                | 180B       | 6B                    | Y      |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)                  | 397B       | 17B                   | Y      |

## Update History

- 2026/09/23: The Volcano Engine Coding Plan (Personal Edition) and Agent Plan (Personal Edition) model libraries were updated: added doubao-seed-2.1-pro (new-generation flagship model with all-round capability gains, 1024k context window / 256k output), doubao-seed-2.1-lite (lightweight and efficient, 1024k context window / 256k output), doubao-seed-2.0-mini (ultra-fast responses, 256k context window / 128k output) and deepseek-v4.1-flash (the lightweight flagship of DeepSeek's new-architecture series, 552B total-parameter MoE, natively capable of multimodal vision understanding, 1024k context window / 384k max output; it had already joined the Agent Plan and now joins the Coding Plan); doubao-seed-2.1-turbo and doubao-seed-2.0-lite are marked "being retired" (the official announcement calls it "model retirement initiated"), and doubao-seedance-1.5-pro was removed from the Agent Plan model table; the Agent Plan deduction coefficients were updated accordingly — doubao-seed-2.1-pro 2.5, doubao-seed-2.1-lite 0.5 (4.5 with audio input), and doubao-seed-2.0-mini refined to 0.25 without audio input / 2.5 with audio input; both the Coding Plan and Agent Plan 1M-context supported lists now include deepseek-v4.1-flash (Agent Plan list: doubao-seed-evolving, glm-5.3, glm-5.3-flash, kimi-k3, kimi-k2.8-preview, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro)
- 2026/09/23: The CTCloud Programming Token Plan switched to credit metering and gained a "Programming Token Plan (Credits Edition)": tiers and prices are unchanged (29/89/199/399/699 RMB per month) but the quota changed from a fixed token allowance to 3,000/10,000/25,000/50,000/100,000 credits per subscription month, and the supported models became DeepSeek-V4-Pro, DeepSeek-V4-Flash-0731, GLM-5.2, GLM-5.1, Kimi-K2.6 and MiniMax-M3 (GLM-5.0 and DeepSeek-V3.2 moved out). The page added a "credit-to-model conversion" table (tokens per credit, input/output — DeepSeek-V4-Pro 1,111/370, DeepSeek-V4-Flash 3,333/1,111, GLM-5.2 1,250/357, GLM-5.1 input [0,32k] 1,667 (output 417) and input (32k,200k] 1,250 (output 357), Kimi-K2.6 1,538/370, MiniMax-M3 input [0,512k] 4,762 (output 1,190) and input (512k,1M] 2,381 (output 595)) plus a note that the model library is updated dynamically and no given model is guaranteed permanently. The previous token-metered plans are labelled "old plans being retired — only existing subscribers may renew, new purchases not supported", with their supported models now DeepSeek-V4-Flash-0731, GLM-5.1, GLM-5.0 (retiring 2026-10-10) and DeepSeek-V3.2 (written "DeepSeeV3.2" on the page, retiring 2026-10-10)
- 2026/09/23: The Kuaishou Wanqing (StreamLake/Vanchin, the platform behind the KwaiKAT Coding Plan) model list added DeepSeek-V4.1-Flash (listed in the multimodal section: deep thinking + image understanding, 1M context / 384K max output, native multimodal visual understanding, default rate limit RPM 10 / TPM 300,000; model list page updated 2026-09-22 23:11); this page is Wanqing's pay-as-you-go model catalog and does not state whether the model is covered by the KwaiKAT Coding Plan quota
- 2026/09/23: Alibaba Cloud Bailian Token Plan (Personal Edition) abolished the weekly limit and switched to a subscription-month quota (relevant pages updated 2026-09-22 23:52): the Personal Edition moved from a "fixed 7-day window quota" to a monthly quota — a subscription month runs 30 days from the subscription date, and once cumulative consumption within the subscription month reaches the plan quota, service is paused until the quota resets in the next subscription month (auto-refreshed based on the subscription date, not a fixed calendar date), with unused quota not rolling over; per-tier quotas were adjusted to Lite 11,500 / Essential 25,500 / Standard 45,000 / Pro 180,000 Credits per month (tiers and prices unchanged, limited-time prices 39/79/139/499 RMB per month), and the remaining quota of existing subscriptions was reset once to the full monthly quota of the corresponding plan on 2026-09-22 with the subscription cycle and expiry date unchanged; the previous "reset card / quota reset entitlement" (the "Reset quota" button and reset-count notes on the page) was removed entirely, with quota resets now handled automatically each subscription month; the deduction order became "each request is deducted first from the current subscription month's plan quota, and once exhausted, from Usage Pack quota", and Usage Packs are no longer described as "not subject to the 7-day window limit" but rather as "neither occupying nor counting toward the plan monthly quota"; the upgrade rule changed so that the current subscription cycle is not reset — the price difference is paid as (new plan price − old plan price) × remaining days ÷ 30 (partial days counted as a full day), and the new quota for the current cycle is granted as remaining days ÷ 30 × (new monthly quota − old monthly quota), rounded up, with the new tier's monthly quota applying from the next subscription month; the 429 error message changed from `insufficient_quota: Your token-plan 1-week quota has been exhausted.` to `insufficient_quota: Your token-plan quota has been exhausted.`; the Team Edition FAQ comparison table's "Personal Edition quota mechanism" was updated to "monthly quota, auto-refreshed per subscription month", and the Team Edition overview table dropped the "7-day limit: unlimited" row
- 2026/09/22: The SenseTime SenseNova API docs (including the TokenPlan credits rules and model overview) changed their model library: DeepSeek V4 Pro was removed from the model overview and DeepSeek V4.1 Flash was added (model ID `deepseek-flash`, 1M context, image input support), while DeepSeek V4 Flash (`deepseek-v4-flash`) stays listed. The corresponding model sections were rewritten and gained an image-input section with limits (single image ≤50 MB, ≤200 images per request, ≤64 MB per request body, ≤200 MB total for URL-passed images; video input is only supported by the Chat Completions API), `max_tokens` now defaults to 131072 (range 1–393216, thinking is truncated when it exceeds the limit), `reasoning_effort` has native none/low/high/max levels with compatibility mappings, and explicit caching is stated as unsupported
- 2026/09/22: Zhipu GLM Coding Plan (announced on both the China site bigmodel.cn and the international z.ai DevPack pages) added two limited-time campaigns: the "GLM-5.3-Flash Usage Campaign" — from 2026-09-03 to 2026-10-07, daily 23:00–09:00, plan users get unlimited GLM-5.3-Flash usage via [ZCode](https://zcode.z.ai/cn) plus doubled quota on other agents; and the "Double Festival" campaign — from 2026-09-25 to 2026-10-07 all-day usage is charged at the off-peak rate (50% points consumption around the clock). The official pages note that stacking the night campaign on top makes the actual available quota far higher than the allowance reference table suggests
- 2026/09/22: Alibaba Cloud Bailian model calling prices, model library and context cache updated: the Stepfun deployment added stepfun/step-5-preview (7 CNY input / 20 CNY output per million tokens, no free quota, alongside stepfun/step-3.7-flash at 1.35/8.1 CNY) and the Unisound section lists unisound/unisound-u2 (1 CNY input / 2 CNY output; the section appears twice on the page); a new "audio generation" billing section was added (qwen-audio-3.1-tts-next, billed on input and output tokens at 6/12 CNY); speech recognition added the Qwen-Audio-3.1 series and switched from per-second audio billing to per-token billing — qwen-audio-3.1-asr-flash-message and qwen-audio-3.1-asr-flash-streaming cost 6/4.5 CNY (international 6.781/5.104 CNY), qwen-audio-3.1-asr-flash-filetrans and qwen-audio-3.1-asr-flash cost 0.8/2.7 CNY (international 1.094/3.427 CNY), while the 3.0 series per-second tiers remain; the "Choose a model" page switched its speech-recognition recommendation from qwen-audio-3.0-asr-flash-streaming/-filetrans to the 3.1 versions; the context-cache Stepfun (StepFun deployment) list added stepfun/step-5-preview; qwen3.8-max-prime's fast-mode doc link changed from /fast-mode to /prime-mode; the Workspace ID link in the official OpenCode / OpenClaw integration docs changed from "Get Workspace ID" to the regions page (/zh/model-studio/regions#h2_migrate_domain)
- 2026/09/22: Alibaba Cloud Bailian Token Plan (Personal Edition) night discount changed: qwen3.8-max went from 50% off to 40% off and qwen3.8-flash was added at 40% off; deepseek-v4-pro-0813, deepseek-v4-flash-0731 and deepseek-v4.1-flash stay at 50% off (all are Credits-consumption discounts for calls between 22:00 and 08:00)
- 2026/09/22: OpenCode Go added three models — Grok 4.7, MiMo-V2.6-Flash and MiMo-V2.6-Pro. Grok 4.7 has the same pricing and request limits as Grok 4.6 (≤200K tokens: input $2.00 / output $6.00 / cache read $0.50; >200K tokens: $4.00/$12.00/$1.00 per 1M tokens; allowance $15/month; request limits 169 per 5 hours, 423 per week, 845 per month; model ID grok-4.7). MiMo-V2.6-Flash/V2.6-Pro have pricing and request limits identical to the previous generations they replace, MiMo-V2.5/V2.5-Pro ($0.14/$0.28/$0.0028 with a $60 allowance, and $0.435/$0.87/$0.003625 with a $15 allowance)
- 2026/09/22: The Xiaomi MiMo Token Plan page was reworked into the "Personal Edition" and its supported models went from 9 to 8 — mimo-v2.6-pro and mimo-v2.6-flash were added (Credit conversion matches the previous generation: V2.6-Pro 2.5 cached / 300 uncached / 600 output, V2.6-Flash 2/100/200 Credits per token), while MiMo-V2-Pro, MiMo-V2-Omni and MiMo-V2-TTS were removed from the supported-model list and the Credit table; a notice at the top of the page states that mimo-v2.5-pro and mimo-v2.5 will be retired at 10:00 Beijing time on 2026-10-21. Plan prices and quotas are unchanged (39/99/329/659 RMB or 6/16/50/100 USD per month, 4.1B/11B/38B/82B Credits per month). The discount description was narrowed to "88% off first purchase, 88% off annual auto-renewal, 0.8x consumption at night", the earlier Token Plan upgrade "Credits usage reset" campaign (effective 2026-05-27) was removed from the page, and the purchase note now reads "only one Personal Edition plan can be held at a time"
- 2026/09/21: Alibaba Cloud Bailian Token Plan (Personal Edition) added auto to its supported models (official description: "a platform-provided smart model that automatically matches the underlying model to the request, balancing quality and cost"; capability label "reasoning, text generation"; listed first under the Qwen brand in the model table). The official OpenCode / OpenClaw integration docs added an auto entry to both the Personal and Team Edition configurations (in OpenCode it only declares text input/output, with no reasoning or limit fields; in OpenClaw contextWindow 1,000,000, maxTokens 393,216, reasoning false) and changed OpenClaw's default model from `bailian-token-plan/qwen3.8-flash` to `bailian-token-plan/auto`
- 2026/09/21: Alibaba Cloud Bailian's model calling prices and context-cache supported model list added two models — ZHIPU/GLM-5.3-FlashX (Zhipu deployment, thinking mode only, 2 CNY input / 7 CNY output per million tokens, no free quota; cache-hit discount 28.5%, higher than the 25% of the other five models in the same series such as ZHIPU/GLM-5.3-Flash) and vanchin/deepseek-v4.1-flash (Kuaishou Wanqing deployment, 2 CNY input / 8 CNY output per million tokens; cache-hit discount 2%, lower than vanchin/deepseek-v4-pro's 8.33%)
- 2026/09/21: OpenCode Go extended its limited-time 4x quota boost for DeepSeek V4.1 Flash — the end date moved from 2026-09-20 to 2026-09-27 (the $60 monthly usage allowance, the request limits of 26,000 per 5 hours / 65,000 per week / 130,000 per month and the token pricing are all unchanged)
- 2026/09/20: StepFun Step Plan added step-5-preview to its supported models (next-generation flagship base model for real-world tasks) and removed step-image-edit-2 along with the previous image model retirement notice, so the plan no longer covers any text-to-image or image editing model; the official model description correspondingly changed from "flagship models covering text, reasoning, voice, image editing and intelligent routing" to "text, reasoning, voice and intelligent routing". The official docs also split the Base URL guidance per tool — Claude Code / Anthropic SDK use `https://api.stepfun.com/step_plan` while OpenAI SDK Chat Completions calls still use `https://api.stepfun.com/step_plan/v1` — and clarified that the Step Plan channel consumes plan Credits and is independent of the regular API channel quota (the FAQ now likewise says to pick the address by tool)
- 2026/09/18: The Kimi Code docs added per-model ID membership tier requirements and introduced the Plus / Pro tier names for the first time — k3 / k3-256k require Moderato / Plus or above (1M context requires Allegretto / Pro or above); the wording for kimi-for-coding changed from "available to all members" to "available to Andante / Plus or above"; kimi-for-coding-highspeed requires Allegretto / Pro or above. The same page added overseas API endpoint domains: Kimi Code overseas OpenAI-compatible https://api.kimi.ai/coding/v1 and Anthropic-compatible https://api.kimi.ai/coding/, and Kimi Open Platform overseas https://api.moonshot.ai/v1 (domestic endpoints are api.kimi.com/coding and api.moonshot.cn/v1)
- 2026/09/18: OpenCode Go removed the Union Alpha Free model (limited-time free period ended) — the model (model ID union-alpha) was removed from the supported model list, the token price table, the request limit table and the endpoint table
- 2026/09/18: Volcano Engine Coding Plan (Personal Edition) and Agent Plan (Personal Edition) added the kimi-k2.8-preview model (overall performance close to K3 with higher thinking efficiency, supports text and image input; 1M context window / 1M max output, supported by all plans); Agent Plan deduction coefficient 8, at 40% off (4.8) from 2026-09-17 00:00 to 2026-09-30 23:59; during the promotion from 2026-09-18 00:00 to 2026-09-30 23:59 the available quota of this model in the Coding Plan is comparable to that during the Agent Plan 40%-off deduction promotion; the model also joins the 1M-context supported list (now glm-5.3, glm-5.3-flash, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro, kimi-k3, kimi-k2.8-preview)
- 2026/09/18: Alibaba Cloud Bailian Token Plan Personal Edition added the Essential tier, expanding the personal tiers from three (Lite/Standard/Pro) to four: list price 120 RMB/month, 79 RMB/month for a limited time, 5,625 Credits every 7 days (2.25x Lite), supports 2-3 concurrent Agents, and its benefits are all Lite benefits; the official page also moved the Usage Pack (100 RMB each/month, 20,000 Credits; requires an active subscription, up to 5 held at a time, not subject to the 7-day window limit) from a table row to a footnote
- 2026/09/17: OpenCode Go added the Union Alpha Free model (limited time): input/output/cache read are all Free, with unlimited requests and quota (limited time); model ID union-alpha, endpoint https://opencode.ai/zen/go/v1/messages (Anthropic-compatible)
- 2026/09/16: Alibaba Cloud Bailian Token Plan (Personal Edition) added glm-5.3 to its "Supported models" list (Zhipu AI, capability label "reasoning, text generation", coexisting with glm-5.2; glm-5.3 had already been added to the Bailian model catalog on 2026-09-15 but was not part of the Token Plan at that time); the official integration docs added the corresponding model config — OpenClaw with contextWindow 1,000,000, maxTokens 16,384, reasoning false, and OpenCode with thinking enabled (budgetTokens 8192); the Personal Edition limited-time night 50%-off list is unchanged (qwen3.8-max, deepseek-v4-pro-0813, deepseek-v4-flash-0731, deepseek-v4.1-flash)
- 2026/09/15: Kuaishou Wanqing (StreamLake/Vanchin, the platform behind the KwaiKAT Coding Plan) model list added three models — GLM-5.3, GLM-5.3-Flash and DeepSeek-V4-Pro-0813 (model list page updated 2026-09-15 21:15); this page is Wanqing's pay-as-you-go model catalog and does not state whether these models are covered by the KwaiKAT Coding Plan quota
- 2026/09/15: Alibaba Cloud Bailian model calling prices added the GLM model glm-5.3 (non-thinking and thinking modes, no token tiers, 8 CNY input / 28 CNY output per million tokens, the same price for China-site regions such as China North 2 (Beijing) and the "global" deployment; 10.208/32.084 CNY on the international site) with 1 million free tokens; the list of GLM models supported by context caching (deployed on Alibaba Cloud Bailian) also added glm-5.3 (25% cache-hit discount, the same tier as glm-5.2 and glm-5.2-fast-preview); meanwhile the mode of ZHIPU/GLM-5.3 (GLM deployed by Zhipu) was corrected from "non-thinking and thinking modes" to "thinking mode only" (price unchanged at 8 CNY input / 28 CNY output, no free quota)
- 2026/09/15: Volcano Engine Agent Plan (Personal Edition) added the deepseek-v4.1-flash model (supported by all plans; 1M context window / 384K max output, natively capable of multimodal vision understanding) with a deduction coefficient of 2.5, at 50% off (1.25) from 2026-09-15 00:00 to 2026-09-28 23:59; the model also joins the 1M-context supported list (now glm-5.3, glm-5.3-flash, deepseek-v4.1-flash, deepseek-v4-flash, deepseek-v4-pro, kimi-k3)
- 2026/09/14: In the Alibaba Cloud Bailian Token Plan (Personal Edition) supported-model list, deepseek-v4.1-flash's capability label changed from "reasoning, text generation" to "reasoning, vision understanding, text generation"; the official integration doc (OpenClaw) also changed that model's config `input` from `["text"]` to `["text", "image"]`, confirming the model accepts image input directly within the Token Plan
- 2026/09/14: Volcano Engine Agent Plan (Personal Edition) added two multimodal models: doubao-seedream-5-0-pro (image generation, all plans; input images are free for the first image and 10 AFP per image thereafter, output images cost 150 AFP for ≤2.61M pixels and 300 AFP above that for single-image generation, and 75/150 AFP for layer separation) and doubao-seedance-2.5 (video generation, Large/Max; 210 per token when the input contains video and 350 when it does not for 480p/720p, 230/385 for 1080p); doubao-seedance-1.5-pro is marked as being retired
- 2026/09/14: Alibaba Cloud Bailian Token Plan (Personal Edition) added deepseek-v4.1-flash to its supported models (it had previously only been added to the Bailian model library, not to the Token Plan); the model also joined the Personal Edition limited-time night discount (50% off Credits from 22:00 to 08:00), whose list is now qwen3.8-max, deepseek-v4-pro-0813, deepseek-v4-flash-0731, deepseek-v4.1-flash
- 2026/09/14: Tencent Cloud Token Plan Enterprise Professional Plan (Guangzhou/Singapore) added DeepSeek-V4.1-Flash Official direct-supply (model ID `deepseek/deepseek-flash`) to its model library; the Official direct-supply Flash-series credit prices were lowered across the board — DeepSeek-V4-Flash 0731 Official direct-supply (previously ~39 off-peak / ~77 peak credits per 1M tokens) and DeepSeek-V4-Flash-Vision-Exp Official direct-supply (previously ~35 / ~70) both dropped to match the new model (cached 2 / uncached 100 / output 400 off-peak, 4/200/800 peak; estimated blended ~26 / ~51), following DeepSeek's upstream move of routing the legacy model names to V4.1-Flash billing; the same page removed the GLM-5.3-Flash 50%-off credit-price promotion section that had expired on 2026-09-10
- 2026/09/14: OpenCode Go temporarily boosted the DeepSeek V4.1 Flash limits 4x: monthly usage allowance raised from $15 to $60 (promotion ends 2026-09-20), request limits raised from 6,500 per 5 hours / 16,250 per week / 32,500 per month to 26,000 per 5 hours / 65,000 per week / 130,000 per month; token pricing unchanged
- 2026/09/14: Alibaba Cloud Bailian added deepseek-v4.1-flash to its model library: China North 2 (Beijing) / global pricing is peak input 2 RMB, off-peak input 1 RMB, peak output 8 RMB, off-peak output 4 RMB per 1M tokens (with a 1M-token free quota); international site peak 2.188/8.75 RMB, off-peak 1.094/4.375 RMB. Context-cache hits cost 10% of the input price (peak 0.2 RMB, off-peak 0.1 RMB), a better discount than the 20% applied to other Bailian models but still pricier than DeepSeek's official API cache-hit price (0.04/0.02 RMB). The "Choose a model" page also swapped its featured slot from deepseek-v4-flash-0731 to this model; it is not yet in the Bailian Token Plan (Personal/Team Edition) supported-model lists
- 2026/09/12: OpenCode Go renamed the DeepSeek V4.1 Flash model ID from deepseek-flash to deepseek-v4.1-flash
- 2026/09/12: Kimi Code's standard tier moved from K2.7 Code to K2.8 Preview (model name kimi-for-coding now maps to K2.8 Preview, supporting up to 1M context and low/high/max thinking levels); the High Speed tier remains K2.7 Code HighSpeed
- 2026/09/12: DeepSeek reversed its V4 Pro retirement plan: the vendor will keep providing the DeepSeek V4 Pro API service after 2026-09-14 with unchanged billing
- 2026/09/10: Added DeepSeek-V4.1-Flash to the model parameters comparison table (552B total parameters, 8B input / 16B output activation, multimodal support)
- 2026/09/10: DeepSeek released DeepSeek-V4.1-Flash (new model name deepseek-flash, 1M context, supports image understanding) with significantly lower pricing (off-peak: cached 0.02, uncached 1, output 4 RMB; peak 0.04/2/8 RMB per 1M tokens); old model names deepseek-v4-flash and deepseek-v4-flash-vision-exp are discontinued (requests served by V4.1-Flash at Flash pricing); V4 Pro is planned for orderly retirement — after 2026-09-14 12:00 all deepseek-v4-pro requests route to V4.1 Flash at Flash pricing (note: this change was previously missed by the archiver and added after manual verification)
- 2026/09/10: Zhipu GLM-5.3-Flash limited-time 50% off promotion ended, reverting to standard pricing (uncached input 0.8, output 2.8, cached input 0.23 RMB per 1M tokens); Alibaba Cloud Bailian also removed the "50% off (limited time)" label for the same model; Tencent Cloud Token Plan (Personal Edition Universal Plan and Enterprise Professional Plan) marked GLM-5, GLM-5.1 and GLM-5-Turbo for discontinuation on 2026-10-09; OpenCode Go billing limits redefined as per-model monthly amounts (5 hours = 20% of monthly, week = 50%, month = 100%), with differing monthly limits per model (e.g. GLM-5.3 $15, GLM-5.3-Flash $60)
- 2026/09/09: Volcano Engine Coding Plan (Personal Edition) added the Kimi-K3 model (1M context / 128K max output, native visual understanding, high deduction coefficient, recommended only for Pro plan users); iFlytek Astron Token Plan Team Edition added the Spark-X2.5 model (256K, input 320 / cache 48 / output 1200 / thinking 1200 credits per 1M tokens), Spark-X2 and Spark-X2-Agent discontinued
- 2026/09/04: StepFun Step Plan announced that the step-image-edit-2 model will be retired on 2026-10-10, and the Step Plan text-to-image and image editing APIs will stop serving requests simultaneously
- 2026/09/04: OpenCode Go added support for the Omen Alpha model (input $0.20/1M, output $0.66/1M, cache read $0.04/1M, usage allowance $100/month; request limits 11,600 per 5 hours, 29,000 per week, 57,900 per month; model ID omen-alpha)
- 2026/09/04: Tencent Cloud LLM Token Plan expanded its model library: both the Universal Token Plan (Personal Edition) and the Enterprise Professional Plan added the GLM-5.3-Flash and Kimi K3 models; the Enterprise Professional Plan also published the credit prices for these two models (Guangzhou GLM-5.3-Flash 23/80/280, Kimi K3 200/2000/10000; Singapore GLM-5.3-Flash 21.5898/107.949/359.83, credits per 1M tokens)
- 2026/09/03: Kimi Code page's "Core Advantages" section was revised: it now explicitly states the plan is powered by the flagship K3 model (~2.8 trillion parameters) with the K2.7 Code in two modes (standard / High Speed), with a maximum inference speed of 260 Tokens/s (previously described as 100 Tokens/s) and a 1M Token context window; it removed the statements "High Speed version is 5–6x the standard version" and "approx. 300–1200 requests per 5 hours, max concurrency 30"
- 2026/09/03: Alibaba Cloud Bailian Token Plan (Personal Edition) usage policy tightened: the official guide changed from "you may configure the same API Key on multiple of your own devices (e.g., home and office computers)" to "for the subscriber's own use on a single device."
- 2026/09/03: OpenCode Go added support for the Muse Spark 1.3 Contributor model (Meta Contributor tier: allows Meta to use prompts and completions for training future models in exchange for heavily discounted token pricing; input $0.10/1M, output $0.20/1M, cache read $0.002/1M, usage allowance $60; request limits 45,300 per 5 hours, 113,300 per week, 226,600 per month; model ID muse-spark-1.3-contributor; only available in regions permitted by Meta's [Geographic Use Policy](https://ai.developer.meta.com/legal/geographic-use-policy))
- 2026/09/02: Tencent Cloud LLM Token Plan Personal Edition Hy Token Plan Pro Plan corrected its credits per subscription month from 1,560 to 4,760 (238 RMB/month price unchanged; 1,560 was a mislabel/typo in the official page and inconsistent with the price × 20 pattern of the other tiers)
- 2026/09/01: Volcano Engine Agent Plan (Personal Edition) deduction coefficient rule adjustment: the input and output deduction coefficients for text-generation/embedding models are now determined solely by the model and no longer vary with input length (previously input coefficient = model coefficient × input segment factor: ×0.67 for ≤32k, ×1 for 32k–128k, ×2 for >128k; the length segmentation has been removed). Input/output deduction coefficients per model: doubao-seed-2.0-mini 0.25, doubao-seed-2.0-lite/deepseek-v4-flash 0.5, glm-5.3-flash 0.5 (0.25 for the first two weeks at 50% off), doubao-seed-2.1-turbo/doubao-seed-evolving/minimax-m3 2.5, kimi-k2.7-code 4.5, glm-5.3 (glm-latest) 4.5, deepseek-v4-pro 5.5, kimi-k3 10, doubao-embedding-vision 0.5
- 2026/09/01: OpenCode Go Qwen3.7 Max model allowance reduced: request limits lowered from 340 per 5 hours, 840 per week, 1,690 per month to 170 per 5 hours, 420 per week, 840 per month, and the monthly usage allowance lowered from $60 to $30 (pricing input $2.50/1M, output $7.50/1M, cache read $0.50/1M, cache write $3.125/1M unchanged)
- 2026/08/31: Tencent Cloud LLM Token Plan switched to credit-based deduction: the Personal Edition changed from token quotas to credits effective 2026-08-31 17:00 (Universal Token Plan Lite/Standard/Pro/Max = 39/99/299/599 RMB/month, 780/1,980/5,980/11,980 credits/month; Hy Token Plan Lite/Standard/Pro/Max = 28/78/238/468 RMB/month, 560/1,560/1,560 (as-is in source doc, likely a typo)/9,360 credits/month); Universal Token Plan supported models updated to Auto, DeepSeek-V4-Flash/Pro Official direct-supply, MiniMax-M2.7, MiniMax-M3, GLM-5/5.1/5.2/5.3, Kimi K2.7 Code, Hy4 preview (Kimi-K2.5 discontinued), Hy Token Plan supports Hy3 and Hy4 preview (Hy3 preview auto-routes to Hy3); Enterprise Professional Plan added DeepSeek-V4-Flash-Vision-Exp Official direct-supply (multimodal/visual understanding, text capability on par with V4-Flash Official, multimodal Agent performance approaching Claude Opus-4.8) and removed Kimi-K2.5; DeepSeek V4 Official direct-supply peak-valley billing adjusted from 2026-08-29 to weekdays only (weekends all off-peak), DeepSeek V4 Official peak hours are Mon–Sun 9:00–12:00 and 14:00–18:00
- 2026/08/31: Volcano Engine Coding Plan (Personal Edition) and Agent Plan (Personal Edition) removed the GLM-5.2 model (previously marked as "phasing out"); GLM-5.2 is no longer listed among supported models or in the 1M-context supported list; the GLM-5.3 deduction coefficient description changed from "same as GLM-5.2" to "high"
- 2026/08/31: Alibaba Cloud Bailian model pricing added ZHIPU/GLM-5.3-Flash (thinking-only mode, input 0.8 RMB, output 2.8 RMB per 1M tokens, supports context-cache hit discount at 25%) and qwen-flash-character (0.25/1.5 RMB); qwen3-vl-rerank price lowered (text 0.7→0.5 RMB, image 1.8→0.5 RMB); Token Plan (Personal Edition) limited-time night discount added deepseek-v4-flash-0731
- 2026/08/29: OpenCode Go added the Hy4 preview model (input $0.834/1M, output $2.501/1M, cache read $0.042/1M, usage allowance $30; request limits 1,350 per 5 hours, 3,380 per week, 6,770 per month; model ID hy4-preview)
- 2026/08/29: Volcano Engine Coding Plan (Personal Edition) and Agent Plan (Personal Edition) added the glm-5.3-flash model (Zhipu's first natively multimodal model, 320B total params / 18B active, supports image input, 1M context / 128K max output; first two weeks deduction coefficient at 50% off, promotion ends 2026-09-11 23:59:59); Agent Plan's Agent Evolution changed to first 50 files free
- 2026/08/28: Zhipu International (Z.ai DevPack) GLM Coding Plan model change: all plans now support {GLM-5.3, GLM-5.3-Flash} (was {GLM-5.3, GLM-5-Flash}); requests for GLM-5.2/GLM-5.1 auto-routed to GLM-5.3, GLM-4.7 auto-routed to GLM-5.3-Flash (GLM-5-Turbo no longer a routing target); release notes removed the GLM-5V-Turbo and GLM-5-Turbo model entries
- 2026/08/28: OpenCode Go added support for Qwen3.8 Flash model (input $0.15/1M, output $0.47/1M, cache read $0.016/1M, cache write $0.20/1M, usage limit $30; request limits 5,400 per 5 hours, 13,500 per week, 27,000 per month; model ID qwen3.8-flash)
- 2026/08/28: Infini-AI GenStudio changelog: a batch of models were discontinued on 2026-08-28 (deepseek-r1, deepseek-v3 series, deepseek-v3.2/v3.2-thinking, glm-4.5/4.5-air/4.6/4.7/5/4.5v/4.6v, minimax-m2.1/m2.5, kimi-k2.5), recommended migration to deepseek-v4-flash/v4-pro, glm-5.2, kimi-k2.6, minimax-m2.7; DeepSeek V4 series (deepseek-v4-flash-0731, deepseek-v4-pro-0813) launched on 2026-08-18
- 2026/08/27: Alibaba Cloud Bailian Token Plan (Personal Edition) added model qwen3.8-flash
- 2026/08/27: Volcano Engine Coding Plan (Personal Edition) and Agent Plan DeepSeek-V4-Pro changed from "early-access preview" to officially released (significantly enhanced Agent capabilities, accessible via model name and console selection)
- 2026/08/27: Alibaba Cloud Bailian model pricing adjustments: qwen3.8-flash China input dropped from 1 to 0.8 RMB and output from 3 to 2.7 RMB (international input dropped from 1.167 to 1.094 RMB, output unchanged); added kimi-k3 (thinking-only mode, global 20/100 RMB, international 21.875/109.376 RMB per 1M tokens); tongyi-xiaomi-analysis-flash/pro now support context cache discounts; added kling/kling-v3-turbo video generation model (audio video 720P 0.8 RMB/sec, 1080P 1.0 RMB/sec)
- 2026/08/27: Alibaba Cloud Bailian context cache rule adjustments: implicit cache minimum token count raised from 256 to 1,024 (same as explicit cache, but meaning differs — reaching 1,024 only qualifies for a hit, does not guarantee one); qwen3.8-flash added to cached_token discount exceptions (no longer billed at 20% of input); added tongyi-xiaomi-analysis-pro/flash industry models; added DeepSeek (Kuaishou Wanqing deployment) cache pricing (vanchin/deepseek-v4-pro 8.33%, vanchin/deepseek-v3.2-think 10%, etc.)
- 2026/08/27: Tencent Cloud Token Plan (Personal Edition) Universal Plan Kimi-K2.5 discontinuation date changed from 2026-07-31 to 2026-08-31 (and removed the peak-hour rate-limit notice)
- 2026/08/26: Zhipu added GLM-5.3-Flash API pricing (bigmodel.cn): cached input 0.115/0.23 RMB, uncached input 0.4/0.8 RMB, output 1.4/2.8 RMB per 1M tokens, 1M context, currently 50% off for two weeks
- 2026/08/26: Zhipu GLM Coding Plan supported models changed from {GLM-5.3, GLM-5-Turbo, GLM-4.7} to {GLM-5.3, GLM-5.3-Flash}; GLM-5.3-Flash (320B total params / 18B active, hybrid linear+sparse attention, native vision) launched for Coding Plan with deduction coefficients Input 2.3 / Cached Input 0.56 / Output 8 (including visual understanding MCP); GLM-5-Turbo/GLM-4.7 requests auto-routed to GLM-5.3-Flash; token allowance reference table restructured to show per-model breakdowns at 95%/96%/98% cache hit rates; "save up to 92%" claim restored
- 2026/08/26: OpenCode Go added GLM-5.3-Flash model, removed Ox Alpha Free model (limited-time free ended)
- 2026/08/26: Qwen3.8-Flash-Next and GLM-5.3-Flash released
- 2026/08/26: MiniMax Token Plan price adjustment: International edition Plus/Max/Ultra plans increased from $20/$50/$120/month to $22/$55/$132/month; Chinese edition prepaid credits packages adjusted — ¥30 for 4,489 credits (was 4,285), ¥150 for 22,460 credits (was 21,430), ¥500 for 74,900 credits (was 71,435); Chinese subscription plan prices unchanged
- 2026/08/26: OpenCode Go upgraded Grok model from 4.5 to 4.6: rate limits increased (169/5hr, 423/week, 845/month, previously 120/300/600), pricing changed to tiered (≤200K tokens: input $2.00, output $6.00, cache $0.50; >200K tokens: input $4.00, output $12.00, cache $1.00, previously flat $2.00/$6.00/$0.30), model ID changed from grok-4.5 to grok-4.6
- 2026/08/25: Tencent Cloud Token Plan Enterprise Professional Plan lowered minimum purchase from 100K to 50K Credits, added DeepSeek-V4-Flash 0731 Official and DeepSeek-V4-Pro 0813 Official models (peak-valley pricing, off-peak rates same as direct-supply versions)
- 2026/08/25: OpenCode Go added support for LongCat-2.0 model (input $0.30/1M, output $1.20/1M, cache read $0.006/1M)
- 2026/08/24: OpenCode Go removed first-month discount, pricing changed from "$5 first month, then $10/month" to a flat $10/month
- 2026/08/23: DeepSeek API peak-valley weekend rule now in effect: peak hours are explicitly Monday to Friday 9:00-12:00, 14:00-18:00 Beijing time; weekends are now charged at off-peak rates all day
- 2026/08/22: DeepSeek API peak-valley pricing rule adjustment: starting 2026-08-23 (Sunday) 00:00 Beijing time, weekends (Saturday and Sunday) will no longer distinguish peak/off-peak — all day will be charged at off-peak rates (previously weekends still followed peak/off-peak schedule)
- 2026/08/21: Volcano Engine Coding Plan (Personal Edition) added support for Doubao-Seed-Evolving model (for Coding & Agent scenarios, weekly upgrades, 1M context window, 256K max output); OpenCode Go added support for DeepSeek V4 Flash Vision Exp model (pricing Off-Peak $0.22/$0.66, Peak $0.44/$1.32 per 1M tokens, images converted to tokens based on size); Tencent Cloud Token Plan (Personal Edition) Universal Plan removed discontinued models (Tencent HY 2.0 Instruct, Tencent HY 2.0 Think, Hunyuan-T1, Hunyuan-TurboS, MiniMax-M2.5)
- 2026/08/21: DeepSeek added new vision model deepseek-v4-flash-vision-exp (experimental), priced same as deepseek-v4-flash, FIM completion not supported, concurrency limit 2500, images converted to tokens based on size; Tencent Cloud Token Plan Enterprise Professional Plan removed MiniMax-M2.5 model; Volcano Engine Agent Plan (Personal Edition) updated quota rules: image/video generation models, voice models, and Harness merged into a single daily quota category (no longer separated as "vision models" and "voice models"), daily quota uniformly set to half of monthly plan quota; OpenCode Go added Ox Alpha Free model (limited-time free)
- 2026/08/20: CTCloud Programming Token Plan updated supported models: added GLM-5.1, DeepSeek-V4-Flash-0731; renamed GLM-5 to GLM-5.0 (Official); DeepSeek-V3.2 labeled as Flagship
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
- 2026/03/18: Z.ai released GLM-5-Turbo model:
    - Designed for high-throughput OpenClaw lobster workloads, GLM-5-Turbo focuses on improving stability and efficiency in long-chain Agent tasks, enabling smoother execution for complex, multi-step workflows.
    - It strengthens tool and Skills integration and enhances complex instruction decomposition, allowing the model to better identify task goals, plan execution steps, coordinate across multiple agents, and maintain temporal consistency in extended tasks.
    - GLM-5 support in Coding Plan: Supported on both Max and Pro plans; expected to be available on the Lite plan by the end of March
    - GLM-5-Turbo support in Coding Plan: Supported on the Max plan; expected to be available on the Pro plan by the end of March and on the Lite plan sometime in April
    - GLM-5 and GLM-5-Turbo are advanced models designed to rival Claude Opus model. Its usage will be deducted at 3 × during peak hours and 2 × during off-peak hours. We recommend switching to GLM-5 for complex tasks and continuing to use GLM-4.7 for routine tasks to avoid rapid quota consumption. As a limited-time benefit, GLM-5-Turbo will only consume 1× quota during off-peak hours, valid through the end of April. Peak hours are 14:00–18:00 (UTC+8).
- 2026/03/17: Added iFlytek MaaS Astron Coding Plan
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
