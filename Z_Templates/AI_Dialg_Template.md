---
created: {{date:YYYY-MM-DD HH:mm}}
tags: [ai,对话]
---
<%*
// AI_Dialg_Template: 只针对Z_OBS_Sidebar_Dialg/下AI聊天笔记，自动添加frontmatter + 将 **user**: 转为 # **user**: 一级标题
// 最简单更新：保留原逻辑，只加正文替换

const file = app.workspace.activeFile;
if (!file) return;

// 只处理 Z_OBS_Sidebar_Dialg/ 文件夹下的文件
if (!file.path.startsWith("Z_OBS_Sidebar_Dialg/")) return;

// 获取文件名，判断 topic（原逻辑保留）
let fileName = file.basename;
let topic = "通用";

if (fileName.includes("写") || fileName.includes("文章") || fileName.includes("文案")) {
    topic = "写作";
} else if (fileName.includes("代码") || fileName.includes("编程") || fileName.includes("debug")) {
    topic = "编程";
} else if (fileName.includes("学习") || fileName.includes("复习") || fileName.includes("考试")) {
    topic = "学习";
} else if (fileName.includes("计划") || fileName.includes("安排") || fileName.includes("时间")) {
    topic = "计划";
} else if (fileName.includes("简历") || fileName.includes("求职") || fileName.includes("面试")) {
    topic = "求职";
} else if (fileName.includes("PPT") || fileName.includes("演示") || fileName.includes("汇报")) {
    topic = "演示";
} else if (fileName.includes("Tool") || fileName.includes("结构") || fileName.includes("Query")) {
    topic = "工具实施方案";  // 新增：匹配你的示例文件名（Tool_Implementation_Structure_Query）
}

// Frontmatter（原逻辑保留，使用逗号分隔tags）
const frontmatter = `---
tags: ai,对话,${topic}
created: ${new Date().toISOString().slice(0, 19).replace('T', ' ')}
epoch: ${Date.now()}
modelKey: x-ai/grok-4-fast:free|openrouterai  // 可选：从活跃笔记复制，如果需要
topic: "${topic}"
---`;

// 读取当前文件内容
let content = await app.vault.read(file);

// 处理frontmatter（原逻辑保留）
if (!content.trim().startsWith("---")) {
    content = frontmatter + "\n\n" + content;
} else {
    // 如果已有，更新tags 和 created
    const fmEnd = content.indexOf('\n---\n') + 5;
    if (fmEnd > 0) {
        const beforeFM = content.substring(0, fmEnd);
        const afterFM = content.substring(fmEnd);
        let newFM = beforeFM.replace(/tags: .*/g, `tags: ai,对话,${topic}`);
        newFM = newFM.replace(/created: .*/g, `created: ${new Date().toISOString().slice(0, 19).replace('T', ' ')}`);
        content = newFM + afterFM;
    }
}

// 【新增：最简单替换 **user**: 为 # **user**: 一级标题】
// 只匹配 **user**: 行（忽略前后空格/换行），转为 # **user**: + 原后文（保留时间戳等）
try {
    const userPattern = /^\s*\*\*user\*\*:\s*(.*)$/gm;  // gm=全局多行，$1=捕获后文
    const matches = content.match(userPattern) || [];
    content = content.replace(userPattern, '# **user**: $1');  // 替换为标题
    
    console.log("✅ **user**: 已转为#标题，共替换 " + matches.length + " 个");
} catch (error) {
    console.error("替换错误：", error);
}

// 保存（原逻辑 + 新增）
await app.vault.modify(file, content);

console.log(`✅ 更新完成：topic=${topic}`);
%>