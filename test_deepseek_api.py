# 文件名: test_deepseek_api.py - 独立连通性测试

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()

# --- 从 .env 文件中读取配置 ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
# 按照我们修正后的设置，这里应该是 https://api.deepseek.com/v1
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL") 
# 按照我们修正后的设置，这里应该是 deepseek-content-embedding
# EMBEDDING_MODEL = "deepseek-content-embedding" 
EMBEDDING_MODEL = "deepseek-ai/deepseek-content-embedding" 

print(f"--- DeepSeek API 连通性测试 ---")
print(f"Base URL: {DEEPSEEK_BASE_URL}")
print(f"Model:    {EMBEDDING_MODEL}")
print(f"Key Found: {'✅' if DEEPSEEK_API_KEY else '❌'}")
print("-" * 35)

if not DEEPSEEK_API_KEY or not DEEPSEEK_BASE_URL:
    print("❌ 错误：环境变量读取失败，请检查 .env 文件。")
    exit()

try:
    # 1. 初始化 DeepSeek 客户端
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    test_text = "千锤百问，一起打造人生新境界。"
    
    # 2. 调用 Embedding API
    print(f"🚀 尝试对文本进行向量化: '{test_text}'")
    
    response = client.embeddings.create(
        input=test_text,
        model=EMBEDDING_MODEL
    )
    
    # 3. 结果校验
    embedding = response.data[0].embedding
    
    print("\n🎉 API 调用成功！")
    print(f"✅ 模型名称和 Base URL 配置正确。")
    print(f"✅ DeepSeek 向量维度: {len(embedding)}")
    print(f"✅ 向量前5位: {embedding[:5]}")
    
except Exception as e:
    # 打印详细错误，帮助排查
    print("\n❌ API 调用失败！")
    print(f"错误类型: {type(e).__name__}")
    print(f"详细信息: {e}")
    
    # 针对 404 错误给出具体建议
    if "Error code: 404" in str(e):
        print("\n💡 404 错误很可能意味着：")
        print("1. **模型名称错误：** 请确认您使用的是 'deepseek-content-embedding'。")
        print("2. **API Key 权限问题：** 您的 Key 可能未开通或不支持 DeepSeek 的 Embedding 服务。")
        print("3. **Base URL 错误：** 尝试将 .env 中的 BASE_URL 改为 'https://api.deepseek.com' (移除 /v1)。")
    elif "Authentication" in str(e):
        print("\n💡 身份验证失败 (401)，请检查 DEEPSEEK_API_KEY 是否正确或已过期。")