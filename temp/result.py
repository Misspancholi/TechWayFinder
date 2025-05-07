import streamlit as st
import pickle
import numpy as np
import sqlite3
import base64

def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def load_css(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def get_roadmap_link(career):
    # Instead of external links, we'll use internal navigation
    # This will set the current_roadmap in session state
    return f"javascript:setRoadmap('{career}')"

def check_eligibility(user_id):
    conn = sqlite3.connect('temp/TWF.db', check_same_thread=False)
    c = conn.cursor()
    
    # Check if user_profile table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profile'")
    if not c.fetchone():
        conn.close()
        return False, None
    
    # Check if user has filled the profile form
    c.execute("SELECT * FROM user_profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    
    if not profile:
        return False, None
    
    # Check if user has an eligible qualification
    eligible_qualifications = ["BCA", "MCA", "B.Tech", "M.Tech", "Ph.D.", "Other(related to IT)"]
    # Assuming qualification is stored in the second column (index 1)
    return True, profile[1] in eligible_qualifications

def check_quiz_taken(user_id):
    conn = sqlite3.connect('temp/TWF.db', check_same_thread=False)
    c = conn.cursor()
    
    # Check if quiz_scores table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_scores'")
    if not c.fetchone():
        conn.close()
        return False
    
    # Check if user has quiz scores
    c.execute("SELECT * FROM quiz_scores WHERE user_id = ?", (user_id,))
    scores = c.fetchone()
    conn.close()
    
    return scores is not None

def results():
    # Load CSS
    st.markdown(f"<style>{load_css('static/results_styles.css')}</style>", unsafe_allow_html=True)
    
    # Check eligibility first
    profile_completed, has_eligible_qualification = check_eligibility(st.session_state.user_id)
    
    if not profile_completed:
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 30px;'>
                <img src='data:image/jpeg;base64,{get_base64_from_file("images/logo.jpg")}' style='width: 150px; margin-bottom: 20px;'>
                <div style='background: linear-gradient(135deg, rgba(255, 99, 71, 0.1), rgba(255, 99, 71, 0.2)); 
                            padding: 20px; border-radius: 15px; margin: 20px 0;'>
                    <h1 style='color: #ff6347; font-family: Montserrat, sans-serif; margin-bottom: 15px;'>
                        Profile Required
                    </h1>
                    <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1.1em; margin-bottom: 10px;'>
                        Before viewing quiz results, you need to complete your profile.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Complete Your Profile", use_container_width=True, type="primary"):
            st.session_state.page = "profile"
            st.rerun()
            
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.page = "index"
            st.rerun()
            
        return
    
    # Check if user has eligible qualification
    # if not has_eligible_qualification:
    #     st.markdown(f"""
    #         <div style='text-align: center; margin-bottom: 30px;'>
    #             <img src='data:image/jpeg;base64,{get_base64_from_file("images/logo.jpg")}' style='width: 150px; margin-bottom: 20px;'>
    #             <div style='background: linear-gradient(135deg, rgba(255, 184, 0, 0.1), rgba(255, 184, 0, 0.2)); 
    #                         padding: 20px; border-radius: 15px; margin: 20px 0;'>
    #                 <h1 style='color: #ff9800; font-family: Montserrat, sans-serif; margin-bottom: 15px;'>
    #                     Qualification Requirement
    #                 </h1>
    #                 <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1.1em; margin-bottom: 10px;'>
    #                     The quiz is designed for users with IT-related qualifications.
    #                 </p>
    #                 <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1em;'>
    #                     Eligible qualifications: BCA, MCA, B.Tech, M.Tech, Ph.D., or other IT-related degrees.
    #                 </p>
    #             </div>
    #         </div>
    #     """, unsafe_allow_html=True)
        
    #     if st.button("Update Your Profile", use_container_width=True, type="primary"):
    #         st.session_state.page = "profile"
    #         st.rerun()
            
    #     if st.button("Back to Dashboard", use_container_width=True):
    #         st.session_state.page = "index"
    #         st.rerun()
            
    #     return
    
    # Check if quiz has been taken
    if not check_quiz_taken(st.session_state.user_id):
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 30px;'>
                <img src='data:image/jpeg;base64,{get_base64_from_file("images/logo.jpg")}' style='width: 150px; margin-bottom: 20px;'>
                <div style='background: linear-gradient(135deg, rgba(255, 184, 0, 0.1), rgba(255, 184, 0, 0.2)); 
                            padding: 20px; border-radius: 15px; margin: 20px 0;'>
                    <h1 style='color: #ff9800; font-family: Montserrat, sans-serif; margin-bottom: 15px;'>
                        Quiz Required
                    </h1>
                    <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1.1em; margin-bottom: 10px;'>
                        You need to complete the technical skills assessment quiz before viewing results.
                    </p>
                    <p style='color: #666; font-family: Poppins, sans-serif; font-size: 1em;'>
                        The quiz helps us analyze your skills and provide personalized career recommendations.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Take Quiz Now", use_container_width=True, type="primary"):
            st.session_state.page = "quiz"
            st.rerun()
            
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.page = "index"
            st.rerun()
            
        return
    
    # Original results code continues here
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

        # Add JavaScript function to set roadmap and trigger navigation
        st.markdown("""
            <script>
            function setRoadmap(roadmapName) {
                // Use Streamlit's postMessage to communicate with Python
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: roadmapName,
                    dataType: "string",
                    key: "selected_roadmap"
                }, "*");
            }
            </script>
        """, unsafe_allow_html=True)

        # Create a hidden component to receive the selected roadmap
        selected_roadmap = st.empty()
        if selected_roadmap := st.session_state.get("selected_roadmap"):
            st.session_state.current_roadmap = selected_roadmap
            st.session_state.page = "roadmaps"
            st.rerun()

        # Display top 3 predictions with roadmap links
        for i, (career, _) in enumerate(reversed(st.session_state.predictions)):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            roadmap_link = get_roadmap_link(career)
            
            st.markdown(f"""
                <div class='career-card'>
                    <div class='career-content'>
                        <h2>{medal} {career}</h2>
                        <a href='{roadmap_link}' class='roadmap-button'>
                            View Career Roadmap →
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Add button for direct navigation as a fallback
        for i, (career, _) in enumerate(reversed(st.session_state.predictions)):
            if st.button(f"View {career} Roadmap", key=f"roadmap_btn_{i}"):
                st.session_state.current_roadmap = career
                st.session_state.page = "roadmaps"
                st.rerun()

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
    
