---
epoch: 1759146208195
modelKey: x-ai/grok-4-fast:free|openrouterai
topic: "Update Anyrouter Claude URL in VSCode"


tags:
  - copilot-conversation
---

**user**: 如何在VScode里更新 Anyrouter的claude code url
[Timestamp: 2025/09/29 19:43:28]

**ai**: ### 在 VSCode 中更新 Anyrouter 的 Claude Code URL

根据您的查询，您想在 VSCode 中更新 Anyrouter 的 Claude Code 配置中的 URL（即 `ANTHROPIC_BASE_URL`）。Anyrouter 的默认 API 地址是 `https://anyrouter.top`，但如果需要优化（如针对中国大陆网络），可以切换到备用端点 `https://pmpjfbhq.cn-nb1.rainapp.top`。Claude Code 是一个 CLI 工具（通过 npm 安装），在 VSCode 中运行时，主要依赖环境变量配置。下面是详细步骤，确保您已安装 Node.js 和 Claude Code（参考笔记中的安装指南）。

#### 1. **确认前提条件**
   - 已安装 Claude Code：运行 `npm install -g @anthropic-ai/claude-code` 和 `claude --version` 检查。
   - 已获取 Anyrouter 的 API Token（以 `sk-` 开头），从 Anyrouter 控制台的 “API 令牌” 页面获取。
   - 在 VSCode 中打开您的项目文件夹（`File > Open Folder`），并使用集成终端（`Ctrl + `` 或 `View > Terminal`）。

#### 2. **更新环境变量（推荐方式：临时或永久设置）**
   Claude Code 通过环境变量 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL` 读取配置。在 VSCode 的集成终端中更新这些变量即可生效。

   - **临时更新（仅当前终端会话）**：
     在 VSCode 集成终端中运行以下命令（替换 `sk-...` 为您的实际 Token）：
     ```bash
     export ANTHROPIC_AUTH_TOKEN=sk-您的实际Token
     export ANTHROPIC_BASE_URL=https://pmpjfbhq.cn-nb1.rainapp.top  # 或保持 https://anyrouter.top
     claude
     ```
     - 这会启动 Claude Code，使用新 URL。
     - 如果遇到网络问题（如 Fetch failed），优先用备用 URL `https://pmpjfbhq.cn-nb1.rainapp.top`。

   - **永久更新（全局环境变量，推荐避免重复输入）**：
     将环境变量添加到您的 shell 配置文件（如 `~/.bash_profile`、`~/.bashrc` 或 `~/.zshrc`，取决于您的 shell）。在 VSCode 终端中编辑：
     ```bash
     # 编辑配置文件（例如使用 nano 或 vim）
     nano ~/.zshrc  # macOS/Linux 默认用 zsh；Windows 用 ~/.bash_profile
     ```
     在文件末尾添加：
     ```bash
     export ANTHROPIC_AUTH_TOKEN=sk-您的实际Token
     export ANTHROPIC_BASE_URL=https://pmpjfbhq.cn-nb1.rainapp.top  # 更新为备用 URL
     ```
     保存后，重启 VSCode 或运行 `source ~/.zshrc` 生效。然后在项目文件夹中运行 `claude` 即可。

#### 3. **在 VSCode 中集成和测试**
   - **启动 Claude Code**：
     - 在 VSCode 终端中，进入项目目录：`cd your-project-folder`。
     - 运行 `claude`。
     - 首次运行会提示选择主题、安全须知、终端配置和工作目录信任，按 Enter 确认。
   
   - **如果使用 VSCode 扩展**（如果您安装了 Claude 相关的 VSCode 插件，如 Continue 或其他 AI 助手）：
     - 打开 VSCode 设置（`Ctrl + ,`），搜索 “Anthropic” 或 “Claude”。
     - 在 `settings.json` 中添加自定义配置（通过 `File > Preferences > Settings > Open Settings (JSON)`）：
       ```json
       {
         "anthropic.apiKey": "sk-您的实际Token",
         "anthropic.baseUrl": "https://pmpjfbhq.cn-nb1.rainapp.top"  // 更新 URL
       }
       ```
     - 重启 VSCode，测试 AI 功能（如代码补全）。

   - **常见问题排查**：
     - **Invalid API Key**：检查 Token 是否正确设置（运行 `echo $ANTHROPIC_AUTH_TOKEN` 验证）。
     - **Offline 或 Fetch failed**：确保网络代理正常（Claude Code 需要国际连接判断网页）。用备用 URL 重试，或退出重启 `claude`。
     - **无法访问**：Anyrouter 可能有网络优化问题，参考笔记中的 FAQ。多重试，或检查 Anyrouter 系统公告。
     - 如果 VSCode 终端不识别环境变量，确保 VSCode 使用正确的 shell（设置中搜索 “terminal.integrated.defaultProfile”）。

#### 4. **注意事项**
   - Anyrouter 的 Claude Code 支持仅限特定模型（如 sonnet[1m]），更新 URL 后可使用 `/model sonnet[1m]` 开启 1M 上下文。
   - 如果您是 OpenAI Codex 用户，配置不同（用 `~/.codex/config.toml` 中的 `base_url = "https://anyrouter.top/v1"` 更新）。
   - 余额和使用：监控 Anyrouter 控制台（https://anyrouter.top/console），每日签到可获赠额度。
   - 如遇 API 错误，参考笔记 FAQ 或邮件反馈 anyrouter.top@gmail.com。

如果这些步骤后仍有问题，请提供更多细节（如错误消息或您的操作系统），我可以进一步帮助！
[Timestamp: 2025/09/29 19:45:33]