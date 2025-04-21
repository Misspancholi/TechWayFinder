import streamlit as st
import pickle
import numpy as np
import sqlite3

def get_roadmap_link(career):
    roadmap_links = {
        "Frontend Developer": "https://roadmap.sh/frontend",
        "Backend Developer": "https://roadmap.sh/backend",
        "Full Stack Developer": "https://roadmap.sh/full-stack",
        "DevOps Engineer": "https://roadmap.sh/devops",
        "Data Scientist": "https://roadmap.sh/ai-data-scientist",
        "Machine Learning Engineer": "https://roadmap.sh/ai-ml",
        "Data Engineer": "https://roadmap.sh/data-engineer",
        "Security Engineer": "https://roadmap.sh/cyber-security",
        "Penetration Tester": "https://roadmap.sh/pen-tester",
        "Security Analyst": "https://roadmap.sh/security-analyst",
        "Cloud Engineer": "https://roadmap.sh/cloud-engineer",
        "AWS Developer": "https://roadmap.sh/aws",
        "Azure Developer": "https://roadmap.sh/azure"
    }
    return roadmap_links.get(career, "#")

def results():
    if "result_stage" not in st.session_state:
        st.session_state.result_stage = "load"
        
    if st.session_state.result_stage == "load":
        st.markdown("""
            <div class='loading-container'>
                <div class='loading-spinner'></div>
                <p>Analyzing your responses...</p>
            </div>
        """, unsafe_allow_html=True)
        
        conn = sqlite3.connect("temp/TWF.db")
        c = conn.cursor()
        c.execute("select * from quiz_scores where user_id == ?", (st.session_state.user_id,))
        
        result = c.fetchone()
        if result:
            st.session_state.quiz_results = result[1:18]
            st.session_state.result_stage = "pred"
        else:
            st.warning("⚠️ No results found. Please complete the quiz first!")
        conn.close()

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
        st.markdown("""
            <div class='results-container'>
                <h2>🎯 Your Career Match Results</h2>
                <p class='subtitle'>Based on your responses, here are your top career matches:</p>
            </div>
        """, unsafe_allow_html=True)

        # Display top 3 predictions with progress bars and roadmap links
        for i, (career, probability) in enumerate(reversed(st.session_state.predictions)):
            percentage = round(probability * 100, 1)
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            
            st.markdown(f"""
                <div class='career-card'>
                    <div class='career-header'>
                        <h3>{medal} {career}</h3>
                        <!--<span class='percentage'>{percentage}% Match</span> -->
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(probability)
            
            # Roadmap button
            roadmap_link = get_roadmap_link(career)
            if st.button(f"📚 View {career} Roadmap", key=f"roadmap_{i}"):
                st.markdown(f'<script>window.open("{roadmap_link}", "_blank");</script>', 
                          unsafe_allow_html=True)
                st.markdown(f"[Click here if the roadmap doesn't open automatically]({roadmap_link})")
            
            st.markdown("<br>", unsafe_allow_html=True)

        # Add custom CSS
        st.markdown("""
            <style>
            .results-container {
                text-align: center;
                margin-bottom: 2rem;
            }
            .subtitle {
                color: #888;
                font-size: 1.1em;
                margin-bottom: 2rem;
            }
            .career-card {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 1rem;
                transition: transform 0.3s ease;
            }
            .career-card:hover {
                transform: translateY(-5px);
            }
            .career-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            .career-header h3 {
                margin: 0;
                color: #E0B0FF;
            }
            .percentage {
                font-size: 1.2em;
                font-weight: bold;
                color: #4CAF50;
            }
            .loading-container {
                text-align: center;
                padding: 2rem;
            }
            .loading-spinner {
                border: 4px solid rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                border-top: 4px solid #E0B0FF;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            /* Style for roadmap buttons */
            .stButton button {
                background-color: rgba(224, 176, 255, 0.2);
                color: white;
                border: 1px solid rgba(224, 176, 255, 0.3);
                padding: 0.75rem;
                border-radius: 5px;
                transition: all 0.3s ease;
                width: 100%;
            }
            .stButton button:hover {
                background-color: rgba(224, 176, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            </style>
        """, unsafe_allow_html=True)
    
