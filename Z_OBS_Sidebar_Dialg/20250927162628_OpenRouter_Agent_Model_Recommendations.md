---
epoch: 1758961588000
modelKey: x-ai/grok-4-fast:free|openrouterai
topic: "OpenRouter Agent Model Recommendations"


tags:
  - copilot-conversation
---

# **user**: 以下openrouter的免费模型, 哪些适合agent和embedding, 请整理推荐"Models
53 models
Reset Filters
free
SortNewest
Top Weekly
Pricing: Low to High
Pricing: High to Low
Context: High to Low
Throughput: High to Low
Latency: Low to High


xAI: Grok 4 Fast (free)

790B tokens
Grok 4 Fast is xAI's latest multimodal model with SOTA cost-efficiency and a 2M token context window. It comes in two flavors: non-reasoning and reasoning. Read more about the model on xAI's news post. Reasoning can be enabled using the reasoning enabled parameter in the API. Learn more in our docs  Prompts and completions on Grok 4 Fast Free may be used by xAI or OpenRouter to improve future models.

by x-ai
2M context
$0/M input tokens
$0/M output tokens
DeepSeek: DeepSeek V3.1 (free)

209B tokens
DeepSeek-V3.1 is a large hybrid reasoning model (671B parameters, 37B active) that supports both thinking and non-thinking modes via prompt templates. It extends the DeepSeek-V3 base with a two-phase long-context training process, reaching up to 128K tokens, and uses FP8 microscaling for efficient inference. Users can control the reasoning behaviour with the reasoning enabled boolean. Learn more in our docs  The model improves tool use, code generation, and reasoning efficiency, achieving performance comparable to DeepSeek-R1 on difficult benchmarks while responding more quickly. It supports structured tool calling, code agents, and search agents, making it suitable for research, coding, and agentic workflows.   It succeeds the DeepSeek V3-0324 model and performs well on a variety of tasks.

by deepseek
164K context
$0/M input tokens
$0/M output tokens
Z.AI: GLM 4.5 Air (free)

21.6B tokens
GLM-4.5-Air is the lightweight variant of our latest flagship model family, also purpose-built for agent-centric applications. Like GLM-4.5, it adopts the Mixture-of-Experts (MoE) architecture but with a more compact parameter size. GLM-4.5-Air also supports hybrid inference modes, offering a "thinking mode" for advanced reasoning and tool use, and a "non-thinking mode" for real-time interaction. Users can control the reasoning behaviour with the reasoning enabled boolean. Learn more in our docs

by z-ai
131K context
$0/M input tokens
$0/M output tokens
DeepSeek: R1 0528 (free)

13.2B tokens
May 28th update to the original DeepSeek R1 Performance on par with OpenAI o1, but open-sourced and with fully open reasoning tokens. It's 671B parameters in size, with 37B active in an inference pass.  Fully open-source model.

by deepseek
164K context
$0/M input tokens
$0/M output tokens
DeepSeek: DeepSeek V3 0324 (free)

12.2B tokens
DeepSeek V3, a 685B-parameter, mixture-of-experts model, is the latest iteration of the flagship chat model family from the DeepSeek team.  It succeeds the DeepSeek V3 model and performs really well on a variety of tasks.

by deepseek
164K context
$0/M input tokens
$0/M output tokens
Qwen: Qwen3 Coder 480B A35B (free)

8.74B tokens
Qwen3-Coder-480B-A35B-Instruct is a Mixture-of-Experts (MoE) code generation model developed by the Qwen team. It is optimized for agentic coding tasks such as function calling, tool use, and long-context reasoning over repositories. The model features 480 billion total parameters, with 35 billion active per forward pass (8 out of 160 experts).  Pricing for the Alibaba endpoints varies by context length. Once a request is greater than 128k input tokens, the higher pricing is used.

by qwen
262K context
$0/M input tokens
$0/M output tokens
TNG: DeepSeek R1T Chimera (free)

