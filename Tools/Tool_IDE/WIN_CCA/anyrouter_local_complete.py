#!/usr/bin/env python3
"""
AnyRouter 本地完整版 - 包含监控功能
用途：在本地电脑运行，提供完整的刷新和监控功能
"""

import asyncio
import logging
import sys
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout
import re
import schedule
import time

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('anyrouter_local.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ============ 配置区域 ============
# 多账号配置列表
ACCOUNT_LIST = [
    {
        'username': '123463452',
        'password': '123463452',
        'name': 'rrxsUK'
    },
    {
        'username': 'RichardX',
        'password': 'Austin050824',
        'name': 'RichardXieSong'
    },
    {
        'username': '5757344544',
        'password': '5757344544',
        'name': 'rrxsJP'
    },
]

# 全局配置
CONFIG = {
    'URL': 'https://anyrouter.top/console',
    'TIMEOUT': 30000,  # 30秒超时
    'WAIT_AFTER_LOGIN': 5000,  # 登录后等待5秒
    'REFRESH_RETRY_COUNT': 3,  # 刷新按钮重试次数
    'SCREENSHOT_ON_ERROR': True,
    'ACCOUNT_DELAY': 2,  # 账号之间的延迟（秒）
    'ENABLE_MONITORING': True,  # 启用使用量监控
    'DAILY_REFRESH_TARGET': 25,  # 每日刷新目标金额（美元）
    'DATA_FILE': 'usage_history.json',  # 历史数据文件
    'AUTO_SCHEDULE': False,  # 是否自动定时运行
}
# =================================

class ColoredLogger:
    """彩色日志工具类"""
    @staticmethod
    def success(msg):
        logger.info(f"\033[92m{msg}\033[0m")  # 绿色

    @staticmethod
    def account_info(msg):
        logger.info(f"\033[94m{msg}\033[0m")  # 蓝色

    @staticmethod
    def warning(msg):
        logger.warning(f"\033[93m{msg}\033[0m")  # 黄色

    @staticmethod
    def money(msg):
        logger.info(f"\033[96m{msg}\033[0m")  # 青色

    @staticmethod
    def header(msg):
        logger.info(f"\033[95m{msg}\033[0m")  # 紫色

# 添加彩色日志方法
logger.success = ColoredLogger.success
logger.account_info = ColoredLogger.account_info
logger.warning_colored = ColoredLogger.warning
logger.money = ColoredLogger.money
logger.header = ColoredLogger.header

class UsageMonitor:
    """使用量监控类"""

    def __init__(self, data_file: str = CONFIG['DATA_FILE']):
        self.data_file = data_file
        self.today = datetime.now().strftime('%Y-%m-%d')

    def load_history(self) -> Dict:
        """加载历史数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"加载历史数据失败: {e}")
            return {}

    def save_history(self, data: Dict) -> None:
        """保存历史数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存历史数据失败: {e}")

    def record_usage(self, account_name: str, usage_data: Dict) -> None:
        """记录使用量数据"""
        history = self.load_history()

        if account_name not in history:
            history[account_name] = {}

        # 记录今日数据
        history[account_name][self.today] = {
            **usage_data,
            'timestamp': datetime.now().isoformat()
        }

        self.save_history(history)

    def get_yesterday_data(self, account_name: str) -> Optional[Dict]:
        """获取昨日数据"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        history = self.load_history()

        if account_name in history and yesterday in history[account_name]:
            return history[account_name][yesterday]
        return None

    def verify_refresh_success(self, account_name: str, current_balance: float) -> Tuple[bool, str]:
        """验证刷新是否成功"""
        yesterday_data = self.get_yesterday_data(account_name)

        if not yesterday_data:
            return True, f"无昨日数据对比，当前余额: ${current_balance:.2f}"

        yesterday_balance = yesterday_data.get('balance_after_refresh', yesterday_data.get('current_balance', 0))
        expected_today = yesterday_balance + CONFIG['DAILY_REFRESH_TARGET']

        # 允许一定的误差范围（±1美元）
        if abs(current_balance - expected_today) <= 1.0:
            return True, f"✅ 刷新成功！昨日: ${yesterday_balance:.2f} → 今日: ${current_balance:.2f} (增加 ${current_balance - yesterday_balance:.2f})"
        else:
            return False, f"❌ 刷新异常！期望: ${expected_today:.2f}，实际: ${current_balance:.2f} (差异 ${current_balance - expected_today:.2f})"

    def generate_usage_report(self) -> None:
        """生成使用量报告"""
        history = self.load_history()

        logger.header("=" * 80)
        logger.header("💰 AnyRouter 账号余额和使用量报告")
        logger.header(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.header("=" * 80)

        total_balance = 0
        for account_name in [acc['name'] for acc in ACCOUNT_LIST]:
            today_data = history.get(account_name, {}).get(self.today, {})

            if today_data:
                balance = today_data.get('current_balance', 0)
                refresh_success = today_data.get('refresh_success', False)
                status = "✅ 成功" if refresh_success else "❌ 失败"
                logger.money(f"{account_name}: ${balance:.2f} - 刷新{status}")
                total_balance += balance
            else:
                logger.money(f"{account_name}: 无今日数据")

        logger.header(f"💰 总余额: ${total_balance:.2f}")

        # 显示7日趋势
        logger.header("\n📈 7日余额趋势:")
        for i in range(7, 0, -1):
            date = (datetime.now() - timedelta(days=i-1)).strftime('%Y-%m-%d')
            date_total = 0
            date_accounts = 0

            for account_name in [acc['name'] for acc in ACCOUNT_LIST]:
                if account_name in history and date in history[account_name]:
                    date_total += history[account_name][date].get('current_balance', 0)
                    date_accounts += 1

            if date_accounts > 0:
                logger.info(f"  {date}: ${date_total:.2f} ({date_accounts}个账号)")

        # 使用建议
        if total_balance > 0:
            # 找到余额最高的账号
            max_balance = 0
            recommended_account = ""
            for account_name in [acc['name'] for acc in ACCOUNT_LIST]:
                today_data = history.get(account_name, {}).get(self.today, {})
                balance = today_data.get('current_balance', 0)
                if balance > max_balance:
                    max_balance = balance
                    recommended_account = account_name

            if recommended_account:
                logger.header(f"\n💡 使用建议:")
                logger.header(f"建议优先使用 {recommended_account} (余额最高: ${max_balance:.2f})")

        logger.header("=" * 80)

class AnyRouterRefresher:
    """AnyRouter 刷新器 - 本地完整版"""

    def __init__(self, account: Dict[str, str]):
        self.account = account
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright_instance = None
        self.usage_monitor = UsageMonitor() if CONFIG['ENABLE_MONITORING'] else None
        self.usage_data = {}

    async def init_browser(self) -> None:
        """初始化浏览器实例"""
        self.playwright_instance = await async_playwright().start()

        # 本地环境可以使用正常模式
        self.browser = await self.playwright_instance.chromium.launch(
            headless=False,  # 本地可以显示浏览器
            args=['--disable-blink-features=AutomationControlled'],
            timeout=60000
        )

        # 创建浏览器上下文
        context = await self.browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )

        # 创建新页面
        self.page = await context.new_page()
        self.page.set_default_timeout(CONFIG['TIMEOUT'])

        logger.info(f"[{self.account['name']}] 浏览器初始化成功")

    async def extract_usage_info(self) -> Dict:
        """提取使用量和余额信息"""
        if not self.usage_monitor:
            return {}

        try:
            logger.info(f"[{self.account['name']}] 开始提取使用量信息...")
            await asyncio.sleep(3)

            usage_info = {
                'extraction_time': datetime.now().isoformat(),
                'raw_data': {},
                'current_balance': 0.0,
                'daily_usage': 0.0
            }

            # 尝试提取页面文本中的金额信息
            page_content = await self.page.content()

            # 使用正则表达式查找金额
            money_patterns = [
                r'\$\s*(\d+\.?\d*)',  # $25.00 或 $25
                r'(\d+\.?\d*)\s*USD',  # 25.00 USD
                r'余额[：:]\s*\$?(\d+\.?\d*)',  # 余额: $25.00
                r'Balance[：:]\s*\$?(\d+\.?\d*)',  # Balance: $25.00
            ]

            found_amounts = []
            for pattern in money_patterns:
                matches = re.findall(pattern, page_content, re.IGNORECASE)
                for match in matches:
                    try:
                        amount = float(match)
                        if 0 <= amount <= 1000:  # 合理的金额范围
                            found_amounts.append(amount)
                    except ValueError:
                        continue

            if found_amounts:
                # 通常最大的金额是余额
                usage_info['current_balance'] = max(found_amounts)
                usage_info['raw_data']['found_amounts'] = found_amounts

                logger.money(f"[{self.account['name']}] 💰 检测到余额: ${usage_info['current_balance']:.2f}")
            else:
                logger.warning_colored(f"[{self.account['name']}] ⚠️  未能自动检测到余额信息")

            return usage_info

        except Exception as e:
            logger.error(f"[{self.account['name']}] 提取使用量信息失败: {e}")
            return {'extraction_time': datetime.now().isoformat(), 'error': str(e)}

    async def login_and_refresh(self) -> bool:
        """登录并刷新"""
        try:
            logger.account_info(f"开始处理账号: {self.account['name']} ({self.account['username']})")

            # 初始化浏览器
            await self.init_browser()

            # 导航到登录页面
            logger.info(f"[{self.account['name']}] 开始访问: {CONFIG['URL']}")
            response = await self.page.goto(
                CONFIG['URL'],
                wait_until='networkidle',
                timeout=60000
            )

            if not response:
                logger.error(f"[{self.account['name']}] 页面加载失败")
                return False

            # 等待页面稳定
            await asyncio.sleep(2)

            # 如果启用监控，先提取登录前信息
            if self.usage_monitor:
                login_before_info = await self.extract_usage_info()
                self.usage_data['before_login'] = login_before_info

            # 查找并填写用户名
            username_selectors = [
                'input[type="text"][name*="user" i]',
                'input[type="text"][name*="email" i]',
                'input[type="text"][placeholder*="用户" i]',
                '#username', '#email',
                'input.semi-input[type="text"]'
            ]

            username_input = None
            for selector in username_selectors:
                try:
                    username_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if username_input:
                        logger.info(f"[{self.account['name']}] 找到用户名输入框")
                        break
                except:
                    continue

            if not username_input:
                logger.error(f"[{self.account['name']}] 未找到用户名输入框")
                return False

            await username_input.click()
            await username_input.fill('')
            await username_input.type(self.account['username'], delay=100)

            # 查找并填写密码
            password_input = await self.page.wait_for_selector('input[type="password"]', timeout=5000)
            await password_input.click()
            await password_input.fill('')
            await password_input.type(self.account['password'], delay=100)

            # 查找并点击登录按钮
            login_selectors = [
                'button[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Login")',
                'button.semi-button-primary'
            ]

            login_button = None
            for selector in login_selectors:
                try:
                    login_button = await self.page.wait_for_selector(selector, timeout=3000)
                    if login_button:
                        break
                except:
                    continue

            if not login_button:
                logger.error(f"[{self.account['name']}] 未找到登录按钮")
                return False

            await login_button.click()
            logger.info(f"[{self.account['name']}] 已点击登录按钮")

            # 等待登录完成
            await asyncio.sleep(CONFIG['WAIT_AFTER_LOGIN'] / 1000)

            # 提取登录后信息
            if self.usage_monitor:
                login_after_info = await self.extract_usage_info()
                self.usage_data['after_login'] = login_after_info

                current_balance = login_after_info.get('current_balance', 0)
                if current_balance > 0:
                    logger.money(f"[{self.account['name']}] 💰 登录后余额: ${current_balance:.2f}")

            # 点击刷新按钮 - 使用JavaScript方法
            logger.info(f"[{self.account['name']}] 准备点击刷新按钮")

            refresh_success = False
            for attempt in range(CONFIG['REFRESH_RETRY_COUNT']):
                try:
                    refresh_button = await self.page.evaluate_handle('''
                        () => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            for (const btn of buttons) {
                                const icons = btn.querySelectorAll('[class*="refresh"], [class*="reload"]');
                                if (icons.length > 0) {
                                    return btn;
                                }
                            }
                            const headerButtons = document.querySelectorAll('header button, [class*="header"] button');
                            if (headerButtons.length > 0) {
                                return headerButtons[headerButtons.length - 1];
                            }
                            return null;
                        }
                    ''')

                    if refresh_button:
                        await self.page.evaluate('(btn) => btn.click()', refresh_button)
                        logger.success(f"[{self.account['name']}] ✅ 成功点击刷新按钮！")
                        refresh_success = True
                        break

                except Exception as e:
                    logger.debug(f"[{self.account['name']}] 刷新尝试 {attempt+1} 失败: {e}")
                    await asyncio.sleep(2)

            if not refresh_success:
                logger.error(f"[{self.account['name']}] 刷新按钮点击失败")
                return False

            # 等待刷新完成并提取最终信息
            await asyncio.sleep(3)

            if self.usage_monitor:
                after_refresh_info = await self.extract_usage_info()
                self.usage_data['after_refresh'] = after_refresh_info

                final_balance = after_refresh_info.get('current_balance', 0)
                if final_balance > 0:
                    logger.money(f"[{self.account['name']}] 💰 刷新后余额: ${final_balance:.2f}")

                    # 记录数据
                    self.usage_monitor.record_usage(self.account['name'], {
                        'current_balance': final_balance,
                        'balance_after_refresh': final_balance,
                        'usage_data': self.usage_data,
                        'refresh_success': True
                    })

                    # 验证刷新效果
                    success, message = self.usage_monitor.verify_refresh_success(
                        self.account['name'], final_balance
                    )
                    if success:
                        logger.success(f"[{self.account['name']}] {message}")
                    else:
                        logger.warning_colored(f"[{self.account['name']}] {message}")

            return True

        except Exception as e:
            logger.error(f"[{self.account['name']}] 处理失败: {e}")
            return False

        finally:
            # 清理浏览器资源
            if self.browser:
                await self.browser.close()
            if self.playwright_instance:
                await self.playwright_instance.stop()

async def refresh_all_accounts():
    """刷新所有账号"""
    logger.header("=" * 80)
    logger.header(f"AnyRouter 本地完整版启动 - 共 {len(ACCOUNT_LIST)} 个账号")
    logger.header("=" * 80)

    results = []

    for i, account in enumerate(ACCOUNT_LIST):
        refresher = AnyRouterRefresher(account)
        success = await refresher.login_and_refresh()
        results.append({
            'account': account['name'],
            'username': account['username'],
            'success': success
        })

        # 如果不是最后一个账号，等待一段时间
        if i < len(ACCOUNT_LIST) - 1:
            logger.info(f"等待 {CONFIG['ACCOUNT_DELAY']} 秒后处理下一个账号...")
            await asyncio.sleep(CONFIG['ACCOUNT_DELAY'])

    # 输出总结
    logger.header("=" * 80)
    logger.header("任务执行完成 - 结果汇总:")
    logger.header("=" * 80)

    success_count = 0
    for result in results:
        status = "✅ 成功" if result['success'] else "❌ 失败"
        logger.info(f"{result['account']} ({result['username']}): {status}")
        if result['success']:
            success_count += 1

    logger.header("=" * 80)
    logger.header(f"总计: {success_count}/{len(ACCOUNT_LIST)} 个账号刷新成功")
    logger.header("=" * 80)

    # 生成详细报告
    if CONFIG['ENABLE_MONITORING']:
        monitor = UsageMonitor()
        monitor.generate_usage_report()

async def check_balance_only():
    """仅检查余额，不执行刷新"""
    logger.header("=" * 80)
    logger.header("AnyRouter 余额检查模式")
    logger.header("=" * 80)

    results = []

    for account in ACCOUNT_LIST:
        refresher = AnyRouterRefresher(account)
        try:
            # 只初始化浏览器和登录，不刷新
            await refresher.init_browser()

            response = await refresher.page.goto(CONFIG['URL'], timeout=60000)
            await asyncio.sleep(2)

            # 登录
            username_input = await refresher.page.wait_for_selector('input[type="text"]', timeout=10000)
            await username_input.fill(account['username'])

            password_input = await refresher.page.wait_for_selector('input[type="password"]', timeout=5000)
            await password_input.fill(account['password'])

            login_button = await refresher.page.wait_for_selector('button[type="submit"]', timeout=5000)
            await login_button.click()
            await asyncio.sleep(3)

            # 提取余额
            usage_info = await refresher.extract_usage_info()
            balance = usage_info.get('current_balance', 0)

            results.append({
                'account': account['name'],
                'balance': balance,
                'success': balance > 0
            })

            logger.money(f"{account['name']}: ${balance:.2f}")

        except Exception as e:
            logger.error(f"[{account['name']}] 检查失败: {e}")
            results.append({
                'account': account['name'],
                'balance': 0,
                'success': False
            })
        finally:
            if refresher.browser:
                await refresher.browser.close()
            if refresher.playwright_instance:
                await refresher.playwright_instance.stop()

    # 显示总结
    total_balance = sum(r['balance'] for r in results)
    successful_checks = sum(1 for r in results if r['success'])

    logger.header(f"\n💰 总余额: ${total_balance:.2f}")
    logger.header(f"✅ 成功检查: {successful_checks}/{len(results)} 个账号")

def show_menu():
    """显示菜单"""
    print("\n" + "="*50)
    print("🚀 AnyRouter 本地完整版")
    print("="*50)
    print("1. 立即刷新所有账号 (包含余额监控)")
    print("2. 仅检查余额 (不执行刷新)")
    print("3. 显示历史报告")
    print("4. 清理历史数据")
    print("5. 退出")
    print("="*50)

def main():
    """主菜单"""
    while True:
        show_menu()
        choice = input("请选择操作 (1-5): ").strip()

        if choice == '1':
            print("\n开始刷新所有账号...")
            asyncio.run(refresh_all_accounts())
            input("\n按回车键继续...")

        elif choice == '2':
            print("\n开始检查余额...")
            asyncio.run(check_balance_only())
            input("\n按回车键继续...")

        elif choice == '3':
            print("\n显示历史报告...")
            monitor = UsageMonitor()
            monitor.generate_usage_report()
            input("\n按回车键继续...")

        elif choice == '4':
            confirm = input("确定要清理历史数据吗？(y/N): ").strip().lower()
            if confirm == 'y':
                if os.path.exists(CONFIG['DATA_FILE']):
                    os.remove(CONFIG['DATA_FILE'])
                    print("历史数据已清理")
                else:
                    print("没有历史数据文件")
            input("\n按回车键继续...")

        elif choice == '5':
            print("再见！")
            break

        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()