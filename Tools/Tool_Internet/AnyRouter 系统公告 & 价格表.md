##### 系统公告

  

**🚀快速开始**

  
  

**点击右上角 系统公告🔔 可再次查看 ｜ 完整内容可参考[使用文档](https://docs.anyrouter.top/)**

  
  
❗️提示  
  
[2025/09/30] Claude Sonnet 4.5 模型现已发布，使用 npm i -g @anthropic-ai/claude-code 更新最新版本 Claude Code 并使用 /model 选择 sonnet 4.5 体验最新模型  
  
[2025/07/27] 本站目前试验性开放邮箱登录，为防止滥用，当前仅允许 *.edu.cn 后缀邮箱注册，发送邮件可能有一定的延迟，也可能被识别为垃圾邮件，请注意检查  
  
[2025/07/16] 由于持续遭受攻击，本站停止服务一天，请关注后续通知。另外本站从未官方或授权其他人建立群聊、发布教程等，除官网所示备用 API 域名外也没有建立其他 AnyRouter 或近似名称的镜像站，请注意避免受到欺骗  
  
[2025/07/15] 此前的封禁中有一条错误的规则导致很多用户正常通过 GitHub 登录会遭遇封禁，现在已经找到了问题并进行了修复，烦请各位用户通过自助解封功能恢复账号，造成不便敬请谅解  
  
[2025/07/15] 根据启发式规则封禁了部分用户。后续将提供自助解除封禁的功能，目前管理员无法对所有此类邮件进行回复，请耐心等待  
  
[2025/07/15] 本站日前遭遇了大量攻击和滥用。为保障服务质量，本站暂时停止来自 Github 账号的新用户注册；来自 Linux Do 账号的注册以及所有已注册用户的登录均不受影响。

  
  
1️⃣ 安装 Node.js（已安装可跳过）  
  
确保 Node.js 版本 ≥ 18.0

```bash
# Ubuntu / Debian 用户
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo bash -
sudo apt-get install -y nodejs
node --version

# macOS 用户
sudo xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install node
node --version
```

  
  
2️⃣ 安装 Claude Code  
  

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

  
  
3️⃣ 开始使用  
  

- **获取 Auth Token：** `ANTHROPIC_AUTH_TOKEN` ：注册后在 `API令牌` 页面点击 `添加令牌` 获得（以 `sk-` 开头）
    - 名称随意，额度建议设为无限额度，其他保持默认设置即可

  

- **API地址：** `ANTHROPIC_BASE_URL`：`https://anyrouter.top` 是本站的 API 服务地址，**与主站地址相同**

  
在您的项目目录下运行：  

```bash
cd your-project-folder
export ANTHROPIC_AUTH_TOKEN=sk-... 
export ANTHROPIC_BASE_URL=https://anyrouter.top
claude
```

  
运行后

- 选择你喜欢的主题 + Enter
- 确认安全须知 + Enter
- 使用默认 Terminal 配置 + Enter
- 信任工作目录 + Enter

  
开始在终端里和你的 AI 编程搭档一起写代码吧！🚀

  
  

4️⃣ 配置环境变量（推荐）  
  
为避免每次重复输入，可将环境变量写入 bash_profile 和 bashrc：  

```bash
echo -e '\n export ANTHROPIC_AUTH_TOKEN=sk-...' >> ~/.bash_profile
echo -e '\n export ANTHROPIC_BASE_URL=https://anyrouter.top' >> ~/.bash_profile
echo -e '\n export ANTHROPIC_AUTH_TOKEN=sk-...' >> ~/.bashrc
echo -e '\n export ANTHROPIC_BASE_URL=https://anyrouter.top' >> ~/.bashrc
echo -e '\n export ANTHROPIC_AUTH_TOKEN=sk-...' >> ~/.zshrc
echo -e '\n export ANTHROPIC_BASE_URL=https://anyrouter.top' >> ~/.zshrc
```

  
重启终端后，直接使用：  

```bash
cd your-project-folder
claude
```

  
即可使用 Claude Code

  
  

💡 OpenAI Codex 使用方式  
  
1️⃣ 安装 Node.js  
  
与 Claude Code 步骤 1️⃣ 相同  
  
2️⃣ 安装 codex  
  

```bash
npm i -g @openai/codex
codex --version
```

  
  
3️⃣ 开始使用  
  

- **获取 Auth Token：** 注册后在 `API令牌` 页面点击 `添加令牌` 获得（以 `sk-` 开头）
    - 名称随意，额度建议设为无限额度，其他保持默认设置即可  
          
        
- 创建 `~/.codex/config.toml` 文件，并添加如下配置：

```toml
model = "gpt-5-codex"
model_provider = "anyrouter"
preferred_auth_method = "apikey"


[model_providers.anyrouter]
name = "Any Router"
base_url = "https://anyrouter.top/v1"
wire_api = "responses"
```

- 创建 `~/.codex/auth.json` 文件，并添加如下配置：

```json
{
  "OPENAI_API_KEY":"这里换成你申请的 KEY"
}
```

  
  
⚠️ 上述配置文件的路径 `~/.codex` 也可以用 `CODEX_HOME` 环境变量指定  
  
在您的项目目录下运行：  

```bash
cd your-project-folder
codex
```

  
  

❓FAQ  
  

- 本站直接接入官方 Claude Code 转发，无法转发非 Claude Code 的 API 流量  
      
    
- 如遇 API 报错，可能是转发代理不稳定导致，可以考虑退出 Claude Code 重试几次  
      
    
- 如果网页遇到登录错误可以尝试清除本站的 Cookie，重新登录  
      
    
- `Invalid API Key · Please run /login` 怎么解决？这表明 Claude Code 没有检测到 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL` 环境变量，检查环境变量是否配好。  
      
    
- 显示 `offline` 是什么原因？Claude Code 会通过检查是否能连接到 Google 来对网络进行判断。显示 `offline` 并不影响正常使用 Claude Code，只是表明 Claude Code 未能连接 Google。  
      
    
- 为什么浏览网页的 Fetch 会失败？这是因为 Claude Code 在访问网页前会调用 Claude 的服务来判断网页是否可以访问。需要保持国际互联网连接并进行全局代理，才可以访问 Claude 判断网页是否可以访问的服务。  
      
    
- 为什么请求总是显示 fetch failed？可能是因为所在地区的网络环境导致的，可以尝试使用代理工具或者使用备用 API 端点 `ANTHROPIC_BASE_URL=https://pmpjfbhq.cn-nb1.rainapp.top`



# 价格表
| 可用性 | 模型名称 | 计费类型 | 可用分组 | 倍率 | 模型价格 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | `gpt-5-codex` | 按量计费 | `default` | 模型倍率: 0.625<br>补全倍率: 8<br>分组倍率: 1 | 提示 $1.250 / 1M tokens<br>补全 $10.000 / 1M tokens |
| ✅ | `claude-3-5-haiku-20241022` | 按量计费 | `default` | 模型倍率: 0.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $1.000 / 1M tokens<br>补全 $5.000 / 1M tokens |
| ✅ | `claude-3-5-sonnet-20241022` | 按量计费 | `default` | 模型倍率: 1.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $3.000 / 1M tokens<br>补全 $15.000 / 1M tokens |
| ✅ | `claude-3-7-sonnet-20250219` | 按量计费 | `default` | 模型倍率: 1.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $3.000 / 1M tokens<br>补全 $15.000 / 1M tokens |
| ✅ | `claude-haiku-4-5-20251001` | 按量计费 | `default` | 模型倍率: 0.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $1.000 / 1M tokens<br>补全 $5.000 / 1M tokens |
| ✅ | `claude-opus-4-1-20250805` | 按量计费 | `default` | 模型倍率: 7.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $15.000 / 1M tokens<br>补全 $75.000 / 1M tokens |
| ✅ | `claude-opus-4-20250514` | 按量计费 | `default` | 模型倍率: 7.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $15.000 / 1M tokens<br>补全 $75.000 / 1M tokens |
| ✅ | `claude-sonnet-4-20250514` | 按量计费 | `default` | 模型倍率: 1.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $3.000 / 1M tokens<br>补全 $15.000 / 1M tokens |
| ✅ | `claude-sonnet-4-5` | 按量计费 | `default` | 模型倍率: 1.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $3.000 / 1M tokens<br>补全 $15.000 / 1M tokens |
| ✅ | `claude-sonnet-4-5-20250929` | 按量计费 | `default` | 模型倍率: 1.5<br>补全倍率: 5<br>分组倍率: 1 | 提示 $3.000 / 1M tokens<br>补全 $15.000 / 1M tokens |
| ✅ | `gemini-2.5-pro` | 按量计费 | `default` | 模型倍率: 0.625<br>补全倍率: 8<br>分组倍率: 1 | 提示 $1.250 / 1M tokens<br>补全 $10.000 / 1M tokens |
