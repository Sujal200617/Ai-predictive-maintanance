import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Predictive Maintenance System",
    page_icon="⚙️",
    layout="wide"
)


# ---------------------------------------------------
# MACHINE DATABASE
# ---------------------------------------------------

MACHINES = {

    "🚗 Petrol Engine": {

        "description": """
        This module monitors the health of a petrol engine by analysing
        engine temperature, vibration, engine RPM, oil pressure and battery voltage.
        """,

        "sensors": [

            {
                "name": "Engine Temperature",
                "unit": "°C",
                "min": 20.0,
                "max": 130.0,
                "default": 85.0,
                "step": 0.5,
                "normal_min": 70,
                "normal_max": 100,
                "warning_max": 110
            },

            {
                "name": "Vibration",
                "unit": "mm/s",
                "min": 0.0,
                "max": 15.0,
                "default": 2.0,
                "step": 0.1,
                "normal_min": 0,
                "normal_max": 4,
                "warning_max": 6
            },

            {
                "name": "Engine RPM",
                "unit": "RPM",
                "min": 0,
                "max": 7000,
                "default": 1500,
                "step": 50,
                "normal_min": 700,
                "normal_max": 4000,
                "warning_max": 6000
            },

            {
                "name": "Oil Pressure",
                "unit": "bar",
                "min": 0.0,
                "max": 10.0,
                "default": 4.0,
                "step": 0.1,
                "normal_min": 2,
                "normal_max": 6,
                "warning_max": 8
            },

            {
                "name": "Battery Voltage",
                "unit": "V",
                "min": 0.0,
                "max": 16.0,
                "default": 13.5,
                "step": 0.1,
                "normal_min": 12,
                "normal_max": 14.5,
                "warning_max": 15.5
            }
        ],

        "faults": {

            "High Temperature":
            "Possible engine overheating. Check the cooling system, coolant level and engine load.",

            "High Vibration":
            "Possible engine imbalance, worn bearings or loose engine mounting.",

            "Low RPM":
            "Possible engine performance or fuel system problem.",

            "High RPM":
            "Possible excessive engine speed or abnormal operating condition.",

            "Low Oil Pressure":
            "Possible lubrication problem. Inspect engine oil level and lubrication system.",

            "High Oil Pressure":
            "Possible restriction in the lubrication system.",

            "Low Battery Voltage":
            "Possible battery or charging system problem.",

            "High Battery Voltage":
            "Possible alternator or voltage regulator problem."
        }
    },


    # ---------------------------------------------------
    # RECIPROCATING PUMP
    # ---------------------------------------------------

    "🔧 Reciprocating Pump": {

        "description": """
        This module monitors a reciprocating pump using mechanical,
        pressure and flow-related parameters.
        """,

        "sensors": [

            {
                "name": "Temperature",
                "unit": "°C",
                "min": 20.0,
                "max": 100.0,
                "default": 48.0,
                "step": 0.5,
                "normal_min": 20,
                "normal_max": 70,
                "warning_max": 80
            },

            {
                "name": "Vibration",
                "unit": "mm/s",
                "min": 0.0,
                "max": 15.0,
                "default": 2.5,
                "step": 0.1,
                "normal_min": 0,
                "normal_max": 4,
                "warning_max": 6
            },

            {
                "name": "Motor Current",
                "unit": "A",
                "min": 0.0,
                "max": 8.0,
                "default": 2.2,
                "step": 0.1,
                "normal_min": 0,
                "normal_max": 3,
                "warning_max": 4
            },

            {
                "name": "RPM",
                "unit": "RPM",
                "min": 500,
                "max": 2500,
                "default": 1200,
                "step": 10,
                "normal_min": 900,
                "normal_max": 1600,
                "warning_max": 2000
            },

            {
                "name": "Discharge Pressure",
                "unit": "bar",
                "min": 0.0,
                "max": 15.0,
                "default": 5.0,
                "step": 0.1,
                "normal_min": 3,
                "normal_max": 9,
                "warning_max": 12
            },

            {
                "name": "Flow Rate",
                "unit": "L/min",
                "min": 0.0,
                "max": 50.0,
                "default": 16.0,
                "step": 0.5,
                "normal_min": 8,
                "normal_max": 30,
                "warning_max": 40
            }
        ],

        "faults": {

            "High Temperature":
            "Inspect bearings and mechanical loading.",

            "High Vibration":
            "Possible bearing problem, loose mounting or connecting mechanism problem.",

            "High Current":
            "Possible overload or excessive mechanical resistance.",

            "Low Pressure":
            "Possible valve leakage or discharge problem.",

            "High Pressure":
            "Possible blockage in the discharge system.",

            "Low Flow":
            "Possible valve problem, leakage or flow restriction.",

            "Abnormal RPM":
            "Inspect the motor drive and mechanical system."
        }
    },


    # ---------------------------------------------------
    # HYDRAULIC TURBINE
    # ---------------------------------------------------

    "⚡ Hydraulic Turbine": {

        "description": """
        This module monitors the operating condition of a hydraulic turbine
        using mechanical and hydraulic parameters.
        """,

        "sensors": [

            {
                "name": "Temperature",
                "unit": "°C",
                "min": 20.0,
                "max": 110.0,
                "default": 50.0,
                "step": 0.5,
                "normal_min": 20,
                "normal_max": 75,
                "warning_max": 85
            },

            {
                "name": "Vibration",
                "unit": "mm/s",
                "min": 0.0,
                "max": 15.0,
                "default": 2.2,
                "step": 0.1,
                "normal_min": 0,
                "normal_max": 4,
                "warning_max": 6
            },

            {
                "name": "RPM",
                "unit": "RPM",
                "min": 500,
                "max": 3000,
                "default": 1500,
                "step": 10,
                "normal_min": 1200,
                "normal_max": 2000,
                "warning_max": 2300
            },

            {
                "name": "Pressure",
                "unit": "bar",
                "min": 0.0,
                "max": 20.0,
                "default": 8.0,
                "step": 0.1,
                "normal_min": 5,
                "normal_max": 12,
                "warning_max": 16
            },

            {
                "name": "Flow Rate",
                "unit": "L/s",
                "min": 0.0,
                "max": 100.0,
                "default": 25.0,
                "step": 0.5,
                "normal_min": 15,
                "normal_max": 60,
                "warning_max": 80
            }
        ],

        "faults": {

            "High Temperature":
            "Inspect bearings, lubrication and operating load.",

            "High Vibration":
            "Possible shaft imbalance, bearing problem or loose mounting.",

            "Low RPM":
            "Check hydraulic supply and mechanical resistance.",

            "High RPM":
            "Check turbine operating conditions and control system.",

            "Low Pressure":
            "Possible insufficient hydraulic supply.",

            "High Pressure":
            "Inspect hydraulic system operating conditions.",

            "Low Flow":
            "Possible restriction in the water supply system."
        }
    }
}


