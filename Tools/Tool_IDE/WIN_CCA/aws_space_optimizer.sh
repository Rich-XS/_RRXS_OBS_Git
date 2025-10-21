#!/bin/bash
# aws_space_optimizer.sh - AWS EC2 disk space optimization script
# Run this on AWS server to free up space

echo "=================================="
echo "AWS EC2 Disk Space Optimizer"
echo "=================================="

echo "Current disk usage:"
df -h /

echo ""
echo "[1] Cleaning package cache..."
sudo apt clean
sudo apt autoremove -y --purge

echo ""
echo "[2] Cleaning system logs..."
sudo journalctl --vacuum-time=3d
sudo find /var/log -name "*.log" -size +10M -delete 2>/dev/null || true
sudo find /var/log -name "*.log.*" -delete 2>/dev/null || true

echo ""
echo "[3] Cleaning temporary files..."
sudo find /tmp -type f -atime +1 -delete 2>/dev/null || true
sudo find /var/tmp -type f -atime +1 -delete 2>/dev/null || true

echo ""
echo "[4] Cleaning user cache..."
rm -rf ~/.cache/* 2>/dev/null || true
rm -rf ~/.npm 2>/dev/null || true
rm -rf ~/.pip 2>/dev/null || true

echo ""
echo "[5] Cleaning old kernels..."
sudo apt autoremove --purge -y

echo ""
echo "[6] Cleaning snap cache..."
sudo rm -rf /var/lib/snapd/cache/* 2>/dev/null || true

echo ""
echo "[7] Cleaning Docker (if installed)..."
if command -v docker &> /dev/null; then
    sudo docker system prune -af 2>/dev/null || true
fi

echo ""
echo "[8] Cleaning Playwright cache (keep only essentials)..."
if [ -d ~/.cache/ms-playwright ]; then
    # Keep only chromium, remove others
    find ~/.cache/ms-playwright -name "*firefox*" -exec rm -rf {} + 2>/dev/null || true
    find ~/.cache/ms-playwright -name "*webkit*" -exec rm -rf {} + 2>/dev/null || true

    # Clean chromium crash dumps
    find ~/.cache/ms-playwright -name "*crashpad*" -delete 2>/dev/null || true
    find ~/.cache/ms-playwright -name "*.dmp" -delete 2>/dev/null || true
fi

echo ""
echo "=================================="
echo "Optimization Complete!"
echo "=================================="
echo "Disk usage after cleanup:"
df -h /

echo ""
echo "Space freed up:"
echo "Before cleanup was shown above"
echo ""

# Save this as a daily cleanup cron job
echo ""
echo "To make this run daily, add to crontab:"
echo "0 2 * * * /home/ubuntu/aws_space_optimizer.sh >> /var/log/cleanup.log 2>&1"