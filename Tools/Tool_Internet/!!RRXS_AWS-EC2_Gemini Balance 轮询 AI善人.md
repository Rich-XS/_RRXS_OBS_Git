---
标签:
tags:
  - 轮询
  - Gemini
---
[!!!VSC CCA&CCR&CPG 三引擎 Master](!!!VSC%20CCA&CCR&CPG%20三引擎%20Master.md)
[!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)
[Ubuntu常用命令一览](Ubuntu常用命令一览.md)
[!常见 API 错误代码与解决方案](!常见%20API%20错误代码与解决方案.md)


视频: [十几个场景榨干AI善人，Gemini 2.5 Pro API又免费了 #ai #人工智能 #科技 #教程 #计算机](https://www.youtube.com/watch?v=s3dXrSl7ltU&t=312s)

https://aistudio.google.com/ 
获取gemini api key


Gemini proxy
  
snailyp/_gemini_-balance
[snailyp/gemini-balance: Gemini polling proxy service （gemini轮询代理服务）](https://github.com/snailyp/gemini-balance)

[从零部署 Gemini Balance 手册之clawcloud上部署sqlite版本 | Gemini Balance](https://gb-docs.snaily.top/guide/setup-clawcloud-sqlite.html)
[[从零部署 Gemini Balance 手册之clawcloud上部署sqlite版本  Gemini Balance]]

https://inlkiebrwgvo.ap-southeast-1.clawcloudrun.com
key: sk-adog

```
cd D:\OneDrive_RRXS\OneDrive\_AIGPT\VSCodium\AnyRouter_Refresh\arb_web_api
python app.py
```
### 🔑 API 访问信息
- **基础 URL**: `http://127.0.0.1:9876`
- **认证 Token**: `sk-ARB-RRXS`


# 轮询

## Provider: Openrouter

## 云服务器: Amazon EC2(https://aws.amazon.com/cn/free) 

richardxiesong@gmail.com Au..4! Root-User rrxs@outlook.com(Au..4!) 邮件验证码验证. (backup rrxsus@gmail.com Au..4!)
实例: RRXYXYZ_EC2; 密钥对名称: RRXYXYZ_EC2 (E:\Software\Tools_Internet\!AWS\RRXYXZY_EC2.pem)

AWS-EC2-Singapore 云端邮件Gmail "AnyRouter-EC2"应用专用密码"ywhh uimf qrfl nlqr"

公用IPv4: 54.252.140.109
私用IPv4: 172.31.8.33

##   新 EC2 已创建完成！
    新加坡 IP 地址: 3.0.55.179 
    使用的密钥: RRXSXYZ_EC2_Singapore
    密钥文件位置: C:\Users\rrxs\.ssh\RRXSXYZ_EC2_Singapore.pem

API URL: "http://54.252.140.109:8000"
API KEY: "sk-BaiWen_RRXS"

API URL: "http://3.0.55.179:8000"
API KEY: "sk-BaiWen_RRXS"
==ssh -i "C:\Users\rrxs\.ssh\RRXSXYZ_EC2_Singapore.pem" ubuntu@3.0.55.179==
ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109 

~~~~rrxsjp@gmail.comm/Au..4! (RRXS-Tokyo-Free)XIESONG/19534071485 (201104...) Root: rrxsaws@outlook.com(Au..4)~~~~
### tabby Terminal https://github.com/Eugeny/tabby/releases/tag/v1.0.227

配置>新配置> 公用IPv4+密钥文件 ![](_AI善人%20轮询-20251009032218086.png)

### **ubuntu**
- EC2 实例的 ubuntu 用户密码说明: 默认情况：没有密码使用 `sudo -i` 或 `sudo su` 切换到 Root 用户 
```
  ubuntu@ip-172-31-8-33:~$sudo -i
  root@ip-172-31-8-33:~# 
```
-  步骤2：添加 Docker 的官方 GPG 密钥
```
# 添加 Docker 的官方 GPG 密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
- 步骤 3：设置 Docker 存储库
```
# 设置 Docker 存储库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- 步骤 4：安装 Docker Engine
```
# 再次更新 apt 软件包列表
sudo apt update
# 安装 Docker 引擎、CLI 和 Containerd
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```
- 步骤 5：启动并设置开机自启（可选）
```
# 启动 Docker 服务 (可能不需要，因为安装后通常会启动)
sudo systemctl start docker

# 设置开机自启
sudo systemctl enable docker
```
- 步骤 6：配置非 Root 用户权限（**重要！**）
这是最重要的一步，它将允许您的 ubuntu 用户在不使用 sudo 的情况下运行 Docker 命令。
```
# 将当前用户（ubuntu）添加到 docker 组
sudo usermod -aG docker ubuntu

# 激活新的组配置，您需要重新登录 SSH，或者执行以下命令：
# 注意：此命令将退出并重新登录，可能会中断您的终端会话。
exec newgrp docker
```
提示： 运行完 exec newgrp docker 后，您的终端会话可能会断开或重置。建议直接关闭当前的 SSH 窗口，然后用密钥重新连接。
- 步骤 7：验证安装
重新连接 SSH 后，测试 Docker 是否正常工作。
```
# 运行官方的测试镜像
docker run hello-world
```

[!十几个场景榨干AI善人，Gemini 2.5 Pro API又免费了](!十几个场景榨干AI善人，Gemini%202.5%20Pro%20API又免费了.md)


## Gemini 2.5 Pro API 免费增强 
>> 视频: [!十几个场景榨干AI善人，Gemini 2.5 Pro API又免费了](!十几个场景榨干AI善人，Gemini%202.5%20Pro%20API又免费了.md)(https://www.youtube.com/watch?v=s3dXrSl7ltU&t=312s)
### 事先准备: 无限使用 Gemini Key
[Google AI Studio](https://aistudio.google.com/api-keys)
richardxiesong@gmail.com:  GeminiBalance / ==AIzaSyBkUQh33qWNvw-NoSGr639DkbuQ8Q63dzQ==
richardxiesong@gmail.com:  GB_RRXS2 / AIzaSyAc2n94S--V3ktYnxUV44FE_8AgzpfXorU
richxie.mx@gmail.com   Miaoxi / GeminiBalance2 |    ~~AIzaSyAXNCHjqnybdNXTqJOOE9CiJTmTi7Sr0H0~~ | Miaoxi / GeminiBalance3 |     
**AIzaSyC6DuTDFvkg73Kej23iCz_h1piiqh81vdc** | 
rrxsjp@gmail.com:  ==AIzaSyDl9JNa08EaAIzTZ3W7gE5CJMaOrqAdOwg== | AIzaSyAruoDHV_7azIsuqovtJXGX_gh7VP59dWE
rrxsuk@gmail.com ~~AIzaSyDM6_sKf_WZ5B7Yk0WdQBvB7rC93ZHoX6A~~ | **AIzaSyCOqz9W7FqAmESxW9vE4RTTwNZBDepLCbE**
rrxsus@gmail.com  AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0 |  ==AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0==

## Gemini Balance配置 [snailyp/gemini-balance: Gemini polling proxy service （gemini轮询代理服务）](https://github.com/snailyp/gemini-balance)
- unbuntu启动docker(如果已经启动"hello"可略过), 
```
ubuntu@ip-172-31-8-33:~$ sudo -i
root@ip-172-31-8-33:~# server docker start

//开始创建环境
:~#: vi .env
```
- 获取env.example 前11行[gemini-balance/.env.example at main · snailyp/gemini-balance](https://github.com/snailyp/gemini-balance/blob/main/.env.example)
- 在API_KEYS 更新
	- RRXS1, RichXie.MX, RRXSJP1, RRXSUK1, RRXSUS1, 
	  "AIzaSyBkUQh33qWNvw-NoSGr639DkbuQ8Q63dzQ", "AIzaSyAXNCHjqnybdNXTqJOOE9CiJTmTi7Sr0H0", "AIzaSyDl9JNa08EaAIzTZ3W7gE5CJMaOrqAdOwg", "AIzaSyDM6_sKf_WZ5B7Yk0WdQBvB7rC93ZHoX6A", "AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0"
	- RRXS2, RichXie.MX2, RRXSJP2, RRXSUK2, RRXSUS2,
	  ...
```
# 数据库配置
DATABASE_TYPE=mysql
#SQLITE_DATABASE=default_db
MYSQL_HOST=gemini-balance-mysql
#MYSQL_SOCKET=/run/mysqld/mysqld.sock
MYSQL_PORT=3306
MYSQL_USER=gemini
MYSQL_PASSWORD=change_me
MYSQL_DATABASE=default_db
API_KEYS=["AIzaSyBkUQh33qWNvw-NoSGr639DkbuQ8Q63dzQ", "AIzaSyAXNCHjqnybdNXTqJOOE9CiJTmTi7Sr0H0", "AIzaSyDl9JNa08EaAIzTZ3W7gE5CJMaOrqAdOwg", "AIzaSyDM6_sKf_WZ5B7Yk0WdQBvB7rC93ZHoX6A", "AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0"]
ALLOWED_TOKENS=["sk-BaiWen_RRXS"]
~                                                         
```
- ALLOWED_TOKENS: ["sk-BaiWen_RRXS"]]
- esc / :wq! / 回车
- 创建 docker-compose  40分钟的Docker实战([Freedom in Every Wave](https://www.youtube.com/watch?v=_-IPi1a774E))
```
:~# vi docker-compose.yaml
```
- Gemini Balance 找到 Docker-Compose [gemini-balance/docker-compose.yml at main · snailyp/gemini-balance](https://github.com/snailyp/gemini-balance/blob/main/docker-compose.yml)
  > Github文件上的内容完全copypaste到Unbuntu的Docker-Compose.yaml, 保存退出
- 启动项目
```
:~# docker compose up -d
//或: 如果非root用户
:~# sudo docker compose up -d
....
[+] Running 4/4
 ✔ Network root_default            Created        0.1s 
 ✔ Volume root_mysql_data          Created        0.0s 
 ✔ Container gemini-balance-mysql  Healthy        16.3s 
 ✔ Container gemini-balance        Started        16.8s 
root@ip-172-31-8-33:~# 
```
- Docker创建完成

- 完成浏览器8000设定
  [ModifyInboundSecurityGroupRules | EC2 | ap-southeast-2](https://ap-southeast-2.console.aws.amazon.com/ec2/home?region=ap-southeast-2#ModifyInboundSecurityGroupRules:securityGroupId=sg-036f126d575190720) 
	- AWS控制台>搜索:EC2>实例: RRXSXYZ_EC2, 点击实例ID>中间的'安全'菜单> 安全组>编辑入站规则
- 浏览器验证: [验证页面 - Gemini Balance](http://54.252.140.109:8000/)>>输入"==sk-BaiWen_RRXS=="

==API URL: "http://54.252.140.109:8000"
API KEY: "sk-BaiWen_RRXS"==

model ID: gemini-2.5-pro, gemini-2.5-flash

所有密钥: 

AIzaSyC8Vy13HWXwYZ696HBYaqqsnt4F72reZEc
AIzaSyAXNCHjqnybdNXTqJOOE9CiJTmTi7Sr0H0
AIzaSyDl9JNa08EaAIzTZ3W7gE5CJMaOrqAdOwg
AIzaSyDM6_sKf_WZ5B7Yk0WdQBvB7rC93ZHoX6A
AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0

sk-784f284ee3e14b079dd8d382782823e2
AIzaSyC6DuTDFvkg73Kej23iCz_h1piiqh81vdc
AIzaSyAruoDHV_7azIsuqovtJXGX_gh7VP59dWE
AIzaSyCOqz9W7FqAmESxW9vE4RTTwNZBDepLCbE
AIzaSyCEmvjKXdbTPGaCUHjjolGzOl0q28AftO0

AIzaSyAc2n94S--V3ktYnxUV44FE_8AgzpfXorU
AIzaSyBkUQh33qWNvw-NoSGr639DkbuQ8Q63dzQ
AIzaSyDwqzZVhogjwCCBieFMfrQgsjAIpLjyW38
AIzaSyA61oeugkd3s-KNixyAnQ5goJ5UEq_iqgo

## ==模型选择==


| CCR UI 分类        | 日常使用量 (日均 / 日峰值)           | 模型名                       | 模型 Slug                               | 优先级 | 免费限制 RPD/RPM   | 您的需求 (RPD) 所需账号数 Max | 适配要点                                                |
| ---------------- | -------------------------- | ------------------------- | ------------------------------------- | --- | -------------- | -------------------- | --------------------------------------------------- |
| 思考/推理/长文本        | 低频次 / 极低 (估算 20/50 RPD)    | Gemini 2.5 Pro            | gemini-2.5-pro                        | 首选  | 25 RPD / 5 RPM | 105 个                | 核心专业分析。仅用于“专家模式”、“评审模式”等最高能力需求，避免浪费 25 RPD 的宝贵免费额度。 |
| 后台 (高吞吐)         | 高频次 / 极高 (估算 700/2300 RPD) | Gemini 2.5 Flash-Lite 预览版 | gemini-2.5-flash-lite-preview-09-2025 | 首选  | 500 RPD        | 6 个                  | 轮询池主力。承载 VSC CCA 编码、CPG 协同、笔记摘要等绝大部分高频请求。极致低成本方案。   |
|                  |                            | Gemini 2.5 Flash-Lite     | gemini-2.5-flash-lite                 | 次选  | 500 RPD        | 6 个                  | 轮询池备选。作为 Lite 预览版的替代，确保容量。                          |
|                  |                            | Gemini 2.0 Flash-Lite     | gemini-2.0-flash-lite                 | 备选  | 500 RPD        | 6 个                  | 低成本降级。当 2.5 系列 Key 失败时的次低成本选项。                      |
| 默认 (通用)          | 中频次 / 中高 (估算 130/260 RPD)  | Gemini 2.5 Flash          | gemini-2.5-flash                      | 首选  | 500 RPD        | 6 个                  | 高性能主力。用于对速度和能力有更高要求的普通通用任务。                         |
|                  |                            | Gemini 2.0 Flash          | gemini-2.0-flash                      | 备选  | 500 RPD        | 6 个                  | 备用降级。当 2.5 系列 Key 失败时使用。                            |
| 嵌入 (Embedding)   | 后台 / 稳定 (估算 3/8 RPD)       | Gemini Embedding 001      | gemini-embedding-001                  | 首选  | 免费/高速          | 1 个                  | 知识库核心。专用于 Obsidian DSk 的向量化，必须使用独立 Key 保证稳定。        |
| 搜索 (网络/Grounded) | 低频次 / 中 (估算 0/50 RPD)      | Gemini 2.5 Flash-Lite 预览版 | gemini-2.5-flash-lite-preview-09-2025 | 首选  | 500 RPD (免费)   | 6 个                  | 高吞吐网络查询。使用 Flash/Lite 轮询池的免费网络搜索功能。                 |
| 图片 (图像)          | 极低频次 / 极低 (估算 0/5 RPD)     | Gemini 2.5 Flash 图片       | gemini-2.5-flash-image                | 首选  | 无免费            | 1 个                  | 内容配图。用于 IP 视觉输出，建议使用付费 Key 或 AI Studio 免费试用。        |
|                  |                            |                           |                                       |     |                |                      |                                                     |

|                              |                                              |                                           |                         |             |                                                                    |
| ---------------------------- | -------------------------------------------- | ----------------------------------------- | ----------------------- | ----------- | ------------------------------------------------------------------ |
| 任务类别 (CCR UI 配置)             | 适用场景 (您的项目)                                  | 模型选择 (首选)                                 | 所需账号/Key数               | 免费 RPD/限速   | 路由目标                                                               |
| P1: 后台/高吞吐 (Flash-Lite Pool) | VSC CCA (Doer) 编码、CPG (Viber) 协同、长篇笔记整理、批量文案 | Gemini 2.5 Flash-Lite 预览版 (次选 Flash/Lite) | 6 个 (组成轮询池)             | 500 RPD/Key | 承载 95% 的请求量。 启用**轮询（Round-Robin）**模式，自动切换 Key 以覆盖 2,618 RPD 的峰值需求。 |
| P2: 思考/推理 (Pro Key)          | “专家模式”、“评审模式”、“杠精模式” 等复杂逻辑、代码架构、行业深度分析。      | Gemini 2.5 Pro                            | 1 个 (独立 Key)            | 25 RPD/Key  | 专用通道，用于最高质量的推理。确保低频次的关键任务获得最高模型能力。                                 |
| P3: 嵌入/知识库 (Embedding)       | Obsidian (DSk) 知识库的向量化、索引和检索                 | Gemini Embedding 001                      | 1 个 (独立 Key)            | 免费/高速       | 专用于后台知识管理，确保您的“第二大脑”基础稳定运行。                                        |
| P4: 备选/容错 (Fallback)         | 当前所有 Key RPD 耗尽时的紧急任务                        | OpenRouter (Gemini Lite Preview)          | 1 个 (现有 OpenRouter Key) | 按平台限额       | 最后的防线。 当 Google 官方 RPD 全部用尽时，自动切换到 OpenRouter 额度，保证任务不中断。          |


这个流量倾斜是系统自己判断的吧, 不是我能设定的吧? 我可以做什么?

这是一个非常关键的问题！您说得完全正确：**流量的“倾斜”和“路由”不是系统自动完成的，而是需要您在 CCR UI 中进行手动设定的。**

在您使用的 **VSC+Obsidian+CCR** 体系中，您需要做的就是通过配置规则，来**强制模型按照您的低成本、高效率策略执行**。

以下是您可以做的具体操作和配置要点，确保流量严格按照我们规划的策略倾斜：

---

## 1. 流量倾斜/路由的设定方法

您在 CCR（Claude Code Router 或 AnyRouter）UI 中设定的路由规则，就是实现“流量倾斜”的核心机制。

**实现机制：** 您不能直接设定“82% 的流量去 Flash-Lite”，但您可以设定 **“所有符合某一条件的请求”** 必须优先使用某个模型。

|流量倾斜目标|**CCR UI 设定动作**|
|---|---|
|**82% 高吞吐量**|**设定默认路由模型（Default Model）为 Flash-Lite 轮询池**。这意味着大部分没有特殊标记或要求的请求，都会自动流向这个成本最低、容量最大的池子。|
|**推理任务**|设定特定的 **“魔法提示词”前缀** 或 **请求关键词** (如：“专家分析”、“给我做代码重构”)，一旦触发，则**强制路由**到 **Gemini 2.5 Pro Key**。|
|**知识库任务**|设定 Obsidian 插件（如 DSk）的配置，**直接指定**模型为 **Embedding 001**。|

导出到 Google 表格

---

## 2. 您可实施的 CCR UI 配置要点 (小白教程)

根据您是使用 **VSC+Obsidian** 工作的习惯，这里是具体的实施步骤：

### 步骤一：配置模型 Key 池（轮询）

这是您实现 **6 个 Key 轮询** 的基础。在 CCR 的配置界面（通常是一个 JSON/YAML 文件或配置 UI）：

1. **创建 Flash-Lite Pool：** 将 6 个 `gemini-2.5-flash-lite-preview-09-2025` 或 `gemini-2.5-flash` 的 Key 集中配置在一个名为 `flash_lite_pool` 的组中，并设置其**负载模式为 Round-Robin (轮询)**。
    
2. **创建 Pro Key：** 将 1 个 `gemini-2.5-pro` Key 单独配置，命名为 `gemini_pro_expert`。
    
3. **创建 Embedding Key：** 将 1 个 `gemini-embedding-001` Key 单独配置。
    

### 步骤二：设定默认模型 (流量倾斜的核心)

**核心操作：** 将 CCR 的全局**默认模型 (Default Model)** 设置为您的 **Flash-Lite 轮询池**。

- **路径：** CCR/Router 设置 → General → **Default Model Name**。
    
- **设置值：** `flash_lite_pool`
    

> 这样，所有没有明确指定模型的请求，都会自动、免费地进入这个低成本、高容量的池子，完成 **82% 的流量倾斜**。

### 步骤三：设定路由规则（魔法提示词）

利用 CCR 的**路由规则（Routing Rules）**功能，将您的“9魔法模式”中的高价值任务，强制导向 **Pro Key**。

|路由规则|触发条件 (关键词)|目标模型|效果|
|---|---|---|---|
|**Pro_Expert**|包含关键词：`[专家模式]` 或 `[评审模式]` 或 `代码重构`|`gemini_pro_expert`|确保最高推理能力。|
|**Pro_Complex**|包含关键词：`[未来倒推模式]` 或 `[杠精模式]`|`gemini_pro_expert`|将对逻辑要求最高的任务路由过去。|

导出到 Google 表格

### 步骤四：Obsidian/VSC 插件配置（特定任务）

对于特定的工作流，您需要直接在插件中指定模型，绕过 CCR 的默认设置：

- **Obsidian DSk 配置：** 在 DeepSeeK 或相关向量库的配置中，**硬编码** 模型名称为 `gemini-embedding-001`，确保知识库功能稳定。
    
- **VSC CCA 编码：** 如果您的 CCA 任务是通用的，可以继续使用默认路由（即 Flash-Lite Pool）；如果是复杂代码，您可以在 CCA 的提示词中加入 **`[专家模式]`** 关键词来触发 Pro 路由。
    

通过以上 **“默认模型设定 + 特定路由规则”** 的组合拳，您就完全掌握了流量的倾斜，实现了根据模型能力和成本进行任务路由的 **Gemini Balance 轮询** 策略。