8.58B tokens
DeepSeek-R1T-Chimera is created by merging DeepSeek-R1 and DeepSeek-V3 (0324), combining the reasoning capabilities of R1 with the token efficiency improvements of V3. It is based on a DeepSeek-MoE Transformer architecture and is optimized for general text generation tasks.  The model merges pretrained weights from both source models to balance performance across reasoning, efficiency, and instruction-following tasks. It is released under the MIT license and intended for research and commercial use.

by tngtech
164K context
$0/M input tokens
$0/M output tokens
TNG: DeepSeek R1T2 Chimera (free)

7.37B tokens
DeepSeek-TNG-R1T2-Chimera is the second-generation Chimera model from TNG Tech. It is a 671 B-parameter mixture-of-experts text-generation model assembled from DeepSeek-AI’s R1-0528, R1, and V3-0324 checkpoints with an Assembly-of-Experts merge. The tri-parent design yields strong reasoning performance while running roughly 20 % faster than the original R1 and more than 2× faster than R1-0528 under vLLM, giving a favorable cost-to-intelligence trade-off. The checkpoint supports contexts up to 60 k tokens in standard use (tested to ~130 k) and maintains consistent <think> token behaviour, making it suitable for long-context analysis, dialogue and other open-ended generation tasks.

by tngtech
164K context
$0/M input tokens
$0/M output tokens
DeepSeek: R1 (free)

5.88B tokens
DeepSeek R1 is here: Performance on par with OpenAI o1, but open-sourced and with fully open reasoning tokens. It's 671B parameters in size, with 37B active in an inference pass.  Fully open-source model & technical report.  MIT licensed: Distill & commercialize freely!

by deepseek
164K context
$0/M input tokens
$0/M output tokens
Microsoft: MAI DS R1 (free)

5.53B tokens
MAI-DS-R1 is a post-trained variant of DeepSeek-R1 developed by the Microsoft AI team to improve the model’s responsiveness on previously blocked topics while enhancing its safety profile. Built on top of DeepSeek-R1’s reasoning foundation, it integrates 110k examples from the Tulu-3 SFT dataset and 350k internally curated multilingual safety-alignment samples. The model retains strong reasoning, coding, and problem-solving capabilities, while unblocking a wide range of prompts previously restricted in R1.  MAI-DS-R1 demonstrates improved performance on harm mitigation benchmarks and maintains competitive results across general reasoning tasks. It surpasses R1-1776 in satisfaction metrics for blocked queries and reduces leakage in harmful content categories. The model is based on a transformer MoE architecture and is suitable for general-purpose use cases, excluding high-stakes domains such as legal, medical, or autonomous systems.

by microsoft
164K context
$0/M input tokens
$0/M output tokens"
[Timestamp: 2025/09/27 16:26:28]

**ai**: ### OpenRouter 免费模型推荐：适合 Agent 和 Embedding

根据您提供的 OpenRouter 免费模型列表，我对这些模型进行了分析。列表中共有 10 个模型，主要都是大型语言模型 (LLM)，专注于生成、推理和聊天任务。以下是针对“Agent”（AI 代理，通常需要工具调用、推理、代码生成和代理工作流支持）和“Embedding”（嵌入模型，用于文本向量化表示）的推荐整理。

#### 1. 适合 Agent 的模型推荐
Agent 任务通常要求模型支持工具调用 (tool use)、结构化输出、长上下文推理、代码代理 (code agents) 和搜索代理 (search agents) 等功能。从列表中，我筛选出明确提到或适合这些能力的模型。这些模型大多基于 MoE (Mixture-of-Experts) 架构，支持推理模式 (reasoning/thinking mode)，性能接近 OpenAI o1 等高级模型，且免费使用。

我按适合度排序（从高到低），并用表格总结关键信息：

