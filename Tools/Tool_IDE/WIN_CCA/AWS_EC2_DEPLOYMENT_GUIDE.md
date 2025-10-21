# AWS EC2 部署指导 - AnyRouter 刷新脚本

## 📋 部署前准备

### 需要的信息
1. **AWS 账号信息**（需要您提供）:
   - AWS Access Key ID
   - AWS Secret Access Key
   - 首选区域（推荐 us-east-1 或 ap-southeast-1）

2. **AnyRouter 账号信息**（已配置）:
   - rrxsUK: 123463452 / 123463452
   - RichardXieSong: RichardX / Austin050824
   - rrxsJP: 5757344544 / 5757344544

## 🚀 方案一：自动化部署脚本

### 1. EC2 实例创建和配置脚本

```bash
#!/bin/bash
# ec2_setup.sh - 自动创建和配置 EC2 实例

# 配置变量（请根据需要修改）
INSTANCE_TYPE="t3.micro"
AMI_ID="ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS
KEY_NAME="anyrouter-key"
SECURITY_GROUP="anyrouter-sg"
REGION="us-east-1"

echo "🚀 开始创建 EC2 实例..."

# 1. 创建密钥对
echo "📋 创建密钥对..."
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > ${KEY_NAME}.pem
chmod 400 ${KEY_NAME}.pem

# 2. 创建安全组
echo "🔒 创建安全组..."
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name $SECURITY_GROUP \
    --description "AnyRouter Refresher Security Group" \
    --query 'GroupId' --output text)

# 3. 添加安全组规则（SSH访问）
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# 4. 启动 EC2 实例
echo "🖥️ 启动 EC2 实例..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=AnyRouter-Refresher}]' \
    --query 'Instances[0].InstanceId' --output text)

echo "✅ EC2 实例已创建: $INSTANCE_ID"

# 5. 等待实例启动
echo "⏳ 等待实例启动..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# 6. 获取公网IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "🌐 实例公网IP: $PUBLIC_IP"
echo "🔑 SSH连接命令: ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP"

# 7. 保存实例信息
cat > instance_info.txt << EOF
Instance ID: $INSTANCE_ID
Public IP: $PUBLIC_IP
Key File: ${KEY_NAME}.pem
SSH Command: ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP
EOF

echo "✅ 实例信息已保存到 instance_info.txt"
```

### 2. 服务器环境配置脚本

```bash
#!/bin/bash
# server_setup.sh - 在 EC2 实例上安装必要软件

echo "🔧 开始配置服务器环境..."

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
echo "🐳 安装 Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# 安装 Python 和 pip
echo "🐍 安装 Python..."
sudo apt install -y python3 python3-pip

# 安装 Playwright 依赖
echo "🎭 安装 Playwright..."
pip3 install playwright
python3 -m playwright install-deps

# 创建工作目录
mkdir -p ~/anyrouter-refresher
cd ~/anyrouter-refresher

# 安装 crontab
sudo apt install -y cron
sudo systemctl enable cron
sudo systemctl start cron

echo "✅ 服务器环境配置完成！"
```

## 🛠️ 方案二：手动部署步骤

### Step 1: 创建 EC2 实例

1. **登录 AWS 控制台**
   - 进入 EC2 服务
   - 选择区域（推荐 us-east-1）

2. **启动实例**
   - 点击 "Launch Instance"
   - 选择 Ubuntu 22.04 LTS AMI
   - 实例类型：t3.micro（免费套餐）
   - 创建新的密钥对并下载 `.pem` 文件

3. **配置安全组**
   - 允许 SSH（端口 22）访问
   - 来源：0.0.0.0/0（或限制为您的 IP）

### Step 2: 连接到实例

```bash
# 修改密钥权限
chmod 400 your-key.pem

# SSH 连接
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### Step 3: 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 安装 Python 环境
sudo apt install -y python3 python3-pip
pip3 install playwright

# 重新登录以使 Docker 权限生效
exit
# 重新 SSH 连接

# 安装浏览器
python3 -m playwright install chromium
python3 -m playwright install-deps
```

