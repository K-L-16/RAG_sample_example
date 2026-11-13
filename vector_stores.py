from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import config_data as config




class VectorStoreService:
    def __init__(self,embedding):
        # Initialize the vector store service
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

#返回向量检索器，方便加入链
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})  # 设置相似度阈值，超过该阈值的文本将被认为是重复的

if __name__ == '__main__':
    embedding = OpenAIEmbeddings(
        model=config.embedding_model,
        api_key=config.embedding_api_key,
        base_url="https://openrouter.ai/api/v1",
        check_embedding_ctx_length=False,
        chunk_size=1
    )
    vector_store_service = VectorStoreService(embedding)
    retriever = vector_store_service.get_retriever()
    print(retriever.invoke("我的体重150斤，身高1米75"))
