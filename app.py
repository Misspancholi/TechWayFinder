import streamlit as st
import pandas as pd
import base64
import time
import sqlite3
import hashlib
import os 
import random
import re
from temp.sidebar import show_sidebar

# Set page config with favicon
st.set_page_config(
    page_title="TechWayFinder",
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
    st.session_state.authenticated = False

# Intro Animation Page
if st.session_state.page == "intro":
    st.markdown(f"""
         <div style='display: flex; justify-content: center; align-items: center; height: 100vh;' class='fade-in'>
            <img src='data:image/jpeg;base64,{logo_image}' style='width: 100%; max-width: 700px;'>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Show logo for 2 seconds
    st.session_state.page = "landing"
    st.rerun()

elif st.session_state.page == "landing":
    from temp.landing import show_landing_page
    show_landing_page()

# Authentication Page
elif st.session_state.page == "auth":
    # Skip to index if already authenticated
    if st.session_state.get("authenticated", False):
        st.session_state.page = "index"
        st.rerun()
    else:
        from temp.login_page import show_auth_page
        show_auth_page()

# Main Dashboard
elif st.session_state.page == "index":
    from temp.index import show_dashboard
    show_dashboard()    

# Quiz Page
elif st.session_state.page == "quiz":
    from temp.quiz import display_quiz  
    display_quiz()
    

# Quiz Results Page
elif st.session_state.page == "results":
    st.markdown("<div class='navbar'>📊 Quiz Results</div>", unsafe_allow_html=True)
    # st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Based on your Performance")
    from temp.result import results
    results()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Chatbot Page
elif st.session_state.page == "chatbot":
    st.subheader("Ask me anything!")
    from temp.chat import chatbot
    chatbot()
    # Remove the duplicate dashboard button
    # dashbt = st.sidebar.button("Back to Dashboard", key="chatbot_back_to_dashboard")
    # if dashbt:
    #     st.session_state.page = "index"
    #     # clearing messages without changing system role content
    #     st.session_state.messages=[st.session_state.messages[0]]
    #     st.rerun()

# Roadmaps Page
elif st.session_state.page == "roadmaps":
    from temp.roadmaps import show_roadmaps
    show_roadmaps()
    
    # Back button is handled within the roadmaps module

# Profile Form Page
elif st.session_state.page == "profile":
    from temp.profile_form import show_profile_form
    show_profile_form()

print("app is finished", "\nst.session state =",st.session_state.page)
