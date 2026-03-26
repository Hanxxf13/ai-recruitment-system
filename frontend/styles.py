import streamlit as st

def inject_premium_css():
    """
    Injects a premium, modern design system using glassmorphism and tailored colors.
    """
    st.markdown("""
    <style>
    /* CSS Variables for a cohesive theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #2af598 0%, #009efd 100%);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-color: #f8f9fa;
    }

    /* Modern font and background */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    .stApp {
        font-family: 'Outfit', sans-serif;
    }

    /* Glassmorphism containers */
    div.stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4);
    }

    /* Custom Cards */
    .job-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    
    .job-card:hover {
        transform: scale(1.01);
        background: rgba(255, 255, 255, 0.08);
    }

    /* Metric refinement */
    [data-testid="stMetricValue"] {
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        border-bottom: 1px solid var(--glass-border) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def card(title, content, footer=""):
    st.markdown(f"""
    <div class="job-card">
        <h3>{title}</h3>
        <p>{content}</p>
        <div style="font-size: 0.8rem; opacity: 0.7;">{footer}</div>
    </div>
    """, unsafe_allow_html=True)
