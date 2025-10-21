<%*
// AI Startup Template: 最终优化版本 (使用tp.file.content + 脚本输出)

const file = app.workspace.activeFile;
if (!file) return;

// 1. 路径检查
if (!file.path.startsWith("Z_OBS_Sidebar_Dialg/")) return; 

// 2. 确定 Topic 
let fileName = file.basename;
let topic = "通用";
// ... (保留您的 Topic 判断逻辑不变)
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

// 3. 同步获取内容
let content = tp.file.content; 
if (!content) return; // 如果内容为空，直接退出

// --- 4. Frontmatter 处理 (改为只检查，不修改) ---
// 因为我们要输出整个文件内容，所以不在这里修改 frontmatter
// 否则会造成重复的 frontmatter，这一步我们留给用户手动处理或使用其他插件
const frontmatterTemplate = `---
tags: ai,对话,${topic}
created: ${tp.date.now("YYYY-MM-DD HH:mm:ss")}
---`;

if (!content.trim().startsWith("---")) {
    // 只有在没有 frontmatter 时才添加
    content = frontmatterTemplate + "\n\n" + content;
} else {
    // ⚠️ 警告：为了稳定性，我们跳过修改已有 frontmatter 的逻辑
    // 如果需要更新tags，请使用 Dataview/Metaedit 插件
}

// --- 5. 核心格式化：合并替换 ---
const timestamp = tp.date.now("YYYY/MM/DD HH:mm:ss");
try {
    const userPattern = /^\s*\*\*user\*\*:\s*(.*)$/gm; 
    
    // 替换并添加时间戳
    content = content.replace(userPattern, (match, p1) => {
        return `# **user**: ${p1.trim()}\n[Timestamp: ${timestamp}]\n`; 
    });

} catch (error) {
    // 格式化错误不会影响脚本输出
    console.error("格式化错误，但继续输出内容：", error); 
}

// ⚠️ 关键步骤：使用 tp.file.cursor() 确保内容被输出到文件中，
// 但是因为我们要覆盖整个文件，我们需要一个巧妙的办法。
// 最简单的办法是让脚本打印出新的内容，然后手动覆盖旧内容。

// 如果您想完全覆盖文件，请将 Templater 插入点放在文件开头，并删除所有原始内容
// 由于 Templater Insert 无法“覆盖”整个文件，我们必须退一步：
// 将处理后的内容放在剪贴板，让您手动粘贴。

// 将最终内容放入剪贴板 (需要 Templater 启用 "Shell commands" 或其他剪贴板插件)
// 启用 'tp.system.clipboard' 需要 'Templater' 设置中启用 'Use community plugins' 
// 建议：直接输出到控制台，然后手动复制内容到文件，这是最稳定的

console.log("------------------- 新内容已准备好 (请复制) -------------------");
console.log(content);
console.log("----------------------------------------------------------------");

// 最终我们让脚本输出处理后的内容，但**用户必须手动替换**。
// 因为 `app.vault.modify()` 失败，而 `tp.file.include` 无法覆盖整个文件。
// 我们可以使用 tp.file.cursor() 确保脚本能插入内容，但插入点需要用户自行清理。

// 返回新内容，但用户必须清理插入点
tR += content; // 这一行会将内容输出到插入点
-%>