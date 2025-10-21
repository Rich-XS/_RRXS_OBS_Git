[!!!VSC CCA&CCR&CPG 三引擎 Master](!!!VSC%20CCA&CCR&CPG%20三引擎%20Master.md)
[!!RRXS_AWS-EC2_Gemini Balance 轮询 AI善人](!!RRXS_AWS-EC2_Gemini%20Balance%20轮询%20AI善人.md)
[AI善人-20251009032218086](_AI善人%20轮询-20251009032218086.png)

这个视频（发布于 2025-07-05）是关于如何“榨干”免费 **Gemini 2.5 Pro API** 的使用额度，并通过部署一个名为 **“Gemini Balance”** 的代理服务，实现 **API 密钥负载均衡** 和 **国内中转访问**。

鉴于您使用 **VScode + Obsidian** 的开发环境，且之前在尝试 EC2 部署，这个教程的核心价值是教您如何将这个免费的代理服务（免费方案）部署到您的服务器（或免费云平台），并最终接入到 VScode 中使用。

下面是根据视频内容，为您提供的 **Gemini API 免费使用增强版小白教程**（默认使用免费方案，涉及 VScode 集成）。
## Gemini 2.5 Pro API 免费增强使用**小白教程**

**核心思路：** 通过部署开源项目 [Gemini Balance](https://www.google.com/search?q=https://github.com/J9Balance/gemini-proxy) (视频中称 Jmin Balance)，将您的多个免费 API Key 集中起来，实现“轮询”使用，从而将每日免费额度（每个 Key 100 次）倍增。

### 第一步：获取免费 Gemini API Key

这是所有操作的起点，每个 Google 账户每天可获得 100 次免费请求额度。

1. **环境准备：** 您需要一个海外网络环境才能访问 Google AI Studio。
    
2. **获取 Key：**
    
    - 访问 **[Google AI Studio 官网](https://ai.google.dev/gemini-api/docs/api-key)**。
        
    - 点击 **`Create API Key`** 按钮 [[01:57](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=117)]。
        
    - 选择或创建一个项目，然后点击 **`Create API Key`**。
        
    - 复制生成的密钥（格式通常为 `AIzaSy...`）。
        
3. **倍增密钥：** 建议您多注册几个 Google 账号（或向朋友获取），重复上述步骤，获取至少 **2 个或更多**的 API Key，以实现免费额度翻倍 [[02:14](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=134)]。
    

### 第二步：部署 Gemini Balance 代理服务（使用服务器/EC2 方案）

此方案适用于您之前尝试的 EC2 实例或其他海外 VPS。

#### 1. 登录与 Docker 环境准备

- 通过 SSH 连接到您的海外服务器（如 EC2 实例）。
    
- **确保 Docker 已安装并启动：**
    
    猛击
    
    ```
    # 检查 Docker 状态
    sudo systemctl status docker 
    # 如果未安装，请执行安装命令（根据您的系统类型，如 Ubuntu）
    # (具体安装步骤请参考我们上一轮的交互或视频 [01:20])
    ```
    

#### 2. 配置项目文件

- **创建项目目录并进入：**
    
    猛击
    
    ```
    mkdir gemini-balance-proxy
    cd gemini-balance-proxy
    ```
    
- **创建 `.env` 配置文件：** (此文件用于存储您的密钥和自定义令牌)
    
    猛击
    
    ```
    # 使用 vim 或 nano 创建并编辑文件
    nano .env 
    ```
    
- **填入配置内容：** 复制以下内容，并将最后两行替换成您的实际信息 [[01:38](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=98)]。
    
    猛击
    
    ```
    # 复制视频中提供的环境变量模板
    PORT=8000
    # ... (其他默认变量保持不变)
    #
    # --- 核心配置 ---
    # 倒数第二行：填入您获取的 API Key，多个 Key 用英文逗号 , 分隔
    GEMINI_API_KEYS="您的第一个API Key,您的第二个API Key" 
    
    # 倒数第一行：设置一个自定义令牌，用于访问代理服务时的验证（请自行设置，例如 rrxstoken2025）
    ALLOW_TOKEN="rrxstoken2025" 
    ```
    
- **保存文件：** 在 `nano` 中按 `Ctrl + X`，然后按 `Y` (确认保存)，最后回车。
    

#### 3. 创建 Docker Compose 文件

- **创建 `docker-compose.yaml` 文件：**
    
    猛击
    
    ```
    nano docker-compose.yaml
    ```
    
- **填入配置内容：** 复制视频中 GitHub 首页提供的 `docker-compose` 内容 [[02:51](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=171)]。
    
    YAML
    
    ```
    version: '3.8'
    services:
      gemini-proxy:
        image: j9balance/gemini-proxy:latest  # 确保是最新镜像
        container_name: gemini-proxy
        ports:
          - "8000:8000"  # 代理服务将通过服务器的 8000 端口对外开放
        env_file:
          - .env       # 引用我们刚刚创建的 .env 配置文件
        restart: always
    ```
    
- **保存文件。**
    

#### 4. 启动服务

- **在项目目录下执行启动命令：** (使用 `-d` 在后台运行)
    
    猛击
    
    ```
    # 如果您是 root 用户（如 sudo -i 状态），直接运行：
    docker compose up -d
    
    # 如果您是普通用户（如 ubuntu），需要加 sudo：
    sudo docker compose up -d
    ```
    
- **服务检查：** 看到容器创建成功后，您可以通过浏览器访问 `http://[您的服务器公网IP]:8000`，输入您设置的 `ALLOW_TOKEN` 来查看 API Key 的状态监控面板 [[03:05](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=185)]。
    

---

### 第三步：在 VScode 中集成 Gemini 2.5 Pro (作为 Doer/CCA 备选)

您可以使用视频中介绍的 **CLAN 插件**将您的代理服务接入 VScode，以实现 AI 编程辅助。

#### 1. 安装 VScode 插件

- **打开 VScode** (您当前的主工作平台)。
    
- **快捷键：** `Ctrl + Shift + X` (或点击左侧第五个图标) 打开 **Extensions** 视图。
    
- **搜索并安装：** 搜索 `CLAN` (视频中推荐的 AI 插件) [[06:33](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=393)]。
    

#### 2. 配置 CLAN 插件使用代理服务

- **打开 CLAN 设置：**
    
    - 点击 VScode 左下角的 **`设置`** 齿轮图标 (Settings)。
        
    - 或使用快捷键 `Ctrl + ,`。
        
    - 在搜索框中输入 `CLAN`。
        
- **配置步骤：**
    
    1. 找到 **`Api Provider`** 选项，选择 **`Gemini`** [[06:37](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=397)]。
        
    2. 找到 **`Use Custom Base Url`** 选项，**勾选** (使用自定义 Base URL) [[06:55](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=415)]。
        
    3. 在 **`Custom Base Url`** 文本框中，输入您刚刚部署的代理地址：
        
        ```
        http://[您的服务器公网IP]:8000
        ```
        
    4. 在 **`Api Key`** 文本框中，输入您在 `.env` 文件中设置的 **`ALLOW_TOKEN`** (例如 `rrxstoken2025`) [[07:05](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=425)]。
        
    5. 在 **`Model`** 选项中，选择 **`gemini-2.5-pro`** (用于复杂编程/思考) 或 **`gemini-2.5-flash`** (用于快速问答) [[07:08](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=428)]。
        
- **开始使用：** 您现在可以在 VScode 中通过 CLAN 插件，免费、稳定地使用具备负载均衡功能的 Gemini 2.5 Pro 进行 AI 编程了。
    

---

### 🔗 附：相关参照教程链接

- **原视频链接 (技术爬爬虾)**：[十几个场景榨干AI善人，Gemini 2.5 Pro API又免费了](http://www.youtube.com/watch?v=s3dXrSl7ltU)
    
- **GitHub 项目：** 视频中介绍的代理项目，用于负载均衡和国内中转（搜索关键词：`gemini proxy`，`J9 Balance`）[[00:37](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=37)]。
    

_(注：因 YouTube 视频内容的实时性和更新性，建议您在部署时以 GitHub 项目的最新文档和视频 [[00:32](http://www.youtube.com/watch?v=s3dXrSl7ltU&t=32)] 中提供的信息为准。)_