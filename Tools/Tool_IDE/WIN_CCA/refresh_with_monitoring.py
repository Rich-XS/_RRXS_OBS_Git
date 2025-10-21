#!/usr/bin/env python3
"""
AnyRouter 每日额度自动刷新脚本 V20.0 - 增强监控版
新特性：
- 多账号支持
- JavaScript 定位优先策略
- 优化的资源管理
- 详细的账号级别日志
- 💰 使用量监控和余额跟踪
- 📊 每日$25刷新验证
- 📈 历史数据对比分析
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

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('anyrouter_refresh_monitoring.log', encoding='utf-8')
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

# 添加彩色日志方法
logger.success = ColoredLogger.success
logger.account_info = ColoredLogger.account_info
logger.warning_colored = ColoredLogger.warning
logger.money = ColoredLogger.money

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

class AnyRouterRefresher:
    """AnyRouter 额度刷新自动化类 - 增强监控版"""

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

        # 浏览器启动参数（针对 Docker 环境优化）
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-blink-features=AutomationControlled'
        ]

        self.browser = await self.playwright_instance.chromium.launch(
            headless=True,  # Docker 环境使用无头模式
            args=browser_args,
            timeout=60000
        )

        # 创建浏览器上下文
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            ignore_https_errors=True  # 忽略 SSL 错误
        )

        # 创建新页面
        self.page = await context.new_page()

        # 设置默认超时
        self.page.set_default_timeout(CONFIG['TIMEOUT'])

        logger.info(f"[{self.account['name']}] 浏览器初始化成功")

    async def handle_popups_and_overlays(self) -> None:
        """处理可能的弹窗和遮罩层"""
        try:
            # 处理可能的 Cookie 弹窗
            cookie_selectors = [
                'button:has-text("Accept")',
                'button:has-text("接受")',
                'button:has-text("OK")',
                'button:has-text("确定")',
                '[class*="cookie"] button',
                '[class*="privacy"] button'
            ]

            for selector in cookie_selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=1000)
                    if element:
                        await element.click(force=True)
                        logger.info(f"[{self.account['name']}] 关闭了弹窗: {selector}")
                        await asyncio.sleep(0.5)
                except:
                    continue

            # 处理可能的遮罩层
            overlay_selectors = [
                '[class*="overlay"]',
                '[class*="modal-backdrop"]',
                '[class*="mask"]'
            ]

            for selector in overlay_selectors:
                try:
                    await self.page.evaluate(f'''
                        () => {{
                            const elements = document.querySelectorAll('{selector}');
                            elements.forEach(el => el.remove());
                        }}
                    ''')
                except:
                    continue

        except Exception as e:
            logger.debug(f"[{self.account['name']}] 处理弹窗时出现异常（可忽略）: {e}")

    async def extract_usage_info(self) -> Dict:
        """提取使用量和余额信息"""
        if not self.usage_monitor:
            return {}

        try:
            logger.info(f"[{self.account['name']}] 开始提取使用量信息...")

            # 等待页面加载完成
            await asyncio.sleep(3)

            # 常见的余额/使用量选择器
            balance_selectors = [
                # 余额相关
                '[class*="balance"]',
                '[class*="credit"]',
                '[class*="amount"]',
                'span:has-text("$")',
                'div:has-text("$")',
                '[class*="money"]',
                '[class*="fund"]',
                # 使用量相关
                '[class*="usage"]',
                '[class*="used"]',
                '[class*="consume"]',
                '[class*="spend"]',
            ]

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

            # 尝试通过JavaScript获取更多信息
            try:
                js_data = await self.page.evaluate('''
                    () => {
                        const texts = [];
                        // 获取所有包含数字的文本节点
                        const walker = document.createTreeWalker(
                            document.body,
                            NodeFilter.SHOW_TEXT,
                            {
                                acceptNode: (node) => {
                                    return /\\d/.test(node.textContent) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
                                }
                            }
                        );

                        let node;
                        while (node = walker.nextNode()) {
                            const text = node.textContent.trim();
                            if (text.length > 0 && (text.includes('$') || text.includes('余额') || text.includes('Balance'))) {
                                texts.push(text);
                            }
                        }
                        return texts.slice(0, 20); // 限制返回数量
                    }
                ''')

                usage_info['raw_data']['js_extracted_texts'] = js_data

                # 从JS提取的文本中再次查找金额
                for text in js_data:
                    for pattern in money_patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            try:
                                amount = float(match)
                                if 0 <= amount <= 1000 and amount not in found_amounts:
                                    found_amounts.append(amount)
                                    if amount > usage_info['current_balance']:
                                        usage_info['current_balance'] = amount
                            except ValueError:
                                continue

            except Exception as e:
                logger.debug(f"[{self.account['name']}] JS提取失败: {e}")

            return usage_info

        except Exception as e:
            logger.error(f"[{self.account['name']}] 提取使用量信息失败: {e}")
            return {'extraction_time': datetime.now().isoformat(), 'error': str(e)}

    async def login(self) -> bool:
        """执行登录操作"""
        try:
            logger.info(f"[{self.account['name']}] 开始访问: {CONFIG['URL']}")

            # 导航到登录页面
            response = await self.page.goto(
                CONFIG['URL'],
                wait_until='networkidle',
                timeout=60000
            )

            if not response:
                logger.error(f"[{self.account['name']}] 页面加载失败")
                return False

            logger.info(f"[{self.account['name']}] 页面响应状态: {response.status}")

            # 等待页面稳定
            await asyncio.sleep(2)

            # 处理弹窗和遮罩
            await self.handle_popups_and_overlays()

            # 如果启用监控，先提取登录前的信息
            if self.usage_monitor:
                login_before_info = await self.extract_usage_info()
                self.usage_data['before_login'] = login_before_info

            # 尝试多种用户名输入框定位器
            username_selectors = [
                'input[type="text"][name*="user" i]',
                'input[type="text"][name*="email" i]',
                'input[type="text"][placeholder*="用户" i]',
                'input[type="text"][placeholder*="账号" i]',
                'input[type="text"][placeholder*="Email" i]',
                '#username',
                '#email',
                'input.semi-input[type="text"]'
            ]

            username_input = None
            for selector in username_selectors:
                try:
                    username_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if username_input:
                        logger.info(f"[{self.account['name']}] 找到用户名输入框: {selector}")
                        break
                except:
                    continue

            if not username_input:
                logger.error(f"[{self.account['name']}] 未找到用户名输入框")
                return False

            # 输入用户名
            await username_input.click(force=True)
            await username_input.fill('')  # 清空
            await username_input.type(self.account['username'], delay=100)
            logger.info(f"[{self.account['name']}] 已输入用户名")

            # 尝试多种密码输入框定位器
            password_selectors = [
                'input[type="password"]',
                'input[name*="pass" i][type="password"]',
                'input[placeholder*="密码" i]',
                '#password',
                'input.semi-input[type="password"]'
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if password_input:
                        logger.info(f"[{self.account['name']}] 找到密码输入框: {selector}")
                        break
                except:
                    continue

            if not password_input:
                logger.error(f"[{self.account['name']}] 未找到密码输入框")
                return False

            # 输入密码
            await password_input.click(force=True)
            await password_input.fill('')  # 清空
            await password_input.type(self.account['password'], delay=100)
            logger.info(f"[{self.account['name']}] 已输入密码")

            # 尝试多种登录按钮定位器
            login_selectors = [
                'button[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
                'button:has-text("登 录")',
                'button.semi-button-primary',
                'input[type="submit"]'
            ]

            login_button = None
            for selector in login_selectors:
                try:
                    login_button = await self.page.wait_for_selector(selector, timeout=3000)
                    if login_button:
                        logger.info(f"[{self.account['name']}] 找到登录按钮: {selector}")
                        break
                except:
                    continue

            if not login_button:
                logger.error(f"[{self.account['name']}] 未找到登录按钮")
                return False

            # 点击登录按钮
            await login_button.click(force=True)
            logger.info(f"[{self.account['name']}] 已点击登录按钮")

            # 等待登录完成（通过 URL 变化或特定元素出现）
            try:
                await self.page.wait_for_function(
                    'window.location.href.includes("console")',
                    timeout=30000
                )
                logger.info(f"[{self.account['name']}] 成功跳转到控制台页面")
            except:
                logger.warning(f"[{self.account['name']}] 等待跳转超时，尝试继续...")

            # 额外等待页面加载
            await asyncio.sleep(CONFIG['WAIT_AFTER_LOGIN'] / 1000)

            # 再次处理可能的弹窗
            await self.handle_popups_and_overlays()

            # 如果启用监控，提取登录后的信息
            if self.usage_monitor:
                login_after_info = await self.extract_usage_info()
                self.usage_data['after_login'] = login_after_info

                # 记录登录后余额
                current_balance = login_after_info.get('current_balance', 0)
                if current_balance > 0:
                    logger.money(f"[{self.account['name']}] 💰 登录后余额: ${current_balance:.2f}")

                    # 验证刷新是否成功（基于登录后余额）
                    success, message = self.usage_monitor.verify_refresh_success(
                        self.account['name'], current_balance
                    )

                    if success:
                        logger.success(f"[{self.account['name']}] {message}")
                    else:
                        logger.warning_colored(f"[{self.account['name']}] {message}")

            return True

        except Exception as e:
            logger.error(f"[{self.account['name']}] 登录失败: {e}")
            if CONFIG['SCREENSHOT_ON_ERROR']:
                await self.take_screenshot('login_error')
            return False

    async def click_refresh_button(self) -> bool:
        """点击刷新按钮 - JavaScript 定位优先策略"""

        # 记录刷新前的余额
        if self.usage_monitor:
            before_refresh_info = await self.extract_usage_info()
            self.usage_data['before_refresh'] = before_refresh_info

            before_balance = before_refresh_info.get('current_balance', 0)
            if before_balance > 0:
                logger.money(f"[{self.account['name']}] 💰 刷新前余额: ${before_balance:.2f}")

        # 定义多个定位策略（JavaScript 优先）
        refresh_strategies = [
            # 策略1: JavaScript 定位（V18.0 证明最可靠）
            {
                'selector': None,
                'name': 'JavaScript定位',
                'js_code': '''
                    () => {
                        // 查找所有包含刷新图标的按钮
                        const buttons = Array.from(document.querySelectorAll('button'));
                        for (const btn of buttons) {
                            const icons = btn.querySelectorAll('[class*="refresh"], [class*="reload"]');
                            if (icons.length > 0) {
                                return btn;
                            }
                        }
                        // 备用：查找右上角的最后一个按钮
                        const headerButtons = document.querySelectorAll('header button, [class*="header"] button');
                        if (headerButtons.length > 0) {
                            return headerButtons[headerButtons.length - 1];
                        }
                        return null;
                    }
                '''
            },
            # 策略2: 使用 filter 和 has
            {
                'selector': 'button:has(.semi-icon-refresh)',
                'name': 'CSS :has()定位'
            },
            # 策略3: 基于 aria-label
            {
                'selector': 'button[aria-label*="refresh" i], button[aria-label*="刷新" i]',
                'name': 'aria-label定位'
            },
            # 策略4: 基于类名组合
            {
                'selector': 'button:has(span.semi-icon-refresh)',
                'name': '精确类名定位'
            },
            # 策略5: 使用 XPath（改进版）
            {
                'selector': '//button[.//span[contains(@class, "semi-icon-refresh")]]',
                'name': 'XPath定位'
            },
        ]

        refresh_success = False

        for attempt in range(CONFIG['REFRESH_RETRY_COUNT']):
            logger.info(f"[{self.account['name']}] 尝试点击刷新按钮 - 第 {attempt + 1} 次")

            for strategy in refresh_strategies:
                try:
                    logger.debug(f"[{self.account['name']}] 使用策略: {strategy['name']}")

                    if strategy.get('js_code'):
                        # JavaScript 定位策略
                        refresh_button = await self.page.evaluate_handle(strategy['js_code'])
                        if refresh_button:
                            await self.page.evaluate('(btn) => btn.scrollIntoView({block: "center"})', refresh_button)
                            await asyncio.sleep(0.5)

                            # 尝试多种点击方式
                            try:
                                await self.page.evaluate('(btn) => btn.click()', refresh_button)
                            except:
                                await refresh_button.click(force=True)

                            logger.success(f"[{self.account['name']}] ✅ 成功通过 {strategy['name']} 点击刷新按钮！")
                            refresh_success = True
                            break
                    else:
                        # 普通选择器策略（快速超时，因为JS策略更可靠）
                        refresh_button = await self.page.wait_for_selector(
                            strategy['selector'],
                            state='visible',
                            timeout=3000  # 减少到3秒
                        )

                        if refresh_button:
                            # 滚动到元素
                            await refresh_button.scroll_into_view_if_needed()
                            await asyncio.sleep(0.5)

                            # 检查元素是否可交互
                            is_enabled = await refresh_button.is_enabled()
                            is_visible = await refresh_button.is_visible()

                            logger.debug(f"[{self.account['name']}] 按钮状态 - 可见: {is_visible}, 可用: {is_enabled}")

                            # 尝试多种点击方式
                            click_methods = [
                                lambda: refresh_button.click(),
                                lambda: refresh_button.click(force=True),
                                lambda: refresh_button.dispatch_event('click'),
                                lambda: self.page.evaluate('(el) => el.click()', refresh_button)
                            ]

                            for click_method in click_methods:
                                try:
                                    await click_method()
                                    logger.success(f"[{self.account['name']}] ✅ 成功通过 {strategy['name']} 点击刷新按钮！")

                                    # 验证点击效果
                                    await asyncio.sleep(1)
                                    refresh_success = True
                                    break
                                except Exception as e:
                                    logger.debug(f"[{self.account['name']}] 点击方法失败: {e}")
                                    continue

                    if refresh_success:
                        break

                except PlaywrightTimeout:
                    logger.debug(f"[{self.account['name']}] {strategy['name']} 超时")
                    continue
                except Exception as e:
                    logger.debug(f"[{self.account['name']}] {strategy['name']} 失败: {e}")
                    continue

            if refresh_success:
                break

            # 如果所有策略都失败，等待后重试
            if attempt < CONFIG['REFRESH_RETRY_COUNT'] - 1:
                logger.info(f"[{self.account['name']}] 等待 2 秒后重试...")
                await asyncio.sleep(2)

                # 再次处理可能的遮罩
                await self.handle_popups_and_overlays()

        if not refresh_success:
            logger.error(f"[{self.account['name']}] 所有刷新按钮点击尝试均失败")
            return False

        # 等待刷新操作完成
        await asyncio.sleep(3)

        # 记录刷新后的余额
        if self.usage_monitor:
            after_refresh_info = await self.extract_usage_info()
            self.usage_data['after_refresh'] = after_refresh_info

            after_balance = after_refresh_info.get('current_balance', 0)
            if after_balance > 0:
                logger.money(f"[{self.account['name']}] 💰 刷新后余额: ${after_balance:.2f}")

                # 计算刷新获得的金额
                before_balance = self.usage_data.get('before_refresh', {}).get('current_balance', 0)
                if before_balance > 0:
                    refresh_amount = after_balance - before_balance
                    if refresh_amount > 0:
                        logger.success(f"[{self.account['name']}] 🎉 本次刷新获得: ${refresh_amount:.2f}")
                    else:
                        logger.warning_colored(f"[{self.account['name']}] ⚠️  刷新前后余额无变化")

        return True

    async def take_screenshot(self, name: str) -> None:
        """截图保存"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # 添加账号名称到文件名
            safe_account_name = self.account['name'].replace(' ', '_')
            filename = f"screenshot_{safe_account_name}_{name}_{timestamp}.png"
            await self.page.screenshot(path=filename, full_page=True)
            logger.info(f"[{self.account['name']}] 截图已保存: {filename}")
        except Exception as e:
            logger.error(f"[{self.account['name']}] 截图失败: {e}")

    async def cleanup(self) -> None:
        """清理浏览器资源"""
        try:
            if self.browser:
                await self.browser.close()
                logger.info(f"[{self.account['name']}] 浏览器已关闭")

            if self.playwright_instance:
                await self.playwright_instance.stop()
                logger.info(f"[{self.account['name']}] Playwright 实例已停止")
        except Exception as e:
            logger.error(f"[{self.account['name']}] 清理资源时出错: {e}")

    async def run(self) -> bool:
        """主运行流程"""
        try:
            logger.account_info(f"{'='*60}")
            logger.account_info(f"开始处理账号: {self.account['name']} ({self.account['username']})")
            logger.account_info(f"{'='*60}")

            # 初始化浏览器
            await self.init_browser()

            # 执行登录
            if not await self.login():
                logger.error(f"[{self.account['name']}] 登录失败，跳过该账号")
                return False

            logger.info(f"[{self.account['name']}] 登录成功，准备点击刷新按钮")

            # 等待页面完全加载
            try:
                await self.page.wait_for_load_state('networkidle', timeout=10000)
            except:
                logger.warning(f"[{self.account['name']}] 等待页面加载超时，继续执行")

            # 点击刷新按钮
            if await self.click_refresh_button():
                logger.success(f"[{self.account['name']}] ✅ 刷新操作成功完成！")

                # 等待刷新效果
                await asyncio.sleep(3)

                # 如果启用监控，记录最终数据
                if self.usage_monitor:
                    final_balance = self.usage_data.get('after_refresh', {}).get('current_balance', 0)
                    if final_balance > 0:
                        # 记录到历史数据
                        self.usage_monitor.record_usage(self.account['name'], {
                            'current_balance': final_balance,
                            'balance_after_refresh': final_balance,
                            'usage_data': self.usage_data,
                            'refresh_success': True
                        })

                # 保存成功截图
                await self.take_screenshot('success')
                return True
            else:
                logger.error(f"[{self.account['name']}] ❌ 刷新操作失败")

                # 记录失败数据
                if self.usage_monitor:
                    current_balance = self.usage_data.get('after_login', {}).get('current_balance', 0)
                    self.usage_monitor.record_usage(self.account['name'], {
                        'current_balance': current_balance,
                        'usage_data': self.usage_data,
                        'refresh_success': False
                    })

                await self.take_screenshot('refresh_failed')
                return False

        except Exception as e:
            logger.error(f"[{self.account['name']}] 执行过程中出现异常: {e}")
            await self.take_screenshot('error')
            return False
        finally:
            # 清理资源
            await self.cleanup()

