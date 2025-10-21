// background.js - 后台服务脚本
class BackgroundService {
  constructor() {
    this.init();
  }

  init() {
    // 监听安装事件
    chrome.runtime.onInstalled.addListener(() => {
      this.onInstalled();
    });

    // 监听消息
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
      return true; // 保持消息通道开放
    });

    // 监听标签页更新
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && this.isSupportedSite(tab.url)) {
        this.initializeContentScript(tabId);
      }
    });
  }

  async onInstalled() {
    // 设置默认配置
    const defaultSettings = {
      autoSave: true,
      autoDownload: true,
      showNotifications: true,
      saveInterval: 30
    };

    await this.setStorageData('settings', defaultSettings);
    
    console.log('RRXS Chat History Saver 已安装');
  }

  async handleMessage(message, sender, sendResponse) {
    try {
      switch (message.action) {
        case 'saveChat':
          await this.saveChatData(message.data);
          sendResponse({ success: true });
          break;
          
        case 'getSettings':
          const settings = await this.getStorageData('settings');
          sendResponse({ settings });
          break;
          
        case 'updateLastSaveTime':
          await this.setStorageData('lastSaveTime', message.timestamp);
          sendResponse({ success: true });
          break;
          
        case 'exportData':
          const exportData = await this.exportAllData();
          sendResponse({ data: exportData });
          break;
          
        default:
          sendResponse({ error: 'Unknown action' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ error: error.message });
    }
  }

  async saveChatData(chatData) {
    const storageKey = `chat_${chatData.platform}_${chatData.id}`;
    await this.setStorageData(storageKey, chatData);
    
    // 更新统计信息
    await this.updateStats(chatData);
    
    console.log(`已保存聊天记录: ${storageKey}`);
  }

  async updateStats(chatData) {
    const stats = await this.getStorageData('stats') || {
      totalSessions: 0,
      totalMessages: 0,
      platforms: {},
      lastUpdate: null
    };

    stats.totalSessions += 1;
    stats.totalMessages += chatData.messages.length;
    stats.platforms[chatData.platform] = (stats.platforms[chatData.platform] || 0) + 1;
    stats.lastUpdate = new Date().toISOString();

    await this.setStorageData('stats', stats);
  }

  async exportAllData() {
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

  isSupportedSite(url) {
    if (!url) return false;
    
    const supportedDomains = [
      'chat.openai.com',
      'claude.ai',
      'gemini.google.com',
      'kimi.moonshot.cn',
      'tongyi.aliyun.com'
    ];
    
    return supportedDomains.some(domain => url.includes(domain));
  }

  async initializeContentScript(tabId) {
    try {
      const settings = await this.getStorageData('settings');
      chrome.tabs.sendMessage(tabId, {
        action: 'initialize',
        settings: settings
      });
    } catch (error) {
      console.error('初始化内容脚本失败:', error);
    }
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

// 初始化后台服务
new BackgroundService();