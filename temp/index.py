import streamlit as st
import base64

def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def show_dashboard():
    st.markdown("<div class='navbar animated-text'>🌟 Welcome to TechWayFinder</div>", unsafe_allow_html=True)
    
    # Welcome message with custom styling and background
    st.markdown("""
        <div style='text-align: center; margin: 20px 0; padding: 30px; background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1)); border-radius: 15px;' class='animated-text'>
            <h1 style='font-family: Montserrat, sans-serif; color: #6c5ce7; font-size: 2.5em; margin-bottom: 10px;'>
                Hello, {}</h1>
            <p style='font-family: Poppins, sans-serif; color: #E0B0FF; font-size: 1.2em;'>
                Ready to explore your tech career path?</p>
            <p style='font-family: Poppins, sans-serif; color: #666; font-size: 1em; margin-top: 10px;'>
                Discover your perfect tech role through our interactive quiz, AI-powered chat assistance, and comprehensive roadmaps.</p>
        </div>
    """.format(st.session_state.get('user_name', 'Guest')), unsafe_allow_html=True)
    if st.button("Eligibility Test"):
            st.session_state.page = "profile"
            st.rerun()
    
    # Create four columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='dashboard-column animated-text'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Quiz'>
                </div>
                <h3>Take Quiz</h3>
                <p>Test your knowledge with our interactive quizzes</p>
            </div>
        """.format(get_base64_from_file("images/quiz.png")), unsafe_allow_html=True)
        if st.button("Quiz"):
            st.session_state.page = "quiz"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Results'>
                </div>
                <h3>View Results</h3>
                <p>Check your performance and progress</p>
            </div>
        """.format(get_base64_from_file("images/result.png")), unsafe_allow_html=True)
        if st.button("Quiz Results"):
            st.session_state.page = "results"
            st.rerun()
            
    with col3:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Chatbot'>
                </div>
                <h3>Chat Assistant</h3>
                <p> Get help from our AI chatbot regarding your career   <br></p>
            </div>
        """.format(get_base64_from_file("images/chatbot.png")), unsafe_allow_html=True)
        if st.button("Chatbot"):
            st.session_state.page = "chatbot"
            st.rerun()
    
    with col4:
        st.markdown("""
            <div class='dashboard-column'>
                <div class='image-container'>
                    <img src='data:image/png;base64,{}' class='dashboard-image' alt='Roadmaps'>
                </div>
                <h3>Career Roadmaps</h3>
                <p>Explore learning paths for different tech roles</p>
            </div>
        """.format(get_base64_from_file("images/roadmap.png")), unsafe_allow_html=True)
        if st.button("Roadmaps"):
            st.session_state.page = "roadmaps"
            st.rerun()
    
   
        
    # Logout button in a centered container
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.page = "auth"
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Back to Homepage"):
        st.session_state.page = "landing"
        st.rerun()
    # Add some space before footer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Footer implementation
    st.markdown("""
        <style>
            .footer {
                position: relative;  /* Changed from fixed to relative */
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: rgba(108, 92, 231, 0.1);
                padding: 20px;
                text-align: center;
                border-top: 1px solid rgba(108, 92, 231, 0.2);
                margin-top: 50px;  /* Added margin-top */
            }
            .footer p {
                margin: 5px 0;
                color: #666;
                font-size: 14px;
                font-family: 'Poppins', sans-serif;
            }
            
            /* Add padding to main content to prevent footer overlap */
            .main-content {
                padding-bottom: 100px;
            }
        </style>
        <div class='footer'>
            <p>Developed by Students of MLSU - Kavish Menaria & Kanishka Pancholi</p>
            <p>© 2025 TechWayFinder. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)
