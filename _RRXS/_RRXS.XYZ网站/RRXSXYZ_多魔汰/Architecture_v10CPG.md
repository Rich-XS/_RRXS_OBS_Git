## duomotai v10 — CPG更新（详尽可执行版）

更新时间：2025-10-09

概述
----
本文件面向 CCR（Doer）与 CPG（方案/脚本提供者），目标是把 duomotai v10 的架构目标和现有的项目治理（`CLAUDE.md`、`progress.md`、agent/pending-delta 流程）融合为一份直接可执行、易验证、低风险的交付规范。文档采用模块化结构：目标与验收、任务分解、脚本与模板、写入与回滚 runbook、验证用例、CI/部署建议、duomotai 特有工程项（角色卡/辩论引擎）等。

使用约定
----
- 所有对 `CLAUDE.md` / `progress.md` 的修改优先走 `\.claude/pending_delta.md` 审核流程。
- Agent 写入流程遵循：Acquire Lock -> Snapshot -> Merge Strategy -> Atomic Write -> Backup -> Audit -> Optional Git Commit（不自动 push）。
- 初始实现采用文件锁（PowerShell）与 NTFS 原子 rename。多节点场景再升级为 Redis 分布式锁。

一、目标与验收标准（明确定义 Done 条件）
----
主要目标
- 在不停止或影响 CCR 当前终端进程的前提下，完成 P0/P1 的自动化保护措施，并交付 duomotai v10 的最小可验证产品（MVP）：安全写入流水线 + 角色卡展示 + 基本辩论引擎接口。

验收标准（必须在 `progress.md` 中记录回执）：
1) scripts/atomicWrite.js 已就绪并能通过 temp->rename 实现原子写入；写入后 `.claude/audit.log` 有对应记录：WRITE_DONE + timestamp + author + reason + size。
2) scripts/lock.ps1 能正确 Acquire/Release（无死锁），在 30s 内失败会返回明确错误码与日志。
3) `.githooks/pre-commit` 放置于仓库且在测试分支验证通过（默认不启用 core.hooksPath）。
4) `.claude/pending_delta.example.md` 与 agent 写入示例已文档化。
5) duomotai 前端能加载并渲染 16 角色卡至少在本地运行通过（截图或录屏作为交付回执）。

二、最小可交付项（MVP）与时间建议
----
P0（24-72 小时内完成）
- T1 Atomic Write wrapper（scripts/atomicWrite.js）—— Node 脚本，支持命令行参数：--path --content-file --author --reason。工作量估 3。
- T2 Lock 实现（scripts/lock.ps1）—— PowerShell 脚本，支持 Acquire/Release/Status/Timeout。工作量估 2。
- T3 Pending-delta 模板与示例（.claude/pending_delta.example.md）—— 包含变更预览、目标区块、author/reason/timestamp、合并策略。工作量估 1。
- T4 duomotai 角色卡 JSON 模版与前端最小渲染（16 张卡，静态数据加载测试通过）。工作量估 4。

P1（1 周内完成）
- T5 Backup 集成（确认 scripts/TaskDone_BackUp_Exclude.ps1 作为 post-write 步骤并验证回执格式）。工作量 1。
- T6 pre-commit hook 文档与示例（.githooks/pre-commit）。测试分支验证并记录结果。工作量 2。
- T7 Diff-checker（可选）：写前对 delta 与目标文件行数差距做阈值阻断（20%）。工作量 3。

P2（2-4 周）
- T8 ContextDatabase MVP（轻量文件索引 + 简易搜索 API，为 summaryEngine 提供基础）。工作量 6。
- T9 SummaryEngine（自动摘要/裁剪引擎，API 接口设计与骨架实现）。工作量 6。

长期（可规划）
- 分布式锁（Redis）、CI 集成、可视化报表、全量审计查询界面。

三、增量融合（写入/回滚/审计）详尽流程
----
流程目标：保证自动化写入不会丢失历史、不会导致不同步、并且任何异常都有可回滚的快照。

