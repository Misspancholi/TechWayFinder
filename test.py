import streamlit as st

if "question" not in st.session_state:
    st.session_state.question = 1
if "page" not in st.session_state:
    st.session_state.page = 'quiz'

def go_to_page(question):
    st.session_state.question = question


if st.session_state.question == 1:
    st.write("Question 1: What is the capital of France?")
    answer = st.radio("Select one:", ["Paris", "London", "Berlin", "Madrid"])
    st.button("Next", on_click=go_to_page, args=(2,))


if st.session_state.question == 2:
    st.write("you have sucessfully completed the quiz")
    if st.button("submit"):
        st.session_state.page = 'quiz_result'

if st.session_state.page == 'quiz_result':
    st.balloons()
    st.write("you passed the test.")