#基于steamlit完成web网页上传服务
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time
#streamlist 核心是当前端发生变化时，streamlit会重新运行整个脚本
#添加title
st.title("知识库更新服务")

#file_uploder
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False
)
#session_state就是一个字典，存储了当前会话的所有状态信息,不会随着页面刷新而丢失
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    #提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 #kb

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式:{file_size} | 大小 : {file_size:.2f} KB")

    #get_value
    text = uploader_file.getvalue().decode("utf-8")
    #调用service的upload_by_str方法，将文本和文件名传入
    with st.spinner("正在上传文件到知识库，请稍等..."): #表示一个加载状态
        time.sleep(1) #模拟上传时间
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)