步骤详解：
1) 生成 pending delta：Agent 将要写入的内容保存为 `\.claude/pending_delta_<ts>.md`，内容包含：
   - metadata：{id, author, timestamp, reason, targetFile, blockIdOrPath}
   - summary：一句话变更目的
   - diffPreview：上下文前后 5 行的变更示例
   - mergeStrategy：append | replace | patch

2) 人工/自动审核：CCR 审阅 pending delta；若同意，在文件或会话中写入批准短语：
   `同意写入（author: CCR，reason: <简述>）`

3) 写前快照（script）
   - 复制 targetFile 到 `.claude/snapshots/<file>.<ts>.bak`。
   - 记录 snapshot 元数据到 `.claude/snapshots/index.json`（方便回滚查找）。

4) Acquire lock
   - 调用 `scripts/lock.ps1 -Acquire -Name "progress-md-write" -Timeout 30`。
   - 若返回失败，写入 `.claude/last_write_receipt.md` 并通知触发会话。

5) 合并策略执行
   - 如果 mergeStrategy=append：把 delta 内容插入到目标区块末尾。
   - 如果 replace：计算 new/old 行数比，若减少 >20%，暂停并要求人工二次确认。
   - 如果 patch：按行匹配并替换对应片段。

6) 原子写入
   - 使用 `scripts/atomicWrite.js` 把合并后的内容写入临时文件并 rename 到目标路径（在 Windows/NTFS 上 rename 为原子操作）。
   - atomicWrite 也将写入 `.claude/audit.log`：一行 JSON 或 CSV 记录（见下）。

7) 立即触发备份
   - 执行 `scripts/TaskDone_BackUp_Exclude.ps1 -Keyword "post-write" -TaskId "<id>" -Execute`。
   - 记录 BACKUP_DONE 与 SIZE 到 `.claude/last_write_receipt.md`。

8) Release lock 与回执
   - 调用 `scripts/lock.ps1 -Release -Name "progress-md-write"`。
   - 把回执（WRITE_DONE, BACKUP_DONE, audit entry）写入触发会话或 `progress.md` 的 designated 回执区。

异常/回退策略
- 写入失败或备份失败：回退到 `.claude/snapshots/<file>.<ts>.bak`，并把失败原因写到 `.claude/last_write_receipt.md`，通知 CCR 并停止自动重试。
- 锁超时：返回错误，记录并不进行任何写操作。

审计日志格式（建议 JSON 每行）
示例条目：
{
  "ts":"2025-10-09T10:23:45.123Z",
  "action":"WRITE",
  "file":"progress.md",
  "author":"agent-x",
  "reason":"task update: T1",
  "size":12345,
  "snapshot":".claude/snapshots/progress.md.20251009102345.bak",
  "backup":".claude/backups/backup_20251009_102400.zip"
}

四、自动化脚本（草稿与示例）
----
下列脚本将由 CPG 草拟并放置于 `scripts/`，默认 commit 本地但不 push。CCR 审阅后决定启用或调整。

1) scripts/atomicWrite.js（Node, Windows 友好）
----
// scripts/atomicWrite.js
const fs = require('fs');
const path = require('path');

function usage() {
  console.log('Usage: node atomicWrite.js --path <target> --content-file <file> --author <author> --reason <reason>');
}

const argv = require('minimist')(process.argv.slice(2));
if (!argv.path || !argv['content-file']) {
  usage();
  process.exit(2);
}

const targetPath = path.resolve(argv.path);
const contentFile = path.resolve(argv['content-file']);
const author = argv.author || 'agent';
const reason = argv.reason || '';

