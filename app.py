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
# PROFESSIONAL DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #07111f;
    color: #eef3f8;
}

[data-testid="stSidebar"] {
    background-color: #0a1524;
}

[data-testid="stMetric"] {
    background-color: #0d1a2a;
    border: 1px solid #21354a;
    border-radius: 12px;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MACHINE DATABASE
# =========================================================

MACHINES = {

    "Petrol Engine": {
        "icon": "🚗",
        "parameters": {
            "Temperature (°C)": (20.0, 140.0, 88.0, 70.0, 100.0),
            "Vibration (mm/s)": (0.0, 20.0, 3.2, 0.0, 5.0),
            "RPM": (500.0, 8000.0, 2450.0, 700.0, 6000.0),
            "Oil Pressure (bar)": (0.0, 10.0, 4.1, 2.0, 6.0)
        }
    },

    "Reciprocating Pump": {
        "icon": "🔧",
        "parameters": {
            "Temperature (°C)": (20.0, 120.0, 65.0, 40.0, 90.0),
            "Vibration (mm/s)": (0.0, 20.0, 2.5, 0.0, 4.5),
            "Pressure (bar)": (0.0, 20.0, 8.0, 5.0, 12.0),
            "Flow Rate (L/min)": (0.0, 200.0, 90.0, 60.0, 140.0)
        }
    },

    "Hydraulic Turbine": {
        "icon": "⚡",
        "parameters": {
            "Temperature (°C)": (20.0, 120.0, 55.0, 30.0, 80.0),
            "Vibration (mm/s)": (0.0, 20.0, 2.0, 0.0, 4.0),
            "RPM": (100.0, 5000.0, 1800.0, 800.0, 3500.0),
            "Water Flow (L/s)": (0.0, 500.0, 180.0, 100.0, 350.0)
        }
    }

}


# =========================================================
# SESSION STATE
# =========================================================

if "readings" not in st.session_state:
    st.session_state.readings = {}

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def reading_key(machine, parameter):
    return machine + "__" + parameter


def calculate_data(machine):

    values = {}
    risks = {}

    parameters = MACHINES[machine]["parameters"]

    for name, limits in parameters.items():

        minimum = limits[0]
        maximum = limits[1]
        default = limits[2]
        normal_min = limits[3]
        normal_max = limits[4]

        key = reading_key(machine, name)

        value = float(
            st.session_state.readings.get(
                key,
                default
            )
        )

        values[name] = value

        if normal_min <= value <= normal_max:

            risk = 0.0

        elif value < normal_min:

            difference = normal_min - value
            range_value = normal_min - minimum

            if range_value == 0:
                risk = 0.0
            else:
                risk = (difference / range_value) * 100

        else:

            difference = value - normal_max
            range_value = maximum - normal_max

            if range_value == 0:
                risk = 0.0
            else:
                risk = (difference / range_value) * 100

        risk = max(0.0, min(risk, 100.0))

        risks[name] = round(risk, 1)

    total_risk = round(
        sum(risks.values()) / len(risks),
        1
    )

    health_score = round(
        100 - total_risk,
        1
    )

    fault_parameter = max(
        risks,
        key=risks.get
    )

    return (
        values,
        risks,
        total_risk,
        health_score,
        fault_parameter
    )


def get_status(risk):

    if risk <= 20:
        return "HEALTHY"

    if risk <= 50:
        return "WARNING"

    return "HIGH RISK"


def get_risk_color(risk):

    if risk <= 20:
        return "#36c76b"

    if risk <= 50:
        return "#f5c542"

    return "#ef5350"


def get_recommendation(parameter):

    recommendations = {

        "Temperature (°C)":
        "Inspect the cooling system and check for overheating.",

        "Vibration (mm/s)":
        "Inspect bearings, alignment and loose mounting components.",

        "RPM":
        "Inspect the speed control system and mechanical load.",

        "Oil Pressure (bar)":
        "Check oil level, lubrication system and possible leakage.",

        "Pressure (bar)":
        "Inspect valves, seals and the pressure system.",

        "Flow Rate (L/min)":
        "Inspect the suction line, valves and possible blockage.",

        "Water Flow (L/s)":
        "Inspect water inlet, guide system and water supply."
    }

    return recommendations.get(
        parameter,
        "Perform a complete machine inspection."
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ AI-PMS")

    st.caption(
        "AI Predictive Maintenance System"
    )

    st.divider()

    machine = st.selectbox(
        "SELECT MACHINE",
        list(MACHINES.keys())
    )

    st.caption(
        "Choose the machine to monitor"
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📡 Live Monitoring",
            "⚠️ Fault Diagnosis",
            "📜 History & Records",
            "📊 Reports",
            "⚙️ Settings",
            "ℹ️ About System"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.success("🟢 System Online")

    st.caption(
        MACHINES[machine]["icon"]
        + " "
        + machine
    )


# =========================================================
# GET CURRENT MACHINE DATA
# =========================================================

values, risks, total_risk, health_score, fault_parameter = calculate_data(machine)

machine_status = get_status(total_risk)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("AI Predictive Maintenance System")

    st.caption(
        "Intelligent Machine Monitoring & Fault Diagnosis"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "MACHINE STATUS",
            machine_status
        )

    with col2:

        st.metric(
            "HEALTH SCORE",
            str(health_score) + "%"
        )

    with col3:

        st.metric(
            "RISK OF FAILURE",
            str(total_risk) + "%"
        )

    with col4:

        sensor_count = len(values)

        st.metric(
            "SENSORS ACTIVE",
            str(sensor_count)
            + " / "
            + str(sensor_count)
        )

    st.divider()

    left, right = st.columns(2)

    # -----------------------------------------------------
    # FAULT DIAGNOSIS
    # -----------------------------------------------------

    with left:

        st.subheader("⚠️ Fault Diagnosis")

        bar_chart = go.Figure(
            go.Bar(
                x=list(risks.keys()),
                y=list(risks.values()),
                marker_color=[
                    get_risk_color(value)
                    for value in risks.values()
                ],
                text=[
                    str(value) + "%"
                    for value in risks.values()
                ],
                textposition="auto"
            )
        )

        bar_chart.update_layout(
            title="Fault Severity by Parameter",
            yaxis_title="Severity (%)",
            yaxis_range=[0, 100],
            paper_bgcolor="#07111f",
            plot_bgcolor="#07111f",
            font=dict(color="#eef3f8"),
            height=400
        )

        st.plotly_chart(
            bar_chart,
            use_container_width=True
        )

        st.subheader("📍 Primary Fault Location")

        st.warning(
            "Primary fault location: "
            + fault_parameter
        )

        st.subheader("🛠 Recommendation")

        st.info(
            get_recommendation(
                fault_parameter
            )
        )

    # -----------------------------------------------------
    # RISK ANALYSIS
    # -----------------------------------------------------

    with right:

        st.subheader(
            "📊 Risk of Failure Analysis"
        )

        gauge_chart = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=total_risk,
                number={
                    "suffix": "%"
                },
                title={
                    "text": "Failure Risk"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": get_risk_color(
                            total_risk
                        )
                    },

                    "steps": [

                        {
                            "range": [0, 20],
                            "color": "#183d29"
                        },

                        {
                            "range": [20, 50],
                            "color": "#443b16"
                        },

                        {
                            "range": [50, 100],
                            "color": "#451b20"
                        }

                    ]
                }
            )
        )

        gauge_chart.update_layout(
            paper_bgcolor="#07111f",
            font=dict(color="#eef3f8"),
            height=400
        )

        st.plotly_chart(
            gauge_chart,
            use_container_width=True
        )

        st.subheader(
            "Machine Condition"
        )

        if total_risk <= 20:

            st.success(
                "The machine is operating within safe limits."
            )

        elif total_risk <= 50:

            st.warning(
                "The machine requires preventive inspection."
            )

        else:

            st.error(
                "High failure risk detected. Immediate inspection is recommended."
            )

    # -----------------------------------------------------
    # LIVE SENSOR TABLE
    # -----------------------------------------------------

    st.divider()

    st.subheader("📡 Live Sensor Readings")

    table_rows = []

    for name, value in values.items():

        parameter_risk = risks[name]

        table_rows.append(
            {
                "Parameter": name,
                "Current Value": value,
                "Risk (%)": parameter_risk,
                "Status": get_status(parameter_risk)
            }
        )

    sensor_dataframe = pd.DataFrame(
        table_rows
    )

    st.dataframe(
        sensor_dataframe,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# LIVE MONITORING PAGE
# =========================================================

elif page == "📡 Live Monitoring":

    st.title("📡 Live Monitoring")

    st.caption(
        "Adjust sensor readings for "
        + machine
    )

    st.divider()

    parameters = MACHINES[machine]["parameters"]

    columns = st.columns(2)

    index = 0

    for name, limits in parameters.items():

        minimum = float(limits[0])
        maximum = float(limits[1])
        default = float(limits[2])
        normal_min = float(limits[3])
        normal_max = float(limits[4])

        current_key = reading_key(
            machine,
            name
        )

        slider_key = (
            current_key
            + "_slider"
        )

        current_value = float(
            st.session_state.readings.get(
                current_key,
                default
            )
        )

        with columns[index % 2]:

            value = st.slider(
                name,
                min_value=minimum,
                max_value=maximum,
                value=current_value,
                key=slider_key
            )

            st.session_state.readings[
                current_key
            ] = value

            st.caption(
                "Normal range: "
                + str(normal_min)
                + " to "
                + str(normal_max)
            )

        index += 1

    st.divider()

    if st.button(
        "🔄 UPDATE READINGS",
        use_container_width=True
    ):

        st.success(
            "Sensor readings updated successfully."
        )

    (
        values,
        risks,
        total_risk,
        health_score,
        fault_parameter
    ) = calculate_data(machine)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Health Score",
            str(health_score) + "%"
        )

    with col2:

        st.metric(
            "Failure Risk",
            str(total_risk) + "%"
        )

    with col3:

        st.metric(
            "Machine Status",
            get_status(total_risk)
        )


