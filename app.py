import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
import time
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from utils.mirror_agent import MirrorAgent
from config import Config

# Page configuration
st.set_page_config(
    page_title="MirrorMe - AI Personality Clone",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS and JS files for advanced styling
def load_external_assets():
    """Load external CSS and JavaScript files for enhanced dark theme"""
    try:
        # Load advanced CSS
        with open('assets/advanced_styles.css', 'r') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        
        # Load dark theme enforcer JavaScript
        with open('assets/dark_theme_enforcer.js', 'r') as f:
            js_content = f.read()
        st.markdown(f'<script>{js_content}</script>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("External assets not found. Using fallback styling.")

# Load external assets
load_external_assets()

# Perfect dark theme with excellent visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* FORCE DARK THEME EVERYWHERE */
    html, body, .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #0a0a0a !important;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0a0a0a 75%, #1a1a2e 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 20s ease infinite !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh !important;
    }
    
    /* FORCE ALL CONTAINERS TO BE TRANSPARENT */
    .main, .main > div, .block-container, .stApp > div, .stApp section, 
    [data-testid="stAppViewContainer"] > div, .element-container {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* FORCE MAIN CONTENT AREA */
    .main .block-container {
        background: transparent !important;
        background-color: transparent !important;
        max-width: 1200px !important;
        padding: 1rem 2rem !important;
    }
    
    /* OVERRIDE ANY STREAMLIT DEFAULTS */
    .stApp * {
        color: inherit !important;
    }
    
    /* FORCE DARK THEME ON ALL ELEMENTS */
    div[data-testid="stAppViewContainer"], 
    div[data-testid="stHeader"], 
    section[data-testid="stSidebar"],
    .css-1d391kg {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main container - Fixed */
    .main .block-container {
        padding: 1rem 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        position: relative !important;
        background: transparent !important;
    }
    
    /* Ensure proper content containment */
    .main {
        background: transparent !important;
        overflow-x: hidden !important;
    }
    
    /* Fix any layout issues */
    .stApp [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    .stApp [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Header - Enhanced with stunning effects */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #ff6b6b 50%, #4ecdc4 75%, #667eea 100%);
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4), 0 0 30px rgba(255, 107, 107, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header:before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: rotate 8s linear infinite;
    }
    
    .main-header:after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 20px;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 2;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.8rem;
        color: #ffffff !important;
        opacity: 0.95;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 2;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* FORCE SIDEBAR DARK THEME */
    .css-1d391kg, .stSidebar, .stSidebar > div, [data-testid="stSidebar"], 
    .css-1aumxhk, section[data-testid="stSidebar"] {
        background-color: #1a1a2e !important;
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f0f1a 100%) !important;
        border-right: 2px solid rgba(102, 126, 234, 0.4) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* FORCE SIDEBAR ELEMENTS */
    .stSidebar, .stSidebar > div, .stSidebar .element-container, 
    .stSidebar .block-container, section[data-testid="stSidebar"] > div {
        background-color: transparent !important;
        background: transparent !important;
        padding: 1rem !important;
    }
    
    /* FORCE SIDEBAR TEXT COLORS */
    .stSidebar, .stSidebar *, 
    .stSidebar .stMarkdown, .stSidebar .stMarkdown *, 
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4,
    .stSidebar p, .stSidebar div, .stSidebar span, .stSidebar label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* SIDEBAR PARAGRAPH TEXT */
    .stSidebar .stMarkdown p, .stSidebar .stMarkdown div:not(.stats-card), .stSidebar .stMarkdown span {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    /* Select box styling - Enhanced fix */
    .stSelectbox {
        background: transparent !important;
    }
    
    .stSelectbox > div {
        background: transparent !important;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.95) 0%, rgba(30, 30, 60, 0.9) 100%) !important;
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stSelectbox > div > div > select {
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stSelectbox > div > div > select:focus {
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.4) !important;
        outline: none !important;
    }
    
    .stSelectbox > div > div > select option {
        background: #1a1a2e !important;
        color: #ffffff !important;
        padding: 0.5rem !important;
    }
    
    /* Select box label */
    .stSelectbox > label {
        color: #ffffff !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Select box arrow */
    .stSelectbox svg {
        fill: #ffffff !important;
    }
    
    /* Chat messages - Enhanced with stunning effects */
    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        color: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 22px 22px 6px 22px;
        margin: 1.5rem 0 1.5rem auto;
        max-width: 75%;
        animation: slideInRight 0.5s ease-out;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4), 0 0 20px rgba(255, 107, 107, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        word-wrap: break-word;
        overflow-wrap: break-word;
        font-size: 1.05rem;
        line-height: 1.6;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: slideInRight 0.5s ease-out, gradientShift 8s ease infinite;
    }
    
    .message-user:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 22px 22px 6px 22px;
        pointer-events: none;
    }
    
    .message-assistant {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 50%, #4ecdc4 100%);
        color: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 22px 22px 22px 6px;
        margin: 1.5rem auto 1.5rem 0;
        max-width: 75%;
        animation: slideInLeft 0.5s ease-out;
        box-shadow: 0 12px 30px rgba(45, 55, 72, 0.5), 0 0 20px rgba(78, 205, 196, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        word-wrap: break-word;
        overflow-wrap: break-word;
        font-size: 1.05rem;
        line-height: 1.6;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: slideInLeft 0.5s ease-out, gradientShift 10s ease infinite;
    }
    
    .message-assistant:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 22px 22px 22px 6px;
        pointer-events: none;
    }
    
    /* Input field styling - Enhanced */
    .stTextInput > div > div {
        position: relative !important;
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.9) 0%, rgba(30, 30, 60, 0.8) 100%) !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 15px !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1.1rem !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.3), 0 12px 30px rgba(102, 126, 234, 0.2) !important;
        background: linear-gradient(135deg, rgba(30, 30, 70, 0.95) 0%, rgba(40, 40, 80, 0.9) 100%) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #b0b0b0 !important;
        font-weight: 400 !important;
        transition: color 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus::placeholder {
        color: #d0d0d0 !important;
    }
    
    /* Button styling - Enhanced */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        width: 100% !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        background-size: 200% 200% !important;
        animation: gradientShift 3s ease infinite !important;
    }
    
    .stButton > button:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6), 0 0 20px rgba(255, 107, 107, 0.3) !important;
        background-position: 100% 100% !important;
    }
    
    .stButton > button:hover:before {
        left: 100% !important;
    }
    
    /* Form submit button - Enhanced */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #4ecdc4 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        width: 100% !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        background-size: 200% 200% !important;
        animation: gradientShift 3s ease infinite !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6), 0 0 20px rgba(78, 205, 196, 0.4) !important;
        background-position: 100% 100% !important;
    }
    
    /* Stats cards - Fixed and enhanced */
    .stats-card {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.95) 0%, rgba(30, 30, 60, 0.9) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stats-card:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 3px !important;
        background: linear-gradient(90deg, #667eea, #764ba2, #4ecdc4, #ff6b6b) !important;
        background-size: 200% 100% !important;
        animation: gradientShift 3s ease infinite !important;
    }
    
    .stats-card:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5), 0 0 20px rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.7) !important;
    }
    
    .stats-number {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        text-shadow: 0 2px 8px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #667eea, #4ecdc4) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .stats-label {
        font-size: 1rem !important;
        color: #ffffff !important;
        margin-top: 0.5rem !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Loading indicator - Enhanced */
    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-radius: 20px 20px 20px 6px;
        margin: 1.5rem auto 1.5rem 0;
        max-width: 75%;
        animation: slideInLeft 0.5s ease-out, pulse 2s infinite;
        border: 2px solid rgba(102, 126, 234, 0.4);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .loading-indicator:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    .loading-text {
        color: #ffffff;
        font-weight: 500;
        font-size: 1rem;
    }
    
    .loading-dots {
        display: flex;
        gap: 6px;
    }
    
    .loading-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: bounce 1.4s ease-in-out infinite both;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    .loading-dot:nth-child(3) { animation-delay: 0s; }
    
    /* Personality badges - Enhanced */
    .personality-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #4ecdc4 100%);
        color: #ffffff;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.4rem;
        display: inline-block;
        animation: fadeInUp 0.6s ease-out, float 3s ease-in-out infinite;
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
    }
    
    .personality-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);
        background-position: 100% 100%;
    }
    
    .personality-badge:nth-child(odd) {
        animation-delay: 0.2s;
    }
    
    .personality-badge:nth-child(even) {
        animation-delay: 0.4s;
    }
    
    /* Metric containers - Enhanced */
    .metric-container {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.9) 0%, rgba(30, 30, 60, 0.8) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        color: #ffffff;
        font-size: 1rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .metric-container:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
    }
    
    /* FORCE ALL TEXT TO BE WHITE ON DARK BACKGROUND */
    *, *::before, *::after,
    .stApp, .stApp *,
    .stMarkdown, .stMarkdown *,
    h1, h2, h3, h4, h5, h6,
    p, div, span, li, strong, em {
        color: #ffffff !important;
    }
    
    /* FORCE HEADINGS */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .main h1, .main h2, .main h3, .main h4 {
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        font-weight: 700 !important;
    }
    
    /* FORCE PARAGRAPH TEXT */
    .stMarkdown p, .stMarkdown div:not(.stats-card):not(.metric-container):not(.message-user):not(.message-assistant),
    .stMarkdown span, .stMarkdown li {
        color: #e0e0e0 !important;
        font-weight: 400 !important;
    }
    
    /* FORCE CODE BLOCKS */
    .stMarkdown pre, .stMarkdown code, pre, code {
        background-color: rgba(20, 20, 40, 0.95) !important;
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.95) 0%, rgba(30, 30, 60, 0.9) 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* FORCE INLINE CODE */
    .stMarkdown code {
        background-color: rgba(102, 126, 234, 0.2) !important;
        color: #ffffff !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }
    
    /* FORCE CHART TEXT */
    .plotly, .plotly *, .js-plotly-plot * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* FORCE TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(20, 20, 40, 0.8) !important;
        border-radius: 10px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        background: transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
    }
    
    /* OVERRIDE STREAMLIT DEFAULTS */
    .stApp [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
    
    /* Info boxes - Enhanced */
    .stInfo {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(78, 205, 196, 0.1) 100%) !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(102, 126, 234, 0.1) 100%) !important;
        border: 2px solid rgba(76, 175, 80, 0.4) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 6px 18px rgba(76, 175, 80, 0.2) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.15) 0%, rgba(255, 107, 107, 0.1) 100%) !important;
        border: 2px solid rgba(244, 67, 54, 0.4) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 6px 18px rgba(244, 67, 54, 0.2) !important;
    }
    
    /* Enhanced Animations */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 50% 100%; }
        75% { background-position: 0% 50%; }
        100% { background-position: 50% 0%; }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
        }
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
    
    @keyframes glow {
        0% {
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.2);
        }
        50% {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.6), 0 0 30px rgba(102, 126, 234, 0.4);
        }
        100% {
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.2);
        }
    }
    
    @keyframes rotate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    @keyframes shimmer {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
    
    @keyframes sparkle {
        0%, 100% {
            opacity: 0;
            transform: scale(0);
        }
        50% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Loading dots enhanced animation */
    .loading-dot {
        animation: bounce 1.4s ease-in-out infinite both, glow 2s ease-in-out infinite alternate !important;
    }
    
    /* Add sparkle effect to interactive elements */
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        animation: glow 0.5s ease-in-out infinite alternate !important;
    }
    
    /* Smooth transitions for all elements */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 40, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c8df1, #8a5eb2);
    }
    
    /* ELIMINATE ALL WHITE BACKGROUNDS */
    .stApp, .stApp > div, .main, section[data-testid="stSidebar"] > div,
    .stColumn, .stForm, .element-container, .stMarkdown,
    [data-testid="stMarkdownContainer"], .block-container {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* FORCE PLOTLY CHARTS DARK */
    .js-plotly-plot, .js-plotly-plot .plotly, .plotly {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* ENHANCED ERROR MESSAGES */
    .stAlert, .stError, .stWarning, .stInfo, .stSuccess {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.15) 0%, rgba(255, 107, 107, 0.1) 100%) !important;
        background-color: rgba(244, 67, 54, 0.1) !important;
        border: 2px solid rgba(244, 67, 54, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* ENSURE NOTHING IS WHITE */
    div, span, p, h1, h2, h3, h4, h5, h6, strong, em {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* FINAL OVERRIDE - NUCLEAR OPTION */
    .stApp div:not(.stats-card):not(.metric-container):not(.message-user):not(.message-assistant):not(.loading-indicator):not(.personality-badge) {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .message-user, .message-assistant, .loading-indicator {
            max-width: 90%;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mirror_agent' not in st.session_state:
    try:
        st.session_state.mirror_agent = MirrorAgent()
    except Exception as e:
        st.error(f"Error initializing MirrorAgent: {e}")
        st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

def display_loading_indicator():
    """Display loading indicator for AI response"""
    st.markdown("""
    <div class="loading-indicator">
        <span class="loading-text">MirrorMe is analyzing your message and generating response</span>
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_personality_chart(personality_traits: Dict[str, Any]) -> go.Figure:
    """Create a radar chart for personality traits with FORCED dark theme"""
    if not personality_traits:
        # Return empty figure with dark theme
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#ffffff"),
            title=dict(text="No data available", font=dict(color="#ffffff"))
        )
        return fig
    
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    values = [personality_traits.get(trait.lower(), 5) for trait in traits]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=traits,
        fill='toself',
        name='Personality Profile',
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.3)',
        marker=dict(color='#667eea', size=8)
    ))
    
    # FORCE DARK THEME with comprehensive layout
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickmode='linear',
                tick0=0,
                dtick=2,
                gridcolor='rgba(255,255,255,0.3)',
                linecolor='rgba(255,255,255,0.3)',
                tickcolor='#ffffff',
                tickfont=dict(color='#ffffff', size=12)
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.3)',
                linecolor='rgba(255,255,255,0.3)',
                tickcolor='#ffffff',
                tickfont=dict(color='#ffffff', size=12)
            )
        ),
        showlegend=False,
        title={
            "text": "Personality Traits Analysis",
            "x": 0.5,
            "font": {"size": 18, "color": "#ffffff", "family": "Inter"}
        },
        font=dict(family="Inter, sans-serif", color="#ffffff"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=80, b=50),
        height=400
    )
    
    return fig

def create_learning_progress_chart(progress: Dict[str, Any]) -> go.Figure:
    """Create learning progress visualization"""
    try:
        stages = ['Initial Learning', 'Basic Patterns', 'Style Recognition', 'Personality Modeling', 'Advanced Mirroring']
        current_stage = progress.get('learning_stage', 'Initial Learning')
        
        # Find current stage index safely
        current_index = 0
        try:
            current_index = stages.index(current_stage)
        except ValueError:
            # If stage not found, default to first stage
            current_stage = stages[0]
            current_index = 0
        
        stage_values = []
        colors = []
        for i, stage in enumerate(stages):
            if i <= current_index:
                stage_values.append(100)
                colors.append('#667eea')
            else:
                stage_values.append(20)  # Show partially for better visual
                colors.append('rgba(255,255,255,0.3)')
        
        fig = go.Figure(data=[
            go.Bar(
                x=stages,
                y=stage_values,
                marker=dict(
                    color=colors,
                    line=dict(color='#667eea', width=2)
                ),
                text=[f"{v}%" if v == 100 else "" for v in stage_values],
                textposition='inside',
                textfont=dict(color='white', size=12, family='Inter')
            )
        ])
        
        fig.update_layout(
            title={
                "text": "Learning Progress",
                "x": 0.5,
                "font": {"size": 18, "color": "#ffffff", "family": "Inter"}
            },
            xaxis=dict(
                title="Learning Stages",
                titlefont=dict(color="#ffffff", size=14),
                tickfont=dict(color="#ffffff", size=10),
                gridcolor='rgba(255,255,255,0.1)',
                tickangle=45
            ),
            yaxis=dict(
                title="Completion %",
                titlefont=dict(color="#ffffff", size=14),
                tickfont=dict(color="#ffffff", size=10),
                gridcolor='rgba(255,255,255,0.1)',
                range=[0, 120]
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="#ffffff"),
            height=400,
            margin=dict(l=50, r=50, t=80, b=100)
        )
        
        return fig
        
    except Exception as e:
        # Return empty figure on error
        fig = go.Figure()
        fig.update_layout(
            title="Chart temporarily unavailable",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#ffffff")
        )
        return fig

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>MirrorMe</h1>
        <p>Advanced AI Personality Cloning System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Chat", "Personality Dashboard", "Learning Analytics", "Settings"],
            key="page_selector"
        )
        
        st.markdown("---")
        
        # Quick stats with enhanced visibility
        try:
            progress = st.session_state.mirror_agent.get_learning_progress()
            
            st.markdown("### Quick Stats")
            
            # Messages Analyzed Card
            messages_count = progress.get('messages_analyzed', 0)
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{messages_count}</div>
                <div class="stats-label">Messages Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Current Stage Card
            stage = progress.get('learning_stage', 'Initial Learning')
            stage_display = stage.split()[0] if stage else 'Initial'
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stage_display}</div>
                <div class="stats-label">Current Stage</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading stats: {e}")
        
        st.markdown("---")
        
        # Reset button
        if st.button("Reset Memory", help="Clear all learned personality data", key="reset_btn"):
            try:
                st.session_state.mirror_agent.reset_memory()
                st.session_state.messages = []
                st.session_state.is_generating = False
                st.success("Memory reset successfully")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error resetting memory: {e}")
    
    # Main content
    if page == "Chat":
        chat_page()
    elif page == "Personality Dashboard":
        personality_dashboard()
    elif page == "Learning Analytics":
        learning_analytics()
    else:
        settings_page()

def chat_page():
    """Main chat interface"""
    st.markdown("### Chat with Your AI Mirror")
    
    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message-user">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-assistant">
                <strong>MirrorMe:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Show loading indicator
    if st.session_state.is_generating:
        display_loading_indicator()
    
    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "message",
                placeholder="Type your message here and watch me learn your communication style...",
                label_visibility="collapsed",
                key="user_message_input"
            )
        
        with col2:
            send_button = st.form_submit_button("Send", use_container_width=True)
    
    # Handle message sending
    if send_button and user_input and not st.session_state.is_generating:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.is_generating = True
        st.rerun()
    
    # Generate AI response
    if st.session_state.is_generating and len(st.session_state.messages) > 0:
        # Get the last user message
        last_user_message = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break
        
        if last_user_message:
            try:
                # Generate response
                response = st.session_state.mirror_agent.generate_response(last_user_message)
                
                # Add AI response
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.is_generating = False
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
                st.session_state.is_generating = False
                st.rerun()
    
    # Additional controls
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat", use_container_width=True, key="clear_chat_btn"):
            st.session_state.messages = []
            st.session_state.is_generating = False
            st.rerun()

def personality_dashboard():
    """Personality analysis dashboard"""
    st.markdown("### Personality Dashboard")
    
    try:
        # Get personality data
        personality_summary = st.session_state.mirror_agent.get_personality_summary()
        profile = st.session_state.mirror_agent.memory_manager.get_personality_traits()
        
        if not profile:
            st.info("Start chatting to see your personality analysis")
            return
        
        # Personality summary
        st.markdown("#### Personality Summary")
        st.markdown(personality_summary)
        
        st.markdown("---")
        
        # Personality traits visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personality Traits")
            if 'personality_traits' in profile:
                try:
                    fig = create_personality_chart(profile['personality_traits'])
                    st.plotly_chart(fig, use_container_width=True, key="personality_radar_chart")
                except Exception as e:
                    st.markdown("""
                    <div class="chart-error">
                        <h3>🎆 Personality Radar</h3>
                        <p>Your personality chart will appear here as the AI learns more about you.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="chart-error">
                    <h3>🎆 Personality Radar</h3>
                    <p>Start chatting to see your personality analysis!</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Communication Style")
            comm_style = profile.get('communication_style', {})
            
            if comm_style:
                st.markdown(f"""
                <div class="personality-badge">Tone: {comm_style.get('tone', 'Unknown')}</div>
                <div class="personality-badge">Formality: {comm_style.get('formality_level', 5)}/10</div>
                <div class="personality-badge">Enthusiasm: {comm_style.get('enthusiasm_level', 5)}/10</div>
                """, unsafe_allow_html=True)
                
                if comm_style.get('uses_emojis'):
                    st.markdown('<div class="personality-badge">Uses Emojis</div>', unsafe_allow_html=True)
                
                if comm_style.get('uses_slang'):
                    st.markdown('<div class="personality-badge">Uses Slang</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Interests and phrases
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Interests & Topics")
            interests = profile.get('interests_and_topics', [])
            if interests:
                for interest in interests[:10]:
                    st.markdown(f"• {interest}")
            else:
                st.info("No specific interests identified yet")
        
        with col2:
            st.markdown("#### Favorite Phrases")
            phrases = profile.get('favorite_phrases', [])
            if phrases:
                for phrase in phrases[:5]:
                    st.markdown(f"• '{phrase}'")
            else:
                st.info("No favorite phrases identified yet")
    
    except Exception as e:
        st.error(f"Error loading personality dashboard: {e}")

def learning_analytics():
    """Learning analytics and progress tracking"""
    st.markdown("### Learning Analytics")
    
    try:
        progress = st.session_state.mirror_agent.get_learning_progress()
        profile = st.session_state.mirror_agent.memory_manager.get_personality_traits()
        
        # Progress overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            messages_count = progress.get('messages_analyzed', 0)
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{messages_count}</div>
                <div class="stats-label">Messages Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            next_update = progress.get('next_analysis_at', 'N/A')
            if isinstance(next_update, int):
                next_update = f"{next_update}"
            elif next_update == 'N/A':
                next_update = "5"
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{next_update}</div>
                <div class="stats-label">Next Update At</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            updates = "Yes" if progress.get('personality_updates', False) else "No"
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{updates}</div>
                <div class="stats-label">Profile Updated</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            stage = progress.get('learning_stage', 'Initial Learning')
            # Extract stage number or use meaningful display
            if 'Initial' in stage:
                stage_display = "1"
            elif 'Basic' in stage:
                stage_display = "2" 
            elif 'Style' in stage:
                stage_display = "3"
            elif 'Personality' in stage:
                stage_display = "4"
            elif 'Advanced' in stage:
                stage_display = "5"
            else:
                stage_display = "1"
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stage_display}</div>
                <div class="stats-label">Learning Stage</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Learning progress chart with enhanced error handling
        st.markdown("#### Learning Progress")
        try:
            fig = create_learning_progress_chart(progress)
            st.plotly_chart(fig, use_container_width=True, key="learning_progress_chart")
        except Exception as chart_error:
            st.markdown("""
            <div class="chart-error">
                <h3>📈 Learning Progress Chart</h3>
                <p>Chart will appear as you continue chatting with your AI mirror.</p>
                <p style="font-size: 0.9rem; opacity: 0.7;">Currently building your personality profile...</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Message statistics
        if profile and 'message_statistics' in profile:
            stats = profile['message_statistics']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Message Statistics")
                st.markdown(f"""
                <div class="metric-container">
                    <strong>Average Words per Message:</strong> {stats.get('avg_words_per_message', 0):.1f}
                </div>
                <div class="metric-container">
                    <strong>Average Characters per Message:</strong> {stats.get('avg_chars_per_message', 0):.1f}
                </div>
                <div class="metric-container">
                    <strong>Average Sentiment:</strong> {stats.get('avg_sentiment', 0):.3f}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Common Words")
                common_words = stats.get('common_words', [])
                if common_words and len(common_words) > 0:
                    try:
                        # Simple word list instead of word cloud for now
                        st.markdown("**Top words used:**")
                        for i, word in enumerate(common_words[:10], 1):
                            st.markdown(f"{i}. {word}")
                    except Exception as word_error:
                        st.error(f"Error displaying words: {word_error}")
                        st.info("Word analysis temporarily unavailable")
                else:
                    st.info("Not enough data for word analysis yet")
        else:
            st.info("No message statistics available yet. Start chatting to see analytics!")
    
    except Exception as e:
        st.error(f"Error loading learning analytics: {e}")
        st.markdown("""
        **Troubleshooting:**
        1. Try refreshing the page
        2. Make sure you have chatted with the AI first
        3. Check if your OpenAI API key is configured correctly
        """)

def settings_page():
    """Settings and configuration page"""
    st.markdown("### Settings")
    
    try:
        # Export data
        st.markdown("#### Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Chat History", use_container_width=True, key="export_chat_btn"):
                data = st.session_state.mirror_agent.export_data()
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name=f"mirrorme_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_chat_btn"
                )
        
        with col2:
            if st.button("Export Personality Profile", use_container_width=True, key="export_profile_btn"):
                profile = st.session_state.mirror_agent.memory_manager.get_personality_traits()
                if profile:
                    st.download_button(
                        label="Download Profile",
                        data=json.dumps(profile, indent=2),
                        file_name=f"personality_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key="download_profile_btn"
                    )
        
        st.markdown("---")
        
        # Configuration settings
        st.markdown("#### Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <strong>Model:</strong> {Config.MODEL_NAME}
            </div>
            <div class="metric-container">
                <strong>Temperature:</strong> {Config.TEMPERATURE}
            </div>
            <div class="metric-container">
                <strong>Max Tokens:</strong> {Config.MAX_TOKENS}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <strong>Analysis Frequency:</strong> Every {Config.PERSONALITY_ANALYSIS_FREQUENCY} messages
            </div>
            <div class="metric-container">
                <strong>Min Messages for Analysis:</strong> {Config.MIN_MESSAGES_FOR_ANALYSIS}
            </div>
            <div class="metric-container">
                <strong>Max Memory Items:</strong> {Config.MAX_MEMORY_ITEMS}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # About section
        st.markdown("#### About MirrorMe")
        st.markdown("""
        **MirrorMe** is an advanced AI personality cloning system that learns your communication style over time.
        
        **Features:**
        - Advanced personality analysis using GPT and LangChain
        - Intelligent memory system with FAISS vector search
        - Real-time learning progress tracking
        - Professional dark theme interface
        - Comprehensive analytics dashboard
        
        **Tech Stack:**
        - OpenAI GPT for language generation
        - LangChain for AI agent orchestration
        - FAISS for semantic similarity search
        - Streamlit for web interface
        - Plotly for interactive visualizations
        """)
    
    except Exception as e:
        st.error(f"Error loading settings: {e}")

if __name__ == "__main__":
    main()
    
    # Add JavaScript to enforce dark theme after page load
    st.markdown("""
    <script>
    // Trigger dark theme enforcement after Streamlit loads
    setTimeout(function() {
        if (window.mirrorMeTheme) {
            window.mirrorMeTheme.reinitialize();
            console.log('🎨 MirrorMe Dark Theme Applied Successfully!');
        }
    }, 1000);
    
    // Additional enforcement for dynamic content
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            if (window.mirrorMeTheme) {
                window.mirrorMeTheme.enforceCharts();
                window.mirrorMeTheme.fixStats();
            }
        }, 1500);
    });
    </script>
    
    <style>
    /* Additional chart overrides */
    .js-plotly-plot .plot-container .svg-container svg {
        background: transparent !important;
    }
    
    /* Force any remaining white backgrounds */
    .js-plotly-plot .bg, .plotly .bg {
        fill: transparent !important;
    }
    
    /* Enhanced stats card visibility */
    .stats-card .stats-number {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)