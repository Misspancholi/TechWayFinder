import streamlit as st
import pandas as pd
import base64
import time
import sqlite3
import hashlib
import os 
import random

# Function to encode image
db_path = "temp/TWF.db"
@st.cache_data
def get_base64_from_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Encode background image
logo_image=bg_image = get_base64_from_file("images/logo.jpg")

def apply_custom_css():
    st.markdown(
        """
        <style>
            body {
                background-color: indigo;
                font-family: Arial, sans-serif;
            }
            .navbar {
                background-color: rgba(0, 0, 0, 0.8);
                padding: 15px;
                text-align: center;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }
            .content-container {
                text-align: center;
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }
            .stButton>button {
                background-color: #E0B0FF;
                color: black;
                font-size: 18px;
                padding: 12px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
                transition: transform 0.2s, background-color 0.3s, box-shadow 0.3s;
            }
            .stButton>button:hover {
                background-color: #E0B0FF;
                transform: scale(1.05);
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .fade-in {
                animation: fadeIn 2s ease-in-out;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    hashed_passord = get_hashed_password(password)
    conn = sqlite3.connect(db_path)  # Update this line with the correct path
    c = conn.cursor()
    c.execute('select * from users where email=? and password=?',(email, hashed_passord))
    user = c.fetchone()
    conn.close()
    print(user)
    if user:
        st.session_state.user_id = user[0]
        st.success("Authenticated")
        st.session_state.page = "index"
        st.session_state.authenticated = True
        st.session_state.user_name = user[3]
    else:
        print("Not Authenticated")
        st.error("Invalid username or password")
        st.session_state.authenticated = False

def signup_user(name, email, age, password):
    hashed_password = get_hashed_password(password)
    conn = sqlite3.connect(db_path)  # Update this line with the correct path
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email, age, password) VALUES (?, ?, ?, ?)', (name, email, age, hashed_password))
        conn.commit()
        conn.close()
        st.success("User created successfully")
    except sqlite3.IntegrityError:
        conn.close()
        st.error("User already exists")

apply_custom_css()

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
    st.session_state.page = "login"
    st.rerun()

# Login Page
elif st.session_state.page == "login":
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        st.markdown("<div class='navbar'>🔐 Login Page</div>", unsafe_allow_html=True)
        st.markdown("<div class='content-container'>", unsafe_allow_html=True)
        login_email = st.text_input("email", placeholder="Enter your username").strip()
        login_password = st.text_input("Password", type="password", placeholder="Enter your password").strip()
        
        # Captcha image show
        if 'captcha_image_name' not in st.session_state:
            image_files = [f for f in os.listdir('captcha') if f.endswith(('png',))] 
            st.session_state.captcha_image_name = random.choice(image_files) # captcha image name
        captcha_image = "captcha/" + st.session_state.captcha_image_name # captcha image path
        st.image(captcha_image)
        
        # Add captcha input field
        captcha_input = st.text_input("Enter Captcha", placeholder="Enter the text shown in image above").strip()
        
        if st.button("Login"):
            if login_email == "" or login_password == "" or captcha_input == "":
                st.error("Please fill in all fields")
            else:
                login_user(login_email, login_password)    
                if st.session_state.authenticated:
                    st.success("Login Successful")
                    st.rerun()        
        st.markdown("</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown("<div class='navbar'>🔐 Sign Up Page</div>", unsafe_allow_html=True)
        st.markdown("<div class='content-container'>", unsafe_allow_html=True)
        new_fullname = st.text_input("Full Name", key="signup_fullname").strip()
        new_email = st.text_input("Email Address", key="signup_email").strip()
        new_age = st.number_input("Age", min_value=0, max_value=120, key="signup_age")
        new_password = st.text_input("Password", type="password", key="signup_password").strip()
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password").strip()
        if st.button('Sign up'):
            if (new_fullname=="" or new_email=="" or new_password=="" or confirm_password==""):
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("passwords does not match")
            else:
                signup_user(new_fullname, new_email, new_age, new_password)



# Main Dashboard
elif st.session_state.page == "index":
    st.markdown("<div class='navbar'>🌟 Welcome to the Dashboard</div>", unsafe_allow_html=True)
    #st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    st.subheader("Select an Option")
    
    if st.button("Quiz"):
        st.session_state.page = "quiz"
        st.rerun()
    if st.button("Quiz Results"):
        st.session_state.page = "results"
        st.rerun()
    if st.button("Chatbot"):
        st.session_state.page = "chatbot"
        st.rerun()
    if st.button("Logout"):
        st.session_state.page = "login"
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