function atomicWrite(targetPath, content, auditInfo={}) {
  const dir = path.dirname(targetPath);
  const base = path.basename(targetPath);
  const tmp = path.join(dir, `.${base}.tmp.${Date.now()}`);
  fs.writeFileSync(tmp, content, { encoding: 'utf8' });
  try {
    fs.renameSync(tmp, targetPath);
  } catch (err) {
    // attempt unlink tmp
    try { fs.unlinkSync(tmp); } catch(e){}
    throw err;
  }
  // audit
  const auditDir = path.join(process.cwd(), '.claude');
  if (!fs.existsSync(auditDir)) fs.mkdirSync(auditDir, { recursive: true });
  const auditFile = path.join(auditDir, 'audit.log');
  const line = JSON.stringify(Object.assign({
    ts: new Date().toISOString(),
    action: 'WRITE',
    file: targetPath,
    author: auditInfo.author || 'agent',
    reason: auditInfo.reason || '',
    size: Buffer.byteLength(content, 'utf8')
  })) + '\n';
  fs.appendFileSync(auditFile, line, { encoding: 'utf8' });
}

const content = fs.readFileSync(contentFile, 'utf8');
atomicWrite(targetPath, content, { author, reason });

console.log('WRITE_DONE', targetPath);

// End scripts/atomicWrite.js


2) scripts/lock.ps1（PowerShell 文件锁模板）
----
<#
Usage:
  - Acquire: powershell -File scripts\lock.ps1 -Acquire -Name "progress-md-write" -Timeout 30
  - Release: powershell -File scripts\lock.ps1 -Release -Name "progress-md-write"
#>
param(
  [switch]$Acquire,
  [switch]$Release,
  [string]$Name = 'progress-md-lock',
  [int]$Timeout = 30
)

$lockFile = Join-Path $env:TEMP ($Name + '.lock')
if ($Acquire) {
  $sw = Get-Date
  while (Test-Path $lockFile) {
    Start-Sleep -Seconds 1
    if ((Get-Date) - $sw -gt (New-TimeSpan -Seconds $Timeout)) {
      Write-Error "Lock timeout"
      exit 2
    }
  }
  '' | Out-File -FilePath $lockFile -Encoding utf8
  Write-Output "LOCK_ACQUIRED:$lockFile"
  exit 0
}
if ($Release) {
  if (Test-Path $lockFile) { Remove-Item $lockFile -ErrorAction SilentlyContinue }
  Write-Output "LOCK_RELEASED"
  exit 0
}

Write-Output "Usage: -Acquire|-Release -Name <name> [-Timeout <sec>]"


3) .githooks/pre-commit（示例 shell 脚本，默认不启用）
----
#!/bin/sh
# 如果修改了 CLAUDE.md 或 progress.md，则两者必须同时被修改或提供理由
STAGED=$(git diff --cached --name-only)
if echo "$STAGED" | grep -qE '^CLAUDE.md$|^progress.md$'; then
  echo "$STAGED" | grep -q '^CLAUDE.md$' && CLAUDE=1 || CLAUDE=0
  echo "$STAGED" | grep -q '^progress.md$' && PROG=1 || PROG=0
  if [ "$CLAUDE" -ne "$PROG" ]; then
    echo "Error: CLAUDE.md and progress.md must be updated together. If intentional, please add a signed reason file in .claude/" >&2
    exit 1
  fi
fi
exit 0


五、pending-delta 模板与示例
----
文件：`.claude/pending_delta.example.md`

---
id: pd-20251009-001
author: agent-v1
timestamp: 2025-10-09T10:00:00Z
reason: 更新 T1 atomic write 脚本说明文档
targetFile: progress.md
mergeStrategy: append
preview:
  - "@@ context before"
  - "+ 新增: atomicWrite.js 脚本说明"
  - "@@ context after"
---

变更内容示例（后续为实际追加内容）


六、duomotai 专属工程项（角色卡与辩论引擎）
----
1) 角色卡 JSON Schema（建议放在 `duomotai/src/data/roles.schema.json`）
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type":"string"},
    "name": {"type":"string"},
    "type": {"type":"string","enum":["core","external","value"]},
    "summary": {"type":"string"},
    "goals": {"type":"array","items":{"type":"string"}},
    "persona": {"type":"string"},
    "example_prompt": {"type":"string"},
    "ui": {"type":"object"},
    "priority": {"type":"integer","minimum":1,"maximum":5}
  },
  "required": ["id","name","type","summary","persona","example_prompt","ui"]
}

