# 🤖 所有 AI 对话记录索引

> ✅ 自动聚合 `Z_OBS_Sidebar_Dialg/` 及其子文件夹下所有对话笔记  
> ✅ 输入关键词实时搜索标题或内容  
> ✅ 支持按标签分类（如 #写作、#编程）  
> ✅ 最新对话置顶，点击直达

---
能否批量帮我把"Z_OBS_Sidebar_Dialg"目录下的侧边栏对话文件中 行首为 "**user:**"(用户提示词开头), 改为"# **user:**", 从而 把用户提问作为一级目录, 一目了然?
能否批量帮我把"Z_OBS_Sidebar_Dialg"目录下的侧边栏对话文件中 行首为 "**user**:"(用户提示词开头), 改为"# **user**:", 从而 把用户提问作为一级目录, 一目了然?

<input type="text" id="searchInput" placeholder="🔍 输入关键词搜索对话..." style="width: 350px; padding: 10px; margin: 15px 0; font-size: 16px; border: 2px solid #007acc; border-radius: 6px;">

<div id="searchResults" style="margin-top: 20px;"></div>

```dataviewjs
// ========== 配置 ==========
const folderPath = "Z_OBS_Sidebar_Dialg"; // 修改为你自己的路径
const defaultSort = "file.ctime DESC";    // 默认排序：最新在前

// ========== 初始化 ==========
const searchInput = document.getElementById('searchInput');
const resultsDiv = document.getElementById('searchResults');

if (!searchInput || !resultsDiv) {
    dv.paragraph("❌ 搜索组件加载失败，请检查 HTML 结构。");
    return;
}

// 初始加载全部对话
updateResults('');

// 监听输入变化
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    updateResults(query);
});

// ========== 核心函数 ==========
async function updateResults(query) {
    resultsDiv.innerHTML = '<p style="color: #666;">⏳ 正在搜索...</p>';
    
    // 获取所有对话笔记
    const files = app.vault.getMarkdownFiles()
        .filter(f => f.path.startsWith(folderPath + "/"));

    if (query === '') {
        // 显示全部对话
        displayAll(files);
    } else {
        // 搜索：标题 + 内容
        const matches = await searchInFiles(files, query);
        displayResults(matches, query);
    }
}

async function searchInFiles(files, query) {
    let matches = [];
    for (let file of files) {
        const content = await app.vault.read(file);
        if (file.basename.toLowerCase().includes(query.toLowerCase()) ||
            content.toLowerCase().includes(query.toLowerCase())) {
            matches.push(file);
        }
    }
    return matches;
}

function displayAll(files) {
    if (files.length === 0) {
        resultsDiv.innerHTML = `<div style="padding: 20px; background: #f8f8f8; border-radius: 8px; text-align: center;">
            <h3>📂 尚无对话记录</h3>
            <p>请先与 AI 进行对话并保存～</p>
        </div>`;
        return;
    }

    // 按时间排序
    files.sort((a, b) => b.stat.ctime - a.stat.ctime);

    const list = files.map(f => {
        const date = dv.date("yyyy-MM-dd HH:mm", f.stat.ctime);
        const tags = getTags(f)?.join(" ") || "";
        return `
            <div style="padding: 12px; margin: 8px 0; border-left: 4px solid #007acc; background: #f9f9f9; border-radius: 4px;">
                <a href="${f.path}" style="font-weight: bold; font-size: 16px; color: #007acc; text-decoration: none;">${f.basename}</a>
                <div style="font-size: 13px; color: #666; margin-top: 4px;">📅 ${date} ${tags}</div>
            </div>
        `;
    }).join('');

    resultsDiv.innerHTML = `
        <h3 style="margin: 20px 0 10px 0; padding-bottom: 8px; border-bottom: 2px solid #007acc;">📌 全部对话（共 ${files.length} 条）</h3>
        <div>${list}</div>
    `;
}

function displayResults(matches, query) {
    const list = matches
        .sort((a, b) => b.stat.ctime - a.stat.ctime)
        .map(f => {
            const date = dv.date("yyyy-MM-dd HH:mm", f.stat.ctime);
            const tags = getTags(f)?.join(" ") || "";
            return `
                <div style="padding: 12px; margin: 8px 0; border-left: 4px solid #007acc; background: #f9f9f9; border-radius: 4px;">
                    <a href="${f.path}" style="font-weight: bold; font-size: 16px; color: #007acc; text-decoration: none;">${f.basename}</a>
                    <div style="font-size: 13px; color: #666; margin-top: 4px;">📅 ${date} ${tags}</div>
                </div>
            `;
        }).join('');

    resultsDiv.innerHTML = `
        <h3 style="margin: 20px 0 10px 0; padding-bottom: 8px; border-bottom: 2px solid #007acc;">🔍 搜索“<strong>${query}</strong>”结果（共 ${matches.length} 条）</h3>
        <div>${list || '<p style="color: #999; padding: 20px;">未找到匹配项 😕</p>'}</div>
    `;
}

// 提取标签（兼容逗号分隔和 YAML 列表）
function getTags(file) {
    const cache = dv.io.cache[file.path];
    if (!cache || !cache.frontmatter || !cache.frontmatter.tags) return null;
    
    let tags = cache.frontmatter.tags;
    if (typeof tags === 'string') {
        return tags.split(',').map(t => `#${t.trim()}`).filter(t => t !== '#');
    } else if (Array.isArray(tags)) {
        return tags.map(t => `#${t}`);
    }
    return null;
}