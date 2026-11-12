import os
from dotenv import load_dotenv

load_dotenv()

# Chroma 配置
collection_name = "my_knowledge_base_sample"
persist_directory = "./data/chroma_db"
md5_path = "./data/md5.txt"

# Embedding 模型配置
embedding_model = "liquid/lfm-2.5-embedding-350m:free"
embedding_api_key = os.getenv("OPENROUTER_API_KEY")

#slitter
chunk_size = 1000
chunk_overlap =100
separators=["\n\n","\n",".","!","?","。","！","？"," ",""]
max_split_char_number = 1000 #文本分割阈值