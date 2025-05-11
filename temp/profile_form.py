import streamlit as st
import sqlite3
import base64
from temp.sidebar import show_sidebar

def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_connection():
    return sqlite3.connect('temp/TWF.db', check_same_thread=False)

def update_user_profile(user_id, qualification, grade, tech_skills, soft_skills):
    conn = get_connection()
    c = conn.cursor()
    
    # Check if user_profile table exists, if not create it
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id INTEGER PRIMARY KEY,
            qualification TEXT,
            grade TEXT,
            technical_skills TEXT,
            soft_skills TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Check if profile exists
    c.execute("SELECT * FROM user_profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    
    if profile:
        # Update existing profile
        c.execute('''
            UPDATE user_profile 
            SET qualification = ?, grade = ?, technical_skills = ?, soft_skills = ?
            WHERE user_id = ?
        ''', (qualification, grade, tech_skills, soft_skills, user_id))
    else:
        # Insert new profile
        c.execute('''
            INSERT INTO user_profile (user_id, qualification, grade, technical_skills, soft_skills)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, qualification, grade, tech_skills, soft_skills))
    
    conn.commit()
    conn.close()
    return True

def get_user_profile(user_id):
    conn = get_connection()
    c = conn.cursor()
    
    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profile'")
    if not c.fetchone():
        conn.close()
        return None
    
    c.execute("SELECT * FROM user_profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    
    if profile:
        return {
            "qualification": profile[1],
            "grade": profile[2],
            "technical_skills": profile[3],
            "soft_skills": profile[4]
        }
    return None

def show_profile_form():
    # Show sidebar
    show_sidebar()
    
    # Header with logo
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <img src='data:image/jpeg;base64,{get_base64_from_file("images/logo.jpg")}' style='width: 150px; margin-bottom: 20px;'>
            <h1 style='color: #6c5ce7; font-family: Montserrat, sans-serif;'>Your Profile</h1>
            <p style='color: #666; font-family: Poppins, sans-serif;'>
                Update your profile information to personalize your experience.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get existing profile if available
    user_profile = get_user_profile(st.session_state.user_id)
    
    # Check if profile exists
    profile_exists = user_profile is not None
    
    # Show appropriate header based on whether profile exists
    if profile_exists:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1)); 
                        padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='color: #6c5ce7; margin-bottom: 10px;'>Edit Your Profile</h3>
                <p style='color: #666;'>
                    You can update your profile information at any time.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1)); 
                        padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='color: #6c5ce7; margin-bottom: 10px;'>Complete Your Profile</h3>
                <p style='color: #666;'>
                    Help us personalize your experience by providing more information about your background.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Initialize user_profile if it doesn't exist
    if user_profile is None:
        user_profile = {
            "qualification": "",
            "grade": "",
            "technical_skills": "",
            "soft_skills": ""
        }
    
    # Create columns for form layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Qualification dropdown
        qualification_options = [
            "BA",
            "B.Com",
            "B.Sc",
            "BCA",
            "BBA",
            "B.Tech",
            "MA",
            "M.Com",
            "M.Sc", 
            "MCA",
            "MBA",
            "M.Tech",
            "Ph.D.",
            "Other(related to IT)"
        ]
        
        # Find index of current qualification or default to 0
        qual_index = 0
        if user_profile["qualification"] in qualification_options:
            qual_index = qualification_options.index(user_profile["qualification"])
        
        qualification = st.selectbox(
            "Highest Qualification",
            options=qualification_options,
            index=qual_index
        )
        
        # Grade dropdown
        grade_options = [
            "A+ (90-100%)",
            "A (85-89%)",
            "B+ (80-84%)",
            "B (75-79%)",
            "C+ (70-74%)",
            "C (65-69%)",
            "D (60-64%)",
            "Pass",
            "Not Applicable"
        ]
        
        # Find index of current grade or default to 0
        grade_index = 0
        if user_profile["grade"] in grade_options:
            grade_index = grade_options.index(user_profile["grade"])
        
        grade = st.selectbox(
            "Grade/Performance",
            options=grade_options,
            index=grade_index
        )
    
    with col2:
        # Technical skills multiselect
        tech_skills_options = [
            "Programming",
            "Database Management",
            "Web Development",
            "Mobile Development",
            "Cloud Computing",
            "DevOps",
            "Data Science",
            "Machine Learning",
            "Artificial Intelligence",
            "Cybersecurity",
            "Networking",
            "UI/UX Design",
            "Game Development",
            "Blockchain",
            "IoT",
            "AR/VR",
            "Robotics"
        ]
        
        default_tech = user_profile["technical_skills"].split(",") if user_profile["technical_skills"] else []
        # Remove empty strings
        default_tech = [skill for skill in default_tech if skill]
        
        tech_skills = st.multiselect(
            "Technical Skills",
            options=tech_skills_options,
            default=default_tech
        )
        
        # Soft skills multiselect
        soft_skills_options = [
            "Communication",
            "Teamwork",
            "Problem Solving",
            "Critical Thinking",
            "Time Management",
            "Leadership",
            "Adaptability",
            "Creativity",
            "Emotional Intelligence",
            "Conflict Resolution",
            "Presentation Skills",
            "Project Management",
            "Negotiation",
            "Customer Service",
            "Decision Making"
        ]
        
        default_soft = user_profile["soft_skills"].split(",") if user_profile["soft_skills"] else []
        # Remove empty strings
        default_soft = [skill for skill in default_soft if skill]
        
        soft_skills = st.multiselect(
            "Soft Skills",
            options=soft_skills_options,
            default=default_soft
        )
    
    # Submit button text changes based on whether profile exists
    button_text = "Update Profile" if profile_exists else "Save Profile"
    
    if st.button(button_text, use_container_width=True, type="primary"):
        tech_skills_str = ",".join(tech_skills)
        soft_skills_str = ",".join(soft_skills)
        
        if update_user_profile(st.session_state.user_id, qualification, grade, tech_skills_str, soft_skills_str):
            success_message = "Profile updated successfully!" if profile_exists else "Profile created successfully!"
            st.success(success_message)
            st.balloons()
        else:
            st.error("Failed to update profile. Please try again.")
    
    # Back button
    if st.button("Back to Dashboard", use_container_width=True):
        st.session_state.page = "index"
        st.rerun()
    
    # Add custom styling
    st.markdown("""
        <style>
        div[data-testid="stSelectbox"] {
            margin-bottom: 20px;
        }
        
        div[data-testid="stMultiSelect"] {
            margin-bottom: 20px;
        }
        
        .stButton button {
            background-color: #6c5ce7;
            color: white;
            font-weight: 500;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin-top: 20px;
        }
        
        .stButton button:hover {
            background-color: #5b4cc4;
        }
        
        /* Style for the multiselect boxes */
        div[data-baseweb="select"] {
            border-radius: 8px;
        }
        
        div[data-baseweb="tag"] {
            background-color: rgba(108, 92, 231, 0.2);
            border: 1px solid #6c5ce7;
        }
        
        /* Style for the select dropdown */
        div[data-baseweb="select"] > div {
            border-color: #6c5ce7;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)




