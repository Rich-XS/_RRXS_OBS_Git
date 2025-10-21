重装要点1. "everything 搜索 "
[!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)
[ClaudeCode（anyrouter）](ClaudeCode（anyrouter）.md)
[VSC_CCR 免费模型配置优化建议_Gemini](VSC_CCR%20免费模型配置优化建议_Gemini.md)
[OpenRouter 选型 Free models 10](OpenRouter%20选型%20Free%20models%2010.md)
以下是专为您的 **RRXS 千锤百问** 项目总结的 **《CCR Agent 灾难恢复与 $0 成本配置小白教程》**，确保您下次重装能够 **100% 成功**！




---

## 💡 **核心总结：故障与关键修复点**

在整个过程中，最关键的三个障碍点和解决方案如下：

| 阶段         | 错误现象                    | 根本原因                                                                                      | 最终解决方案                                                                           |
| ---------- | ----------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **程序崩溃**   | `500 ImageAgent` 错误     | **CCR 内部 Bug (Issue #820)**：`ImageAgent` 在初始化时崩溃，与配置无关。                                   | 重新全局安装 (`npm install -g...`) + **移除 `Router` 字段中的 `image` 路由** (虽然是 Bug，但移除能缓解)。 |
| **配置注入**   | `400 Missing model` 错误  | **JSON 语法错误**：手动编辑 `config.json` 时加入了 `//` 注释。                                            | **必须使用纯净 JSON 格式，JSON 文件中不允许任何注释**。                                              |
| **API 鉴权** | `401 User not found` 错误 | **API Key 不一致或不完整**：手动编辑和 UI 保存时，Key 在 `APIKEY` 和 `Providers.openrouter.api_key` 两个位置不一致。 | **API Key 必须粘贴到 `config.json` 中所有出现 `Key` 的位置，确保完全一致。**                          |

---

## 📘 **CCR Agent 重设终极指南 (开始启动 - #90EE90)**

本教程假设您已在 **VSCode 终端**中，处于您的工作区目录 `rrxsxyz_next` 下。

### 步骤 1: 彻底清理与重装
==**下面1.1 之后 用everything 全电脑搜索 claude-code-router, 确保清理, 其他的 Claude 或 anthropic 无关1
记得要清理系统里的环境变量-- 如果使用了AnyRouter的环境变量设置的话 [!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)**==
**中国用户：若慢，==用镜像 npm config set registry [https://registry.npmmirror.com](https://registry.npmmirror.com/)==**
npm install -g @anthropic-ai/claude-code

| 动作                  | 指令/代码                                           | 目的               |
| ------------------- | ----------------------------------------------- | ---------------- |
| **1.1 ==全局/环境清理**== | npm uninstall -g @musistudio/claude-code-router | 移除旧版程序，防止文件残留。   |
| **1.2 ==全局安装**==    | npm install -g @musistudio/claude-code-router   | 安装最新、干净的 CCR 版本。 |
|                     |                                                 |                  |
|                     |                                                 |                  |
|                     |                                                 |                  |
==**在项目目录下, 全局(非环境)安装**==
### 步骤 2: 启动 UI 接口并生成新配置

这是为了在 `C:\Users\rrxs\.claude-code-router` 路径下生成一个**干净的 `config.json` 文件**。
==**使用ccr ui 配置, 不要在 config.json自己填; 确认OpenRouter API是对的, 新设一个?**==

| 动作            | 指令/代码               | 目的                         |
| ------------- | ------------------- | -------------------------- |
| **2.1 启动 UI** | ==`ccr ui`==        | 启动服务，自动生成配置文件，并在浏览器中打开 UI。 |
| **2.2 停止服务**  | 在终端按 **`Ctrl + C`** | 停止 `ccr ui` 进程，准备手动配置。     |

JSON ==**不要用这个, 用 ui生成的**==
### 步骤 3: 注入 $0 成本配置与 Bug 绕过 **(进展 - #0000FF)**
这是整个流程中**最关键的步骤**，避免所有已知的配置 Bug。
1. **打开文件：** 导航至 `C:\Users\rrxs\.claude-code-router\config.json` 并打开。
2. **粘贴 Key：** 将您的 **完整的 OpenRouter Key** 粘贴到以下 **两个位置**：
    - `"APIKEY": "sk-or-v1-xxxxxxxxxxxxxxxxx"`
    - `"Providers"` 块中 `"api_key": "sk-or-v1-xxxxxxxxxxxxxxxxx"`
3. **覆盖 Router 配置：** 将整个 `Router` 部分替换为以下 $0 成本配置，并**确保其中没有 `//` 等注释符号**：
**==

==**路由**==

默认openrouter, anthropic/claude-3-haiku
后台openrouter, anthropic/claude-3-haiku 
思考openrouter, deepseek/deepseek-chat-v3.1:free
长上下文openrouter, google/gemini-2.5-pro-preview
上下文阈值: 60000
网络搜索openrouter, z-ai/glm-4.5-air:free
图像 (beta)openrouter, qwen/qwen2.5-vl-72b-instruct:free
强制使用图像代理

其他: 
qwen/qwen3-235b-a22b:free
qwen/qwen3-coder:free
deepseek/deepseek-chat-v3.1:free ?think?
google/gemini-2.0-flash-exp:free
google/gemini-2.5-flash-lite-preview-09-2025
google/gemini-2.0-flash-exp:free ?think?

4. **保存** 文件。
    

### 步骤 4: 启动服务与最终验证 **(收获 - #EAA200)**

| 动作               | 指令/代码                       | 目的              |
| ---------------- | --------------------------- | --------------- |
| **4.1 启动服务**     | `ccr restart` 或 `ccr start` | 启动 CCR 后台服务。    |
| **4.2 启动 Agent** | `ccr code`                  | 启动 Agent 终端。    |
| **4.3 最终验证**     | `hi`                        | 确认服务成功启动并能正常响应。 |

启动注意
==**/permissions -> add "acceptEdits",  shift+tab 设定授权状态**==
进入Think状态时 Deepseek:free没有调用功能, 需@background (Qwen3) tool-use
>>recap
>>record
>>archive
>>wrap-up
>>

==**【核心原则】**==
1.  **必须优先使用 $0 成本模型。**
2.  **必须严格遵循路由功能与模型兼容性，避免 Deepseek 的工具调用 Bug。**

**【路由使用规范】**
* **日常问答/简单分析 (`default`)：** 仅用于简单的聊天、问候、纯文本生成（如 Hook 文案），不涉及文件读取或代码操作。
* **编码/自动化/文件操作 (`@background`)：** 凡涉及 **`Read`、`Write`、`Bash` 或 `progress-recorder`** 等工具调用、代码生成、或文件内容分析的复杂任务，**必须强制使用 `@background` 路由** (Qwen3-Coder:free) 来启动任务。
* **高级策略 (`@think`)：** 用于纯粹的高级逻辑推理或策略制定（不涉及文件操作时）。如果需要同时进行策略制定和文件操作，**必须退回使用 `@background`**。

**【权限与安全】**
* Agent 必须确认已获得 **`acceptEdits`** 和 **`allow writes`** 权限，才能执行代码或文件修改操作。

> ==@background !请长期记忆 增加以下约束：凡涉及文件操作、代码执行或工具调用，必须使用 @background 路由，因 deepseek 模型不支持工具调用。==
---

### 🌟 **特殊问题与提示**

1. **VPN/网络问题 (401 错误)：** 如果再次遇到 `401 Unauthorized` 错误，请在 `ccr restart` 前**检查并稳定您的 VPN 连接** [cite: 2025-10-03]。
    
2. **Obsidian 同步问题 (OneDrive)：** 确保您的 `_RRXS_OBS` 库和 `rrxsxyz_next` 目录都设置了 **OneDrive 客户端的“始终保留在此设备上”** 选项，以避免同步延迟导致的文件读取错误。==**目前是没打开onedrive**==
    
3. **时间同步问题：** 虽然不是本次故障的原因，但在涉及 **VPN 跨境** 传输时，请确保您的 Windows 系统时间与实际时间（尤其是秒级）保持精确同步。==**node file-sync-json问题未解决**==



```
{
  "LOG": false,
  "LOG_LEVEL": "debug",
  "CLAUDE_PATH": "",
  "HOST": "127.0.0.1",
  "PORT": 3456,
  "APIKEY": "",
  "API_TIMEOUT_MS": "600000",
  "PROXY_URL": "",
  "transformers": [],
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "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",
      "models": [
        "google/gemini-2.5-pro-preview",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking",
        "qwen/qwen2.5-vl-72b-instruct:free",
        "x-ai/grok-4-fast:free",
        "z-ai/glm-4.5-air:free",
        "deepseek/deepseek-chat-v3.1:free",
        "qwen/qwen3-coder:free"
      ],
      "transformer": {
        "use": [
          "openrouter"
        ]
      }
    }
  ],
  "StatusLine": {
    "enabled": false,
    "currentStyle": "default",
    "default": {
      "modules": []
    },
    "powerline": {
      "modules": []
    }
  },
  "Router": {
    "default": "openrouter,x-ai/grok-4-fast:free",
    "background": "openrouter,qwen/qwen3-coder:free",
    "think": "openrouter,deepseek/deepseek-chat-v3.1:free",
    "longContext": "openrouter,x-ai/grok-4-fast:free",
    "longContextThreshold": 60000,
    "webSearch": "openrouter,z-ai/glm-4.5-air:free",
    "image": "openrouter,qwen/qwen2.5-vl-72b-instruct:free"
  },
  "CUSTOM_ROUTER_PATH": ""
}
```


## 您ClashVerge(==设置/端口设置==)启用了专用的 SOCKS 7898, (或 **HTTP(s) 代理端口 `7899`)，这使得==设置环境变量更加清晰和稳定==。

==记得要Clash Verge **关掉重新打开**==

## ==VSC+CCR 小白教程==：高效率稳定配置（最终方案与故障排除）

这份指南提供了从零到一实现 **VSC_CCA+CPG“双引擎”** 高效稳定工作流的详尽步骤。

### 第一部分：配置步骤（最终方案）

#### 步骤一：VSC 环境与 Manifest 提速

|实施内容|步骤|代码/文件路径|
|---|---|---|
|**安装组件**|确保已安装 **VSCode**、**Python/Venv**、**Node.js** 和 **CCR (Claude Code Router)**。|`npm install -g @musistudio/claude-code-router`|
|**项目文件提速**|在您的项目文件 **`Project.md`** 顶部，添加文件访问限制代码，消除 Agent 暴力搜索，降低 Token 成本。|**文件：** `rrxsxyz_next/Project.md` **代码：** `/allow_access progress.md` `/deny_access **/*`|
|**上下文阈值**|在 CCR UI 中，将**长上下文阈值**（LongContextThreshold）设置为 **`16000`**，进一步控制成本和速度。|**UI 位置：** 路由 > 长上下文 > 上下文阈值|

导出到 Google 表格

#### 步骤二：Clash Verge 代理配置（确认）

|实施内容|步骤|端口/协议|
|---|---|---|
|**代理端口**|确保 Clash Verge 中 **`Http(s)代理端口`** 已开启并记住端口号。|**`Http(s)代理端口`**：**`7899`**|

导出到 Google 表格

#### 步骤三：`config.json` 配置文件修改（永久生效）

请手动打开 **`C:\Users\rrxs\.claude-code-router\config.json`** 文件，进行以下关键修改。这是解决所有启动失败的**最终方案**。

|配置项|最终配置值|作用|
|---|---|---|
|**API Key**|`"api_key": "sk-or-v1-..."`|解决 CCR 服务启动时的凭证缺失问题。|
|**服务端口**|`"PORT": 5001`|解决本地端口冲突（原 `3456`），确保服务能启动并常驻。|
|**网络代理**|`"PROXY_URL": "http://127.0.0.1:7899"`|解决网络连接问题及底层协议解析错误。|

导出到 Google 表格

#### 步骤四：启动工作流

1. **保存** `config.json` 文件。
    
2. 在 VSC 终端中，**重启 CCR 服务**以加载新配置：
    
    PowerShell
    
    ```
    ccr restart
    ```
    
3. **确认状态**：使用 `ccr status` 确认显示 `✅ Status: Running`。
    
4. **运行任务**：
    
    PowerShell
    
    ```
    ccr code "进行 recap回顾"
    ```
    

---

### 第二部分：常见问题及故障排除（故障排除演进史）

| 常见问题              | 现象/报错                                             | 原因分析及**最终解决方案**                                                                                                                                                           |
| ----------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **服务启动失败**        | `Service startup timeout` 或 `Service not running` | **原因：** 服务进程启动时缺乏关键信息（API Key 或端口冲突）。 **最终解决：** 将 **API Key**、**PORT: 5001** 和 **PROXY_URL** 三项写入 **`config.json`** 实现持久化。                                                |
| **网络请求失败**        | 启动后报错 `UND_ERR_INVALID_ARG`                       | **原因：** `PROXY_URL` 字段使用的 **SOCKS 协议** (`socks5://127.0.0.1:7898`) 格式无法被 CCR 底层网络库正确解析。 **最终解决：** 协议切换为 **HTTP**。将 `PROXY_URL` 设置为 **`http://127.0.0.1:7899`**，解决了格式解析问题。 |
| **Token 消耗高/速度慢** | 任务执行前有大量文件搜索 (`Search(pattern: "server/**/*")`)   | **原因：** Agent 默认尝试加载整个项目的文件上下文。 **最终解决：** 在 **`Project.md`** 中添加 `/deny_access **/*` 限制文件访问，同时将**上下文阈值**降到 **16000**。                                                     |
| **模型使用疑虑**        | 任务日志中总是看到 DeepSeek 模型在运行，不见 Haiku                 | **原因：** DeepSeek 是您的 **`思考`** 模型，因为它设置为 **`free`**，CCR 优先用它进行成本最低的规划和分析。Haiku (`default`) 只在执行核心代码任务时才被调用。 **最终结论：** **配置完美生效**，成本控制到位。                                   |
       

### CCR指令 
---

```

## CCR指令 Usage: ccr [command]

Commands:
  start         Start server 
  stop          Stop server
  restart       Restart server
  status        Show server status
  statusline    Integrated statusline
  code          Execute claude command
  ui            Open the web UI in browser
  -v, version   Show version information
  -h, help      Show help information

Example:
  ccr start
  ccr code "Write a Hello World"
  ccr ui