# =========================================================
# FAULT DIAGNOSIS PAGE
# =========================================================

elif page == "⚠️ Fault Diagnosis":

    st.title("⚠️ Fault Diagnosis")

    st.caption(
        "AI-based parameter analysis"
    )

    st.divider()

    st.subheader(
        "Fault Severity by Parameter"
    )

    diagnosis_rows = []

    for name in risks:

        diagnosis_rows.append(
            {
                "Parameter": name,
                "Severity (%)": risks[name],
                "Condition": get_status(
                    risks[name]
                )
            }
        )

    diagnosis_dataframe = pd.DataFrame(
        diagnosis_rows
    )

    st.dataframe(
        diagnosis_dataframe,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "📍 Primary Fault Location"
    )

    st.warning(
        fault_parameter
    )

    st.subheader(
        "🛠 Recommended Maintenance Action"
    )

    st.info(
        get_recommendation(
            fault_parameter
        )
    )


# =========================================================
# HISTORY PAGE
# =========================================================

elif page == "📜 History & Records":

    st.title("📜 History & Records")

    st.caption(
        "Saved machine monitoring records"
    )

    st.divider()

    if len(
        st.session_state.history
    ) == 0:

        st.info(
            "No saved records yet. "
            "Save a reading from the Reports page."
        )

    else:

        history_dataframe = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_dataframe,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        if st.button(
            "🗑️ CLEAR HISTORY"
        ):

            st.session_state.history = []

            st.success(
                "History cleared successfully."
            )