# ---------------------------------------------------
# INITIALISE HISTORY
# ---------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------------------------------
# ANALYSIS FUNCTION
# ---------------------------------------------------

def analyse_machine(machine_name, sensor_data):

    risk = 0
    problems = []

    for sensor in sensor_data:

        name = sensor["name"]
        value = sensor["value"]

        normal_min = sensor["normal_min"]
        normal_max = sensor["normal_max"]
        warning_max = sensor["warning_max"]

        # TEMPERATURE
        if "Temperature" in name:

            if value > warning_max:
                risk += 30
                problems.append("High Temperature")

            elif value > normal_max:
                risk += 15
                problems.append("High Temperature")

        # VIBRATION
        elif name == "Vibration":

            if value > warning_max:
                risk += 35
                problems.append("High Vibration")

            elif value > normal_max:
                risk += 20
                problems.append("High Vibration")

        # MOTOR CURRENT
        elif name == "Motor Current":

            if value > warning_max:
                risk += 25
                problems.append("High Current")

            elif value > normal_max:
                risk += 15
                problems.append("High Current")

        # ENGINE RPM
        elif name == "Engine RPM":

            if value < normal_min:
                risk += 20
                problems.append("Low RPM")

            elif value > warning_max:
                risk += 25
                problems.append("High RPM")

        # NORMAL RPM
        elif name == "RPM":

            if value < normal_min:

                if machine_name == "⚡ Hydraulic Turbine":
                    problems.append("Low RPM")
                else:
                    problems.append("Abnormal RPM")

                risk += 20

            elif value > warning_max:

                if machine_name == "⚡ Hydraulic Turbine":
                    problems.append("High RPM")
                else:
                    problems.append("Abnormal RPM")

                risk += 20

        # OIL PRESSURE
        elif name == "Oil Pressure":

            if value < normal_min:
                risk += 30
                problems.append("Low Oil Pressure")

            elif value > warning_max:
                risk += 20
                problems.append("High Oil Pressure")

        # NORMAL PRESSURE
        elif "Pressure" in name:

            if value < normal_min:
                risk += 20
                problems.append("Low Pressure")

            elif value > warning_max:
                risk += 20
                problems.append("High Pressure")

        # BATTERY VOLTAGE
        elif name == "Battery Voltage":

            if value < normal_min:
                risk += 20
                problems.append("Low Battery Voltage")

            elif value > warning_max:
                risk += 20
                problems.append("High Battery Voltage")

        # FLOW
        elif "Flow" in name:

            if value < normal_min:
                risk += 20
                problems.append("Low Flow")

    risk = min(risk, 100)

    problems = list(dict.fromkeys(problems))

    return risk, problems


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("⚙️ AI-Based Multipurpose Predictive Maintenance System")

