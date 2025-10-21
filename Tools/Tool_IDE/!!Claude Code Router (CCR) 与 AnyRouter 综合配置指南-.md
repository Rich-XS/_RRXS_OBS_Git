# 

## 核心概念

**CCR (Claude-Code-Router)** 是一个强大的CLI工具，允许您通过路由机制在不同AI模型间智能切换，特别适合需要$0成本模型的开发场景。它与 **AnyRouter** 服务结合使用，可访问多种免费模型，包括Claude、Gemini、Qwen等。

## 基础配置流程

### 1. 环境准备

- **安装Node.js** (v18+):
  ```bash
  # 中国用户推荐使用镜像
  npm config set registry https://registry.npmmirror.com
  ```

- **安装CCR**:
  ```bash
  npm uninstall -g @musistudio/claude-code-router  # 先清理旧版本
  npm install -g @musistudio/claude-code-router    # 安装最新版
  ```

### 2. AnyRouter 配置

- **获取API Token**:
  1. 访问 [AnyRouter控制台](https://anyrouter.top/console)
  2. 生成新Token (格式: `sk-or-v1-...`)

- **设置环境变量**:
  ```bash
  # 临时设置 (当前终端会话)
  export ANTHROPIC_AUTH_TOKEN="sk-or-v1-..."
  export ANTHROPIC_BASE_URL="https://pmpjfbhq.cn-nb1.rainapp.top"  # 中国优化URL
  
  # 永久设置 (推荐)
  echo 'export ANTHROPIC_AUTH_TOKEN="sk-or-v1-..."' >> ~/.zshrc
  echo 'export ANTHROPIC_BASE_URL="https://pmpjfbhq.cn-nb1.rainapp.top"' >> ~/.zshrc
  source ~/.zshrc
  ```

### 3. CCR 配置与启动

- **生成配置文件**:
  ```bash
  ccr ui  # 启动UI生成配置
  # 在浏览器中完成基本配置后，按Ctrl+C停止
  ```

- **关键配置项** (编辑 `~/.claude-code-router/config.json`):
  ```json
  {
    "APIKEY": "sk-or-v1-...",
    "Providers": [
      {
        "name": "openrouter",
        "api_key": "sk-or-v1-...",
        "models": [
          "google/gemini-2.5-pro-preview",
          "anthropic/claude-3.5-sonnet",
          "qwen/qwen2.5-vl-72b-instruct:free",
          "deepseek/deepseek-chat-v3.1:free",
          "qwen/qwen3-coder:free"
        ]
      }
    ],
    "Router": {
      "default": "openrouter,anthropic/claude-3-haiku",
      "background": "openrouter,qwen/qwen3-coder:free",
      "think": "openrouter,deepseek/deepseek-chat-v3.1:free",
      "longContext": "openrouter,google/gemini-2.5-pro-preview",
      "longContextThreshold": 60000,
      "webSearch": "openrouter,z-ai/glm-4.5-air:free",
      "image": "openrouter,qwen/qwen2.5-vl-72b-instruct:free"
    }
  }
  ```

- **启动服务**:
  ```bash
  ccr restart
  ccr code
  ```

## $0 成本模型使用规范

### 路由使用策略

| 路由类型 | 推荐模型 | 适用场景 | 关键约束 |
|---------|---------|---------|---------|
| **default** | `anthropic/claude-3-haiku` | 简单聊天、纯文本生成 | 不涉及文件操作 |
| **@background** | `qwen/qwen3-coder:free` | **文件操作、代码执行、工具调用** | 必须用于所有涉及`Read`/`Write`/`Bash`的任务 |
| **@think** | `deepseek/deepseek-chat-v3.1:free` | 纯逻辑推理 | 不涉及文件操作时使用 |
| **长上下文** | `google/gemini-2.5-pro-preview` | 大文件分析 | 上下文阈值: $$60000$$ tokens |

> **核心原则**: 凡涉及文件操作、代码执行或工具调用，**必须**使用 `@background` 路由，因为 Deepseek 模型不支持工具调用。

### 权限设置

- 在CCR中必须启用:
  - `acceptEdits`
  - `allow writes`
  
  通过 `/permissions` 命令添加，使用 `Shift+Tab` 设定授权状态

## 记忆Agent配置 (Progress Recorder)

为解决AI Coding过程中"丢需求"问题，可配置记忆Agent:

### 配置步骤

1. **创建记忆文件**:
   ```bash
   mkdir -p .claude/agents
   touch .claude/agents/progress-recorder.md
   ```

2. **添加记忆规则**:
   ```markdown
   [项目记忆规则]
   - **必须主动调用** progress-recorder agent 记录关键决策
   - 检测到以下情况时**自动触发**:
     - "决定使用/最终选择/将采用"等决策语言
     - "必须/不能/要求"等约束语言
     - "完成了/实现了/修复了"等完成标识
     - "需要/应该/计划"等新任务
   ```

3. **常用命令**:
   - `>>record` - 执行增量合并任务
   - `>>archive` - 执行快照归档
   - `>>recap` - 回顾项目状态
   - `>>wrap-up` - 生成项目总结

### 工作流程

1. 当CCR Agent做出重要决策时，自动触发 `>>record`
2. 系统将关键信息结构化写入 `progress.md`
3. 当记录超过100条时，使用 `>>archive` 归档到 `progress.archive.md`
4. 通过 `>>recap` 快速回顾项目状态

## 常见问题解决方案

| 问题现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| `500 ImageAgent` 错误 | CCR内部Bug (Issue #820) | 重新全局安装 + **移除Router中的image路由** |
| `400 Missing model` 错误 | JSON语法错误(含注释) | **必须使用纯净JSON，禁止//注释** |
| `401 User not found` 错误 | API Key不一致 | **确保API Key在config.json所有位置完全一致** |
| 网络连接问题 | 区域网络限制 | 使用备用URL: `https://pmpjfbhq.cn-nb1.rainapp.top` |
| Deepseek无法调用工具 | 模型限制 | **涉及文件操作必须使用@background路由** |

## 最佳实践

1. **重装清理要点**:
   - 使用Everything搜索 `claude-code-router` 彻底清理
   - 检查并清理系统环境变量
   - 确保OneDrive设置"始终保留在此设备上"

2. **VSCode集成**:
   - 安装Continue扩展增强体验
   - 配置MCP (Model Context Protocol) 工具
   - 推荐安装8个免费MCP: GitHub、Context7、Serena、ChromeDevTools、Firecrawl、Notion、Microsoft Learn、Playwright

3. **模型选择策略**:
   - 日常简单任务: `claude-3-haiku`
   - 代码生成/文件操作: `qwen/qwen3-coder:free`
   - 长文本分析: `google/gemini-2.5-pro-preview`
   - 图像处理: `qwen/qwen2.5-vl-72b-instruct:free`

> **重要提示**: 中国用户遇到网络问题时，优先使用备用URL `https://pmpjfbhq.cn-nb1.rainapp.top` 并确保稳定VPN连接。



## 💡 OpenRouter 低成本 CCR ==%% 模型选择 %%==推荐 Top 5

| 排名    | 模型名称 (ID)                                         | 建议 CCR 路由                     | Input ($/1M tokens) | 上下文 (tokens)  | 综合打分 (满分 110) | 建议权重 (%) |
| ----- | ------------------------------------------------- | ----------------------------- | ------------------- | ------------- | ------------- | -------- |
| **1** | **Qwen3 Coder 480B A35B (free)**                  | **Default / Think (高阶代码)**    | **$0**              | 262,144       | **103**       | **35%**  |
| **2** | **Z.AI: GLM 4.5 Air (free)**                      | **Default / Background (工具)** | **$0**              | 131,072       | **100**       | **30%**  |
| **3** | **Tongyi DeepResearch 30B A3B (free)**            | **Think (规划/研究)**             | **$0**              | 131,072       | **95**        | **15%**  |
| **4** | **Google: Gemini 2.5 Flash Lite Preview 09-2025** | **LongContext (知识库)**         | $0.10               | **1,048,576** | **90**        | **15%**  |
| **5** | **Mistral Small 3.2 24B (free)**                  | **Background (稳定备份)**         | **$0**              | 131,072       | **90**        | **5%**   |

"Router": { // 免费代码主力：解决您的 ccr code 任务 "default": "openrouter,qwen/qwen3-coder:free", // 免费 Agent 备份/工具执行：解决一般 Agent 任务 "background": "openrouter,z-ai/glm-4.5-air:free", // 免费规划/研究 Agent：解决 DeepSeek 的工具调用错误 "think": "openrouter,alibaba/tongyi-deepresearch-30b-a3b:free", // 付费长上下文：处理大文件和知识库 "longContext": "openrouter,google/gemini-2.5-flash-lite-preview-09-2025", "longContextThreshold": 600000, // 免费 Agent 搜索：利用 GLM-4.5 Air 的 Agent 能力 "webSearch": "openrouter,z-ai/glm-4.5-air:free", // 免费多模态：处理图像/图表任务 "image": "openrouter,qwen/qwen2.5-vl-72b-instruct:free"
![](!!Claude%20Code%20Router%20(CCR)%20与%20AnyRouter%20综合配置指南--20251006215423172.png)>>>>![](!!Claude%20Code%20Router%20(CCR)%20与%20AnyRouter%20综合配置指南--20251006233441602.png)






## 相关资源

- [[!!CCR (Claude-Code-Router)]]
- [[!VSCode 重装后配置 Anyrouter Claude Code URL 的详细步骤指导]]
- [[!我给 Claude Code 装了个记忆Agent，让你在AI Coding 时不再丢需求]]
- [[!!AnyRouter.Top MasterFile]]

通过以上配置，您将拥有一个稳定、高效且成本优化的AI编程环境，特别适合RRXS千锤百问项目中的"第二大脑+手和脚"实现目标。