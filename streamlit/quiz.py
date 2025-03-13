import streamlit as st
import sqlite3

# Create a selectbox for page navigation
conn = sqlite3.connect('streamlit\TWF.db')
c = conn.cursor()

res = c.execute('''SELECT * FROM questions''')
questions = res.fetchall()
conn.close()

# Display only the top 3 questions
with st.form("quiz"):
    selections = []
    for question in questions[:3]:
        selections.append(st.radio(f"{question[1]}", [question[3], question[4], question[5], question[6]], index=None))
    submit_button = st.form_submit_button("Submit")
if submit_button:
    if None in selections:
        st.error("please answer all questions.")
    else:
        st.success("Thank you for completing the quiz!")

        # Save the scores to the database
        c.execute('''insert into quiz_scores() values(?,?,?,?)''',)
        