# =========================================================
# REPORTS PAGE
# =========================================================

elif page == "📊 Reports":

    st.title("📊 Save & Report")

    st.caption(
        "Save current machine readings"
    )

    st.divider()

    st.subheader(
        "💾 Save Current Reading"
    )

    if st.button(
        "💾 SAVE READING",
        use_container_width=True
    ):

        record = {

            "Date & Time":
            datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            ),

            "Machine":
            machine,

            "Health Score (%)":
            health_score,

            "Risk (%)":
            total_risk,

            "Status":
            machine_status
        }

        for name, value in values.items():

            record[name] = value

        st.session_state.history.append(
            record
        )

        st.success(
            "Reading saved successfully."
        )

    st.divider()

    st.subheader(
        "📥 Download Report"
    )

    report_rows = []

    for name, value in values.items():

        report_rows.append(
            {
                "Parameter": name,
                "Current Value": value,
                "Risk (%)": risks[name],
                "Status": get_status(
                    risks[name]
                )
            }
        )

    report_dataframe = pd.DataFrame(
        report_rows
    )

    csv_data = report_dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ DOWNLOAD CSV REPORT",
        data=csv_data,
        file_name="predictive_maintenance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "🖨 Print Report"
    )

    st.caption(
        "To print the report, use your browser's print option."
    )


# =========================================================
# SETTINGS PAGE
# =========================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.caption(
        "Configure the monitoring system"
    )

    st.divider()

    alert_enabled = st.checkbox(
        "Enable fault alerts",
        value=True
    )

    monitoring_enabled = st.checkbox(
        "Enable automatic monitoring",
        value=True
    )

    critical_alerts = st.checkbox(
        "Enable critical risk alerts",
        value=True
    )

    if st.button(
        "SAVE SETTINGS"
    ):

        st.success(
            "Settings saved successfully."
        )


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "ℹ️ About System":

    st.title("ℹ️ About System")

    st.divider()

    st.markdown(
        """
### AI Predictive Maintenance System

This project is designed to monitor important machine operating
parameters and identify possible faults before they become serious.

### Supported Machines

- 🚗 Petrol Engine
- 🔧 Reciprocating Pump
- ⚡ Hydraulic Turbine

### Parameters Monitored

Depending on the selected machine, the system monitors:

- Temperature
- Vibration
- RPM
- Pressure
- Flow Rate
- Water Flow

### System Workflow

**Machine → Sensors → Data Collection → AI Analysis → Fault Diagnosis → Maintenance Action**

This application can later be connected with real sensors such as
temperature, vibration, RPM, pressure and flow sensors.
        """
    )
