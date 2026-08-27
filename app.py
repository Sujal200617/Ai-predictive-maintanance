import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO


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

st.markdown(
    """
    <style>

    .stApp {
        background-color: #07111f;
        color: #e8eef7;
    }

    [data-testid="stSidebar"] {
        background-color: #091524;
        border-right: 1px solid #1d3045;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #f4f7fb;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 16px;
        color: #9eafc2;
        margin-top: -5px;
        margin-bottom: 25px;
    }

    .card {
        background: linear-gradient(145deg, #0c1929, #0a1523);
        border: 1px solid #20364d;
        border-radius: 12px;
        padding: 22px;
        min-height: 150px;
    }

    .card-title {
        font-size: 14px;
        color: #aebdce;
        font-weight: 600;
        text-align: center;
    }

    .card-value {
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-top: 15px;
    }

    .card-text {
        font-size: 15px;
        text-align: center;
        color: #9eafc2;
    }

    .section-box {
        background-color: #0a1625;
        border: 1px solid #20364d;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }

    .healthy {
        color: #46d369;
        font-weight: bold;
    }

    .warning {
        color: #ffca28;
        font-weight: bold;
    }

    .danger {
        color: #ff4d4d;
        font-weight: bold;
    }

    .small-label {
        color: #9eafc2;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MACHINE PROFILES
# =========================================================

MACHINES = {

    "Petrol Engine": {
        "icon": "🚗",
        "parameters": {
            "Temperature (°C)": [20, 140, 88, 70, 100],
            "Vibration (mm/s)": [0.0, 20.0, 3.2, 0.0, 5.0],
            "RPM": [500, 8000, 2450, 700, 6000],
            "Oil Pressure (bar)": [0.0, 10.0, 4.1, 2.0, 6.0]
        }
    },

    "Reciprocating Pump": {
        "icon": "🔧",
        "parameters": {
            "Temperature (°C)": [20, 120, 65, 40, 90],
            "Vibration (mm/s)": [0.0, 20.0, 2.5, 0.0, 4.5],
            "Pressure (bar)": [0.0, 20.0, 8.0, 5.0, 12.0],
            "Flow Rate (L/min)": [0.0, 200.0, 90.0, 60.0, 140.0]
        }
    },

    "Hydraulic Turbine": {
        "icon": "⚡",
        "parameters": {
            "Temperature (°C)": [20, 120, 55, 30, 80],
            "Vibration (mm/s)": [0.0, 20.0, 2.0, 0.0, 4.0],
            "RPM": [100, 5000, 1800, 800, 3500],
            "Water Flow (L/s)": [0.0, 500.0, 180.0, 100.0, 350.0]
        }
    }
}


# =========================================================
# SESSION STATE
# =========================================================

if "machine" not in st.session_state:
    st.session_state.machine = "Petrol Engine"

if "readings" not in st.session_state:
    st.session_state.readings = {}

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# FUNCTIONS
# =========================================================

def calculate_parameter_risk(value, normal_min, normal_max, min_value, max_value):

    if normal_min <= value <= normal_max:
        return 0

    if value < normal_min:
        distance = normal_min - value
        total = normal_min - min_value
    else:
        distance = value - normal_max
        total = max_value - normal_max

    if total <= 0:
        return 0

    risk = (distance / total) * 100

    return min(round(risk, 1), 100)


def get_system_data():

    machine = st.session_state.machine
    profile = MACHINES[machine]

    parameters = profile["parameters"]

    values = {}
    risks = {}

    for name, data in parameters.items():

        minimum = data[0]
        maximum = data[1]
        default = data[2]
        normal_min = data[3]
        normal_max = data[4]

        value = st.session_state.readings.get(
            name,
            default
        )

        values[name] = value

        risks[name] = calculate_parameter_risk(
            value,
            normal_min,
            normal_max,
            minimum,
            maximum
        )

    total_risk = round(
        sum(risks.values()) / len(risks),
        1
    )

    health_score = round(
        max(0, 100 - total_risk),
        1
    )

    if total_risk <= 20:
        status = "HEALTHY"
        status_class = "healthy"

    elif total_risk <= 50:
        status = "WARNING"
        status_class = "warning"

    else:
        status = "HIGH RISK"
        status_class = "danger"

    fault_parameter = max(
        risks,
        key=risks.get
    )

    return (
        values,
        risks,
        total_risk,
        health_score,
        status,
        status_class,
        fault_parameter
    )


def get_recommendation(parameter, machine):

    recommendations = {

        "Temperature (°C)":
        "Inspect the cooling system and check for overheating.",

        "Vibration (mm/s)":
        "Inspect bearings, alignment, mounting and rotating components.",

        "RPM":
        "Check the speed control system and mechanical load.",

        "Oil Pressure (bar)":
        "Inspect lubrication level, oil pump and possible leakage.",

        "Pressure (bar)":
        "Check valves, seals and the pressure system.",

        "Flow Rate (L/min)":
        "Inspect pump valves, suction line and possible blockage.",

        "Water Flow (L/s)":
        "Inspect turbine inlet, flow channel and water supply."
    }

    return recommendations.get(
        parameter,
        "Perform a complete machine inspection."
    )


def create_gauge(value, title, color):

    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={
                "text": title,
                "font": {"color": "#e8eef7"}
            },
            number={
                "font": {"color": "#ffffff"}
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#9eafc2"
                },

                "bar": {
                    "color": color
                },

                "bgcolor": "#0a1625",

                "steps": [
                    {
                        "range": [0, 20],
                        "color": "#153020"
                    },
                    {
                        "range": [20, 50],
                        "color": "#332b0d"
                    },
                    {
                        "range": [50, 100],
                        "color": "#351515"
                    }
                ]
            }
        )
    )

    figure.update_layout(
        height=260,
        paper_bgcolor="#0a1625",
        font_color="#e8eef7",
        margin=dict(l=20, r=20, t=50, b=10)
    )

    return figure


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# ⚙️ AI-PMS")
    st.caption("AI Predictive Maintenance System")

    st.divider()

    st.markdown("### SELECT MACHINE")

    machine = st.selectbox(
        "Choose a machine to monitor",
        list(MACHINES.keys()),
        index=list(MACHINES.keys()).index(
            st.session_state.machine
        )
    )

    st.session_state.machine = machine

    st.markdown(
        f"### {MACHINES[machine]['icon']} {machine}"
    )

    st.divider()

    st.markdown("### SYSTEM STATUS")
    st.success("🟢 System Online")

    st.caption(
        "Machine monitoring, fault detection and predictive maintenance"
    )


# =========================================================
# DASHBOARD PAGE
# =========================================================

def dashboard():

    (
        values,
        risks,
        total_risk,
        health_score,
        status,
        status_class,
        fault_parameter
    ) = get_system_data()

    machine = st.session_state.machine

    st.markdown(
        '<div class="main-title">AI Predictive Maintenance System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Intelligent Machine Monitoring & Fault Diagnosis</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">MACHINE STATUS</div>
            <div class="card-value {status_class}">{status}</div>
            <div class="card-text">{machine}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">HEALTH SCORE</div>
            <div class="card-value healthy">{health_score}%</div>
            <div class="card-text">Machine Health</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        risk_class = (
            "healthy"
            if total_risk <= 20
            else "warning"
            if total_risk <= 50
            else "danger"
        )

        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">RISK OF FAILURE</div>
            <div class="card-value {risk_class}">{total_risk}%</div>
            <div class="card-text">Failure Probability</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">SENSORS ACTIVE</div>
            <div class="card-value">4 / 4</div>
            <div class="card-text">All Sensors Online</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    left, right = st.columns([1, 1])

    with left:

        st.subheader("⚠️ Fault Diagnosis")

        chart = go.Figure(
            go.Bar(
                x=list(risks.keys()),
                y=list(risks.values()),
                marker_color=[
                    "#2ecc71"
                    if risk <= 20
                    else "#f1c40f"
                    if risk <= 50
                    else "#e74c3c"
                    for risk in risks.values()
                ]
            )
        )

        chart.update_layout(
            title="Fault Severity by Parameter",
            yaxis_title="Risk (%)",
            yaxis_range=[0, 100],
            paper_bgcolor="#0a1625",
            plot_bgcolor="#0a1625",
            font_color="#e8eef7",
            height=350
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        st.markdown("### Primary Fault Location")

        st.warning(
            f"⚠️ **{fault_parameter}** requires the most attention."
        )

        st.markdown("### Recommendation")

        st.info(
            get_recommendation(
                fault_parameter,
                machine
            )
        )

    with right:

        st.subheader("📊 Risk of Failure Analysis")

        color = (
            "#2ecc71"
            if total_risk <= 20
            else "#f1c40f"
            if total_risk <= 50
            else "#e74c3c"
        )

        st.plotly_chart(
            create_gauge(
                total_risk,
                "Failure Risk (%)",
                color
            ),
            use_container_width=True
        )

        if total_risk <= 20:
            st.success(
                "The machine is operating within safe limits."
            )

        elif total_risk <= 50:
            st.warning(
                "The machine requires inspection and preventive maintenance."
            )

        else:
            st.error(
                "High risk detected. Immediate inspection is recommended."
            )

    st.divider()

    st.subheader("📡 Live Sensor Readings")

    rows = []

    for parameter, value in values.items():

        risk = risks[parameter]

        if risk <= 20:
            parameter_status = "Normal"
        elif risk <= 50:
            parameter_status = "Warning"
        else:
            parameter_status = "Critical"

        rows.append(
            {
                "Parameter": parameter,
                "Current Value": value,
                "Risk (%)": risk,
                "Status": parameter_status
            }
        )

    dataframe = pd.DataFrame(rows)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# LIVE MONITORING PAGE
# =========================================================

def live_monitoring():

    machine = st.session_state.machine
    parameters = MACHINES[machine]["parameters"]

    st.title("📡 Live Monitoring")
    st.caption(
        f"Real-time sensor monitoring for {machine}"
    )

    st.divider()

    columns = st.columns(2)

    index = 0

    for parameter, data in parameters.items():

        with columns[index % 2]:

            value = st.slider(
                parameter,
                min_value=float(data[0]),
                max_value=float(data[1]),
                value=float(
                    st.session_state.readings.get(
                        parameter,
                        data[2]
                    )
                )
            )

            st.session_state.readings[parameter] = value

        index += 1

    st.divider()

    if st.button(
        "🔄 UPDATE READINGS",
        use_container_width=True
    ):
        st.success("Sensor readings updated successfully.")

    values, risks, total_risk, health_score, status, status_class, fault_parameter = get_system_data()

    st.subheader("Current Monitoring Status")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Health Score",
        f"{health_score}%"
    )

    col2.metric(
        "Failure Risk",
        f"{total_risk}%"
    )

    col3.metric(
        "Status",
        status
    )


# =========================================================
# FAULT DIAGNOSIS PAGE
# =========================================================

def fault_diagnosis():

    (
        values,
        risks,
        total_risk,
        health_score,
        status,
        status_class,
        fault_parameter
    ) = get_system_data()

    st.title("⚠️ Fault Diagnosis")
    st.caption(
        "AI-based machine condition analysis"
    )

    st.divider()

    st.subheader("Fault Severity Analysis")

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=list(risks.keys()),
            y=list(risks.values()),
            marker_color=[
                "#2ecc71"
                if value <= 20
                else "#f1c40f"
                if value <= 50
                else "#e74c3c"
                for value in risks.values()
            ]
        )
    )

    figure.update_layout(
        yaxis_title="Severity (%)",
        yaxis_range=[0, 100],
        paper_bgcolor="#0a1625",
        plot_bgcolor="#0a1625",
        font_color="#ffffff"
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )

    st.subheader("🔍 Primary Fault Location")

    risk_value = risks[fault_parameter]

    if risk_value <= 20:
        st.success(
            f"{fault_parameter}: Operating normally."
        )

    elif risk_value <= 50:
        st.warning(
            f"{fault_parameter}: Moderate fault risk detected."
        )

    else:
        st.error(
            f"{fault_parameter}: High fault risk detected."
        )

    st.subheader("🛠 Recommended Maintenance Action")

    st.info(
        get_recommendation(
            fault_parameter,
            st.session_state.machine
        )
    )


# =========================================================
# HISTORY PAGE
# =========================================================

def history_records():

    st.title("📜 History & Records")
    st.caption(
        "Saved machine monitoring readings"
    )

    st.divider()

    if len(st.session_state.history) == 0:

        st.info(
            "No readings have been saved yet. "
            "Go to Reports and save the current reading."
        )

    else:

        history_data = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "🗑 Clear History"
        ):
            st.session_state.history = []
            st.rerun()


# =========================================================
# REPORTS PAGE
# =========================================================

def reports():

    (
        values,
        risks,
        total_risk,
        health_score,
        status,
        status_class,
        fault_parameter
    ) = get_system_data()

    machine = st.session_state.machine

    st.title("📊 Save & Report")
    st.caption(
        "Save monitoring readings and generate reports"
    )

    st.divider()

    st.subheader("💾 Save Current Reading")

    if st.button(
        "💾 SAVE CURRENT READING",
        use_container_width=True
    ):

        record = {
            "Date & Time": datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            ),
            "Machine": machine,
            "Risk (%)": total_risk,
            "Health Score (%)": health_score,
            "Status": status
        }

        record.update(values)

        st.session_state.history.append(
            record
        )

        st.success(
            "Reading saved successfully."
        )

    st.divider()

    st.subheader("📥 Export Report")

    report_data = pd.DataFrame(
        [
            {
                "Parameter": parameter,
                "Current Value": values[parameter],
                "Risk (%)": risks[parameter]
            }
            for parameter in values
        ]
    )

    csv = report_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV Report",
        data=csv,
        file_name="predictive_maintenance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    excel_file = BytesIO()

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        report_data.to_excel(
            writer,
            index=False,
            sheet_name="Maintenance Report"
        )

    st.download_button(
        label="📊 Export to Excel",
        data=excel_file.getvalue(),
        file_name="predictive_maintenance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# =========================================================
# SETTINGS PAGE
# =========================================================

def settings():

    st.title("⚙️ Settings")
    st.caption(
        "Configure your AI Predictive Maintenance System"
    )

    st.divider()

    st.subheader("System Configuration")

    auto_update = st.checkbox(
        "Enable automatic monitoring
    
