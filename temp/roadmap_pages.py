import streamlit as st
import os
from temp.sidebar import show_sidebar

def display_roadmap_content(file_path):
    """Display the content of a roadmap file with proper formatting"""
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

def show_roadmap_page(roadmap_name, file_path):
    # Show sidebar
    show_sidebar()
    
    # Add roadmap-specific navigation
    with st.sidebar:
        if st.button("Back to Roadmaps", key="sidebar_roadmaps"):
            # Clear the current roadmap from session state
            if "current_roadmap" in st.session_state:
                del st.session_state.current_roadmap
            st.rerun()
    
    # Header section
    st.markdown(f"""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #333;'>{roadmap_name}</h1>
            <p style='color: #666;'>Comprehensive career path and skill development guide</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Display the roadmap content
        display_roadmap_content(file_path)
    
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
    
    # Back button - Fixed implementation
    if st.button("Back to Roadmaps", key="back_to_roadmaps_btn"):
        # Clear the current roadmap from session state
        if "current_roadmap" in st.session_state:
            del st.session_state.current_roadmap
        st.rerun()

def get_roadmap_details():
    """Return a dictionary of roadmap details with names and file paths"""
    return {
        "Software Developer": "roadmaps/software_dev.txt",
        "Software Tester": "roadmaps/software_tester.txt",
        "Data Scientist": "roadmaps/data_sci.txt",
        "AI ML Specialist": "roadmaps/AI_ML.txt",
        "Database Administrator": "roadmaps/DBA.txt",
        "Cyber Security Specialist": "roadmaps/cyb_sec.txt",
        "Information Security Specialist": "roadmaps/IS_specialist.txt",
        "Networking Engineer": "roadmaps/network_eng.txt",
        "Hardware Engineer": "roadmaps/hardware_eng.txt",
        "Business Analyst": "roadmaps/business_analyst.txt"
    }




