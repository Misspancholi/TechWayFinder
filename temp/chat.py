from langchain_openai.chat_models import ChatOpenAI
import os
import streamlit as st
from dotenv import load_dotenv

def chatbot():
    load_dotenv()
    client = ChatOpenAI(
        base_url="https://api.together.xyz/v1",
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        temperature=1,
        api_key=os.getenv("together_api_key"),
        max_tokens=5000
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": """You are an AI assistant for helping users to guide, show roadmaps, and resolve their queries towards their preferred job. 
            You are deployed on a website called TechWayFinder,
            which takes a quiz and predicts specifically tech job roles based on skill scores. 
            we have a quiz page where user can take a quiz and get their results so ensure they use that. quiz can be accessed from the dashboard.
            Keep your tone gentle and student-friendly.
            Strictly stay on track and avoid unrelated topics.
            """}
        ]

    st.title("🤖 TWF AI Conversational Chatbot")

    for msg in st.session_state["messages"]:
        if msg["role"] != "system":  
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("Ask me anything about your career path...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        print(st.session_state["messages"])
        st.chat_message("user").markdown(user_input)

        response = client.invoke(st.session_state["messages"])
        bot_reply = response.content

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

def new_func():
    print(st.session_state["messages"])
