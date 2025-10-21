// content.js - 聊天记录捕获脚本
class ChatHistorySaver {
  constructor() {
    this.platform = this.detectPlatform();
    this.isCapturing = false;
    this.lastSaveTime = 0;
    this.captureInterval = 30000; // 30秒保存一次
    this.init();
  }

  detectPlatform() {
    const hostname = window.location.hostname;
    if (hostname.includes('openai.com')) return 'ChatGPT';
    if (hostname.includes('claude.ai')) return 'Claude';
    if (hostname.includes('gemini.google.com')) return 'Gemini';
    if (hostname.includes('moonshot.cn')) return 'Kimi';
    if (hostname.includes('tongyi.aliyun.com')) return 'Tongyi';
    return 'Unknown';
  }

  init() {
    console.log(`RRXS Chat Saver initialized for ${this.platform}`);
    this.startAutoCapture();
    this.addManualSaveButton();
  }

  startAutoCapture() {
    setInterval(() => {
      if (Date.now() - this.lastSaveTime > this.captureInterval) {
        this.captureAndSave();
      }
    }, 10000); // 每10秒检查一次
  }

  addManualSaveButton() {
    const button = document.createElement('button');
    button.innerHTML = '💾 保存对话';
    button.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
      background: #4CAF50;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 12px;
    `;
    button.onclick = () => this.captureAndSave(true);
    document.body.appendChild(button);
  }

  async captureAndSave(manual = false) {
    try {
      const chatData = this.extractChatData();
      if (chatData.messages.length === 0) return;

      const sessionData = {
        id: this.generateId(),
        platform: this.platform,
        title: this.getPageTitle(),
        url: window.location.href,
        timestamp: new Date().toISOString(),
        messages: chatData.messages,
        metadata: {
          userAgent: navigator.userAgent,
          manual: manual,
          messageCount: chatData.messages.length
        }
      };

      // 保存到 Chrome 存储
      await this.saveToStorage(sessionData);
      
      // 下载 Markdown 文件
      this.downloadMarkdown(sessionData);
      
      this.lastSaveTime = Date.now();
      
      if (manual) {
        this.showNotification('✅ 对话已保存', 'success');
      }
      
    } catch (error) {
      console.error('保存对话失败:', error);
      this.showNotification('❌ 保存失败', 'error');
    }
  }

  extractChatData() {
    const messages = [];
    let messageElements = [];

    // 根据平台选择不同的选择器
    switch (this.platform) {
      case 'ChatGPT':
        messageElements = document.querySelectorAll('[data-message-author-role]');
        break;
      case 'Claude':
        messageElements = document.querySelectorAll('.font-claude-message, [data-is-streaming]');
        break;
      case 'Gemini':
        messageElements = document.querySelectorAll('.model-response-text, .user-input-text');
        break;
      case 'Kimi':
        messageElements = document.querySelectorAll('.message-item');
        break;
      default:
        // 通用选择器
        messageElements = document.querySelectorAll('.message, .conversation-turn, [role="article"]');
    }

    messageElements.forEach((element, index) => {
      const content = this.extractTextContent(element);
      if (content.trim()) {
        messages.push({
          id: `msg_${index}`,
          role: this.detectMessageRole(element),
          content: content,
          timestamp: new Date().toISOString(),
          element_info: {
            tagName: element.tagName,
            className: element.className,
            index: index
          }
        });
      }
    });

    return { messages };
  }

  extractTextContent(element) {
    // 移除按钮和其他UI元素
    const clone = element.cloneNode(true);
    const buttonsToRemove = clone.querySelectorAll('button, .copy-button, .action-button');
    buttonsToRemove.forEach(btn => btn.remove());
    
    return clone.textContent.trim();
  }

  detectMessageRole(element) {
    const elementText = element.outerHTML.toLowerCase();
    const classNames = element.className.toLowerCase();
    
    if (elementText.includes('user') || classNames.includes('user') || 
        elementText.includes('human') || classNames.includes('human')) {
      return 'user';
    }
    if (elementText.includes('assistant') || classNames.includes('assistant') || 
        elementText.includes('bot') || classNames.includes('ai')) {
      return 'assistant';
    }
    
    // 根据位置推断（偶数索引通常是用户，奇数是AI）
    const allMessages = document.querySelectorAll('.message, .conversation-turn, [role="article"]');
    const index = Array.from(allMessages).indexOf(element);
    return index % 2 === 0 ? 'user' : 'assistant';
  }

  getPageTitle() {
    // 尝试从不同位置获取对话标题
    const titleSelectors = [
      '.conversation-title',
      '.chat-title',
      '[data-testid="conversation-title"]',
      'h1',
      'title'
    ];
    
    for (const selector of titleSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent.trim()) {
        return element.textContent.trim();
      }
    }
    
    return `${this.platform}对话_${new Date().toLocaleString()}`;
  }

  async saveToStorage(sessionData) {
    const storageKey = `chat_${sessionData.platform}_${sessionData.id}`;
    
    // 保存到 Chrome 本地存储
    return new Promise((resolve, reject) => {
      chrome.storage.local.set({ [storageKey]: sessionData }, () => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve();
        }
      });
    });
  }

  downloadMarkdown(sessionData) {
    const markdown = this.generateMarkdown(sessionData);
    const fileName = `${sessionData.platform}_对话_${sessionData.id}.md`;
    
    const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  generateMarkdown(sessionData) {
    const date = new Date(sessionData.timestamp).toLocaleString('zh-CN');
    
    let markdown = `# ${sessionData.title}

**平台**: ${sessionData.platform}
**时间**: ${date}
**URL**: ${sessionData.url}
**消息数量**: ${sessionData.messages.length}

---

## 对话内容

`;

    sessionData.messages.forEach((msg, index) => {
      const role = msg.role === 'user' ? '👤 **用户**' : '🤖 **AI助手**';
      const time = new Date(msg.timestamp).toLocaleTimeString('zh-CN');
      
      markdown += `### ${index + 1}. ${role} (${time})

${msg.content}

---

`;
    });

    markdown += `
## 元数据

- **对话ID**: ${sessionData.id}
- **保存时间**: ${date}
- **平台**: ${sessionData.platform}
- **消息总数**: ${sessionData.messages.length}
- **是否手动保存**: ${sessionData.metadata.manual ? '是' : '否'}

## 标签

#聊天记录 #${sessionData.platform} #AI对话 #${new Date(sessionData.timestamp).toISOString().split('T')[0]}

---
*由 RRXS Chat History Saver 自动生成*
`;

    return markdown;
  }

  showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 70px;
      right: 20px;
      z-index: 10001;
      padding: 12px 20px;
      border-radius: 5px;
      color: white;
      font-size: 14px;
      font-weight: bold;
      background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      transition: opacity 0.3s;
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后自动删除
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
  }

  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }
}

// 页面加载完成后启动
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new ChatHistorySaver();
  });
} else {
  new ChatHistorySaver();
}