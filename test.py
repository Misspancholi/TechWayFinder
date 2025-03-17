import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

st.title("🦜🔗 Quickstart App")

def generate_response(input_text):
    model = ChatOpenAI(
        base_url="https://api.together.xyz/v1",
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        temperature=0.7,
        api_key=os.getenv("together_api_key"), 
        max_completion_tokens=10,
        max_tokens=50
    )
    st.info(model.invoke(input_text).content)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted and text:
        generate_response(text)