| 模型名称 | 提供者 | 上下文长度 | 适合 Agent 的理由 | 推荐指数 |
|----------|--------|------------|-------------------|----------|
| DeepSeek V3.1 (free) | DeepSeek | 164K | 支持工具调用、代码生成、推理效率高；明确适用于代码代理、搜索代理和代理工作流 (agentic workflows)；可控制 reasoning 模式，响应更快。 | ★★★★★ |
| GLM 4.5 Air (free) | Z.AI | 131K | 专为代理中心应用 (agent-centric) 设计；支持混合推理模式 (thinking/non-thinking)，擅长高级推理和工具使用；轻量高效。 | ★★★★★ |
| Qwen3 Coder 480B A35B (free) | Qwen | 262K | 优化用于代理编码任务 (agentic coding)；支持函数调用、工具使用和长上下文仓库推理；MoE 架构，参数高效。 | ★★★★☆ |
| DeepSeek R1 0528 (free) | DeepSeek | 164K | 性能媲美 OpenAI o1，支持开放推理令牌；适合复杂代理任务，如问题解决和代码代理；开源且高效。 | ★★★★☆ |
| DeepSeek R1 (free) | DeepSeek | 164K | 与 R1 0528 类似，强推理能力；适用于代理中的多步思考和工具集成；MIT 许可，便于商业化。 | ★★★★☆ |
| Microsoft MAI DS R1 (free) | Microsoft | 164K | 基于 R1 改进，增强推理、编码和问题解决；支持多语言安全对齐，适合通用代理场景（非高风险领域）。 | ★★★☆☆ |
| TNG DeepSeek R1T Chimera (free) | TNG | 164K | 合并 R1 和 V3，平衡推理与效率；适合长上下文代理分析和对话生成。 | ★★★☆☆ |
| TNG DeepSeek R1T2 Chimera (free) | TNG | 164K | 二代 Chimera，推理强且速度快 (比 R1 快 20%)；适用于开放式代理任务，如长上下文对话。 | ★★★☆☆ |

**其他模型的说明**：
- xAI Grok 4 Fast：多模态支持强，但更偏向通用生成和 SOTA 效率；可用于简单代理，但未明确强调工具调用，推荐指数 ★★★☆☆。
- DeepSeek V3 0324：通用聊天模型，推理能力好，但不如 V3.1 针对代理优化，推荐指数 ★★☆☆☆。

**总体建议**：优先选择 DeepSeek V3.1 或 GLM 4.5 Air，它们直接支持代理核心功能，且上下文长、免费无限制。如果您的 Agent 涉及编码，Qwen3 Coder 是最佳补充。这些模型均支持 reasoning 参数启用高级模式，适合构建工具集成代理。

#### 2. 适合 Embedding 的模型推荐
列表中所有模型均为生成式 LLM（聊天/推理模型），**没有专用的 Embedding 模型**（如 OpenAI 的 text-embedding-ada-002 或类似向量化专用模型）。这些 LLM 可以通过 API 生成简单文本表示，但不推荐用于专业 Embedding 任务，因为：
- Embedding 需要高效的向量输出（通常 768+ 维），而这些模型更擅长文本生成，而非纯向量嵌入。
- 没有模型描述中提到 Embedding 支持（如语义搜索或向量数据库集成）。

**推荐**：如果您需要免费 Embedding，建议在 OpenRouter 之外探索其他提供商（如 Hugging Face 的免费 Embedding 模型，或 OpenAI 的免费额度）。列表中无合适模型；如果这是误解（例如指 Agent 中的嵌入组件），请提供更多上下文，我可以进一步分析。

如果您有特定任务细节（如 Agent 的工具类型或 Embedding 的应用场景），我可以更精确地调整推荐！
[Timestamp: 2025/09/27 16:26:51]

# **user**: 如果一定要用收费模型, 适合我的agent, 请比较前5, 列表生成优劣和费用
[Timestamp: 2025/09/27 17:34:56]

**ai**: ### OpenRouter 收费模型推荐：适合 Agent 的前 5 比较

如果您一定要使用收费模型来构建 Agent（AI 代理，通常涉及工具调用、推理、多步规划、代码生成和长上下文处理），我基于 OpenRouter 的热门收费模型推荐前 5 个。这些模型在 Agent 任务中表现出色，支持结构化工具使用（如 JSON 输出）和高级推理。推荐优先级基于 Agent 适用性（工具集成、响应速度、准确性和上下文长度），数据来源于 OpenRouter 的典型定价和模型规格（截至最新知识，实际费用可能因提供商而略有浮动；建议查阅 OpenRouter 实时定价）。

