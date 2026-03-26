import streamlit as st

def inject_premium_css():
    """
    Injects a premium, modern design system using glassmorphism and tailored colors.
    """
    st.markdown("""
    <style>
    /* CSS Variables for a cohesive theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --secondary-gradient: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        --glass-bg: rgba(15, 23, 42, 0.7);
        --glass-border: rgba(255, 255, 255, 0.1);
        --accent-glow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Amiri:wght@700&display=swap');
    
    .stApp {
        background: 
            radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
            #0f172a;
        font-family: 'Outfit', sans-serif;
    }

    .nukhba-logo {
        font-family: 'Amiri', serif;
        font-size: 5rem;
        font-weight: 700;
        background: linear-gradient(to right, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        line-height: 0.85;
    }
    
    .nukhba-subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 6px;
        opacity: 0.6;
        margin-top: -5px;
        font-weight: 300;
        text-transform: uppercase;
    }

    /* Elite Card Design */
    .elite-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: var(--accent-glow);
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .elite-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(15, 23, 42, 0.85);
    }

    /* Styled Buttons */
    div.stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
        transform: rotate(-1deg) scale(1.05);
    }

    /* Metric refinement */
    [data-testid="stMetricValue"] {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.1) !important;
        border-bottom: 2px solid #818cf8 !important;
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
