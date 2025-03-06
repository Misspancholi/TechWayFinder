import streamlit as st

def display_page1():
    st.title("Page 1")
    st.write("Welcome to Page 1!")

    # Button to navigate back to the Main Page
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
        st.experimental_rerun()  # Ensures that the main page is displayed immediately