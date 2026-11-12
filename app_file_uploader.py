#基于steamlit完成web网页上传服务
import streamlit as st

#添加title
st.title("知识库更新服务")

#file_uploder
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False
)

if uploader_file is not None:
    #提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 #kb

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式:{file_size} | 大小 : {file_size:.2f} KB")

    #get_value
    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)