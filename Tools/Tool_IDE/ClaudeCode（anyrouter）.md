---
tags:
原文发布链接:
categories:
created: "2025-09-28 15:11 "
updated: "2025-09-28 15:11 "
---


# 世一 Claude Code 免費任玩，免VPN，免信用卡！

  

148 views Jul 12, 2025

手續超簡單，3分鐘就攞到試用金。 領取100美元credit，只需用以下連結登入 ： [https://anyrouter.top/register?aff=in2N](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbjRSQnp5VHBMRGFqbDRseEFSdUtXZG9JWlhOQXxBQ3Jtc0tuX1c2bDJBbkRySHhzMkV5cE83OHNld3h3eUpweFFWWHFXOVNqUTNuME5iaUowNkRiS01VenhhNjcxTnk2UU9wWHlhcDUzU1VoSlpKWjQ2T0lkOGJaTFFaSEVpYW03Y01RR0NyNTc5eEJGU2I1LW9Eaw&q=https%3A%2F%2Fanyrouter.top%2Fregister%3Faff%3Din2N&v=D_pMrHHAMPE) Chapter [00:00](https://www.youtube.com/watch?v=D_pMrHHAMPE) ：前言 [00:45](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=45s) ：Anyrouter 介紹 [02:06](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=126s) ：註冊GITHUB [02:30](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=150s) ：註冊 Anyrouter [02:55](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=175s) ：建立API KEY [03:58](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=238s) ：Claude Code 安裝 [06:34](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=394s) ：Claude Code 示範 [08:20](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=500s) ：Gemini CLI 示範 [09:30](https://www.youtube.com/watch?v=D_pMrHHAMPE&t=570s) ： 後話

[(4 条消息) Windows 下轻松玩转 Claude Code？用 AnyRouter 一键搞定，附详细教程 - 知乎](https://zhuanlan.zhihu.com/p/1937835472492696293)

[🚀 AnyRouter｜Claude Code 免费共享平台](https://anyrouter.top/)

[[anyrouter]]

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

  
  
❓FAQ  
  

- 本站直接接入官方 Claude Code 转发，无法转发非 Claude Code 的 API 流量  
      
    
- 如遇 API 报错，可能是转发代理不稳定导致，可以考虑退出 Claude Code 重试几次  
      
    
- 如果网页遇到登录错误可以尝试清除本站的 Cookie，重新登录  
      
    
- `Invalid API Key · Please run /login` 怎么解决？这表明 Claude Code 没有检测到 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL` 环境变量，检查环境变量是否配好。  
      
    
- 显示 `offline` 是什么原因？Claude Code 会通过检查是否能连接到 Google 来对网络进行判断。显示 `offline` 并不影响正常使用 Claude Code，只是表明 Claude Code 未能连接 Google。  
      
    
- 为什么浏览网页的 Fetch 会失败？这是因为 Claude Code 在访问网页前会调用 Claude 的服务来判断网页是否可以访问。需要保持国际互联网连接并进行全局代理，才可以访问 Claude 判断网页是否可以访问的服务。  
      
    
- 为什么请求总是显示 fetch failed？可能是因为所在地区的网络环境导致的，可以尝试使用代理工具或者使用备用 API 端点 `ANTHROPIC_BASE_URL=https://pmpjfbhq.cn-nb1.rainapp.top`
