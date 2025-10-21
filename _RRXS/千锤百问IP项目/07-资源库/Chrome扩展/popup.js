// popup.js - 扩展弹窗脚本
class PopupManager {
  constructor() {
    this.init();
  }

  async init() {
    await this.loadSettings();
    this.bindEvents();
    this.updateStatus();
    this.loadStats();
  }

  async loadSettings() {
    const settings = await this.getStorageData('settings') || {
      autoSave: true,
      autoDownload: true,
      showNotifications: true,
      saveInterval: 30
    };

    // 更新UI
    document.getElementById('autoSaveToggle').classList.toggle('active', settings.autoSave);
    document.getElementById('autoDownloadToggle').classList.toggle('active', settings.autoDownload);
    document.getElementById('notificationToggle').classList.toggle('active', settings.showNotifications);
    document.getElementById('saveInterval').value = settings.saveInterval;
  }

  bindEvents() {
    // 立即保存按钮
    document.getElementById('saveNow').addEventListener('click', () => {
      this.saveCurrentChat();
    });

    // 导出所有记录
    document.getElementById('exportAll').addEventListener('click', () => {
      this.exportAllHistory();
    });

    // 查看历史记录
    document.getElementById('viewHistory').addEventListener('click', () => {
      this.openHistoryView();
    });

    // 设置切换
    this.bindToggle('autoSaveToggle', 'autoSave');
    this.bindToggle('autoDownloadToggle', 'autoDownload');
    this.bindToggle('notificationToggle', 'showNotifications');

    // 保存间隔设置
    document.getElementById('saveInterval').addEventListener('change', (e) => {
      this.updateSetting('saveInterval', parseInt(e.target.value));
    });
  }

  bindToggle(elementId, settingKey) {
    document.getElementById(elementId).addEventListener('click', async (e) => {
      const element = e.target;
      element.classList.toggle('active');
      const value = element.classList.contains('active');
      await this.updateSetting(settingKey, value);
    });
  }

  async updateSetting(key, value) {
    const settings = await this.getStorageData('settings') || {};
    settings[key] = value;
    await this.setStorageData('settings', settings);
    
    // 通知 content script 更新设置
    this.sendMessageToContentScript({ action: 'updateSettings', settings });
  }

  async saveCurrentChat() {
    try {
      const button = document.getElementById('saveNow');
      button.textContent = '保存中...';
      button.disabled = true;

      await this.sendMessageToContentScript({ action: 'saveNow' });
      
      button.textContent = '✅ 已保存';
      setTimeout(() => {
        button.textContent = '🚀 立即保存当前对话';
        button.disabled = false;
      }, 2000);

      this.updateStatus();
      this.loadStats();
    } catch (error) {
      console.error('保存失败:', error);
      const button = document.getElementById('saveNow');
      button.textContent = '❌ 保存失败';
      button.disabled = false;
    }
  }

  async exportAllHistory() {
    try {
      const button = document.getElementById('exportAll');
      button.textContent = '导出中...';
      button.disabled = true;

      const allData = await this.getAllChatHistory();
      const exportData = this.generateExportData(allData);
      
      this.downloadFile('RRXS_聊天记录_完整导出.json', JSON.stringify(exportData, null, 2));
      this.downloadMarkdownSummary(allData);

      button.textContent = '✅ 导出完成';
      setTimeout(() => {
        button.textContent = '📁 导出所有记录';
        button.disabled = false;
      }, 2000);
    } catch (error) {
      console.error('导出失败:', error);
    }
  }

  async getAllChatHistory() {
    return new Promise((resolve) => {
      chrome.storage.local.get(null, (items) => {
        const chatData = {};
        Object.keys(items).forEach(key => {
          if (key.startsWith('chat_')) {
            chatData[key] = items[key];
          }
        });
        resolve(chatData);
      });
    });
  }

  generateExportData(allData) {
    const sessions = Object.values(allData);
    const summary = {
      exportTime: new Date().toISOString(),
      totalSessions: sessions.length,
      totalMessages: sessions.reduce((sum, session) => sum + session.messages.length, 0),
      platforms: [...new Set(sessions.map(s => s.platform))],
      dateRange: {
        earliest: sessions.reduce((min, s) => s.timestamp < min ? s.timestamp : min, sessions[0]?.timestamp),
        latest: sessions.reduce((max, s) => s.timestamp > max ? s.timestamp : max, sessions[0]?.timestamp)
      }
    };

    return {
      summary,
      sessions: sessions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    };
  }

