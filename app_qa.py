
import time
from rag import RagService
import streamlit as st

# 标题
st.title("智能客服")
st.divider()  # 分隔符

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "你好，有什么可以帮助你？"}
    ]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:

    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("AI思考中..."):
        result = st.session_state["rag"].chain.invoke({"input": prompt}, {"configurable":{"session_id":"test_session"}})
        st.session_state["message"].append(
            {"role": "assistant", "content": result}
        )
