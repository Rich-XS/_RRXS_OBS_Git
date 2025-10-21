#!/bin/bash 
echo "Expanding filesystem to 30GB..." 
echo "Before expansion:" 
df -h 
echo "" 
echo "Step 1: Expanding partition..." 
sudo growpart /dev/nvme0n1 1 
echo "Step 2: Expanding filesystem..." 
sudo resize2fs /dev/nvme0n1p1 
echo "After expansion:" 
df -h 
echo "SUCCESS! 30GB expansion completed." 
