import streamlit as st
import pandas as pd
import base64

# Function to encode image
@st.cache_data
def get_base64_from_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Encode background image
bg_image = get_base64_from_file("C:/Career_website/TWFlogo.jpg")

def apply_custom_css():
    st.markdown(
        f"""
        <style>
            .main-bg {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: url('data:image/jpeg;base64,{bg_image}') no-repeat center center fixed;
                background-size: cover;
                z-index: -1;
                filter: blur(5px);
            }}
            .navbar {{
                background-color: rgba(0, 0, 0, 0.8);
                padding: 15px;
                text-align: center;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }}
            .content-container {{
                text-align: center;
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }}
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 12px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                transition: transform 0.2s, background-color 0.3s, box-shadow 0.3s;
            }}
            .stButton>button:hover {{
                background-color: #45a049;
                transform: scale(1.05);
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }}
        </style>
        <div class='main-bg'></div>
        """,
        unsafe_allow_html=True,
    )

apply_custom_css()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"

# Login Page
if st.session_state.page == "login":
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.title("🔐 Login Page")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        if username == "admin" and password == "password123":
            st.session_state.page = "index"
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.markdown("</div>", unsafe_allow_html=True)

# Main Dashboard
elif st.session_state.page == "index":
    st.markdown("<div class='navbar'>🌟 Welcome to the Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Select an Option")
    
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        if st.button("Quiz"):
            st.session_state.page = "quiz"
            st.rerun()
    with col2:
        if st.button("Quiz Results"):
            st.session_state.page = "results"
            st.rerun()
    with col3:
        if st.button("Chatbot"):
            st.session_state.page = "chatbot"
            st.rerun()
    with col4:
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.authenticated = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Quiz Page
elif st.session_state.page == "quiz":
    st.markdown("<div class='navbar'>📊 Take Quiz</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Retake Quiz")
    if "quiz_results" in st.session_state:
        df = pd.DataFrame(st.session_state["quiz"], columns=["Question", "Your Answer", "Correct Answer", "Result"])
        st.table(df)
    else:
        st.write("No quiz results found. Please take the quiz first.")
    if st.button("Back to Dashboard"):
        st.session_state.page = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Quiz Results Page
elif st.session_state.page == "results":
    st.markdown("<div class='navbar'>📊 Quiz Results</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Your Performance")
    if "quiz_results" in st.session_state:
        df = pd.DataFrame(st.session_state["quiz_results"], columns=["Question", "Your Answer", "Correct Answer", "Result"])
        st.table(df)
    else:
        st.write("No quiz results found. Please take the quiz first.")
    if st.button("Back to Dashboard"):
        st.session_state.page = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Chatbot Page
elif st.session_state.page == "chatbot":
    st.markdown("<div class='navbar'>🤖 Chatbot</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Ask me anything!")
    user_input = st.text_input("You:", "", key="chat_input")
    if st.button("Send"):
        if user_input.strip():
            st.write(f"**Bot:** I'm here to help with {user_input}!")
        else:
            st.warning("Please enter a message.")
    if st.button("Back to Dashboard"):
        st.session_state.page = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)