2) 前端集成（MVP）要点
- 把角色数据放在 `duomotai/public/data/roles.json`，并在首页展示卡片网格。
- 每张卡应展示 name / summary / priority / avatar；点击弹出 persona 与 example_prompt。

3) 辩论引擎接口（简易协议）
- POST /api/debate/start {sessionId, participants: [roleId...], topic, initiator}
- POST /api/debate/round {sessionId, roundIndex, actions: [{roleId, action, content}...]}
- GET /api/debate/state?sessionId=xxx

七、验证用例（Smoke tests & Acceptance tests）
----
Smoke Test 1: atomic write 全流程
1) 准备：创建 `.claude/pending_delta_test.md` 包含简单 append 文本。
2) Acquire lock：`powershell -File scripts/lock.ps1 -Acquire -Name progress-md-write -Timeout 10`。
3) 执行 atomic write：`node scripts/atomicWrite.js --path progress.md --content-file .\\claude\\pending_delta_test.md --author cpg --reason smoke-test`
4) 验证：`.claude/audit.log` 包含最近一条 WRITE，`.claude/snapshots` 包含快照，备份脚本返回 BACKUP_DONE（如已集成）。

Acceptance Test 1: pre-commit 验证
1) 在测试分支上启用 hooksPath：`git config core.hooksPath .githooks`
2) 模拟只修改 CLAUDE.md：`git add CLAUDE.md && git commit -m "test"` 应被阻止。

辩论引擎测试
- 启动后端 stub，POST /api/debate/start -> 返回 sessionId -> 调用 /api/debate/round 多轮，保证状态可查询与导出 JSON 报告。

八、CI / 部署 & 运行建议
----
- CI（建议 GitHub Actions 示例）
  - job: lint & test
  - job: smoke-tests（运行 atomicWrite smoke test 与 pre-commit hook 测试）
  - job: build & deploy（由 CCR 人工触发或需 review 批准）

- 部署
  - 后端使用 PM2 或 node process manager；前端静态文件放 nginx 或静态主机。
  - 环境变量：把 AI keys、mail creds 等放在 `.env`（不要提交）并提供 `.env.example`。

九、风险评估与缓解
----
- 风险 1：自动写入误覆盖历史
  - 缓解：写前快照 + 阈值校验 + 人工批准（默认不开自动 push）。
- 风险 2：锁失效或死锁
  - 缓解：锁加超时控制，失败回退并通知。
- 风险 3：AI 调用失败影响功能链
  - 缓解：实现模型降级和本地缓存策略，并在 server 中记录失败次数与报警。

十、待决问题（需要 CCR 指示）
----
1) 是否允许 agent 提交后自动创建并 push git commit？（建议：否）
2) 备份文件的远端存储（S3/云盘）策略与保留周期是多少？
3) 是否在仓库内启用 `.githooks` 为默认 hooksPath？

十一、交付清单（CPG 提供）
----
- scripts/atomicWrite.js（草稿）
- scripts/lock.ps1（草稿）
- .githooks/pre-commit（示例）
- .claude/pending_delta.example.md
- duomotai/src/data/roles.schema.json
- smoke test 文档 `.claude/test_run_<ts>.md`

十二、下一步建议（我 CP G 的执行选项）
----
请选择其中之一：
- 开始执行：我将把上列脚本写入 `scripts/` 并本地 commit（不 push），并运行 smoke-test，生成回执到 `.claude/test_run_<ts>.md`。
- 只给脚本：我把脚本内容直接贴到回复，你手动部署并运行验证。
- 先看草稿：我仅生成 `\.claude/pending_delta.example.md` 与脚本清单供你审阅，不改仓库。

----

附录：CPG 作为独立 Doer（无 CCR 参与）—— 前期工作、文件框架与逐步执行计划
====

