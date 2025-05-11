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
    """
    This function is now deprecated and should not be used directly.
    The functionality has been moved into show_roadmaps() to avoid duplicate sidebar calls.
    """
    # This is now just a placeholder to maintain compatibility
    # The actual implementation has been moved to show_roadmaps()
    st.warning("This function is deprecated. Please update your code to use the new implementation.")
    pass

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


