import streamlit as st
import pickle
import numpy as np
import sqlite3

def results():
    if "result_stage" not in st.session_state:
        st.session_state.result_stage = "load"
        
    if st.session_state.result_stage == "load":
        print("result loading ------------------")
        conn = sqlite3.connect("temp/TWF.db")
        c = conn.cursor()
        c.execute("select * from quiz_scores where user_id == ?", (st.session_state.user_id,))
        
        result = c.fetchone()
        if result:
            st.session_state.quiz_results = result[1:18]
            print(st.session_state.quiz_results)
            st.session_state.result_stage = "pred"
        else:
            st.warning("result not found please try quiz first")
        conn.close()
        # st.session_state.result_stage = "pred"
    if st.session_state.result_stage == "pred":
        with open("model/trained_knn_model.sav", "rb") as model_file:
            model = pickle.load(model_file)
        model.feature_names_in_ = None
        data = np.array(st.session_state.quiz_results).reshape(1, -1)

        proba = model.predict_proba(data)
        top_3_indices = np.argsort(proba, axis=1)[:, -3:]
        st.session_state.predictions = [(model.classes_[i], proba[0][i]) for i in top_3_indices[0]]
        st.session_state.result_stage = "show"

    if st.session_state.result_stage == "show":
        print("predictions are:")
        print(f"{st.session_state.predictions[2][0]}\n{st.session_state.predictions[1][0]}\n{st.session_state.predictions[0][0]}")
        st.write(st.session_state.predictions)
    