说明（范围限定）
- 本节专门说明当 CPG 作为“独立 Doer”承担全部实现工作时的前期准备、文件布局、执行约束与逐步操作清单。当前阶段仅用于规划与文档落地：CPG 仅更新 `duomotai_architecture_v10CPG.md`（此文件），不对仓库其它文件或进程做任何直接操作，除非得到明确指令。该说明的目标是：当 CCR 不可用或授权 CPG 独立完成任务时，提供一套可执行、安全、可审计的操作手册。

一、为什么需要“CPG 作为独立 Doer”的计划？
- 背景：仓库中许多流程与触发假定 CCR（终端运行者/Claude-Code）会参与审阅或批准，但在 CCR 无法参与时，项目不能停滞。CPG 需要在不越权、不破坏历史审计、并可回滚的前提下独立交付 P0/P1 项目需求。
- 目标：定义 CPG 在独立执行时的边界（哪些可做、哪些必须等待 CCR）、前期稽核步骤、文件与目录布局、变更记录格式与审批替代策略。

二、权限与边界（必须严格遵守）
- CPG 可独立完成（无需 CCR 实时参与）的操作：
  - 在本地仓库分支上创建与修改脚本、模板、文档（如 `scripts/atomicWrite.js`、`.githooks/pre-commit`、`.claude/pending_delta.example.md`、`duomotai/src/data/roles.schema.json`）。
  - 运行本地 smoke-tests 并生成测试回执文件（写入 `.claude/test_run_<ts>.md`）。
  - 提交本地 commit（必须使用私有分支，默认不 push 远端）。

- CPG 不得在未获 CCR 或项目所有者明确授权下执行的操作（必须等待人工授权）：
  - 直接覆盖 `progress.md` 或 `CLAUDE.md` 的主分支写入与 push。
  - 在主分支启用或强制生效 Git hooksPath（`git config core.hooksPath`）。
  - 自动化推送（push）或创建带关键变更的远程 PR（除非事先沟通并授权）。

三、前期检查清单（Pre-flight audit）
（CPG 在开始编码/撰写脚本前必须完成以下核查并把结果记录到此文档或 `.claude/preflight_<ts>.md`）

1) 仓库状态确认
  - 确认当前分支（建议使用 `ccr/test-enable-hooks` 或另建 `cpg/<feature>-<date>`）。
  - 列出未提交变更：`git status --porcelain`（确保 workspace 干净，或把需要的改动放到临时 stash）。
  - 获取 `progress.md` 与 `CLAUDE.md` 的最新 HEAD（保存为快照以便记录）。

2) 运行时/进程敏感性评估
  - 确认本地运行的守护进程（如 Smart File Sync Guard）不会与写入脚本冲突；若存在，记录风险并选择非高峰时段执行本地 smoke test。

3) 环境准备
  - Node、npm、PowerShell 可用并在 PATH 中。
  - 在本地创建工作分支：`git checkout -b cpg/v10-scripts-<ts>`。

4) 记录审计基线
  - 复制当前 `progress.md` 与 `CLAUDE.md` 到 `.claude/preflight_snapshots/` 并在文档中记录文件大小、行数、最后更新时间。

四、文件框架（CPG 建议默认布局）
（CPG 独立实施时按下列布局放置所有生成或修改的文件，便于 CCR 审核）

根目录（推荐）
- scripts/                — CPG 提交的所有工具脚本（atomicWrite.js、lock.ps1、diff-checker.js）
- .githooks/              — pre-commit 示例（默认不启用）
- .claude/                — agent 与审计文件夹（audit.log、pending_delta.example.md、snapshots/、test_run_*.md）
- duomotai/src/data/      — 角色卡、schema、静态 role JSON
- duomotai/duomotai_architecture_v10CPG.md  — 本文件（CPG 变更记录）

