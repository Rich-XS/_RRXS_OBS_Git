#!/usr/bin/env python3
"""
AnyRouter 每日额度自动刷新脚本 V19.0
新特性：
- 多账号支持
- JavaScript 定位优先策略
- 优化的资源管理
- 详细的账号级别日志
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Optional, Dict, List
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('anyrouter_refresh.log', encoding='utf-8')
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
    'REFRESH_RETRY_COUNT': 3,  # 刷新按钮重试次数（减少为3次，因为JS策略更可靠）
    'SCREENSHOT_ON_ERROR': True,
    'ACCOUNT_DELAY': 2,  # 账号之间的延迟（秒）
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

# 添加彩色日志方法
logger.success = ColoredLogger.success
logger.account_info = ColoredLogger.account_info

class AnyRouterRefresher:
    """AnyRouter 额度刷新自动化类"""

    def __init__(self, account: Dict[str, str]):
        self.account = account
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright_instance = None

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

            return True

        except Exception as e:
            logger.error(f"[{self.account['name']}] 登录失败: {e}")
            if CONFIG['SCREENSHOT_ON_ERROR']:
                await self.take_screenshot('login_error')
            return False

    async def click_refresh_button(self) -> bool:
        """点击刷新按钮 - JavaScript 定位优先策略"""

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
                            return True
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
                                    return True
                                except Exception as e:
                                    logger.debug(f"[{self.account['name']}] 点击方法失败: {e}")
                                    continue

                except PlaywrightTimeout:
                    logger.debug(f"[{self.account['name']}] {strategy['name']} 超时")
                    continue
                except Exception as e:
                    logger.debug(f"[{self.account['name']}] {strategy['name']} 失败: {e}")
                    continue

            # 如果所有策略都失败，等待后重试
            if attempt < CONFIG['REFRESH_RETRY_COUNT'] - 1:
                logger.info(f"[{self.account['name']}] 等待 2 秒后重试...")
                await asyncio.sleep(2)

                # 再次处理可能的遮罩
                await self.handle_popups_and_overlays()

        logger.error(f"[{self.account['name']}] 所有刷新按钮点击尝试均失败")
        return False

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

                # 保存成功截图
                await self.take_screenshot('success')
                return True
            else:
                logger.error(f"[{self.account['name']}] ❌ 刷新操作失败")
                await self.take_screenshot('refresh_failed')
                return False

        except Exception as e:
            logger.error(f"[{self.account['name']}] 执行过程中出现异常: {e}")
            await self.take_screenshot('error')
            return False
        finally:
            # 清理资源
            await self.cleanup()

async def main():
    """主函数 - 处理所有账号"""
    logger.info("=" * 80)
    logger.info(f"AnyRouter 自动刷新脚本 V19.0 启动 - 共 {len(ACCOUNT_LIST)} 个账号")
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
