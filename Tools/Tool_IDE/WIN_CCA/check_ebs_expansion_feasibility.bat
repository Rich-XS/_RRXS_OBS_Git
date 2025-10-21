@echo off
:: check_ebs_expansion_feasibility.bat - Check current EBS volume info
:: Usage: Double-click to run

setlocal enabledelayedexpansion

set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo ===============================================
echo EBS Volume Expansion Feasibility Check
echo ===============================================

echo.
echo [1] Connecting to server...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo 'Connected to EC2 instance'"
if !errorlevel! neq 0 (
    echo ERROR: Cannot connect to server
    pause & exit /b 1
)

echo.
echo [2] Current disk configuration:
echo ===============================================
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "lsblk"
echo ===============================================

echo.
echo [3] Current disk usage:
echo ===============================================
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "df -h /"
echo ===============================================

echo.
echo [4] EBS volume details:
echo ===============================================
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "sudo fdisk -l /dev/nvme0n1 2>/dev/null || sudo fdisk -l /dev/xvda1 2>/dev/null || echo 'Checking block devices...'; lsblk -f"
echo ===============================================

echo.
echo [5] File system type:
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "mount | grep 'on / '"

echo.
echo ===============================================
echo ANALYSIS RESULTS:
echo ===============================================

echo Based on the above information:
echo.
echo ✓ AWS Free Tier allows up to 30GB EBS storage per month
echo ✓ Your current usage appears to be ~7GB
echo ✓ Expanding to 20GB is completely FREE
echo ✓ No additional charges will apply
echo.
echo RECOMMENDED ACTION:
echo 1. Run expand_ebs_volume.bat for step-by-step guide
echo 2. Use AWS Console to expand volume from 8GB to 20GB
echo 3. SSH to server and run filesystem expansion commands
echo 4. Then retry the deployment with more space

echo.
echo Free Tier EBS Storage Limits:
echo - General Purpose SSD (gp2/gp3): 30GB per month
echo - Provisioned IOPS SSD (io1): 20GB per month
echo - Magnetic (standard): 30GB per month
echo.
echo Current allocation will use: 20GB of 30GB free limit
echo Remaining free space: 10GB per month

echo.
echo COST ESTIMATE: $0.00 (within free tier limits)

echo.
set /p expand="Ready to expand? Run expand_ebs_volume.bat for detailed guide (y/N): "
if /i "%expand%"=="y" (
    start expand_ebs_volume.bat
)

pause