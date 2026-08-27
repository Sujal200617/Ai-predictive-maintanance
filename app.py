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
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #08121e;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.title-text {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: white;
}

.subtitle-text {
    text-align: center;
    font-size: 17px;
    color: #aeb8c2;
    margin-bottom: 30px;
}

.section-box {
    background-color: #101d2b;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #22354a;
    margin-bottom: 20px;
}

.metric-card {
    background-color: #132536;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #27445e;
    text-align: center;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}

.small-title {
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}

</
