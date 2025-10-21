@echo off
:: debug_connection.bat - Debug SSH connection issues
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo SSH Connection Diagnostic Tool
echo Target: %EC2_IP%
echo ===============================================

echo.
echo [Test 1] Checking key file...
if exist "%KEY_PATH%" (
    echo OK: Key file found at %KEY_PATH%
) else (
    echo ERROR: Key file not found at %KEY_PATH%
    pause & exit /b 1
)

echo.
echo [Test 2] Testing network connectivity...
ping -n 4 %EC2_IP%
if !errorlevel! neq 0 (
    echo WARNING: Ping failed - but this is normal for many EC2 instances
) else (
    echo OK: Server is reachable
)

echo.
echo [Test 3] Testing SSH port...
echo Testing port 22...
powershell -Command "Test-NetConnection -ComputerName %EC2_IP% -Port 22 -InformationLevel Quiet"
if !errorlevel! neq 0 (
    echo ERROR: Port 22 is not accessible
    echo This could be:
    echo - Security group blocking SSH
    echo - Instance not running
    echo - Wrong IP address
    pause & exit /b 1
) else (
    echo OK: Port 22 is open
)

echo.
echo [Test 4] Testing SSH with verbose output...
echo Attempting SSH connection with detailed output...
ssh -i "%KEY_PATH%" -v -o ConnectTimeout=30 -o StrictHostKeyChecking=no %USER%@%EC2_IP% "echo 'SSH connection successful'"

echo.
echo [Test 5] Alternative connection test...
echo Trying with different SSH options...
ssh -i "%KEY_PATH%" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null %USER%@%EC2_IP% "whoami && date"

echo.
echo ===============================================
echo If all tests pass, your SSH connection is working.
echo If tests fail, check:
echo 1. EC2 instance is running
echo 2. Security group allows SSH (port 22)
echo 3. Key file has correct permissions
echo 4. IP address is correct
echo ===============================================
pause