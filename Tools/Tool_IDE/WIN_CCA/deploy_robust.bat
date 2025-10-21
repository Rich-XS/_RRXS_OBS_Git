@echo off
:: deploy_robust.bat - Robust deployment with better error handling
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo AnyRouter Robust Deployment Tool
echo Target: %EC2_IP%
echo ===============================================

:: Check files first
echo.
echo [1/8] Checking files...
if not exist "refresh_with_monitoring.py" (
    echo ERROR: refresh_with_monitoring.py missing
    pause & exit /b 1
)
echo OK: Files ready

:: Test basic connectivity
echo.
echo [2/8] Testing network...
powershell -Command "Test-NetConnection -ComputerName %EC2_IP% -Port 22 -InformationLevel Quiet" >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Cannot reach server on port 22
    echo Please check:
    echo - Is EC2 instance running?
    echo - Security group allows SSH?
    echo - Correct IP address?
    pause & exit /b 1
)
echo OK: Port 22 reachable

:: Test SSH key
echo.
echo [3/8] Testing SSH key...
ssh -i "%KEY_PATH%" -o ConnectTimeout=15 -o StrictHostKeyChecking=no %USER%@%EC2_IP% "echo test" >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: SSH authentication failed
    echo Trying to fix key permissions...
    powershell -Command "icacls '%KEY_PATH%' /inheritance:r /grant:r '%USERNAME%:(R)'" >nul 2>&1

    echo Retrying SSH...
    ssh -i "%KEY_PATH%" -o ConnectTimeout=15 -o StrictHostKeyChecking=no %USER%@%EC2_IP% "echo test" >nul 2>&1
    if !errorlevel! neq 0 (
        echo ERROR: SSH still failing
        echo Please check key file and server access
        pause & exit /b 1
    )
)
echo OK: SSH working

:: Upload files
echo.
echo [4/8] Uploading files...
scp -i "%KEY_PATH%" -o StrictHostKeyChecking=no refresh_with_monitoring.py %USER%@%EC2_IP%:~/
if !errorlevel! neq 0 (
    echo ERROR: File upload failed
    pause & exit /b 1
)
scp -i "%KEY_PATH%" -o StrictHostKeyChecking=no usage_checker.py %USER%@%EC2_IP%:~/
echo OK: Files uploaded

:: Check Python
echo.
echo [5/8] Checking Python environment...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "python3 --version && pip3 --version" >nul 2>&1
if !errorlevel! neq 0 (
    echo Installing Python...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "sudo apt update && sudo apt install -y python3 python3-pip"
)
echo OK: Python ready

:: Install playwright
echo.
echo [6/8] Installing Playwright...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "python3 -c 'import playwright' 2>/dev/null" >nul 2>&1
if !errorlevel! neq 0 (
    echo Installing Playwright (this may take a few minutes)...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "pip3 install playwright --break-system-packages && python3 -m playwright install chromium && sudo python3 -m playwright install-deps"
    if !errorlevel! neq 0 (
        echo ERROR: Playwright installation failed
        pause & exit /b 1
    )
)
echo OK: Playwright ready

:: Setup logs
echo.
echo [7/8] Setting up logging...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "sudo mkdir -p /var/log && sudo touch /var/log/anyrouter_refresh.log && sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log"

:: Setup cron
echo.
echo [8/8] Setting up schedule...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"(crontab -l 2>/dev/null | grep -v anyrouter || true) > /tmp/cron.tmp && ^
echo '0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/cron.tmp && ^
echo '0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/anyrouter_refresh.log 2>&1' >> /tmp/cron.tmp && ^
crontab /tmp/cron.tmp && rm /tmp/cron.tmp"

:: Test
echo.
set /p test="Quick test? (y/N): "
if /i "%test%"=="y" (
    echo Testing script (30 second timeout)...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "timeout 30 python3 refresh_with_monitoring.py || echo 'Test completed'"
)

echo.
echo ===============================================
echo SUCCESS! Deployment completed
echo ===============================================
echo Daily schedule:
echo - 08:00 Beijing: Auto refresh
echo - 20:00 Beijing: Balance check
echo.
echo Manual commands:
echo SSH: ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo Run: python3 refresh_with_monitoring.py
echo Logs: tail -f /var/log/anyrouter_refresh.log
echo ===============================================
pause