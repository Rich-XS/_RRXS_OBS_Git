
[!!CCR (Claude-Code-Router)](!!CCR%20(Claude-Code-Router).md)

|     |             |          |                   |              |              |                |                  |                                 |                       |       |
| --- | ----------- | -------- | ----------------- | ------------ | ------------ | -------------- | ---------------- | ------------------------------- | --------------------- | ----- |
| w   | 配置维度        | 核心任务     | Input/Output (模态) | ContextLen   | Prompt $     | Supp-Para (工具) | Provider/Series  | **优选模型 (FREE) !**               | 备选模型 (低成本/稳定)         | 模型额度? |
| w=5 | LongContext | 归档/Recap | Text !            | 极高 (>100K) ! | FREE ! 或 <$1 | N/A            | Google/Anthropic | **Gemini 2.0 Flash Exp (free)** | Claude 3 Haiku        |       |
| w=4 | Default     | 高频主力     | Text !            | 中等 (32K+)    | FREE !       | N/A            | DeepSeek         | **DeepSeek V3.1 (free)**        | z-ai/glm-4.5-air:free |       |
| w=4 | Think       | 流程规划     | Text !            | 中等 (32K+)    | <$0.5 !      | N/A            | GLM/Claude       | **GLM 4.5 Air (free)**          | Claude 3 Haiku        |       |
| w=3 | Background  | 后台 I/O   | Text !            | 中等 (32K+)    | FREE !       | N/A            | DeepSeek         | **DeepSeek V3.1 (free)**        | z-ai/glm-4.5-air:free |       |
| w=3 | WebSearch   | 信息调研     | Text !            | 中等 (32K+)    | FREE !       | tools !        | GLM              | **GLM 4.5 Air (free)**          | N/A                   |       |
| w=2 | Image       | 多模态分析    | Text+Image !      | 高 (64K+)     | FREE !       | N/A            | Qwen             | **Qwen 2.5-VL-72B (free)**      | N/A                   |       |
![](Pasted%20image%2020251004135604.png)>>>![](Pasted%20image%2020251004135837.png)

**查找并修改配置块：**

- 在 `settings.local.json` 文件中，找到模型配置块：`"claudeCode.modelConfiguration": { ... }`。
    
- 您的 UI 配置已经自动写入了大部分设置，现在您只需在代码块内**补充**以下这一行：
    

JSON

```
// ... 其他模型设置 (UI已写入) ...

// 核心补充：w=5 LongContext 的备用模型（稳定且低成本的 Haiku）
"longContextFallback": "openrouter,anthropic/claude-3-haiku", 

// ... 确保大括号 } 匹配完整 ...
```
更新后为
```
{
    // --- 权限设置（保留您现有的） ---
    "permissions": {
        "allow": [
            "allow writes"
        ],
        "deny": [],
        "ask": []
    },

    // --- 核心模型配置覆盖（强制本地生效） ---
    // 仅列出 LongContext 和 Fallback，以最简洁的方式强制覆盖全局错误配置
    "claudeCode.modelConfiguration": {
        // 主选模型 (w=5 核心): 免费超长上下文模型
        "longContext": "openrouter,google/gemini-2.0-flash-exp:free",
        // 长上下文触发阈值：UI中设置的 64000
        "longContextThreshold": 64000, 
        // 备选模型 (w=5 保险): 低成本、高稳定性的 Claude 3 Haiku
        "longContextFallback": "openrouter,anthropic/claude-3-haiku"
    }
}
```

==**json文件不支持标识, 改名为 jsonc**==
- 在 **VS Code 的文件资源管理器**中，找到您的目标文件（例如 `settings.local.json`）。 
- **右键点击**该文件，选择 **`Rename` (重命名)**。
- 将文件扩展名从 `.json` 改为 **`.jsonc`**。

