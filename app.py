import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Predictive Maintenance System",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL CSS DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: white;
}

/* Main Title */
.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #94A3B8;
    margin-bottom: 30px;
}

/* Cards */
.metric-card {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #24324A;
    text-align: center;
}

.metric-title {
    font-size: 15px;
    color: #94A3B8;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

/* Status Cards */
.status-card {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-top: 10px;
}

.healthy {
    background-color: #064E3B;
    border: 1px solid #10B981;
}

.warning {
    background-color: #78350F;
    border: 1px solid #F59E0B;
}

.danger {
    background-color: #7F1D1D;
    border: 1px solid #EF4444;
}

/* Recommendation Box */
.recommendation {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #38BDF8;
    margin-top: 15px;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# ⚙️ Control Panel")

machine = st.sidebar.selectbox(
    "Select Machine",
    [
        "Reciprocating Pump",
        "Hydraulic Turbine",
        "Petrol Engine"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🧠 System Information")

st.sidebar.info(
    "This AI Predictive Maintenance System analyses machine parameters "
    "and estimates the maintenance risk."
)


# =========================================================
# RECIPROCATING PUMP
# =========================================================

if machine == "Reciprocating Pump":

    machine_icon = "🔧"

    st.sidebar.markdown("### 📡 Sensor Inputs")

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        20.0,
        120.0,
        45.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0,
        20.0,
        2.0
    )

    pressure = st.sidebar.slider(
        "Pressure (bar)",
        0.0,
        20.0,
        5.0
    )

    rpm = st.sidebar.slider(
        "RPM",
        100,
        3000,
        1000
    )

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Pressure": pressure,
        "RPM": rpm
    }

    risk = 0

    if temperature > 85:
        risk += 30

    if vibration > 8:
        risk += 35

    if pressure > 15 or pressure < 2:
        risk += 20

    if rpm > 2500:
        risk += 15


# =========================================================
# HYDRAULIC TURBINE
# =========================================================

elif machine == "Hydraulic Turbine":

    machine_icon = "💧"

    st.sidebar.markdown("### 📡 Sensor Inputs")

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        10.0,
        120.0,
        40.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0,
        20.0,
        2.0
    )

    water_flow = st.sidebar.slider(
        "Water Flow (L/s)",
        10.0,
        1000.0,
        200.0
    )

    rpm = st.sidebar.slider(
        "RPM",
        100,
        5000,
        1500
    )

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Water Flow": water_flow,
        "RPM": rpm
    }

    risk = 0

    if temperature > 80:
        risk += 25

    if vibration > 7:
        risk += 35

    if water_flow < 50:
        risk += 20

    if rpm > 4000:
        risk += 20


# =========================================================
# PETROL ENGINE
# =========================================================

elif machine == "Petrol Engine":

    machine_icon = "🚗"

    st.sidebar.markdown("### 📡 Sensor Inputs")

    temperature = st.sidebar.slider(
        "Engine Temperature (°C)",
        20.0,
        140.0,
        85.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0,
        20.0,
        3.0
    )

    rpm = st.sidebar.slider(
        "Engine RPM",
        500,
        8000,
        2500
    )

    oil_pressure = st.sidebar.slider(
        "Oil Pressure (bar)",
        0.0,
        10.0,
        4.0
    )

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "RPM": rpm,
        "Oil Pressure": oil_pressure
    }

    risk = 0

    if temperature > 110:
        risk += 30

    if vibration > 8:
        risk += 30

    if rpm > 6000:
        risk += 15

    if oil_pressure < 1.5:
        risk += 25


# =========================================================
# LIMIT RISK
# =========================================================

risk = min(risk, 100)
health_score = 100 - risk


# =========================================================
# MACHINE CONDITION
# =========================================================

if risk <= 20:
    status = "HEALTHY"
    status_icon = "🟢"
    status_class = "healthy"
    recommendation = (
        "Machine parameters are within the normal operating range. "
        "Continue regular monitoring and preventive maintenance."
    )

elif risk <= 50:
    status = "WARNING"
    status_icon = "🟡"
    status_class = "warning"
    recommendation = (
        "Some machine parameters require attention. "
        "Inspect the machine and schedule maintenance soon."
    )

