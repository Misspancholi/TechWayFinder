import streamlit as st

# Hardcoded user credentials (Replace with a database in real-world apps)
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "test123",
}

def login():
    """Login page for user authentication"""
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def main_app():
    """Main application page after authentication"""
    st.title("Welcome to the App!")
    st.write(f"Hello, {st.session_state['username']}!")

    if st.button("Logout"):
        del st.session_state["authenticated"]
        del st.session_state["username"]
        st.experimental_rerun()

def main():
    """Handles authentication and routing"""
    if "authenticated" not in st.session_state:
        login()
    else:
        main_app()

if __name__ == "__main__":
    main()