我选择了以下前 5（按 Agent 适合度排序）：
1. **Claude 3.5 Sonnet** (Anthropic) - Agent 首选，工具调用顶级。
2. **GPT-4o** (OpenAI) - 平衡性强，多模态支持。
3. **o1-preview** (OpenAI) - 专为复杂推理设计。
4. **Gemini 1.5 Pro** (Google) - 长上下文专家。
5. **Llama 3.1 405B** (Meta) - 开源高效，成本低。

#### 比较表格
表格包括：**模型名称**、**上下文长度**、**优劣（针对 Agent）**、**费用（输入/输出 per 1M tokens，USD）**。优劣聚焦 Agent 场景，如工具调用效率、推理深度和潜在局限。

| 模型名称              | 上下文长度 | 优劣（针对 Agent）                                                                 | 费用（输入 $ /M） | 费用（输出 $ /M） |
|-----------------------|------------|------------------------------------------------------------------------------------|-------------------|-------------------|
| Claude 3.5 Sonnet    | 200K      | **优**：工具调用和函数调用最强，支持复杂多步 Agent 工作流；推理准确、响应自然；安全对齐好，避免幻觉。**劣**：速度稍慢于 GPT-4o；不支持图像输入（纯文本 Agent 影响小）。适合研究/企业 Agent。 | 3.00              | 15.00             |
| GPT-4o               | 128K      | **优**：多模态（文本+图像+语音），易集成工具（如 API 调用）；速度快、成本效益高；OpenAI 生态丰富，便于 Agent 开发。**劣**：在极长上下文时准确率略降；有时过度泛化。通用 Agent 最佳平衡。 | 2.50              | 10.00             |
| o1-preview           | 128K      | **优**：推理深度超群（如数学/代码 Agent），模拟人类思考过程；工具使用可靠，适合复杂规划任务。**劣**：响应时间长（思考链内部化）；输出不可见中间步骤，调试难；不适合实时 Agent。 | 15.00             | 60.00             |
| Gemini 1.5 Pro       | 1M+ (实验 2M) | **优**：超长上下文处理（如整个代码库 Agent）；多模态强，支持视频/音频工具集成；Google 搜索工具无缝。**劣**：工具调用不如 Claude 精确；偶尔输出冗长。适合长文档/搜索 Agent。 | 3.50              | 10.50             |
| Llama 3.1 405B       | 128K      | **优**：开源（可微调 Agent 自定义）；参数大，推理/代码生成强；成本最低，适合高吞吐 Agent。**劣**：工具调用需额外提示工程；一致性不如闭源模型；在敏感话题上可能不稳定。预算友好选择。 | 1.00              | 3.00              |

#### 总体分析与建议
- **费用总结**：Llama 3.1 最便宜（适合高频 Agent 测试），o1-preview 最贵（仅用于高价值复杂任务）。平均每月费用取决于使用量：例如，处理 1B tokens 的 Agent，Claude 可能需 90-450 USD，Llama 仅 20-100 USD。OpenRouter 无最低消费，支持按需付费。
- **选择依据**：如果您的 Agent 强调工具集成和安全性，选 Claude 3.5 Sonnet；需多模态或快速响应，选 GPT-4o；复杂推理优先 o1-preview。Gemini 适合长上下文场景，Llama 适合自定义/低成本。
- **注意**：这些模型在 OpenRouter 上通过统一 API 访问，便于切换。实际性能测试推荐从小规模 Agent 原型开始。如果您的 Agent 有特定需求（如编码重点或实时性），提供更多细节，我可以进一步优化推荐！
[Timestamp: 2025/09/27 17:35:15]

# **user**: 优先国内的, 包括deepseek, qwen 其他3国内
[Timestamp: 2025/09/27 17:35:42]