类似的, ## `_RRXS_OBS` 的 `settings.local.json` 是否需要相同配置？**不需要完全相同，但需要覆盖 LongContext 的配置**
```
{
    // --- 权限设置（保留您现有的） ---
    "permissions": {
        "allow": [
            "Bash(mkdir:*)"
        ],
        "deny": [],
        "ask": []
    },

    // --- 仅 LongContext 覆盖：保护 Obsidian 库的长文本处理 ---
    // 强制使用 LongContext 策略，确保长笔记归档稳定且成本受控。
    "claudeCode.modelConfiguration": {
        // 主选模型 (w=5): 免费超长上下文模型
        "longContext": "openrouter,google/gemini-2.0-flash-exp:free",
        // 长上下文触发阈值：UI中设置的 64000
        "longContextThreshold": 64000, 
        // 备选模型 (w=5 保险): 低成本、高稳定性的 Claude 3 Haiku
        "longContextFallback": "openrouter,anthropic/claude-3-haiku"
    }
}
```
>> **==之后再 局部环境下运行==**


xAI: Grok 4 Fast (free) | x-ai/grok-4-fast:free
DeepSeek: DeepSeek V3.1 (free) | deepseek/deepseek-chat-v3.1:free
Z.AI: GLM 4.5 Air (free) | z-ai/glm-4.5-air:free
TNG: DeepSeek R1T2 Chimera (free) | tngtech/deepseek-r1t2-chimera:free
Microsoft: MAI DS R1 (free) | microsoft/mai-ds-r1:free
Qwen: Qwen3 Coder 480B A35B (free) | qwen/qwen3-coder:free
Qwen: Qwen3 235B A22B (free) | qwen/qwen3-235b-a22b:free
Google: Gemini 2.0 Flash Experimental (free) | google/gemini-2.0-flash-exp:free
Meta: Llama 3.3 70B Instruct (free) | meta-llama/llama-3.3-70b-instruct:free
OpenAI: gpt-oss-20b (free) | openai/gpt-oss-20b:free

Qwen: Qwen2.5 VL 72B Instruct (free) | qwen/qwen2.5-vl-72b-instruct:free



## Openrouter 免费模型匹配适配

| 路由选项 (Routing Option) | 推荐模型 (Recommended Model)              | 模型 ID (Model ID)                       | 推荐原因与能力侧重                                                                                      |
| --------------------- | ------------------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 默认 (Default)          | Google: Gemini 2.0 Flash Experimental | google/gemini-2.0-flash-exp:free       | 速度快，通用性强，知识面广。 适合绝大多数日常提问、信息检索和快速对话。                                                           |
| 后台 (Backend)          | Meta: Llama 3.3 70B Instruct          | meta-llama/llama-3.3-70b-instruct:free | 大参数量，综合性能优秀。 适合用于内容生成、逻辑梳理和复杂的长文本处理，作为“默认”模型的后备保障。                                             |
| 思考 (Reflection)       | DeepSeek: DeepSeek V3.1 (free)        | deepseek/deepseek-chat-v3.1:free       | 中文理解与推理能力突出。 适合用于“思考”环节，生成高质量的逻辑链（CoT）或结构化分析，特别是对于您的“千锤百问”项目。                                  |
| 上下文 (Context)         | xAI: Grok 4 Fast (free)               | x-ai/grok-4-fast:free                  | 速度快，上下文处理效率高。 能够快速处理长上下文，保持对话连贯性，并保证默认路由的速度优势。                                                 |
| 网络搜索 (Web Search)     | Z.AI: GLM 4.5 Air (free)              | z-ai/glm-4.5-air:free                  | 新兴模型，信息检索整合能力突出。 适合处理需要实时信息查询的任务。或者，如果界面允许，选择一个专门用于搜索的模型（如DeepSeek或Gemini Flash，如果不能重复选，选GLM）。 |
| 图像 (beta) (Image)     | Qwen: Qwen2.5 VL 72B Instruct         | qwen/qwen2.5-vl-72b-instruct:free      | 视觉理解(VL)专精模型。 Qwen系列在多模态方面有良好口碑，该模型就是针对视觉任务设计的。                                                |
| 上下文阈值 (Context Value) | 60000                                 | N/A                                    | 保持默认。 这是一个较高的数值，适合处理您在Obsidian和VSCode中整理的笔记和项目文档，确保上下文记忆能力足够强大。                                |
|                       |                                       |                                        |                                                                                                |


