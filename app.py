import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "saved_readings" not in st.session_state:
    st.session_state.saved_readings = []

# ---------------------------------------------------------
# MACHINE SELECTION
# ---------------------------------------------------------

machine_options = [
    "Reciprocating Pump",
    "Hydraulic Turbine",
    "Petrol Engine"
]

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("⚙️ CONTROL PANEL")

machine = st.sidebar.selectbox(
    "Select Machine",
    machine_options
)

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Sensor Readings")

temperature = st.sidebar.slider(
    "Temperature (°C)",
    0.0,
    150.0,
    45.0,
    0.5
)

vibration = st.sidebar.slider(
    "Vibration (mm/s)",
    0.0,
    20.0,
    2.0,
    0.1
)

current = st.sidebar.slider(
    "Current (A)",
    0.0,
    100.0,
    5.0,
    0.1
)

rpm = st.sidebar.slider(
    "RPM",
    0,
    5000,
    1500,
    10
)

# ---------------------------------------------------------
# MACHINE-SPECIFIC SENSOR
# ---------------------------------------------------------

if machine == "Reciprocating Pump":

    extra_name = "Pressure (bar)"

    extra_value = st.sidebar.slider(
        "Pressure (bar)",
        0.0,
        30.0,
        5.0,
        0.1
    )

elif machine == "Hydraulic Turbine":

    extra_name = "Water Flow (L/s)"

    extra_value = st.sidebar.slider(
        "Water Flow (L/s)",
        0.0,
        500.0,
        100.0,
        1.0
    )

else:

    extra_name = "Oil Pressure (bar)"

    extra_value = st.sidebar.slider(
        "Oil Pressure (bar)",
        0.0,
        15.0,
        5.0,
        0.1
    )

# ---------------------------------------------------------
# AI ANALYSIS FUNCTION
# ---------------------------------------------------------

def analyse_machine():

    risk = 0
    faults = []
    positions = []
    recommendations = []

    # TEMPERATURE

    if temperature > 110:
        risk += 35
        faults.append("Critical Overheating")
        positions.append("Cooling System")
        recommendations.append(
            "Stop the machine and inspect the cooling system."
        )

    elif temperature > 85:
        risk += 20
        faults.append("High Temperature")
        positions.append("Cooling System")
        recommendations.append(
            "Inspect coolant, ventilation and heat removal."
        )

    # VIBRATION

    if vibration > 12:
        risk += 35
        faults.append("Critical Vibration")
        positions.append("Bearing and Shaft Assembly")
        recommendations.append(
            "Inspect bearings, shaft alignment and mounting."
        )

    elif vibration > 7:
        risk += 20
        faults.append("High Vibration")
        positions.append("Bearing Assembly")
        recommendations.append(
            "Check bearing condition and alignment."
        )

    # CURRENT

    if current > 80:
        risk += 25
        faults.append("High Electrical Load")
        positions.append("Motor or Electrical System")
        recommendations.append(
            "Inspect electrical load and motor connections."
        )

    elif current > 50:
        risk += 15
        faults.append("Increased Current")
        positions.append("Electrical System")
        recommendations.append(
            "Monitor electrical load and motor performance."
        )

    # RPM

    if rpm < 500 or rpm > 3500:
        risk += 20
        faults.append("Abnormal RPM")
        positions.append("Drive System")
        recommendations.append(
            "Inspect the rotating and speed control system."
        )

    # RECIPROCATING PUMP

    if machine == "Reciprocating Pump":

        if extra_value < 2:
            risk += 20
            faults.append("Low Pressure")
            positions.append("Pump Valve or Piston")
            recommendations.append(
                "Check pump valves, piston and possible leakage."
            )

        elif extra_value > 20:
            risk += 20
            faults.append("High Pressure")
            positions.append("Delivery Line")
            recommendations.append(
                "Check for blockage in the delivery line."
            )

    # HYDRAULIC TURBINE

    elif machine == "Hydraulic Turbine":

        if extra_value < 40:
            risk += 20
            faults.append("Low Water Flow")
            positions.append("Water Inlet or Nozzle")
            recommendations.append(
                "Inspect the water inlet and turbine nozzle."
            )

        elif extra_value > 400:
            risk += 15
            faults.append("Excessive Water Flow")
            positions.append("Flow Control System")
            recommendations.append(
                "Inspect the flow control system."
            )

    # PETROL ENGINE

    elif machine == "Petrol Engine":

        if extra_value < 2:
            risk += 25
            faults.append("Low Oil Pressure")
            positions.append("Lubrication System")
            recommendations.append(
                "Check engine oil level and oil pump."
            )

        elif extra_value > 10:
            risk += 15
            faults.append("High Oil Pressure")
            positions.append("Oil Circulation System")
            recommendations.append(
                "Inspect oil passages and pressure regulation."
            )

    # LIMIT RISK

    if risk > 100:
        risk = 100

    # MACHINE CONDITION

    if risk < 20:
        condition = "HEALTHY"
        message = "Machine is operating within the normal range."

    elif risk < 45:
        condition = "MONITOR"
        message = "Minor abnormalities detected. Continue monitoring."

    elif risk < 70:
        condition = "WARNING"
        message = "Maintenance inspection is recommended."

    else:
        condition = "CRITICAL"
        message = "Immediate inspection is recommended."

    # DEFAULT RESULTS

    if len(faults) == 0:
        faults.append("No Major Fault Detected")

    if len(positions) == 0:
        positions.append("No Critical Fault Position Detected")

    if len(recommendations) == 0:
        recommendations.append(
            "Continue normal operation and regular monitoring."
        )

    return risk, condition, message, faults, positions, recommendations


