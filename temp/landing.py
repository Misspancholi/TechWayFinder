import streamlit as st

def show_landing_page():
    # Create a container for the header to allow for button clicks
    header_container = st.container()
    
    with header_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image("images/logo.jpg", width=100)
        with col2:
            st.markdown("<h1 class='site-title'>TechWayFinder</h1>", unsafe_allow_html=True)
        with col3:
            # Position the login button at the top right
            st.markdown("<div class='header-login-container'>", unsafe_allow_html=True)
            if st.session_state.get("authenticated", False):
                # Show dashboard button if authenticated
                if st.button("Go to Dashboard", key="header_dashboard_button"):
                    st.session_state.page = "index"
                    st.rerun()
            else:
                # Show login button if not authenticated
                if st.button("Login / Sign Up", key="header_login_button", 
                            help="Click to login or create an account"):
                    st.session_state.page = "auth"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown(
        """
        <div class='hero-section'>
            <h1 class='hero-title'>
                Find Your Perfect Tech Career Path
            </h1>
            <p class='hero-text'>
                TechWayFinder uses AI-powered assessments to match your skills and interests with the ideal tech career.
                Get personalized roadmaps, expert guidance, and resources to succeed in the tech industry.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Add a Streamlit button instead of HTML button
    if st.session_state.get("authenticated", False):
        # If authenticated, show button to go to dashboard
        if st.button("Go to Dashboard", key="start_journey_button", 
                    use_container_width=False, type="primary"):
            st.session_state.page = "index"
            st.rerun()
    else:
        # If not authenticated, show button to start journey
        if st.button("Start Your Journey", key="start_journey_button", 
                    use_container_width=False, type="primary"):
            st.session_state.page = "auth"
            st.rerun()

    # How It Works Section
    st.markdown("<h2 class='section-title'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>📝</div>
                <h3 class='feature-title'>Take the Assessment</h3>
                <p class='feature-text'>Complete our comprehensive skills assessment to evaluate your technical aptitude across various domains.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>🔍</div>
                <h3 class='feature-title'>Get Matched</h3>
                <p class='feature-text'>Our AI algorithm analyzes your responses to identify the tech careers that best match your skills and interests.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>🗺️</div>
                <h3 class='feature-title'>Follow Your Roadmap</h3>
                <p class='feature-text'>Receive personalized career roadmaps with learning resources, skill requirements, and growth opportunities.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # About Us Section
    st.markdown("<h2 class='section-title'>About Us</h2>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class='about-section'>
            <p class='about-text'>
                TechWayFinder was created by students of MLSU - Kavish Menaria & Kanishka Pancholi, with a mission to help aspiring tech professionals 
                find their ideal career path. We understand that the tech industry offers countless opportunities, but navigating this landscape 
                can be overwhelming.
            </p>
            <p class='about-text' style='margin-top: 15px;'>
                Our platform combines educational expertise with advanced AI technology to provide personalized guidance. 
                We believe everyone deserves access to quality career guidance that considers their unique skills, interests, and goals.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Features Section
    st.markdown("<h2 class='section-title'>Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>🧠</div>
                <h3 class='feature-title'>AI-Powered Assessment</h3>
                <p class='feature-text'>Our sophisticated algorithm evaluates your technical aptitude across multiple domains to identify your strengths.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>💬</div>
                <h3 class='feature-title'>Career Chat Assistant</h3>
                <p class='feature-text'>Get instant answers to your career questions from our AI assistant trained on tech industry knowledge.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>📊</div>
                <h3 class='feature-title'>Personalized Results</h3>
                <p class='feature-text'>Receive detailed career matches with percentage scores showing how well each path aligns with your profile.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col4:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>📚</div>
                <h3 class='feature-title'>Learning Resources</h3>
                <p class='feature-text'>Access curated roadmaps and learning materials to help you develop the skills needed for your chosen career.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Call to Action
    st.markdown(
        """
        <div class='cta-section'>
            <h2 class='cta-title' align='center'>
                                           Ready to Discover Your Tech Career Path?
            </h2>
            <p class='cta-title' align='center'>
            Join thousands of students and professionals who have found their ideal tech career with TechWayFinder.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Add a Streamlit button instead of HTML button
    if st.session_state.get("authenticated", False):
        # If authenticated, show button to go to dashboard
        if st.button("Go to Dashboard", key="get_started_button", 
                    use_container_width=False, type="primary"):
            st.session_state.page = "index"
            st.rerun()
    else:
        # If not authenticated, show button to get started
        if st.button("Get Started Now", key="get_started_button", 
                    use_container_width=False, type="primary"):
            st.session_state.page = "auth"
            st.rerun()
