# RRXS 聊天记录自动保存系统
# Python 版本 - 完整解决方案

import os
import json
import time
import schedule
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChatHistoryManager:
    def __init__(self):
        self.base_dir = Path(r"d:\OneDrive_RRXS\OneDrive\_RRXS_OBS\_RRXS\千锤百问IP项目\07-资源库\对话记录")
        self.backup_dir = self.base_dir / "backup"
        self.export_dir = self.base_dir / "exports"
        
        # 确保目录存在
        for dir_path in [self.base_dir, self.backup_dir, self.export_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.platforms = {
            'chatgpt': {
                'url': 'https://chat.openai.com',
                'selectors': {
                    'messages': '[data-message-author-role]',
                    'title': '.conversation-title, h1'
                }
            },
            'claude': {
                'url': 'https://claude.ai',
                'selectors': {
                    'messages': '.font-claude-message, [data-is-streaming]',
                    'title': '.conversation-title, h1'
                }
            },
            'gemini': {
                'url': 'https://gemini.google.com',
                'selectors': {
                    'messages': '.model-response-text, .user-input-text',
                    'title': 'h1, .title'
                }
            }
        }
        
        self.driver = None
        self.config = self.load_config()

    def load_config(self):
        """加载配置文件"""
        config_file = self.base_dir / "config.json"
        default_config = {
            "auto_save_interval": 30,  # 分钟
            "max_storage_days": 90,    # 天
            "platforms": ["chatgpt", "claude", "gemini"],
            "auto_backup": True,
            "export_formats": ["json", "markdown"],
            "notification_enabled": True
        }
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
        else:
            config = default_config
            self.save_config(config)
        
        return config

    def save_config(self, config):
        """保存配置文件"""
        config_file = self.base_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def setup_driver(self):
        """设置 Selenium 驱动"""
        options = Options()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # 设置用户数据目录，保持登录状态
        user_data_dir = Path.home() / "chrome_profile_rrxs"
        options.add_argument(f'--user-data-dir={user_data_dir}')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(30)
            return True
        except Exception as e:
            print(f"❌ 无法启动浏览器: {e}")
            return False

    def capture_platform_chat(self, platform_name):
        """捕获指定平台的聊天记录"""
        if not self.driver:
            if not self.setup_driver():
                return None
        
        platform = self.platforms.get(platform_name)
        if not platform:
            print(f"❌ 不支持的平台: {platform_name}")
            return None
        
        try:
            print(f"🔍 正在捕获 {platform_name} 的聊天记录...")
            self.driver.get(platform['url'])
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)
            
            # 获取对话标题
            title = self.get_page_title(platform['selectors']['title'])
            
            # 获取消息
            messages = self.extract_messages(platform['selectors']['messages'])
            
            if not messages:
                print(f"⚠️ {platform_name} 没有发现对话消息")
                return None
            
            # 构建聊天数据
            chat_data = {
                'id': self.generate_id(),
                'platform': platform_name,
                'title': title,
                'url': self.driver.current_url,
                'timestamp': datetime.now().isoformat(),
                'messages': messages,
                'metadata': {
                    'capture_method': 'selenium',
                    'page_title': self.driver.title,
                    'message_count': len(messages)
                }
            }
            
            # 保存数据
            self.save_chat_data(chat_data)
            print(f"✅ 成功保存 {platform_name} 对话记录 (ID: {chat_data['id']})")
            
            return chat_data
            
        except Exception as e:
            print(f"❌ 捕获 {platform_name} 对话失败: {e}")
            return None

    def get_page_title(self, selectors):
        """获取页面标题"""
        try:
            for selector in selectors.split(', '):
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].text.strip():
                    return elements[0].text.strip()
            return f"对话_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        except:
            return f"对话_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def extract_messages(self, selector):
        """提取对话消息"""
        messages = []
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            for i, element in enumerate(elements):
                content = element.text.strip()
                if content:
                    # 判断消息角色
                    role = self.detect_message_role(element, i)
                    
                    messages.append({
                        'id': f"msg_{i}",
                        'role': role,
                        'content': content,
                        'timestamp': datetime.now().isoformat(),
                        'element_info': {
                            'tag': element.tag_name,
                            'class': element.get_attribute('class'),
                            'index': i
                        }
                    })
        except Exception as e:
            print(f"⚠️ 提取消息时出错: {e}")
        
        return messages

    def detect_message_role(self, element, index):
        """检测消息角色"""
        element_html = element.get_attribute('outerHTML').lower()
        class_name = element.get_attribute('class').lower() if element.get_attribute('class') else ''
        
        # 检查关键词
        user_keywords = ['user', 'human', 'me', 'question']
        assistant_keywords = ['assistant', 'ai', 'bot', 'response', 'answer']
        
        for keyword in user_keywords:
            if keyword in element_html or keyword in class_name:
                return 'user'
        
        for keyword in assistant_keywords:
            if keyword in element_html or keyword in class_name:
                return 'assistant'
        
        # 根据索引推断（偶数通常是用户）
        return 'user' if index % 2 == 0 else 'assistant'

    def save_chat_data(self, chat_data):
        """保存聊天数据"""
        # 保存 JSON 格式
        json_file = self.base_dir / f"{chat_data['platform']}_{chat_data['id']}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)
        
        # 保存 Markdown 格式
        if 'markdown' in self.config['export_formats']:
            self.save_as_markdown(chat_data)
        
        # 更新索引
        self.update_index(chat_data)

    def save_as_markdown(self, chat_data):
        """保存为 Markdown 格式"""
        markdown_content = self.generate_markdown(chat_data)
        md_file = self.base_dir / f"{chat_data['platform']}_{chat_data['id']}.md"
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    def generate_markdown(self, chat_data):
        """生成 Markdown 内容"""
        date = datetime.fromisoformat(chat_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
        markdown = f"""# {chat_data['title']}

**平台**: {chat_data['platform']}
**时间**: {date}
**URL**: {chat_data['url']}
**对话ID**: {chat_data['id']}
**消息数量**: {len(chat_data['messages'])}

---

## 对话内容

"""
        
        for i, msg in enumerate(chat_data['messages'], 1):
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            role_text = "用户" if msg['role'] == 'user' else "AI助手"
            msg_time = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
            
            markdown += f"""### {i}. {role_icon} **{role_text}** ({msg_time})

{msg['content']}

---

"""
        
        # 添加元数据
        markdown += f"""
## 元数据

- **对话ID**: {chat_data['id']}
- **平台**: {chat_data['platform']}
- **捕获时间**: {date}
- **消息总数**: {len(chat_data['messages'])}
- **页面标题**: {chat_data['metadata'].get('page_title', '未知')}
- **捕获方法**: {chat_data['metadata'].get('capture_method', '未知')}

## 标签

#聊天记录 #{chat_data['platform']} #AI对话 #{datetime.now().strftime('%Y-%m-%d')}

---
*由 RRXS Chat History Manager 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return markdown

    def update_index(self, chat_data):
        """更新索引文件"""
        index_file = self.base_dir / "index.json"
        
        # 读取现有索引
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {'sessions': [], 'stats': {'total_sessions': 0, 'total_messages': 0, 'platforms': {}}}
        
        # 添加新会话
        session_info = {
            'id': chat_data['id'],
            'platform': chat_data['platform'],
            'title': chat_data['title'],
            'timestamp': chat_data['timestamp'],
            'message_count': len(chat_data['messages']),
            'file_path': f"{chat_data['platform']}_{chat_data['id']}.json"
        }
        
        index['sessions'].append(session_info)
        
        # 更新统计
        index['stats']['total_sessions'] += 1
        index['stats']['total_messages'] += len(chat_data['messages'])
        
        platform = chat_data['platform']
        if platform not in index['stats']['platforms']:
            index['stats']['platforms'][platform] = {'sessions': 0, 'messages': 0}
        
        index['stats']['platforms'][platform]['sessions'] += 1
        index['stats']['platforms'][platform]['messages'] += len(chat_data['messages'])
        
        # 保存更新后的索引
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def auto_capture_all(self):
        """自动捕获所有平台的对话"""
        print(f"🚀 开始自动捕获所有平台的对话...")
        
        results = []
        for platform in self.config['platforms']:
            try:
                result = self.capture_platform_chat(platform)
                if result:
                    results.append(result)
                time.sleep(2)  # 避免请求过快
            except Exception as e:
                print(f"❌ 捕获 {platform} 时出错: {e}")
        
        print(f"✅ 自动捕获完成，成功保存 {len(results)} 个对话")
        return results

    def cleanup_old_files(self):
        """清理过期文件"""
        if not self.config['max_storage_days']:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.config['max_storage_days'])
        deleted_count = 0
        
        for file_path in self.base_dir.glob("*.json"):
            if file_path.name == "index.json" or file_path.name == "config.json":
                continue
            
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                # 移动到备份目录而不是删除
                backup_path = self.backup_dir / file_path.name
                shutil.move(str(file_path), str(backup_path))
                
                # 同时移动对应的 markdown 文件
                md_file = file_path.with_suffix('.md')
                if md_file.exists():
                    backup_md_path = self.backup_dir / md_file.name
                    shutil.move(str(md_file), str(backup_md_path))
                
                deleted_count += 1
        
        if deleted_count > 0:
            print(f"🗑️ 已将 {deleted_count} 个过期文件移动到备份目录")

    def export_summary_report(self):
        """导出汇总报告"""
        index_file = self.base_dir / "index.json"
        if not index_file.exists():
            print("⚠️ 没有找到索引文件，无法生成报告")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        # 生成报告
        report = self.generate_summary_report(index)
        
        # 保存报告
        report_file = self.export_dir / f"聊天记录汇总报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📊 汇总报告已生成: {report_file}")

    def generate_summary_report(self, index):
        """生成汇总报告"""
        stats = index['stats']
        sessions = index['sessions']
        
        # 按时间排序
        sessions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        report = f"""# RRXS 聊天记录汇总报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 总体统计

- **总对话数**: {stats['total_sessions']}
- **总消息数**: {stats['total_messages']}
- **平均每对话消息数**: {stats['total_messages'] / stats['total_sessions']:.1f}

## 🌐 平台分布

"""
        
        for platform, platform_stats in stats['platforms'].items():
            report += f"### {platform.upper()}\n"
            report += f"- 对话数: {platform_stats['sessions']}\n"
            report += f"- 消息数: {platform_stats['messages']}\n"
            report += f"- 平均消息数: {platform_stats['messages'] / platform_stats['sessions']:.1f}\n\n"
        
        # 时间分析
        report += "## 📅 时间分析\n\n"
        
        # 按月统计
        monthly_stats = {}
        daily_stats = {}
        
        for session in sessions:
            date = datetime.fromisoformat(session['timestamp'])
            month_key = date.strftime('%Y-%m')
            day_key = date.strftime('%Y-%m-%d')
            
            monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
            daily_stats[day_key] = daily_stats.get(day_key, 0) + 1
        
        report += "### 月度统计\n"
        for month, count in sorted(monthly_stats.items(), reverse=True)[:6]:
            report += f"- **{month}**: {count} 个对话\n"
        
        report += "\n### 最近7天\n"
        recent_days = sorted(daily_stats.items(), reverse=True)[:7]
        for day, count in recent_days:
            report += f"- **{day}**: {count} 个对话\n"
        
        # 最近对话列表
        report += "\n## 📝 最近对话 (前20个)\n\n"
        
        for i, session in enumerate(sessions[:20], 1):
            date = datetime.fromisoformat(session['timestamp']).strftime('%m-%d %H:%M')
            report += f"{i}. **{session['title'][:50]}{'...' if len(session['title']) > 50 else ''}**\n"
            report += f"   - 平台: {session['platform']} | 时间: {date} | 消息数: {session['message_count']}\n\n"
        
        report += f"""
## 🏷️ 标签

#聊天记录汇总 #AI对话分析 #RRXS #数据统计 #{datetime.now().strftime('%Y-%m')}

---
*由 RRXS Chat History Manager 自动生成*
"""
        
        return report

    def start_scheduler(self):
        """启动定时任务调度器"""
        print("⏰ 启动聊天记录自动保存调度器...")
        
        # 设置定时任务
        interval = self.config['auto_save_interval']
        schedule.every(interval).minutes.do(self.auto_capture_all)
        
        # 每天凌晨2点清理过期文件
        schedule.every().day.at("02:00").do(self.cleanup_old_files)
        
        # 每周日生成汇总报告
        schedule.every().sunday.at("23:00").do(self.export_summary_report)
        
        print(f"✅ 调度器已启动 - 每 {interval} 分钟自动保存一次")
        print("按 Ctrl+C 停止程序")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n🛑 程序已停止")
        finally:
            if self.driver:
                self.driver.quit()

    def generate_id(self):
        """生成唯一ID"""
        return f"{int(time.time())}_{hash(str(datetime.now()))}"[-12:]

    def __del__(self):
        """析构函数，确保浏览器关闭"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()


def main():
    """主函数"""
    print("🚀 RRXS 聊天记录自动保存系统")
    print("=" * 50)
    
    manager = ChatHistoryManager()
    
    while True:
        print("\n📋 请选择操作:")
        print("1. 立即捕获所有平台对话")
        print("2. 捕获指定平台对话")
        print("3. 生成汇总报告")
        print("4. 清理过期文件")
        print("5. 启动自动调度器")
        print("6. 查看配置")
        print("7. 退出")
        
        choice = input("\n请输入选项 (1-7): ").strip()
        
        if choice == '1':
            manager.auto_capture_all()
        
        elif choice == '2':
            print("\n支持的平台:")
            for i, platform in enumerate(manager.config['platforms'], 1):
                print(f"{i}. {platform}")
            
            try:
                platform_choice = int(input("请选择平台 (输入数字): ")) - 1
                platform = manager.config['platforms'][platform_choice]
                manager.capture_platform_chat(platform)
            except (ValueError, IndexError):
                print("❌ 无效选择")
        
        elif choice == '3':
            manager.export_summary_report()
        
        elif choice == '4':
            manager.cleanup_old_files()
        
        elif choice == '5':
            manager.start_scheduler()
        
        elif choice == '6':
            print("\n当前配置:")
            for key, value in manager.config.items():
                print(f"  {key}: {value}")
        
        elif choice == '7':
            print("👋 再见!")
            break
        
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    main()