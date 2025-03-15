import streamlit as st
import sqlite3

def display_quiz():
    # Create a selectbox for page navigation
    def get_connection():
        return sqlite3.connect('temp/TWF.db', check_same_thread=False)
    print("-------------------------------------------------------------")
    # Reading questions
    conn_read = get_connection()
    c_read = conn_read.cursor()
    print('reading questions')
    res = c_read.execute('''SELECT * FROM questionss''')
    print("reading done")
    print(res)
    questions = res.fetchall()
    conn_read.close() 

    # Use a unique key for the form
    with st.form("quiz_form_" + str(st.session_state.user_id) + "_" + str(st.session_state.get('form_counter', 0))):
        st.title("Technical Skills Quiz")
        selections = []
        for question in questions[:34]:
            selections.append(st.radio(f"{question[1]}", [question[3], question[4], question[5], question[6]], index=0))
        submit_button = st.form_submit_button("Submit")
    if submit_button:
        if None in selections:
            st.error("please answer all questions.")
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
                    # print('question:', questions[i][7])
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
                st.session_state.result_stage='load'
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
                st.session_state.result_stage='load'
            conn.commit()
            conn.close()
    # Increment the form counter
    st.session_state.form_counter = st.session_state.get('form_counter', 0) + 1

display_quiz()