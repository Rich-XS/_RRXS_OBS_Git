# CLAUDE.md

  

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

  

---

  

## 🤖 Custom Agent Configuration

  

**Progress Recorder Agent** - 项目记忆与上下文持续性管理

  

本项目使用自定义 agent 进行项目记忆管理。详细规则见：

- **记忆规则配置**: `my_main_agent.md`

- **Agent 定义**: `.claude/agents/progress-recorder.md`

- **进度记录**: `progress.md`（活跃记忆）

- **历史归档**: `progress.archive.md`（冷存储）

  

**触发关键词：**

- `>> recap` - 项目回顾总结

- `>> record` - 增量记录当前进度

- `>> archive` - 归档历史记录

- `>> wrap-up` - 会话收尾（准备关机时使用）

  

**⚠️ 强制触发规则（Claude Code 必须遵守）：**

  

当对话中出现以下关键词时，**必须立即调用 Task tool 启动 progress-recorder agent**，而不是手动编辑 progress.md：

  

1. **决策完成**：用户说"我决定"/"确定"/"选用"/"将采用" → 立即调用 agent 记录决策 → 更新 progress.md Decisions

2. **任务完成**：出现"已完成"/"完成了"/"已实现"/"修复了" → 立即调用 agent 更新 Done

3. **新任务产生**：出现"需要"/"应该"/"待办"/"TODO" → 立即调用 agent 添加 TODO

4. **需求变更**：出现"需求更新"/"架构调整"/"变更"/"重构" → 立即调用 agent 更新 progress.md **和 CLAUDE.md**，并在 CLAUDE.md 末尾添加时间戳

5. **会话收尾**：用户输入 `>> wrap-up` 或说"准备关机" → 立即调用 agent 总结会话，更新 progress.md，确认可安全关机

6. **用户明确要求**：用户输入 >> record 或 >> recap 或 >> archive → 立即调用 agent

  

**禁止行为：**

- ❌ 禁止直接手动编辑 progress.md（除非是修复格式错误）

- ❌ 禁止绕过 agent 直接使用 Edit/Write tool 修改 progress.md

- ❌ 禁止在需求变更时忘记同步更新 CLAUDE.md

- ✅ 必须通过 Task tool 调用 progress-recorder agent 来更新项目记忆

- ✅ 需求变更时必须同时更新 progress.md 和 CLAUDE.md

  

---

  

## 项目概述

  

**RRXS.XYZ** - 个人品牌自媒体网站，包含两大核心模块：

- **百问自测系统**：100题自媒体商业化能力评估工具

- **多魔汰辩论系统**：多角色AI辩论决策支持系统

  

## 核心命令

  

### 启动开发环境

  

**推荐方式（完整功能）：**

```bash

# 双击运行启动脚本，选择 [3] Full Stack

启动本地服务器-更新版.bat

```

  

**手动启动：**

```bash

# 前端服务器（Python，端口8080）

python -m http.server 8080

  

# 后端API服务器（Node.js，端口3000）

cd server

npm install  # 仅首次运行

npm run dev

```

  

### 访问地址

- 首页：http://localhost:8080/

- 百问自测：http://localhost:8080/baiwen.html

- 多魔汰：http://localhost:8080/duomotai/

- 后端API：http://localhost:3000/

  

### 测试

```bash

# 测试邮件服务

cd server

node test-email.js

  

# 健康检查

curl http://localhost:3000/health

```

  

## 架构设计

  

### 前端架构

  

**静态页面（Vanilla JS + HTML）：**

- `index.html` - 主页（含Coze AI聊天）

- `baiwen.html` - 百问自测入口页

- `Projects.html` - 项目展示页

  

**React项目：**

```

html/projects/

├── media-assessment-v1/     # 百问V1 - 深度思考版

├── media-assessment-v2/     # 百问V2 - 选项版

├── media-assessment-v4.html # 百问V4 - 单文件最终版（主要使用）

└── duomotai/               # 多魔汰系统（独立HTML+模块）

```

  

**多魔汰系统模块化设计：**

```

duomotai/

├── index.html              # 主入口（单文件，包含所有逻辑）

├── src/

│   ├── config/

│   │   └── roles.js        # 16个辩论角色配置

│   ├── modules/

│   │   └── debateEngine.js # 辩论引擎核心逻辑

│   ├── components/         # UI组件

│   └── utils/              # 工具函数

└── public/                 # 静态资源

```

  

