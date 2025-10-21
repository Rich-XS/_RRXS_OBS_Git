# cloud_indexer.py 伪代码 - 在 VSCode 中运行一次性脚本

import os
from openai import OpenAI
from supabase import create_client, Client
from langchain.text_splitter import MarkdownTextSplitter

# 配置信息# 文件名: cloud_indexer.py - DeepSeek Embedding 实施方案

import os
import time
from openai import OpenAI # 仍然使用 OpenAI 库，但指向 DeepSeek API
from supabase import create_client, Client
from langchain.text_splitter import MarkdownTextSplitter
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()

# ----------------- 1. 配置信息 -----------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
# ⚠️ 关键：使用 DeepSeek 密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

# ⚠️ 关键：需要同步的核心目录（已根据您的路径推断修正）
TARGET_FOLDERS = [
    "_RRXS/千锤百问IP学长RRXS",  
    "_RRXS/千锤百问IP项目",       
    "_RRXS/_RRXS.XYZ网站"      
]
# 强制检查：表名使用 rrx_notes 规范
SUPABASE_TABLE_NAME = 'rrxs_notes' 
EMBEDDING_MODEL = "deepseek-ai/deepseek-content-embedding"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# ----------------- 2. 初始化客户端 -----------------
print("===============================================")
print("📢 正在启动 Obsidian Vault 云端索引同步...")

if not all([SUPABASE_URL, SUPABASE_KEY, DEEPSEEK_API_KEY, OBSIDIAN_VAULT_PATH]):
    print("❌ 错误：关键环境变量缺失，请检查 .env 文件。")
    exit()

try:
    # ⚠️ 初始化 DeepSeek 客户端：修改 base_url
    deepseek_client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ 客户端初始化成功：DeepSeek API & Supabase 连接就绪。")
except Exception as e:
    print(f"❌ 客户端初始化失败: {e}")
    exit()

# ----------------- 3. 初始化 Markdown 切块器 -----------------
markdown_splitter = MarkdownTextSplitter(
    chunk_size=1000,
    chunk_overlap=200, 
    length_function=len
)

def is_target_file(file_path):
    """检查文件是否位于目标同步目录内"""
    relative_path = os.path.relpath(file_path, OBSIDIAN_VAULT_PATH)
    
    # 检查相对路径是否以任一目标文件夹开头
    for folder in TARGET_FOLDERS:
        if relative_path.startswith(folder.replace('/', os.sep)):
            return True
    return False

def index_file(file_path):
    """处理单个 Markdown 文件：切块 -> 向量化 -> 插入 Supabase"""
    try:
        if not is_target_file(file_path):
            return # 跳过非目标文件
            
        print(f"\n--- 正在处理: {file_path} ---")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

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
                "metadata": {"path": file_path, "index": i}
            }).execute()

            print(f"  - 片段 {i+1}/{len(chunks)} 索引成功。")
            time.sleep(0.1) # 增加延迟，避免潜在的速率限制

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时发生错误: {e}")


# ----------------- 4. 遍历 Vault 并索引 -----------------
file_count = 0
for root, _, files in os.walk(OBSIDIAN_VAULT_PATH):
    for file in files:
        if file.endswith(".md"):
            index_file(os.path.join(root, file))
            file_count += 1

print("\n===============================================")
print(f"🎉 所有 Obsidian Vault 核心笔记已同步至 Supabase 云端知识库 ({SUPABASE_TABLE_NAME})。")
print(f"总计扫描并处理了 {file_count} 个 .md 文件。")
print("下一步：请在 Supabase 部署 Edge Function 作为 Agent 的检索接口。")
print("===============================================")w
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_KEY"
OBSIDIAN_VAULT_PATH = "/path/to/your/Obsidian/Vault"

# 1. 初始化客户端
openai_client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. 文档切块（使用 LangChain 保持专业性）
markdown_splitter = MarkdownTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def index_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 2.1 切块
    chunks = markdown_splitter.create_documents([content])

    for chunk in chunks:
        text = chunk.page_content
        
        # 2.2 生成 Embedding (CALL CLOUD API)
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002" 
        )
        embedding = response.data[0].embedding
        
        # 2.3 插入 Supabase
        # 注意：此处需处理 API 错误和速率限制
        data, count = supabase.table('rrxs_notes').insert({
            "content": text,
            "embedding": embedding,
            "source": file_path,
            "metadata": {"tags": "Ref-Prep"}
        }).execute()
        
        print(f"Indexed chunk from {file_path}")

# 3. 遍历 Vault 并索引（仅针对 .md 文件）
for root, _, files in os.walk(OBSIDIAN_VAULT_PATH):
    for file in files:
        if file.endswith(".md"):
            index_file(os.path.join(root, file))

print("Obsidian Vault 向量化索引完成，已同步至 Supabase 云端。")