## 日常操作功能模型多维度推荐（免费/高性价比）

| 功能维度 (Function/Modality)                  | 适用您的项目/日常操作 (Context: RRXS/Obsidian/VScode)                      | Top 1 推荐模型 (评分 9.0+)                        | Top 2 推荐模型 (评分 8.5+)                      | Top 3 推荐模型 (评分 8.0+)              |
| ----------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------- | --------------------------------- |
| **1. 编码/代码分析** (Coding/Refactoring)       | **核心：** VScode中自动化和代理（'CC'）的代码生成、bug修复、文档生成。                     | **DeepSeek-Coder V2** (开放源码/API)            | **Qwen3 Coder** (开放源码/API)                | **Gemini 2.5 Pro** (长上下文/API)     |
| **2. 逻辑思考/推理** (Complex Reasoning/CoT)    | **核心：** '思考'路由、'progress-recorder'的`wrap-up`分析、**RRXS**方法论的系统规划。 | **DeepSeek V3.1** (免费/API)                  | **Claude 3.5 Sonnet** (部分免费/API)          | **Gemini 2.5 Flash** (免费/API)     |
| **3. 内容文案/生成** (Long-Form Writing)        | **核心：** 小红书/公众号文章生成（z6风格），基于Obsidian笔记的`recap`总结。                | **Meta Llama 3.3 70B Instruct** (免费/开放)     | **GLM 4.5 Air** (免费/API)                  | **Claude 3 Haiku** (速度快/API)      |
| **4. 图像识别/理解** (Image Analysis/OCR)       | **核心：** 理解爆款配图、分析流程截图、从图表中提取数据。                                  | **Qwen2.5 VL 72B Instruct** (免费/开放)         | **Grok-1.5V** (X-AI/多模态)                  | **Gemini 2.5 Flash** (原生多模态)      |
| **5. 快速检索/问答** (Fast Q&A/Search)          | **核心：** '默认'路由、临时信息查询、Obsidian库内RAG查询。                           | **Gemini 2.0 Flash Experimental** (免费/API)  | **xAI: Grok 4 Fast** (免费/API)             | **Mistral 7B Instruct** (开放/本地部署) |
| **6. 语音识别/转录** (Speech-to-Text)           | **核心：** 会议录音、想法口述的快速转录（Obsidian笔记输入）。                            | **OpenAI Whisper** (开放源码)                   | **Google Speech-to-Text (Cloud)** (免费额度)  | **FunASR** (阿里/开放/中文优化)           |
| **7. 营销文案/钩子** (Hook/Short Content)       | **核心：** 短视频**≤20秒**文案、标题**≤12字**、小红书标题**≤20字**。                  | **GPT-4o mini** (速度/简洁/API)                 | **Claude 3 Haiku** (响应速度)                 | **Llama 3 8B Instruct** (精简高效)    |
| **8. 角色扮演/模拟** (Role-playing/Simulation)  | **核心：** '9魔法模式'应用（专家/导师/教练），模拟用户画像。                              | **Claude 3.5 Sonnet** (API/角色稳定性高)          | **Meta Llama 3.3 70B Instruct** (开放/人设稳定) | **DeepSeek V3.1** (中文理解佳)         |
| **9. 视频/长文本摘要** (Video/Long Text Summary) | **核心：** 总结外部教程链接、整理长篇`archive`文件、视频学习笔记。                         | **Gemini 2.5 Pro** (长上下文/API)               | **Claude 3.5 Sonnet** (长上下文/API)          | **Mixtral 8x7B** (MoE/效率高)        |
| **10. 图像生成** (Text-to-Image)              | **核心：** 为内容配图（生活化氛围图/专业图表）、品牌识别码的素材创作。                           | **Stable Diffusion XL (SDXL)** (开放源码/本地/免费) | **DALL-E 3** (API/付费, 结构化好)               | **Midjourney** (订阅/质量             |