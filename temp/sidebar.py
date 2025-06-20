import streamlit as st
import sqlite3

def get_user_info(user_id):
    """Get user information from database"""
    conn = sqlite3.connect("temp/TWF.db")
    c = conn.cursor()
    c.execute("SELECT name, email FROM users WHERE user_id = ?", (user_id,))
    user_info = c.fetchone()
    conn.close()

    if user_info:
        return {"name": user_info[0], "email": user_info[1]}
    return {"name": "Guest", "email": ""}

def generate_profile_picture(name):
    """Generate a profile picture with the first letter of the name"""
    if not name or name == "Guest":
        initial = "G"
    else:
        initial = name[0].upper()

    # Color palette for profile pictures
    colors = [
        "#6c5ce7", "#a29bfe", "#fd79a8", "#fdcb6e",
        "#e17055", "#00b894", "#00cec9", "#0984e3",
        "#6c5ce7", "#a29bfe", "#fd79a8", "#e84393"
    ]

    # Use the first letter to determine color consistently
    color_index = ord(initial) % len(colors)
    bg_color = colors[color_index]

    # Generate SVG for the profile picture
    svg = f"""
    <svg width="50" height="50" xmlns="http://www.w3.org/2000/svg" style="border-radius: 50%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">
        <circle cx="25" cy="25" r="25" fill="{bg_color}"/>
        <text x="25" y="32" font-family="Montserrat, sans-serif" font-size="20"
              font-weight="600" fill="white" text-anchor="middle">{initial}</text>
    </svg>
    """
    return svg

def show_sidebar():
    """Display common sidebar with user info and navigation"""
    with st.sidebar:
        # User info section
        if st.session_state.get("authenticated", False):
            user_info = get_user_info(st.session_state.user_id)
            profile_pic_svg = generate_profile_picture(user_info['name'])

            # Display profile section with picture
            st.markdown("### User Profile")

            # Create columns for profile layout
            col1, col2 = st.columns([1, 2])

            with col1:
                # Display profile picture
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                        {profile_pic_svg}
                """, unsafe_allow_html=True)

            with col2:
                # Display user info
                st.markdown(f"""
                    <div style="padding-left: 5px;">
                        <div style="font-family: 'Montserrat', sans-serif; font-weight: 600;
                                    font-size: 14px; color: #333; margin-bottom: 4px;">
                            {user_info['name']}
                        </div>
                        <div style="font-family: 'Poppins', sans-serif; font-weight: 400;
                                    font-size: 11px; color: #666;">
                            {user_info['email']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.divider()
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Common navigation buttons with unique keys based on current page
        current_page = st.session_state.page
        
        # Dashboard button - disabled if already on dashboard
        if st.button("Dashboard", 
                    key=f"sidebar_dashboard_{current_page}", 
                    disabled=(current_page == "index")):
            st.session_state.page = "index"
            st.rerun()
            
        # Profile button - disabled if already on profile
        if st.button("Profile", 
                    key=f"sidebar_profile_{current_page}", 
                    disabled=(current_page == "profile")):
            st.session_state.page = "profile"
            st.rerun()
            
        # Homepage button - disabled if already on landing
        if st.button("Back to Homepage", 
                    key=f"sidebar_homepage_{current_page}", 
                    disabled=(current_page == "landing")):
            st.session_state.page = "landing"
            st.rerun()
            
        if st.session_state.get("authenticated", False):
            if st.button("Logout", 
                        key=f"sidebar_logout_{current_page}"):
                st.session_state.page = "auth"
                st.session_state.authenticated = False
                st.rerun()

