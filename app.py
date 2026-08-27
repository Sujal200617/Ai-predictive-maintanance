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
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: white;
}

.subtitle {
    font-size: 17px;
    color: #94A3B8;
    margin-bottom: 25px;
}

.metric-card {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #24324A;
    text-align: center;
}

.metric-title {
    color: #94A3B8;
    font-size: 15px;
}

.metric-value {
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.healthy {
    background-color: #064E3B;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}

.warning {
    background-color: #78350F;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}

.danger {
    background-color: #7F1D1D;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}

.recommendation {
    background-color: #111C2E;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #38BDF8;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

machine = st.sidebar.selectbox(
    "Select Machine",
    [
        "Reciprocating Pump",
        "Hydraulic Turbine",
        "Petrol Engine"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Live Sensor Inputs")


# =========================================================
# RECIPROCATING PUMP
# =========================================================

if machine == "Reciprocating Pump":

    machine_icon = "🔧"

    temperature = st.sidebar.slider("Temperature (°C)", 20.0, 120.0, 45.0)
    vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 20.0, 2.0)
    pressure = st.sidebar.slider("Pressure (bar)", 0.0, 20.0, 5.0)
    rpm = st.sidebar.slider("RPM", 100, 3000, 1000)

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Pressure": pressure,
        "RPM": rpm
    }

    # FAULT SEVERITY CALCULATION
    fault_scores = {
        "Temperature": max(0, min(100, (temperature - 70) * 2)),
        "Vibration": max(0, min(100, vibration * 10)),
        "Pressure": max(0, min(100, abs(pressure - 8) * 12)),
        "RPM": max(0, min(100, (rpm - 1800) / 12))
    }

    fault_causes = {
        "Temperature": "Possible bearing overheating or insufficient cooling.",
        "Vibration": "Possible bearing wear, misalignment or mechanical imbalance.",
        "Pressure": "Possible leakage, valve problem or pressure system fault.",
        "RPM": "Possible motor speed or drive system abnormality."
    }


# =========================================================
# HYDRAULIC TURBINE
# =========================================================

elif machine == "Hydraulic Turbine":

    machine_icon = "💧"

    temperature = st.sidebar.slider("Temperature (°C)", 10.0, 120.0, 40.0)
    vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 20.0, 2.0)
    water_flow = st.sidebar.slider("Water Flow (L/s)", 10.0, 1000.0, 200.0)
    rpm = st.sidebar.slider("RPM", 100, 5000, 1500)

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Water Flow": water_flow,
        "RPM": rpm
    }

    fault_scores = {
        "Temperature": max(0, min(100, (temperature - 70) * 2)),
        "Vibration": max(0, min(100, vibration * 11)),
        "Water Flow": max(0, min(100, (100 - water_flow) * 0.8)),
        "RPM": max(0, min(100, (rpm - 3500) / 15))
    }

    fault_causes = {
        "Temperature": "Possible bearing overheating.",
        "Vibration": "Possible turbine imbalance or bearing fault.",
        "Water Flow": "Possible blockage, leakage or reduced water supply.",
        "RPM": "Possible turbine speed control problem."
    }


# =========================================================
# PETROL ENGINE
# =========================================================

else:

    machine_icon = "🚗"

    temperature = st.sidebar.slider(
        "Engine Temperature (°C)",
        20.0, 140.0, 85.0
    )

    vibration = st.sidebar.slider(
        "Vibration (mm/s)",
        0.0, 20.0, 3.0
    )

    rpm = st.sidebar.slider(
        "Engine RPM",
        500, 8000, 2500
    )

    oil_pressure = st.sidebar.slider(
        "Oil Pressure (bar)",
        0.0, 10.0, 4.0
    )

    parameters = {
        "Temperature": temperature,
        "Vibration": vibration,
        "RPM": rpm,
        "Oil Pressure": oil_pressure
    }

    fault_scores = {
        "Temperature": max(0, min(100, (temperature - 95) * 3)),
        "Vibration": max(0, min(100, vibration * 10)),
        "RPM": max(0, min(100, (rpm - 5500) / 20)),
        "Oil Pressure": max(0, min(100, (2.5 - oil_pressure) * 40))
    }

    fault_causes = {
        "Temperature": "Possible engine overheating or cooling system problem.",
        "Vibration": "Possible engine imbalance, mounting or mechanical problem.",
        "RPM": "Possible excessive engine speed or load.",
        "Oil Pressure": "Possible lubrication system or oil pump problem."
    }


# =========================================================
# CALCULATE OVERALL RISK
# =========================================================

risk = int(sum(fault_scores.values()) / len(fault_scores))
risk = min(risk, 100)

health_score = 100 - risk


# =========================================================
# FIND MAIN FAULT LOCATION
# =========================================================

main_fault = max(fault_scores, key=fault_scores.get)
main_fault_score = fault_scores[main_fault]

fault_description = fault_causes[main_fault]


# =========================================================
# MACHINE STATUS
# =========================================================

if risk <= 20:

    status = "HEALTHY"
    status_icon = "🟢"
    status_class = "healthy"

elif risk <= 50:

    status = "WARNING"
    status_icon = "🟡"
    status_class = "warning"

else:

    status = "HIGH RISK"
    status_icon = "🔴"
    status_class = "danger"


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="main-title">
        {machine_icon} AI Predictive Maintenance System
    </div>

    <div class="subtitle">
        Intelligent Machine Monitoring • Fault Detection • Failure Risk Prediction
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader(f"🏭 Selected Machine: {machine}")


# =========================================================
# SENSOR METRIC CARDS
# =========================================================

cols = st.columns(len(parameters))

for col, (name, value) in zip(cols, parameters.items()):

    with col:

        if "Temperature" in name:
            unit = "°C"

        elif "Vibration" in name:
            unit = "mm/s"

        elif "Pressure" in name:
            unit = "bar"

        elif "Flow" in name:
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


st.markdown("---")


# =========================================================
# MACHINE STATUS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Machine Condition")

    st.markdown(
        f"""
        <div class="{status_class}">
            <h1>{status_icon} {status}</h1>
            <h3>Failure Risk: {risk}%</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(health_score / 100)

    st.write(f"### Machine Health Score: {health_score}/100")


with col2:

    st.subheader("AI Failure Risk")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk,
            number={"suffix": "%"},
            title={"text": "Overall Failure Risk"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 20]},
                    {"range": [20, 50]},
                    {"range": [50, 100]}
                ]
            }
        )
    )

    gauge.update_layout(
        height=350,
        paper_bgcolor="#0B1120",
        font={"color": "white"}
    )

    st.plotly_chart(gauge, use_container_width=True)


# =========================================================
# NEW FAULT LOCATION CHART
# =========================================================

st.markdown("---")

st.header("🚨 Fault Detection & Fault Location")

st.info(
    "The chart below identifies which machine parameter is showing "
    "the highest abnormality."
)

fault_df = pd.DataFrame({
    "Machine Parameter": list(fault_scores.keys()),
    "Fault Severity (%)": list(fault_scores.values())
})

fault_chart = go.Figure()

fault_chart.add_trace(
    go.Bar(
        x=fault_df["Machine Parameter"],
        y=fault_df["Fault Severity (%)"],
        text=fault_df["Fault Severity (%)"].round(1),
        textposition="auto"
    )
)

fault_chart.update_layout(
    title="Fault Severity by Machine Parameter",
    xaxis_title="Machine Parameter",
    yaxis_title="Fault Severity (%)",
    yaxis=dict(range=[0, 100]),
    height=450,
    paper_bgcolor="#0B1120",
    plot_bgcolor="#111C2E",
    font={"color": "white"}
)

st.plotly_chart(fault_chart, use_container_width=True)


# =========================================================
# FAULT DIAGNOSIS
# =========================================================

st.markdown("## 🤖 AI Fault Diagnosis")

if main_fault_score < 20:

    st.success(
        f"🟢 No significant fault detected. "
        f"The highest monitored parameter is {main_fault}, "
        f"but it is currently within a safe range."
    )

else:

    if main_fault_score <= 50:
        level = "MODERATE WARNING"
        icon = "🟡"
    else:
        level = "CRITICAL FAULT"
        icon = "🔴"

    st.markdown(
        f"""
        <div class="recommendation">
            <h2>{icon} {level}</h2>
            <h3>Fault Location: {main_fault}</h3>
            <h3>Fault Severity: {main_fault_score:.1f}%</h3>
            <p><b>AI Diagnosis:</b> {fault_description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PARAMETER STATUS TABLE
# =========================================================

st.markdown("## 📊 Individual Parameter Analysis")

analysis_rows = []

for parameter, score in fault_scores.items():

    if score < 20:
        condition = "🟢 Normal"

    elif score < 50:
        condition = "🟡 Warning"

    else:
        condition = "🔴 Critical"

    analysis_rows.append({
        "Parameter": parameter,
        "Fault Severity (%)": round(score, 1),
        "Condition": condition
    })

analysis_df = pd.DataFrame(analysis_rows)

st.dataframe(
    analysis_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# MAINTENANCE RECOMMENDATION
# =========================================================

st.markdown("## 🔧 AI Maintenance Recommendation")

if main_fault_score < 20:

    recommendation = (
        "Continue normal operation and follow the regular "
        "preventive maintenance schedule."
    )

else:

    recommendation = (
        f"Inspect the {main_fault} system first. "
        f"{fault_description}"
    )

st.markdown(
    f"""
    <div class="recommendation">
        <h3>Recommended Action</h3>
        <p>{recommendation}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SENSOR DETAILS
# =========================================================

st.markdown("## 📡 Sensors Used")

sensor_df = pd.DataFrame({
    "Parameter": list(parameters.keys()),
    "Purpose": [
        "Monitors machine operating condition"
        for i in parameters
    ]
})

st.dataframe(
    sensor_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

st.caption(
    f"⚙️ AI Predictive Maintenance System | "
    f"Last Analysis: {current_time}"
)
