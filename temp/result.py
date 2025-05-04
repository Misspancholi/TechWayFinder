import streamlit as st
import pickle
import numpy as np
import sqlite3

def get_roadmap_link(career):
    roadmap_links = {
        "Software Developer": "https://roadmap.sh/full-stack",
        "API Integration Specialist": "https://roadmap.sh/backend",
        "Software Tester": "https://roadmap.sh/qa",
        "Data Scientist": "https://roadmap.sh/ai-data-scientist",
        "AI ML Specialist": "https://roadmap.sh/ai-data-scientist",
        "Database Administrator": "https://roadmap.sh/postgresql-dba",
        "Cyber Security Specialist": "https://roadmap.sh/cyber-security",
        "Information Security Specialist": "https://roadmap.sh/cyber-security",
        "Networking Engineer": "https://roadmap.sh/devops",
        "Hardware Engineer": "https://roadmap.sh/computer-science",
        "Project Manager": "https://roadmap.sh/project-manager",
        "Business Analyst": "https://roadmap.sh/business-analyst",
        "Technical Writer": "https://roadmap.sh/technical-writer",
        "Application Support Engineer": "https://roadmap.sh/devops",
        "Helpdesk Engineer": "https://roadmap.sh/devops",
        "Customer Service Executive": "https://roadmap.sh/software-design-architecture",
        "Graphics Designer": "https://roadmap.sh/design-system"
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
        conn.close()
        
        if result:
            st.session_state.quiz_results = result[1:18]
            st.session_state.result_stage = "pred"
            st.rerun()  # Add this to trigger the prediction stage
        else:
            st.warning("⚠️ No results found. Please complete the quiz first!")
            st.session_state.result_stage = "load"  # Reset stage if no results
            return

    if st.session_state.result_stage == "pred":
        try:
            with open("model/trained_knn_model.sav", "rb") as model_file:
                model = pickle.load(model_file)
            model.feature_names_in_ = None
            data = np.array(st.session_state.quiz_results).reshape(1, -1)

            proba = model.predict_proba(data)
            top_3_indices = np.argsort(proba, axis=1)[:, -3:]
            st.session_state.predictions = [(model.classes_[i], proba[0][i]) for i in top_3_indices[0]]
            st.session_state.result_stage = "show"
            st.rerun()  # Add this to trigger the show stage
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            st.session_state.result_stage = "load"
            return

    if st.session_state.result_stage == "show":
        st.markdown("""
            <div class='results-header'>
                <h1>Your Career Match Results</h1>
                <p>Based on your technical skills assessment, here are your recommended career paths:</p>
            </div>
        """, unsafe_allow_html=True)

        # Display top 3 predictions with roadmap links
        for i, (career, _) in enumerate(reversed(st.session_state.predictions)):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            roadmap_link = get_roadmap_link(career)
            
            st.markdown(f"""
                <div class='career-card'>
                    <div class='career-content'>
                        <h2>{medal} {career}</h2>
                        <a href='{roadmap_link}' target='_blank' class='roadmap-button'>
                            View Career Roadmap →
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Add custom CSS with improved color scheme
        st.markdown("""
            <style>
            .results-header {
                text-align: center;
                margin: 2rem 0;
                padding: 2rem;
                background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1));
                border-radius: 15px;
            }
            
            .results-header h1 {
                color: #2D3748;
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            
            .results-header p {
                color: #4A5568;
                font-size: 1.2rem;
            }
            
            .career-card {
                background: linear-gradient(135deg, #6c5ce7, #a78bfa);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1.5rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .career-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            
            .career-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .career-content h2 {
                color: white;
                margin: 0;
                font-size: 1.5rem;
            }
            
            .roadmap-button {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                text-decoration: none;
                transition: background 0.3s ease;
                font-weight: 500;
                display: inline-block;
            }
            
            .roadmap-button:hover {
                background: rgba(255, 255, 255, 0.3);
                color: white;
            }
            
            .loading-container {
                text-align: center;
                padding: 3rem;
            }
            
            .loading-spinner {
                border: 4px solid rgba(108, 92, 231, 0.1);
                border-radius: 50%;
                border-top: 4px solid #6c5ce7;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @media (max-width: 768px) {
                .career-content {
                    flex-direction: column;
                    text-align: center;
                }
                
                .roadmap-button {
                    width: 100%;
                    text-align: center;
                }
            }
            </style>
        """, unsafe_allow_html=True)
    