细节说明：
- `.claude/snapshots/`：写前快照（按 ISO 时间戳命名），用于回滚与审计索引。
- `.claude/audit.log`：每次自动写入与手动关键事件均以单行 JSON 记录。
- `.claude/pending_delta/`：存放 CPG 为自动 agent 或 CCR 审阅准备的 pending delta 文件（每个 delta 有 metadata 与 preview）。

五、CPG 独立执行的详细步骤（逐条、可直接复制到操作手册）
（注意：下面步骤仅用于文档与计划，CPG 在未获得进一步明确授权前仅更新本文档）

阶段 0 — 初始化（文档/分支/快照）
1) 在本地创建工作分支：
   - git checkout -b cpg/v10-cpg-doer-<YYYYMMDDHHmm>
2) 生成 preflight 快照并写入 `.claude/preflight_<ts>.md`：
   - 记录 `git rev-parse HEAD`、`ls -la scripts`、`Get-ChildItem .claude`（PowerShell）等输出。
3) 在 `.claude/` 中建立 `pending_delta/` 子目录（如果不存在），并写入 `pending_delta.example.md` 模板供 CCR 审阅。

阶段 1 — 编写与本地提交脚本/文件（不 push）
4) 在 `scripts/` 中创建草稿脚本：`atomicWrite.js`、`lock.ps1`、`diff-checker.js`（或 Node/Powershell 两种实现）。
5) 在 `.githooks/` 中放置 `pre-commit` 示例脚本（默认不启用）。
6) 在 `duomotai/src/data/` 中放置 `roles.schema.json` 与 `roles.json`（MVP 16 角色数据）。
7) 本地执行轻量 smoke-tests（见下文），并把输出写入 `.claude/test_run_<ts>.md`。
8) 本地 commit 所有变更：
   - git add scripts/ .githooks/ .claude/ duomotai/src/data/
   - git commit -m "cpg: add atomic write, lock scripts, pending_delta template, roles schema (local commit)" 
   说明：必须明确在 commit message 中写明“local commit / do not push”。

阶段 2 — 内部自测与回执生成（CPG 内部验证）
9) 运行 smoke-test（atomic write 全流程，非主分支）：
   - Acquire lock（scripts/lock.ps1 -Acquire）
   - 生成 pending delta 文件（.claude/pending_delta/test-<ts>.md）
   - 使用 atomicWrite.js 将合并后的内容写入临时目标文件（测试目标建议为 `progress.test.md` 而不是主 `progress.md`）
   - 验证 `.claude/audit.log`、`.claude/snapshots/`、`.claude/test_run_<ts>.md` 的回执条目
10) 如果 smoke-test 失败，记录错误到 `.claude/test_run_<ts>.md` 并修正脚本后重试。

阶段 3 — 生成审阅包交付给 CCR（或管理员）
11) 生成审阅包（审阅用的 pending delta 与变更说明）：
   - 把 `.claude/pending_delta/<pd>.md`、scripts/、roles.json、test_run.md 压缩为 `cpg_review_<ts>.zip`（放在 `.claude/review/`）。
12) 在本文件末尾追加审阅摘要与回执路径（供 CCR 人工审核）。

阶段 4 — 等待授权与后续（如果 CCR 授权）
13) 若 CCR 回复精确授权短语 `同意写入（author: CCR，reason: <...>）`，则 CPG 可按增量融合流程把 pending delta 通过 atomicWrite 写入目标文件，并执行备份与审计；否则 CPG 仅把审阅包提交为 PR 或把变更放在 `.claude/review/` 中。
14) 如果 CCR 不回复，CPG 可选择把审阅包直接创建为 `draft PR`（非合并）并通知 CCR。但未经明确授权不得合并或 push 到主分支。

六、替代审批与紧急授权策略（在 CCR 无法及时响应时）
- 情境：CCR 短期无法响应，但有迫切安全或回滚需要（例如发现 data-loss 或安全漏洞），CPG 可依据下列紧急授权流程执行写入：
  1) CPG 在 `\.claude/emergency_authorization.md` 中记录事件详情、为什么需要紧急操作、影响范围与变更内容。
  2) CPG 发送电子邮件或即时消息到项目所有者与维护组（保留通信记录）。
  3) 若在 2 小时内收到 1 名以上维护者（含项目 owner）的书面同意（电子邮件或聊天记录），CPG 可执行写入并在操作完成后把所有通信记录与回执附入 `\.claude/emergency_log.md`。
 说明：该流程用于极端紧急情况，且必须保留完整审计链。

