import streamlit as st

def inject_premium_css():
    """
    Injects a premium, modern design system using glassmorphism and tailored colors.
    """
    st.markdown("""
    <style>
    /* CSS Variables for a cohesive theme */
    :root {
        --primary-gold: linear-gradient(135deg, #C5A059 0%, #F1D28C 100%);
        --accent-gold: #D4AF37;
        --pure-black: #000000;
        --obsidian: #0A0A0A;
        --glass-white: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(197, 160, 89, 0.2);
    }

    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Amiri:wght@700&display=swap');
    
    .stApp {
        background: var(--pure-black);
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(197, 160, 89, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(197, 160, 89, 0.05) 0%, transparent 40%);
        font-family: 'Outfit', sans-serif;
        color: #E2E2E2;
    }

    .nukhba-logo {
        font-family: 'Amiri', serif;
        font-size: 5.5rem;
        font-weight: 700;
        background: var(--primary-gold);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        line-height: 0.85;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    .nukhba-subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 8px;
        color: var(--accent-gold);
        opacity: 0.8;
        margin-top: -5px;
        font-weight: 400;
        text-transform: uppercase;
    }

    /* Elite Card Design - Obsidian Edition */
    .elite-card {
        background: var(--obsidian);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }
    
    .elite-card:hover {
        transform: translateY(-5px);
        border-color: var(--accent-gold);
        box-shadow: 0 15px 50px rgba(197, 160, 89, 0.15);
    }

    /* Gold Buttons */
    div.stButton > button {
        background: var(--primary-gold);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 14px 28px;
        font-weight: 800;
        letter-spacing: 1.5px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(197, 160, 89, 0.4);
    }

    /* Metric refinement */
    [data-testid="stMetricValue"] {
        background: var(--primary-gold);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Tabs styling - Obsidian */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-gold) !important;
        border-bottom: 2px solid var(--accent-gold) !important;
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