**ai**: ### OpenRouter 收费模型推荐：优先国内模型，适合 Agent 的前 5 比较

根据您的要求，我优先推荐国内模型（中国 AI 公司开发），包括 DeepSeek 和 Qwen，并补充其他 3 个国内知名模型：GLM-4（智谱 AI）、Yi-1.5（零一万物）和 Baichuan2（百川智能）。这些模型在 OpenRouter 或类似平台上可用，适合 Agent 任务（如工具调用、推理、多步规划和代码生成）。国内模型的优势在于成本低、响应快、对中文优化好，且支持长上下文。

推荐前 5（按 Agent 适合度排序）：
1. **DeepSeek-V2** (DeepSeek AI) - 推理和工具调用强。
2. **Qwen2.5** (阿里云 Qwen) - 通用 Agent 平衡。
3. **GLM-4** (智谱 AI) - 代理中心设计。
4. **Yi-1.5-34B** (零一万物) - 开源高效。
5. **Baichuan2-13B** (百川智能) - 成本最低。

#### 比较表格
表格包括：**模型名称**、**上下文长度**、**优劣（针对 Agent）**、**费用（输入/输出 per 1M tokens，USD）**。费用基于 OpenRouter 典型定价（实际以平台实时为准，国内模型通常更便宜；无最低消费，按需付费）。优劣聚焦 Agent 场景，如工具集成和中文支持。

| 模型名称          | 上下文长度 | 优劣（针对 Agent）                                                                 | 费用（输入 $ /M） | 费用（输出 $ /M） |
|-------------------|------------|------------------------------------------------------------------------------------|-------------------|-------------------|
| DeepSeek-V2      | 128K      | **优**：MoE 架构，推理深度高，支持工具调用和代码代理；中文/英文双强，响应高效；开源，便于自定义 Agent。**劣**：长上下文时偶尔幻觉；工具输出需提示优化。适合复杂编码/搜索 Agent。 | 0.14              | 0.28              |
| Qwen2.5          | 128K      | **优**：多模态支持（文本+图像），工具使用流畅；阿里生态集成好，适合企业 Agent 工作流；长上下文推理准确。**劣**：在极复杂多步任务中不如 DeepSeek 稳定；输出有时冗长。通用中文 Agent 首选。 | 0.20              | 0.40              |
| GLM-4            | 128K      | **优**：专为代理应用设计，支持混合推理模式（thinking/non-thinking）；工具调用精确，中文优化优秀；安全对齐强。**劣**：速度中等，不如 Qwen 快；参数大，部署需资源。适合工具密集 Agent。 | 0.50              | 1.00              |
| Yi-1.5-34B       | 200K      | **优**：开源（MIT 许可），推理/代码生成强；上下文超长，适合仓库级 Agent；成本低，易微调。**劣**：工具调用依赖提示工程；一致性在敏感话题上稍弱。预算型长上下文 Agent 好选择。 | 0.10              | 0.20              |
| Baichuan2-13B    | 32K       | **优**：轻量高效，响应极快；中文任务出色，适合实时 Agent（如聊天工具）；开源，便于本地部署。**劣**：上下文较短，不宜超长任务；推理深度不如大模型。入门级/低成本 Agent 推荐。 | 0.05              | 0.10              |

#### 总体分析与建议
- **费用总结**：国内模型整体低廉（Yi 和 Baichuan 最便宜，适合高频测试；每月 1B tokens 处理，DeepSeek 约 10-50 USD）。相比国际模型（如 Claude），节省 70%+，且延迟低（国内服务器优势）。
- **选择依据**：如果 Agent 需强推理和工具，选 DeepSeek-V2；中文/多模态优先 Qwen2.5；代理专用选 GLM-4。Yi 适合自定义，Baichuan 适合简单实时场景。这些模型在 OpenRouter 上统一 API，便于切换。
- **注意**：国内模型对合规敏感（如避免敏感话题），但 Agent 性能已接近国际水平。建议从小规模测试开始。如果您的 Agent 有特定需求（如编码重点或集成工具），提供更多细节，我可以进一步调整！