# ---------------------------------------------------------
# RUN ANALYSIS
# ---------------------------------------------------------

risk, condition, message, faults, positions, recommendations = analyse_machine()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("⚙️ AI Predictive Maintenance System")

st.caption(
    "Machine Condition Monitoring • Fault Detection • Failure Risk Prediction"
)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 1 - MACHINE READINGS
# ---------------------------------------------------------

st.header("📊 1. Live Machine Readings")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Temperature",
    str(temperature) + " °C"
)

col2.metric(
    "Vibration",
    str(vibration) + " mm/s"
)

col3.metric(
    "Current",
    str(current) + " A"
)

col4.metric(
    "RPM",
    str(rpm)
)

col5.metric(
    extra_name,
    str(extra_value)
)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 2 - CONDITION AND FAILURE RISK
# ---------------------------------------------------------

st.header("🤖 2. AI Condition Analysis")

left_column, right_column = st.columns(2)

with left_column:

    st.subheader("Machine Condition")

    if condition == "HEALTHY":
        st.success("🟢 " + condition)

    elif condition == "MONITOR":
        st.info("🔵 " + condition)

    elif condition == "WARNING":
        st.warning("🟠 " + condition)

    else:
        st.error("🔴 " + condition)

    st.write(message)

with right_column:

    st.subheader("Failure Risk")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk,
            number={"suffix": "%"},
            title={"text": "Predicted Failure Risk"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "red"},
                "steps": [
                    {"range": [0, 25], "color": "lightgreen"},
                    {"range": [25, 50], "color": "yellow"},
                    {"range": [50, 75], "color": "orange"},
                    {"range": [75, 100], "color": "lightcoral"}
                ]
            }
        )
    )

    gauge.update_layout(
        height=320
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.markdown("---")

# ---------------------------------------------------------
# SECTION 3 - FAULT POSITION
# ---------------------------------------------------------

st.header("📍 3. Fault Position Detection")

fault_data = pd.DataFrame(
    {
        "Detected Fault": faults,
        "Possible Fault Position": positions
    }
)

st.dataframe(
    fault_data,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 4 - COMPONENT HEALTH
# ---------------------------------------------------------

st.header("📈 4. Component Health Chart")

components = [
    "Temperature System",
    "Bearings",
    "Electrical System",
    "Drive System",
    "Machine Specific Part"
]

health = [100, 100, 100, 100, 100]

if temperature > 85:
    health[0] = max(20, 100 - risk)

if vibration > 7:
    health[1] = max(20, 100 - risk)

if current > 50:
    health[2] = max(20, 100 - risk)

if rpm < 500 or rpm > 3500:
    health[3] = max(20, 100 - risk)

if machine == "Reciprocating Pump":
    if extra_value < 2 or extra_value > 20:
        health[4] = max(20, 100 - risk)

elif machine == "Hydraulic Turbine":
    if extra_value < 40 or extra_value > 400:
        health[4] = max(20, 100 - risk)

else:
    if extra_value < 2 or extra_value > 10:
        health[4] = max(20, 100 - risk)

chart = go.Figure(
    go.Bar(
        x=components,
        y=health
    )
)

chart.update_layout(
    title="Component Health Percentage",
    xaxis_title="Machine Component",
    yaxis_title="Health (%)",
    yaxis_range=[0, 100],
    height=400
)

st.plotly_chart(
    chart,
    use_container_width=True
)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 5 - MAINTENANCE RECOMMENDATIONS
# ---------------------------------------------------------

st.header("🔧 5. AI Maintenance Recommendation")

for item in recommendations:
    st.info(item)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 6 - SAVE READING
# ---------------------------------------------------------

st.header("💾 6. Save and Download Reading")

save_column, download_column = st.columns(2)

with save_column:

    if st.button("💾 Save Current Reading"):

        reading = {
            "Date and Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Machine": machine,
            "Temperature": temperature,
            "Vibration": vibration,
            "Current": current,
            "RPM": rpm,
            extra_name: extra_value,
            "Condition": condition,
            "Failure Risk": risk
        }

        st.session_state.saved_readings.append(reading)

        st.success("Reading saved successfully!")

with download_column:

    report = "AI PREDICTIVE MAINTENANCE REPORT\n\n"

    report += "Machine: " + machine + "\n"
    report += "Date: " + datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ) + "\n\n"

    report += "MACHINE READINGS\n"
    report += "Temperature: " + str(temperature) + " °C\n"
    report += "Vibration: " + str(vibration) + " mm/s\n"
    report += "Current: " + str(current) + " A\n"
    report += "RPM: " + str(rpm) + "\n"
    report += extra_name + ": " + str(extra_value) + "\n\n"

    report += "AI ANALYSIS\n"
    report += "Condition: " + condition + "\n"
    report += "Failure Risk: " + str(risk) + "%\n\n"

    report += "DETECTED FAULTS\n"

    for fault in faults:
        report += "- " + fault + "\n"

    report += "\nFAULT POSITIONS\n"

    for position in positions:
        report += "- " + position + "\n"

    report += "\nMAINTENANCE RECOMMENDATIONS\n"

    for recommendation in recommendations:
        report += "- " + recommendation + "\n"

    st.download_button(
        label="⬇️ Download Maintenance Report",
        data=report,
        file_name="maintenance_report.txt",
        mime="text/plain"
    )

st.markdown("---")

# ---------------------------------------------------------
# SECTION 7 - SAVED READINGS
# ---------------------------------------------------------

st.header("📋 7. Saved Readings")

if len(st.session_state.saved_readings) > 0:

    saved_data = pd.DataFrame(
        st.session_state.saved_readings
    )

    st.dataframe(
        saved_data,
        use_container_width=True,
        hide_index=True
    )

    csv_data = saved_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download All Readings as CSV",
        data=csv_data,
        file_name="machine_readings.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No readings saved yet."
    )

st.markdown("---")

st.caption(
    "AI Predictive Maintenance System | Mechanical Engineering College Project"
)
