import streamlit as st
import webbrowser

def show_roadmaps():
    st.markdown("<div class='navbar'>🗺️ Career Roadmaps</div>", unsafe_allow_html=True)
    
    roadmaps = {
        "Development & Testing": {
            "Software Developer": "https://roadmap.sh/full-stack",  # Fixed typo in URL
            "API Integration Specialist": "https://roadmap.sh/backend",
            "Software Tester": "https://roadmap.sh/qa",
        },
        "Data & AI": {
            "Data Scientist": "https://roadmap.sh/ai-data-scientist",
            "AI ML Specialist": "https://roadmap.sh/ai-data-scientist",
            "Database Administrator": "https://roadmap.sh/postgresql-dba",
        },
        "Infrastructure & Security": {
            "Cyber Security Specialist": "https://roadmap.sh/cyber-security",
            "Information Security Specialist": "https://roadmap.sh/cyber-security",
            "Networking Engineer": "https://roadmap.sh/devops",
            "Hardware Engineer": "https://roadmap.sh/computer-science",
        },
        "Management & Support": {
            "Project Manager": "https://roadmap.sh/project-manager",
            "Business Analyst": "https://roadmap.sh/business-analyst",
            "Technical Writer": "https://roadmap.sh/technical-writer",
            "Application Support Engineer": "https://roadmap.sh/devops",
            "Helpdesk Engineer": "https://roadmap.sh/devops",
            "Customer Service Executive": "https://roadmap.sh/software-design-architecture",
            "Graphics Designer": "https://roadmap.sh/design-system"
        }
    }

    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #333;'>Choose Your Career Path</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for different categories
    tabs = st.tabs(list(roadmaps.keys()))

    # Display roadmaps in each tab
    for tab_idx, (tab, (category, paths)) in enumerate(zip(tabs, roadmaps.items())):
        with tab:
            st.markdown(f"### {category} Paths", help=f"Explore {category} career paths")
            
            for i in range(0, len(paths), 2):
                col1, col2 = st.columns(2)
                colors = ['#6c5ce7', '#E0B0FF']
                
                # First item
                path_name = list(paths.keys())[i]
                path_url = list(paths.values())[i]
                card_color = colors[i % 2]
                with col1:
                    st.markdown(f"""
                        <div style='
                            background-color: {card_color};
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            margin: 10px 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            transition: transform 0.3s ease;
                        '>
                            <h4 style='color: white; margin: 0;'>{path_name}</h4>
                            <a href='{path_url}' target='_blank' style='
                                display: inline-block;
                                margin-top: 10px;
                                padding: 8px 16px;
                                background-color: white;
                                color: {card_color};
                                text-decoration: none;
                                border-radius: 5px;
                                font-weight: 500;
                            '>View Roadmap</a>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Second item (if exists)
                if i + 1 < len(paths):
                    path_name = list(paths.keys())[i + 1]
                    path_url = list(paths.values())[i + 1]
                    card_color = colors[(i + 1) % 2]
                    with col2:
                        st.markdown(f"""
                            <div style='
                                background-color: {card_color};
                                padding: 20px;
                                border-radius: 10px;
                                text-align: center;
                                margin: 10px 0;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                transition: transform 0.3s ease;
                            '>
                                <h4 style='color: white; margin: 0;'>{path_name}</h4>
                                <a href='{path_url}' target='_blank' style='
                                    display: inline-block;
                                    margin-top: 10px;
                                    padding: 8px 16px;
                                    background-color: white;
                                    color: {card_color};
                                    text-decoration: none;
                                    border-radius: 5px;
                                    font-weight: 500;
                                '>View Roadmap</a>
                            </div>
                        """, unsafe_allow_html=True)

    # Updated styling with purple and pink theme
    st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] {
                gap: 20px;
                justify-content: center;
                background-color: #f0f2f6;
                padding: 10px;
                border-radius: 10px;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                padding: 0 20px;
                background: linear-gradient(135deg, #6c5ce7, #E0B0FF);
                border-radius: 5px;
                color: white !important;
                font-weight: 500;
                border: none;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background: linear-gradient(135deg, #5849c4, #D1A1F0);
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #5849c4, #D1A1F0) !important;
                border-bottom: 3px solid white;
            }
            
            .stButton button {
                width: 100%;
                background: linear-gradient(135deg, #6c5ce7, #E0B0FF) !important;
                color: white !important;
                border: none !important;
                padding: 0.75rem !important;
                margin-top: 10px;
                border-radius: 5px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stButton button:hover {
                background: linear-gradient(135deg, #5849c4, #D1A1F0) !important;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }

            .stTabs [data-baseweb="tab-panel"] {
                padding: 20px 0;
            }

            h3 {
                color: #333;
                margin-bottom: 20px;
                text-align: center;
            }

            /* Hover effect for cards */
            div[style*="background-color"] {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            div[style*="background-color"]:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }

            /* Navbar gradient */
            .navbar {
                background: linear-gradient(135deg, #6c5ce7, #E0B0FF);
                padding: 15px;
                text-align: center;
                color: white;
                font-size: 24px;
                font-weight: 600;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