### 后端架构

  

```

server/

├── server.js               # Express主服务器

├── services/

│   ├── aiService.js        # AI模型调用（Qwen/DeepSeek/OpenAI容错）

│   ├── emailService.js     # 邮件服务（QQ邮箱/SendGrid）

│   ├── userDataService.js  # 用户数据管理（JSON存储）

│   └── userAuthService.js  # 用户认证（验证码）

└── .env                    # 环境配置（需手动创建）

```

  

### 关键技术栈

  

**前端：**

- React 18 + Vite（百问V1/V2项目）

- TailwindCSS + Shadcn/UI（组件库）

- Recharts（数据可视化）

- 单文件HTML（V4和多魔汰 - 简化部署）

  

**后端：**

- Node.js 18+ + Express

- AI服务：Qwen API（主）→ DeepSeek → OpenAI（降级）

- 邮件：Nodemailer（QQ邮箱免费方案）

- 数据：JSON文件存储 + LocalStorage

  

## 重要设计决策

  

### 1. 多魔汰辩论系统 - 5阶段流程

  

**核心流程：**

```

准备阶段 → 策划阶段 → 确认阶段 → 辩论阶段 → 交付阶段

   ↓         ↓         ↓         ↓         ↓

用户输入  领袖规划  用户确认  多轮辩论  总结报告

话题背景  初步方案  补充信息  N轮对话  委托人点评

```

  

**16个角色分组：**

- **必选角色（6个）**：杠精、行业专家、用户金主、第一性原理、风险管理师、资源整合者

- **可选角色（9个）**：时间穿越者、竞争对手、机会猎手、财务顾问、心理咨询师、法律顾问、技术极客、营销大师、哲学家

- **系统角色（1个）**：领袖（自动分配，组织辩论）

  

**文件位置：** `duomotai/src/config/roles.js`

  

### 2. 百问自测 - 三版本演进

  

- **V1**（`media-assessment-v1/`）：100个纯开放题，React项目，重思考

- **V2**（`media-assessment-v2/`）：混合题型（单选+文本），优化体验

- **V4**（`media-assessment-v4.html`）：**主要使用版本**，单文件部署，包含完整功能

  

**V4核心功能：**

- 用户信息采集 + 新老用户判断

- 100题五大维度答题（定位/用户/产品/流量/体系）

- 答题质量实时检测

- AI分析报告生成（多模型容错）

- 邮件发送报告

- 数据持久化（LocalStorage + 后端JSON）

  

### 3. AI服务多模型容错机制

  

**降级策略（server/services/aiService.js）：**

```

Qwen API → DeepSeek API → OpenAI API → 备用静态报告

```

  

**调用示例：**

```javascript

POST /api/ai/analyze

{

  "prompt": "分析内容",

  "model": "qwen"  // 可选，默认qwen

}

```

  

### 4. 环境配置要求

  

**必需配置（server/.env）：**

```env

# AI服务（至少配置一个）

QWEN_API_KEY=your_key

DEEPSEEK_API_KEY=your_key

OPENAI_API_KEY=your_key

  

# 邮件服务（推荐QQ邮箱免费方案）

EMAIL_SERVICE=qq

EMAIL_USER=your_qq_email@qq.com

EMAIL_PASS=your_authorization_code  # 注意：是授权码，不是QQ密码

  

# 服务端口

PORT=3000

```

  

## 常见开发任务

  

### 修改百问自测题目

**文件：** `html/projects/media-assessment-v4.html`（搜索 `const questions =`）

  

### 修改多魔汰角色配置

**文件：** `duomotai/src/config/roles.js`

  

### 添加新的API接口

**文件：** `server/server.js`

**示例：**

```javascript

app.post('/api/your-endpoint', async (req, res) => {

  try {

    // 实现逻辑

    res.json({ success: true, data: result });

  } catch (error) {

    res.status(500).json({ success: false, error: error.message });

  }

});

```

  

### 修改导航栏

**文件：** `index.html`, `baiwen.html`, `Projects.html`（搜索 `<nav>`）

  

### 调试AI服务

