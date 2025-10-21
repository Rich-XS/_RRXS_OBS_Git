@echo off
:: deploy_to_ec2.bat - Windows版本的自动部署脚本
:: 使用方法：双击运行或在命令行执行 deploy_to_ec2.bat

setlocal enabledelayedexpansion

:: 配置变量
set EC2_IP=54.252.140.109
set KEY_PATH=C:/Users/rrxs/.ssh/RRXSXYZ_EC2.pem
set USER=ubuntu

echo 🚀 开始部署 AnyRouter 增强监控脚本到 EC2...
echo 目标服务器: %EC2_IP%

:: 1. 检查本地文件
echo.
echo 📋 检查本地文件...
if not exist "refresh_with_monitoring.py" (
    echo ❌ 文件 refresh_with_monitoring.py 不存在！
    echo 请确保在包含脚本文件的目录下运行
    pause
    exit /b 1
)

if not exist "usage_checker.py" (
    echo ❌ 文件 usage_checker.py 不存在！
    echo 请确保在包含脚本文件的目录下运行
    pause
    exit /b 1
)
echo ✅ 本地文件检查完成

:: 2. 连接测试
echo.
echo 🔗 测试 SSH 连接...
ssh -i "%KEY_PATH%" -o ConnectTimeout=10 -o BatchMode=yes %USER%@%EC2_IP% "echo 连接成功" >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ SSH 连接失败，请检查：
    echo   - 密钥文件路径: %KEY_PATH%
    echo   - 服务器IP: %EC2_IP%
    echo   - 网络连接
    pause
    exit /b 1
)
echo ✅ SSH 连接正常

:: 3. 检查服务器环境
echo.
echo 🔍 检查服务器环境...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% "echo '🖥️  服务器信息:'; echo '  操作系统:' $(lsb_release -d | cut -f2); echo '  Python版本:' $(python3 --version 2>/dev/null || echo '未安装'); echo '  Docker状态:' $(docker --version 2>/dev/null || echo '未安装'); echo '  磁盘空间:' $(df -h / | tail -1 | awk '{print $4}') '可用'"

:: 4. 上传脚本文件
echo.
echo 📤 上传脚本文件...
scp -i "%KEY_PATH%" refresh_with_monitoring.py %USER%@%EC2_IP%:~/
if !errorlevel! neq 0 (
    echo ❌ 上传 refresh_with_monitoring.py 失败
    pause
    exit /b 1
)

scp -i "%KEY_PATH%" usage_checker.py %USER%@%EC2_IP%:~/
if !errorlevel! neq 0 (
    echo ❌ 上传 usage_checker.py 失败
    pause
    exit /b 1
)
echo ✅ 文件上传完成

:: 5. 安装依赖
echo.
echo 🔧 配置服务器环境...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"set -e; ^
echo '📦 更新系统包...'; ^
sudo apt update -qq; ^
echo '🐍 安装 Python 依赖...'; ^
sudo apt install -y python3 python3-pip >/dev/null; ^
if python3 -c 'import playwright' 2>/dev/null; then ^
    echo '✅ Playwright 已安装'; ^
else ^
    echo '🎭 安装 Playwright...'; ^
    pip3 install playwright --break-system-packages; ^
    python3 -m playwright install chromium; ^
    sudo python3 -m playwright install-deps; ^
fi; ^
echo '📁 创建日志目录...'; ^
sudo mkdir -p /var/log; ^
sudo touch /var/log/anyrouter_refresh.log; ^
sudo touch /var/log/usage_check.log; ^
sudo chown ubuntu:ubuntu /var/log/anyrouter_refresh.log; ^
sudo chown ubuntu:ubuntu /var/log/usage_check.log; ^
echo '✅ 服务器环境配置完成'"

if !errorlevel! neq 0 (
    echo ❌ 服务器环境配置失败
    pause
    exit /b 1
)

:: 6. 配置定时任务
echo.
echo ⏰ 配置定时任务...
ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
"crontab -l > mycron 2>/dev/null || touch mycron; ^
grep -v 'anyrouter\|usage_checker\|refresh_with_monitoring' mycron > mycron_new; ^
echo '' >> mycron_new; ^
echo '# AnyRouter 增强监控任务' >> mycron_new; ^
echo '# 每天 UTC 00:00 (北京时间 08:00) 运行增强版刷新' >> mycron_new; ^
echo '0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1' >> mycron_new; ^
echo '' >> mycron_new; ^
echo '# 每天 UTC 12:00 (北京时间 20:00) 运行余额检查' >> mycron_new; ^
echo '0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/usage_check.log 2>&1' >> mycron_new; ^
echo '' >> mycron_new; ^
echo '# 每周清理旧日志（保留30天）' >> mycron_new; ^
echo '0 2 * * 0 find /var/log -name \"*anyrouter*\" -mtime +30 -delete 2>/dev/null' >> mycron_new; ^
echo '0 2 * * 0 find /home/ubuntu -name \"screenshot_*\" -mtime +7 -delete 2>/dev/null' >> mycron_new; ^
crontab mycron_new; ^
rm mycron mycron_new; ^
echo '📅 定时任务配置完成:'; ^
crontab -l | grep -A5 -B1 'AnyRouter'"

if !errorlevel! neq 0 (
    echo ❌ 定时任务配置失败
    pause
    exit /b 1
)

:: 7. 询问是否测试
echo.
set /p test_run="🧪 是否要立即测试运行增强版刷新脚本？(y/n): "
if /i "!test_run!"=="y" (
    echo.
    echo 🔬 正在服务器上测试运行（请等待约3-5分钟）...
    ssh -i "%KEY_PATH%" %USER%@%EC2_IP% ^
    "echo '⏳ 开始测试运行...'; ^
    timeout 300 python3 refresh_with_monitoring.py || echo '测试运行完成（可能因为超时结束）'; ^
    echo '📊 检查生成的文件...'; ^
    ls -la usage_history.json 2>/dev/null && echo '✅ 历史数据文件已创建' || echo 'ℹ️  历史数据文件尚未创建'; ^
    ls -la screenshot_* 2>/dev/null && echo '✅ 截图文件已生成' || echo 'ℹ️  无截图文件生成'; ^
    echo '📝 查看最近的日志...'; ^
    tail -20 /var/log/anyrouter_refresh.log 2>/dev/null || echo '日志文件为空'"
) else (
    echo ⏭️  跳过测试运行
)

:: 8. 部署完成总结
echo.
echo ════════════════════════════════════════
echo 🎉 部署完成！
echo ════════════════════════════════════════
echo 📍 服务器地址: %EC2_IP%
echo 📅 定时任务:
echo   - 每天 08:00 (北京时间): 自动刷新 + 监控
echo   - 每天 20:00 (北京时间): 余额检查
echo.
echo 📋 SSH连接命令:
echo ssh -i "%KEY_PATH%" %USER%@%EC2_IP%
echo.
echo 🔍 日志查看命令:
echo   tail -f /var/log/anyrouter_refresh.log    # 刷新日志
echo   tail -f /var/log/usage_check.log         # 余额检查日志
echo.
echo 🧪 手动测试命令:
echo   python3 refresh_with_monitoring.py       # 手动刷新
echo   python3 usage_checker.py                 # 手动检查余额
echo.
echo 📈 数据查看命令:
echo   cat usage_history.json                   # 查看历史数据
echo   python3 -m json.tool usage_history.json # 格式化查看
echo.
echo ✅ 系统将自动运行，无需手动干预！
echo.
pause