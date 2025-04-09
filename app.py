import streamlit as st
import pandas as pd
import base64
import time
import sqlite3
import hashlib
import os 
import random
import re

# Set page config with favicon
st.set_page_config(
    page_title="CareerGeek",
    page_icon="images/logo.jpg",
    layout="wide"
)

# Function to load CSS
def load_css():
    with open('static/app_styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
load_css()

# Function to encode image
db_path = "temp/TWF.db"
@st.cache_data
def get_base64_from_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Encode background image
logo_image=bg_image = get_base64_from_file("images/logo.jpg")


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Intro Animation Page
if st.session_state.page == "intro":
    st.markdown(f"""
         <div style='display: flex; justify-content: center; align-items: center; height: 100vh;' class='fade-in'>
            <img src='data:image/jpeg;base64,{logo_image}' style='width: 100%; max-width: 700px;'>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Show logo for 2 seconds
    st.session_state.page = "auth"
    st.rerun()

# Authentication Page
elif st.session_state.page == "auth":
    from pages.login_page import show_auth_page
    show_auth_page()

# Main Dashboard
elif st.session_state.page == "index":
    st.markdown("<div class='navbar'>🌟 Welcome to the Dashboard</div>", unsafe_allow_html=True)
    
    # Create three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Quiz'>
                </div>
                <h3>Take Quiz</h3>
                <p>Test your knowledge with our interactive quizzes</p>
            </div>
        """.format(get_base64_from_file("images/quiz.png")), unsafe_allow_html=True)
        if st.button("Quiz"):
            st.session_state.page = "quiz"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Results'>
                </div>
                <h3>View Results</h3>
                <p>Check your performance and progress</p>
            </div>
        """.format(get_base64_from_file("images/result.png")), unsafe_allow_html=True)
        if st.button("Quiz Results"):
            st.session_state.page = "results"
            st.rerun()
            
    with col3:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Chatbot'>
                </div>
                <h3>Chat Assistant</h3>
                <p>Get help from our AI chatbot</p>
            </div>
        """.format(get_base64_from_file("images/chatbot.png")), unsafe_allow_html=True)
        if st.button("Chatbot"):
            st.session_state.page = "chatbot"
            st.rerun()
    
    # Logout button in a centered container
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.page = "auth"
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Quiz Page
elif st.session_state.page == "quiz":
    from temp.quiz import display_quiz  
    display_quiz()
    if st.button("Back to Dashboard"):
        st.session_state.page = "index"
        st.rerun()


# Quiz Results Page
elif st.session_state.page == "results":
    st.markdown("<div class='navbar'>📊 Quiz Results</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Based on your Performance")
    from temp.result import results
    results()
    if st.button("Back to Dashboard"):
        st.session_state.page = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Chatbot Page
elif st.session_state.page == "chatbot":
    st.subheader("Ask me anything!")
    from temp.chat import chatbot
    chatbot()
    dashbt = st.sidebar.button("Back to Dashboard")
    if dashbt:
        st.session_state.page = "index"
        # clearing messages without changing system role content
        st.session_state.messages=[st.session_state.messages[0]]
        
        st.rerun()
print("app is finished", "\nst.session state =",st.session_state.page)
