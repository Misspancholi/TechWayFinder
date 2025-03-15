import streamlit as st
import sqlite3

def create_table():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS form_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_data(name):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO form_data (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def main():
    st.title("Form Submission to Database")
    create_table()
    
    name = st.text_input("Enter your name")
    
    if st.button("Submit"):
        if name:
            insert_data(name)
            st.success(f"Data saved successfully: {name}")
        else:
            st.error("Please enter a name")
    
if __name__ == "__main__":
    main()
