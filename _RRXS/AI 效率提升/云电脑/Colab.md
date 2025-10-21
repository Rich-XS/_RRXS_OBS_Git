ollama部署 gpt-oss:20b
。硬件加速:16G显存，可以选择T4 GPU及以上
。个人主页:https://www,youtube.com/@a=yuan/featured作者:陶渊小明
【]#1.安装 Linux 包
!apt-get install pciutils lshw
【] #2.检查 INVIDA CUDA 编译器的版本
!nvcc --version
【] #3.检查当前是否启用了 NVIDIA GPU
!nvidia-smi
【]#4.下载并安装 ollama
!curl https://ollama.ai/install.sh | sh
#5、在后台启动 ollama
!nohup ollama serve &
【]#6.拉取 gpt-oss:20b 镜像(1.4G)!ollama pull gpt-oss:20b
# 7.简单测试
!ollama run gpt-oss:20b "用中文介绍gpt-oss LLM 模型"