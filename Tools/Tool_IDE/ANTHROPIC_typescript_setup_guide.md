# TypeScript + VS Code 性能优化完整教程

## 📋 适用场景
- VS Code 频繁出现 "compacting" 消息
- 大型 JavaScript 项目（文件 > 2000 行）
- 需要为 TypeScript 做准备

---

## 🎯 教程目标
完成以下三个配置：
1. VS Code 性能优化（`settings.json`）
2. TypeScript 配置（`tsconfig.json`）
3. npm 编译脚本（`package.json`）

---

## ✅ 第一步：优化 VS Code 设置

### 1.1 打开设置文件
- **Windows/Linux**: Ctrl + Shift + P → 搜索 "settings.json" → 选择"首选项: 打开用户设置(JSON)"
- **Mac**: Cmd + Shift + P → 同上

### 1.2 复制完整配置
将以下完整内容复制到 `settings.json`：

```json
{
  // 增加 TypeScript 内存分配
  "typescript.tsserver.maxTsServerMemory": 4096,
  
  // 禁用可能触发 compacting 的功能
  "typescript.tsserver.experimental.enableProjectDiagnostics": false,
  
  // 减少文件监视开销
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "**/.venv/**": true
  },
  
  // 限制打开的编辑器数量
  "workbench.editor.limit.enabled": true,
  "workbench.editor.limit.value": 10,
  
  // 禁用不必要的验证
  "html.validate.scripts": false,
  "css.validate": false,
  
  // Python 相关配置（如需要）
  "python.pythonPath": ".venv/Scripts/python.exe",
  "python.defaultInterpreterPath": ".venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "python.terminal.activateEnvInCurrentTerminal": true,
  
  // 终端配置
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "args": [
        "-NoExit",
        "-Command",
        "& { if (Test-Path '.venv\\Scripts\\Activate.ps1') { & '.venv\\Scripts\\Activate.ps1' } }"
      ]
    }
  },
  
  // 文件和搜索排除
  "files.exclude": {
    "**/.venv": true,
    "**/node_modules": true
  },
  "search.exclude": {
    "**/.venv": true,
    "**/node_modules": true
  },
  "explorer.excludeGitIgnore": true
}
```

### 1.3 保存
按 Ctrl + S 保存文件

---

## ✅ 第二步：配置 tsconfig.json

### 2.1 检查项目根目录
确保 `tsconfig.json` 与 `package.json` 在同一级目录

```
你的项目/
├── package.json
├── tsconfig.json          ← 在这里
├── node_modules/
└── ...
```

### 2.2 创建或编辑 tsconfig.json
在项目根目录创建 `tsconfig.json` 文件，复制以下内容：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "strict": false,
    "skipLibCheck": true,
    "skipDefaultLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true,
    "moduleResolution": "node",
    "allowJs": true,
    "checkJs": false
  },
  "include": [
    ".claude/**/*.js",
    "duomotai/**/*.js",
    "html/**/*.js",
    "modules/**/*.js",
    "scripts/**/*.js",
    "server/**/*.js"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "build",
    ".venv",
    "**/*.test.js"
  ]
}
```

### 2.3 保存
按 Ctrl + S 保存

---

## ✅ 第三步：配置 package.json

### 3.1 打开 package.json
在项目根目录打开 `package.json`

### 3.2 添加编译脚本
修改 `package.json`，添加 `"scripts"` 部分：

```json
{
  "scripts": {
    "check": "tsc --noEmit",
    "build": "tsc"
  },
  "devDependencies": {
    "typescript": "^5.9.3"
  }
}
```

### 3.3 保存
按 Ctrl + S 保存

### 3.4 安装依赖
在终端运行：

```bash
npm install
```

---

## ✅ 第四步：验证配置

### 4.1 验证 TypeScript 版本
```bash
npx tsc --version
```

**预期输出**：
```
Version 5.x.x
```

### 4.2 检查配置
```bash
npm run check
```

**预期输出**：无错误提示，返回命令提示符

### 4.3 测试编译
```bash
npm run build
```

**预期输出**：
- 可能生成 `dist/` 文件夹
- 无错误提示

### 4.4 验证成功
如果所有命令都没有错误，说明**配置完全成功**！✅

---

## 🔍 常见问题排查

### 问题 1：`tsc: command not found`
**解决方案**：
```bash
npm install -D typescript
```

### 问题 2：找不到 tsconfig.json
**检查项目结构**：
```bash
# 确保在项目根目录
ls tsconfig.json
ls package.json
```

### 问题 3：JSON 格式错误
**检查方法**：
- 确保没有多余逗号
- 确保所有引号匹配
- 在线 JSON 验证器：https://jsonlint.com/

### 问题 4：仍然出现频繁 compacting
**进阶方案**：
1. 模块化大型 JavaScript 文件（>2000行）
2. 在启动 VS Code 时增加内存：
   ```bash
   code --max-memory=8192
   ```

---

## 📊 配置效果检查表

| 项目 | 完成情况 | 备注 |
|------|--------|------|
| VS Code settings.json 优化 | ☐ | 增加内存，减少监视 |
| tsconfig.json 创建 | ☐ | 配置 TypeScript |
| package.json 添加脚本 | ☐ | 添加 npm 命令 |
| npm install 安装依赖 | ☐ | 安装 TypeScript |
| npx tsc --version 验证 | ☐ | 检查版本 |
| npm run check 测试 | ☐ | 测试检查命令 |
| npm run build 测试 | ☐ | 测试编译命令 |

---

## 🚀 优化效果

完成以上配置后，你应该能看到：

✅ **VS Code 性能提升**
- compacting 频率明显降低
- 编辑响应速度加快
- 内存占用减少

✅ **代码质量改善**
- 可以通过 `npm run check` 快速检查代码
- 为未来 TypeScript 迁移做准备
- 更好的代码组织

✅ **开发体验改善**
- 快捷命令：`npm run check` 和 `npm run build`
- 自动生成编译输出
- 类型检查支持

---

## 📝 重装系统时的快速恢复步骤

1. **复制 settings.json** 配置内容
2. **复制 tsconfig.json** 配置内容
3. **复制 package.json** 中的 `scripts` 和 `devDependencies`
4. 运行 `npm install`
5. 运行 `npm run check` 验证

**预计时间**：5 分钟

---

## 💡 进阶建议

### 如果还有性能问题
考虑模块化大型文件（如 `debateEngine.js`）：

```javascript
// 原来：debateEngine.js (2752 lines)
// 改为：
// debateEngine/
//   ├── core.js        (核心逻辑)
//   ├── ui.js          (UI相关)
//   ├── api.js         (API调用)
//   └── index.js       (入口)
```

### 如果要迁移到 TypeScript
1. 重命名文件：`.js` → `.ts`
2. TypeScript 会自动检查类型
3. 逐步修复类型错误
4. 代码质量显著提升

---

## 📞 快速参考

**常用命令**：
```bash
npm run check           # 检查代码（推荐经常运行）
npm run build           # 编译代码
npx tsc --version       # 检查 TypeScript 版本
npm install             # 安装/更新依赖
```

**配置文件位置**：
- VS Code settings：`%APPDATA%\Code\User\settings.json`（Windows）
- 项目 tsconfig：`项目根目录/tsconfig.json`
- 项目 package：`项目根目录/package.json`

---

**最后更新**：2025年10月13日  
**适用版本**：TypeScript 5.9.3+, VS Code 最新版