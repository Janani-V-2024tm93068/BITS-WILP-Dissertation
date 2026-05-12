import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
    font-family: 'Arial', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Release Readiness Dashboard", layout="wide")

st.title("Release Readiness Analytics Dashboard")

# Fetch Data from Flask API

url = "http://127.0.0.1:5000/readiness"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    st.error(f"API Error: {response.status_code}")
    st.text(response.text)
    st.stop()
    
df = pd.DataFrame(data)

df = df[
    [
        "Sprint",
        "StoryCompletionRate",
        "TestCoverage",
        "BuildSuccessRate",
        "OpenCriticalBugs",
        "DemoFeedback",
        "MustHaveCompletion",
        "ReadinessScore",
        "Status"
    ]
]

# KPI SUMMARY

st.subheader("Key Metrics Summary")

col1, col2, col3, col4 = st.columns(4)

avg_score = df["ReadinessScore"].mean()
total_sprints = len(df)
ready_sprints = len(df[df["Status"] == "READY"])
risky_sprints = len(df[df["ReadinessScore"] < 0.7])

col1.metric("Avg Readiness", round(avg_score, 2))
col2.metric("Total Sprints", total_sprints)
col3.metric("Ready Sprints", ready_sprints)
col4.metric("Risky Sprints", risky_sprints)


# Sprint Filter

st.subheader("Filter Sprint Data")

selected_sprint = st.selectbox(
    "Select Sprint",
    ["All"] + list(df["Sprint"])
)

filtered_df = df if selected_sprint == "All" else df[df["Sprint"] == selected_sprint]


# Data Table

st.subheader("Sprint Metrics Data")
st.dataframe(filtered_df)


# Bar Chart

st.subheader("Readiness Score per Sprint")
st.bar_chart(filtered_df.set_index("Sprint")["ReadinessScore"])


# Status Distribution

st.subheader(" Status Distribution")
status_counts = df["Status"].value_counts()
st.bar_chart(status_counts)


# Gauge Chart

st.subheader("Overall Release Readiness")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_score * 100,
    title={'text': "Release Readiness (%)"},
    gauge={
        'axis': {'range': [0, 100]},
        'steps': [
            {'range': [0, 60], 'color': "red"},
            {'range': [60, 80], 'color': "orange"},
            {'range': [80, 100], 'color': "green"}
        ]
    }
))

st.plotly_chart(fig, width="stretch")


# Trend Chart

st.subheader("Readiness Trend Across Sprints")

st.line_chart(df.set_index("Sprint")["ReadinessScore"])


# Risk Detection

st.subheader("Risk Detection")

risk_sprints = df[df["ReadinessScore"] < 0.7]

if len(risk_sprints) > 0:
    for index, row in risk_sprints.iterrows():
        st.error(f" {row['Sprint']} has LOW readiness ({row['ReadinessScore']})")
else:
    st.success("No high-risk sprints detected")


# Sprint Health Status

st.subheader("Sprint Health Status")

for index, row in filtered_df.iterrows():
    if row["Status"] == "READY":
        st.success(f"{row['Sprint']} → READY (Score: {row['ReadinessScore']})")
    elif row["Status"] == "CONDITIONAL":
        st.warning(f"{row['Sprint']} → CONDITIONAL (Score: {row['ReadinessScore']})")
    else:
        st.error(f"{row['Sprint']} → NOT READY (Score: {row['ReadinessScore']})")