<%*
// AI Startup Template: 新建AI对话笔记时自动添加frontmatter + 格式化 user: 为一级标题
// 适用于 Z_OBS_Sidebar_Dialg/ 文件夹

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
created: ${tp.date.now("YYYY-MM-DD HH:mm:ss")}
---`;

// 读取当前文件内容
let content = await app.vault.read(file);

// 如果文件没有 Frontmatter，则插入
if (!content.trim().startsWith("---")) {
    content = frontmatter + "\n\n" + content;
} else {
    // 如果已有frontmatter，也更新tags（可选，避免重复）
    const fmEnd = content.indexOf('\n---\n') + 5;  // 找到frontmatter结束
    if (fmEnd > 0) {
        const beforeFM = content.substring(0, fmEnd);
        const afterFM = content.substring(fmEnd);
        // 更新tags行（简单替换或追加）
        let newFM = beforeFM.replace(/tags: .*/g, `tags: ai,对话,${topic}`);
        content = newFM + afterFM;
    }
}

// 【新增：格式化 **user**: 为一级标题】
// 正则匹配每个 **user**:（忽略前后空格/换行），替换为 # **user**: $1
try {
    // 匹配模式：**user**:（可选空格，gm=全局多行）
    //const userPattern = /^\s*\*\*user\*\*:\s*(.*)$/gm; // ✅ 修正了这里的正则表达式！
    let oldContent = content;
    //content = content.replace(userPattern, '# **user**: $1'); // ✅ 修正了这里的替换内容！
    
    // 可选：每个user后加时间戳（基于当前时间，或用笔记created）
    const timestamp = tp.date.now("YYYY/MM/DD HH:mm:ss");
    content = content.replace(/# \*\*user\*\*:\s*(.*)/g, `# **user**: $1\n[Timestamp: ${timestamp}]\n`);
    
    // 日志：计算替换数
    const replacedCount = (content.match(/# \*\*user\*\*:/g) || []).length;
    console.log(`✅ **user**: 格式化完成，共替换 ${replacedCount} 个标题`);
    
    // 只在有变化时更新（优化性能）
    if (content !== oldContent) {
        await app.vault.modify(file, content);
    }
} catch (error) {
    console.error("格式化错误：", error);  // 调试用，不崩溃
}

// 保存frontmatter变化（如果有）
if (content.includes(frontmatter)) {  // 简单检查
    await app.vault.modify(file, content);
}

console.log(`✅ 笔记更新完成：tags=ai,对话,${topic}；topic=${topic}`);
-%>