  downloadMarkdownSummary(allData) {
    const sessions = Object.values(allData);
    let markdown = `# RRXS 聊天记录汇总报告

**生成时间**: ${new Date().toLocaleString('zh-CN')}
**总对话数**: ${sessions.length}
**总消息数**: ${sessions.reduce((sum, session) => sum + session.messages.length, 0)}

## 📊 统计信息

### 平台分布
`;

    const platformStats = {};
    sessions.forEach(session => {
      platformStats[session.platform] = (platformStats[session.platform] || 0) + 1;
    });

    Object.entries(platformStats).forEach(([platform, count]) => {
      markdown += `- **${platform}**: ${count} 个对话\n`;
    });

    markdown += `\n### 时间分布\n`;
    const monthStats = {};
    sessions.forEach(session => {
      const month = new Date(session.timestamp).toISOString().substring(0, 7);
      monthStats[month] = (monthStats[month] || 0) + 1;
    });

    Object.entries(monthStats).sort().forEach(([month, count]) => {
      markdown += `- **${month}**: ${count} 个对话\n`;
    });

    markdown += `\n## 📝 对话列表\n\n`;
    
    sessions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).forEach((session, index) => {
      const date = new Date(session.timestamp).toLocaleString('zh-CN');
      markdown += `### ${index + 1}. ${session.title}
- **平台**: ${session.platform}
- **时间**: ${date}
- **消息数**: ${session.messages.length}
- **ID**: ${session.id}

---

`;
    });

    markdown += `\n## 🏷️ 标签\n\n#聊天记录汇总 #AI对话 #RRXS #数据分析\n\n---\n*由 RRXS Chat History Saver 生成*`;

    this.downloadFile('RRXS_聊天记录_汇总报告.md', markdown);
  }

  downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    chrome.downloads.download({
      url: url,
      filename: filename,
      saveAs: true
    });
  }

  async updateStatus() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const platform = this.detectPlatform(tab.url);
    
    document.getElementById('platform').textContent = platform || '未知平台';
    
    const lastSave = await this.getStorageData('lastSaveTime');
    if (lastSave) {
      document.getElementById('lastSave').textContent = new Date(lastSave).toLocaleString('zh-CN');
    }
  }

  async loadStats() {
    const allData = await this.getAllChatHistory();
    const sessions = Object.values(allData);
    
    const totalSessions = sessions.length;
    const totalMessages = sessions.reduce((sum, session) => sum + session.messages.length, 0);
    const platforms = [...new Set(sessions.map(s => s.platform))];
    
    document.getElementById('stats').innerHTML = `
      📊 总对话数: ${totalSessions}<br>
      💬 总消息数: ${totalMessages}<br>
      🌐 平台数: ${platforms.length}<br>
      💾 存储大小: ${this.formatBytes(JSON.stringify(allData).length)}
    `;
  }

  detectPlatform(url) {
    if (url.includes('openai.com')) return 'ChatGPT';
    if (url.includes('claude.ai')) return 'Claude';
    if (url.includes('gemini.google.com')) return 'Gemini';
    if (url.includes('moonshot.cn')) return 'Kimi';
    if (url.includes('tongyi.aliyun.com')) return 'Tongyi';
    return null;
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  async sendMessageToContentScript(message) {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return chrome.tabs.sendMessage(tab.id, message);
  }

  openHistoryView() {
    chrome.tabs.create({ url: chrome.runtime.getURL('history.html') });
  }

  async getStorageData(key) {
    return new Promise((resolve) => {
      chrome.storage.local.get([key], (result) => {
        resolve(result[key]);
      });
    });
  }

  async setStorageData(key, value) {
    return new Promise((resolve) => {
      chrome.storage.local.set({ [key]: value }, resolve);
    });
  }
}

// 初始化弹窗管理器
document.addEventListener('DOMContentLoaded', () => {
  new PopupManager();
});