```bash

# 查看后端日志

cd server

npm run dev  # 控制台会显示详细日志

  

# 测试AI调用

curl -X POST http://localhost:3000/api/ai/analyze \

  -H "Content-Type: application/json" \

  -d '{"prompt":"测试","model":"qwen"}'

```

  

## 项目特殊约定

  

### 用户手机号特殊处理

**手机号 `13917895758` 标记为测试账号**

- 百问自测：标记为老用户（`media-assessment-v4.html`）

- 多魔汰：测试模式，固定验证码 `888888`

  

### 数据存储位置

- **前端数据：** LocalStorage（键格式：`user_{phone}`, `answers_{phone}`, `analysis_{phone}`）

- **后端数据：** `server/data/` 目录（JSON文件）

  

### 备份策略

- 修改HTML前自动备份（格式：`filename_YYYYMMDD_HHMMSS.html`）

- 示例：`index_20250930_234301.html`

  

### 版本管理策略

  

**重要版本完成后的版本管理流程：**

  

1. **识别版本完成时机：**

   - 完成一个重要功能模块（如：用户认证系统、辩论引擎等）

   - 准备开始新的重大功能开发前

   - 进行架构调整或重构前

  

2. **执行版本备份：**

   ```bash

   # 在相应目录下创建 Backup 文件夹（如果不存在）

   mkdir Backup

  

   # 移动旧版本文件到 Backup 文件夹

   # 文件命名格式：原文件名_YYYYMMDD_HHMMSS.扩展名

   # 示例：userAuth_20251001_011435.js

   ```

  

3. **Backup 文件夹位置：**

   - `duomotai/Backup/` - 多魔汰模块备份

   - `html/projects/Backup/` - 百问自测项目备份

   - `server/Backup/` - 后端服务备份

   - 根目录 `Backup/` - 配置文件和文档备份

  

4. **备份命名约定：**

   - 格式：`{原文件名}_{YYYYMMDD}_{HHMMSS}.{扩展名}`

   - 示例：

     - `userAuth_20251001_011435.js`

     - `index_20250930_234301.html`

     - `网站更新百问和多魔汰模块的框架及执行_v2_20251001_002733.md`

  

5. **自动执行提示：**

   当 Claude Code 检测到以下关键词时，应提醒执行版本备份：

   - "版本完成"、"准备开始新功能"、"重构"、"架构调整"

   - 完成 P0/P1 优先级任务后

   - progress.md 中标记为 "版本里程碑" 的任务完成后

  

### CORS配置

后端默认允许：

- `http://localhost:3000`

- `file://` 协议（本地HTML直接访问）

- 生产环境需配置 `ALLOWED_ORIGINS` 环境变量

  

## 重要文档参考

  

- **本地开发指南：** `本地开发启动指南.md`

- **详细执行计划：** `网站更新百问和多魔汰模块的框架及执行.md`

- **后端API文档：** `server/README.md`

- **项目进度跟踪：** `progress.md`

- **更新日志：** `UPDATE_LOG.md`

  

## 安全注意事项

  

1. **永远不要提交 `.env` 文件到版本控制**

2. **API密钥通过环境变量配置，不要硬编码**

3. **后端已配置速率限制（15分钟100请求）和Helmet安全头**

4. **生产环境需启用CSP（当前开发环境已禁用）**

  

## 部署架构

  

**当前（本地开发）：**

- 前端：Python HTTP Server (:8080)

- 后端：Node.js Express (:3000)

- 数据：本地JSON文件 + OneDrive同步

  

**生产环境建议：**

- 域名：rrxs.xyz

- 服务器：腾讯云轻量（2核4G，￥112/年）

- 反向代理：Nginx + Let's Encrypt SSL

- CDN：腾讯云CDN（静态资源加速）

- 进程管理：PM2

- 备份：OneDrive + Syncthing + GitHub私有仓库

  

## 性能优化目标

  

- 首屏加载时间 < 2秒

- Lighthouse评分 > 90

- 移动端适配优先（响应式设计）

- 懒加载图片和组件

- Service Worker离线缓存（待实现）

  

## 联系与资源

  

- **网站主页：** rrxs.xyz

- **问题反馈：** 通过网站"论坛&留言"提交

- **项目维护者：** 百问学长-RRXS

**Last Updated**: 2025-10-02 00:51