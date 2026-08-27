import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

    .stApp {
        background-color: #0B1220;
        color: #E5E7EB;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263244;
    }

    /* Title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
        color: white;
    }

    .subtitle {
        font-size: 17px;
        color: #94A3B8;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* Metric cards */
    .metric-card {
        background: #151F30;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 22px;
        min-height: 120px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
    }

    .metric-title {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    /* Section card */
    .dashboard-card {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }

    /* Machine badge */
    .machine-badge {
        background: linear-gradient(90deg, #1D4ED8, #2563EB);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 15px;
    }

    /* Healthy */
    .healthy-box {
        background-color: #064E3B;
        border: 1px solid #10B981;
        padding: 16px;
        border-radius: 12px;
        color: #D1FAE5;
    }

    /* Warning */
    .warning-box {
        background-color: #78350F;
        border: 1px solid #F59E0B;
        padding: 16px;
        border-radius