st.write(
    "### Mechanical Engineering Smart Machine Health Monitoring Platform"
)

st.caption(
    "Petrol Engine • Reciprocating Pump • Hydraulic Turbine"
)


# ---------------------------------------------------
# MACHINE SELECTION
# ---------------------------------------------------

st.sidebar.title("⚙️ Control Panel")

machine_name = st.sidebar.selectbox(
    "Select Machine",
    list(MACHINES.keys())
)

machine = MACHINES[machine_name]

st.sidebar.markdown("---")

st.sidebar.subheader("📡 Sensor Inputs")

st.sidebar.caption(
    "Adjust the sensor values to simulate different machine conditions."
)


# ---------------------------------------------------
# SENSOR INPUTS
# ---------------------------------------------------

sensor_data = []

for sensor in machine["sensors"]:

    value = st.sidebar.slider(

        f'{sensor["name"]} ({sensor["unit"]})',

        min_value=sensor["min"],
        max_value=sensor["max"],
        value=sensor["default"],
        step=sensor["step"]
    )

    sensor_copy = sensor.copy()
    sensor_copy["value"] = value

    sensor_data.append(sensor_copy)


# ---------------------------------------------------
# ANALYSIS
# ---------------------------------------------------

risk, problems = analyse_machine(
    machine_name,
    sensor_data
)


# ---------------------------------------------------
# STATUS
# ---------------------------------------------------

if risk < 25:
    status = "HEALTHY"
    status_icon = "🟢"

elif risk < 60:
    status = "WARNING"
    status_icon = "🟡"

else:
    status = "FAULT RISK"
    status_icon = "🔴"


# ---------------------------------------------------
# MACHINE INFORMATION
# ---------------------------------------------------

st.divider()

st.subheader(machine_name)

st.write(machine["description"])


# ---------------------------------------------------
# MAIN METRICS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Machine Status",
    f"{status_icon} {status}"
)

col2.metric(
    "Risk Indicator",
    f"{risk}%"
)

