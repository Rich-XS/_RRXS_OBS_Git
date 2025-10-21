@echo off
:: deploy_minimal_aws.bat - Minimal AWS deployment (refresh only)
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo Minimal AWS Deployment - Refresh Only
echo Goal: Save space, ensure core function works
echo ===============================================

echo.
echo [1] Connecting and cleaning...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo apt clean && ^
sudo apt autoremove -y && ^
sudo journalctl --vacuum-time=3d && ^
sudo find /tmp -type f -delete 2>/dev/null || true && ^
sudo find /var/log -name '*.log' -size +10M -delete 2>/dev/null || true && ^
sudo find /var/cache -type f -delete 2>/dev/null || true && ^
echo 'Cleanup completed'"

echo.
echo [2] Space after cleanup:
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h / | tail -1"

echo.
echo [3] Installing minimal Python...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo apt update -qq && ^
sudo apt install -y python3 python3-pip --no-install-recommends"

echo.
echo [4] Creating minimal refresh script...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% 'cat > minimal_refresh.py << '\''EOF'\''
#!/usr/bin/env python3
"""
AnyRouter Minimal Refresh Script - AWS Server Version
Only does refresh, no monitoring to save space
"""
import asyncio
import logging
import sys
from datetime import datetime
from playwright.async_api import async_playwright
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

ACCOUNTS = [
    {"username": "123463452", "password": "123463452", "name": "rrxsUK"},
    {"username": "RichardX", "password": "Austin050824", "name": "RichardXieSong"},
    {"username": "5757344544", "password": "5757344544", "name": "rrxsJP"},
]

async def refresh_account(account):
    playwright_instance = None
    browser = None
    try:
        playwright_instance = await async_playwright().start()
        browser = await playwright_instance.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
        )

        page = await browser.new_page()
        page.set_default_timeout(30000)

        # Login
        await page.goto("https://anyrouter.top/console", timeout=60000)
        await asyncio.sleep(2)

        # Find username input
        username_input = None
        for selector in ["input[type=\"text\"]", "#username", "input.semi-input[type=\"text\"]"]:
            try:
                username_input = await page.wait_for_selector(selector, timeout=5000)
                if username_input: break
            except: continue

        if not username_input:
            logger.error(f"[{account[\"name\"]}] Username input not found")
            return False

        await username_input.fill(account["username"])

        # Find password input
        password_input = await page.wait_for_selector("input[type=\"password\"]", timeout=5000)
        await password_input.fill(account["password"])

        # Find login button
        login_button = None
        for selector in ["button[type=\"submit\"]", "button:has-text(\"登录\")", "button:has-text(\"Login\")\"]:
            try:
                login_button = await page.wait_for_selector(selector, timeout=3000)
                if login_button: break
            except: continue

        if login_button:
            await login_button.click()
            await asyncio.sleep(5)

        # Click refresh - use JavaScript method only (most reliable)
        refresh_success = False
        for attempt in range(3):
            try:
                refresh_button = await page.evaluate_handle("""
                    () => {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        for (const btn of buttons) {
                            const icons = btn.querySelectorAll("[class*=\"refresh\"], [class*=\"reload\"]");
                            if (icons.length > 0) return btn;
                        }
                        const headerButtons = document.querySelectorAll("header button, [class*=\"header\"] button");
                        if (headerButtons.length > 0) return headerButtons[headerButtons.length - 1];
                        return null;
                    }
                """)

                if refresh_button:
                    await page.evaluate("(btn) => btn.click()", refresh_button)
                    logger.info(f"[{account[\"name\"]}] ✅ Refresh clicked successfully!")
                    refresh_success = True
                    break

            except Exception as e:
                logger.debug(f"[{account[\"name\"]}] Attempt {attempt+1} failed: {e}")
                await asyncio.sleep(2)

        return refresh_success

    except Exception as e:
        logger.error(f"[{account[\"name\"]}] Error: {e}")
        return False
    finally:
        if browser: await browser.close()
        if playwright_instance: await playwright_instance.stop()
        # Clean up after each account
        os.system("rm -rf /tmp/.org.chromium.* 2>/dev/null || true")

async def main():
    logger.info("=" * 50)
    logger.info("AnyRouter Minimal Refresh - Starting")
    logger.info("=" * 50)

    results = []
    for account in ACCOUNTS:
        logger.info(f"Processing {account[\"name\"]}...")
        success = await refresh_account(account)
        results.append({"name": account["name"], "success": success})
        await asyncio.sleep(2)

    # Summary
    logger.info("=" * 50)
    success_count = sum(1 for r in results if r["success"])
    for result in results:
        status = "✅" if result["success"] else "❌"
        logger.info(f"{result[\"name\"]}: {status}")

    logger.info(f"Total: {success_count}/{len(results)} successful")
    logger.info("=" * 50)

    # Auto cleanup after run
    logger.info("Cleaning up temporary files...")
    os.system("rm -rf ~/.cache/ms-playwright/chromium*/chrome-linux/chrome_crashpad_handler* 2>/dev/null || true")
    os.system("find /tmp -name \"playwright*\" -delete 2>/dev/null || true")

    sys.exit(0 if success_count == len(results) else 1)

if __name__ == "__main__":
    asyncio.run(main())
EOF'

echo.
echo [5] Installing minimal Playwright...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"pip3 install playwright --break-system-packages --no-cache-dir && ^
python3 -m playwright install chromium --with-deps && ^
rm -rf ~/.cache/pip 2>/dev/null || true"

echo.
echo [6] Setting up auto-cleanup cron job...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"(crontab -l 2>/dev/null | grep -v anyrouter || true) > /tmp/c && ^
echo '# AnyRouter Minimal - Refresh only with cleanup' >> /tmp/c && ^
echo '0 0 * * * cd /home/ubuntu && python3 minimal_refresh.py >> /var/log/refresh.log 2>&1 && find /tmp -name \"*chromium*\" -delete 2>/dev/null && journalctl --vacuum-time=1d' >> /tmp/c && ^
crontab /tmp/c && rm /tmp/c"

echo.
echo [7] Final space check...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h /"

echo.
echo [8] Quick test...
set /p test="Test minimal refresh now? (y/N): "
if /i "%test%"=="y" (
    echo Testing (60 second limit)...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "timeout 60 python3 minimal_refresh.py"
)

echo.
echo ===============================================
echo AWS MINIMAL DEPLOYMENT COMPLETE!
echo ===============================================
echo AWS Server Role: Daily auto-refresh ONLY
echo - Every day 08:00 Beijing time
echo - Auto cleanup after each run
echo - Minimal disk usage
echo.
echo Next: Run local monitoring script on your PC
echo for balance checking and reporting
echo ===============================================
pause