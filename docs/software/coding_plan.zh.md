# AI Coding Plan

## Coding Plan

### Kimi

[Kimi 登月计划](https://www.kimi.com/membership/pricing) [Kimi Code](https://www.kimi.com/code)

- Andante（49 RMB 每月）
- Moderato（99 RMB 每月）
- Allegretto（199 RMB 每月）
- Allegro（699 RMB 每月）
- 订阅续购规则调整：因算力资源紧张，将优先保障订阅中用户的使用体验，你可于 2026-08-20 00:00 前续订，逾期将无法直接购买
- [K3 API 价格](https://platform.kimi.com/docs/pricing/chat-k3)：
    - 输入命中缓存 2 RMB 每 1M tokens
    - 输入未命中缓存 20 RMB 每 1M tokens
    - 输出 100 RMB 每 1M tokens
    - 1M 上下文
- [K2.7-Code API 价格](https://platform.kimi.com/docs/pricing/chat-k27-code)：
    - 输入命中缓存 1.3 RMB 每 1M tokens
    - 输入未命中缓存 6.5 RMB 每 1M tokens
    - 输出 27 RMB 每 1M tokens
    - 256K 上下文
- [K2.7-Code-HighSpeed API 价格](https://platform.kimi.com/docs/pricing/chat-k27-code)：
    - 输入命中缓存 2.6 RMB 每 1M tokens
    - 输入未命中缓存 13.0 RMB 每 1M tokens
    - 输出 54 RMB 每 1M tokens
    - 256K 上下文

### MiniMax

[MiniMax Token Plan](https://platform.minimaxi.com/docs/token-plan/intro) [产品定价](https://platform.minimaxi.com/docs/guides/pricing-token-plan) [订阅](https://platform.minimaxi.com/subscribe/token-plan)

- Token Plan 支持范围已从"所有模型"调整为"旗舰模型"，音乐相关 API（Music-3.0、Music-2.6、歌词生成等）已下线，Token Plan 额度不再包含音乐资源
- Plus（49 RMB 每月）: 月度 M3 Token 用量约 6 亿+
- Max（119 RMB 每月）: 月度 M3 Token 用量约 18 亿+
- Ultra（469 RMB 每月）: 月度 M3 Token 用量约 71 亿+
- 预付积分包：¥30 获 4489 积分、¥150 获 22460 积分、¥500 获 74900 积分，有效期 365 天
- [MiniMax M3 API 价格](https://platform.minimaxi.com/docs/guides/pricing-paygo)：
    - `<=` 512K 输入 token：
        - 输入命中缓存 0.42 RMB 每 1M tokens
        - 输入未命中缓存 2.10 RMB 每 1M tokens
        - 输出 8.40 RMB 每 1M tokens
    - `>` 512K 输入 token：
        - 输入命中缓存 0.84 RMB 每 1M tokens
        - 输入未命中缓存 4.20 RMB 每 1M tokens
        - 输出 16.80 RMB 每 1M tokens
    - 1M 上下文

[MiniMax 国际版 Token Plan](https://platform.minimax.io/docs/token-plan/intro) [产品定价](https://platform.minimax.io/docs/guides/pricing-token-plan)

- Plus（$22 每月）: 个人项目与原型开发
- Max（$55 每月）: 日常编程 Agent 与多模态调用
- Ultra（$132 每月）: 重度 Agent 工作流与长时使用

### 智谱

[智谱 GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite 套餐（118 RMB 每月）：每 5 小时 2000 积分，每周 10000 积分
- Pro 套餐（538 RMB 每月）：每 5 小时 12000 积分，每周 60000 积分
- Max 套餐（1078 RMB 每月）：每 5 小时 28000 积分，每周 140000 积分
- 模型消耗积分数=（输入 Token × Input 抵扣系数 + 缓存命中 Token × Cached Input 抵扣系数 + 输出 Token × Output 抵扣系数）/ 10000
- MCP 消耗积分数=调用次数 × Output 抵扣系数
- 所有套餐均支持 **GLM-5.3**、**GLM-5.3-Flash**。
- 调用历史模型 GLM-5.2、GLM-5.1 都将自动切换至 GLM-5.3，调用 GLM-5-Turbo、GLM-4.7 将自动切换至 GLM-5.3-Flash。
- 非高峰时段内，模型调用按基础积分消耗的 50% 抵扣。高峰时段：每周一至周五的 14:00～18:00（UTC+8）。
- GLM-5.3：Input 抵扣系数 6.9，Cached Input 抵扣系数 1.7，Output 抵扣系数 24
- GLM-5.3-Flash（含视觉理解 MCP）：Input 抵扣系数 2.3，Cached Input 抵扣系数 0.56，Output 抵扣系数 8
- 套餐的 Token 用量会因缓存命中率而有所不同，具体如下：

| 缓存命中率 | 模型          | Lite（亿 Tokens/周） | Pro（亿 Tokens/周） | Max（亿 Tokens/周） |
|------------|---------------|--------------------|-------------------|-------------------|
| 95%        | GLM-5.3       | 0.48～0.97          | 2.90～5.80         | 6.76～13.52        |
| 95%        | GLM-5.3-Flash | 1.46～2.92          | 8.77～17.55        | 20.47～40.95       |
| 96%        | GLM-5.3       | 0.50～0.99          | 2.97～5.95         | 6.94～13.87        |
| 96%        | GLM-5.3-Flash | 1.50～3.00          | 9.00～18.01        | 21.01～42.02       |
| 98%        | GLM-5.3       | 0.52～1.04          | 3.13～6.27         | 7.31～14.63        |
| 98%        | GLM-5.3-Flash | 1.58～3.17          | 9.50～19.00        | 22.17～44.33       |


- 区间说明
    - 最多 Tokens：全部在非高峰时段，按 0.5 倍积分消耗
    - 最少 Tokens：全部在高峰时段，按 1 倍积分消耗
- 当充分利用非高峰时段优惠时，相较于按量调用 GLM-5.3 标准 API，最高可节省 92% 成本
- [GLM-5.3 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 2 RMB 每 1M tokens
    - 输入未命中缓存 8 RMB 每 1M tokens
    - 输出 28 RMB 每 1M tokens
    - 1M 上下文
- [GLM-5.3-Flash API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 0.115/0.23 RMB 每 1M tokens
    - 输入未命中缓存 0.4/0.8 RMB 每 1M tokens
    - 输出 1.4/2.8 RMB 每 1M tokens
    - 1M 上下文（5 折限时两周）
- [GLM-5.2 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 2 RMB 每 1M tokens
    - 输入未命中缓存 8 RMB 每 1M tokens
    - 输出 28 RMB 每 1M tokens
    - 1M 上下文
- [GLM-5.1 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 1.3/2 RMB 每 1M tokens
    - 输入未命中缓存 6/8 RMB 每 1M tokens
    - 输出 24/28 RMB 每 1M tokens
    - 200K 上下文
- [GLM-5-Turbo API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 1.2/1.8 RMB 每 1M tokens
    - 输入未命中缓存 5/7 RMB 每 1M tokens
    - 输出 22/26 RMB 每 1M tokens
    - 200K 上下文
- [GLM-4.7 API 价格](https://bigmodel.cn/pricing)：
    - 输入命中缓存 0.4/0.6/0.8 RMB 每 1M tokens
    - 输入未命中缓存 2/3/4 RMB 每 1M tokens
    - 输出 8/14/16 RMB 每 1M tokens
    - 200K 上下文

[智谱 GLM Coding Plan 团队版](https://docs.bigmodel.cn/cn/coding-plan/team)

- 团队标准版（598 RMB 每月）：每 5 小时最多 0.6 亿 tokens 每席位，每周最多 3 亿 tokens 每席位
- 团队高级版（1198 RMB 每月）：每 5 小时最多 1.6 亿 tokens 每席位，每周最多 8 亿 tokens 每席位
- “最多”指在 1 倍消耗系数 下，可实际消耗的 Tokens 总量。当前各模型的额度消耗规则如下：
    - GLM-4.7、GLM-4.5-Air：全天按 1 倍系数 消耗额度
    - GLM-5.2、GLM-5-Turbo：作为高阶模型，调用时按“高峰期 3 倍，非高峰期 2 倍”系数消耗额度。作为限时福利，截至至 6 月底，GLM-5.2 与 GLM-5-Turbo 在非高峰期将仅按 1 倍系数抵扣额度。
    - 注：高峰期时间为每日 14:00～18:00（UTC+8）。

[智谱国际版 GLM Coding Plan](https://z.ai/subscribe)：所有套餐均支持 GLM-5.3、GLM-5.3-Flash；调用 GLM-5.2/GLM-5.1 自动路由至 GLM-5.3，GLM-4.7 自动路由至 GLM-5.3-Flash

### 云厂商

- [方舟 Coding Plan 个人版](https://www.volcengine.com/activity/codingplan) [文档](https://www.volcengine.com/docs/82379/1925114)
    - Lite 套餐（40 RMB 每月）：每 5 小时：最多约 1,200 次请求。每周：最多约 9,000 次请求。每订阅月：最多约 18,000 次请求。
    - Pro 套餐（200 RMB 每月）：Lite 套餐的 5 倍用量
    - 支持模型：Doubao-Seed-2.1-turbo、Doubao-Seed-Evolving、Doubao-Seed-2.0-lite、MiniMax-M3、Kimi-K2.7-Code、GLM-5.3、GLM-5.3-Flash、DeepSeek-V4-Flash、DeepSeek-V4-Pro
    - GLM-5.3-Flash 为新增模型：智谱首个原生多模态模型，320B 总参数/18B 激活，支持图片输入，1M 上下文/128K 最大输出；首两周抵扣系数 5 折优惠，活动截止 2026-09-11 23:59:59
    - DeepSeek-V4-Pro 已转正式版上线（原为尝鲜体验版），Agent 能力全面跃升，支持通过 model name 及控制台选择访问
- [方舟 Agent Plan 个人版](https://www.volcengine.com/docs/82379/2366394)
    - Agent 燃料值（Agent Fuel Point，简称 AFP）是 Agent Plan 套餐的统一用量计费单位，用于量化智能体（Agent）资源的消耗。
        - 文本生成模型、向量化模型：(输入 token * 输入抵扣系数 + 输出 token * 输出抵扣系数) / 10,000
        - 视频生成模型：消耗的 token / 10,000 * 抵扣系数
        - 图片生成模型：成功生成的图片张数 * 抵扣系数
        - 文本生成/向量化模型的输入抵扣系数与输出抵扣系数由模型统一决定、不随输入长度变化（此前输入抵扣系数 = 模型抵扣系数 × 输入分段系数：≤32k ×0.67、32k–128k ×1、>128k ×2，现已去掉长度分段）
        - 各模型抵扣系数（输入/输出相同）：
            - doubao-seed-2.0-mini：0.25
            - doubao-seed-2.0-lite、deepseek-v4-flash：0.5
            - glm-5.3-flash：0.5（0.25 限时5折）
            - doubao-seed-2.1-turbo、doubao-seed-evolving、minimax-m3：2.5
            - kimi-k2.7-code：4.5
            - glm-5.3（glm-latest）：4.5
            - deepseek-v4-pro：5.5
            - kimi-k3：10
            - doubao-embedding-vision：0.5
    - Small 套餐（40 RMB 每月）：每 5 小时：2000 AFP。每周：7000 AFP。每月：20000 AFP。日额度：10000 AFP。
    - Medium 套餐（200 RMB 每月）：每 5 小时：10000 AFP。每周：35000 AFP。每月：100000 AFP。日额度：50000 AFP。
    - Large 套餐（500 RMB 每月）：每 5 小时：25000 AFP。每周：87500 AFP。每月：250000 AFP。日额度：125000 AFP。
    - Max 套餐（1000 RMB 每月）：每 5 小时：50000 AFP。每周：175000 AFP。每月：500000 AFP。日额度：250000 AFP。
    - 图片生成模型、视频生成模型、语音模型、Harness 没有5小时、周额度限制，仅受日额度和套餐月额度限制。日额度限制统一都是套餐月额度的一半。
    - 全套餐支持模型：doubao-seed-2.0-mini、doubao-seed-2.0-lite、deepseek-v4-flash、deepseek-v3.2、minimax-m3、glm-5.3、glm-5.3-flash、kimi-k2.7-code、deepseek-v4-pro、doubao-embedding-vision、doubao-seedream-5.0-lite、doubao-seed-tts-2.0、doubao-seed-asr-2.0
    - Agent 进化：前 50 个文件免费（此前为限制/收费项）
    - Medium 以上套餐额外支持模型：doubao-seedance-1.5-pro、doubao-seedance-2.0、doubao-seedance-2.0-fast、doubao-seedance-2.0-mini
- [阿里云百炼 Token Plan（个人版）](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
    - Lite 套餐（60 RMB 每月）：2500 Credits 每 7 天
    - Standard 套餐（180 RMB 每月）：10000 Credits 每 7 天
    - Pro 套餐（600 RMB 每月）：40000 Credits 每 7 天
    - 用量包（100 RMB 每月）：20000 Credits
    - 支持模型：qwen3.8-max、qwen3.8-flash、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、qwen-image-3.0-pro、qwen-audio-3.0-tts-plus、qewn-audio-3.0-realtime-plus、qwen-audio-3.0-asr-flash、wan2.7-image、wan2.7-image-pro、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731、glm-5.2、happyhorse-1.1-i2v、happyhorse-1.1-t2v、happyhorse-1.1-r2v
- [阿里云百炼 Token Plan（团队版）](https://help.aliyun.com/zh/model-studio/token-plan-overview)
    - 标准坐席（¥198/坐席/月）：25,000 Credits/坐席/月
    - 高级坐席（¥698/坐席/月）：100,000 Credits/坐席/月
    - 尊享坐席（¥1,398/坐席/月）：250,000 Credits/坐席/月
    - 共享用量包（¥5,000/个）：625,000 Credits/个
    - 单次消耗的 Credits 由模型类型、Token 用量、思考模式及工具调用等动态决定，实际消耗以账单为准。
    - 以 Qwen3.6-plus 为例，每 5000 输入未命中缓存 token、每 50000 输入命中缓存 token、每 5000/6 输出 token 为一个 Credit
    - 如果按 256K 以内的上下文算，一个 Credit 对应的 API 价格（隐式缓存）是 0.01-0.02 元，按 256K-1M 的上下文，一个 Credit 对应 0.04-0.08 元
    - 支持模型：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro、qwen-image-3.0-pro、qwen-audio-3.0-tts-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-asr-flash、wan2.7-image、wan2.7-image-pro、deepseek-v4-pro、deepseekv4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、kimi-k2.7-code、kimi-k2.6、kimi-k2.5、glm-5.2、glm-5.1、glm-5、minimax-m2.5、happyhorse-1.1-i2v、happyhorse-1.1-t2v、happyhorse-1.1-r2v
- [腾讯云大模型 Token Plan](https://cloud.tencent.com/act/pro/tokenplan)
    - Token Plan 企业版：
        - 专业套餐：每月 1 元/100 积分，单次购买最低 5 万积分（500 元/月）；可用模型库（广州/新加坡地域略有差异）：Auto、GLM-5.3、GLM-5.2、GLM-5、GLM-5.1、GLM-5-Turbo、Kimi K2.7 Code、Kimi K2.7 Code HighSpeed、Kimi-K2.6、MiniMax-M2.7、MiniMax-M3、DeepSeek-V4-Flash、DeepSeek-V4-Pro、DeepSeek-V4-Flash 0731 正式版、DeepSeek-V4-Pro 0813 正式版、DeepSeek-V4-Flash 正式版 原厂直供、DeepSeek-V4-Pro 正式版 原厂直供、DeepSeek-V4-Flash-Vision-Exp 原厂直供（纯文本能力与 V4-Flash 正式版持平，并大幅补强视觉理解，多模态 Agent 表现接近 Claude Opus-4.8；Kimi-K2.5 已于 2026-08-31 下线）
        - 峰谷计费（2026-08-29 起调整）：DeepSeek V4【原厂直供】工作日（周一至周五）继续峰谷计费（高峰时段 9:00–12:00、14:00–18:00），周末（周六、周日）全天按空闲时段价格计费；DeepSeek V4 正式版高峰时段为周一至周日 9:00–12:00、14:00–18:00；单次请求计费时段以平台服务端接收请求时间（北京时间）为准
        - 轻享套餐：每月 2 元/百万 tokens
    - Token Plan 个人版（自 2026-08-31 17:00 起改为积分抵扣模式）：
        - Hy Token Plan:
            - Lite 套餐（28 RMB 每月）：每订阅月 560 积分
            - Standard 套餐（78 RMB 每月）：每订阅月 1560 积分
            - Pro 套餐（238 RMB 每月）：每订阅月 4760 积分（238 元 × 20 = 4760，与其余档位一致；此前页面误标为 1560 积分，现已更正）
            - Max 套餐（468 RMB 每月）：每订阅月 9360 积分
            - 支持模型（暂不支持图片、视频等多模态能力）：Hy3、Hy4 preview（Hy3 preview 调用自动路由至 Hy3 模型）
        - 通用 Token Plan:
            - Lite 套餐（39 RMB 每月）：每订阅月 780 积分
            - Standard 套餐（99 RMB 每月）：每订阅月 1980 积分
            - Pro 套餐（299 RMB 每月）：每订阅月 5980 积分
            - Max 套餐（599 RMB 每月）：每订阅月 11980 积分
            - 支持模型：Auto、DeepSeek-V4-Flash 正式版 原厂直供、DeepSeek-V4-Pro 正式版 原厂直供、MiniMax-M2.7、MiniMax-M3、GLM-5、GLM-5.1、GLM-5.2、GLM-5.3、Kimi K2.7 Code、Hy4 preview（Kimi-K2.5 已下线）
            - DeepSeek-V4-Flash/DeepSeek-V4-Pro 正式版原厂直供 model 别名 deepseek/deepseek-v4-flash-0731、deepseek/deepseek-v4-flash、deepseek/deepseek-v4-pro-0813、deepseek/deepseek-v4-pro
            - Token Plan 企业版专业套餐已移除 MiniMax-M2.5 模型（2026年8月7日下线）
- [百度千帆 Token Plan 个人版](https://cloud.baidu.com/product/codingplan.html) [个人版文档](https://cloud.baidu.com/doc/qianfan/s/Dmrabu8b6) [企业版文档](https://cloud.baidu.com/doc/qianfan/s/ymq8wwch2)
    - Mini 套餐（9.9 RMB 每月）：1000 万 token 每月
    - Lite 套餐（40 RMB 每月）：4200 万 token 每月
    - Pro 套餐（200 RMB 每月）：2.3 亿 token 每月
    - Max 套餐（600 RMB 每月）：7 亿 token 每月
    - 支持模型：DeepSeek-V4-Pro、DeepSeek-V4-Flash、GLM-5.2、GLM-5.1、Kimi-K2.6、ERNIE 5.1
- [京东云 Coding Plan](https://docs.jdcloud.com/cn/jdaip/PackageOverview)
    - Lite 套餐（首购 19.9 RMB 每月，续费 40 RMB 每月）：每 5 小时：最多 1,200 次请求，每周：最多 9,000 次请求，每订阅月：最多 18,000 次请求
    - Pro 套餐（首购 99.9 RMB 每月，续费 200 RMB 每月）：每 5 小时：最多 6,000 次请求，每周：最多 45,000 次请求，每订阅月：最多 90,000 次请求
    - 支持模型：DeepSeek-V3.2、GLM-5、GLM-4.7、MiniMax-M2.5、Kimi-K2.5、Kimi-K2-Turbo、Qwen3-Coder
- [讯飞星辰 Astron Token Plan 团队版](https://www.xfyun.cn/doc/spark/TokenPlan.html) [订阅](https://maas.xfyun.cn/tokenPlan/subscription)
    - 标准成员（200 RMB/席/月）：20000 Credits，200 万 TPM
    - 高级成员（600 RMB/席/月）：60000 Credits，300 万 TPM
    - 尊享成员（1200 RMB/席/月）：200000 Credits，500 万 TPM
    - 支持模型：Spark-X2、Spark-X2-Flash、GLM-5.2、GLM-5.1、GLM-5、DeepSeek-V4-Pro、DeepSeek-V4-Flash、DeepSeek-V3.2、Kimi-K2.6、Kimi-K2.5、MiniMax-M2.5、Qwen3.5-397B-A17B、Qwen3.6-35B-A3B、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、GLM-4.7-Flash
- [讯飞星辰 Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html) [订阅](https://maas.xfyun.cn/packageSubscription)
    - 专业版（39 RMB 每月）：每 5 小时：最多约 1,200 次请求；每周：最多约 9,000 次请求；每订阅月：最多约 18,000 次请求，支持 Spark-X2-Agent、Spark-X2、Auto、GLM-5.1、GLM-5、MiniMax-M2.5、Kimi-K2.6、Kimi-K2.5、DeepSeek-V3.2、Spark-X2-Flash、Qwen3.6-35B-A3B、GLM-4.7-Flash、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、Qwen3.5-397B-A17B 模型
    - 高效版（199 RMB 每月）：每 5 小时：最多约 6,000 次请求；每周：最多约 45,000 次请求；每订阅月：最多约 90,000 次请求，支持 Spark-X2-Agent、Spark-X2、Auto、GLM-5、GLM-5.2、DeepSeek-V4-Pro、DeepSeek-V4-Flash、MiniMax-M2.5、Kimi-K2.6、Kimi-K2.5、DeepSeek-V3.2、Spark-X2-Flash、Qwen3.6-35B-A3B、GLM-4.7-Flash、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、Qwen3.5-397B-A17B 模型
- [天翼云编程 Token Plan](https://www.ctyun.cn/document/11061839/11092368)
    - 29 RMB 每月：2500 万 tokens
    - 89 RMB 每月：8000 万 tokens
    - 199 RMB 每月：18000 万 tokens
    - 399 RMB 每月：38000 万 tokens
    - 699 RMB 每月：68000 万 tokens
    - 支持模型：GLM-5.0（正式版）、DeepSeek-V3.2（旗舰版）、GLM-5.1、DeepSeek-V4-Flash-0731
- [华为云 MaaS Token Plan](https://support.huaweicloud.com/Token-plan-maas/tokenplan-maas-0001.html)
    - Lite（59 RMB 每月）：每订阅月 5000 万 tokens
    - Standard（149 RMB 每月）：每订阅月 1.3 亿 tokens
    - Pro（399 RMB 每月）：每订阅月 3.8 亿 tokens
    - Max（799 RMB 每月）：每订阅月 8.8 亿 tokens
    - 支持模型：GLM-5、GLM-5.1、Kimi-K2.6、DeepSeek-V3.2、DeepSeek-V4-Flash

### 其他

- [阶越星辰 Step Plan](https://platform.stepfun.com/docs/zh/step-plan/overview)
    - Flash Mini（49 RMB 每月）：400M Credit
    - Flash Plus（99 RMB 每月）：1600M Credit
    - Flash Pro（199 RMB 每月）：8000M Credit
    - Flash Max（699 RMB 每月）：40000M Credit
    - 支持模型：step-3.7-flash、step-3.5-flash-2603、step-3.5-flash、stepaudio-2.5-realtime、stepaudio-2.5-chat、stepaudio-2.5-tts、stepaudio-2.5-asr、step-router-v1（在 deepseek-v4-pro 和 step-3.5-flash 之间智能路由）、step-image-edit-2
- [小米 MiMo Token Plan](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription)
    - Lite（39 RMB 或 6 USD 每月）：41 亿 Credits 每月
    - Standard（99 RMB 或 16 USD 每月）：110 亿 Credits 每月
    - Pro（329 RMB 或 50 USD 每月）：380 亿 Credits 每月
    - Max（659 RMB 或 100 USD 每月）：820 亿 Credits 每月
    - 支持模型：各套餐均支持 MiMo-V2.5-Pro、MiMo-V2.5、MiMo-V2.5-ASR、MiMo-V2.5-TTS-VoiceClone、MiMo-V2.5-TTS-VoiceDesign、MiMo-V2.5-TTS、MiMo-V2-Pro、MiMo-V2-Omni、MiMo-V2-TTS 共 9 款模型。
    - 额度消耗：按 Token 数扣除 Credit 额度，套餐中的可用模型按不同比例并行消耗，不是独立消耗，TTS 系列模型限时免费，不消耗套餐 Token。
- [OpenCode Go](https://opencode.ai/docs/zh-cn/go)（面向国际用户的低成本开源编程模型订阅服务）
    - 每月 10 美元
    - 使用限制：5 小时 $12、每周 $30、每月 $60
    - 支持模型：Grok 4.6、GLM-5.3/5.3-Flash/5.2/5.1、GPT 5.6 Luna、Kimi K3/K2.7 Code/K2.6、LongCat-2.0、MiMo-V2.5/V2.5-Pro、MiniMax M3/M2.7/M2.5、**Muse Spark 1.2 Contributor**、Qwen3.8 Max/Qwen3.8 Flash/Qwen3.7 Max/Qwen3.7 Plus/Qwen3.6 Plus、DeepSeek V4 Pro/V4 Flash/V4 Flash Vision Exp、Hy4 preview、Hy3
    - Hy4 preview 为新增模型：input $0.834/1M、output $2.501/1M、cache read $0.042/1M（使用额度 $30）；请求限额 1,350/5 小时、3,380/周、6,770/月；model ID hy4-preview
    - Muse Spark 1.2 Contributor 为新增模型：允许 Meta 使用提示词和补全结果训练未来模型以换取大幅折扣 token 价格（input $0.10/1M、output $0.20/1M、cache read $0.002/1M）。仅在 Meta 的[地理使用政策](https://ai.developer.meta.com/legal/geographic-use-policy)允许的地区提供
    - Qwen3.8 Flash 为新增模型：input $0.15/1M、output $0.47/1M、cache read $0.016/1M、cache write $0.20/1M（使用额度 $30）；请求限额 5,400/5 小时、13,500/周、27,000/月；model ID qwen3.8-flash
    - Qwen3.7 Max：请求限额 170/5 小时、420/周、840/月，使用额度 $30/月；定价 input $2.50/1M、output $7.50/1M、cache read $0.50/1M、cache write $3.125/1M（2026-09-01 起请求限额由 340/840/1,690 减半、月度使用额度由 $60 降为 $30）
- [阶越星辰国际版 Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)
- [联通元景 GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)
- [摩尔线程 AI Coding Plan](https://code.mthreads.com/)
- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)
- [DeepSeek API 定价](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)：
    - 自 2026-08-17 00:00 起采用峰谷定价，空闲时段价格为高峰时段的一半，较此前价格整体大幅上调
    - 高峰时段：北京时间周一至周五 9:00-12:00、14:00-18:00（其余为空闲时段）
    - deepseek-v4-flash（DeepSeek-V4-Flash-0731，1M 上下文）：
        - 空闲时段：输入命中缓存 0.05 RMB / 输入未命中缓存 1.5 RMB / 输出 4.5 RMB 每 1M tokens
        - 高峰时段：输入命中缓存 0.10 RMB / 输入未命中缓存 3.0 RMB / 输出 9.0 RMB 每 1M tokens
    - deepseek-v4-pro（DeepSeek-V4-Pro-0813，1M 上下文）：
        - 空闲时段：输入命中缓存 0.15 RMB / 输入未命中缓存 4.5 RMB / 输出 13.5 RMB 每 1M tokens
        - 高峰时段：输入命中缓存 0.30 RMB / 输入未命中缓存 9.0 RMB / 输出 27.0 RMB 每 1M tokens
    - deepseek-v4-flash-vision-exp（DeepSeek-V4-Flash-Vision-Exp，视觉模型实验版）：
        - 价格与 deepseek-v4-flash 一致（空闲时段 / 高峰时段）
        - 不支持 FIM 补全，并发限制 2500
        - 图片按尺寸换算成 token 与文本 token 一并计费

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

| 模型名称                                                                            | 参数量 | 激活量 | 视觉 |
|-------------------------------------------------------------------------------------|--------|--------|------|
| [DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | 284B   | 13B    | 否   |
| [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)           | 284B   | 13B    | 否   |
| [DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)     | 1.6T   | 49B    | 否   |
| [DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)               | 1.6T   | 49B    | 否   |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)                       | 30B    | 3B     | 否   |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                                   | 355B   | 32B    | 否   |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                                   | 744B   | 40B    | 否   |
| [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)                                   | 744B   | 40B    | 否   |
| [GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash)                       | 320B   | 18B    | 是   |
| [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3)                                   | 744B   | 40B    | 否   |
| [Hy3-preview](https://huggingface.co/tencent/Hy3-preview)                           | 295B   | 21B    | 否   |
| [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)                                | 2.8T   | 104B   | 是   |
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)                            | 1T     | 32B    | 是   |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)                           | 428B   | 23B    | 是   |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)                       | 230B   | 10B    | 否   |
| [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)                  | 2.4T   | 95B    | 是   |
| [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)                              | 27B    | -      | 是   |
| [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)                | 180B   | 6B     | 是   |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)                  | 397B   | 17B    | 是   |

## 更新历史

- 2026/09/02：腾讯云大模型 Token Plan 个人版 Hy Token Plan 进阶套餐（Pro）每订阅月积分由 1560 更正为 4760 积分（238 元/月价格不变；1560 为官方页面误标笔误，与 238 元 × 20 的档位规律不符）
- 2026/09/01：火山方舟 Agent Plan 个人版抵扣系数规则调整：文本生成/向量化模型的输入抵扣系数与输出抵扣系数改为由模型统一决定、不再随输入长度变化（此前输入抵扣系数 = 模型抵扣系数 × 输入分段系数：≤32k ×0.67、32k–128k ×1、>128k ×2，现已去掉长度分段）。各模型输入/输出抵扣系数：doubao-seed-2.0-mini 0.25、doubao-seed-2.0-lite/deepseek-v4-flash 0.5、glm-5.3-flash 0.5（0.25 限时5折）、doubao-seed-2.1-turbo/doubao-seed-evolving/minimax-m3 2.5、kimi-k2.7-code 4.5、glm-5.3（glm-latest）4.5、deepseek-v4-pro 5.5、kimi-k3 10、doubao-embedding-vision 0.5
- 2026/09/01：OpenCode Go Qwen3.7 Max 模型额度下调：请求限额由 340/5 小时、840/周、1,690/月 降至 170/5 小时、420/周、840/月，月度使用额度由 $60 降至 $30（定价 input $2.50/1M、output $7.50/1M、cache read $0.50/1M、cache write $3.125/1M 不变）
- 2026/08/31：腾讯云大模型 Token Plan 调整为积分抵扣模式：个人版自 2026-08-31 17:00 起由 Token 定额改为积分（通用 Token Plan Lite/Standard/Pro/Max = 39/99/299/599 元每月，780/1980/5980/11980 积分/月；Hy Token Plan Lite/Standard/Pro/Max = 28/78/238/468 元每月，560/1560/1560（原文如此，疑为官方笔误）/9360 积分/月）；通用 Token Plan 可用模型更新为 Auto、DeepSeek-V4-Flash/Pro 正式版 原厂直供、MiniMax-M2.7、MiniMax-M3、GLM-5/5.1/5.2/5.3、Kimi K2.7 Code、Hy4 preview（Kimi-K2.5 已下线），Hy Token Plan 支持 Hy3、Hy4 preview（Hy3 preview 自动路由至 Hy3）；企业版专业套餐新增 DeepSeek-V4-Flash-Vision-Exp 原厂直供（多模态/视觉理解，纯文本能力与 V4-Flash 正式版持平，多模态 Agent 表现接近 Claude Opus-4.8）、移除 Kimi-K2.5；DeepSeek V4 原厂直供峰谷计费自 2026-08-29 起改为工作日峰谷、周末全天按空闲时段价格，DeepSeek V4 正式版高峰时段为周一至周日 9:00–12:00、14:00–18:00
- 2026/08/31：火山方舟 Coding Plan 个人版与 Agent Plan 个人版移除 GLM-5.2 模型（此前标记为"即将下线"），GLM-5.2 不再列入支持模型与 1M 上下文支持列表；GLM-5.3 的抵扣系数描述由"与 GLM-5.2 一致"改为"较高"
- 2026/08/31：阿里云百炼模型调用价格新增 ZHIPU/GLM-5.3-Flash（仅思考模式，输入 0.8 元、输出 2.8 元每百万 Tokens，支持上下文缓存命中折扣 25%）与 qwen-flash-character（0.25/1.5 元）；qwen3-vl-rerank 价格下调（文本 0.7→0.5 元、图片 1.8→0.5 元）；Token Plan 个人版限时夜间五折新增 deepseek-v4-flash-0731
- 2026/08/29：OpenCode Go 新增 Hy4 preview 模型（input $0.834/1M、output $2.501/1M、cache read $0.042/1M，使用额度 $30；请求限额 1,350/5 小时、3,380/周、6,770/月；model ID hy4-preview）
- 2026/08/29：火山方舟 Coding Plan 个人版与 Agent Plan 个人版新增 glm-5.3-flash 模型（智谱首个原生多模态模型，320B 总参/18B 激活，支持图片输入，1M 上下文/128K 最大输出；首两周抵扣系数 5 折优惠，活动截止 2026-09-11 23:59:59）；Agent Plan 的 Agent 进化改为前 50 个文件免费
- 2026/08/28：智谱国际版（Z.ai DevPack）GLM Coding Plan 模型调整：所有套餐支持模型从 {GLM-5.3, GLM-5-Flash} 变更为 {GLM-5.3, GLM-5.3-Flash}；调用 GLM-5.2/GLM-5.1 自动路由至 GLM-5.3，GLM-4.7 自动路由至 GLM-5.3-Flash（GLM-5-Turbo 不再作为路由目标）；发布日志移除 GLM-5V-Turbo、GLM-5-Turbo 两条模型条目
- 2026/08/28：OpenCode Go 新增支持 Qwen3.8 Flash 模型（input $0.15/1M、output $0.47/1M、cache read $0.016/1M、cache write $0.20/1M，使用额度 $30；请求限额 5,400/5 小时、13,500/周、27,000/月；model ID qwen3.8-flash）
- 2026/08/28：无问芯穹 Infini GenStudio 更新日志：2026-08-28 一批模型下线（deepseek-r1、deepseek-v3 系列、deepseek-v3.2/v3.2-thinking、glm-4.5/4.5-air/4.6/4.7/5/4.5v/4.6v、minimax-m2.1/m2.5、kimi-k2.5），建议迁移至 deepseek-v4-flash/v4-pro、glm-5.2、kimi-k2.6、minimax-m2.7；2026-08-18 上线 DeepSeek V4 系列（deepseek-v4-flash-0731、deepseek-v4-pro-0813）
- 2026/08/27：阿里云百炼 Token Plan 个人版新增模型 qwen3.8-flash
- 2026/08/27：火山方舟 Coding Plan 个人版与 Agent Plan 的 DeepSeek-V4-Pro 从"尝鲜体验版"转为正式版上线（Agent 能力全面跃升，支持通过 model name 及控制台选择访问）
- 2026/08/27：阿里云百炼模型调用价格调整：qwen3.8-flash 中国站输入从 1 元降至 0.8 元、输出从 3 元降至 2.7 元（国际版输入从 1.167 元降至 1.094 元，输出不变）；新增 kimi-k3（仅思考模式，全球 20/100 元、国际 21.875/109.376 元每百万 tokens）；tongyi-xiaomi-analysis-flash/pro 新增支持上下文缓存折扣；新增 kling/kling-v3-turbo 视频生成模型（有声视频 720P 0.8 元/秒、1080P 1.0 元/秒）
- 2026/08/27：阿里云百炼上下文缓存规则调整：隐式缓存最少 Token 数从 256 提升至 1024（与显式缓存一致，但含义不同——达到 1024 仅代表具备命中条件，不保证实际命中）；qwen3.8-flash 加入 cached_token 折扣例外（不再按输入价 20% 计费）；新增 tongyi-xiaomi-analysis-pro/flash 行业模型；新增 DeepSeek（快手万擎部署）缓存定价（vanchin/deepseek-v4-pro 8.33%、vanchin/deepseek-v3.2-think 10% 等）
- 2026/08/27：腾讯云 Token Plan 个人版通用套餐 Kimi-K2.5 下线日期从 2026-07-31 调整为 2026-08-31（并移除高峰限频提示）
- 2026/08/26：智谱新增 GLM-5.3-Flash API 定价（bigmodel.cn），输入命中缓存 0.115/0.23 元、输入未命中缓存 0.4/0.8 元、输出 1.4/2.8 元每百万 tokens，1M 上下文，当前为 5 折限时两周
- 2026/08/26：智谱 GLM Coding Plan 可用模型从 {GLM-5.3, GLM-5-Turbo, GLM-4.7} 变为 {GLM-5.3, GLM-5.3-Flash}；GLM-5.3-Flash（320B 总参/18B 激活，混合线性+稀疏注意力，原生视觉）上线 Coding Plan，抵扣系数 Input 2.3 / Cached Input 0.56 / Output 8（含视觉理解 MCP）；GLM-5-Turbo/GLM-4.7 调用自动切换至 GLM-5.3-Flash；额度参考表改为按模型分列（95%/96%/98% 缓存命中率）；恢复"最高可节省 92% 成本"表述
- 2026/08/26：OpenCode Go 新增 GLM-5.3-Flash 模型，移除 Ox Alpha Free 模型（限时免费结束）
- 2026/08/26：Qwen3.8-Flash-Next 和 GLM-5.3-Flash 发布
- 2026/08/26：MiniMax Token Plan 价格调整：国际版 Plus/Max/Ultra 套餐从 $20/$50/$120 每月涨至 $22/$55/$132 每月；中文版预付积分包调整——¥30 获 4489 积分（原 4285）、¥150 获 22460 积分（原 21430）、¥500 获 74900 积分（原 71435），中文版订阅套餐价格不变
- 2026/08/26：OpenCode Go Grok 模型从 4.5 升级至 4.6：请求限额提升（169/5hr、423/周、845/月，原 120/300/600），定价改为分档（≤200K tokens: input $2.00、output $6.00、cache $0.50；>200K tokens: input $4.00、output $12.00、cache $1.00，原统一 $2.00/$6.00/$0.30），模型 ID 从 grok-4.5 改为 grok-4.6
- 2026/08/25：腾讯云 Token Plan 企业版专业套餐最低购买额度从 10 万积分降至 5 万积分，新增 DeepSeek-V4-Flash 0731 正式版和 DeepSeek-V4-Pro 0813 正式版（峰谷定价，空闲时段价格与原厂直供版本一致）
- 2026/08/25：OpenCode Go 新增支持 LongCat-2.0 模型（input $0.30/1M、output $1.20/1M、cache read $0.006/1M）
- 2026/08/24：OpenCode Go 取消首月优惠，定价从"首月 5 美元、之后每月 10 美元"调整为统一每月 10 美元
- 2026/08/23：DeepSeek API 峰谷定价周末规则正式生效：高峰时段现明确为北京时间周一至周五 9:00-12:00、14:00-18:00，周末全天按空闲时段价格计费
- 2026/08/22：DeepSeek API 峰谷定价规则调整：自 2026-08-23（周日）00:00 起，周末（周六、周日）全天不再区分峰谷时段，统一按照低谷时段价格收取调用费用（此前周末仍按峰谷时段收费）
- 2026/08/21：方舟 Coding Plan 个人版新增支持 Doubao-Seed-Evolving 模型（面向 Coding 与 Agent 场景，持续周级升级，1M 上下文窗口，256K 最大输出）；OpenCode Go 新增支持 DeepSeek V4 Flash Vision Exp 模型（定价 Off-Peak $0.22/$0.66、Peak $0.44/$1.32 每百万 tokens，图片按尺寸换算为 token 计费）；腾讯云 Token Plan 个人版通用套餐移除已下线模型（Tencent HY 2.0 Instruct、Tencent HY 2.0 Think、Hunyuan-T1、Hunyuan-TurboS、MiniMax-M2.5）
- 2026/08/21：DeepSeek 新增视觉模型 deepseek-v4-flash-vision-exp（实验版），价格与 deepseek-v4-flash 一致，不支持 FIM 补全，并发限制 2500，图片按尺寸换算成 token 计费；腾讯云 Token Plan 企业版专业套餐移除 MiniMax-M2.5 模型；火山方舟 Agent Plan 个人版更新额度规则：图片/视频生成模型、语音模型、Harness 合并为同一日额度类别（不再区分"视觉模型"和"语音模型"），日额度统一为套餐月额度的一半；OpenCode Go 新增 Ox Alpha Free 模型（限时免费）
- 2026/08/19：阿里云百炼新增开源模型 qwen3.8-27b，定价 Input 3 RMB / Output 12 RMB 每百万 tokens（支持上下文缓存折扣），国际版定价 Input 3.646 RMB / Output 21.875 RMB 每百万 tokens；腾讯云 Token Plan 个人版和企业版专业套餐 DeepSeek-V4-Pro 原厂直供更名为 DeepSeek-V4-Pro 正式版 原厂直供，新增模型 ID deepseek/deepseek-v4-pro-0813 和 deepseek/deepseek-v4-pro；MiniMax Token Plan 支持范围从"所有模型"调整为"旗舰模型"，音乐相关 API（Music-3.0、Music-2.6、歌词生成等）已下线，Token Plan 额度不再包含音乐资源
- 2026/08/19：智谱发布 GLM-5.3 模型，编程能力较 GLM-5.2 提升 50%，网络安全能力持平 Mythos 5；GLM Coding Plan 可用额度参考更新为按不同缓存命中率（90.9%、95%、98%）展示；GLM-5.3 API 定价与 GLM-5.2 一致
- 2026/08/18：方舟 Coding Plan 个人版和 Agent Plan 移除了 MiniMax-M2.7 和 Kimi-K2.6 模型（此前标记为即将下线）
- 2026/08/17：方舟 Coding Plan 个人版和 Agent Plan 移除了 Doubao-Seed-2.0-Code、Doubao-Seed-2.0-pro、Doubao-Seed-Code 模型（此前标记为即将下线），GLM-5.2 标记为即将下线，GLM-5.3 替代 GLM-5.2 成为 glm-latest 默认指向
- 2026/08/14：方舟 Coding Plan 个人版和 Agent Plan 新增支持 GLM-5.3 模型（1M 上下文窗口，1024k 上下文 / 128k 最大输出，默认开启思考且不支持关闭，抵扣系数与 GLM-5.2 一致）
- 2026/08/14：智谱 GLM Coding Plan 旗舰模型从 GLM-5.2 升级为 GLM-5.3：所有套餐支持 GLM-5.3、GLM-5-Turbo、GLM-4.7，调用历史模型 GLM-5.2/GLM-5.1 将自动切换至 GLM-5.3，模型抵扣系数不变（Input 6.9 / Cached Input 1.7 / Output 24）；官方文档同时移除了"最高可节省 92% 成本"表述；智谱国际版（Z.ai DevPack）同步升级至 GLM-5.3
- 2026/08/13：DeepSeek API 将于 2026-08-17 00:00 起采用峰谷定价：高峰时段（北京时间 9:00-12:00、14:00-18:00）价格为空闲时段的两倍，整体价格较此前大幅上调（如 deepseek-v4-pro 输出价格从 6 元涨至高峰 27 元/空闲 13.5 元每百万 tokens）
- 2026/07/31：GLM Coding Plan 改为基于积分的限额
- 2026/07/20：Kimi Code 权益从 Kimi 会员套餐中独立，由专属的新版 Kimi Code 套餐订阅提供
- 2026/07/16：Kimi-K3 模型发布
- 2026/07/13：百度千帆 Token Plan 个人版上线
- 2026/06/27：Infini Coding Plan 下线
- 2026/06/13：GLM-5.2 模型发布
- 2026/06/12：Kimi K2.7-Code 模型发布
- 2026/06/10：GLM Coding Plan 团队版上线
- 2026/06/08：方舟 Coding Plan 和 Agent Plan 上线 MiniMax-M3
- 2026/06/08：MiniMax M3 API 价格永久五折
- 2026/06/07：阿里云百炼 Coding Plan 新增模型 qwen3.7-plus
- 2026/06/05：华为云 MaaS Token Plan 上线
- 2026/06/01：MiniMax M3 发布
- 2026/05/29：阶越星辰 Coding Plan 新增支持 step-3.7-flash 模型
- 2026/05/27：小米 MiMo Token Plan 限额巨额上调
- 2026/05/22：百度千帆 Coding Plan 新增支持 DeepSeek-V4-Pro 模型
- 2026/05/22：阿里云 Token Plan 新增支持 qwen3.7-max 模型
- 2026/05/08：百度千帆 Coding Plan 新增支持 DeepSeek-V4-Flash、GLM-5.1 模型
- 2026/05/07：火山方舟 Agent Plan 个人版上线
- 2026/04/30：腾讯云 Token Plan 个人版新增支持 GLM-5.1 和 MiniMax-M2.7 模型
- 2026/04/30：阶越星辰 Coding Plan 删除了 deepseek-v4-pro 模型，必须通过 step-router-v1 模型间接访问
- 2026/04/28：阶越星辰 Coding Plan 新增了 deepseek-v4-pro 和 step-router-v1 模型
- 2026/04/27：GLM Coding Plan 的限额折扣限时福利截止时间从 4 月底延期到 6 月底
- 2026/04/24：阿里云百炼 Token Plan 输入命中缓存 token 对应的 Credit 数减半
- 2026/04/23：MiMo-V2.5 系列模型上线
- 2026/04/23：阶跃星辰 Coding Plan 新增支持 stepaudio-2.5-asr 模型
- 2026/04/23：GLM Coding Plan 将于 2026 年 4 月 30 日统一关闭老套餐（无周限额版本）的自动续订，当前已生效周期不受影响；同时，系统会自动为受影响用户赠送 2 个月同等级新套餐，在当前套餐到期后顺延生效，无需手动领取。详见[《老套餐迁移与补偿说明》](https://docs.bigmodel.cn/cn/coding-plan/transition)。
- 2026/04/22：方舟 Coding Plan 上线 MiniMax-M2.7、Kimi-K2.6、GLM-5.1
- 2026/04/21：阿里云百炼 Token Plan 团队版上线
- 2026/04/21：Kimi 正式发布 Kimi-K2.6 模型
- 2026/04/14：Kimi Code 上线 K2.6-code-preview 模型
- 2026/04/12：智谱国际版 GLM Coding Plan 起步价从 10 USD 每月涨至 18 USD 每月
- 2026/04/11：阿里云百炼 Coding Plan Lite 基础套餐于 2026 年 4 月 13 日起停止续费和升级，此前已于 2026 年 3 月 19 日停止新购
- 2026/04/11：添加了天翼云 Coding Plan
- 2026/08/20：天翼云编程 Token Plan 支持模型更新：新增 GLM-5.1、DeepSeek-V4-Flash-0731，GLM-5 更名为 GLM-5.0（正式版），DeepSeek-V3.2 标注为旗舰版
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
    ```
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
