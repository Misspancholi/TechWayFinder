import streamlit as st

def show_roadmaps():
    st.markdown("<div class='navbar'>🗺️ Career Roadmaps</div>", unsafe_allow_html=True)
    
    # Define roadmap data
    roadmaps = {
        "Software Development": {
            "Frontend Developer": "https://roadmap.sh/frontend",
            "Backend Developer": "https://roadmap.sh/backend",
            "Full Stack Developer": "https://roadmap.sh/full-stack",
            "DevOps Engineer": "https://roadmap.sh/devops",
        },
        "Data Science & AI": {
            "Data Scientist": "https://roadmap.sh/ai-data-scientist",
            "Machine Learning Engineer": "https://roadmap.sh/ai-ml",
            "Data Engineer": "https://roadmap.sh/data-engineer",
        },
        "Cybersecurity": {
            "Security Engineer": "https://roadmap.sh/cyber-security",
            "Penetration Tester": "https://roadmap.sh/pen-tester",
            "Security Analyst": "https://roadmap.sh/security-analyst",
        },
        "Cloud Computing": {
            "Cloud Engineer": "https://roadmap.sh/cloud-engineer",
            "AWS Developer": "https://roadmap.sh/aws",
            "Azure Developer": "https://roadmap.sh/azure",
        }
    }

    # Add JavaScript for handling clicks
    st.markdown("""
        <script>
            function openRoadmap(url) {
                window.open(url, '_blank');
            }
        </script>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='roadmaps-container'>
            <h1 style='text-align: center; margin-bottom: 30px;'>Choose Your Career Path</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for different categories
    tabs = st.tabs(list(roadmaps.keys()))

    # Display roadmaps for each category
    for tab_idx, (category, paths) in enumerate(roadmaps.items()):
        with tabs[tab_idx]:
            st.markdown(f"### {category} Paths")
            
            # Create columns for roadmap cards
            for role, link in paths.items():
                # Create a clickable button for each roadmap
                if st.button(f"📚 {role}", key=f"btn_{category}_{role}", use_container_width=True):
                    st.markdown(f'<script>window.open("{link}", "_blank");</script>', unsafe_allow_html=True)
                    # Provide a manual link as fallback
                    st.markdown(f"[Click here if the roadmap doesn't open automatically]({link})")

    # Add custom CSS for roadmaps page
    st.markdown("""
        <style>
        .roadmaps-container {
            padding: 20px;
            margin-bottom: 30px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            gap: 10px;
            padding: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.1);
        }
        /* Style for roadmap buttons */
        .stButton button {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 15px;
            margin: 5px 0;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
