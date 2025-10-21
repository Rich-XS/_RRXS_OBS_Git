
[!!!VSC CCA&CCR&CPG 三引擎 Master](!!!VSC%20CCA&CCR&CPG%20三引擎%20Master.md)
[!!测试rrxyxyz_Next VSCode+AnyRouterCC](!!测试rrxyxyz_Next%20VSCode+AnyRouterCC.md)

[WIN_CCA AnyRouter Fresher_PROJECT_SUMMARY](WIN_CCA%20AnyRouter%20Fresher_PROJECT_SUMMARY.md)
[crontab_config](crontab_config.txt)

'变化'更新为'余额变化'("余额变化"(=今日最新'当前余额'-昨日最近'当前余额') 在'余额变化'后增加两列: 
- "消耗变化"(=今日最新'历史消耗'-昨日最近'历史消耗');
-  "新增赠值"(="余额变化"-"消耗变化")


# 🎯 [RRXS] AnyRouter额度自动刷新：V19.0多账号高可用体系

> **创建日期:** 2025-10-11
> **更新日期:** 待定 (V19.0部署完成后更新)
> **标签:** #RRXS/AI与效率工具 #Docker #Playwright #Crontab #自动化 #多账号维护
> **颜色系列:** 深海蓝 (AI与效率工具 RGB: 47, 85, 151)
> **核心行动口号:** 别再瞎摸索，咱们用100天，一起个人升级, 迎接新境界。

## 一、核心价值：从“单兵作战”到“体系维护”

V19.0 解决了网络不稳定（通过 **JavaScript 终极定位**）和**多账号管理**两大痛点，同时加入了 **EC2 磁盘自动清理**任务，将效率自动化体系推向极致。

### 架构回顾：铁三角稳定架构

| 架构层 | 工具/技术 | 核心作用 | V19.0 升级点 |
| :--- | :--- | :--- | :--- |
| **主机层** | AWS EC2 (Ubuntu) | 24/7 运行环境 | **新增** 每月自动磁盘清理任务 |
| **环境层** | Docker | 隔离 Playwright 依赖 | - |
| **脚本层** | Python + Playwright (V19.0) | 模拟用户登录和点击 | **核心重构**：多账号循环 + JavaScript定位前置 |
| **调度层** | Crontab | 每天定时触发 Docker 任务 | **新增** Docker 系统冗余数据清理任务 |

---

## 二、V19.0 实施步骤：终极部署

### 🚨 步骤 A: CCA 脚本重构（WIN-PS 终端操作）

这是最关键的一步，利用 WIN-PS/CCA (Opus) 的能力，将 V18.0 升级为多账号 V19.0，并优化性能。

#### **请将以下提示词，完整地粘贴给您的 WIN-PS CCA (Sonnet 4.5/Opus)：**
[WIN_CCA AnyRouter Fresher_PROJECT_SUMMARY](WIN_CCA%20AnyRouter%20Fresher_PROJECT_SUMMARY.md)

```
角色：您是精通 Playwright 异步编程和 Python 项目重构的顶级专家。我需要您基于成功的 V18.0 脚本，实现**多账号刷新**和**系统维护**。

项目名称：AnyRouter 额度自动刷新 工作目录：/home/ubuntu/anyrouter-refresher (在 AWS EC2 上)

目标： 请提供一个 **V19.0 完整脚本** 和一个 **新的 Crontab 完整配置**。

行动步骤：

1. **V19.0 脚本重构 (多账号支持与优化)：** a. **多账号配置：** 将当前的 CONFIG 更改为 `ACCOUNT_LIST`，这是一个包含多个字典的列表，每个字典包含 `'username'` 和 `'password'`，以及一个 `'name'` 字段用于日志记录。 * **请使用以下示例数据进行重构：** `python ACCOUNT_LIST = [ {'username': '123463452', 'password': '123463452', 'name': '主号-RRXS'}, {'username': 'user_b', 'password': 'pass_b', 'name': '副号-流量'} ]` b. **主函数重构：** 将 `main()` 函数重构为循环遍历 `ACCOUNT_LIST`。对于每个账号，都需要调用 `refresher.run_single_account(account_data)`，并在每次运行后确保浏览器资源被完全关闭，以便为下一个账号启动新会话。 c. **刷新优化 (JavaScript定位提前)：** 基于 V18.0 的成功经验，将 `'JavaScript定位'` 策略提升为**第一个**尝试的策略，以减少不必要的超时等待。
    
2. **Crontab 任务列表：** a. **主任务（刷新 V19.0）：** 每天 UTC 00:00 (北京时间 08:00) 运行多账号脚本。 * 指令：`0 0 * * * cd /home/ubuntu/anyrouter-refresher && docker run --rm anyrouter-refresher > /dev/null 2>&1` b. **维护任务（磁盘清理）：** 每月 1 日 UTC 01:00 (北京时间 09:00) 执行 Docker 磁盘深度清理。 * 指令：`0 1 1 * * docker system prune -a -f > /dev/null 2>&1`
    

请直接输出：

1. **V19.0 完整脚本**（`refresh.py` 内容）
    
2. **新的 Crontab 完整内容**（可以直接粘贴到 `crontab -e` 中的所有行）
```

### 步骤 B: 部署 V19.0 脚本 (EC2 终端操作)

在您的 EC2 终端 (`/home/ubuntu/anyrouter-refresher`) 执行以下操作：

1.  **删除旧脚本：**
    ```bash
    rm refresh.py
    ```
2.  **创建/粘贴 V19.0 脚本：**
    ```bash
    nano refresh.py
    # 🚨 将 CCA 输出的 V19.0 完整脚本内容粘贴到这里，确认 ACCOUNT_LIST 已更新为您真实的账号信息！
    ```
3.  **构建新的 Docker 镜像：**
    ```bash
    docker build -t anyrouter-refresher .
    ```
4.  **验证 V19.0 脚本（运行一次）：**
    ```bash
    docker run --rm anyrouter-refresher
    # 预期：脚本会依次登录并刷新列表中的所有账号。
    ```

### 步骤 C: 部署 Crontab 定时任务（一劳永逸）

1.  **打开 Crontab 编辑器：**
    ```bash
    crontab -e
    ```
2.  **粘贴 V19.0 的 Crontab 完整内容：**
    * 将 CCA 输出的**完整的两行**（刷新任务和清理任务）粘贴到文件末尾。

    ```bash
    # 🚨 请将 CCA 输出的 Crontab 完整内容（包含注释）粘贴到这里，共两行任务！

    # 1. 每日刷新任务：每天 UTC 00:00 (北京时间 08:00) 自动运行多账号刷新脚本
    # 0 0 * * * cd /home/ubuntu/anyrouter-refresher && docker run --rm anyrouter-refresher > /dev/null 2>&1

    # 2. 每月维护任务：每月 1 日 UTC 01:00 (北京时间 09:00) 自动清理 Docker 冗余磁盘空间
    # 0 1 1 * * docker system prune -a -f > /dev/null 2>&1
    ```

3.  **保存并退出：** `Ctrl + X` → `Y` → `Enter`。

---

## 三、故障排除与维护 (教练模式)

| 问题 | 诊断思路 | 解决方案 |
| :--- | :--- | :--- |
| **刷新失败** | 检查 `anyrouter_refresh.log`。 V19.0 升级了定位策略，失败概率极低。 | 重新运行 `docker run --rm anyrouter-refresher`，查看日志详情，将日志发给 AI 分析。 |
| **EC2 磁盘满** | 检查 Docker 缓存是否过多，或日志文件是否过大。 | **手动运行一次** `docker system prune -a -f` 并检查 Crontab 维护任务是否配置正确。 |
| **Crontab 不执行**| 检查 Crontab 指令路径是否正确（`/home/ubuntu/anyrouter-refresher`）。 | 运行 `crontab -l` 确认任务已安装。确保任务指令路径无误。 |
| **IP/VPN 更改** | AnyRouter 依赖国际网络访问。 | 确保您的 EC2 所在的 AWS 区域拥有稳定的国际出口，或者您在 EC2 内部配置的代理/VPN 稳定运行。 |

---

> **核心总结：** 恭喜学长，您已将一个日常琐事彻底自动化，这正是个人升级 (RRXS) 的核心价值体现！







# 🛠️ **AnyRouter 额度刷新自动化部署：全套小白教程 (VSC 终端版)**




### 准备阶段 
确保SSH不掉线- 最简单、最稳定的解决方法是在您的本地电脑上设置 **SSH 心跳包（KeepAlive）**机制，让客户端每隔一段时间自动向服务器发送一个微小的数据包，以证明连接仍然活跃。
**在 VSC 中打开 `config` 文件**（如果您已经关闭）
```
code C:\Users\rrxs\.ssh\config
```
确保其中内容 底部增加KeepAlive部分
```
Host github.com
    HostName github.com
    User git
    IdentityFile "D:/OneDrive_RRXS/OneDrive/__RRXS_XYZ/home/ubuntu/rrxs.xyz/GitHub SSH Key"

Host 120.55.168.94
    HostName 120.55.168.94
    User root
    # Password Austin050824

Host https://ipinfo.io/dashboard/lite
    HostName https://ipinfo.io/dashboard/lite

# --- 以下是新增的 KeepAlive 防掉线配置 ---
# SSH KeepAlive Configuration
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 5
```


### **第一阶段：连接到远程 EC2 实例**

您当前在 ==VSC/本地 PowerShell 终端==：`(.venv) PS D:\_100W\rrxsxyz_next>`。

#### **步骤 1.1：执行 SSH 连接（直接复制粘贴）**

我们将使用您密钥的**绝对路径**和您 EC2 的 IP 地址 `54.252.140.109` 进行连接。

> **🚨 注意：** 如果您的 EC2 实例曾停止后重新启动，公网 IP 可能会发生变化。请务必检查 AWS 控制台，如果 IP 变化，请替换下面的 `54.252.140.109` 为新 IP。

**请直接复制并粘贴以下指令到您的 VSC 终端中执行：**

Bash

```
# 使用已知的绝对路径 C:\Users\rrxs\.ssh\RRXSXYZ_EC2.pem 进行连接
ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109
```

**指令解释：**

- `-i`：指定身份文件（您的密钥）。
    
- `"C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem"`：密钥的 Windows 绝对路径（使用斜杠 `/` 更兼容 Bash 环境）。
    
- `ubuntu@54.252.140.109`：登录名为 `ubuntu`，目标主机 IP 是 `54.252.140.109`。
    

#### **步骤 1.2：确认终端状态**

成功连接后，您的终端提示符将变为：

Bash

```
ubuntu@ip-172-31-8-33:~$
```

**📢 确认终端是 `ubuntu@...` 状态后，继续执行下面的步骤。**

---

### **第二阶段：文件创建与修正（EC2 远程操作）**

遵循您的习惯：`rm` (删除旧文件) 后 `nano` (创建新文件并粘贴内容)。

#### **步骤 2.1：创建 `refresh.py` 脚本（核心逻辑）**

1. **删除并重建文件：**
    
    Bash
    
    ```
    rm refresh.py
    Y
    ```
    
1. **粘贴代码**，**并务必替换** `USER_CREDENTIAL` 和 `PASS_CREDENTIAL` 为您的真实 AnyRouter 登录信息：
```
# refresh.py (Playwright - V15.0 最终版 - 登录跳转容错)
import time
from playwright.sync_api import sync_playwright

# --- 您的配置信息 ---
LOGIN_URL = "https://anyrouter.top/login" 
CONSOLE_URL = "https://anyrouter.top/console" 

# 🚨 已替换为您提供的 AnyRouter 登录凭证！ 🚨
USER_CREDENTIAL = "123463452"  
PASS_CREDENTIAL = "123463452"         

# --- 关键定位器 ---
USER_SELECTOR = 'input[name="username"]'
PASS_SELECTOR = 'input[name="password"]'
LOGIN_SUBMIT_SELECTOR = 'button:has-text("登录")' 
FALLBACK_SUBMIT_SELECTOR = 'button[type="submit"]' 
REFRESH_ICON_SELECTOR = 'span.semi-icon-refresh' 


def refresh_quota():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = browser.new_page()

            # --- 1. 执行登录 ---
            print(f"访问登录页面: {LOGIN_URL}")
            page.goto(LOGIN_URL, wait_until='domcontentloaded')

            print("直接尝试输入凭证...")
            page.fill(USER_SELECTOR, USER_CREDENTIAL)
            page.fill(PASS_SELECTOR, PASS_CREDENTIAL)

            print("尝试点击提交/登录按钮 (增加强制点击容忍度)...")
            try:
                page.click(LOGIN_SUBMIT_SELECTOR, timeout=5000) 
            except Exception:
                page.click(FALLBACK_SUBMIT_SELECTOR, timeout=10000, force=True)

            # --- 1.1 登录后容错跳转 ---
            print("登录点击完成，等待页面跳转（5秒缓冲）...")
            time.sleep(5) 

            # 尝试等待URL跳转，如果失败，则直接二次 goto
            try:
                page.wait_for_url(CONSOLE_URL, timeout=15000)
                print("成功跳转到控制台。")
            except Exception:
                print("跳转超时或失败，尝试二次 goto 确保位于控制台。")
                page.goto(CONSOLE_URL, wait_until='domcontentloaded', timeout=15000)

            # --- 2. 执行刷新操作 ---
            print(f"已进入控制台，尝试点击刷新按钮: {REFRESH_ICON_SELECTOR}")
            # 等待刷新图标出现
            page.wait_for_selector(REFRESH_ICON_SELECTOR, timeout=15000)
            page.click(REFRESH_ICON_SELECTOR) 

            print(">>> 额度刷新操作已执行！等待 5 秒确认赠送...")
            time.sleep(5)

            browser.close()
            print("刷新任务完成。")

    except Exception as e:
        print(f"任务执行失败: {e}")

if __name__ == '__main__':
    refresh_quota()
```

3. **保存并退出 `nano`：** 按 `Ctrl + X` → 按 `Y` → 按 `Enter`。
    

#### **步骤 2.2：创建 `Dockerfile`（环境配置）**

1. **删除并重建文件：**
    
    Bash
    
    ```
    rm Dockerfile
    nano Dockerfile
    ```
    
2. **粘贴代码**（已修正版本不匹配和模块缺失问题）：
    
    Dockerfile
    
    ```
    # Dockerfile (最终修正版 - 修复版本和依赖)
    FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy
    
    # 修复 ModuleNotFoundError: 显式安装 Playwright Python 库
    RUN pip install playwright
    
    # 复制脚本到容器 /app 目录
    COPY refresh.py /app/
    WORKDIR /app
    
    # 容器启动时运行的命令
    CMD ["python", "refresh.py"]
    ```
    
3. **保存并退出 `nano`：** 按 `Ctrl + X` → 按 `Y` → 按 `Enter`。
    

---

### **第三阶段：构建与功能验证**

#### **步骤 3.1：磁盘清理（防呆：解决空间不足）**

如果您上次遇到了空间不足错误，请执行清理：

Bash

```
docker system prune -a
```

**提示：** 出现 `Are you sure you want to continue? [y/N]` 时，**输入 `y` 并按 `Enter` 确认。**

#### **步骤 3.2：构建 Docker 镜像**

构建名为 `anyrouter-refresher` 的镜像：

Bash

```
docker build -t anyrouter-refresher .
```

#### **步骤 3.3：最终功能测试（核心验证）**

运行容器进行功能验证：

Bash

```
docker run --rm anyrouter-refresher
```

**📢 最后的关键一步！请将这次 `docker run` 的完整输出复制给我！**


---

### **第四阶段：设置定时任务（如果步骤 3.3 成功）**

这是实现“全流程自动化”的最后一步。

1. **打开 Cron 编辑器：**
    
    Bash
    
    ```
    crontab -e
    ```
    
2. **在文件末尾添加以下行：** （设置**每天凌晨 1 点**运行任务，并将日志记录在 `refresh_log.txt` 中）
    
    Bash
    
    ```
    # 每天凌晨 1 点运行 Docker 容器，并记录日志到 /home/ubuntu/refresh_log.txt
    0 1 * * * /usr/bin/docker run --rm anyrouter-refresher >> /home/ubuntu/refresh_log.txt 2>&1
    ```
    
3. **保存并退出 `nano`：** 按 `Ctrl + X` → 按 `Y` → 按 `Enter`。