col3.metric(
    "Detected Abnormalities",
    len(problems)
)


st.divider()


# ---------------------------------------------------
# HEALTH ANALYSIS
# ---------------------------------------------------

left_column, right_column = st.columns(2)


with left_column:

    st.subheader("🤖 Predictive Health Analysis")

    st.progress(risk / 100)

    if status == "HEALTHY":

        st.success(
            "The machine is operating within the normal range."
        )

    elif status == "WARNING":

        st.warning(
            "Abnormal operating conditions have been detected. Inspection is recommended."
        )

    else:

        st.error(
            "High-risk operating condition detected. Maintenance attention is required."
        )

    st.subheader("🔍 Possible Fault Diagnosis")

    if len(problems) == 0:

        st.success("No abnormal condition detected.")

    else:

        for problem in problems:

            st.write(f"### ⚠️ {problem}")

            if problem in machine["faults"]:

                st.write(machine["faults"][problem])


with right_column:

    st.subheader("📊 Sensor Readings")

    table_data = []

    for sensor in sensor_data:

        value = sensor["value"]

        if sensor["normal_min"] <= value <= sensor["normal_max"]:

            sensor_status = "🟢 Normal"

        else:

            sensor_status = "🟡 Check"

        table_data.append({

            "Parameter": sensor["name"],
            "Value": value,
            "Unit": sensor["unit"],
            "Status": sensor_status

        })

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------
# GRAPH
# ---------------------------------------------------

st.divider()

st.subheader("📈 Current Machine Parameters")

parameter_names = []
parameter_values = []

for sensor in sensor_data:

    parameter_names.append(sensor["name"])
    parameter_values.append(sensor["value"])


fig = go.Figure()

fig.add_trace(

    go.Bar(
        x=parameter_names,
        y=parameter_values,
        text=parameter_values,
        textposition="auto"
    )
)

fig.update_layout(
    title="Current Sensor Readings",
    xaxis_title="Machine Parameters",
    yaxis_title="Sensor Values",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------

st.divider()

st.subheader("💾 Machine Reading History")

if st.button("➕ Save Current Reading"):

    history_entry = {

        "Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Machine": machine_name,

        "Status": status,

        "Risk (%)": risk
    }

    for sensor in sensor_data:

        history_entry[sensor["name"]] = sensor["value"]

    st.session_state.history.append(
        history_entry
    )

    st.success(
        "Current machine reading saved successfully!"
    )


if len(st.session_state.history) > 0:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download Maintenance Data (CSV)",

        data=csv,

        file_name="machine_maintenance_data.csv",

        mime="text/csv"
    )

else:

    st.info(
        "No readings have been saved yet."
    )


# ---------------------------------------------------
# SYSTEM WORKING
# ---------------------------------------------------

st.divider()

st.subheader("🔄 How the System Works")

st.markdown("""

### System Flow

**Machine**

⬇️

**Sensors**

⬇️

**Data Collection**

⬇️

**AI-Based Analysis**

⬇️

**Machine Health Status**

⬇️

**Fault Diagnosis**

⬇️

**Maintenance Recommendation**

""")


# ---------------------------------------------------
# PROJECT INFORMATION
# ---------------------------------------------------

st.divider()

st.subheader("🎓 Project Machines")

st.markdown("""

### 🚗 Petrol Engine
Monitors engine temperature, vibration, RPM, oil pressure and battery voltage.

### 🔧 Reciprocating Pump
Monitors temperature, vibration, motor current, RPM, pressure and flow rate.

### ⚡ Hydraulic Turbine
Monitors temperature, vibration, RPM, hydraulic pressure and water flow rate.

""")


st.divider()

st.info("""

🎓 PROJECT NOTE

This is a multipurpose predictive maintenance prototype for mechanical
engineering applications.

Currently, the system uses engineering-based threshold analysis.

In the future, real sensors, ESP32/Arduino and machine-learning models
can be connected for real-time predictive maintenance.

""")
