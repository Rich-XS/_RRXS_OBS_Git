<%*
const pathMapping = {
    // 映射规则（同之前提供的规则）
    "Tmp": "00-Inbox",
    "error": "00-Inbox",
    "AI Biz": "01-Projects/AI-Biz",
    // ...（完整规则见上文）
};
const files = app.vault.getFiles().filter(f => f.path.includes("印象笔记"));
let log = "";
for (const file of files) {
    let newDir = null;
    for (const [key, value] of Object.entries(pathMapping)) {
        if (file.path.includes(key)) {
            newDir = value;
            break;
        }
    }
    if (newDir) {
        const newPath = `${newDir}/${file.name}`;
        await app.vault.rename(file, newPath);
        log += `Moved: ${file.path} → ${newPath}\n`;
    }
}
await tp.system.clipboard(log);
%>