import os 
import random
import streamlit as st

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Load and apply CSS
def load_css(css_file):
    with open(css_file, 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load CSS file
load_css('static/styles.css')

# Navigation bar with JavaScript for handling clicks
st.markdown("""
    <script>
        function handleNav(page) {
            window.location.hash = page;
            window.location.reload();
        }
    </script>
    <div class="nav-bar">
        <a href="#" class="nav-button" onclick="handleNav('home')">Home</a>
        <a href="#" class="nav-button" onclick="handleNav('services')">Services</a>
        <a href="#" class="nav-button" onclick="handleNav('contact')">Contact</a>
    </div>
""", unsafe_allow_html=True)

def show_home_page():
    st.header("Home Page")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/home1.jpg", use_container_width=True)
        if st.button('Learn More', key='home1'):
            st.write('Home Section 1 clicked!')
    
    with col2:
        st.image("images/home2.jpg", use_container_width=True)
        if st.button('Explore', key='home2'):
            st.write('Home Section 2 clicked!')
    
    with col3:
        st.image("images/home3.jpg", use_container_width=True)
        if st.button('Details', key='home3'):
            st.write('Home Section 3 clicked!')

def show_services_page():
    st.header("Services")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/service1.jpg", use_container_width=True)
        if st.button('Service 1', key='service1'):
            st.write('Service 1 clicked!')
    
    with col2:
        st.image("images/service2.jpg", use_container_width=True)
        if st.button('Service 2', key='service2'):
            st.write('Service 2 clicked!')
    
    with col3:
        st.image("images/service3.jpg", use_container_width=True)
        if st.button('Service 3', key='service3'):
            st.write('Service 3 clicked!')

def show_contact_page():
    st.header("Contact Us")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/contact1.jpg", use_container_width=True)
        if st.button('Email Us', key='contact1'):
            st.write('Email contact clicked!')
    
    with col2:
        st.image("images/contact2.jpg", use_container_width=True)
        if st.button('Call Us', key='contact2'):
            st.write('Phone contact clicked!')
    
    with col3:
        st.image("images/contact3.jpg", use_container_width=True)
        if st.button('Visit Us', key='contact3'):
            st.write('Location clicked!')

# Page navigation
if st.button('Home', key='nav_home'):
    st.session_state.current_page = 'home'
if st.button('Services', key='nav_services'):
    st.session_state.current_page = 'services'
if st.button('Contact', key='nav_contact'):
    st.session_state.current_page = 'contact'

# Display current page
if st.session_state.current_page == 'home':
    show_home_page()
elif st.session_state.current_page == 'services':
    show_services_page()
else:
    show_contact_page()
