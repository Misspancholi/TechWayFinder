import streamlit as st
import sqlite3
import base64

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
        return False
    
    # Check if user has filled the profile form
    c.execute("SELECT * FROM user_profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    
    if not profile:
        return False
    
    # Check if user has an eligible qualification
    eligible_qualifications = ["BCA", "MCA", "B.Tech", "M.Tech", "Ph.D.", "Other(related to IT)"]
    # Assuming qualification is stored in the second column (index 1)
    return profile[1] in eligible_qualifications

def display_quiz():
    # Check eligibility first
    if not check_eligibility(st.session_state.user_id):
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 30px;'>
                <img src='data:image/jpeg;base64,{get_base64_from_file("images/logo.jpg")}' style='width: 150px; margin-bottom: 20px;'>
                <div style='background: linear-gradient(135deg, rgba(255, 99, 71, 0.1), rgba(255, 99, 71, 0.2)); 
                            padding: 20px; border-radius: 15px; margin: 20px 0;'>
                    <h1 style='color: #ff6347; font-family: Montserrat, sans-serif; margin-bottom: 15px;'>
                        Eligibility Check Failed
                    </h1>
                    <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1.1em; margin-bottom: 10px;'>
                        This quiz is designed for users with IT-related qualifications.
                    </p>
                    <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1em;'>
                        Eligible qualifications: BCA, MCA, B.Tech, M.Tech, Ph.D., or other IT-related degrees.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Update Your Profile", use_container_width=True, type="primary"):
            st.session_state.page = "profile"
            st.rerun()
            
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.page = "index"
            st.rerun()
            
        return
    
    # Original quiz code continues here
    # Add logo and welcome content at the top
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <img src='data:image/jpeg;base64,{}' style='width: 150px; margin-bottom: 20px;'>
            <div style='background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1)); 
                        padding: 20px; border-radius: 15px; margin: 20px 0;'>
                <h1 style='color: #6c5ce7; font-family: Montserrat, sans-serif; margin-bottom: 15px;'>
                    Technical Skills Assessment Quiz
                </h1>
                <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1.1em; margin-bottom: 10px;'>
                    Welcome to TechWayFinder's comprehensive skills assessment! This quiz will help evaluate your technical 
                    proficiency across various domains.
                </p>
                <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1em;'>
                    📝 34 carefully crafted questions<br>
                    ⏱️ Take your time to answer thoughtfully<br>
                    🎯 Get personalized career recommendations based on your responses
                </p>
            </div>
        </div>
    """.format(get_base64_from_file("images/logo.jpg")), unsafe_allow_html=True)

    if "submit" not in st.session_state:
        st.session_state.submit = False
    
    def get_connection():
        return sqlite3.connect('temp/TWF.db', check_same_thread=False)
    
    # Reading questions
    conn_read = get_connection()
    c_read = conn_read.cursor()
    print('reading questions')
    ques = c_read.execute('''SELECT * FROM questions''')
    print("reading done")
    print("results:::::",ques)
    questions = ques.fetchall()
    conn_read.close() 

    # Initialize selections in session state if not already present
    if 'quiz_selections' not in st.session_state:
        st.session_state.quiz_selections = [None] * 34

    # Add instructions before the form
    st.markdown("""
        <div style='background: rgba(224, 176, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h4 style='color: #6c5ce7; margin-bottom: 10px;'>Instructions:</h4>
            <ul style='color: #666; margin-left: 20px;'>
                <li>Select one option for each question</li>
                <li>All questions must be answered to submit</li>
                <li>Your responses will help generate personalized career recommendations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Use a unique key for the form
    with st.form("quiz_form_" + str(st.session_state.user_id)):
        # Display questions without sections
        for i, question in enumerate(questions[:34]):
            # Use a unique key for each radio button
            key = f"question_{i}_{st.session_state.user_id}"
            selection = st.radio(
                f"{question[1]}", 
                [question[3], question[4], question[5], question[6]], 
                key=key,
                index=None  # This ensures no default selection
            )
            st.session_state.quiz_selections[i] = selection
            
        # Add submit button with custom styling
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(
            "Submit Quiz",
            use_container_width=True
        )

        # Rest of your existing submit logic...
        print("submit button", submit_button)
        if submit_button:
            st.session_state.submit = True
            selections = st.session_state.quiz_selections
            
            if None in selections:
                st.error("Please answer all questions.")
            else:
                st.success("Thank you for completing the quiz!")
                
                score = 0
                skill_score = []
                for i in range(34):
                    if i % 2 == 0 and i != 0:
                        skill_score.append(score)
                        score = 0
                    if selections[i] == questions[i][3]:
                        score += questions[i][7]
                    elif selections[i] == questions[i][4]:
                        score += questions[i][8]
                    elif selections[i] == questions[i][5]:  
                        score += questions[i][9]
                    elif selections[i] == questions[i][6]:
                        score += questions[i][10]
                skill_score.append(score)

                userid = st.session_state.user_id

                # Save the scores to the database           
                conn = get_connection()
                c = conn.cursor()
                c.execute(""" select * from quiz_scores where user_id = ? """, (userid,))
                entry_check = c.fetchone()
                if entry_check:
                    print("updating")
                    c.execute('''UPDATE quiz_scores SET 
                        "Database_Fundamentals" = ?, "Computer_Architecture" = ?, 
                        "Distributed_Computing_Systems" = ?, "Cyber_Security" = ?, 
                        "Networking" = ?, "Development" = ?, "Programming_Skills" = ?, 
                        "Project_Management" = ?, "Computer_Forensics_Fundamentals" = ?, 
                        "Technical_Communication" = ?, "AI_ML" = ?, "Software_Engineering" = ?, 
                        "Business_Analysis" = ?, "Communication_Skills" = ?, "Data_Science" = ?, 
                        "Troubleshooting_Skills" = ?, "Graphics_Designing" = ? 
                        WHERE user_id = ?''', (*skill_score, userid))
                    st.info("Your quiz results have been updated!")
                else:
                    c.execute('''INSERT INTO quiz_scores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                            (userid, *skill_score))
                    st.info("Your quiz results have been saved!")
                conn.commit()
                conn.close()

