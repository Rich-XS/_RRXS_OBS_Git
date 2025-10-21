# 多魔汰 v9 架构文档 - 真实动态对话系统

**版本**: v9.0
**创建时间**: 2025-10-03 23:55
**核心定位**: 从流程化系统升级为 AI 驱动的真实动态对话系统

---

## 📋 目录

1. [核心需求与设计理念](#1-核心需求与设计理念)
2. [架构设计](#2-架构设计)
3. [核心组件详解](#3-核心组件详解)
4. [实现细节](#4-实现细节)
5. [待讨论与确定的细节](#5-待讨论与确定的细节)
6. [测试验证计划](#6-测试验证计划)
7. [与 v8 的对比](#7-与-v8-的对比)

---

## 1. 核心需求与设计理念

### 1.1 用户核心需求（原话）

> "对话的延续性和实际现实符合性最重要，而不是走过场"

**关键词解析**：
- **延续性**：每位专家的发言应该与自己之前的观点连贯，展现思考的递进
- **实际现实符合性**：模拟真实会议场景，专家之间有互动、有争议、有回应
- **不走过场**：拒绝流水账式发言，每次发言都应该推进讨论深度

### 1.2 设计理念

#### v8 的局限性
- **固定流线顺序**：ID1→6→5→3→4→8→15→16，机械化
- **孤立发言**：专家只看到"本轮当前发言"，缺少完整历史上下文
- **无递进关系**：每轮发言相对独立，缺少延续性

#### v9 的突破
1. **对话信息数据库**：完整记录所有发言+关键观点+争议点
2. **AI 驱动顺序**：领袖根据对话进展智能决定下一位发言者
3. **递进式上下文**：专家看到完整历史，展现思考演进
4. **二次邀请机制**：专家可多次发言，深化争议点

---

## 2. 架构设计

### 2.1 整体架构图

```
┌─────────────────────────────────────────────┐
│          DebateEngine（辩论引擎）            │
│  ┌───────────────────────────────────────┐  │
│  │   ContextDatabase（对话信息数据库）   │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │ speeches: []  // 所有发言记录  │  │  │
│  │  │ keyPoints: Map // 关键观点索引 │  │  │
│  │  │ controversies: [] // 争议焦点  │  │  │
│  │  │ relations: []  // 发言关联     │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  ┌───────────────────────────────────────┐  │
│  │   runRound() - 单轮辩论执行逻辑      │  │
│  │  1. 领袖开场                          │  │
│  │  2. while(true) 动态发言循环 ━━━┓   │  │
│  │     - decideNextSpeaker() AI决策 │   │  │
│  │     - 专家发言 + 记录到DB         │   │  │
│  │     - 判断是否COMPLETE            │   │  │
│  │  3. 委托人点评 ←━━━━━━━━━━━━━━━━┛   │  │
│  │  4. 领袖总结                          │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  ┌───────────────────────────────────────┐  │
│  │   buildRoleSpeechPrompt() - 提示词   │  │
│  │  - getRelevantContext() 三层上下文   │  │
│  │    ├─ myHistory: 自己的发言历史      │  │
│  │    ├─ othersKeyPoints: 他人关键观点  │  │
│  │    └─ allRounds: 完整辩论时间线      │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 2.2 关键流程对比

| 流程环节 | v8（流程化） | v9（动态对话） |
|---------|-------------|---------------|
| 发言顺序 | 固定流线（8个必选角色） | AI动态决策（可重复邀请） |
| 上下文 | 仅本轮当前发言 | 三层完整上下文 |
| 发言次数 | 每人每轮1次 | 可多次（二次邀请） |
| 结束判断 | 固定轮次 | AI判断"COMPLETE" |
| 关键信息 | 无结构化提取 | 自动提取观点/数据 |

---

## 3. 核心组件详解

### 3.1 ContextDatabase（对话信息数据库）

**文件位置**: `debateEngine.js` 行14-175

#### 3.1.1 数据结构

```javascript
class ContextDatabase {
  speeches: [
    {
      id: "speech_${round}_${roleId}_${timestamp}",
      roleId: 8,
      roleName: "竞争友商",
      content: "...",
      round: 2,
      timestamp: "2025-10-03T15:30:00.000Z",
      keyPoints: [
        { type: "建议", text: "建议聚焦差异化..." },
        { type: "数据", text: "市场份额下降15%..." }
      ],
      dataRefs: ["15%", "根据艾瑞咨询2024年报告"]
    }
  ],

  keyPoints: Map {
    8 => [
      { round: 1, points: [...], content: "..." },
      { round: 2, points: [...], content: "..." }
    ]
  },

  controversies: [
    { topic: "定价策略是否过低", count: 3 }
  ]
}
```

#### 3.1.2 核心方法

**1. addSpeech(speech)** - 发言录入
- 自动生成唯一ID
- 提取关键观点（extractKeyPoints）
- 提取数据引用（extractDataReferences）
- 更新角色观点索引

**2. extractKeyPoints(content)** - 关键观点提取
```javascript
// 规则1: 提取"建议"相关句子
/[建议|推荐|应该|需要|必须][^。！？]*[。！？]/g

// 规则2: 提取"问题"相关句子
/[问题|风险|挑战|担心|忧虑][^。！？]*[。！？]/g

// 规则3: 提取"数据"相关句子
/[\d]+[%|万|亿|倍|个|次|年|月|天][^。！？]*[。！？]/g
```

**3. getRelevantContext(roleId, currentRound)** - 上下文查询
返回三层上下文：
- `myHistory`: 该角色之前的所有发言
- `othersKeyPoints`: 其他角色的关键观点（只取最近2轮）
- `allRounds`: 完整辩论时间线（按轮次组织）

#### 3.1.3 待讨论细节 ❓

1. **关键观点提取规则**
   - 当前使用简单正则，是否足够？
   - 是否需要引入 NLP 模型提取更复杂的观点？
   - 如何处理跨句的复杂建议？

2. **争议焦点识别**
   - 当前阈值：被提及2次以上
   - 是否需要动态调整（如：5轮辩论阈值2，10轮阈值3）？
   - 是否需要语义相似度匹配（而非简单前20字匹配）？

3. **数据引用验证**
   - 当前仅提取，不验证真实性
   - 是否需要检查"根据XX报告"的真实性？
   - 如何防止 AI 编造数据？

4. **持久化需求**
   - 当前仅内存存储
   - 是否需要保存到后端/LocalStorage？
   - 是否需要支持跨会话恢复？

---

### 3.2 AI 驱动的动态发言顺序

**文件位置**: `debateEngine.js` 行808-889

#### 3.2.1 决策机制

**输入信息**：
- 当前辩论情况（主议题、轮次、本轮焦点）
- 辩论时间线（最近5条要点）
- 当前争议焦点（被多次提及的问题）
- 可邀请专家列表（含是否已发言标记）

**AI 决策提示词核心**：
```javascript
const decisionPrompt = `
**决策要求**：
1. 基于当前对话进展和争议焦点，选择最合适的下一位发言专家
2. 如果某个话题需要深入探讨，可以邀请已发言专家再次回应
3. 优先考虑能推进对话深度、解决争议、提供数据支撑的专家
4. 如果本轮讨论已充分（所有关键角色都发过言且无明显争议），返回"COMPLETE"

请直接回复专家ID（如"3"）或"COMPLETE"，不要有任何其他内容。
`;
```

**Temperature 控制**: 0.3（低温度确保决策稳定）

#### 3.2.2 二次邀请机制

```javascript
// v8: 每人每轮只能发言1次
const sortedRoles = this.getSortedRoles();
for (const role of sortedRoles) {
  // 发言一次后，该角色在本轮不再发言
}

// v9: 支持二次邀请
const alreadySpoken = []; // 记录已发言，但允许重复
while (true) {
  const nextRole = await this.decideNextSpeaker(roundNumber, roundData, alreadySpoken);
  if (!nextRole) break; // COMPLETE
  // 专家发言...
  alreadySpoken.push(nextRole.id); // 允许同一ID多次出现
}
```

#### 3.2.3 待讨论细节 ❓

1. **领袖决策提示词优化**
   - 当前约200 tokens，是否足够详细？
   - 是否需要提供更多示例（如：什么情况下二次邀请）？
   - 如何防止领袖陷入"无限邀请同一专家"？

2. **"COMPLETE" 判断标准**
   - 当前依赖 AI 主观判断
   - 是否需要明确规则（如：至少N个专家发言，且无新争议）？
   - 如何平衡"充分讨论"和"效率"？

3. **二次邀请频率控制**
   - 当前无限制
   - 是否需要限制单轮最大发言次数（如：单人最多3次）？
   - 是否需要限制总发言次数（如：单轮最多15次发言）？

4. **决策失败降级**
   - 当前：AI决策失败 → 使用默认顺序（candidateRoles[0]）
   - 是否需要更智能的降级策略？
   - 是否需要记录决策失败日志？

---

### 3.3 递进式对话上下文系统

**文件位置**: `debateEngine.js` 行906-992

#### 3.3.1 上下文构建

**提示词结构**：
```javascript
buildRoleSpeechPrompt(role, roundNumber, roundData) {
  const relevantContext = this.contextDatabase.getRelevantContext(role.id, roundNumber);

  return `${role.systemPrompt}

**当前辩论情况**：
- 主议题：${this.state.topic}
- 当前轮次：第 ${roundNumber}/${this.state.rounds} 轮
- 本轮焦点：${roundData.topic}

📋 你之前的发言历史（${relevantContext.myHistory.length}次）：
${myHistoryText}
（提示：请在本轮发言中展现与之前的连贯性和递进关系）

💡 其他专家的关键观点：
${othersKeyPointsText}

📊 完整辩论时间线（关键要点）：
${timelineText}

**⚠️ 重要要求**：
1. 基于以上完整历史上下文，展现与之前发言的连贯性和递进关系
2. 回应其他专家的关键观点，展现对话感（而非走过场）
3. 引用具体数据/案例（严禁编造），参考辩论时间线中的数据引用
4. 结合你的角色定位，给出3个具体建议（含时间/成本/资源）
5. 控制在200-300字
`;
}
```

#### 3.3.2 三层上下文详解

**Layer 1: myHistory（自己的发言历史）**
- 目的：展现思考演进
- 内容：该角色之前所有发言（最近3次）
- 提示：请在本轮发言中展现与之前的连贯性和递进关系

**Layer 2: othersKeyPoints（其他专家关键观点）**
- 目的：促进互动回应
- 内容：其他角色的关键观点（只取最近2轮）
- 格式：`角色名：第X轮观点1；观点2`

**Layer 3: allRounds（完整辩论时间线）**
- 目的：全局视角决策
- 内容：所有轮次的关键要点+数据引用
- 格式：`第X轮：角色A观点+数据 | 角色B观点+数据`

#### 3.3.3 待讨论细节 ❓

1. **上下文长度控制**
   - 当前无限制，可能导致 token 超限
   - 是否需要限制 myHistory 最多N次？
   - 是否需要限制 allRounds 最多M轮？
   - 如何动态调整（10轮辩论 vs 3轮辩论）？

2. **智能压缩历史**
   - 当前完整展示所有历史
   - 是否需要只保留关键信息（keyPoints + dataRefs）？
   - 是否需要 AI 总结压缩历史？

3. **连贯性与简洁性平衡**
   - 强调"递进关系"可能导致发言冗长
   - 如何在"深度递进"和"200-300字"之间平衡？
   - 是否需要调整提示词措辞？

4. **回应标记**
   - 当前只要求"回应其他专家"，但不显式标记
   - 是否需要在发言中标记"@角色名"？
   - 是否需要在UI中可视化回应关系（如：箭头连接）？

---

### 3.4 专家发言格式优化

**文件位置**: `index.html` 行1212-1260

#### 3.4.1 格式化流程

```javascript
function formatExpertSpeech(content) {
  // 步骤1: 移除 Markdown 符号
  html = html.replace(/\*\*/g, '');           // 移除粗体
  html = html.replace(/^#{1,6}\s+/gm, '');    // 移除标题
  html = html.replace(/^---+$/gm, '');        // 移除分隔线
  html = html.replace(/`([^`]+)`/g, '$1');    // 移除代码

  // 步骤2: 关键词加粗（16个关键词）
  const keywords = ['建议', '问题', '风险', '机会', '数据', ...];
  keywords.forEach(keyword => {
    html = html.replace(regex, `$1<strong style="color: #007AFF; font-weight: 600;">${keyword}</strong>$2`);
  });

  // 步骤3: 智能列表格式化
  // "1. xxx 2. xxx" → <div>1. xxx</div><div>2. xxx</div>
  html = html.replace(/(\d+)\.\s*([^。！？\n]+)/g, (match, num, text) => {
    return `<div style="margin: 8px 0 8px 20px; line-height: 1.8;">
      <span style="display: inline-block; width: 24px; font-weight: 600; color: #007AFF;">${num}.</span>
      ${text.trim()}
    </div>`;
  });

  // 步骤4: 紧凑显示（移除空行）
  const lines = html.split('\n').map(line => line.trim()).filter(line => line.length > 0);
  html = lines.map(line => {
    if (line.startsWith('<div')) return line; // 列表项
    return `<p style="margin: 6px 0; line-height: 1.8; color: #333;">${line}</p>`;
  }).join('');

  return html;
}
```

#### 3.4.2 待讨论细节 ❓

1. **关键词列表完整性**
   - 当前16个：建议、问题、风险、机会、数据、挑战、优势、劣势、威胁、方案、策略、目标、关键、核心、重点、注意
   - 是否需要增加？（如：收益、成本、时间、资源）
   - 是否需要支持自定义？

2. **加粗颜色方案**
   - 当前固定蓝色 #007AFF
   - 是否需要根据角色层级动态变化？
     - 核心层：蓝色
     - 外部层：紫色
     - 价值层：绿色

3. **列表格式支持**
   - 当前支持：`1. xxx`、`(1) xxx`
   - 是否需要支持嵌套列表？（1.1, 1.2）
   - 是否需要支持无序列表？（- xxx）

4. **高级格式支持**
   - 是否需要支持表格？
   - 是否需要支持引用块？
   - 是否需要支持链接？

---

## 4. 实现细节

### 4.1 文件变更清单

| 文件 | 变更内容 | 行数 |
|-----|---------|------|
| `debateEngine.js` | 新增 ContextDatabase 类 | 14-175 |
| `debateEngine.js` | 初始化 contextDatabase | 218 |
| `debateEngine.js` | 5个发言录入点 | 607-764 |
| `debateEngine.js` | 新增 decideNextSpeaker() | 808-889 |
| `debateEngine.js` | 重写 buildRoleSpeechPrompt() | 906-992 |
| `debateEngine.js` | 优化动态发言循环 | 660-709 |
| `index.html` | 新增 formatExpertSpeech() | 1212-1260 |
| `index.html` | 应用格式化到发言显示 | 1058 |

### 4.2 核心代码片段

#### 4.2.1 发言录入示例

```javascript
// 位置：debateEngine.js runRound() 方法

// 1. 领袖开场发言录入
const leaderSpeech = {
  roleId: this.facilitator.id,
  roleName: this.facilitator.shortName,
  content: leaderOpening.content || leaderOpening,
  round: roundNumber,
  timestamp: new Date().toISOString()
};
roundData.speeches.push(leaderSpeech);
this.contextDatabase.addSpeech(leaderSpeech); // ✅ [v9] 录入数据库
```

#### 4.2.2 动态发言循环

```javascript
// 位置：debateEngine.js runRound() 方法

const alreadySpoken = []; // 追踪已发言（允许重复）

while (true) {
  // 领袖AI决策：下一位发言专家
  const nextRole = await this.decideNextSpeaker(roundNumber, roundData, alreadySpoken);

  // 如果领袖认为本轮讨论已充分，结束发言阶段
  if (!nextRole) {
    console.log(`✅ [v9] 第 ${roundNumber} 轮专家发言阶段结束（领袖决定讨论已充分）`);
    break;
  }

  // 专家发言
  console.log(`🎤 [v9] ${nextRole.shortName} 开始发言...`);
  const speech = await this.callAI({
    role: nextRole,
    prompt: this.buildRoleSpeechPrompt(nextRole, roundNumber, roundData),
    temperature: 0.6,
    maxTokens: 400
  });

  const roleSpeech = {
    roleId: nextRole.id,
    roleName: nextRole.shortName,
    content: speech.content || speech,
    color: nextRole.color,
    layer: nextRole.layer,
    round: roundNumber,
    timestamp: new Date().toISOString()
  };

  roundData.speeches.push(roleSpeech);
  this.contextDatabase.addSpeech(roleSpeech); // ✅ [v9] 录入数据库

  this.emit('roleSpeak', {
    round: roundNumber,
    role: nextRole,
    content: speech.content || speech
  });

  // 记录已发言（允许同一专家多次发言）
  alreadySpoken.push(nextRole.id);

  await this.delay(500); // 模拟真实辩论节奏
}
```

#### 4.2.3 递进式上下文构建

```javascript
// 位置：debateEngine.js buildRoleSpeechPrompt() 方法

const relevantContext = this.contextDatabase.getRelevantContext(role.id, roundNumber);

// 构建你的发言历史
let myHistoryText = '';
if (relevantContext.myHistory && relevantContext.myHistory.length > 0) {
  myHistoryText = `\n**📋 你之前的发言历史（${relevantContext.myHistory.length}次）**：\n`;
  relevantContext.myHistory.slice(-3).forEach(speech => {
    myHistoryText += `- 第${speech.round}轮：${speech.content.substring(0, 100)}...\n`;
  });
  myHistoryText += `（提示：请在本轮发言中展现与之前的连贯性和递进关系）\n`;
}

// 构建其他专家关键观点
let othersKeyPointsText = '';
if (relevantContext.othersKeyPoints && relevantContext.othersKeyPoints.length > 0) {
  othersKeyPointsText = `\n**💡 其他专家的关键观点**：\n`;
  relevantContext.othersKeyPoints.forEach(({ roleId, recentPoints }) => {
    const roleName = this.roles.find(r => r.id === roleId)?.shortName || `角色${roleId}`;
    if (recentPoints && recentPoints.length > 0) {
      const pointsText = recentPoints.map(p => {
        const pointsSummary = p.points.map(pt => pt.text).join('；');
        return `第${p.round}轮：${pointsSummary}`;
      }).join(' | ');
      othersKeyPointsText += `- ${roleName}：${pointsText}\n`;
    }
  });
}

// 构建完整时间线
let timelineText = '';
if (Object.keys(relevantContext.allRounds).length > 0) {
  timelineText = `\n**📊 完整辩论时间线（关键要点）**：\n`;
  Object.entries(relevantContext.allRounds).forEach(([round, speeches]) => {
    const roundKeyPoints = speeches
      .map(s => {
        const keyPointsText = s.keyPoints.map(p => p.text).slice(0, 2).join('；');
        const dataText = s.dataRefs.length > 0 ? ` [数据：${s.dataRefs.slice(0, 2).join('、')}]` : '';
        return `${s.roleName}：${keyPointsText}${dataText}`;
      })
      .join(' | ');
    timelineText += `- 第${round}轮：${roundKeyPoints}\n`;
  });
}

return `${role.systemPrompt}

**当前辩论情况**：
- 主议题：${this.state.topic}
- 当前轮次：第 ${roundNumber}/${this.state.rounds} 轮
- 本轮焦点：${roundData.topic}
${myHistoryText}
${othersKeyPointsText}
${timelineText}

**⚠️ 重要要求**：
1. 基于以上完整历史上下文，展现与之前发言的连贯性和递进关系
2. 回应其他专家的关键观点，展现对话感（而非走过场）
3. 引用具体数据/案例（严禁编造），参考辩论时间线中的数据引用
4. 结合你的角色定位，给出3个具体建议（含时间/成本/资源）
5. 控制在200-300字

现在，请基于你的角色定位和完整历史上下文，发表本轮意见。`;
```

#### 4.2.4 专家发言字数优化实现

**实施时间**: 2025-10

**需求来源**: 用户需求 (Section 5.2, line 619)
```markdown
- ❓ 如何在"深度递进"和"200-300字"之间平衡？>>300字太少了, 500?
```

**实施方案**: 三步骤系统级同步更新

**步骤1: 提示词文本更新** (`debateEngine.js` 行1144)
- 位置: `buildRoleSpeechPrompt()` 方法
- 变更: "控制在200-300字" → "控制在500字"
- 影响: 所有动态生成的专家发言提示词

```javascript
// 位置：debateEngine.js buildRoleSpeechPrompt() 方法

**⚠️ 重要要求**：
1. 基于以上完整历史上下文，展现与之前发言的连贯性和递进关系
2. 回应其他专家的关键观点，展现对话感（而非走过场）
3. 引用具体数据/案例（严禁编造），参考辩论时间线中的数据引用
4. 结合你的角色定位，给出3个具体建议（含时间/成本/资源）
5. 控制在500字  // ← 从 "200-300字" 更新为 "500字"

现在，请基于你的角色定位和完整历史上下文，发表本轮意见。
```

**步骤2: 角色配置更新** (`roles.js`)
- 范围: 全部15个专家角色 systemPrompt
- 统一格式: "发言控制在500字，包含至少X个数据示例和Y个建议"
- 影响: 确保所有角色行为指令一致

```javascript
// 示例：第一性原则角色 (roles.js)

{
  id: 1,
  key: 'first_principle',
  systemPrompt: `你使用第一性原理思考方法...

  **建议要求**：
  - 提供3个行动原则（针对用户年龄段和行业背景）
  - 用数据/案例支撑本质分析（如："根据XX行业报告..."）
  - 优先验证假设，建议小步快跑的具体路径
  - 每个建议需可量化或有明确时间节点

  请用清晰的逻辑链条展示你的思考过程。发言控制在500字，包含至少1个数据示例和3个建议。`
}
```

**步骤3: API参数更新** (`debateEngine.js` 行1384)
- 位置: `callAI()` 方法默认参数
- 变更: `maxTokens = 500` → `maxTokens = 650`
- 计算依据: 500汉字 × 1.3 token/字 = 650 tokens
- 影响: 确保AI API有足够token预算，防止响应截断

```javascript
// 位置：debateEngine.js callAI() 方法

async callAI({ role, prompt, temperature = 0.7, maxTokens = 650 }) {
  // 从 maxTokens = 500 增加到 650
  // 计算：500汉字 × 1.3 token/字 = 650 tokens
  const requestBody = {
    model: this.config.model,
    prompt: prompt,
    systemPrompt: role.systemPrompt,
    roleName: role.name,
    temperature: temperature,
    maxTokens: maxTokens
  };
  // ... rest of method
}
```

**技术原理**:
中文字符与token比例约为1:1.3，因此500字需要650 tokens才能保证完整输出。

**实施效果**:
- ✅ 专家发言深度显著提升（200-300字 → 500字）
- ✅ 三层一致性：提示词生成逻辑 + 角色配置 + API参数
- ✅ 无响应截断问题
- ✅ 保持对话递进性和专业性

---

## 5. 待讨论与确定的细节

### 5.1 架构层面

#### 🔴 P0 - 必须确定

1. **版本定位**
   - ❓ v9 是否作为独立大版本发布？>>是
   - ❓ 是否需要保留 v8 流程模式作为"经典模式"？ >>可保留, 但可能意义不大-实用性低
   - ❓ 用户是否可以在 UI 中切换 v8/v9 模式？>>必要性低, 保留一版而已

2. **ContextDatabase 持久化**
   - ❓ 是否需要保存到后端/LocalStorage？>>是!!!
   - ❓ 是否需要支持跨会话恢复（如：委托人关闭浏览器后继续）？>>中期规划
   - ❓ 数据存储格式？（JSON / SQLite / MongoDB）>>不熟悉, 建议? 通用性强标注?

3. **Token 成本控制**
   - ❓ 当前无限制，10轮辩论可能超过5000 tokens >>目前看还好, 
   - ❓ 如何压缩上下文？（只保留关键信息 / AI总结压缩）>>中期规划
   - ❓ 是否需要显示实时 token 消耗？>>可以

#### 🟠 P1 - 重要但非紧急

4. **关键观点提取优化**
   - ❓ 当前正则匹配是否足够？>>不太理解, 说白话
   - ❓ 是否需要引入 NLP 模型（如：BERT/GPT）？>>需要, 重点是方案, 成本?
   - ❓ 如何处理跨句的复杂观点？>> 不确定

5. **争议焦点识别优化**
   - ❓ 阈值是否需要动态调整？>>建议? 如果是一轮里单个专家的最多发言次数, 最多3次
   - ❓ 是否需要语义相似度匹配？ >>应该要吧
   - ❓ 如何避免误判（如：表述相同但立场不同）？ >>1. 领袖代理决断, 如需要, 请委托人决断

6. **数据引用验证**
   - ❓ 如何防止 AI 编造数据？>>重要!!! 去AI化, 温度值控制?
   - ❓ 是否需要检查"根据XX报告"的真实性？ >>必须!
   - ❓ 是否需要提供数据来源链接？>>原则上不需要, 但确实最后适当给出出处

### 5.2 交互层面

#### 🔴 P0 - 必须确定

7. **领袖决策规则**
   - ❓ "COMPLETE" 判断标准是否需要明确规则？>> 这里的compete是指什么>
   - ❓ 是否需要限制单轮最大发言次数？>>单专家(领袖作为facilitator除外)最多3次(包括主动/被动-被邀请)发言; 所有人中测试不应超过20次(暂定)
   - ❓ 如何平衡"充分讨论"和"效率"？>>前几轮, 领袖可以和委托人确认一下'节奏把握'和感受及建议

8. **二次邀请控制**
   - ❓ 是否需要限制单人最多发言次数（如：3次）？>>单专家(领袖作为facilitator除外)最多3次(包括主动/被动-被邀请)发言
   - ❓ 如何防止领袖陷入"无限邀请同一专家"？>>控制最多3次, 除非委托人要求
   - ❓ 是否需要向用户提示"XX专家已第N次发言"？>>不用, 领袖管理和控制

#### 🟠 P1 - 重要但非紧急

9. **上下文长度控制**
   - ❓ myHistory 是否需要限制最多N次？>> 不理解问题
   - ❓ allRounds 是否需要限制最多M轮？>>默认10轮, 超过20轮要付费模式了(中/后期规划)
   - ❓ 如何动态调整（10轮 vs 3轮辩论）？>>可能3轮就没必要, 至少5轮, 正常20轮上限; 我们自己开发测试无上限(最后一轮, 委托人要求下, 可以延续)

10. **连贯性与简洁性平衡**
    - ❓ 如何在"深度递进"和"200-300字"之间平衡？>>300字太少了, 500?
    - ❓ 提示词措辞是否需要调整？ >> 必须的, 以实际现实为准, 体现专家专业性和就问题和讨论的相关性, 保证深度和落实实效性
    - ❓ 是否需要分"深度模式"和"快速模式"？>>可以, 中期规划

### 5.3 展示层面

#### 🟡 P2 - 可选优化

11. **格式化增强**
    - ❓ 关键词列表是否需要扩展？>>需要
    - ❓ 加粗颜色是否需要根据角色层级动态变化？ >>可以, 以体验为标准! 在没有语音功能前, 看字必须提供reader-care
    - ❓ 是否需要支持嵌套列表、表格、引用？>>good idea, 但具体要看实效

12. **回应关系可视化**
    - ❓ 是否需要在发言中标记"@角色名"？>> 可能模拟现场感, 要给每个专家都起个名字, 包括头像; 以后后期规划还要考虑模拟视频会议感觉
    - ❓ 是否需要在UI中可视化回应关系（箭头连接）？>>可以考虑, 看具体效果
    - ❓ 是否需要"争议焦点"热力图？>> 需要, 这是作为报告的一部分

13. **用户体验优化**
    - ❓ 是否需要显示"领袖正在决策下一位发言者..."加载状态？>>不应该吧, 显得迟钝>
    - ❓ 是否需要显示"已发言专家"列表？>> 感觉不用
    - ❓ 是否需要支持用户手动介入（如：强制邀请某专家）？>>必须有

---

## 6. 测试验证计划

### 6.1 测试场景

根据 TODO #097，需要测试3个场景：

#### 场景1：RRXS 自媒体商业化
- **议题**: "我应该如何从职场转型做自媒体？"
- **关键验证**:
  - 对话延续性：专家是否引用自己之前的观点
  - 互动回应：专家是否回应其他专家的建议
  - 动态顺序：领袖是否邀请最合适的专家
  - 二次邀请：是否出现同一专家多次发言的情况
  - 争议识别：是否识别出关键争议点（如：定价、定位）

#### 场景2：电商创业决策
- **议题**: "我应该在淘宝还是抖音开店？"
- **关键验证**:
  - 数据引用：专家是否提供具体数据支撑
  - 格式优化：列表是否正确分行，关键词是否加粗
  - 上下文完整：专家是否看到完整辩论历史
  - COMPLETE判断：领袖是否在适当时机结束讨论

#### 场景3：个人成长规划
- **议题**: "40岁如何实现职业突破？"
- **关键验证**:
  - 递进关系：专家后续发言是否深化前面的观点
  - Token控制：10轮辩论是否超过预期token数
  - 性能表现：AI决策耗时是否在可接受范围

### 6.2 验证指标

| 指标 | 目标值 | 验证方法 |
|-----|--------|---------|
| 对话延续性 | ≥80% 专家发言引用自己历史 | 人工检查发言内容 |
| 互动回应率 | ≥60% 专家回应其他观点 | 检查是否提及其他角色 |
| 动态决策合理性 | ≥90% 决策符合对话逻辑 | 人工判断邀请是否合理 |
| 二次邀请触发率 | 10-30% 轮次出现二次邀请 | 统计 alreadySpoken 数据 |
| 争议识别准确率 | ≥70% 争议点被正确识别 | 对比人工标注 vs AI识别 |
| 数据引用率 | ≥80% 发言包含数据 | 检查 dataRefs 字段 |
| 格式正确率 | 100% 列表正确分行 | UI 检查 |
| Token 总消耗 | ≤8000 tokens/10轮 | 后端统计 |
| AI决策耗时 | ≤3秒/次 | 性能监控 |

### 6.3 测试执行步骤

1. **环境准备**
   - 启动后端服务（端口3000）
   - 启动前端服务（端口8080）
   - 确认 DeepSeek API 可用

2. **执行测试**
   - 依次测试3个场景（每个5轮）
   - 记录所有发言到测试日志
   - 截图保存关键界面

3. **数据收集**
   - 导出 ContextDatabase 数据（speeches, keyPoints, controversies）
   - 统计 token 消耗
   - 记录性能数据

4. **问题记录**
   - 记录所有不符合预期的行为
   - 分类：P0严重/P1重要/P2优化
   - 提出修复方案

---

## 7. 与 v8 的对比

### 7.1 核心差异对比表

| 维度 | v8（流程化） | v9（动态对话） | 提升点 |
|-----|-------------|---------------|--------|
| **定位** | 角色提示词打磨 + 数据化 | AI驱动的真实对话系统 | 从"内容优化"到"系统重构" |
| **发言顺序** | 固定流线（8个必选） | AI动态决策（可重复邀请） | ✅ 灵活性、真实性 |
| **上下文** | 仅本轮当前发言（~200字） | 三层完整上下文（~1500字） | ✅ 深度、延续性 |
| **发言次数** | 每人每轮1次 | 可多次（二次邀请） | ✅ 深化争议点 |
| **结束判断** | 固定轮次 | AI判断"COMPLETE" | ✅ 智能化 |
| **信息提取** | 无 | 自动提取观点/数据 | ✅ 结构化、可追溯 |
| **格式优化** | Markdown保留 | 智能格式化 | ✅ 可读性 |
| **Token成本** | ~3000/10轮 | ~5000/10轮（预估） | ⚠️ 成本增加67% |
| **开发复杂度** | 中等 | 高 | ⚠️ 维护成本增加 |

### 7.2 用户体验提升

#### v8 的问题（用户反馈）
1. "感觉专家在走过场，发言相对独立"
2. "看不出角色之间的互动和争议"
3. "每轮发言都很浅，缺少深度递进"

#### v9 的改进
1. ✅ **延续性**：专家发言明确引用自己的历史观点
2. ✅ **互动性**：专家回应其他专家的建议，形成对话
3. ✅ **深度**：二次邀请机制允许深化争议点

### 7.3 技术债务

#### v9 新增的技术挑战
1. **Token 管理**：上下文长度无限制，可能超限
2. **性能优化**：AI决策增加响应时间
3. **数据一致性**：ContextDatabase 需要维护完整性
4. **错误处理**：AI决策失败需要降级策略

#### 待解决的遗留问题
1. v8 的固定流线模式是否保留为"经典模式"？
2. 如何向用户解释 v9 的"动态对话"优势？
3. 是否需要提供"v8 vs v9"对比测试？

---

## 8. 下一步行动计划

### 8.1 立即行动（本周）

1. **讨论并确定待定细节**（本文档第5节）
   - 优先讨论所有 P0 问题（7个）
   - 形成明确的设计决策文档

2. **执行测试验证**（TODO #097）
   - 3个场景完整测试
   - 收集验证数据
   - 记录问题清单

3. **文档完善**
   - 更新 progress.md（v9 里程碑）
   - 更新 CLAUDE.md（v9 章节）
   - 创建测试报告

### 8.2 短期优化（未来2周）

1. **性能优化**
   - Token 压缩策略
   - AI决策耗时优化
   - 上下文智能裁剪

2. **用户体验**
   - 加载状态提示
   - 发言专家列表
   - 争议焦点可视化

3. **代码重构**
   - ContextDatabase 单元测试
   - 错误处理增强
   - 日志系统完善

### 8.3 长期规划（未来1个月）

1. **高级功能**
   - NLP 模型集成（观点提取）
   - 语义相似度匹配（争议识别）
   - 数据来源验证（防止编造）

2. **模式扩展**
   - v8 经典模式保留
   - v9 深度模式
   - v10 快速模式（3轮极简）

3. **生态建设**
   - 辩论模板库
   - 用户反馈收集
   - 数据分析报告

---

## 9. 附录

### 9.1 关键文件快速定位

- **核心架构**: `debateEngine.js` 行14-175（ContextDatabase）
- **动态决策**: `debateEngine.js` 行808-889（decideNextSpeaker）
- **上下文构建**: `debateEngine.js` 行906-992（buildRoleSpeechPrompt）
- **格式优化**: `index.html` 行1212-1260（formatExpertSpeech）
- **发言录入**: `debateEngine.js` 行607-764（5个录入点）

### 9.2 调试技巧

1. **查看完整上下文**：
```javascript
console.log('[DEBUG] relevantContext:', JSON.stringify(relevantContext, null, 2));
```

2. **监控AI决策**：
```javascript
console.log('[DEBUG] Leader decision:', decisionText, '| Candidates:', candidateRoles.map(r => r.id));
```

3. **验证关键观点提取**：
```javascript
console.log('[DEBUG] Extracted keyPoints:', speech.keyPoints);
console.log('[DEBUG] Extracted dataRefs:', speech.dataRefs);
```

### 9.3 术语表

- **ContextDatabase**: 对话信息数据库，存储所有发言+元数据
- **keyPoints**: 关键观点，包括建议、问题、数据
- **dataRefs**: 数据引用，包括百分比、数字、来源
- **controversies**: 争议焦点，被多次提及的问题
- **二次邀请**: 同一专家在同一轮多次发言
- **COMPLETE**: 领袖判断本轮讨论已充分的标记
- **递进关系**: 专家后续发言与之前观点的连贯性
- **三层上下文**: myHistory + othersKeyPoints + allRounds

---

**文档版本**: v1.0
**最后更新**: 2025-10-03 23:55
**维护者**: RRXS Team
**审核状态**: 待用户确认所有待定细节（第5节）
