import streamlit as st
import sqlite3
import hashlib

# Hash password for security
def make_hashed_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Check login credentials
def login_user(email, password):
    conn = sqlite3.connect('streamlit\TWF.db')
    c = conn.cursor()
    
    hashed_password = make_hashed_password(password)
    c.execute('SELECT * FROM users WHERE email=? AND password=?', (email, hashed_password))
    result = c.fetchone()
    conn.close()
    return result

# Add new user
def signup_user(fullname, email, age, password):
    conn = sqlite3.connect('streamlit\TWF.db')
    c = conn.cursor()
    
    password = make_hashed_password(password)
    try:
        c.execute('INSERT INTO users (fullname, email, age, password) VALUES (?, ?, ?, ?)',
                 (fullname, email, age, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def main():
    st.title("Welcome to the App")
        
    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Login Tab
    with tab1:
        st.header("Login")
        login_email = st.text_input("Email Address", key="login_email").strip()
# print(type(login_email))
        login_password = st.text_input("Password", type="password", key="login_password").strip()
        
        if st.button("Login"):
            if login_email.strip() == "" or login_password.strip() == "":
                st.error("Please fill in all fields")
            else:
                result = login_user(login_email, login_password)
                if result:
                    st.success(f"Welcome back, {result[0]}!")
                    st.session_state.authenticated = True
                    st.session_state.page = "index"
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    # Sign Up Tab
    with tab2:
        st.header("Sign Up")
        new_fullname = st.text_input("Full Name", key="signup_fullname")
        new_email = st.text_input("Email Address", key="signup_email")
        new_age = st.number_input("Age", min_value=0, max_value=120, key="signup_age")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        if st.button("Sign Up"):
            if (new_fullname.strip() == "" or new_email.strip() == "" or 
                new_password.strip() == "" or confirm_password.strip() == ""):
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                if signup_user(new_fullname, new_email, new_age, new_password):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Email already exists")

if __name__ == "__main__":
    main()

