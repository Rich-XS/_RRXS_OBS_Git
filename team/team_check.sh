#!/bin/bash

# 团队协作目录检查脚本

TEAM_DIR="/path/to/team"
DOER_DIR="$TEAM_DIR/doer"
VIBER_DIR="$TEAM_DIR/viber"

echo "===== 团队协作目录检查 ====="
echo "检查时间：$(date)"
echo ""

echo "1. Doer 目录文件："
ls -l "$DOER_DIR"
echo ""

echo "2. Viber 目录文件："
ls -l "$VIBER_DIR"
echo ""

echo "3. 最近修改文件："
find "$TEAM_DIR" -type f -mtime -7 | xargs ls -l
echo ""

echo "4. 未读文件："
for file in $(find "$TEAM_DIR" -type f); do
    echo "- $file"
done