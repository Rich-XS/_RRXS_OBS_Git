// 当新建文件时，自动检测是否是 AI 对话笔记
// 并为其添加 tags: ai,对话,写作 等动态标签

const file = app.workspace.activeFile;
if (!file) return;

// 只处理 Z_OBS_Sidebar_Dialg 文件夹下的文件
if (!file.path.startsWith("Z_OBS_Sidebar_Dialg/")) return;

// 获取文件名，判断 topic
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
}

// ✅ 使用逗号分隔标签，确保 Obsidian 正确识别
const frontmatter = `---
tags: ai,对话,${topic}
created: ${new Date().toISOString().slice(0, 19).replace('T', ' ')}
---`;

// 如果文件没有 Frontmatter，则插入
const content = await app.vault.read(file);
if (!content.startsWith("---")) {
    const newContent = frontmatter + "\n\n" + content;
    await app.vault.modify(file, newContent);
}