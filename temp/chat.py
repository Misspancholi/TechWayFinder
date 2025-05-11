from langchain_openai.chat_models import ChatOpenAI
import streamlit as st
from temp.sidebar import show_sidebar

def init_chat_client():
    """Initialize chat client using Streamlit secrets"""
    try:
        api_key = st.secrets["TOGETHER_API_KEY"]
        client = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            temperature=1,
            api_key=api_key,
            max_tokens=5000
        )
        return client
    except Exception:
        print("Error initializing chat client. Check your API key.")
        return None

def chatbot():
    # Show sidebar
    show_sidebar()
    
    client = init_chat_client()
    
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

    st.markdown("""
        <div class='chat-container glass-card page-transition'>
            <h1 class='text-focus-in' style='text-align: center; color: #333; margin-bottom: 30px;'>
                🤖 AI Career Assistant
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # Display chat messages
    for msg in st.session_state["messages"]:
        if msg["role"] != "system":
            role_class = "user" if msg["role"] == "user" else "assistant"
            st.markdown(f"""
                <div class='chat-message {role_class}'>
                    <div class='message-content'>
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Handle input using Streamlit's chat_input
    user_input = st.chat_input("Ask me anything about your career path...")

    if user_input and client:
        try:
            # Add user message to state
            st.session_state["messages"].append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.spinner('Thinking...'):
                response = client.invoke(st.session_state["messages"])
                bot_reply = response.content
                st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
                st.rerun()
        except Exception:
            st.session_state["messages"].pop()
    print(st.session_state["messages"])
