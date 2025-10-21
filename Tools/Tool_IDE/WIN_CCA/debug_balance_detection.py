#!/usr/bin/env python3
"""
余额检测调试工具 - 明日使用
用途：分析AnyRouter页面结构，找出余额显示问题
"""

import asyncio
from playwright.async_api import async_playwright
import re
import json
from datetime import datetime

async def debug_balance_detection():
    """调试余额检测问题"""

    account = {
        'username': '123463452',
        'password': '123463452',
        'name': 'rrxsUK'
    }

    async with async_playwright() as p:
        # 启用可视化调试
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器
            slow_mo=1000     # 减慢操作速度
        )

        page = await browser.new_page()

        print("🔍 开始调试余额检测...")

        try:
            # 访问登录页面
            await page.goto("https://anyrouter.top/console")
            await asyncio.sleep(3)

            # 登录
            print("📝 正在登录...")
            username_input = await page.wait_for_selector('input[type="text"]', timeout=10000)
            await username_input.fill(account['username'])

            password_input = await page.wait_for_selector('input[type="password"]')
            await password_input.fill(account['password'])

            login_button = await page.wait_for_selector('button[type="submit"]')
            await login_button.click()

            await asyncio.sleep(5)

            print("🔍 分析页面结构...")

            # 1. 保存完整页面内容
            page_content = await page.content()
            with open('anyrouter_page_debug.html', 'w', encoding='utf-8') as f:
                f.write(page_content)
            print("💾 页面内容已保存到 anyrouter_page_debug.html")

            # 2. 查找所有包含数字的文本
            all_texts = await page.evaluate('''
                () => {
                    const texts = [];
                    const walker = document.createTreeWalker(
                        document.body,
                        NodeFilter.SHOW_TEXT
                    );

                    let node;
                    while (node = walker.nextNode()) {
                        const text = node.textContent.trim();
                        if (/\d/.test(text) && text.length > 0) {
                            texts.push({
                                text: text,
                                parent: node.parentElement ? node.parentElement.tagName : 'unknown',
                                className: node.parentElement ? node.parentElement.className : '',
                                id: node.parentElement ? node.parentElement.id : ''
                            });
                        }
                    }
                    return texts;
                }
            ''')

            print(f"📊 找到 {len(all_texts)} 个包含数字的文本元素:")
            for i, text_info in enumerate(all_texts[:20]):  # 显示前20个
                print(f"  {i+1}. '{text_info['text']}' in <{text_info['parent']}> class='{text_info['className']}'")

            # 3. 测试现有正则表达式
            money_patterns = [
                r'\$\s*(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*USD',
                r'余额[：:]\s*\$?(\d+\.?\d*)',
                r'Balance[：:]\s*\$?(\d+\.?\d*)',
            ]

            found_amounts = []
            for pattern in money_patterns:
                matches = re.findall(pattern, page_content, re.IGNORECASE)
                if matches:
                    print(f"💰 模式 '{pattern}' 找到: {matches}")
                    for match in matches:
                        try:
                            amount = float(match)
                            if 0 <= amount <= 1000:
                                found_amounts.append(amount)
                        except ValueError:
                            continue

            print(f"💵 检测到的金额: {found_amounts}")

            # 4. 查找所有可能的余额元素
            balance_elements = await page.query_selector_all('[class*="balance"], [class*="credit"], [class*="amount"], [class*="money"]')
            print(f"🎯 找到 {len(balance_elements)} 个可能的余额元素")

            for i, elem in enumerate(balance_elements[:10]):
                text = await elem.text_content()
                tag = await elem.evaluate('el => el.tagName')
                class_name = await elem.get_attribute('class')
                print(f"  {i+1}. <{tag}> class='{class_name}': '{text}'")

            # 5. 截图保存
            await page.screenshot(path='anyrouter_debug_screenshot.png', full_page=True)
            print("📸 调试截图已保存到 anyrouter_debug_screenshot.png")

            # 6. 保存调试报告
            debug_report = {
                'timestamp': datetime.now().isoformat(),
                'found_amounts': found_amounts,
                'text_elements_count': len(all_texts),
                'balance_elements_count': len(balance_elements),
                'sample_texts': all_texts[:10],
                'recommended_selectors': []
            }

            # 推荐新的选择器
            for text_info in all_texts:
                text = text_info['text']
                if any(char in text.lower() for char in ['$', '余额', 'balance', 'credit']):
                    if text_info['className']:
                        debug_report['recommended_selectors'].append(f".{text_info['className']}")

            with open('balance_debug_report.json', 'w', encoding='utf-8') as f:
                json.dump(debug_report, f, indent=2, ensure_ascii=False)

            print("📋 调试报告已保存到 balance_debug_report.json")

            input("🔍 调试完成，按回车键关闭浏览器...")

        except Exception as e:
            print(f"❌ 调试过程中出错: {e}")
            await page.screenshot(path='debug_error_screenshot.png')

        finally:
            await browser.close()

if __name__ == "__main__":
    print("🛠️ AnyRouter 余额检测调试工具")
    print("此工具将帮助分析页面结构并找出余额检测问题")
    print("=" * 50)

    asyncio.run(debug_balance_detection())