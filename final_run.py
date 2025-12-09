import streamlit as st
from weixin_agent import weixinAgent
from langchain_ollama import ChatOllama 


@st.cache_resource
def load_agent():
    return weixinAgent()

agent = load_agent()

st.title("Weixin Customer Service Agent")

customer_id = st.text_input("Weixin ID")
review = st.text_area("Your Review")

if st.button("Process Review"):
    if customer_id and review:
        with st.spinner("Thinking..."):
            response = agent.process_review(customer_id, review)
            st.success("Response:")
            st.write(response)
    else:
        st.warning("Please enter both your Weixin ID and Your Review")