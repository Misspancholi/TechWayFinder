import streamlit as st
import sqlite3
import pandas as pd

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def fetch_all_data(conn, table_name):
    query = f"SELECT * FROM {table_name};"
    cursor = conn.execute(query)
    return cursor.fetchall(), [description[0] for description in cursor.description]

def main():
    st.title("Fetch Data from SQLite")

    # Create a connection to the SQLite database
    conn = create_connection("test.db")

    try:
        # Fetch all data from the specified table
        data, columns = fetch_all_data(conn, "form_data")

        # Check if data is retrieved
        if data:
            # Create a DataFrame using the fetched data and column names
            df = pd.DataFrame(data, columns=columns)
            st.write(df)  # Display the DataFrame in Streamlit
        else:
            st.write("No data found in the table.")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()