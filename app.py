import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

st.set_page_config(page_title="AI Predictive Maintenance", page_icon="⚙️", layout="wide")
DATA_FILE = Path(__file__).parent / "training_data.csv"

@st.cache_resource
def train_model():
    df = pd.read_csv(DATA_FILE)
    X = df[["temperature", "vibration", "current", "rpm"]]
    y = df["status"]
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=150, random_state=42, class_weight="balanced"))
    ])
    model.fit(X, y)
    return model

model = train_model()

st.title("⚙️ AI Predictive Maintenance System")
st.caption("College prototype — machine condition monitoring and failure-risk prediction")

with st.sidebar:
    st.header("Machine Sensor Input")
    temperature = st.slider("Temperature (°C)", 20.0, 100.0, 45.0, 0.5)
    vibration = st.slider("Vibration (mm/s)", 0.0, 15.0, 2.0, 0.1)
    current = st.slider("Motor Current (A)", 0.2, 8.0, 1.8, 0.1)
    rpm = st.slider("RPM", 500, 3000, 1500, 10)
    st.info("Later, these controls can be replaced by Arduino/ESP32 sensor readings.")

sample = pd.DataFrame([{
    "temperature": temperature, "vibration": vibration,
    "current": current, "rpm": rpm
}])

prediction = model.predict(sample)[0]
prob = model.predict_proba(sample)[0]
probabilities = dict(zip(model.classes_, prob))
risk = 1 - probabilities.get("Healthy", 0)

if prediction == "Healthy":
    status_text, icon = "HEALTHY", "🟢"
elif prediction == "Warning":
    status_text, icon = "WARNING", "🟡"
else:
    status_text, icon = "FAULT RISK", "🔴"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Temperature", f"{temperature:.1f} °C")
c2.metric("Vibration", f"{vibration:.1f} mm/s")
c3.metric("Current", f"{current:.1f} A")
c4.metric("RPM", f"{rpm:d}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Machine Condition")
    st.markdown(f"## {icon} {status_text}")
    st.progress(float(min(max(risk, 0), 1)))
    st.write(f"**Failure-risk indicator:** {risk*100:.1f}%")
    if prediction == "Healthy":
        st.success("Machine parameters are within the healthy training range.")
    elif prediction == "Warning":
        st.warning("Abnormal conditions detected. Inspect the machine soon.")
    else:
        st.error("High-risk condition detected. Follow your project's safety procedure.")

with right:
    st.subheader("AI Class Probabilities")
    pdf = pd.DataFrame({"Condition": list(probabilities.keys()),
                        "Probability": [v*100 for v in probabilities.values()]})
    fig = go.Figure(go.Bar(x=pdf["Condition"], y=pdf["Probability"]))
    fig.update_layout(yaxis_title="Probability (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Sensor Overview")
chart = pd.DataFrame({
    "Parameter": ["Temperature", "Vibration", "Current", "RPM"],
    "Value": [temperature, vibration, current, rpm]
})
fig2 = go.Figure(go.Bar(x=chart["Parameter"], y=chart["Value"]))
fig2.update_layout(yaxis_title="Value")
st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("System Flow")
st.code("Sensors → Arduino/ESP32 → Python → Machine Learning → Dashboard → Alert")
st.caption("The included dataset is synthetic demonstration data. For a real project, collect labeled readings from your own machine and retrain the model.")
