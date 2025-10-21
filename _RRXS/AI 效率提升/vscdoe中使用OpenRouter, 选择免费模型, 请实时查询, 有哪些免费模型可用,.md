---
title: "我在vscdoe中使用OpenRouter, 选择免费模型, 请实时查询, 有哪些免费模型可用, ..."
source: "https://gemini.google.com/app/fb46eb745920a1d6"
author:
  - "[[Gemini]]"
published:
created: 2025-09-29
description: "认识 Gemini：Google 旗下的 AI 助理。在写作、规划和开展头脑风暴等方面获得帮助。体验生成式 AI 的强大功能。"
tags:
  - "clippings"
---
我在vscdoe中使用OpenRouter, 选择免费模型, 请实时查询, 有哪些免费模型可用, 推荐-- 针对推理强 和或编程 和或 网站.. 需要能够Agent 只能端到端完成的 (应该至少包括 Grok/Gemini/Qwen/Deepseek, 及其他2个), 就主要维度列表生成

---

很高兴为您提供关于 **OpenRouter 免费模型** 的实时信息和推荐。

根据您在 VS Code 中使用 Agent 且追求 **推理强、编程能力高、端到端自动化** 的需求，以下是目前 OpenRouter 上免费且表现优异的模型列表，重点涵盖了您提到的几大模型系列：

---

## OpenRouter 免费模型推荐及核心维度对比

目前（2025年9月）OpenRouter 上的免费模型多为大型、高性能模型的精简版或特定开源版本，非常适合您的 Agent 自动化工作流。

| 模型系列 (API ID) | 主要优势/特点 | 重点推荐用途 | 推理能力 (Agent/复杂任务) | 编程/代码能力 | Context Window (Tokens) |
| --- | --- | --- | --- | --- | --- |
| **xAI: Grok 4 Fast (free)** | **极高上下文窗口** ，针对推理和代码有优化，支持推理模式。 | **端到端 Agent** 任务、长文档/代码库分析、复杂的逻辑推理。 | **强** (支持 Reasoning) | 优秀 | 2,000,000 |
| **DeepSeek: DeepSeek V3.1 (free)** | **混合推理模型** ，性能与 DeepSeek-R1 相当， **工具使用和代码生成** 能力强。 | **Agent Workflows** 、复杂代码生成、结构化工具调用、研究分析。 | **强** (支持 Thinking Mode) | 优秀 | 164,000 |
| **Z.AI: GLM 4.5 Air (free)** | **专为 Agent 应用程序** 设计，MoE 架构，轻量级，支持思考模式。 | 实时交互、 **Agent 流程** 、需要快速响应和工具使用的任务。 | **强** (支持 Thinking Mode) | 良好 | 131,072 |
| **DeepSeek: R1 0528 (free)** | 强大的 **逻辑推理** 和问题解决能力，性能与 OpenAI o1相当（开源）。 | 复杂的 **规划和调试** 、需要高准确度逻辑的 Agent 规划模式。 | **强** | 优秀 | 164,000 |
| **Qwen: Qwen3 Coder Plus (free)** | **专精于代码任务** ，高性能的 Coder 模型系列中的免费版本。 | 代码生成、代码审查、 **Web 开发** 脚本、技术文档撰写。 | 良好 | **优秀** (专精) | 128,000 |
| **NVIDIA: Nemotron Nano 9B V2 (free)** | NVIDIA的 **轻量级** 模型，具有良好的平衡性能，适合一般编码辅助。 | 快速的代码片段生成、轻量级脚本任务、一般性问答。 | 中等偏上 | 良好 | 128,000 |

### 针对您的需求总结推荐：

1. **端到端 Agent 自动化 (推理 & 逻辑规划)：**
	- 首选： **xAI: Grok 4 Fast (free)** 和 **DeepSeek: DeepSeek V3.1 (free)** 。
	- **Grok 4 Fast** 拥有巨大的 Context Window，适合处理涉及大量文件或信息的复杂端到端流程。
	- **DeepSeek V3.1** 在工具使用（Tool Use）和推理方面经过专门优化，非常适合作为 Agent 的核心决策引擎。
2. **编程与 Web 开发：**
	- 首选： **DeepSeek V3.1 (free)** 和 **Qwen: Qwen3 Coder Plus (free)** 。
	- DeepSeek系列在 **代码生成** 和 **Agentic Coding** 工作流中表现卓越。Qwen Coder系列则是专门为代码任务训练，可以作为代码生成阶段的有力补充。

> **提示：** 您的截图显示了 `Gemini 2.0 Flash Experimental (free)` ，它也是一个优秀的选择，其特点是 **速度快** 且拥有 **大规模上下文窗口** ，适合需要快速迭代和处理大量文本的 Agent 任务。

您对这些模型在您的 **"千锤百问"** 项目中如何分工，或者哪个模型更适合作为您 Obsidian 结合 Agent 的“大脑”有进一步的想法吗？