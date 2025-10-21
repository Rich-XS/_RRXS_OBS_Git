@echo off
:: expand_ebs_volume.bat - Guide for expanding AWS EBS volume
:: This is FREE under AWS Free Tier (up to 30GB)

echo ============================================================
echo AWS EBS Volume Expansion Guide - FREE UNDER FREE TIER
echo Current: ~7GB, Target: 20GB (Well within 30GB free limit)
echo ============================================================

echo.
echo Step 1: Access AWS Console
echo ------------------------
echo 1. Go to: https://console.aws.amazon.com/ec2/
echo 2. Login to your AWS account
echo 3. Make sure you're in the correct region (where your EC2 is)

echo.
echo Step 2: Find Your Volume
echo ------------------------
echo 1. In left menu, click "Elastic Block Store" -> "Volumes"
echo 2. Find the volume attached to your EC2 instance
echo    - Look for "in-use" status
echo    - Instance ID should match your EC2
echo    - Current size should be ~8GB

echo.
echo Step 3: Modify Volume (FREE!)
echo -----------------------------
echo 1. Select your volume (checkbox)
echo 2. Click "Actions" -> "Modify Volume"
echo 3. Change Size from 8 to 20 (GB)
echo 4. Leave Volume Type as "gp2" or "gp3"
echo 5. Click "Modify"
echo 6. Click "Modify" again to confirm

echo.
echo Step 4: Wait for Completion
echo ---------------------------
echo Wait 5-10 minutes for "optimizing" status to complete
echo Status will change: modifying -> optimizing -> in-use

echo.
echo Step 5: Expand File System
echo --------------------------
echo SSH to your server and run:
echo.
echo ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109
echo.
echo Then run these commands:
echo   sudo growpart /dev/nvme0n1 1
echo   sudo resize2fs /dev/nvme0n1p1
echo   df -h
echo.

echo Step 6: Verify Success
echo --------------------
echo After expansion, you should see:
echo   Filesystem      Size  Used Avail Use%% Mounted on
echo   /dev/root        20G  6.0G   13G  32%% /
echo.

echo.
echo ============================================================
echo COST: $0.00 - This is FREE under AWS Free Tier!
echo Free Tier includes 30GB EBS storage per month for 12 months
echo You're only using 20GB, well within limits.
echo ============================================================

echo.
echo After expansion, you can run the AWS deployment script:
echo   deploy_minimal_aws.bat
echo   or
echo   cleanup_and_deploy.bat

echo.
set /p proceed="Do you want me to create a detailed SSH command file? (y/N): "
if /i "%proceed%"=="y" (
    echo Creating SSH expansion script...

    echo #!/bin/bash > expand_filesystem.sh
    echo # Run this on your EC2 instance after EBS expansion >> expand_filesystem.sh
    echo echo "Expanding filesystem to use new space..." >> expand_filesystem.sh
    echo echo "Current disk usage:" >> expand_filesystem.sh
    echo df -h >> expand_filesystem.sh
    echo echo "" >> expand_filesystem.sh
    echo echo "Expanding partition..." >> expand_filesystem.sh
    echo sudo growpart /dev/nvme0n1 1 >> expand_filesystem.sh
    echo echo "" >> expand_filesystem.sh
    echo echo "Expanding filesystem..." >> expand_filesystem.sh
    echo sudo resize2fs /dev/nvme0n1p1 >> expand_filesystem.sh
    echo echo "" >> expand_filesystem.sh
    echo echo "New disk usage:" >> expand_filesystem.sh
    echo df -h >> expand_filesystem.sh
    echo echo "" >> expand_filesystem.sh
    echo echo "Success! You now have more space for Playwright installation." >> expand_filesystem.sh

    echo.
    echo Created: expand_filesystem.sh
    echo.
    echo To use:
    echo 1. First expand volume in AWS Console (steps above)
    echo 2. Upload script: scp -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" expand_filesystem.sh ubuntu@54.252.140.109:~/
    echo 3. Run on server: chmod +x expand_filesystem.sh && ./expand_filesystem.sh
)

echo.
pause