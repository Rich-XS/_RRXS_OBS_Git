## 全局 settings.json C:\Users\rrxs\AppData\Roaming\Code\User
```
// --- 性能优化和基础设置 ---
{
    // 基础和性能优化设置（保留您的现有设置）
    "github.copilot.nextEditSuggestions.enabled": true,
    "security.workspace.trust.untrustedFiles": "open",
    "workbench.startupEditor": "none",
    "editor.experimentalGpuAcceleration": "on",
    "workbench.experimental.experimentalWebRender": true,
    "window.experimental.windowControlsOverlay.enabled": true,
    "editor.fontRenderMethod": "auto",
    "workbench.editor.wrapTabs": false,
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "git.enableSmartCommit": true,
    "python.defaultInterpreterPath": "c:\\Python313\\python.exe",
    "git.enabled": false,

    // --- CCR 免费/低成本模型配置（关键） ---
    "claudeCode.modelConfiguration": {
        // 核心任务：免费且中文能力强的 DeepSeek V3.1
        "default": "openrouter,deepseek/deepseek-chat-v3.1:free", 
        // 后台任务：与 default 相同，保持低成本持续运行
        "background": "openrouter,deepseek/deepseek-chat-v3.1:free", 
        // 思考/规划：免费且快速的 GLM-4.5-Air
        "think": "openrouter,z-ai/glm-4.5-air:free", 
        // 长上下文：使用 DeepSeek 应对，降低触发频率
        "longContext": "openrouter,deepseek/deepseek-chat-v3.1:free",
        // 降低长上下文触发阈值，避免不必要的内存和费用
        "longContextThreshold": 32000, 
        // 联网搜索：免费 GLM-4.5-Air 联网能力
        "webSearch": "openrouter,z-ai/glm-4.5-air:free", 
        // 图像处理：免费 Qwen2.5-VL
        "image": "openrouter,qwen/qwen2.5-vl-72b-instruct:free" 
    },
    
    // --- 内存优化：文件排除配置（rrxsxyz_next & _RRXS_OBS） ---
    "files.exclude": {
        "**/node_modules": true,           // 网站/JS项目常见，占用巨大内存，必排
        "**/.git": true,                  // Git 文件夹，通常不需要 VSC 持续监视
        "**/*.log": true,                 // 日志文件，易堆积
        "**/*.tmp": true,                 // 临时文件
        "**/.DS_Store": true,             // macOS 文件
      "**/*.pdf": true, // 如果 Obsidian 库里有大量 PDF 文档
        "**/*.mp4": true, // 排除视频文件，减少索引压力
        "**/_RRXS_OBS/Exported": true, // 如果您有导出内容的文件夹
        "**/_RRXS_OBS/.obsidian/plugins": true, // 排除插件代码文件夹
        
        
        // 针对 Obsidian 主库 (_RRXS_OBS) 的排除项，大幅减少索引负载
        "**/_RRXS_OBS/.obsidian/backups": true,  // Obsidian 备份文件，可能非常多
        "**/_RRXS_OBS/.obsidian/workspace*": true, // 工作区配置文件，减少监视
        "**/_RRXS_OBS/.obsidian/cache": true,    // 缓存文件
        "**/_RRXS_OBS/attachments": true,        // 如果附件很多，需要排除
        "**/_RRXS_OBS/Assets": true             // 你的图片等资源文件夹（如果文件量大）
    }
}
```

## 工作区 settings.json rrxsxyz_next .vscode
```
permissions": {

    "allow": [

      "acceptEdits"

    ],

    "deny": [],

    "ask": []

  }

}

```

## 工作区 settings.local.json rrxsxyz_next .vscode
```
{
  "permissions": {
    "allow": [
      "allow writes"
    ],
    "deny": [],
    "ask": []
  }
}
```

## 工作区 settings.json _RRXS_OBS .vscode
```
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)"
    ],
    "deny": [],
    "ask": []
  }
}
```

## 工作区 settings.local.json _RRXS_OBS .vscode
```
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)"
    ],
    "deny": [],
    "ask": []
  }
}
```