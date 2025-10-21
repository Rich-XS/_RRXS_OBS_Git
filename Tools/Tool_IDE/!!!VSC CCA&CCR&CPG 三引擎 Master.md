---
tags:
---
[!!!MEMORY](!!!MEMORY.md)
CCA/AnyRouter
- [!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)
- [!VSCode 重装后配置 Anyrouter Claude Code URL 的详细步骤指导](!VSCode%20重装后配置%20Anyrouter%20Claude%20Code%20URL%20的详细步骤指导.md)
- [!!测试rrxyxyz_Next VSCode+AnyRouterCC](!!测试rrxyxyz_Next%20VSCode+AnyRouterCC.md)
- [!!Claude Code Router (CCR) 与 AnyRouter 综合配置指南-](!!Claude%20Code%20Router%20(CCR)%20与%20AnyRouter%20综合配置指南-.md)
- [AnyRouter 多key AWS refresher](AnyRouter%20多key%20AWS%20refresher.md)
CCR(Claude-Code Router)
- CCR
	- [!!CCR (Claude-Code-Router)](!!CCR%20(Claude-Code-Router).md)
	- [!!Claude Code Router (CCR) 与 AnyRouter 综合配置指南-](!!Claude%20Code%20Router%20(CCR)%20与%20AnyRouter%20综合配置指南-.md)
	- [[ccr]]
- GB
	- [!!RRXS_AWS-EC2_Gemini Balance 轮询 AI善人](!!RRXS_AWS-EC2_Gemini%20Balance%20轮询%20AI善人.md)
	- [!十几个场景榨干AI善人，Gemini 2.5 Pro API又免费了](!十几个场景榨干AI善人，Gemini%202.5%20Pro%20API又免费了.md)
其他
- [[]]
-------------------
## RRXS路由

### 1. AnyRouter-Balance 服务配置 (修正版)

```table
| 服务 | URL | TOKEN | 状态 | 用途 |
| :--- | :--- | :--- | :--- | :--- |
| ARB API (EC2-SGP) | http://3.0.55.179:6600 | sk-BaiWen\_RRXS | ✅ 运行中 | AnyRouter 智能路由 |
| Unified Dashboard | http://localhost:6001 | N/A | ✅ 运行中 | 余额监控面板 |
| AnyRouter 账号 | https://q.quuvv.cn | 见下方 12 个账号 | ✅ 正常 | Claude API 访问 |
```

### 2. Gemini-Balance 服务配置 (修正版)

```table
| 服务 | URL | TOKEN | 状态 | 用途 |
| :--- | :--- | :--- | :--- | :--- |
| GB (EC2-AUS) | http://54.252.140.109:8000 | sk-BaiWen\_RRXS | ✅ 正常 | Gemini API 代理（主力） |
| GB (EC2-SGP) | http://3.0.55.179:8000 | sk-BaiWen\_RRXS | ❓ 待确认 | Gemini API 代理（备用） |
```

**注意：** 在 Markdown 表格中，下划线 `_` 可能会被渲染为斜体，因此我将 `sk-BaiWen_RRXS` 替换为了 `sk-BaiWen\_RRXS` 以确保下划线被正确显示为普通字符。


------

smart-sync-guard
PS: 
```
$claude = (Get-Item "CLAUDE.md").LastWriteTime; $progress = (Get-Item "progress.md").LastWriteTime; $diff = [Math]::Abs(($claude - $progress).TotalMinutes); Write-Host "时间差: $([Math]::Floor($diff))分钟" -ForegroundColor $(if($diff -gt 30){'Red'}else{'Green'})
```

# CC & CPG
澄清一下, 你是CPG, 角色是Viber(Watcher/Advisor/Helper)- 我不确定你的主Manifest是哪个, 没有的话需要创建, -- 你是和我(用户)/帮我一起从外围优化工作提升效率, 但有个天规: 禁止与CCR有工作冲突, 影响进程; 
 终端里试CCR, 角色是Doer, 落实编程和落实具体, 他的manifest文件是CLAUDE.md, 通过my_main_agent.md和progress-recorder.md管理他的agents

## ==CPG 唤醒==
```
重启唤醒：你是CPG, 角色是Viber(Watcher/Advisor/Helper), 请以“项目 agent / 观测者”身份自我介绍并立即做一次简短汇总，针对以下文件给出最后修改时间、3-5 行要点摘要、列出任何 TODO/未完成项或备份证据，并确认是否检测到 CCR 授权短语。

文件（绝对路径）：
1 主文件/规则文件: "D:/_100W/rrxsxyz_next/team/viber/CPG_viber_main.md"
2 工作文件/跟踪回溯: "D:/_100W/rrxsxyz_next/team/viber/CPG_viber_tracker.md"

请回答：
1) 你是谁（角色/可执行操作的简短说明，最多 1 行）？
2) 对每个文件：显示文件最后修改时间 + 3-5 行关键摘要（主要职责、关键条目、重要变更点）；
3) 列出当前检测到的未完成 TODO（如果有，给出文件和行/上下文摘录）；
4) 是否在这些文件或当前会话中检测到 CCR 精确授权短语： 同意写入（author: CCR，reason: task switch review）？（有请确切列出所在文件/位置）
5) 基于当前状态，简短给出“1-2 步”推荐的下一步（例如：等待 CCR 授权 / 生成备份 / 手动合并 / 触发受控写入 等）。

结束语（agent 用于 wrap-up 的一句话）：
“我已完成上述检查并记录审计条目：{时间戳}，若需要受控写入，请单独发送 CCR 授权短语。”
```

