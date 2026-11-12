#知识库
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str : str):
    #检查传入的md5字符串是否已经被处理过了
    #False 表示未处理
    #True 表示已经处理
    if not os.path.exists(config.md5_path):
        #if进入表示文件不存在
        open(config.md5_path,"w",encoding="utf-8").close() #创建文件
        return False
    else:
        for line in open(config.md5_path,"r",encoding="utf-8").readlines():
            line = line.strip() #处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False


def save_md5(md5_str : str):
    #将传入的md5字符串，记录到文件内保存
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str+"\n")

def get_string_md5(input_str:str, encoding="utf-8"):
    #将传入的字符串转换为md5字符串
    #将字符串转换为byte字节数组
    str_bytes = input_str.encode(encoding=encoding)

    #创建md5对象
    md5_obj = hashlib.md5() #得到md5对象
    md5_obj.update(str_bytes) #更新内容
    md5_hex = md5_obj.hexdigest()   #得到md5的十六进制字符串

    return md5_hex



class KnowledgeBaseService:

    def __init__(self):
        #如果文件不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        # 1. 创建 Embedding 模型
        self.embedding = OpenAIEmbeddings(
            model=config.embedding_model,
            api_key=config.embedding_api_key,
            base_url="https://openrouter.ai/api/v1",
            check_embedding_ctx_length=False,
            chunk_size=1
        )

        # 2. 创建向量数据库
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

        # 3. 文本分割器
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size, #分割后的文本最大长度
            chunk_overlap=config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separators,#分割符
            length_function=len #使用python自带的len函数作为长度一句
        )

    def upload_by_str(self, data, filename):
        #将传入的字符串，进行向量化，存入向量数据库中
        #先得到传入字符串的md5
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库"

        #由于我们这里拿到的是list【str】
        if(len(data)) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]

        #metadata:
        metadata={
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"admin"
        }
        self.chroma.add_texts(
            #iterable -> list \tuple
            knowledge_chunks,
            metedata=[metadata for _ in knowledge_chunks]
        )
        #保存md5到文件中
        save_md5(md5_hex)
        return "[成功]内容已经存入知识库"
        


if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("这是一个测试知识库的内容","testfile")
    print(r)