@echo off
:: cleanup_and_deploy.bat - Clean up space and deploy
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo Emergency Space Cleanup and Deployment
echo Current usage: 90%% - Need to free up space
echo ===============================================

echo.
echo [1] Connecting...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo 'Connected'"

echo.
echo [2] Emergency cleanup - freeing space...
echo Cleaning package cache...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo apt clean && ^
sudo apt autoremove -y && ^
sudo journalctl --vacuum-time=7d && ^
sudo find /tmp -type f -atime +7 -delete 2>/dev/null || true && ^
sudo find /var/log -name '*.log' -size +50M -delete 2>/dev/null || true && ^
sudo find /var/cache -type f -delete 2>/dev/null || true"

echo.
echo [3] Checking space after cleanup...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h / | tail -1"

echo.
echo [4] Installing minimal Python setup...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo apt update -qq && ^
sudo apt install -y python3 python3-pip --no-install-recommends"

echo.
echo [5] Installing ultra-minimal Playwright...
echo This will take a few minutes...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"pip3 install playwright --break-system-packages --no-cache-dir && ^
python3 -m playwright install chromium --with-deps && ^
rm -rf ~/.cache/pip 2>/dev/null || true && ^
sudo apt autoremove -y && ^
sudo apt clean"

if !errorlevel! neq 0 (
    echo.
    echo ===============================================
    echo INSTALLATION FAILED - INSUFFICIENT SPACE
    echo ===============================================
    echo You have two options:
    echo.
    echo Option A: Expand EBS volume to 20GB+
    echo 1. Go to AWS Console -^> EC2 -^> Volumes
    echo 2. Select your volume
    echo 3. Actions -^> Modify Volume -^> Increase to 20GB
    echo 4. SSH to server and run: sudo resize2fs /dev/root
    echo.
    echo Option B: Use simplified script without browser
    echo ===============================================
    pause
    exit /b 1
)

echo.
echo [6] Uploading scripts...
scp -i "%KEY_PATH%" refresh_with_monitoring.py %USER%@%EC2_IP%:~/
scp -i "%KEY_PATH%" usage_checker.py %USER%@%EC2_IP%:~/

echo.
echo [7] Setting up cron jobs...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo mkdir -p /var/log && ^
sudo touch /var/log/anyrouter_refresh.log && ^
sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log && ^
(crontab -l 2>/dev/null | grep -v anyrouter || true) > /tmp/c && ^
echo '0 0 * * * cd && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/c && ^
echo '0 12 * * * cd && python3 usage_checker.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/c && ^
crontab /tmp/c && rm /tmp/c"

echo.
echo Final space check...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h /"

echo.
echo ===============================================
echo SUCCESS! Minimal deployment completed
echo ===============================================
echo Space saved by cleanup and minimal install
echo.
echo Schedule:
echo - Daily 08:00 Beijing: Auto refresh
echo - Daily 20:00 Beijing: Balance check
echo.
echo Test command:
echo ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo python3 refresh_with_monitoring.py
echo ===============================================
pause