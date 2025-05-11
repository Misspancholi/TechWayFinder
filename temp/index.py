import streamlit as st
import base64
import sqlite3
from temp.sidebar import show_sidebar

def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def check_eligibility(user_id):
    conn = sqlite3.connect('temp/TWF.db', check_same_thread=False)
    c = conn.cursor()
    
    # Check if user_profile table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profile'")
    if not c.fetchone():
        conn.close()
        return False, None
    
    # Check if user has filled the profile form
    c.execute("SELECT * FROM user_profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    
    if not profile:
        return False, None
    
    # Check if user has an eligible qualification
    eligible_qualifications = ["BCA", "MCA", "B.Tech", "M.Tech", "Ph.D.", "Other(related to IT)"]
    # Assuming qualification is stored in the second column (index 1)
    return True, profile[1] in eligible_qualifications

def check_quiz_taken(user_id):
    conn = sqlite3.connect('temp/TWF.db', check_same_thread=False)
    c = conn.cursor()
    
    # Check if quiz_scores table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_scores'")
    if not c.fetchone():
        conn.close()
        return False
    
    # Check if user has quiz scores
    c.execute("SELECT * FROM quiz_scores WHERE user_id = ?", (user_id,))
    scores = c.fetchone()
    conn.close()
    
    return scores is not None

def show_dashboard():
    # Check if user has completed eligibility form and has eligible qualification
    profile_completed, has_eligible_qualification = check_eligibility(st.session_state.user_id)
    
    # Check if user has taken the quiz
    quiz_taken = check_quiz_taken(st.session_state.user_id)
    
    # Show sidebar
    show_sidebar()
    
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
    
    # Show eligibility notification if not completed
    if not profile_completed:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 99, 71, 0.1), rgba(255, 99, 71, 0.2)); 
                        padding: 15px; border-radius: 10px; margin: 20px 0;'>
                <h3 style='color: #ff6347; margin-bottom: 10px;'>⚠️ Profile Required</h3>
                <p style='color: #666;'>
                    Please complete your profile to unlock all features.
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif not has_eligible_qualification:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 184, 0, 0.1), rgba(255, 184, 0, 0.2)); 
                        padding: 15px; border-radius: 10px; margin: 20px 0;'>
                <h3 style='color: #ff9800; margin-bottom: 10px;'>⚠️ Qualification Requirement</h3>
                <p style='color: #666;'>
                    The quiz is designed for users with IT-related qualifications (BCA, MCA, B.Tech, M.Tech, Ph.D., or other IT-related degrees).
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Create a row for profile management
    col_profile1, col_profile2, col_profile3 = st.columns([1, 2, 1])
    
    with col_profile2:
        if profile_completed:
            if st.button("Edit Your Profile", key="edit_profile_btn", use_container_width=True):
                st.session_state.page = "profile"
                st.rerun()
        else:
            if st.button("Complete Your Profile", key="eligibility_btn", use_container_width=True):
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
        
        # Disable quiz button if eligibility not completed or qualification not eligible
        if st.button("Quiz", disabled=not (profile_completed and has_eligible_qualification)):
            st.session_state.page = "quiz"
            st.rerun()
        
        # Show message if button is disabled
        if not profile_completed:
            st.error("Complete your profile to unlock quiz")
        elif not has_eligible_qualification:
            st.error("IT qualification required for quiz")
            
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
        
        # Disable results button if quiz not taken
        if st.button("Quiz Results", disabled=not quiz_taken):
            st.session_state.page = "results"
            st.rerun()
        
        # Show message if button is disabled
        if not quiz_taken:
            st.error("Complete the quiz to view results")
            
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
    
   
        
    # Remove these buttons as they're now in the sidebar
    # st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    # if st.button("Logout"):
    #     st.session_state.page = "auth"
    #     st.session_state.authenticated = False
    #     st.rerun()
    # st.markdown("</div>", unsafe_allow_html=True)
    # if st.button("Back to Homepage"):
    #     st.session_state.page = "landing"
    #     st.rerun()
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
