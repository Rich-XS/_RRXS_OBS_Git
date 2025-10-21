@echo off
:: deploy_to_ec2_english_only.bat - Pure English deployment script
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo AnyRouter Enhanced Monitoring Deployment
echo Target: %EC2_IP%
echo ===============================================

:: 1. Check files
echo.
echo [1/7] Checking local files...
if not exist "refresh_with_monitoring.py" (
    echo ERROR: refresh_with_monitoring.py not found
    pause & exit /b 1
)
if not exist "usage_checker.py" (
    echo ERROR: usage_checker.py not found
    pause & exit /b 1
)
echo OK: Files found

:: 2. Test connection
echo.
echo [2/7] Testing SSH connection...
ssh -i "%KEY_PATH%" -o ConnectTimeout=10 %USER%@%EC2_IP% "echo OK" >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: SSH connection failed
    echo Check: Key path, IP, network
    pause & exit /b 1
)
echo OK: SSH working

:: 3. Check server
echo.
echo [3/7] Checking server...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo Server ready && python3 --version 2>/dev/null || echo Python needed"

:: 4. Upload files
echo.
echo [4/7] Uploading files...
scp -i "%KEY_PATH%" refresh_with_monitoring.py %USER%@%EC2_IP%:~/
scp -i "%KEY_PATH%" usage_checker.py %USER%@%EC2_IP%:~/
echo OK: Files uploaded

:: 5. Install dependencies
echo.
echo [5/7] Installing dependencies...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"sudo apt update -qq && ^
sudo apt install -y python3 python3-pip && ^
pip3 install playwright --break-system-packages && ^
python3 -m playwright install chromium && ^
sudo python3 -m playwright install-deps && ^
sudo mkdir -p /var/log && ^
sudo touch /var/log/anyrouter_refresh.log && ^
sudo touch /var/log/usage_check.log && ^
sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log && ^
sudo chown ubuntu:ubuntu /var/log/usage_check.log && ^
echo Dependencies installed"

:: 6. Setup cron
echo.
echo [6/7] Setting up scheduled tasks...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"(crontab -l 2>/dev/null | grep -v anyrouter || true) > /tmp/mycron && ^
echo '0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/mycron && ^
echo '0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/usage_check.log 2>&1' >> /tmp/mycron && ^
echo '0 2 * * 0 find /var/log -name \"*anyrouter*\" -mtime +30 -delete 2>/dev/null' >> /tmp/mycron && ^
crontab /tmp/mycron && ^
rm /tmp/mycron && ^
echo Cron jobs configured"

:: 7. Test (optional)
echo.
set /p test="[7/7] Test run now? (y/N): "
if /i "%test%"=="y" (
    echo Testing... Please wait 3 minutes...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
    "timeout 180 python3 refresh_with_monitoring.py || echo Test completed && ^
    ls -la usage_history.json 2>/dev/null && echo History file created || echo No history yet && ^
    echo Recent logs: && tail -10 /var/log/anyrouter_refresh.log 2>/dev/null || echo No logs yet"
)

:: Summary
echo.
echo ===============================================
echo DEPLOYMENT COMPLETE!
echo ===============================================
echo Server: %EC2_IP%
echo.
echo Schedule:
echo - Daily 08:00 Beijing: Auto refresh + monitor
echo - Daily 20:00 Beijing: Balance check
echo.
echo SSH: ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo.
echo View logs:
echo   tail -f /var/log/anyrouter_refresh.log
echo   tail -f /var/log/usage_check.log
echo.
echo Manual run:
echo   python3 refresh_with_monitoring.py
echo   python3 usage_checker.py
echo.
echo Data files:
echo   cat usage_history.json
echo.
echo System will run automatically!
echo ===============================================
pause