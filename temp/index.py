import streamlit as st

# Function to navigate to page 1
def go_to_page1():
    st.session_state.page = "page1"

# Function to navigate to page 2
def go_to_page2():
    st.session_state.page = "page2"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "index"

# Main Page Layout
if st.session_state.page == "index":
    st.title("Main Page")
    st.button("Go to Page 1", on_click=go_to_page1)
    st.button("Go to Page 2", on_click=go_to_page2)

# Import and display the appropriate page
if st.session_state.page == "page1":
    from page1 import display_page1
    display_page1()

if st.session_state.page == "page2":
    from page2 import display_page2
    display_page2()