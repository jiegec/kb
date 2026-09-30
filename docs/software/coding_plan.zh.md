# AI Coding Plan

## Coding Plan

### Kimi

[Kimi 登月计划](https://www.kimi.com/membership/pricing) | [Kimi Code](https://www.kimi.com/code)

- 档位（RMB 每月）：Andante 49、Moderato 99、Allegretto 199、Allegro 699
- Kimi Code 基于旗舰 K3 模型（参数规模约 2.8 万亿），提供 K2.8 Preview 普速版与 K2.7 Code HighSpeed 高速版双模式，最高推理速度 260 Tokens/s，支持 1M Tokens 超长上下文；兼容 Kimi Code CLI、Claude Code、VS Code 等主流 Agent 工具
- 模型 ID 与会员档位要求：`k3`、`k3-256k` 需 Moderato / Plus 及以上会员，其中 1M 上下文需 Allegretto / Pro 及以上会员；`kimi-for-coding`（K2.8 Preview）需 Andante / Plus 及以上会员；`kimi-for-coding-highspeed` 需 Allegretto / Pro 及以上会员
- API 接入点区分国内/海外：OpenAI 兼容 国内 `https://api.kimi.com/coding/v1`、海外 `https://api.kimi.ai/coding/v1`；Anthropic 兼容 国内 `https://api.kimi.com/coding/`、海外 `https://api.kimi.ai/coding/`；Kimi 开放平台 国内 `https://api.moonshot.cn/v1`、海外 `https://api.moonshot.ai/v1`
- API 价格（RMB 每 1M tokens）：
    - [K3](https://platform.kimi.com/docs/pricing/chat-k3)：输入命中缓存 2、输入未命中缓存 20、输出 100，1M 上下文
    - [K2.7-Code](https://platform.kimi.com/docs/pricing/chat-k27-code)：输入命中缓存 1.3、输入未命中缓存 6.5、输出 27，256K 上下文
    - [K2.7-Code-HighSpeed](https://platform.kimi.com/docs/pricing/chat-k27-code)：输入命中缓存 2.6、输入未命中缓存 13.0、输出 54，256K 上下文

### MiniMax

[MiniMax M Plan](https://platform.minimaxi.com/docs/token-plan/intro) | [产品定价](https://platform.minimaxi.com/docs/guides/pricing-token-plan) | [订阅](https://platform.minimax.cn/subscribe/token-plan)

- 产品名为 M Plan（原 Token Plan），覆盖范围已收窄为旗舰模型；音乐相关 API（Music-3.0、Music-2.6、歌词生成等）已下线，额度不再包含音乐资源
- 档位（RMB 每月，月度 M3 Token 用量）：Plus 49（约 6 亿+）、Max 119（约 18 亿+）、Ultra 469（约 71 亿+）
- MiniMax-M3.1-Flash-Preview 为新增语言模型（原生多模态、1M 上下文、思考深度可调），暂仅通过 M Plan 和 MiniMax Code 提供
- 停售与迁移：Max-极速（199 元每月）、Ultra-极速（899 元每月）停售，下个续费日自动转入 Max（119 元每月）/ Ultra（469 元每月），月费下调并每月补发等值积分（年包按月独立补发、每月额度独立有效期 1 年、不滚存）；Starter（29 元每月）、Plus-极速（98 元每月）为老用户专属保留档，仅对老用户开放
- 权益规则：2026-06-05 前已订阅用户的老用户权益继续保留；迁移补偿积分有效期自发放日起 1 年；权益加成自订阅生效起自动激活，仅在连续订阅周期内有效，变更档位或取消订阅即放弃
- Ultra 含每日 5 条视频生成额度；已购积分可用于 MiniMax 开放平台大部分模型（暂不支持 MiniMax H3），按各模型 API 刊例价实时扣减，文本/图像/语音/视频跨模态共享
- 预付积分包：¥30 获 4489 积分、¥150 获 22460 积分、¥500 获 74900 积分，有效期 365 天
- [MiniMax M3 API 价格](https://platform.minimaxi.com/docs/guides/pricing-paygo)（RMB 每 1M tokens）：
    - `<=` 512K 输入 token：输入命中缓存 0.42、输入未命中缓存 2.10、输出 8.40
    - `>` 512K 输入 token：输入命中缓存 0.84、输入未命中缓存 4.20、输出 16.80
    - 1M 上下文

[MiniMax 国际版 M Plan](https://platform.minimax.io/docs/token-plan/intro) | [产品定价](https://platform.minimax.io/docs/guides/pricing-token-plan)：Plus $22 每月、Max $55 每月、Ultra $132 每月

### 智谱

[智谱 GLM Coding Plan](https://docs.bigmodel.cn/cn/coding-plan/overview)

- Lite 套餐（118 RMB 每月）：每 5 小时 2000 积分，每周 10000 积分
- Pro 套餐（538 RMB 每月）：每 5 小时 12000 积分，每周 60000 积分
- Max 套餐（1078 RMB 每月）：每 5 小时 28000 积分，每周 140000 积分
- 模型消耗积分数 =（输入 Token × Input 抵扣系数 + 缓存命中 Token × Cached Input 抵扣系数 + 输出 Token × Output 抵扣系数）/ 10000
- MCP 消耗积分数 = 调用次数 × Output 抵扣系数
- 所有套餐均支持 **GLM-5.3**、**GLM-5.3-Flash**；调用历史模型 GLM-5.2、GLM-5.1 自动切换至 GLM-5.3，调用 GLM-5-Turbo、GLM-4.7 自动切换至 GLM-5.3-Flash
- 非高峰时段按基础积分消耗的 50% 抵扣；高峰时段为每周一至周五的 14:00～18:00（UTC+8）
- 限时活动：
    - 「夜间畅用活动」（2026-09-03 至 2026-10-07，每日 23:00～次日 09:00）：在 [ZCode](https://zcode.z.ai/cn)、[AutoClaw](https://autoclaw.zhipuai.cn/) 端调用 GLM-5.3-Flash 无限用量，在其他 Agent 额度翻倍
    - 「庆双节活动」（2026-09-25 至 2026-10-07）：全天按非高峰时段规则消耗额度
- 抵扣系数：GLM-5.3 为 Input 6.9 / Cached Input 1.7 / Output 24；GLM-5.3-Flash（含视觉理解 MCP）为 Input 2.3 / Cached Input 0.56 / Output 8
- 套餐 Token 用量因缓存命中率而异：

| 缓存命中率 | 模型          | Lite（亿 Tokens/周） | Pro（亿 Tokens/周） | Max（亿 Tokens/周） |
|------------|---------------|--------------------|-------------------|-------------------|
| 95%        | GLM-5.3       | 0.48～0.97          | 2.90～5.80         | 6.76～13.52        |
| 95%        | GLM-5.3-Flash | 1.46～2.92          | 8.77～17.55        | 20.47～40.95       |
| 96%        | GLM-5.3       | 0.50～0.99          | 2.97～5.95         | 6.94～13.87        |
| 96%        | GLM-5.3-Flash | 1.50～3.00          | 9.00～18.01        | 21.01～42.02       |
| 98%        | GLM-5.3       | 0.52～1.04          | 3.13～6.27         | 7.31～14.63        |
| 98%        | GLM-5.3-Flash | 1.58～3.17          | 9.50～19.00        | 22.17～44.33       |

区间说明：最多 Tokens 为全部在非高峰时段按 0.5 倍消耗；最少 Tokens 为全部在高峰时段按 1 倍消耗。充分利用非高峰优惠时，相较按量调用 GLM-5.3 标准 API 最高可节省 92% 成本
- API 价格（RMB 每 1M tokens）：
    - [GLM-5.3](https://bigmodel.cn/pricing)：输入命中缓存 2、输入未命中缓存 8、输出 28，1M 上下文
    - [GLM-5.3-Flash](https://bigmodel.cn/pricing)：输入命中缓存 0.23、输入未命中缓存 0.8、输出 2.8，1M 上下文
    - [GLM-5.2](https://bigmodel.cn/pricing)：输入命中缓存 2、输入未命中缓存 8、输出 28，1M 上下文
    - [GLM-5.1](https://bigmodel.cn/pricing)：输入命中缓存 1.3/2、输入未命中缓存 6/8、输出 24/28，200K 上下文
    - [GLM-5-Turbo](https://bigmodel.cn/pricing)：输入命中缓存 1.2/1.8、输入未命中缓存 5/7、输出 22/26，200K 上下文
    - [GLM-4.7](https://bigmodel.cn/pricing)：输入命中缓存 0.4/0.6/0.8、输入未命中缓存 2/3/4、输出 8/14/16，200K 上下文

[智谱 GLM Coding Plan 团队版](https://docs.bigmodel.cn/cn/coding-plan/team)

- 团队标准版（598 RMB 每月）：每 5 小时最多 0.6 亿 tokens 每席位，每周最多 3 亿 tokens 每席位
- 团队高级版（1198 RMB 每月）：每 5 小时最多 1.6 亿 tokens 每席位，每周最多 8 亿 tokens 每席位
- 「最多」指在 1 倍消耗系数下可实际消耗的 Tokens 总量；各模型额度消耗规则：
    - GLM-4.7、GLM-4.5-Air：全天按 1 倍系数消耗
    - GLM-5.2、GLM-5-Turbo：高峰 3 倍、非高峰 2 倍；限时福利为非高峰仅按 1 倍抵扣
    - 高峰时段为每日 14:00～18:00（UTC+8）

[智谱国际版 GLM Coding Plan](https://z.ai/subscribe)：所有套餐均支持 GLM-5.3、GLM-5.3-Flash；调用 GLM-5.2/GLM-5.1 自动路由至 GLM-5.3，GLM-4.7 自动路由至 GLM-5.3-Flash

### 云厂商

- [方舟 Coding Plan 个人版](https://www.volcengine.com/activity/codingplan) | [文档](https://www.volcengine.com/docs/82379/1925114)
    - Lite 套餐（40 RMB 每月）：每 5 小时最多约 1,200 次请求、每周最多约 9,000 次、每订阅月最多约 18,000 次
    - Pro 套餐（200 RMB 每月）：Lite 的 5 倍用量
    - 支持模型：Doubao-Seed-2.1-pro、Doubao-Seed-2.1-lite、Doubao-Seed-2.0-mini、Doubao-Seed-2.1-turbo（即将下线）、Doubao-Seed-Evolving、Doubao-Seed-2.0-lite（即将下线）、MiniMax-M3、Kimi-K2.7-Code、Kimi-K2.8-Preview、Kimi-K3（抵扣系数高，仅建议 Pro 套餐用户）、GLM-5.3、GLM-5.3-Flash、DeepSeek-V4-Flash、DeepSeek-V4-Pro、DeepSeek-V4.1-Flash
    - 1M 上下文支持：doubao-seed-evolving、glm-5.3、glm-5.3-flash、kimi-k3、kimi-k2.8-preview、deepseek-v4.1-flash、deepseek-v4-flash、deepseek-v4-pro
    - 限时活动：deepseek-v4.1-flash 抵扣系数 5 折（2026-09-23 00:00 至 2026-10-30 18:00）；Kimi-K2.8-Preview 可用量活动（2026-09-18 00:00 至 2026-10-14 23:59，与 Agent Plan 6 折抵扣活动期间相当）
    - 主要模型规格：Doubao-Seed-2.1-pro（新一代旗舰，1024k 上下文/256k 输出）、Doubao-Seed-2.1-lite（轻量高效，1024k/256k）、Doubao-Seed-2.0-mini（极速响应，256k/128k）、DeepSeek-V4.1-Flash（552B 总参数 MoE、原生多模态视觉理解，1024k/384k）、Kimi-K2.8-Preview（综合性能接近 K3、思考效率更高，1M/1M、支持文本与图片输入）、GLM-5.3-Flash（智谱首个原生多模态模型，320B 总参数/18B 激活，1M/128K）
- [方舟 Agent Plan 个人版](https://www.volcengine.com/docs/82379/2366394)
    - Agent 燃料值（AFP）为统一用量计费单位：文本/向量模型 =（输入 token × 输入抵扣系数 + 输出 token × 输出抵扣系数）/ 10000；视频模型 = tokens / 10000 × 系数；图片模型 = 成功生成张数 × 系数。抵扣系数由模型统一决定，不随输入长度变化
    - 各模型抵扣系数（输入/输出相同）：doubao-seed-2.0-mini 0.25（输入不含音频）/ 2.5（输入含音频）；doubao-seed-2.0-lite（即将下线）、deepseek-v4-flash 0.5；doubao-seed-2.1-lite 0.5 / 4.5（含音频）；glm-5.3-flash 0.5；doubao-seed-2.1-turbo（即将下线）、doubao-seed-evolving、minimax-m3、doubao-seed-2.1-pro 2.5；deepseek-v4.1-flash 2.5（限时 5 折 1.25）；kimi-k2.7-code 4.5；kimi-k2.8-preview 8（限时 6 折 4.8）；glm-5.3（glm-latest）4.5；deepseek-v4-pro 5.5；kimi-k3 10；doubao-embedding-vision 0.5
    - 档位（AFP，每 5 小时/每周/每月/每日）：Small 40 RMB 每月（2000/7000/20000/10000）、Medium 200（10000/35000/100000/50000）、Large 500（25000/87500/250000/125000）、Max 1000（50000/175000/500000/250000）
    - 图片、视频、语音模型与 Harness 无 5 小时与周限制，仅受日额度与月额度限制，日额度为月额度的一半
    - 全套餐支持：doubao-seed-2.1-pro、doubao-seed-2.1-lite、doubao-seed-2.0-mini、doubao-seed-2.0-lite（即将下线）、deepseek-v4-flash、deepseek-v3.2、minimax-m3、glm-5.3、glm-5.3-flash、kimi-k2.7-code、kimi-k2.8-preview、deepseek-v4-pro、deepseek-v4.1-flash、doubao-embedding-vision、doubao-seedream-5.0-lite（即将下线）、doubao-seedream-5-0-pro、doubao-seed-tts-2.0、doubao-seed-asr-2.0
    - Medium 以上额外支持：doubao-seedance-2.0、doubao-seedance-2.0-fast、doubao-seedance-2.0-mini、doubao-seedance-2.5
    - Agent 进化：前 50 个文件免费
- [阿里云百炼 Token Plan（个人版）](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
    - Lite（60，限时 39）、Essential（120，限时 79）、Standard（180，限时 139）、Pro（600，限时 499）RMB 每月，对应 11500 / 25500 / 45000 / 180000 Credits 每月；用量包（100 RMB 每月）= 20000 Credits
    - 自 2026-09-22 起取消 7 天固定窗口限额，改为订阅月（30 天）额度，订阅月内累计消耗达到套餐额度即暂停服务，未用完额度不结转
    - 抵扣顺序：每次调用优先抵扣当前订阅月的套餐额度，用尽后自动抵扣用量包额度
    - 升配：不重置当前订阅周期，按剩余天数补缴差价并发放当前周期新增额度，自下一个订阅月起按新档位月额度计量
    - Essential 可同时支持 2–3 个 Agent 并发，权益为 Lite 全部权益
    - 仅限本人在单台设备上使用
    - 支持模型：auto、qwen3.8-max、qwen3.8-flash、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、qwen-image-3.0-pro、qwen-audio-3.0-tts-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-asr-flash、wan2.7-image、wan2.7-image-pro、deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731、glm-5.3、glm-5.2、happyhorse-1.1-i2v、happyhorse-1.1-t2v、happyhorse-1.1-r2v、decision-model-preview
    - 限时夜间折扣（每晚 22:00–次日 08:00）：qwen3.8-max、qwen3.8-flash 的 Credits 消耗 4 折；deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash 5 折
    - decision-model-preview（领域模型-决策模型）限时免费，调用不消耗 Credits
- [阿里云百炼 Token Plan（团队版）](https://help.aliyun.com/zh/model-studio/token-plan-overview)
    - 标准坐席 ¥198/坐席/月（25,000 Credits）、高级坐席 ¥698（100,000）、尊享坐席 ¥1,398（250,000）；共享用量包 ¥5,000/个（625,000 Credits）
    - 单次消耗 Credits 由模型类型、Token 用量、思考模式及工具调用动态决定；以 Qwen3.6-plus 为例，每 5000 输入未命中缓存 token、每 50000 输入命中缓存 token、每 5000/6 输出 token 为一个 Credit
    - 1 Credit 对应 API 价格（隐式缓存）：256K 以内上下文 0.01–0.02 元，256K–1M 0.04–0.08 元
    - 支持模型：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro、qwen-image-3.0-pro、qwen-audio-3.0-tts-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-asr-flash、wan2.7-image、wan2.7-image-pro、deepseek-v4-pro、deepseekv4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、kimi-k2.7-code、kimi-k2.6、kimi-k2.5、glm-5.2、glm-5.1、glm-5、minimax-m2.5、happyhorse-1.1-i2v、happyhorse-1.1-t2v、happyhorse-1.1-r2v
- [腾讯云大模型 Token Plan](https://cloud.tencent.com/act/pro/tokenplan)
    - 企业版专业套餐：1 元/100 积分，单次购买最低 5 万积分（500 元/月）；轻享套餐：2 元/百万 tokens
    - 企业版支持模型（广州/新加坡略有差异）：Auto、Hy4 preview、GLM-5.3、GLM-5.3-Flash、GLM-5.2、GLM-5（2026-10-09 下线）、GLM-5.1（2026-10-09 下线）、GLM-5-Turbo（2026-10-09 下线）、Kimi K2.7 Code、Kimi K2.7 Code HighSpeed、Kimi K3、Kimi-K2.6、MiniMax-M2.7、MiniMax-M3、DeepSeek-V4-Pro、DeepSeek-V4-Flash 0731 正式版、DeepSeek-V4-Pro 0813 正式版、DeepSeek-V4.1-Flash（非原厂直供）、DeepSeek-V4.1-Flash 原厂直供、DeepSeek-V4-Flash 0731 正式版 原厂直供、DeepSeek-V4-Pro 0813 正式版 原厂直供、DeepSeek-V4-Flash-Vision-Exp 原厂直供、MiMo-V2.6-Pro、MiMo-V2.6-Flash
    - 峰谷计费：DeepSeek 模型工作日（周一至周五）9:00–12:00、14:00–18:00 为高峰，其余为空闲；周末全天按空闲计费
    - 积分抵扣价（积分每百万 tokens）：DeepSeek-V4.1-Flash（含原厂直供）缓存命中 2 / 未命中 100 / 输出 400（空闲）、4 / 200 / 800（高峰）；Hy4 preview 30 / 600 / 1800；MiMo-V2.6-Pro 广州 2.5/300/600、新加坡 2.59/313.05/626.1；MiMo-V2.6-Flash 广州 2/100/200、新加坡 2.02/100.75/201.5
    - 个人版 Hy Token Plan：Lite 28 RMB 每月（560 积分）、Standard 78（1560）、Pro 238（4760）、Max 468（9360）；支持 Hy3、Hy4 preview
    - 个人版通用 Token Plan：Lite 39（780 积分）、Standard 99（1980）、Pro 299（5980）、Max 599（11980）；支持 Auto、DeepSeek-V4.1-Flash 原厂直供、DeepSeek-V4-Flash 正式版 原厂直供、DeepSeek-V4-Pro 正式版 原厂直供、MiniMax-M2.7、MiniMax-M3、GLM-5、GLM-5.1、GLM-5.2、GLM-5.3、GLM-5.3-Flash、Kimi K2.7 Code、Kimi K3、Hy4 preview、MiMo-V2.6-Flash
- [百度千帆 Token Plan 个人版](https://cloud.baidu.com/product/codingplan.html) | [个人版文档](https://cloud.baidu.com/doc/qianfan/s/Dmrabu8b6) | [企业版文档](https://cloud.baidu.com/doc/qianfan/s/ymq8wwch2)
    - Mini 9.9 RMB 每月（1000 万 token）、Lite 40（4200 万）、Pro 200（2.3 亿）、Max 600（7 亿）
    - 支持模型：DeepSeek-V4-Pro、DeepSeek-V4-Flash、GLM-5.2、GLM-5.1、Kimi-K2.6、ERNIE 5.1
- [京东云 Coding Plan](https://docs.jdcloud.com/cn/jdaip/PackageOverview)
    - Lite 套餐（首购 19.9、续费 40 RMB 每月）：每 5 小时最多 1,200 次请求、每周最多 9,000 次、每订阅月最多 18,000 次
    - Pro 套餐（首购 99.9、续费 200 RMB 每月）：每 5 小时最多 6,000 次、每周 45,000 次、每订阅月 90,000 次
    - 支持模型：DeepSeek-V3.2、GLM-5、GLM-4.7、MiniMax-M2.5、Kimi-K2.5、Kimi-K2-Turbo、Qwen3-Coder
- [讯飞星辰 Astron Token Plan 团队版](https://www.xfyun.cn/doc/spark/TokenPlan.html) | [订阅](https://maas.xfyun.cn/tokenPlan/subscription)
    - 标准成员 200 RMB/席/月（20000 Credits、200 万 TPM）、高级成员 600（60000 Credits、300 万 TPM）、尊享成员 1200（200000 Credits、500 万 TPM）
    - 支持模型：Spark-X2.5、Spark-X2-Flash、GLM-5.2、GLM-5.1、GLM-5、DeepSeek-V4-Pro、DeepSeek-V4-Flash、DeepSeek-V3.2、Kimi-K2.6、Kimi-K2.5、MiniMax-M2.5、Qwen3.5-397B-A17B、Qwen3.6-35B-A3B、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、GLM-4.7-Flash
- [讯飞星辰 Astron Coding Plan](https://www.xfyun.cn/doc/spark/CodingPlan.html) | [订阅](https://maas.xfyun.cn/packageSubscription)
    - 专业版（39 RMB 每月）：每 5 小时约 1,200 次请求、每周约 9,000 次、每订阅月约 18,000 次；支持 Spark-X2-Agent、Spark-X2、Auto、GLM-5.1、GLM-5、MiniMax-M2.5、Kimi-K2.6、Kimi-K2.5、DeepSeek-V3.2、Spark-X2-Flash、Qwen3.6-35B-A3B、GLM-4.7-Flash、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、Qwen3.5-397B-A17B
    - 高效版（199 RMB 每月）：每 5 小时约 6,000 次、每周约 45,000 次、每订阅月约 90,000 次；支持 Spark-X2-Agent、Spark-X2、Auto、GLM-5、GLM-5.2、DeepSeek-V4-Pro、DeepSeek-V4-Flash、MiniMax-M2.5、Kimi-K2.6、Kimi-K2.5、DeepSeek-V3.2、Spark-X2-Flash、Qwen3.6-35B-A3B、GLM-4.7-Flash、Qwen3.5-35B-A3B、Qwen3-Coder-Next-FP8、Qwen3.5-397B-A17B
- [天翼云编程 Token Plan](https://www.ctyun.cn/document/11061839/11092368)（积分版）
    - 29（3000 积分）、89（10000）、199（25000）、399（50000）、699（100000）RMB 每月
    - 支持模型：DeepSeek-V4-Pro、DeepSeek-V4-Flash-0731、GLM-5.2、GLM-5.1、Kimi-K2.6、MiniMax-M3
    - 积分与 Token 兑换关系（1 积分相当于多少个 Token，输入/输出）：DeepSeek-V4-Pro 1,111/370；DeepSeek-V4-Flash 3,333/1,111；GLM-5.2 1,250/357；GLM-5.1 输入 [0,32k] 1,667（输出 417）、(32k,200k] 1,250（输出 357）；Kimi-K2.6 1,538/370；MiniMax-M3 输入 [0,512k] 4,762（输出 1,190）、(512k,1M] 2,381（输出 595）
    - 原按 Token 计量套餐仅存量已订阅用户可续订
- [华为云 MaaS Token Plan](https://support.huaweicloud.com/Token-plan-maas/tokenplan-maas-0001.html)
    - Lite 59 RMB 每月（每订阅月 5000 万 tokens）、Standard 149（1.3 亿）、Pro 399（3.8 亿）、Max 799（8.8 亿）
    - 支持模型：GLM-5、GLM-5.1、Kimi-K2.6、DeepSeek-V3.2、DeepSeek-V4-Flash

### 其他

- [阶越星辰 Step Plan](https://platform.stepfun.com/docs/zh/step-plan/overview)
    - Flash Mini 49 RMB 每月（400M Credit）、Flash Plus 99（1600M）、Flash Pro 199（8000M）、Flash Max 699（40000M）
    - 支持模型：step-5-preview（新一代旗舰基模）、step-3.7-flash、step-3.5-flash-2603、step-3.5-flash、stepaudio-2.5-realtime、stepaudio-2.5-chat、stepaudio-2.5-tts、stepaudio-2.5-asr、step-router-v1（在 deepseek-v4-pro 和 step-3.5-flash 之间智能路由）
- [小米 MiMo Token Plan 个人版](https://platform.xiaomimimo.com/#/docs/tokenplan/subscription)
    - Lite（39 RMB 或 6 USD 每月）：41 亿 Credits 每月；Standard（99 RMB 或 16 USD）：110 亿；Pro（329 RMB 或 50 USD）：380 亿；Max（659 RMB 或 100 USD）：820 亿
    - 支持模型：MiMo-V2.6-Pro、MiMo-V2.6-Flash、MiMo-V2.5-Pro、MiMo-V2.5、MiMo-V2.5-ASR、MiMo-V2.5-TTS-VoiceClone、MiMo-V2.5-TTS-VoiceDesign、MiMo-V2.5-TTS
    - **mimo-v2.5-pro、mimo-v2.5 将于北京时间 2026-10-21 10:00 正式下线，建议尽快切换至新版模型**
    - 折扣：套餐首购 88 折、连续包年 88 折、夜间（0:00–8:00）0.8 倍消耗
- [OpenCode Go](https://opencode.ai/docs/zh-cn/go)
    - 两种方案：**Go（10 美元每月）**与 **Go Plus（40 美元每月）**，两者 token 价格相同，Go Plus 仅各模型用量限制更高（月额度为 Go 的 2–8 倍，多数为 4 倍）
    - 使用限制按各模型每月额度定义：5 小时 = 月限 20%、每周 = 50%、每月 = 100%
    - 支持模型：Grok 4.7、Grok 4.6、GLM-5.3/5.3-Flash/5.2、GPT 6 Luna、GPT 5.6 Luna、Kimi K3/K2.7 Code/K2.6、LongCat-2.0、MiMo-V2.6-Flash/V2.6-Pro/V2.5/V2.5-Pro、MiniMax M3/M2.7、Muse Spark 1.3 Contributor、Muse Spark 1.2 Contributor、Qwen3.8 Max/Qwen3.8 Flash/Qwen3.7 Plus、DeepSeek V4 Pro/V4 Flash/V4 Flash Vision Exp、Hy4 preview、Hy3、Space Bunny Free（限时免费）、LongCat 2.5 Preview Free（限时免费）
- [阶越星辰国际版 Coding Plan](https://platform.stepfun.ai/docs/en/step-plan/overview)
- [联通元景 GLM-5 Coding Plan](https://maas.ai-yuanjing.com/doc/pages/216556920/)
- [摩尔线程 AI Coding Plan](https://code.mthreads.com/)
- [KwaiKAT Coding Plan](https://www.streamlake.com/marketing/coding-plan)
- [DeepSeek API 定价](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)：
    - 峰谷定价：空闲时段价格为高峰时段的一半；高峰时段为北京时间周一至周五 9:00-12:00、14:00-18:00
    - deepseek-flash（DeepSeek-V4.1-Flash，1M 上下文，支持图像理解）：空闲时段输入命中缓存 0.02 / 输入未命中缓存 1 / 输出 4 RMB 每 1M tokens；高峰时段 0.04 / 2 / 8
    - deepseek-v4-pro（DeepSeek-V4-Pro-0813，1M 上下文，不支持图像理解）：空闲时段输入命中缓存 0.15 / 输入未命中缓存 4.5 / 输出 13.5 RMB 每 1M tokens；高峰时段 0.30 / 9.0 / 27.0

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

| 模型名称                                                                                | 参数量  | 激活量            | 视觉 |
|-------------------------------------------------------------------------------------|------|----------------|----|
| [DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | 284B | 13B            | 否  |
| [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)           | 284B | 13B            | 否  |
| [DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)     | 1.6T | 49B            | 否  |
| [DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)               | 1.6T | 49B            | 否  |
| [DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)       | 552B | 输入 8B / 输出 16B | 是  |
| [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)                       | 30B  | 3B             | 否  |
| [GLM-4.7](https://huggingface.co/zai-org/GLM-4.7)                                   | 355B | 32B            | 否  |
| [GLM-5.1](https://huggingface.co/zai-org/GLM-5.1)                                   | 744B | 40B            | 否  |
| [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)                                   | 744B | 40B            | 否  |
| [GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash)                       | 320B | 18B            | 是  |
| [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3)                                   | 744B | 40B            | 否  |
| [Hy3-preview](https://huggingface.co/tencent/Hy3-preview)                           | 295B | 21B            | 否  |
| [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)                                | 2.8T | 104B           | 是  |
| [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)                            | 1T   | 32B            | 是  |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)                           | 428B | 23B            | 是  |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)                       | 230B | 10B            | 否  |
| [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)                  | 2.4T | 95B            | 是  |
| [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)                              | 27B  | -              | 是  |
| [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)                | 180B | 6B             | 是  |
| [Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)                  | 397B | 17B            | 是  |

## 更新历史

- 2026/09/30：腾讯云大模型 Token Plan（企业版 `1823/130659`、个人版 `1823/130060` 与个人版套餐概览 `1772/129449` 三页同步更新至 2026-09-30 14:02）模型库更新：企业版专业套餐（广州/新加坡）新增 Hy4 preview、MiMo-V2.6-Pro、MiMo-V2.6-Flash 三款模型，移除仅有固定积分价、不带「0731 正式版」后缀的 `deepseek-v4-flash`，并把两个原厂直供模型名称补全为「DeepSeek-V4-Flash 0731 正式版 原厂直供」「DeepSeek-V4-Pro 0813 正式版 原厂直供」（model ID 不变）；三款新模型同步公布积分抵扣价——Hy4 preview 缓存命中 30 / 未命中 600 / 输出 1800（广州与新加坡一致，综合单价预估 约 158、50 万积分预估约 31.65 亿 tokens），MiMo-V2.6-Pro 广州 2.5/300/600、新加坡 2.59/313.05/626.1（综合单价预估 约 107 / 约 112），MiMo-V2.6-Flash 广州 2/100/200、新加坡 2.02/100.75/201.5（综合单价预估 约 33），单位均为积分每百万 tokens 且均不分峰谷；个人版通用 Token Plan 可用模型新增 DeepSeek-V4.1-Flash 原厂直供（model ID `deepseek/deepseek-flash`）与 MiMo-V2.6-Flash，各档位积分额度与 Hy Token Plan 未变。峰谷计费方面，新加坡地域章节本次也统一为与广州相同的「工作日（周一至周五）9:00–12:00、14:00–18:00 为高峰时段、其余空闲，周末（周六、周日）全天按空闲时段计费；原厂直供模型自 2026-08-29 00:00 起生效、其他 DeepSeek 模型（除 `deepseek-v4-flash`、`deepseek-v4-pro` 外）自 2026-09-26 00:00 起生效」表述，此前「仅广州章节更新、新加坡仍保留旧表述」的情况已消失；广州地域价格表中 Auto 行名称由「Auto 智能路由」改为「Auto 模型」（与新加坡一致），DeepSeek 免责声明由逐一列举具体模型名改为「由 DeepSeek 原厂直供的模型服务」，峰谷单价、其余模型积分价与套餐价格均未变

- 2026/09/30：MiniMax 官方文档把「Token Plan」更名为「M Plan」：模型概览页与按量计费定价页（中英文共四个页面）中的「Token Plan」字样全部替换为「M Plan」（如「暂时仅通过 M Plan 和 MiniMax Code 提供」「M Plan MCP」插件、「通过 M Plan 调用 API-vlm 时，会按其按量计费价格扣减套餐内 M Plan 额度」），文档站点导航「定价」下拉与文档顶部标签页新增 M Plan（指向 `/docs/m-plan/intro`）并把原 Token Plan 标签隐藏、外链改为 https://www.minimax.cn/m-plan；Token Plan FAQ 与 Token Plan 介绍页本次抓取仍写作「Token Plan」（按量计费页中「资源覆盖范围与 Token Plan 相同」一句及指向 Token Plan 定价页的链接亦未改），说明更名尚在进行中；套餐档位、价格、额度与订阅入口均未变

- 2026/09/29：火山方舟把 kimi-k2.8-preview 的 6 折抵扣活动窗口由 2026-09-30 23:59:59 延长至 2026-10-14 23:59:59：Agent Plan 中该模型抵扣系数 8 的限时 6 折（4.8）活动期（起始 2026-09-17 00:00 不变）随之延后两周；Coding Plan 中该模型可用量「与 Agent Plan 6 折抵扣活动期间相当」的活动期同步由 2026-09-18 00:00 至 2026-09-30 23:59 改为至 2026-10-14 23:59。Agent Plan 个人版计费说明（82379/2516283）、Agent Plan 个人版套餐概览（82379/2366394）与 Coding Plan 个人版套餐概览（82379/1925114）三页于 2026-09-29 15:26 同步更新，套餐价格、档位额度与其余模型的抵扣系数均未变

- 2026/09/29：阿里云百炼 Token Plan 个人版概述页（页面更新时间 2026-09-28 22:20）在升配折算公式下新增一句「实际补差金额以支付页面展示的价格明细为准」——升配补差公式、换算示例与各档价格均未变；同站 FAQ 页本次仅变更「上一篇」导航链接（由「接入 Harness 工具」改为「Harness 权益」），无内容变化；该导航链接已于 2026-09-29 13:38 抓取时改回「接入 Harness 工具」，页面正文内容自始至终未变

- 2026/09/29：OpenCode Go 文档（zh-cn）使用限制章节删除举例说明：原「例如，如果某个模型在 Go 的每月限制为 $60，在 Go Plus 的每月限制为 $120……」的示例，以及「跨模型计算时，Go 的 5 小时、每周和每月额度分别为 $12、$30 和 $60；Go Plus 则分别为 $48、$120 和 $240」一句被整体移除，现仅保留「每个模型 5 小时 = 月限 20%、每周 = 50%、每月 = 100%」与「下方每个模型的每月限制决定其用量如何计入这些额度」；各模型的月度使用额度表、token 价格表与请求限额表未变（该页面无更新时间戳，本次抓取于 2026-09-29 01:22），跨模型合计额度自此不再见于页面

- 2026/09/28：火山方舟 Agent Plan 个人版套餐概览与计费说明（AFP 抵扣规则）把 doubao-seedream-5.0-lite 标记为「即将下线」（模型表中该行、以及 AFP 抵扣示例中的模型名均加上「即将下线」，各档位仍为 √，官方尚未给出具体下线日期）

- 2026/09/28：MiniMax Token Plan FAQ 新增「订阅权益调整说明」与「Token Plan迁移说明」两节，首次以官方文档形式说明档位迁移与补偿规则：Max-极速（199 元每月）、Ultra-极速（899 元每月）停售并转入 Max（119 元每月）/ Ultra（469 元每月），月费分别下调 80/430 元、每月另补发价值约 160/860 元等值积分（年包按月独立补发、每月额度有效期 1 年不滚存）；Starter（29 元）、Plus-极速（98 元）转为老用户专属保留档、不再对新用户售卖；2026-06-05 前订阅用户的老用户权益继续保留，迁移补偿积分有效期由 1 个月自动订正为 1 年；Plus/Max 档价格不变、M2.7 的 5 小时使用次数约 +10%，并新增 M3 使用权限与多模态额度；已购积分可用于开放平台大部分模型（暂不支持 MiniMax H3）且跨模态共享；国际版迁移说明中 Plus/Max 仍写作 $20/$50，与国际版定价页的 $22/$55 不一致

- 2026/09/28：OpenCode Go 新增 **Go Plus（40 美元每月）** 方案并与 Go（10 美元每月）并列：两个方案 token 价格完全相同，Go Plus 仅提高各模型的用量限制——各模型月额度普遍为 Go 的 2–8 倍（多数为 4 倍，如 GLM-5.3 $15→$120、GLM-5.3-Flash $60→$180、Kimi K2.6 $60→$240、DeepSeek V4 Flash $30→$120），跨模型合计额度 Go 为 5 小时 $12 / 每周 $30 / 每月 $60、Go Plus 为 $48/$120/$240；订阅入口名称由 OpenCode Zen 改为 OpenCode Console，每个工作空间仍限一名成员订阅 Go 或 Go Plus。同一页面更新把 GLM-5.1、Qwen3.7 Max、Qwen3.6 Plus、MiniMax M2.5 从模型列表、token 价格表、请求限额预估表、接入点表与数据保留表中移除（Omen Alpha 亦已不在页面任何列表中，本次同步修正 kb 中仍将其列为支持模型的旧内容）

- 2026/09/27：OpenCode Go 新增限时免费的 LongCat 2.5 Preview Free 模型：input、output、cache read 均为 Free，请求限额与月度使用额度均标注为「无限制」（限时活动，官方未给出结束时间）；model ID `longcat-2.5-preview-free`，接入点 https://opencode.ai/zen/go/v1/chat/completions（支持模型列表、token 价格表、请求限额表、接入点表与数据保留表同步新增该模型，其余模型的价格与额度无变化）

- 2026/09/26：OpenCode Go 的 DeepSeek V4.1 Flash 额度提升 4 倍由限时活动转为常规值：定价表中该模型的月度使用额度由「~~$15~~ **$60** 4x · 9 月 27 日结束」改为直接标注 **$60**，请求限额预估表同步把「~~6,500~~ **26,000**（4x · 9 月 27 日结束）」改为 **26,000/65,000/130,000**——原 $15、6,500/16,250/32,500 的基准值与活动结束时间标注全部移除，即额度提升与提高后的请求限额成为常规额度；token 价格不变（空闲时段 input $0.15/1M、output $0.60/1M、cache read $0.003/1M，高峰时段为两倍）

- 2026/09/25：无问芯穹 Infini GenStudio 更新日志发布「2026-10-09 发布预告」：`deepseek-v4-flash` 将于 2026 年 10 月 9 日 12:00 下架，官方推荐替换模型为 `deepseek-v4.1-flash`，建议提前完成迁移（该平台此前的 Infini Coding Plan 已于 2026-06-27 下线，此变化影响 GenStudio API 调用）

- 2026/09/25：阿里云百炼新增领域模型 decision-model-preview 并纳入 Token Plan 个人版（相关页面更新时间 2026-09-24）：模型调用价格页新增「决策模型」章节（计费规则为按输入 token 计费，模型 `decision-model-preview` 输入单价标注「限时免费」，覆盖华北2（北京）与新加坡两地），「选择模型」页新增「决策模型」分类，介绍为「面向高频业务判断的结构化决策模型，一次前向完成分类、是非判断与评分，并返回概率分布与置信度」（模型详情页 /zh/model-studio/decision-model-preview）；Token Plan 个人版概述页的权益说明新增「decision-model-preview 限时免费：调用不消耗 Credits，接入方法参见接入决策模型」，支持模型表新增一行「领域模型 / decision-model-preview / 决策模型」

- 2026/09/25：腾讯云 Token Plan 企业版专业套餐（页面更新时间 2026-09-24 20:08）DeepSeek 峰谷计费规则改写并新增非原厂直供的 DeepSeek-V4.1-Flash：注意事项由「原厂直供模型周末全天空闲、正式版高峰时段为周一至周日」统一改为「所有 DeepSeek 模型工作日（周一至周五）9:00–12:00、14:00–18:00 为高峰时段、其余空闲，周末（周六、周日）全天按空闲时段计费」，并新增生效时间说明——原厂直供模型自北京时间 2026-08-29 00:00 起生效，其他 DeepSeek 模型（除不分峰谷、按固定积分价计费的 `deepseek-v4-flash`、`deepseek-v4-pro` 外）自北京时间 2026-09-26 00:00 起生效，即 DeepSeek-V4-Flash 0731 正式版、DeepSeek-V4-Pro 0813 正式版等平台托管模型自 9 月 26 日起同样享有周末全天空闲价；页面仅更新了广州地域章节的注意事项，新加坡地域章节仍保留旧表述。模型库（广州/新加坡两地）同步新增非原厂直供的 DeepSeek-V4.1-Flash（model ID `deepseek-v4.1-flash`，与原厂直供的 `deepseek/deepseek-flash` 并存），其积分抵扣价与原厂直供完全一致——缓存命中 2 / 未命中 100 / 输出 400（空闲时段）、4 / 200 / 800（高峰时段）积分每百万 tokens，综合单价预估 约 26 / 约 51 积分每百万 tokens

- 2026/09/24：阿里云百炼模型调用价格页 DeepSeek 第三方模型章节补充峰谷时段定义（相关页面更新时间 2026-09-23 23:50）：在 DeepSeek-V4-Flash-0731 峰谷定价说明之后、列有忙时/闲时单价的模型表之前，新增一句「其中，忙时为北京时间 8:00 - 22:00，闲时为北京时间 22:00 - 次日 8:00」；即表中标注忙时/闲时单价的 DeepSeek 模型按每日 8:00–22:00 为忙时、22:00–次日 8:00 为闲时计费（该时段与百炼 Token Plan 个人版夜间折扣时段一致）；价格数字与其他计费规则未变
- 2026/09/24：OpenCode Go 模型列表新增 GPT 6 Luna：按 272K tokens 分档，≤272K tokens 输入 $0.10/输出 $0.50/缓存读取 $0.01/缓存写入 $0.125 每 1M tokens，>272K tokens 为 $0.20/$0.75/$0.02/$0.25；输入与缓存价格恰为 GPT 5.6 Luna 的一半、输出更低（原 $1.20），GPT 5.6 Luna 保留在列表与定价表中；月度使用额度 $15，请求限额 4,230/5 小时、10,560/周、21,130/月；model ID `gpt-6-luna`，接入点 https://opencode.ai/zen/go/v1/responses（数据保留说明同步由「GPT 5.6 Luna」改为「GPT 6 Luna / GPT 5.6 Luna」）
- 2026/09/23：智谱 GLM Coding Plan「夜间畅用活动」的适用客户端由 ZCode 扩展为 ZCode 与 AutoClaw（[autoclaw.zhipuai.cn](https://autoclaw.zhipuai.cn/)）：套餐用户在两个客户端调用 GLM-5.3-Flash 均无限用量，活动时间与其他条款不变（2026-09-03 至 2026-10-07 每日 23:00～次日 09:00，在其他 Agent 端额度翻倍）
- 2026/09/23：OpenCode Go 新增限时免费的 Space Bunny Free 模型：input、output、cache read 均为 Free，请求限额与月度使用额度均标注为「无限制」；model ID `space-bunny-free`，接入点 https://opencode.ai/zen/go/v1/chat/completions（官方未给出该限时活动的结束时间）
- 2026/09/23：火山方舟 Coding Plan 个人版与 Agent Plan 个人版模型库更新：新增 doubao-seed-2.1-pro（新一代旗舰级模型，综合能力全面提升，1024k 上下文窗口/256k 输出）、doubao-seed-2.1-lite（轻量高效，1024k 上下文窗口/256k 输出）、doubao-seed-2.0-mini（极速响应，256k 上下文窗口/128k 输出）与 deepseek-v4.1-flash（DeepSeek 全新架构系列轻量旗舰，552B 总参数 MoE，原生多模态视觉理解，1024k 上下文窗口/384k 最大输出；此前已进入 Agent Plan，本次进入 Coding Plan）；doubao-seed-2.1-turbo、doubao-seed-2.0-lite 标记为「即将下线」（官方公告为「模型启动下线」），doubao-seedance-1.5-pro 从 Agent Plan 模型表移除；Agent Plan 抵扣系数相应更新——doubao-seed-2.1-pro 2.5、doubao-seed-2.1-lite 0.5（输入包含音频 4.5）、doubao-seed-2.0-mini 细化为输入不含音频 0.25 / 输入包含音频 2.5；Coding Plan 与 Agent Plan 的 1M 上下文支持名单均加入 deepseek-v4.1-flash（Agent Plan 名单：doubao-seed-evolving、glm-5.3、glm-5.3-flash、kimi-k3、kimi-k2.8-preview、deepseek-v4.1-flash、deepseek-v4-flash、deepseek-v4-pro）
- 2026/09/23：火山方舟 deepseek-v4.1-flash 抵扣系数限时 5 折活动窗口延长并扩展至 Coding Plan：Agent Plan 中该活动的截止时间由 2026-09-28 23:59 延长至 2026-10-30 18:00（起始 2026-09-15 00:00 不变，抵扣系数 2.5 → 1.25）；Coding Plan 同步新增该活动，活动期为 2026-09-23 00:00 至 2026-10-30 18:00
- 2026/09/23：天翼云编程 Token Plan 改版为积分计量并新增「编程Token Plan（积分版）」：套餐档位与价格不变（29/89/199/399/699 元每月），额度由 Token 定额改为 3000/10000/25000/50000/100000 积分每订阅月，支持模型改为 DeepSeek-V4-Pro、DeepSeek-V4-Flash-0731、GLM-5.2、GLM-5.1、Kimi-K2.6、MiniMax-M3（原 GLM-5.0、DeepSeek-V3.2 移出）；页面新增「积分与模型的兑换关系」表（1 积分相当于多少个 Token，输入/输出——DeepSeek-V4-Pro 1,111/370、DeepSeek-V4-Flash 3,333/1,111、GLM-5.2 1,250/357、GLM-5.1 输入 [0,32k] 1,667（输出 417）与输入 (32k,200k] 1,250（输出 357）、Kimi-K2.6 1,538/370、MiniMax-M3 输入 [0,512k] 4,762（输出 1,190）与输入 (512k,1M] 2,381（输出 595）），并注明模型库为动态更新机制、不承诺永久固定提供任一指定模型；原按 Token 计量套餐标注「老套餐即将下线，仅存量已订阅用户可续订，不支持新购」，其支持模型更新为 DeepSeek-V4-Flash-0731、GLM-5.1、GLM-5.0（2026-10-10 下线）与 DeepSeek-V3.2（页面写作 DeepSeeV3.2，2026-10-10 下线）
- 2026/09/23：快手万擎（StreamLake/Vanchin，KwaiKAT Coding Plan 所在平台）模型列表新增 DeepSeek-V4.1-Flash（列于多模态章节：深度思考 + 图像理解，1M 上下文 / 384K 最大输出，原生多模态视觉理解，默认限流 RPM 10 / TPM 300000；模型列表页更新时间 2026-09-22 23:11）；该页是万擎按量计费的模型目录，未说明该模型是否计入 KwaiKAT Coding Plan 套餐额度
- 2026/09/23：阿里云百炼 Token Plan 个人版取消周限额、改为订阅月额度（相关页面更新时间 2026-09-22 23:52）：个人版由「每 7 天固定窗口限额」改为月额度——订阅月自订阅当日起算 30 天，订阅月内累计消耗达到套餐额度后暂停服务，需等下一个订阅月额度重置（按订阅日自动刷新，非固定日历日期），未用完额度不结转；各档位额度同步调整为 Lite 11,500 / Essential 25,500 / Standard 45,000 / Pro 180,000 Credits 每月（档位与价格不变，限时价 39/79/139/499 元每月），存量订阅的剩余额度已于 2026-09-22 一次性重置为对应套餐的满月额度、订阅周期与到期时间不变；此前的「重置卡 / 额度重置权益」（页面上的「重置限额」按钮与重置次数说明）整体删除，额度重置改为订阅月自动重置；抵扣顺序改为「每次调用优先抵扣当前订阅月的套餐额度，用尽后自动抵扣用量包额度」，用量包不再表述为「不受 7 天窗口限额约束」，而是「不占用、不计入套餐月额度」；升配规则改为不重置当前订阅周期——按 (新套餐价格 − 旧套餐价格) × 剩余天数 ÷ 30（不满一天按一天计算）补缴差价，并按剩余天数 ÷ 30 × (升级后月额度 − 升级前月额度) 向上取整发放当前周期新增 Credits，自下一个订阅月起按新档位月额度计量；429 错误提示由 `insufficient_quota: Your token-plan 1-week quota has been exhausted.` 改为 `insufficient_quota: Your token-plan quota has been exhausted.`；团队版 FAQ 对比表中的「个人版额度机制」同步改为「月额度，按订阅月自动刷新」，团队版概述表格移除「7 天限额：无限制」行
- 2026/09/22：商汤 SenseNova API 文档（含 TokenPlan 积分与模型总览）模型库调整：模型总览移除 DeepSeek V4 Pro，新增 DeepSeek V4.1 Flash（model ID `deepseek-flash`，1M 上下文、支持图像输入），DeepSeek V4 Flash（`deepseek-v4-flash`）保留；对应模型章节同步改写，并新增图像输入说明与限制（单图 ≤50 MB、单请求 ≤200 张、总请求体 ≤64 MB、以 URL 传入图片总大小 ≤200 MB，视频输入仅 Chat Completions 接口支持）、`max_tokens` 默认值改为 131072（范围 1–393216，思考超出长度会被截断）、`reasoning_effort` 原生档位为 none/low/high/max 并提供兼容映射、明确不支持显式缓存
- 2026/09/22：智谱 GLM Coding Plan（国内站 bigmodel.cn 与国际版 z.ai DevPack 页面同步公告）新增两项限时活动：「夜间畅用活动」——2026-09-03 至 2026-10-07 每日 23:00～次日 09:00，套餐用户在 [ZCode](https://zcode.z.ai/cn) 端调用 GLM-5.3-Flash 无限用量，在其他 Agent 额度翻倍；「庆双节活动」——2026-09-25 至 2026-10-07 全天按非高峰时段规则消耗额度（即全天按 50% 积分消耗），官方同时提示叠加夜间活动后实际可用额度远高于额度参考表所列数值
- 2026/09/22：阿里云百炼模型调用价格、模型库与上下文缓存更新：Stepfun-阶跃星辰 部署新增 stepfun/step-5-preview（输入 7 元、输出 20 元每百万 Token，无免费额度，与 stepfun/step-3.7-flash 的 1.35/8.1 元并存）、Unisound-云知声 章节列出 unisound/unisound-u2（1 元输入/2 元输出，该章节在页面中重复出现两次）；新增「音频生成」计费章节（qwen-audio-3.1-tts-next，按输入输出 Token 计费 6/12 元）；语音识别新增 Qwen-Audio-3.1 系列并由按音频秒数计费改为按 Token 计费——qwen-audio-3.1-asr-flash-message 与 qwen-audio-3.1-asr-flash-streaming 为 6/4.5 元（国际站 6.781/5.104 元）、qwen-audio-3.1-asr-flash-filetrans 与 qwen-audio-3.1-asr-flash 为 0.8/2.7 元（国际站 1.094/3.427 元），3.0 系列按秒计费的档次保留；「选择模型」页语音识别推荐位由 qwen-audio-3.0-asr-flash-streaming/-filetrans 换为 3.1 版本；上下文缓存的 Stepfun（阶跃星辰部署）名单新增 stepfun/step-5-preview；qwen3.8-max-prime 的优速模式文档链接由 /fast-mode 改为 /prime-mode；官方 OpenCode / OpenClaw 接入文档中的 Workspace ID 链接由「获取 Workspace ID」改为地域说明页（/zh/model-studio/regions#h2_migrate_domain）
- 2026/09/22：阿里云百炼 Token Plan 个人版限时夜间折扣调整：qwen3.8-max 的折扣由 5 折改为 4 折，并新增 qwen3.8-flash 同为 4 折；deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash 维持 5 折（均为每晚 22:00 - 次日 08:00 的 Credits 消耗优惠）
- 2026/09/22：OpenCode Go 新增 Grok 4.7、MiMo-V2.6-Flash、MiMo-V2.6-Pro 三款模型——Grok 4.7 的定价与请求限额与 Grok 4.6 相同（≤200K tokens 输入 $2.00/输出 $6.00/缓存读取 $0.50，>200K tokens $4.00/$12.00/$1.00 每 1M tokens；额度 $15/月；请求限额 169/5 小时、423/周、845/月；model ID grok-4.7）；MiMo-V2.6-Flash/V2.6-Pro 与其上一代 MiMo-V2.5/V2.5-Pro 的定价与请求限额完全一致（$0.14/$0.28/$0.0028 额度 $60 与 $0.435/$0.87/$0.003625 额度 $15）
- 2026/09/22：小米 MiMo Token Plan 页面改版为「个人版」，支持模型由 9 款改为 8 款——新增 mimo-v2.6-pro、mimo-v2.6-flash（Credit 折算与上一代同档：V2.6-Pro 命中缓存 2.5/未命中 300/输出 600、V2.6-Flash 2/100/200 Credits 每 Token），同时从支持模型与额度消耗表中移除 MiMo-V2-Pro、MiMo-V2-Omni、MiMo-V2-TTS；页面顶部新增公告「mimo-v2.5-pro、mimo-v2.5 将于北京时间 2026-10-21 10:00 正式下线」；套餐价格与额度不变（39/99/329/659 元或 6/16/50/100 美元每月，41/110/380/820 亿 Credits 每月）；折扣说明收敛为「首购 88 折、连续包年 88 折、夜间 0.8 倍消耗」三项，此前页面上的 Token Plan 升级「Credits 用量焕新重置」活动（2026-05-27 生效）已删除，套餐购买说明同时改为「仅支持同时购买 1 个个人版套餐」
- 2026/09/21：阿里云百炼 Token Plan 个人版支持模型新增 auto（官方描述为「平台提供的智能模型，按请求内容自动匹配底层模型，兼顾效果与成本」，能力标注「推理模型、文本生成」，在模型表中列于千问品牌首位）；官方 OpenCode / OpenClaw 接入文档同步为个人版与团队版配置加入 auto 条目（OpenCode 中仅声明 input/output 均为 text，无 reasoning 与 limit 字段；OpenClaw 中 contextWindow 1,000,000、maxTokens 393,216、reasoning false），并把 OpenClaw 的默认模型由 `bailian-token-plan/qwen3.8-flash` 改为 `bailian-token-plan/auto`
- 2026/09/21：阿里云百炼模型调用价格与上下文缓存支持的模型名单新增两款——智谱部署的 ZHIPU/GLM-5.3-FlashX（仅思考模式，输入 2 元、输出 7 元每百万 Tokens，无免费额度；缓存命中折扣 28.5%，高于同系列 ZHIPU/GLM-5.3-Flash 等 5 款模型的 25%）与快手万擎部署的 vanchin/deepseek-v4.1-flash（输入 2 元、输出 8 元每百万 Tokens；缓存命中折扣 2%，低于 vanchin/deepseek-v4-pro 的 8.33%）
- 2026/09/21：OpenCode Go 的 DeepSeek V4.1 Flash 额度限时提升 4 倍活动延长——结束时间由 2026-09-20 改为 2026-09-27（月度使用额度 $60、请求限额 26,000/5 小时、65,000/周、130,000/月与 token 价格均不变）
- 2026/09/20：阶越星辰 Step Plan 支持模型新增 step-5-preview（面向真实任务的新一代旗舰基模），同时移除 step-image-edit-2 并删除原有图像模型下线公告，即套餐不再包含文生图与图像编辑模型，官方对模型的描述相应由「旗舰模型，覆盖文本、推理、语音、图像编辑与智能路由」改为「文本、推理、语音与智能路由」；官方文档把 Base URL 说明按工具拆分——Claude Code / Anthropic SDK 使用 `https://api.stepfun.com/step_plan`，OpenAI SDK 的 Chat Completions 调用仍使用 `https://api.stepfun.com/step_plan/v1`，并明确 Step Plan 通道消耗套餐 Credit、与普通 API 通道额度相互独立（FAQ 同步改为按工具选择地址）
- 2026/09/18：Kimi Code 文档为各模型 ID 补充会员档位要求，并首次出现 Plus / Pro 档位命名——k3 / k3-256k 需 Moderato / Plus 及以上会员（1M 上下文需 Allegretto / Pro 及以上）；kimi-for-coding 的表述由「所有会员可用」改为「Andante / Plus 及以上会员可用」；kimi-for-coding-highspeed 需 Allegretto / Pro 及以上会员。同一页面为 API 接入点补充海外域名：Kimi Code 海外 OpenAI 兼容 https://api.kimi.ai/coding/v1、Anthropic 兼容 https://api.kimi.ai/coding/，Kimi 开放平台 海外 https://api.moonshot.ai/v1（国内分别为 api.kimi.com/coding、api.moonshot.cn/v1）
- 2026/09/18：OpenCode Go 移除 Union Alpha Free 模型（限时免费结束）——支持模型列表、token 价格表、请求限额表与接入点表同步移除该模型（model ID union-alpha）
- 2026/09/18：火山方舟 Coding Plan 个人版与 Agent Plan 个人版新增 kimi-k2.8-preview 模型（综合性能接近 K3、思考效率更高，支持文本和图片输入；1M 上下文窗口/1M 最大输出，全套餐支持）；Agent Plan 抵扣系数 8，2026-09-17 00:00 至 2026-09-30 23:59 限时 6 折（4.8）；Coding Plan 中该模型在 2026-09-18 00:00 至 2026-09-30 23:59 活动期间的可用量与 Agent Plan 6 折抵扣活动期间相当；模型同时加入 1M 上下文支持名单（现为 glm-5.3、glm-5.3-flash、deepseek-v4.1-flash、deepseek-v4-flash、deepseek-v4-pro、kimi-k3、kimi-k2.8-preview）
- 2026/09/18：阿里云百炼 Token Plan 个人版新增 Essential 档，个人版档位由 Lite/Standard/Pro 三档变为四档：原价 120 元/月、限时 79 元/月，每 7 天 5,625 Credits（Lite 的 2.25 倍），可同时支持 2-3 个 Agent 并发，权益为 Lite 全部权益；官方页面同时把用量包（100 元/个/月、20,000 Credits，需先订阅有效套餐后购买、最多同时持有 5 个、不受 7 天窗口限额约束）从套餐表格行改为脚注说明
- 2026/09/17：OpenCode Go 新增 Union Alpha Free 模型（限时）：input/output/cache read 均为 Free，请求与额度不限（限时）；model ID union-alpha，接入点 https://opencode.ai/zen/go/v1/messages（Anthropic 兼容）
- 2026/09/16：阿里云百炼 Token Plan 个人版「支持的模型」新增 glm-5.3（智谱 AI，能力标注「推理模型、文本生成」，与 glm-5.2 并存；glm-5.3 已于 2026-09-15 上线百炼模型库，但当时未列入 Token Plan）；官方接入文档同步加入该模型配置——OpenClaw 中 contextWindow 1,000,000、maxTokens 16,384、reasoning false，OpenCode 中 thinking 开启（budgetTokens 8192）；个人版限时夜间五折名单不变（qwen3.8-max、deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash）
- 2026/09/15：快手万擎（StreamLake/Vanchin，KwaiKAT Coding Plan 所在平台）模型列表新增 GLM-5.3、GLM-5.3-Flash、DeepSeek-V4-Pro-0813 三款模型（模型列表页更新时间 2026-09-15 21:15）；该页是万擎按量计费的模型目录，未说明这些模型是否计入 KwaiKAT Coding Plan 套餐额度
- 2026/09/15：阿里云百炼模型调用价格新增 GLM 系列 glm-5.3（非思考和思考模式，不区分 Token 阶梯，输入 8 元、输出 28 元每百万 Tokens，华北2（北京）等中国站地域与「全球」部署同价；国际站 10.208/32.084 元，赠送 100 万 Tokens 免费额度）；上下文缓存支持的 GLM（阿里云百炼部署）模型名单同步加入 glm-5.3（缓存命中折扣 25%，与 glm-5.2、glm-5.2-fast-preview 同档）；同时「GLM-智谱」部署的 ZHIPU/GLM-5.3 模式由「非思考和思考模式」修正为「仅思考模式」（价格不变，输入 8 元、输出 28 元，无免费额度）
- 2026/09/15：火山方舟 Agent Plan 个人版新增 deepseek-v4.1-flash 模型（全套餐支持；1M 上下文窗口/384K 最大输出，原生具备多模态视觉理解能力），抵扣系数 2.5，2026-09-15 00:00 至 2026-09-28 23:59 限时 5 折（折后 1.25）；该模型同时加入 1M 上下文支持名单（现为 glm-5.3、glm-5.3-flash、deepseek-v4.1-flash、deepseek-v4-flash、deepseek-v4-pro、kimi-k3）
- 2026/09/14：阿里云百炼 Token Plan 个人版支持模型列表中 deepseek-v4.1-flash 的能力标注由「推理模型、文本生成」更新为「推理模型、视觉理解、文本生成」；官方接入文档（OpenClaw）中该模型配置的 input 也由 `["text"]` 改为 `["text", "image"]`，即确认 Token Plan 内该模型可直接接收图片输入
- 2026/09/14：火山方舟 Agent Plan 个人版新增两个多模态模型：doubao-seedream-5-0-pro（图片生成，全套餐支持；输入图第一张免费、第二张起 10 AFP/张，输出图单图生成场景 ≤261 万像素 150、>261 万像素 300 AFP/张，图层拆分场景 75/150）与 doubao-seedance-2.5（视频生成，Large/Max；480p/720p 输入含视频 210、不含视频 350，1080p 输入含视频 230、不含视频 385，单位为 token）；doubao-seedance-1.5-pro 标记为即将下线
- 2026/09/14：阿里云百炼 Token Plan 个人版支持模型新增 deepseek-v4.1-flash（此前仅上线百炼模型库、未列入 Token Plan），同时该模型加入个人版限时夜间五折（每晚 22:00–次日 08:00 Credits 消耗 5 折）名单，名单现为 qwen3.8-max、deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash
- 2026/09/14：腾讯云 Token Plan 企业版专业套餐（广州/新加坡）模型库新增 DeepSeek-V4.1-Flash 原厂直供（model ID `deepseek/deepseek-flash`）；同时原厂直供 Flash 系积分抵扣价统一下调——DeepSeek-V4-Flash 0731 正式版 原厂直供（原空闲 约 39 / 高峰 约 77 积分每百万 tokens）与 DeepSeek-V4-Flash-Vision-Exp 原厂直供（原 约 35 / 约 70）均降至与新模型一致（缓存命中 2 / 未命中 100 / 输出 400 空闲时段、4/200/800 高峰时段，综合单价预估 约 26 / 约 51），即跟随 DeepSeek 原厂把旧模型名统一切换到 V4.1-Flash 计费；同一页面移除了已于 2026-09-10 到期的 GLM-5.3-Flash 积分价 5 折限时优惠活动章节
- 2026/09/14：OpenCode Go 将 DeepSeek V4.1 Flash 的额度限时提升 4 倍：月度使用额度由 $15 提高到 $60（活动 2026-09-20 结束），请求限额同步由 6,500/5 小时、16,250/周、32,500/月 提高到 26,000/5 小时、65,000/周、130,000/月；token 价格不变
- 2026/09/14：阿里云百炼模型库新增 deepseek-v4.1-flash：华北2（北京）/全球价 忙时输入 2 元、闲时 1 元，忙时输出 8 元、闲时 4 元（每百万 tokens，送 100 万 tokens 免费额度）；国际站 忙时 2.188/8.75 元、闲时 1.094/4.375 元。上下文缓存命中单价为输入单价的 10%（忙时 0.2 元、闲时 0.1 元），优于百炼其他模型的 20%，但仍高于 DeepSeek 官方 API 的缓存命中价（0.04/0.02 元）。「选择模型」页推荐位同时由 deepseek-v4-flash-0731 换为该模型；该模型暂未列入百炼 Token Plan（个人版/团队版）支持模型
- 2026/09/12：OpenCode Go 将 DeepSeek V4.1 Flash 的 model ID 由 deepseek-flash 更名为 deepseek-v4.1-flash
- 2026/09/12：Kimi Code 普速版模型由 K2.7 Code 更新为 K2.8 Preview（model 名 kimi-for-coding 现指向 K2.8 Preview，支持最高 1M 上下文与 low/high/max 三档思考强度）；高速版仍为 K2.7 Code HighSpeed
- 2026/09/12：DeepSeek 撤回 V4 Pro 下线计划：官方称应广大用户需求，2026-09-14 之后继续提供 DeepSeek V4 Pro 的 API 调用服务，计费方式保持不变
- 2026/09/10：模型参数比较表新增 DeepSeek-V4.1-Flash（总参数 552B，输入激活 8B / 输出激活 16B，支持多模态）
- 2026/09/10：DeepSeek 发布 DeepSeek-V4.1-Flash（新模型名 deepseek-flash，1M 上下文，支持图像理解），价格大幅下调（空闲时段：缓存命中 0.02、未命中 1、输出 4 元；高峰时段 0.04/2/8 元每百万 tokens）；旧模型名 deepseek-v4-flash、deepseek-v4-flash-vision-exp 已下线（请求由 V4.1-Flash 提供服务并按 Flash 价计费）；官方计划有序下线 V4 Pro，2026-09-14 12:00 后 deepseek-v4-pro 请求将全部路由到 V4.1 Flash 并按 Flash 价计费（注：此变化此前被归档工具漏抓，本次手动核实补充）
- 2026/09/10：智谱 GLM-5.3-Flash 限时五折结束、恢复标准价（输入未命中缓存 0.8、输出 2.8、缓存命中 0.23 元/百万 tokens），阿里云百炼同一模型也移除了「限时5折」标注；腾讯云 Token Plan（个人版通用套餐与企业版专业套餐）GLM-5、GLM-5.1、GLM-5-Turbo 标记将于 2026-10-09 下线；OpenCode Go 计费限制改为按各模型每月额度定义（5 小时 = 月限 20%、每周 = 50%、每月 = 100%），各模型月限不同（如 GLM-5.3 $15、GLM-5.3-Flash $60）
- 2026/09/09：火山方舟 Coding Plan 个人版新增 Kimi-K3 模型（1M 上下文/128K 最大输出，原生视觉理解，抵扣系数高，仅建议 Pro 套餐用户）；讯飞星辰 Astron Token Plan 团队版新增 Spark-X2.5 模型（256K，输入 320/缓存 48/输出 1200/思考 1200 积分每百万 Token），Spark-X2、Spark-X2-Agent 下线
- 2026/09/04：阶越星辰 Step Plan 宣布 step-image-edit-2 模型将于 2026-10-10 下线，Step Plan 文生图与图像编辑接口同步停止服务
- 2026/09/04：OpenCode Go 新增支持 Omen Alpha 模型（input $0.20/1M、output $0.66/1M、cache read $0.04/1M，使用额度 $100/月；请求限额 11,600/5 小时、29,000/周、57,900/月；model ID omen-alpha）
- 2026/09/04：腾讯云大模型 Token Plan 模型库新增：通用 Token Plan（个人版）与企业版专业套餐均新增 GLM-5.3-Flash、Kimi K3 模型；企业版专业套餐同步公布两模型的积分抵扣价（广州 GLM-5.3-Flash 23/80/280、Kimi K3 200/2000/10000；新加坡 GLM-5.3-Flash 21.5898/107.949/359.83，单位积分/百万 tokens）
- 2026/09/03：Kimi Code 页面「核心优势」改版：明确当前基于旗舰 K3 模型（参数规模约 2.8 万亿）与 K2.7 Code 双模式（普速版 / High Speed 高速版），最高推理速度 260 Tokens/s（此前描述为 100 Tokens/s），支持 1M Tokens 超长上下文；移除「高速版为普通版 5–6 倍」及「每 5 小时约 300–1200 次请求、最高并发 30」的表述
- 2026/09/03：阿里云百炼 Token Plan 个人版使用规则收紧：官方将使用说明由"可将同一个 API Key 配置到您本人的多台设备（如家庭电脑和公司电脑）上使用"改为"仅限本人在单台设备上使用"
- 2026/09/03：OpenCode Go 新增支持 Muse Spark 1.3 Contributor 模型（Meta Contributor 体系：允许 Meta 使用提示词和补全结果训练未来模型以换取大幅折扣 token 价格；input $0.10/1M、output $0.20/1M、cache read $0.002/1M，使用额度 $60；请求限额 45,300/5 小时、113,300/周、226,600/月；model ID muse-spark-1.3-contributor；仅在 Meta [地理使用政策](https://ai.developer.meta.com/legal/geographic-use-policy)允许的地区提供）
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
- 2026/08/20：天翼云编程 Token Plan 支持模型更新：新增 GLM-5.1、DeepSeek-V4-Flash-0731，GLM-5 更名为 GLM-5.0（正式版），DeepSeek-V3.2 标注为旗舰版
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
