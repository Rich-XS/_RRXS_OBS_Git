  
理解（基于当前工作区 d:_100W\rrxsxyz_next 和活动文件 CLAUDE.md）

- 项目是个人品牌自媒体平台 rrxs.xyz，包含两大模块：百问自测（media-assessment）和多魔汰辩论系统（duomotai）。
- 前端有单文件 HTML 版本和若干 React 子项目；后端为 Node/Express，AI 服务有多模型容错（Qwen/DeepSeek/OpenAI）；数据以 JSON + LocalStorage 存储。
- 仓库内有一套项目记忆/Agent 约定（progress-recorder、CLAUDE.md、progress.md），以及文件同步与备份脚本（.claude/file-sync-guard.js、scripts/*.ps1）。
- 已定义详细的角色系统、交互流程、备份命名和运维建议，且有多次版本/变更记录（v5/v8 等）。

项目中我认为的核心规则文件（优先级顺序）

1. CLAUDE.md（当前活动文件） — 项目规则、约定、流程与变更准则（最高优先级）
2. [progress.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) / [progress.archive.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — 活动记忆与历史归档（必须通过 agent 更新）
3. .claude/agents/progress-recorder.md（或 agent 定义） — 记忆管理 agent 的实现/调用规范
4. [file-sync-guard.js](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — 文件同步监控脚本（L2 防护）
5. [roles.js](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — 16 角色定义（辩论系统核心）
6. [debateEngine.js](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — 辩论引擎核心逻辑（领袖 prompt、adjustStrategy 等）
7. [aiService.js](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — AI 多模型容错实现（Qwen/DeepSeek/OpenAI）
8. [server.js](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 与 [.env.example](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) — 后端路由与必需环境变量说明
9. scripts/TaskDone_BackUp_Exclude.ps1（或 Backup 脚本） — 备份规则与实现

如果由我独立完成接下来的项目：分阶段计划（精简）  
阶段 A — 初始审计与本地可跑环境（3 天）

- 任务：拉通项目结构、补齐 server/.env.example、安装依赖、启动前端（http.server）与后端（npm run dev），确认测试账号（13917895758）与固定验证码。
- 验证点：/health、AI analyze 接口、本地用户画像 API stub。

阶段 B — 修复/稳固核心规则与监控（2 天）

- 任务：确保 [CLAUDE.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 与 [progress.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 的同步机制可用（启用 .claude/file-sync-guard.js），确认 agent 定义与触发规则；添加/验证 pre-commit hook（可选）。
- 验证点：修改触发词后 agent 行为模拟，守护脚本无报错。

阶段 C — 后端 AI 服务与容错链实现（4-6 天）

- 任务：实现/完善 server/services/aiService.js，集成 DeepSeek 为主、Qwen/OpenAI 为降级；实现 /api/ai/analyze 接口与降级逻辑；增加速率/错误处理与可观测日志。
- 验证点：在 dev 环境模拟多模型失败场景，返回合理 fallback。

阶段 D — 多魔汰功能完备（5-8 天）

- 任务：完善 duomotai 的 userProfile、userAuth、debateEngine（adjustStrategy、confirmAndStart、领袖 system prompt），确保角色配置 roles.js 与 v8 要求一致；UI 按苹果风格微调。
- 验证点：完整准备→策划→确认→N 轮辩论→交付 流程可跑，生成 JSON 报告。

阶段 E — 百问自测整合与邮件/存储（3-5 天）

- 任务：确认 media-assessment-v4.html 的题库、AI 报告生成、邮件发送（emailService.js）、后端 JSON 持久化。
- 验证点：完成 100 题流程，AI 分析与邮件发送成功。

阶段 F — 测试、备份与部署（2-4 天）

- 任务：单元/集成测试、CI（可选）、备份脚本测试（TaskDone_BackUp_Exclude.ps1）、部署准备（PM2/Nginx）。
- 验证点：BACKUP_DONE 回执、性能目标（首屏 <2s）初步达成。

关键问题与需决策项（需回答/解决）

1. AI 凭证与成本：哪些 API key 可用（DeepSeek 优先），是否有使用额度或预算限制？
2. 测试/生产环境区分：是否需要线上域名与证书，部署目标环境是什么（腾讯云轻量机？）？
3. progress-recorder agent 的可运行方式：是自动化工具链（Task tool）还是手动脚本？谁有权限触发？
4. 数据保密与合规：用户数据（手机号/邮箱）是否加密，是否允许外部 AI 提供商存储敏感内容？
5. 接口规范：需实现的后端 API 列表与请求/响应格式（user/profile、auth、ai/analyze 等）的最终定义。
6. 验收标准：功能、性能、可用性与安全的具体通过标准（例如 10 轮辩论 tokens 上限、邮件送达率）。
7. 备份与排除规则确认：是否按 [CLAUDE.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 最新版排除 node_modules/.venv/logs？（CLAUDE.md 中有不同段落，需确认最终规则）
8. 人员与交接：是否需要把 agent/记忆变更交接为 Git 操作或 CI 流程防护（pre-commit hook）？

后续建议（快速可做项）

- 立刻运行：node .claude/file-sync-guard.js（在本地打开一个终端）以保证 [CLAUDE.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 与 [progress.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 同步监控。
- 补齐：在 server 下放一个 .env.example 并列出必须的 API key 环境变量。
- 明确：把 [progress.md](vscode-file://vscode-app/d:/Users/rrxs/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 的编辑权限与 agent 调用流程写成短流程图并放入 README（降低误用概率）。

如需，我可以直接：1) 在该工作区启动审计并列出缺失文件/接口；2) 生成启动步骤和必须的 .env.example；或 3) 修改/补充 debateEngine.js 的 adjustStrategy 与领袖 prompt（请指定下一步）。