# 文件名: cloud_indexer.py
# 目标: 将 Obsidian Vault 的 Markdown 文件分块、向量化后，同步至 Supabase 云端数据库 (rrxs_notes 表)

import os
import time
import re
import pathlib
import uuid
from openai import OpenAI
from supabase import create_client, Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()

# ====================================================================
# ------------------------- 1. 配置信息 ------------------------------
# ====================================================================

# --- Supabase 配置 ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Jina AI / Embedding 配置 (选择中文优化的免费方案) ---
# Jina AI 提供 1000万 tokens 免费额度，中文性能优秀
JINA_API_KEY = os.getenv("JINA_API_KEY") 
JINA_BASE_URL = os.getenv("JINA_BASE_URL") # 应设置为 https://api.jina.ai/v1

# ⚠️ 关键修正：使用 Jina AI 的中文模型
EMBEDDING_MODEL = "jina-embeddings-v2-base-zh" 

# --- 本地 Obsidian 配置 ---
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

# --- 同步目标 ---
# ⚠️ 强制检查：表名使用 rrx_notes 规范
SUPABASE_TABLE_NAME = 'rrxs_notes' 

# 排除的文件夹 (例如，Obsidian 自身的配置和草稿)
EXCLUDED_FOLDERS = ['.obsidian', '.git', 'Templates', 'Excalidraw']

# ====================================================================
# ------------------------- 2. 初始化客户端 --------------------------
# ====================================================================

print("===============================================")
print("📢 正在启动 Obsidian Vault 云端索引同步...")

# 检查所有必需的环境变量
if not all([SUPABASE_URL, SUPABASE_KEY, JINA_API_KEY, OBSIDIAN_VAULT_PATH, JINA_BASE_URL]):
    print("❌ 错误：关键环境变量缺失，请检查 .env 文件中 Supabase 和 Jina AI 的配置项。")
    exit()

try:
    # 2.1 初始化 Jina AI 客户端 (兼容 OpenAI SDK)
    jina_client = OpenAI(
        api_key=JINA_API_KEY,
        base_url=JINA_BASE_URL
    )
    # 2.2 初始化 Supabase 客户端
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ 客户端初始化成功：Jina AI API & Supabase 连接就绪。")
except Exception as e:
    print(f"❌ 客户端初始化失败: {e}")
    exit()

# 2.3 初始化文本分块器
# 适用于 Markdown 和普通文本的递归分块器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""],
) # 确保这里的括号是完整闭合的！