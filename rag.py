from vector_stores import VectorStoreService
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import config_data as config
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history



class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=OpenAIEmbeddings(
                model=config.embedding_model,
                api_key=config.embedding_api_key,
                base_url="https://openrouter.ai/api/v1",
                check_embedding_ctx_length=False,
                chunk_size=1
            )
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的一直参口资料为主，"
                 "简介和专业的回答用户的问题，如果不知道就回答不知道，参考资料如下：{context}"),
                ("system","并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder(variable_name="history"),
                ("user","请回答用户的问题:{input}")
            ]
        )

        self.chat_model  = ChatOpenAI(
            model=config.llm_model,
            api_key= config.llm_api_key,
            base_url=config.llm_base_url
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        #获取最终的执行链
        retriever = self.vector_service.get_retriever()

        def format_documents(docs:list[Document]):
            if not docs:
                return "没有找到相关的文档"
            # 将 list[Document] 转成 str
            formatted_docs = ""
            for doc in docs:
                formatted_docs += f"文档片段: {doc.page_content}\n 文档元数据: {doc.metadata}\n\n"
            formatted_docs += ""
            return formatted_docs

        chain = (
            {
                "input":RunnablePassthrough(),
                "context":retriever | format_documents,
            } | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversion_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversion_chain

if __name__ == '__main__':
    #session_id 配置
    session_config = {
        "configurable":{
            "session_id":"test_session"
        }
    }
    rag_service = RagService()
    user_input = "我的体重150斤，身高1米75,尺码推荐"
    result = rag_service.chain.invoke({"input": user_input}, session_config)
    print(result)


    #NOTE:注意这个玩意因为添加了history所以导致出问题了，教程太复杂繁琐并且chain的使用方式也不太一样，暂时先不修改了
