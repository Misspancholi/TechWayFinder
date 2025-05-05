import streamlit as st

def show_roadmaps():
    st.markdown("<div class='navbar'>🗺️ Career Roadmaps</div>", unsafe_allow_html=True)
    
    roadmaps = {
        "Development & Testing": {
            "Software Developer": "C:/Users/kanis/TechWayFinder/temp/software_dev.txt",  
            "Software Tester": "C:/Users/kanis/TechWayFinder/temp/software_tester.txt"
        },
        "Data & AI": {
            "Data Scientist": "C:/Users/kanis/TechWayFinder/temp/data_sci.txt", 
            "AI ML Specialist": "C:/Users/kanis/TechWayFinder/temp/AI_ML.txt",  
            "Database Administrator": "C:/Users/kanis/TechWayFinder/temp/DBA.txt"
        },
        "Infrastructure & Security": {
            "Cyber Security Specialist": "C:/Users/kanis/TechWayFinder/temp/cyb_sec.txt",
            "Information Security Specialist": "C:/Users/kanis/TechWayFinder/temp/IS_specialist.txt",
            "Networking Engineer": "C:/Users/kanis/TechWayFinder/temp/network_eng.txt",
            "Hardware Engineer": "C:/Users/kanis/TechWayFinder/temp/hardware_eng.txt"
        },
        "Management & Support": {
            "Business Analyst": "C:/Users/kanis/TechWayFinder/temp/business_analyst.txt"
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

