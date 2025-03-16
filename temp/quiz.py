import streamlit as st
import sqlite3

def display_quiz():
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

    # Use a unique key for the form
    with st.form("quiz_form_" + str(st.session_state.user_id)):
        st.title("Technical Skills Quiz")
        selections = []
            
        for i, question in enumerate(questions[:34]):
            # Use a unique key for each radio button
            key = f"question_{i}_{st.session_state.user_id}"
            selection = st.radio(
                f"{question[1]}", 
                [question[3], question[4], question[5], question[6]], 
                key=key
            )
            selections.append(selection)
            
        submit_button = st.form_submit_button(
            "Submit",
            use_container_width=True
        )
        print("submit button", submit_button)
        if submit_button:
            st.session_state.submit = True
            st.session_state.quiz_selections = selections
            
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
                    c.execute('''INSERT INTO quiz_scores(
                        user_id, "Database_Fundamentals", "Computer_Architecture", "Distributed_Computing_Systems",
                        "Cyber_Security", "Networking", "Development", "Programming_Skills",
                        "Project_Management", "Computer_Forensics_Fundamentals", "Technical_Communication",
                        "AI_ML", "Software_Engineering", "Business_Analysis", "Communication_Skills",
                        "Data_Science", "Troubleshooting_Skills", "Graphics_Designing"
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (userid, *skill_score))
                    st.info("Your quiz results have been saved!")
                conn.commit()

