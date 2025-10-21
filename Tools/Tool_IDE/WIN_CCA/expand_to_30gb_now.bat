@echo off
:: expand_to_30gb_now.bat - Immediate 30GB expansion guide
:: This maximizes your free tier allocation

echo ================================================================
echo AWS EBS EXPANSION TO 30GB - IMMEDIATE ACTION GUIDE
echo Using MAXIMUM free tier allocation (30GB = 100%% of free limit)
echo ================================================================

echo.
echo 🎯 TARGET: Expand from ~7GB to 30GB (FREE!)
echo 💰 COST: $0.00 (Maximum free tier usage)
echo ⏱️ TIME: 5-10 minutes total

echo.
echo ================================================================
echo STEP 1: AWS CONSOLE LOGIN
echo ================================================================
echo 1. Open: https://console.aws.amazon.com/ec2/
echo 2. Login with your AWS credentials
echo 3. Select your region (where your EC2 instance is located)

echo.
echo ================================================================
echo STEP 2: LOCATE YOUR EBS VOLUME
echo ================================================================
echo 1. Left sidebar: "Elastic Block Store" → "Volumes"
echo 2. Find volume with:
echo    - State: "in-use"
echo    - Attached to your EC2 instance (54.252.140.109)
echo    - Current size: ~8GB
echo 3. Note the Volume ID (starts with vol-...)

echo.
echo ================================================================
echo STEP 3: MODIFY VOLUME (CRITICAL STEP)
echo ================================================================
echo 1. ✅ SELECT your volume (click checkbox)
echo 2. ✅ Click "Actions" → "Modify Volume"
echo 3. ✅ Change "Size (GiB)" from 8 to: 30
echo 4. ✅ Keep "Volume Type": gp3 (or gp2)
echo 5. ✅ Click "Modify"
echo 6. ✅ Click "Modify" again to CONFIRM
echo.
echo ⚠️  IMPORTANT: You will see "Volume modification succeeded"

echo.
echo ================================================================
echo STEP 4: WAIT FOR COMPLETION
echo ================================================================
echo Status progression:
echo   modifying → optimizing → in-use
echo.
echo ⏳ Wait time: 5-15 minutes
echo 💡 Tip: Refresh the page to see status updates

echo.
echo ================================================================
echo STEP 5: EXPAND FILE SYSTEM ON SERVER
echo ================================================================
echo After volume shows "in-use", run these commands:

echo.
echo SSH Command:
echo ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109

echo.
echo Then execute these commands on server:
echo --------------------------------
echo # Check current setup
echo lsblk
echo df -h
echo.
echo # Expand partition
echo sudo growpart /dev/nvme0n1 1
echo.
echo # Expand file system
echo sudo resize2fs /dev/nvme0n1p1
echo.
echo # Verify success
echo df -h
echo --------------------------------

echo.
echo Expected result after expansion:
echo   Filesystem      Size  Used Avail Use%% Mounted on
echo   /dev/root        30G  6.0G   23G  21%% /

echo.
echo ================================================================
echo STEP 6: VERIFY AND TEST
echo ================================================================

set /p create_script="Create automated SSH expansion script? (y/N): "
if /i "%create_script%"=="y" (
    echo.
    echo Creating expansion script for server...

    echo #!/bin/bash > expand_30gb_filesystem.sh
    echo # AWS EBS 30GB Filesystem Expansion Script >> expand_30gb_filesystem.sh
    echo echo "=== AWS EBS 30GB Expansion ===" >> expand_30gb_filesystem.sh
    echo echo "Before expansion:" >> expand_30gb_filesystem.sh
    echo lsblk >> expand_30gb_filesystem.sh
    echo df -h >> expand_30gb_filesystem.sh
    echo echo "" >> expand_30gb_filesystem.sh
    echo echo "Expanding partition to 30GB..." >> expand_30gb_filesystem.sh
    echo sudo growpart /dev/nvme0n1 1 >> expand_30gb_filesystem.sh
    echo echo "" >> expand_30gb_filesystem.sh
    echo echo "Expanding filesystem..." >> expand_30gb_filesystem.sh
    echo sudo resize2fs /dev/nvme0n1p1 >> expand_30gb_filesystem.sh
    echo echo "" >> expand_30gb_filesystem.sh
    echo echo "After expansion:" >> expand_30gb_filesystem.sh
    echo lsblk >> expand_30gb_filesystem.sh
    echo df -h >> expand_30gb_filesystem.sh
    echo echo "" >> expand_30gb_filesystem.sh
    echo echo "✅ SUCCESS! 30GB expansion completed." >> expand_30gb_filesystem.sh
    echo echo "Available space for Playwright and automation." >> expand_30gb_filesystem.sh

    echo ✅ Created: expand_30gb_filesystem.sh
    echo.
    echo To use after EBS expansion:
    echo 1. scp -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" expand_30gb_filesystem.sh ubuntu@54.252.140.109:~/
    echo 2. ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109
    echo 3. chmod +x expand_30gb_filesystem.sh
    echo 4. ./expand_30gb_filesystem.sh
)

echo.
echo ================================================================
echo FINAL RESULT - WHAT YOU'LL GET:
echo ================================================================
echo ✅ Disk space: 30GB (maximum free tier)
echo ✅ Available: ~23GB free space
echo ✅ Usage: 21%% (from 90%%)
echo ✅ Playwright: Easy installation
echo ✅ Future proof: Room for growth
echo ✅ Cost: Still $0.00

echo.
echo After successful expansion, you can:
echo 1. Run: deploy_minimal_aws.bat (will succeed now)
echo 2. Run: cleanup_and_deploy.bat (with plenty of space)
echo 3. Install full monitoring version

echo.
echo ================================================================
echo 🚀 START NOW: Go to AWS Console and modify your volume!
echo ================================================================
pause