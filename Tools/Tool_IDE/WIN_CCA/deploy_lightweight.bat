@echo off
:: deploy_lightweight.bat - Lightweight deployment for limited disk space
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo AnyRouter Lightweight Deployment
echo For servers with limited disk space
echo ===============================================

echo.
echo [1/6] Testing connection...
ssh -i "%KEY_PATH%" -o ConnectTimeout=15 %USER%@%EC2_IP% "echo 'Connected'"
if !errorlevel! neq 0 (
    echo ERROR: Connection failed
    pause & exit /b 1
)
echo OK: Connected

echo.
echo [2/6] Checking available space...
for /f %%i in ('ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df / | tail -1 | awk '{print $5}' | sed 's/%%//'"') do set USAGE=%%i
echo Current disk usage: %USAGE%%%

if %USAGE% GTR 85 (
    echo WARNING: Disk usage is high (%USAGE%^^)
    echo Proceeding with minimal installation...
    set MINIMAL=1
) else (
    echo OK: Sufficient space available
    set MINIMAL=0
)

echo.
echo [3/6] Uploading files...
scp -i "%KEY_PATH%" -o StrictHostKeyChecking=no refresh_with_monitoring.py %USER%@%EC2_IP%:~/
scp -i "%KEY_PATH%" -o StrictHostKeyChecking=no usage_checker.py %USER%@%EC2_IP%:~/
echo OK: Files uploaded

echo.
echo [4/6] Installing Python basics...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "sudo apt update -qq && sudo apt install -y python3 python3-pip"

echo.
echo [5/6] Installing Playwright...
if %MINIMAL%==1 (
    echo Installing minimal Playwright...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
    "pip3 install playwright --break-system-packages --no-cache-dir && ^
    python3 -m playwright install chromium --with-deps && ^
    echo 'Cleaning cache...' && ^
    rm -rf ~/.cache/pip/* 2>/dev/null || true && ^
    sudo apt autoremove -y && ^
    sudo apt autoclean"
) else (
    echo Installing full Playwright...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
    "pip3 install playwright --break-system-packages && ^
    python3 -m playwright install chromium && ^
    sudo python3 -m playwright install-deps"
)

if !errorlevel! neq 0 (
    echo ERROR: Playwright installation failed
    echo This is likely due to insufficient disk space
    echo.
    echo Suggested solutions:
    echo 1. Increase EBS volume size to 50GB+
    echo 2. Use Docker approach instead
    echo 3. Clean up existing files
    pause & exit /b 1
)

echo.
echo [6/6] Setting up schedule...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo mkdir -p /var/log && ^
sudo touch /var/log/anyrouter_refresh.log && ^
sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log && ^
(crontab -l 2>/dev/null | grep -v anyrouter || true) > /tmp/cron.new && ^
echo '0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/cron.new && ^
echo '0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/cron.new && ^
crontab /tmp/cron.new && rm /tmp/cron.new"

echo.
echo Final disk check...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h /"

echo.
echo ===============================================
echo Deployment completed!
echo ===============================================
echo Schedule:
echo - Daily 08:00 Beijing: Auto refresh + monitor
echo - Daily 20:00 Beijing: Balance check
echo.
echo Commands:
echo SSH: ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo Test: python3 refresh_with_monitoring.py
echo Logs: tail -f /var/log/anyrouter_refresh.log
echo ===============================================

set /p test="Test run now? (y/N): "
if /i "%test%"=="y" (
    echo Testing (30 second limit)...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "timeout 30 python3 refresh_with_monitoring.py || echo 'Test timeout - this is normal'"
)

pause