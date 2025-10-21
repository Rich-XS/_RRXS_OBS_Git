# 文件名: cloud_indexer.py - 千锤百问 DeepSeek 索引器 (最终版)

import os
import time
from openai import OpenAI # 使用 OpenAI 库，通过 base_url 调用 DeepSeek API
from supabase import create_client, Client
from langchain.text_splitter import MarkdownTextSplitter
from dotenv import load_dotenv

# 加载 .env 文件中的配置，确保密钥和路径已设置
load_dotenv()

# --- 1. 配置信息 (从环境变量读取) ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# ⚠️ 关键修改 1：读取 Jina 配置
JINA_API_KEY = os.getenv("JINA_API_KEY") 
JINA_BASE_URL = os.getenv("JINA_BASE_URL")

# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

# 强制检查：表名使用 rrxs_notes 规范 (2025-10-02 强制检查)
SUPABASE_TABLE_NAME = 'rrxs_notes' 

# ⚠️ 关键修改 2：使用 Jina 的中文模型
EMBEDDING_MODEL = "jina-embeddings-v2-base-zh" 


# ⚠️ 关键修正：使用更短的模型名称，避免 API 路径解析错误
# EMBEDDING_MODEL = "deepseek-content-embedding" 
# DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL") 

# ⚠️ 核心目录列表 (已根据您的目录结构推断修正)
TARGET_FOLDERS = [
    "_RRXS/千锤百问IP学长RRXS",  
    "_RRXS/千锤百问IP项目",       
    "_RRXS/_RRXS.XYZ网站"      
]

# --- 2. 客户端初始化与错误检查 ---
print("===============================================")
print("📢 正在启动 Obsidian Vault 云端索引同步...")

if not all([SUPABASE_URL, SUPABASE_KEY, DEEPSEEK_API_KEY, OBSIDIAN_VAULT_PATH]):
    print("❌ 错误：关键环境变量缺失，请检查 .env 文件。")
    exit()

try:
    # 初始化 DeepSeek 客户端：使用修正后的 base_url 指向 DeepSeek
    deepseek_client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ 客户端初始化成功：DeepSeek API & Supabase 连接就绪。")
except Exception as e:
    print(f"❌ 客户端初始化失败: {e}")
    exit()

# --- 3. Markdown 文档切块器 ---
markdown_splitter = MarkdownTextSplitter(
    chunk_size=1000,
    chunk_overlap=200, 
    length_function=len
)

def is_target_file(file_path):
    """根据 TARGET_FOLDERS 检查文件是否需要索引"""
    relative_path = os.path.relpath(file_path, OBSIDIAN_VAULT_PATH)
    
    # 检查相对路径是否以任一目标文件夹开头 (os.sep 确保跨系统兼容)
    for folder in TARGET_FOLDERS:
        if relative_path.startswith(folder.replace('/', os.sep)):
            return True
    return False

def index_file(file_path):
    """处理单个 Markdown 文件：切块 -> 向量化 -> 插入 Supabase"""
    if not is_target_file(file_path):
        return # 跳过非目标文件
        
    print(f"\n--- 正在处理: {file_path} ---")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 切块
        chunks = markdown_splitter.create_documents([content])
        print(f"文件切分完成，共 {len(chunks)} 个片段。")

        for i, chunk in enumerate(chunks):
            text = chunk.page_content
            
            # 3.1 生成 Embedding (调用 DeepSeek API)
            response = deepseek_client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            )
            embedding = response.data[0].embedding
            
            # 3.2 插入 Supabase
            data, count = supabase.table(SUPABASE_TABLE_NAME).insert({
                "content": text,
                "embedding": embedding,
                "source": os.path.basename(file_path),
                # 存储完整路径和索引，方便后续溯源
                "metadata": {"full_path": file_path, "index": i} 
            }).execute()

            print(f"  - 片段 {i+1}/{len(chunks)} 索引成功。")
            time.sleep(0.1) # 增加延迟，避免 API 速率限制

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时发生严重错误: {e}")
        print("请检查 DeepSeek API 额度或 Supabase RLS 策略。")


# --- 4. 遍历 Vault 并索引 ---
file_count = 0
for root, _, files in os.walk(OBSIDIAN_VAULT_PATH):
    for file in files:
        if file.endswith(".md"):
            index_file(os.path.join(root, file))
            file_count += 1

print("\n===============================================")
print(f"🎉 索引扫描完成。总共扫描了 {file_count} 个 .md 文件。")
print(f"数据已同步至 Supabase 云端知识库 ({SUPABASE_TABLE_NAME})。")
print("===============================================")
print("下一步：请在 Supabase 部署 Edge Function 作为 Agent 的检索接口。")