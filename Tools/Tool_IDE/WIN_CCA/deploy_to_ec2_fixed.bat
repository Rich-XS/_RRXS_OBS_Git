@echo off
:: deploy_to_ec2_fixed.bat - Fixed deployment script (English only)
:: Usage: Double-click to run or execute from command line

setlocal enabledelayedexpansion

:: Configuration variables
set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo Starting AnyRouter Enhanced Monitoring Script Deployment to EC2...
echo Target server: %EC2_IP%

:: 1. Check local files
echo.
echo [1/7] Checking local files...
if not exist "refresh_with_monitoring.py" (
    echo ERROR: File refresh_with_monitoring.py not found!
    echo Please run this script from the directory containing the script files
    pause
    exit /b 1
)

if not exist "usage_checker.py" (
    echo ERROR: File usage_checker.py not found!
    echo Please run this script from the directory containing the script files
    pause
    exit /b 1
)
echo SUCCESS: Local files check completed

:: 2. Test SSH connection
echo.
echo [2/7] Testing SSH connection...
ssh -i "%KEY_PATH%" -o ConnectTimeout=10 -o BatchMode=yes %USER%@%EC2_IP% "echo Connection successful" >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: SSH connection failed. Please check:
    echo   - Key file path: %KEY_PATH%
    echo   - Server IP: %EC2_IP%
    echo   - Network connection
    pause
    exit /b 1
)
echo SUCCESS: SSH connection is working

:: 3. Check server environment
echo.
echo [3/7] Checking server environment...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo 'Server Information:'; echo '  OS:' $(lsb_release -d | cut -f2); echo '  Python:' $(python3 --version 2>/dev/null || echo 'Not installed'); echo '  Docker:' $(docker --version 2>/dev/null || echo 'Not installed'); echo '  Disk Space:' $(df -h / | tail -1 | awk '{print $4}') 'available'"

:: 4. Upload script files
echo.
echo [4/7] Uploading script files...
scp -i "%KEY_PATH%" refresh_with_monitoring.py %USER%@%EC2_IP%:~/
if !errorlevel! neq 0 (
    echo ERROR: Failed to upload refresh_with_monitoring.py
    pause
    exit /b 1
)

scp -i "%KEY_PATH%" usage_checker.py %USER%@%EC2_IP%:~/
if !errorlevel! neq 0 (
    echo ERROR: Failed to upload usage_checker.py
    pause
    exit /b 1
)
echo SUCCESS: Files uploaded successfully

:: 5. Install dependencies
echo.
echo [5/7] Configuring server environment...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "set -e; echo 'Updating system packages...'; sudo apt update -qq; echo 'Installing Python dependencies...'; sudo apt install -y python3 python3-pip >/dev/null; if python3 -c 'import playwright' 2>/dev/null; then echo 'Playwright already installed'; else echo 'Installing Playwright...'; pip3 install playwright --break-system-packages; python3 -m playwright install chromium; sudo python3 -m playwright install-deps; fi; echo 'Creating log directories...'; sudo mkdir -p /var/log; sudo touch /var/log/anyrouter_refresh.log; sudo touch /var/log/usage_check.log; sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log; sudo chown ubuntu:ubuntu /var/log/usage_check.log; echo 'Server environment configured successfully'"

if !errorlevel! neq 0 (
    echo ERROR: Server environment configuration failed
    pause
    exit /b 1
)

:: 6. Configure cron jobs
echo.
echo [6/7] Configuring scheduled tasks...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "crontab -l > mycron 2>/dev/null || touch mycron; grep -v 'anyrouter\|usage_checker\|refresh_with_monitoring' mycron > mycron_new; echo '' >> mycron_new; echo '# AnyRouter Enhanced Monitoring Tasks' >> mycron_new; echo '# Daily refresh at UTC 00:00 (Beijing 08:00)' >> mycron_new; echo '0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> mycron_new; echo '' >> mycron_new; echo '# Daily balance check at UTC 12:00 (Beijing 20:00)' >> mycron_new; echo '0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/usage_check.log 2>&1' >> mycron_new; echo '' >> mycron_new; echo '# Weekly cleanup (keep 30 days)' >> mycron_new; echo '0 2 * * 0 find /var/log -name \"*anyrouter*\" -mtime +30 -delete 2>/dev/null' >> mycron_new; echo '0 2 * * 0 find /home/ubuntu -name \"screenshot_*\" -mtime +7 -delete 2>/dev/null' >> mycron_new; crontab mycron_new; rm mycron mycron_new; echo 'Scheduled tasks configured:'; crontab -l | grep -A5 -B1 'AnyRouter'"

if !errorlevel! neq 0 (
    echo ERROR: Scheduled tasks configuration failed
    pause
    exit /b 1
)

:: 7. Test run option
echo.
set /p test_run="[7/7] Do you want to test run the enhanced refresh script now? (y/n): "
if /i "!test_run!"=="y" (
    echo.
    echo Testing script execution on server (please wait 3-5 minutes)...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo 'Starting test run...'; timeout 300 python3 refresh_with_monitoring.py || echo 'Test run completed (may have timed out)'; echo 'Checking generated files...'; ls -la usage_history.json 2>/dev/null && echo 'History data file created' || echo 'History data file not yet created'; ls -la screenshot_* 2>/dev/null && echo 'Screenshot files generated' || echo 'No screenshot files generated'; echo 'Recent log output:'; tail -20 /var/log/anyrouter_refresh.log 2>/dev/null || echo 'Log file is empty'"
) else (
    echo Skipping test run
)

:: 8. Deployment summary
echo.
echo ========================================
echo DEPLOYMENT COMPLETED SUCCESSFULLY!
echo ========================================
echo Server Address: %EC2_IP%
echo Scheduled Tasks:
echo   - Daily 08:00 Beijing Time: Auto refresh + monitoring
echo   - Daily 20:00 Beijing Time: Balance check
echo.
echo SSH Connection Command:
echo ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo.
echo Log Viewing Commands:
echo   tail -f /var/log/anyrouter_refresh.log    # Refresh logs
echo   tail -f /var/log/usage_check.log         # Balance check logs
echo.
echo Manual Testing Commands:
echo   python3 refresh_with_monitoring.py       # Manual refresh
echo   python3 usage_checker.py                 # Manual balance check
echo.
echo Data Viewing Commands:
echo   cat usage_history.json                   # View history data
echo   python3 -m json.tool usage_history.json # Formatted view
echo.
echo The system will run automatically - no manual intervention needed!
echo.
echo ========================================
echo.
pause