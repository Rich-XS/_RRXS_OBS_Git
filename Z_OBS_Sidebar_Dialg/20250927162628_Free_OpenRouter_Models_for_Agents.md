---
epoch: 1758961588881
modelKey: x-ai/grok-4-fast:free|openrouterai
topic: "Free OpenRouter Models for Agents"


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