async def generate_report(results: List[Dict]) -> None:
    """生成详细报告"""
    if not CONFIG['ENABLE_MONITORING']:
        return

    monitor = UsageMonitor()

    logger.info("=" * 80)
    logger.money("💰 账号余额和使用量报告")
    logger.info("=" * 80)

    total_balance = 0
    total_refreshed = 0

    for result in results:
        account_name = result['account']

        # 获取今日数据
        history = monitor.load_history()
        today_data = history.get(account_name, {}).get(monitor.today, {})

        if today_data:
            balance = today_data.get('current_balance', 0)
            refresh_success = today_data.get('refresh_success', False)

            status = "✅ 成功" if refresh_success else "❌ 失败"
            logger.money(f"{account_name}: ${balance:.2f} - 刷新{status}")

            total_balance += balance
            if refresh_success:
                total_refreshed += 1
        else:
            logger.money(f"{account_name}: 无数据记录")

    logger.info("=" * 80)
    logger.money(f"💰 总余额: ${total_balance:.2f}")
    logger.success(f"✅ 成功刷新: {total_refreshed}/{len(results)} 个账号")

    # 生成趋势分析
    logger.info("\n📈 7日余额趋势:")
    for i in range(7, 0, -1):
        date = (datetime.now() - timedelta(days=i-1)).strftime('%Y-%m-%d')
        date_total = 0
        date_accounts = 0

        history = monitor.load_history()
        for account_name in [r['account'] for r in results]:
            if account_name in history and date in history[account_name]:
                date_total += history[account_name][date].get('current_balance', 0)
                date_accounts += 1

        if date_accounts > 0:
            logger.info(f"  {date}: ${date_total:.2f} ({date_accounts}个账号)")