else:
    status = "HIGH RISK"
    status_icon = "🔴"
    status_class = "danger"
    recommendation = (
        "Abnormal operating conditions detected. "
        "A detailed inspection and maintenance check are recommended."
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="main-title">
        {machine_icon} AI Predictive Maintenance System
    </div>

    <div class="subtitle">
        Intelligent machine monitoring and maintenance risk analysis
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MACHINE INFORMATION
# =========================================================

st.markdown(
    f"### 🏭 Selected Machine: {machine}"
)


# =========================================================
# METRIC CARDS
# =========================================================

cols = st.columns(len(parameters))

for column, (name, value) in zip(cols, parameters.items()):

    with column:

        if name == "Temperature":
            unit = "°C"

        elif name == "Vibration":
            unit = "mm/s"

        elif name == "Pressure":
            unit = "bar"

        elif name == "Oil Pressure":
            unit = "bar"

        elif name == "Water Flow":
            unit = "L/s"

        else:
            unit = "RPM"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{name}</div>
                <div class="metric-value">{value} {unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# MACHINE STATUS AND HEALTH SCORE
# =========================================================

left_column, right_column = st.columns([1, 1])


with left_column:

    st.markdown("## Machine Condition")

    st.markdown(
        f"""
        <div class="status-card {status_class}">
            <h1>{status_icon} {status}</h1>
            <h3>Failure Risk: {risk}%</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(health_score / 100)

    st.write(f"### Machine Health Score: {health_score} / 100")


with right_column:

    st.markdown("## 📊 AI Risk Analysis")

    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk,
            title={"text": "Failure Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.75},
                "steps": [
                    {"range": [0, 20]},
                    {"range": [20, 50]},
                    {"range": [50, 100]}
                ]
            }
        )
    )

    figure.update_layout(
        height=350,
        paper_bgcolor="#0B1120",
        font={"color": "white"}
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# =========================================================
# SENSOR ANALYSIS CHART
# =========================================================

st.markdown("## 📈 Sensor Parameter Analysis")

parameter_names = list(parameters.keys())
parameter_values = list(parameters.values())

chart_data = pd.DataFrame(
    {
        "Parameter": parameter_names,
        "Value": parameter_values
    }
)

st.bar_chart(
    chart_data.set_index("Parameter")
)


# =========================================================
# MAINTENANCE RECOMMENDATION
# =========================================================

st.markdown("## 🔧 AI Maintenance Recommendation")

st.markdown(
    f"""
    <div class="recommendation">
        <h3>🤖 Recommendation</h3>
        <p>{recommendation}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SENSOR DETAILS
# =========================================================

st.markdown("## 📡 Recommended Sensors")

if machine == "Reciprocating Pump":

    sensor_data = {
        "Sensor": [
            "Temperature Sensor",
            "Vibration Sensor",
            "Pressure Sensor",
            "RPM Sensor"
        ],
        "Purpose": [
            "Detects overheating",
            "Detects abnormal vibration",
            "Measures pump pressure",
            "Measures motor speed"
        ]
    }


elif machine == "Hydraulic Turbine":

    sensor_data = {
        "Sensor": [
            "Temperature Sensor",
            "Vibration Sensor",
            "Water Flow Sensor",
            "RPM Sensor"
        ],
        "Purpose": [
            "Monitors bearing temperature",
            "Detects turbine imbalance",
            "Measures water flow",
            "Measures turbine rotational speed"
        ]
    }


else:

    sensor_data = {
        "Sensor": [
            "Engine Temperature Sensor",
            "Vibration Sensor",
            "RPM Sensor",
            "Oil Pressure Sensor"
        ],
        "Purpose": [
            "Detects engine overheating",
            "Detects abnormal vibration",
            "Measures engine speed",
            "Monitors lubrication pressure"
        ]
    }


sensor_df = pd.DataFrame(sensor_data)

st.dataframe(
    sensor_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# SYSTEM STATUS
# =========================================================

st.markdown("---")

current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

st.caption(
    f"🤖 AI Predictive Maintenance System | "
    f"Last Analysis: {current_time}"
)
