@echo off
:: expand_30gb_simple.bat - Simple 30GB expansion guide (ASCII only)

cls
echo ============================================================
echo AWS EBS Volume Expansion to 30GB - FREE
echo ============================================================

echo.
echo STEP 1: Login to AWS Console
echo ----------------------------
echo Open: https://console.aws.amazon.com/ec2/
echo Login with your AWS account

echo.
echo STEP 2: Find Your Volume
echo ------------------------
echo 1. Click "Volumes" in left sidebar
echo 2. Find volume attached to your EC2 (54.252.140.109)
echo 3. Current size should show about 8GB

echo.
echo STEP 3: Expand Volume
echo ---------------------
echo 1. Select your volume (click checkbox)
echo 2. Click "Actions" then "Modify Volume"
echo 3. Change Size from 8 to 30
echo 4. Click "Modify" twice to confirm

echo.
echo STEP 4: Wait for Completion
echo ---------------------------
echo Status will change: modifying - optimizing - in-use
echo Wait about 10 minutes

echo.
echo STEP 5: Connect to Server
echo -------------------------
echo ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109

echo.
echo STEP 6: Run These Commands on Server
echo ------------------------------------
echo sudo growpart /dev/nvme0n1 1
echo sudo resize2fs /dev/nvme0n1p1
echo df -h

echo.
echo Expected Result:
echo /dev/root        30G  6.0G   23G  21%% /

echo.
echo After expansion, run: deploy_minimal_aws.bat
echo.

set /p ready="Ready to start? Press Enter when you have completed AWS Console steps..."

echo.
echo Creating server commands file...

echo #!/bin/bash > expand_commands.sh
echo echo "Expanding filesystem to 30GB..." >> expand_commands.sh
echo echo "Before expansion:" >> expand_commands.sh
echo df -h >> expand_commands.sh
echo echo "" >> expand_commands.sh
echo echo "Step 1: Expanding partition..." >> expand_commands.sh
echo sudo growpart /dev/nvme0n1 1 >> expand_commands.sh
echo echo "Step 2: Expanding filesystem..." >> expand_commands.sh
echo sudo resize2fs /dev/nvme0n1p1 >> expand_commands.sh
echo echo "After expansion:" >> expand_commands.sh
echo df -h >> expand_commands.sh
echo echo "SUCCESS! 30GB expansion completed." >> expand_commands.sh

echo.
echo Created: expand_commands.sh
echo.
echo To use after AWS Console expansion:
echo 1. scp -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" expand_commands.sh ubuntu@54.252.140.109:~/
echo 2. ssh -i "C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem" ubuntu@54.252.140.109
echo 3. chmod +x expand_commands.sh
echo 4. ./expand_commands.sh

echo.
echo COST: FREE (within AWS Free Tier 30GB limit)
echo.
pause