async def main():
    """主函数 - 处理所有账号"""
    logger.info("=" * 80)
    logger.info(f"AnyRouter 自动刷新脚本 V20.0 - 增强监控版 启动")
    logger.info(f"共 {len(ACCOUNT_LIST)} 个账号，监控功能: {'启用' if CONFIG['ENABLE_MONITORING'] else '禁用'}")
    logger.info("=" * 80)

    results = []

    for i, account in enumerate(ACCOUNT_LIST):
        refresher = AnyRouterRefresher(account)
        success = await refresher.run()
        results.append({
            'account': account['name'],
            'username': account['username'],
            'success': success
        })

        # 如果不是最后一个账号，等待一段时间再处理下一个
        if i < len(ACCOUNT_LIST) - 1:
            logger.info(f"等待 {CONFIG['ACCOUNT_DELAY']} 秒后处理下一个账号...")
            await asyncio.sleep(CONFIG['ACCOUNT_DELAY'])

    # 生成详细报告
    await generate_report(results)

    # 输出总结
    logger.info("=" * 80)
    logger.info("任务执行完成 - 结果汇总:")
    logger.info("=" * 80)

    success_count = 0
    for result in results:
        status = "✅ 成功" if result['success'] else "❌ 失败"
        logger.info(f"{result['account']} ({result['username']}): {status}")
        if result['success']:
            success_count += 1

    logger.info("=" * 80)
    logger.info(f"总计: {success_count}/{len(ACCOUNT_LIST)} 个账号刷新成功")
    logger.info("=" * 80)

    # 如果所有账号都成功，返回0；否则返回1
    if success_count == len(ACCOUNT_LIST):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())