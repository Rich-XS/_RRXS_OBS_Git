@echo off
:: check_server_space.bat - Check server disk space and status
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo Server Space and Status Check
echo ===============================================

echo.
echo [1] Connecting to server...
ssh -i "%KEY_PATH%" -o ConnectTimeout=20 %USER%@%EC2_IP% "echo 'Connected successfully'"
if !errorlevel! neq 0 (
    echo ERROR: Cannot connect to server
    pause & exit /b 1
)

echo.
echo [2] Checking disk space...
echo ===============================================
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h"
echo ===============================================

echo.
echo [3] Checking memory...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "free -h"

echo.
echo [4] Checking what's using space...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "du -sh /* 2>/dev/null | sort -hr | head -10"

echo.
echo [5] Checking if Playwright is already installed...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "python3 -c 'import playwright; print(\"Playwright installed\")' 2>/dev/null || echo 'Playwright not installed'"

echo.
echo [6] Checking browser files...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "ls -la ~/.cache/ms-playwright/ 2>/dev/null | wc -l || echo 'No browser cache'"

echo.
echo [7] Available space details...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -i /"

echo.
echo ===============================================
echo Analysis complete.
echo If disk usage is over 90%, we need to clean up
echo or use a lighter installation approach.
echo ===============================================
pause