import streamlit as st
import os
import base64
from temp.roadmap_pages import show_roadmap_page, get_roadmap_details
from temp.sidebar import show_sidebar

def show_roadmaps():
    # Show sidebar
    show_sidebar()
    
    # Check if we need to show a specific roadmap
    if "current_roadmap" in st.session_state and st.session_state.current_roadmap:
        roadmap_name = st.session_state.current_roadmap
        roadmap_details = get_roadmap_details()
        if roadmap_name in roadmap_details:
            # Don't call show_roadmap_page directly, instead render the content here
            # to avoid calling show_sidebar() twice
            
            # Get base64 encoded image for background
            def get_base64_from_file(file_path):
                with open(file_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
                    
            bg_image = get_base64_from_file("images/pixel1.jpg")

            # Create the background container with CSS
            st.markdown(f"""
                <style>
                .roadmap-header {{
                    text-align: center;
                    padding: 40px 0;
                    background-image: url("data:image/jpeg;base64,{bg_image}");
                    background-size: cover;
                    background-position: center;
                    position: relative;
                    border-radius: 15px;
                    margin-bottom: 20px;
                    overflow: hidden;
                }}
                .roadmap-header:before {{
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(255, 255, 255, 0.6);  /* Adjust opacity here (0.0 to 1.0) */
                    backdrop-filter: blur(3px);  /* Adjust blur amount here */
                    -webkit-backdrop-filter: blur(3px);  /* Same value as above for Safari */
                }}
                .roadmap-header-content {{
                    position: relative;
                    z-index: 1;
                }}
                .roadmap-title {{
                    color: #333;
                    font-weight: 700;
                }}
                .roadmap-subtitle {{
                    color: #666;
                }}
                </style>
            """, unsafe_allow_html=True)

            # Create the header with separate HTML
            st.markdown(f"""
                <div class="roadmap-header">
                    <div class="roadmap-header-content">
                        <h1 class="roadmap-title">{roadmap_name}</h1>
                        <p class="roadmap-subtitle">Comprehensive career path and skill development guide</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Main content
            col1, col2 = st.columns([7, 3])
            
            with col1:
                # Display the roadmap content
                file_path = roadmap_details[roadmap_name]
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                    # Split content into sections based on emoji headers
                    sections = content.split('🎯')
                    
                    if len(sections) > 1:
                        # Display intro (content before first 🎯)
                        st.markdown(sections[0])
                        
                        # Display each stage with proper formatting
                        for section in sections[1:]:
                            st.markdown(f"🎯{section}")
                            st.markdown("---")
                    else:
                        # If no sections found, display the whole content
                        st.markdown(content)
                        
                except FileNotFoundError:
                    st.error(f"Roadmap file not found: {file_path}")
                except Exception as e:
                    st.error(f"Error loading roadmap: {str(e)}")
            
            with col2:
                # Sidebar with related resources
                st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1));
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    '>
                        <h3>Related Resources</h3>
                        <ul>
                            <li><a href="https://roadmap.sh" target="_blank">Interactive Roadmaps</a></li>
                            <li><a href="https://github.com/kamranahmedse/developer-roadmap" target="_blank">GitHub Resources</a></li>
                            <li><a href="https://www.coursera.org" target="_blank">Online Courses</a></li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add additional resources section
                st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(224, 176, 255, 0.1));
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    '>
                        <h3>Learning Tips</h3>
                        <ul>
                            <li>Focus on one skill at a time</li>
                            <li>Build projects to apply your knowledge</li>
                            <li>Join communities related to this field</li>
                            <li>Follow industry experts on social media</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            # Back button
            if st.button("Back to Roadmaps", key="back_to_roadmaps_btn"):
                # Clear the current roadmap from session state
                if "current_roadmap" in st.session_state:
                    del st.session_state.current_roadmap
                st.rerun()
                
            return
        else:
            # Reset if invalid roadmap
            if "current_roadmap" in st.session_state:
                del st.session_state.current_roadmap
    
    # For the main roadmaps listing page
    else:
        # Get base64 encoded image for background
        def get_base64_from_file(file_path):
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
            
        bg_image = get_base64_from_file("images/pixel1.jpg")
        
        # Create the background container with CSS
        st.markdown(f"""
            <style>
            .roadmap-header {{
                text-align: center;
                padding: 40px 0;
                background-image: url("data:image/jpeg;base64,{bg_image}");
                background-size: cover;
                background-position: center;
                position: relative;
                border-radius: 15px;
                margin-bottom: 20px;
                overflow: hidden;
            }}
            .roadmap-header:before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(3px);
                -webkit-backdrop-filter: blur(10px);
            }}
            .roadmap-header-content {{
                position: relative;
                z-index: 1;
            }}
            .roadmap-title {{
                color: #333;
                font-weight: 700;
            }}
            .roadmap-subtitle {{
                color: #666;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Create the header with separate HTML
        st.markdown(f"""
            <div class="roadmap-header">
                <div class="roadmap-header-content">
                    <h1 class="roadmap-title">🗺️ Career Roadmaps</h1>
                    <p class="roadmap-subtitle">Explore learning paths for different tech roles</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    roadmaps = {
        "Development & Testing": {
            "Software Developer": "temp/software_dev.txt",  
            "Software Tester": "temp/software_tester.txt"
        },
        "Data & AI": {
            "Data Scientist": "temp/data_sci.txt", 
            "AI ML Specialist": "temp/AI_ML.txt",  
            "Database Administrator": "temp/DBA.txt"
        },
        "Infrastructure & Security": {
            "Cyber Security Specialist": "temp/cyb_sec.txt",
            "Information Security Specialist": "temp/IS_specialist.txt",
            "Networking Engineer": "temp/network_eng.txt",
            "Hardware Engineer": "temp/hardware_eng.txt"
        },
        "Management & Support": {
            "Business Analyst": "temp/business_analyst.txt"
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
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View {path_name} Roadmap", key=f"btn_{category}_{i}"):
                        st.session_state.current_roadmap = path_name
                        st.rerun()
                
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
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"View {path_name} Roadmap", key=f"btn_{category}_{i+1}"):
                            st.session_state.current_roadmap = path_name
                            st.rerun()

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
                background: linear-gradient(135deg, #   5849c4, #D1A1F0) !important;
                border-bottom: 3px solid white;
            }
            
            /* Other styles remain the same */
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

    
