import streamlit as st
import sqlite3

if 'page' not in st.session_state:
    st.session_state.page = "login"
    st.session_state.authenticated = False
    st.session_state.user_id = None
    

def login_user(email, password):
    # Hardcoded login for demonstration purposes
    email = 'a@email.com'
    password = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
    conn = sqlite3.connect('streamlit/TWF.db')
    c = conn.cursor()
    c.execute('select * from users where email=? and password=?', (email, password))
    user = c.fetchone()
    conn.close()
    print(user)
    if user:
        st.session_state.user_id = user[1]
        print("Authenticated")
        st.session_state.page = "index"
        st.session_state.authenticated = True
        st.session_state.user_id = user[0]
    else:
        print("Not Authenticated")
        st.error("Invalid username or password")
        st.session_state.authenticated = False
        return False
    return True

if st.session_state.page == "login":
    st.title("Welcome to the App")
    login_email = st.text_input("Email Address", key="login_email").strip()
    login_password = st.text_input("Password", type="password", key="login_password").strip()
    if st.button("Login"):
        if login_email=="" or login_password=="":
            st.error("Please fill in all fields")
        else:
            if login_user(login_email, login_password):   
                st.success("Login Successful")
                st.rerun()