### Step 4: 上传脚本文件

```bash
# 在本地执行（上传文件）
scp -i your-key.pem refresh_with_monitoring.py ubuntu@YOUR_EC2_IP:~/
scp -i your-key.pem usage_checker.py ubuntu@YOUR_EC2_IP:~/

# 或者在服务器上创建文件
nano refresh_with_monitoring.py  # 复制粘贴脚本内容
nano usage_checker.py           # 复制粘贴脚本内容
```

### Step 5: 创建 Docker 环境（可选）

```dockerfile
# Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install playwright

RUN python3 -m playwright install chromium
RUN python3 -m playwright install-deps

WORKDIR /app
COPY refresh_with_monitoring.py .
COPY usage_checker.py .

CMD ["python3", "refresh_with_monitoring.py"]
```

```bash
# 构建镜像
docker build -t anyrouter-refresher .

# 测试运行
docker run --rm anyrouter-refresher
```

### Step 6: 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下内容：
# 每天 UTC 00:00 (北京时间 08:00) 运行刷新任务
0 0 * * * cd /home/ubuntu && python3 refresh_with_monitoring.py >> /var/log/anyrouter_refresh.log 2>&1

# 每天 UTC 12:00 (北京时间 20:00) 运行余额检查
0 12 * * * cd /home/ubuntu && python3 usage_checker.py >> /var/log/usage_check.log 2>&1

# 每月 1 日清理日志
0 1 1 * * find /var/log -name "*anyrouter*" -mtime +30 -delete
```

## 🔧 配置和维护

### 日志查看命令

```bash
# 查看刷新日志
tail -f /var/log/anyrouter_refresh.log

# 查看余额检查日志
tail -f /var/log/usage_check.log

# 查看系统日志中的 cron 任务
sudo tail -f /var/log/syslog | grep CRON
```

### 手动测试命令

```bash
# 测试监控版刷新脚本
python3 refresh_with_monitoring.py

# 测试余额检查脚本
python3 usage_checker.py

# 查看历史数据
cat usage_history.json | python3 -m json.tool
```

### 监控和警报设置

```bash
# 创建监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash

# 检查今日是否成功刷新
TODAY=$(date +%Y-%m-%d)
if grep -q "总计: 3/3 个账号刷新成功" /var/log/anyrouter_refresh.log; then
    echo "[$TODAY] ✅ 所有账号刷新成功"
else
    echo "[$TODAY] ❌ 刷新可能存在问题"
    # 可以在这里添加邮件通知或其他警报
fi
EOF

chmod +x monitor.sh

# 添加到 crontab（每天检查一次）
echo "30 1 * * * /home/ubuntu/monitor.sh >> /var/log/monitor.log 2>&1" | crontab -
```

## 💡 费用优化建议

1. **实例类型**：
   - 免费套餐：t2.micro（1年免费）
   - 性能更好：t3.micro（约 $8.5/月）

2. **存储**：
   - 使用默认的 8GB EBS 卷
   - 定期清理日志和临时文件

3. **网络**：
   - 正常使用下流量费用很低
   - 如需节省可考虑使用弹性IP

## 🔒 安全建议

1. **密钥管理**：
   - 妥善保管 `.pem` 密钥文件
   - 定期轮换密钥

2. **网络安全**：
   - 限制 SSH 访问源 IP
   - 考虑使用 VPN 连接

3. **权限控制**：
   - 使用最小权限原则
   - 定期审查访问日志

## 📞 如需提供信息

为了帮您完成自动化部署，我需要以下信息：

1. **AWS 访问凭证**：
   - Access Key ID
   - Secret Access Key
   - 首选区域

2. **部署偏好**：
   - 是否使用 Docker
   - 是否需要监控告警
   - 首选的运行时间

3. **网络访问**：
   - 您的公网 IP（用于安全组配置）
   - 是否需要固定 IP

有了这些信息，我可以为您生成完整的自动化部署脚本！