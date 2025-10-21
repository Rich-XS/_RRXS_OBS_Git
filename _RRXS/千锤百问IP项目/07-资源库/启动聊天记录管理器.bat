@echo off
chcp 65001
title RRXS 聊天记录自动保存系统

echo.
echo ========================================
echo    RRXS 聊天记录自动保存系统
echo ========================================
echo.

cd /d "d:\OneDrive_RRXS\OneDrive\_RRXS_OBS\_RRXS\千锤百问IP项目\07-资源库"

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 📦 检查依赖包...
pip list | findstr selenium >nul
if errorlevel 1 (
    echo 🔧 正在安装必要的依赖包...
    pip install selenium schedule requests
)

pip list | findstr schedule >nul
if errorlevel 1 (
    echo 🔧 正在安装 schedule...
    pip install schedule
)

echo.
echo ✅ 依赖检查完成
echo.
echo 🚀 启动聊天记录管理器...
echo.

python chat_history_manager.py

echo.
echo 程序已结束，按任意键退出...
pause >nul