# AI Coding Plan

## Coding Plan

### Kimi

[Kimi Membership](https://www.kimi.com/membership/pricing)

- Andante (49 RMB/month): A 5-hour token quota supports approximately 300–1,200 API calls, with a maximum concurrency of 30, ensuring uninterrupted operation for complex workloads
- Moderato (99 RMB/month): 4x Kimi Code quota
- Allegretto (199 RMB/month): 20x Kimi Code quota
- Allegro (699 RMB/month): 60x Kimi Code quota
- Based on actual testing, Andante limits total uncached input + output tokens to 1M per 5 hours (i.e. not counting cached input tokens), 4M per week
- [K2.5 API Pricing](https://platform.moonshot.cn/docs/pricing/chat):
    - Cached input: 0.7 RMB per 1M tokens
    - Uncached input: 4 RMB per 1M tokens
    - Output: 21 RMB per 1M tokens
    - 256K context

### MiniMax

[MiniMax Coding Plan](https://platform.minimaxi.com/docs/coding-plan/intro)

- Starter (29 RMB/month): 40 prompts / per 5 hours
- Plus (49 RMB/month): 100 prompts / per 5 hours
- Max (119 RMB/month): 300 prompts / per 5 hours
- Plus-High-Speed (98 RMB/month): 100 prompts / per 5 hours
- Max-High-Speed (199 RMB/month): 300 prompts / per 5 hours
- Ultra-High-Speed (899 RMB/month): 2000 prompts / per 5 hours
- Q: Why is “1 prompt ≈ 15 model calls”? A: In an AI coding tool, a single action you take (like requesting code completion or an explanation) may be broken down by the tool into multiple, consecutive interactions with the AI model behind the scenes (e.g., fetching context, generating suggestions, refining suggestions, etc.). To simplify billing, we bundle these backend calls into a single “prompt” count. This means that 1 “prompt” within your plan actually covers multiple complex model invocations.
- [M2.5 API Pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo):
    - Cached input: 0.21 RMB per 1M tokens
    - Uncached input: 2.1 RMB per 1M tokens
    - Cache write input: 2.625 RMB per 1M tokens
    - Output: 8.4 RMB per 1M tokens
    - 200K context

[MiniMax International Coding Plan](https://platform.minimax.io/docs/coding-plan/intro)

- Starter (10 USD/month): 100 prompts / per 5 hours
- Plus (20 USD/month): 300 prompts / per 5 hours
- Max (50 USD/month): 1000 prompts / per 5 hours

### Zhipu (GLM, Z.ai)

[Zhipu GLM Coding Plan](https://docs.bigmodel.cn/en/coding-plan/overview)

- Lite Plan (49 RMB/month): Maximum ~80 prompts per 5 hours, maximum ~400 prompts per week
- Pro Plan (149 RMB/month): Maximum ~400 prompts per 5 hours, maximum ~2000 prompts per week
- Max Plan (469 RMB/month): Maximum ~1600 prompts per 5 hours, maximum ~8000 prompts per week
- One prompt refers to one query. Each prompt is estimated to invoke the model 15–20 times. The monthly available quota is converted based on API pricing, equivalent to approximately 15–30× the monthly subscription fee (weekly caps already factored in).
- Note: The above figures are estimates. Actual available usage may vary depending on project complexity, repository size, and whether auto-accept is enabled.
- Note: GLM-5 has a larger parameter size and is benchmarked against the Claude Opus model. Its usage will be deducted at 3 × during peak hours and 2 × during off-peak hours. We recommend switching to GLM-5 for complex tasks and continuing to use GLM-4.7 for routine tasks to avoid rapid quota consumption. Peak hours are 14:00–18:00 (UTC+8).
- Note: For users who subscribed and enabled auto-renewal before February 12 (UTC+8), the original quota will remain in effect throughout the subscription validity period, and no weekly usage limits will apply.
- Note: For users who enabled auto-renewal before February 12, both the renewal price and the usage quota will remain unchanged and will continue to follow the limits shown at the time of your original subscription.
- [GLM-5 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 1/1.5 RMB per 1M tokens
    - Uncached input: 4/6 RMB per 1M tokens
    - Output: 18/22 RMB per 1M tokens
    - 200K context
- [GLM-4.7 API Pricing](https://bigmodel.cn/pricing):
    - Cached input: 0.4/0.6/0.8 RMB per 1M tokens
    - Uncached input: 2/3/4 RMB per 1M tokens
    - Output: 8/14/16 RMB per 1M tokens
    - 200K context

[Zhipu International GLM Coding Plan](https://z.ai/subscribe)

### Others

- [Volcano Engine Coding Plan](https://www.volcengine.com/activity/codingplan)
    - Lite Plan (40 RMB/month): Per 5 hours: maximum ~1,200 requests. Per week: maximum ~9,000 requests. Per subscription month: maximum ~18,000 requests.
    - Pro Plan (200 RMB/month): 5x the Lite Plan quota
- [Alibaba Bailian Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
    - Lite (40 RMB/month): Fixed monthly fee, 18,000 requests per month, 9,000 per week, 1,200 per 5 hours
    - Pro (200 RMB/month): Fixed monthly fee, 90,000 requests per month, 45,000 per week, 6,000 per 5 hours
    - One user question may trigger multiple model calls; each model call counts as one quota consumption. Typical quota consumption scenarios:
    - Simple Q&A or code generation: usually triggers 5-10 model calls
    - Code refactoring or complex tasks: may trigger 10-30 or more model calls
    - Actual quota consumption depends on task complexity, context size, number of tool calls, and other factors. Specific consumption is based on actual usage; you can view plan quota consumption in the Coding Plan console.
    - [Qwen3.5-Plus API Pricing](https://help.aliyun.com/zh/model-studio/models)：
        - Input: 0.8/2/4 RMB per 1M tokens
        - Output: 4.8/12/24 RMB per 1M tokens
        - 1M context
    - [Qwen3-Max API Pricing](https://help.aliyun.com/zh/model-studio/models)：
        - Input: 2.5/4/7 RMB per 1M tokens
        - Output: 10/16/28 RMB per 1M tokens
        - 256K context
- [Infini-AI Coding Plan](https://docs.infini-ai.com/gen-studio/coding-plan/)
    - Lite (40 RMB/month): Fixed monthly fee, 12,000 requests per month, 6,000 per week, 1,000 per 5 hours
    - Pro (200 RMB/month): Fixed monthly fee, 60,000 requests per month, 30,000 per week, 5,000 per 5 hours

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
| [Kimi-K2.5](https://huggingface.co/moonshotai/Kimi-K2.5)           | 1T         | 32B    | Y      |
| [GLM-5](https://huggingface.co/zai-org/GLM-5)                      | 744B       | 40B    | N      |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                  | 355B       | 32B    | N      |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)      | 30B        | 3B     | N      |
| [MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5)      | 230B       | 10B    | N      |
| [DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2)  | 671B       | 37B    | N      |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | 397B       | 17B    | Y      |

## Update History

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
    - Serious comment: The new GLM Coding Plan's cost-effectiveness dropped from “夯”(S-level) to “NPC”(C-level), making Kimi/MiniMax's value stand out. The solution is to continue renewing the old plan and stick with GLM-4.7.
    - If calculated using the new plan at 2/3 of the old quota limit, using GLM-4.7, the Lite plan can use `40M*2/3*4*30/7=457M` tokens per month (30 days); using GLM-5, it would be `40M*2/3*4*30/7/3=152M` tokens.
- 2026/02/12: GLM Coding Plan prices changed from 40/200/400 RMB/month to 49/149/469 RMB/month; meanwhile, usage quotas were reduced to 2/3 of the original:
    - Lite Plan: Maximum ~80 prompts per 5 hours (was 120), equivalent to 3x Claude Pro plan usage
    - Pro Plan: Maximum ~400 prompts per 5 hours (was 600), equivalent to 5x Lite plan usage
    - Max Plan: Maximum ~1600 prompts per 5 hours (was 2400), equivalent to 4x Pro plan usage
    - If using the 2/3 ratio, the Lite plan limit would be `40/3*2=27M` tokens per 5 hours. The new version also has weekly limits (specific rules published on 2026/02/14, see above). After switching to the new plan (I am not planning to), need to test what the new usage limits correspond to in tokens (interested readers can test and provide feedback).
- 2026/02/12: Added description for Kimi Allegro plan
- 2026/02/12: With the release of GLM-5, GLM Coding Plan's quota/limit API no longer returns specific token counts—presumably preparing for GLM-5 and GLM-4.7 to consume usage at different rates (based on API pricing, guessing there might be a 2x coefficient? Awaiting further testing). However, current testing shows GLM-4.7 usage limits remain unchanged; Lite plan is still 40M input + output tokens per 5 hours. Since there's only a per-5-hour limit, calculated at 30 days per month, theoretically maximum monthly usage could be `30*24/5*40=5760M` tokens.
- 2026/01/30: Through actual testing, speculated that GLM Coding Plan's Lite plan usage limit is that the sum of all requests' input + output tokens does not exceed 40M per 5 hours (meaning each prompt corresponds to 40M/120=333K tokens), which is consistent with the results returned by the `https://open.bigmodel.cn/api/monitor/usage/quota/limit` API (after 2026/02/12, this API only returns percentages, not token counts).
