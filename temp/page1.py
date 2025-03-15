import streamlit as st
def go_to_index():
    st.session_state.page = "index"
    st.switch_page("index")
def display_page1():
    st.title("Page 1")
    st.write("Welcome to Page 1!")

    # Button to navigate back to the Main Page
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
        go_to_index()
        # Ensures that the main page is displayed immediately