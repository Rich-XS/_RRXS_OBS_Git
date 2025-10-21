#!/usr/bin/env python3
"""
AnyRouter 账号余额定期检查脚本
用途：
- 本地定期检查各账号的使用量/余额
- 与前日比较，验证每日$25刷新是否成功
- 生成详细的使用量报告和趋势分析
- 可以作为独立脚本运行，不依赖刷新功能

使用方法：
python usage_checker.py
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
from playwright.async_api import async_playwright
import logging
import sys
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('usage_checker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ============ 配置区域 ============
# 账号配置 (与主脚本保持一致)
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

CONFIG = {
    'URL': 'https://anyrouter.top/console',
    'TIMEOUT': 30000,
    'DAILY_REFRESH_TARGET': 25,
    'DATA_FILE': 'usage_history.json',
    'CHECK_ONLY': True,  # 只检查，不执行刷新
}
# =================================

class ColoredLogger:
    """彩色日志工具类"""
    @staticmethod
    def success(msg):
        logger.info(f"\033[92m{msg}\033[0m")  # 绿色

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
logger.warning_colored = ColoredLogger.warning
logger.money = ColoredLogger.money
logger.header = ColoredLogger.header

class UsageAnalyzer:
    """使用量分析器"""

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

    def get_account_trend(self, account_name: str, days: int = 7) -> List[Dict]:
        """获取账号趋势数据"""
        history = self.load_history()
        account_history = history.get(account_name, {})

        trend_data = []
        for i in range(days, 0, -1):
            date = (datetime.now() - timedelta(days=i-1)).strftime('%Y-%m-%d')
            data = account_history.get(date, {})
            trend_data.append({
                'date': date,
                'balance': data.get('current_balance', 0),
                'refresh_success': data.get('refresh_success', False),
                'has_data': bool(data)
            })

        return trend_data

    def analyze_refresh_pattern(self, account_name: str) -> Dict:
        """分析刷新模式"""
        trend = self.get_account_trend(account_name, 30)  # 30天数据

        total_days = len([d for d in trend if d['has_data']])
        successful_refreshes = len([d for d in trend if d['refresh_success']])

        if total_days == 0:
            return {'success_rate': 0, 'avg_balance': 0, 'trend': 'unknown'}

        success_rate = (successful_refreshes / total_days) * 100
        avg_balance = sum([d['balance'] for d in trend if d['has_data']]) / total_days

        # 计算趋势
        recent_balances = [d['balance'] for d in trend[-7:] if d['has_data']]
        if len(recent_balances) >= 2:
            trend_direction = 'increasing' if recent_balances[-1] > recent_balances[0] else 'decreasing'
        else:
            trend_direction = 'stable'

        return {
            'success_rate': success_rate,
            'avg_balance': avg_balance,
            'trend': trend_direction,
            'total_days': total_days,
            'successful_refreshes': successful_refreshes
        }

class AccountChecker:
    """账号检查器"""

    def __init__(self, account: Dict[str, str]):
        self.account = account

    async def check_balance(self) -> Dict:
        """检查账号余额（无头模式）"""
        playwright_instance = None
        browser = None

        try:
            playwright_instance = await async_playwright().start()

            browser = await playwright_instance.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox'],
                timeout=60000
            )

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                ignore_https_errors=True
            )

            page = await context.new_page()
            page.set_default_timeout(CONFIG['TIMEOUT'])

            # 访问登录页面
            logger.info(f"[{self.account['name']}] 开始检查账号余额...")
            await page.goto(CONFIG['URL'], wait_until='networkidle', timeout=60000)

            # 登录流程（简化版）
            await self._login(page)

            # 等待页面加载
            await asyncio.sleep(3)

            # 提取余额信息
            usage_info = await self._extract_balance(page)

            logger.money(f"[{self.account['name']}] 💰 当前余额: ${usage_info.get('current_balance', 0):.2f}")

            return usage_info

        except Exception as e:
            logger.error(f"[{self.account['name']}] 检查失败: {e}")
            return {'error': str(e), 'current_balance': 0}

        finally:
            if browser:
                await browser.close()
            if playwright_instance:
                await playwright_instance.stop()

    async def _login(self, page) -> bool:
        """执行登录（简化版）"""
        try:
            # 查找用户名输入框
            username_selectors = ['input[type="text"]', '#username', '#email']
            username_input = None

            for selector in username_selectors:
                try:
                    username_input = await page.wait_for_selector(selector, timeout=5000)
                    if username_input:
                        break
                except:
                    continue

            if not username_input:
                raise Exception("未找到用户名输入框")

            # 输入用户名
            await username_input.fill(self.account['username'])

            # 查找密码输入框
            password_input = await page.wait_for_selector('input[type="password"]', timeout=5000)
            await password_input.fill(self.account['password'])

            # 查找登录按钮
            login_selectors = ['button[type="submit"]', 'button:has-text("登录")', 'button:has-text("Login")']
            login_button = None

            for selector in login_selectors:
                try:
                    login_button = await page.wait_for_selector(selector, timeout=3000)
                    if login_button:
                        break
                except:
                    continue

            if login_button:
                await login_button.click()
                await asyncio.sleep(3)

            return True

        except Exception as e:
            logger.error(f"[{self.account['name']}] 登录失败: {e}")
            return False

    async def _extract_balance(self, page) -> Dict:
        """提取余额信息（简化版）"""
        try:
            page_content = await page.content()

            # 查找金额的正则表达式
            money_patterns = [
                r'\$\s*(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*USD',
                r'余额[：:]\s*\$?(\d+\.?\d*)',
                r'Balance[：:]\s*\$?(\d+\.?\d*)',
            ]

            found_amounts = []
            for pattern in money_patterns:
                matches = re.findall(pattern, page_content, re.IGNORECASE)
                for match in matches:
                    try:
                        amount = float(match)
                        if 0 <= amount <= 1000:  # 合理范围
                            found_amounts.append(amount)
                    except ValueError:
                        continue

            current_balance = max(found_amounts) if found_amounts else 0

            return {
                'current_balance': current_balance,
                'extraction_time': datetime.now().isoformat(),
                'found_amounts': found_amounts
            }

        except Exception as e:
            logger.error(f"提取余额信息失败: {e}")
            return {'current_balance': 0, 'error': str(e)}

def save_check_result(account_name: str, balance_data: Dict):
    """保存检查结果"""
    analyzer = UsageAnalyzer()
    history = analyzer.load_history()

    if account_name not in history:
        history[account_name] = {}

    today = datetime.now().strftime('%Y-%m-%d')
    history[account_name][today] = {
        **balance_data,
        'check_timestamp': datetime.now().isoformat(),
        'check_only': True  # 标记为只检查模式
    }

    try:
        with open(CONFIG['DATA_FILE'], 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"保存数据失败: {e}")

async def check_single_account(account: Dict) -> Dict:
    """检查单个账号"""
    checker = AccountChecker(account)
    result = await checker.check_balance()

    # 保存结果
    save_check_result(account['name'], result)

    return {
        'account': account['name'],
        'username': account['username'],
        'balance': result.get('current_balance', 0),
        'success': 'error' not in result
    }

def generate_usage_report(results: List[Dict]):
    """生成使用量报告"""
    analyzer = UsageAnalyzer()

    logger.header("=" * 80)
    logger.header("📊 AnyRouter 账号余额检查报告")
    logger.header(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.header("=" * 80)

    total_balance = 0
    successful_checks = 0

    # 当前余额报告
    logger.money("\n💰 当前余额:")
    for result in results:
        account_name = result['account']
        balance = result['balance']
        status = "✅" if result['success'] else "❌"

        logger.money(f"  {account_name}: ${balance:.2f} {status}")
        total_balance += balance
        if result['success']:
            successful_checks += 1

    logger.money(f"\n💰 总余额: ${total_balance:.2f}")
    logger.info(f"✅ 成功检查: {successful_checks}/{len(results)} 个账号")

    # 昨日对比
    logger.header("\n📈 与昨日对比:")
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for result in results:
        account_name = result['account']
        current_balance = result['balance']

        # 获取昨日数据
        history = analyzer.load_history()
        yesterday_data = history.get(account_name, {}).get(yesterday, {})
        yesterday_balance = yesterday_data.get('current_balance', 0)

        if yesterday_balance > 0:
            diff = current_balance - yesterday_balance
            expected_diff = CONFIG['DAILY_REFRESH_TARGET']

            if abs(diff - expected_diff) <= 1.0:  # 允许1美元误差
                status = f"✅ (+${diff:.2f})"
                logger.success(f"  {account_name}: ${yesterday_balance:.2f} → ${current_balance:.2f} {status}")
            else:
                status = f"⚠️  (+${diff:.2f}, 期望+${expected_diff})"
                logger.warning_colored(f"  {account_name}: ${yesterday_balance:.2f} → ${current_balance:.2f} {status}")
        else:
            logger.info(f"  {account_name}: 无昨日数据对比")

    # 7日趋势分析
    logger.header("\n📊 7日余额趋势:")
    for result in results:
        account_name = result['account']
        trend_data = analyzer.get_account_trend(account_name, 7)

        logger.info(f"\n{account_name}:")
        for data in trend_data:
            if data['has_data']:
                refresh_status = "✅" if data['refresh_success'] else "⚠️"
                logger.info(f"  {data['date']}: ${data['balance']:.2f} {refresh_status}")
            else:
                logger.info(f"  {data['date']}: 无数据")

    # 统计分析
    logger.header("\n🔍 账号统计分析:")
    for result in results:
        account_name = result['account']
        analysis = analyzer.analyze_refresh_pattern(account_name)

        logger.info(f"\n{account_name}:")
        logger.info(f"  刷新成功率: {analysis['success_rate']:.1f}%")
        logger.info(f"  平均余额: ${analysis['avg_balance']:.2f}")
        logger.info(f"  总记录天数: {analysis['total_days']} 天")
        logger.info(f"  成功刷新: {analysis['successful_refreshes']} 次")

    logger.header("=" * 80)

async def main():
    """主函数"""
    logger.header("🔍 AnyRouter 账号余额检查器启动")
    logger.info(f"共 {len(ACCOUNT_LIST)} 个账号")
    logger.info("=" * 50)

    results = []

    for account in ACCOUNT_LIST:
        result = await check_single_account(account)
        results.append(result)
        await asyncio.sleep(2)  # 账号间延迟

    # 生成报告
    generate_usage_report(results)

if __name__ == "__main__":
    asyncio.run(main())