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
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 17px;
    color: #94A3B8;
    margin-bottom: 30px;
}

.section-box {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #26354D;
    margin-bottom: 20px;
}

.metric-card {
    background-color: #162235;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #26354D;
    text-align: center;
}

.metric-name {
    color: #94A3B8;
    font-size: 15px;
}

.metric-value {
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.fault-card {
    background-color: #3A1620;
    padding: 25px;
    border-radius: 15px;
    border-left: 6px solid #EF4444;
}

.safe-card {
    background-color: #10352B;
    padding: 25px;
    border-radius: 15px;
    border-left: 6px solid #10B981;
}

.warning-card {
    background-color: #3D2D0B;
    padding: 25px;
    border-radius: 15px;
    border-left: 6px solid #F59E0B;
}

.ai-card {
    background-color: #162235;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-title">
⚙️ AI Predictive Maintenance System
</div>

<div class="subtitle">
Machine Monitoring • Fault Detection • Failure Prediction • Maintenance Planning
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Machine Control")

machine = st.sidebar.selectbox(
    "Select Machine",
    [
        "Reciprocating Pump",
        "Hydraulic Turbine",
        "Petrol Engine"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Sensor Readings")


# =========================================================
# RECIPROCATING PUMP
# =========================================================

if machine == "Reciprocating Pump":

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        20.0, 120.0, 45.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0, 20.0, 2.0
    )

    pressure = st.sidebar.slider(
        "Pressure (bar)",
        0.0, 20.0, 8.0
    )

    rpm = st.sidebar.slider(
        "RPM",
        100, 3000, 1500
    )

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Pressure": pressure,
        "RPM": rpm
    }

    units = {
        "Temperature": "°C",
        "Vibration": "mm/s",
        "Pressure": "bar",
        "RPM": "RPM"
    }

    fault_scores = {
        "Temperature": max(0, min(100, (temperature - 70) * 3)),
        "Vibration": max(0, min(100, (vibration - 3) * 12)),
        "Pressure": max(0, min(100, abs(pressure - 8) * 12)),
        "RPM": max(0, min(100, abs(rpm - 1500) / 12))
    }

    fault_causes = {
        "Temperature":
            "Possible bearing overheating or insufficient cooling.",

        "Vibration":
            "Possible bearing wear, shaft misalignment or imbalance.",

        "Pressure":
            "Possible leakage, valve fault or blockage.",

        "RPM":
            "Possible motor or drive system abnormality."
    }


# =========================================================
# HYDRAULIC TURBINE
# =========================================================

elif machine == "Hydraulic Turbine":

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        10.0, 120.0, 40.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0, 20.0, 2.0
    )

    water_flow = st.sidebar.slider(
        "Water Flow (L/s