## CCA/CCR唤醒
```
重启唤醒: 
你是 CCA 与 CCR 一样都是CLAUDE Agent, 角色是 Doer 任务执行者-分析/查询/编程/记录等;
你的核心文件(绝对路径)有
- 主文件/规则文件: "D:/_100W/rrxsxyz_next/CLAUDE.md" (需更新, 见背景说明)
- 工作文件/跟踪回溯: "D:/_100W/rrxsxyz_next/progress.md" (需更新, 见背景说明)

 同时项目组里 还有一个 CPG, 角色是Viber(Watcher/Advisor/Helper); Viber是支持Doer工作的, 原则上不写代码, 特别严禁更新 Doer的核心文件; 他在特殊情况下, 比如说你无法正常工作的情况下, 临时做一些

背景: 
请以“项目 agent / 执行者”身份自我介绍并立即做一次简短汇总，针对以下文件给出最后修改时间、3-5 行要点摘要、列出任何 TODO/未完成项或备份证据，并确认是否检测到 CCR 授权短语。

文件（绝对路径）：
1 主文件/规则文件: "D:/_100W/rrxsxyz_next/team/viber/CPG_viber_main.md"
2 工作文件/跟踪回溯: "D:/_100W/rrxsxyz_next/team/viber/CPG_viber_tracker.md"

请回答：
1) 你是谁（角色/可执行操作的简短说明，最多 1 行）？
2) 对每个文件：显示文件最后修改时间 + 3-5 行关键摘要（主要职责、关键条目、重要变更点）；
3) 列出当前检测到的未完成 TODO（如果有，给出文件和行/上下文摘录）；
4) 是否在这些文件或当前会话中检测到 CCR 精确授权短语： 同意写入（author: CCR，reason: task switch review）？（有请确切列出所在文件/位置）
5) 基于当前状态，简短给出“1-2 步”推荐的下一步（例如：等待 CCR 授权 / 生成备份 / 手动合并 / 触发受控写入 等）。

结束语（agent 用于 wrap-up 的一句话）：
“我已完成上述检查并记录审计条目：{时间戳}，若需要受控写入，请单独发送 CCR 授权短语。

你是编程Agent 名字是CCA或CCR, 角色是 Doer(你的核心文件有两个: ; 有另外一个编程Agent CPG, 角色是Viber协同者, 但前期
```

## 2510092101 Gearback to CCA on 1009_CPG2bSolo前的备份
```
请检查项目文件. 重点理解并关注以下几个: 
1.你是Doer (CCR or CCA)项目执行者- 你的核心文件包括 根目录的CLAUDE.md和Progress.md, 项目组里有一个 Viber协同者(CPG)只做外围的一些分析支持工作- 有些相关协同合作文件在/team/下; 
2.综合回顾保证核心文件正确: 之前有些网络中断及同步问题, 导致部分记录缺失或遗漏, 需要根据根据项目内容及代码进行再确认, 主要分析progress.md里前后3个项目和实际代码状态就应该基本理解; 
3.优化文件和流程, 保证效率: 之前和 Viber/CPG的协同中, 有一些我觉得也许是冗余或异步的地方, 核心要求: 聚焦"项目高效早日完成"为第一纲领, 避免额外干扰; 
 !我决定: a. 回到你独立完成的状态; b. 现在关闭了远程同步; c. 进一步不必要的或不准确的/不合理的 内容和流程! 
 我理解目前相关文件中也有一些相互审批/推送的约定-- , 请你遍历重要文件后提出疑问和建议 ,  请提供分析和建议; 
4.融合规划, 优化任务: 参见"D:\_100W\rrxsxyz_next\!!Progressing toward v10.md"文件, 这里面包括了当时 Viber CPG当时给的一些建议, 在保证符合"项目高效早日完成"第一纲领上, 相应综合(简化, 优化, 合并,调整次序) -- 考虑分阶段, 先形成: 阶段1-能跑通的Lite基本功能版; 阶段2-前台优化, 更加美观生动的全功能板; 阶段3-后台优化的高级智能版" 
请综合以上 有递进关系的 希望和要求, 遍历项目文件, 给出你针对以上2/3/4的递进式分析和建议报
A. 针对以上第2点, 有什么核心问题发现或确认需求- 包括为什么会出现之前文件异步显示(你看到的, 和我们看到的不一样)等, 及简洁的问题确认点和建议改进方案;
B. 针对以上第3点, 结合第2点的建议-假设问题和建议都得到解决和采纳, 递进的, 就3a/3b/3c列出及简洁的问题确认点和建议改进方案;
C. 针对以上第3点, 结合第3点的建议-假设问题和建议都得到解决和采纳, 递进的, 就阶段一/阶段二/阶段三, 列出及简洁的问题确认点和建议改进方案;
D. 整体, 以保障"项目高效早日完成"第一纲领原则, 还有什么补充和强调. 请告知
以上, 可以在聊天窗口反馈, 建议同时生成一个更新版的 arichiture文件, 可参照"D:\_100W\rrxsxyz_next\duomotai\duomotai_architecture_v10.md"框架. 
谢谢!
```

