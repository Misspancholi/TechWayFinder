import streamlit as st
import sqlite3
import hashlib
import os
import random
import re
from pathlib import Path

def get_hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    hashed_password = get_hashed_password(password)
    conn = sqlite3.connect("temp/TWF.db")
    c = conn.cursor()
    c.execute('select * from users where email=? and password=?',(email, hashed_password))
    user = c.fetchone()
    conn.close()
    if user:
        st.session_state.user_id = user[0]
        st.session_state.page = "index"
        st.session_state.authenticated = True
        st.session_state.user_name = user[3]
        return True
    return False

def signup_user(name, email, age, password):
    hashed_password = get_hashed_password(password)
    conn = sqlite3.connect("temp/TWF.db")
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email, age, password) VALUES (?, ?, ?, ?)', 
                 (name, email, age, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def show_auth_page():
    st.markdown("<div class='navbar'>🔐 Authentication</div>", unsafe_allow_html=True)
    
    # Add welcome message and description
    st.markdown("""
        <div style='text-align: center; margin: 20px 0; padding: 30px; background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1)); border-radius: 15px;'>
            <h1 style='font-family: Montserrat, sans-serif; color: #6c5ce7; margin-bottom: 15px;'>Welcome to TechWayFinder</h1>
            <p style='font-family: Poppins, sans-serif; color: #666; font-size: 1.1em; max-width: 600px; margin: 0 auto;'>
                Your gateway to discovering the perfect tech career path. Join us to explore personalized roadmaps, 
                take skill assessment quizzes, and get AI-powered guidance for your tech journey.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True, 
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    with col2:
        if st.button("Sign Up", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'signup' else "secondary"):
            st.session_state.auth_mode = 'signup'
            st.rerun()

    # st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    
    # Login Form
    if st.session_state.auth_mode == 'login':
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        
        # Create a form that can be submitted with Enter key
        with st.form("login_form", clear_on_submit=True):
            login_email = st.text_input("Email", placeholder="Enter your email", 
                                      key="login_email").strip()
            login_password = st.text_input("Password", type="password", 
                                         placeholder="Enter your password", 
                                         key="login_pass").strip()
            
            # Captcha
            if 'captcha_image_name' not in st.session_state:
                image_files = [f for f in os.listdir('captcha') if f.endswith(('png',))]
                st.session_state.captcha_image_name = random.choice(image_files)
            captcha_image = "captcha/" + st.session_state.captcha_image_name
            st.image(captcha_image)
            captcha_input = st.text_input("Enter Captcha", 
                                        placeholder="Enter the text shown in image above").strip()
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if login_email == "" or login_password == "" or captcha_input == "":
                    st.error("Please fill in all fields")
                elif captcha_input != st.session_state.captcha_image_name.split('.')[0]:
                    st.error("Invalid captcha")
                else:
                    if login_user(login_email, login_password):
                        st.success("Login Successful")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

    # Signup Form
    else:
        st.markdown("<h2>Sign Up</h2>", unsafe_allow_html=True)
        
        # Create a form that can be submitted with Enter key
        with st.form("signup_form", clear_on_submit=True):
            new_fullname = st.text_input("Full Name", key="signup_fullname").strip()
            new_email = st.text_input("Email Address", key="signup_email").strip()
            new_age = st.number_input("Age", min_value=0, max_value=120, key="signup_age")
            new_password = st.text_input("Password", type="password", key="signup_password").strip()
            confirm_password = st.text_input("Confirm Password", type="password", 
                                           key="signup_confirm_password").strip()
            
            submitted = st.form_submit_button('Sign up', use_container_width=True)
            
            if submitted:
                if (new_fullname=="" or new_email=="" or new_password=="" or confirm_password==""):
                    st.error("Please fill in all fields")
                elif not is_valid_email(new_email):
                    st.error("Please enter a valid email address")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters long")
                else:
                    if signup_user(new_fullname, new_email, new_age, new_password):
                        st.success("User created successfully")
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.error("User already exists")

    st.markdown("</div>", unsafe_allow_html=True)


