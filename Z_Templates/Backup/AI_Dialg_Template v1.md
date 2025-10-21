---
created: {{date:YYYY-MM-DD HH:mm}}
tags: [ai,对话]
---
<%*
// 模块名称：AI对话笔记-高可靠性格式化
// 目的：在侧边栏对话记录中，将 **user** 开头的提示词格式化为 # **user** 一级标题。

const file = app.workspace.activeFile;
if (!file) return;

// 1. 路径检查 (如果文件不在目标文件夹，则退出)
if (!file.path.startsWith("Z_OBS_Sidebar_Dialg/")) return;

// 2. 获取文件名，判断 topic (保留原有逻辑)
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
}


// 3. Frontmatter & 内容读取 (使用同步获取，提高稳定性)
// 注意：在 Templater 插入模板时，tp.file.content会获取到文件创建之前的内容或空内容
let content = tp.file.content; 
const timestamp = tp.date.now("YYYY-MM-DD HH:mm:ss");

// 4. 处理 Frontmatter (只在没有时插入)
const frontmatter = `---
tags: ai,对话,${topic}
created: ${timestamp}
---`;

if (!content.trim().startsWith("---")) {
    content = frontmatter + "\n\n" + content;
}

// 5. 核心：格式化 **user**: 为一级标题
// 使用替换函数，确保只替换一次
try {
    // 正则表达式：匹配行首（^）的可选空格（\s*）+ **user**: + 捕获组（.*）+ 允许多行（gm）
    const userPattern = /^\s*\*\*user\*\*:\s*(.*)$/gm; 
    
    // 替换：将匹配到的整行替换为 # **user**: 捕获组内容
    content = content.replace(userPattern, (match, p1) => {
        // p1 是 (.*) 捕获到的用户输入内容
        // 目标：# **user**: [内容]
        return `# **user**: ${p1.trim()}`; 
    });
    
    // 写入日志（可选）
    console.log(`✅ 笔记格式化完成：tags=ai,对话,${topic}，格式化 ${content.match(/# \*\*user\*\*:/g)?.length || 0} 个标题`);
    
    // 6. 最终写入 (使用app.vault.modify，只运行一次)
    await app.vault.modify(file, content);

} catch (error) {
    console.error("❌ 格式化或写入错误：", error); 
}

// 确保脚本没有意外输出
-%>