七、验证矩阵（每项变更必须至少通过其中一个验证点）

变更类型 | 本地 smoke-test | `.claude/audit.log` | snapshot 存在 | CCR 授权 | 备注
---|---:|---:|---:|---:|---
脚本/文档(非核心) | 必须 | 可选 | 可选 | 不必要 | CPG 可直接提交本地 commit
pending_delta (待写入) | 必须（在 test 文件上） | 必须 | 必须 | 推荐（正式写入前） | 为写入做准备
核心文件写入 (progress.md/CLAUDE.md) | 强制（在 test 上） | 强制 | 强制 | 必须 | 除非紧急流程得到书面授权

八、交付与验收（CPG 完成独立 Doer 所需交付）
- 交付物清单（放在 `.claude/review/<ts>/`）：
  1) scripts/atomicWrite.js（注释齐全）
  2) scripts/lock.ps1（注释齐全）
  3) .githooks/pre-commit（示例）
  4) .claude/pending_delta/*.md（待写入 delta）
  5) duomotai/src/data/roles.json + roles.schema.json
  6) .claude/test_run_<ts>.md（smoke-test 输出）
  7) .claude/preflight_<ts>.md（初始化快照与环境说明）

验收条件（由 CCR 或项目 owner 审核）
- 文件齐全且说明清楚
- smoke-test 通过（或有明确失败记录与修复计划）
- 审阅包包含回滚步骤（snapshot 路径）与审计日志条目

九、时间估算（CPG 独立执行，常规节奏）
- 阶段 0（准备）：1-3 小时
- 阶段 1（脚本与本地提交）：3-6 小时
- 阶段 2（自测与修正）：1-4 小时（视失败次数而定）
- 阶段 3（打包审阅）：0.5-1 小时
- 总计（P0 全套交付）：6-14 小时

十、示例条目与模板（便于 CCR 审阅快速理解）

1) `.claude/preflight_<ts>.md`（示例）
```
Preflight Snapshot: 2025-10-09T12:00:00Z
branch: cpg/v10-cpg-doer-202510091200
git HEAD: abcdef1234567890
files snapshot:
  - progress.md lines: 1200 size: 23456
  - CLAUDE.md lines: 868 size: 43210
processes:
  - Smart File Sync Guard: running (pid 1234)
notes: performing non-invasive local operations only. no push.
```

2) `.claude/test_run_<ts>.md`（示例）
```
Test Run: atomic write smoke-test
ts: 2025-10-09T12:30:00Z
steps:
  - lock acquire: PASS
  - atomicWrite to progress.test.md: PASS
  - audit.log appended: PASS
  - snapshot created: PASS (.claude/snapshots/progress.test.md.20251009T123000.bak)
  - backup invoked (TaskDone_BackUp_Exclude): SKIPPED (not run in local smoke)
result: SUCCESS
notes: ready for review
```

十一、文档更新与变更记录规范（写给 CCR 与未来的 CPG）
- 每次 CPG 对本文件或相关脚本做变更时，必须在文件顶部 `更新时间` 字段更新并在 `.claude/change_log.md` 中追加条目，条目包含：作者、时间、变更摘要、回滚路径。

十二、结语（仅限计划/文档更新阶段）
- 本节为 CPG 作为独立 Doer 的完整前期与执行计划草案，目的在于保证在 CCR 不可及或授权 CPG 独立推进时，仍能维持项目的审计纪律与最低风险保障。当前阶段 CP G 仅更新此规划文档（`duomotai_architecture_v10CPG.md`），不对仓库中其他文件做自动化或强制变更。

----
—— End of CPG 更新 —
