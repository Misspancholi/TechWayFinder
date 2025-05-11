import streamlit as st
import sqlite3

def get_user_info(user_id):
    """Get user information from database"""
    conn = sqlite3.connect("temp/TWF.db")
    c = conn.cursor()
    c.execute("SELECT name, email FROM users WHERE user_id = ?", (user_id,))
    user_info = c.fetchone()
    conn.close()
    
    if user_info:
        return {"name": user_info[0], "email": user_info[1]}
    return {"name": "Guest", "email": ""}

def show_sidebar():
    """Display common sidebar with user info and navigation"""
    with st.sidebar:
        # User info section
        if st.session_state.get("authenticated", False):
            user_info = get_user_info(st.session_state.user_id)
            st.markdown("### User Profile")
            st.markdown(f"**Name:** {user_info['name']}")
            st.markdown(f"**Email:** {user_info['email']}")
            st.divider()
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Common navigation buttons
        if st.button("Dashboard", key="sidebar_dashboard"):
            st.session_state.page = "index"
            st.rerun()
            
        if st.button("Profile", key="sidebar_profile"):
            st.session_state.page = "profile"
            st.rerun()
            
        if st.button("Back to Homepage", key="sidebar_homepage"):
            st.session_state.page = "landing"
            st.rerun()
            
        if st.session_state.get("authenticated", False):
            if st.button("Logout", key="sidebar_logout"):
                st.session_state.page = "auth"
                st.session_state.authenticated = False
                st.rerun()