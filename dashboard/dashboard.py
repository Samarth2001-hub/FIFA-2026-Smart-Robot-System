import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh
st.set_page_config(
    page_title="FIFA 2026 Smart Robot Dashboard",
    page_icon="🤖",
    layout="wide"
)
st_autorefresh(
    interval=5000,
    key="robot_dashboard"
)
# Load robot data
df = pd.read_csv("data/robot_data.csv")
st.title("🏟 FIFA World Cup 2026 Smart Robot System")
# =========================
# FIFA Sidebar
# =========================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/a/a1/2026_FIFA_World_Cup_logo.svg",
    width=180
)

st.sidebar.title("🏟 FIFA Smart Stadium")

st.sidebar.markdown("---")

st.sidebar.subheader("⚽ Match")

st.sidebar.write("🇦🇷 Argentina vs 🇧🇷 Brazil")

st.sidebar.write("🕒 76' Minute")

st.sidebar.write("👥 Crowd: 71,200")

st.sidebar.write("🌡 Weather: 29°C")

st.sidebar.markdown("---")

st.sidebar.subheader("🤖 Robot Fleet")

st.sidebar.metric("Total Robots", len(df))

st.sidebar.metric(
    "Average Battery",
    f"{df['Battery'].mean():.1f}%"
)

st.sidebar.metric(
    "Active Robots",
    len(df[df["Status"]=="Active"])
)

st.sidebar.metric(
    "Charging",
    len(df[df["Status"]=="Charging"])
)

st.sidebar.metric(
    "Idle",
    len(df[df["Status"]=="Idle"])
)

st.sidebar.markdown("---")

st.sidebar.success("AI System Online")

st.markdown("---")

df = pd.read_csv("data/robot_data.csv")
df["Performance"] = (
    df["Deliveries"] * 5 +
    df["Distance_Covered"] * 2 +
    df["Battery"] * 0.5
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("🤖 Total Robots", len(df))
col2.metric("🔋 Average Battery", f"{df['Battery'].mean():.1f}%")
col3.metric("📦 Active Robots", len(df[df["Status"] == "Active"]))
col4.metric("⚡ Charging", len(df[df["Status"] == "Charging"]))

st.markdown("---")

st.subheader("🤖 Robot Information")

st.dataframe(df, use_container_width=True)
st.markdown("---")

st.subheader("📊 Robot Task Distribution")

task_count = df["Task"].value_counts().reset_index()
task_count.columns = ["Task", "Count"]

fig = px.pie(
    task_count,
    names="Task",
    values="Count",
    hole=0.45,
    title="Robot Tasks"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("🔋 Battery Level Analysis")

fig = px.bar(
    df,
    x="Robot_Name",
    y="Battery",
    color="Battery",
    text="Battery",
    title="Battery Percentage of Each Robot"
)

fig.update_layout(
    xaxis_title="Robot",
    yaxis_title="Battery (%)"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.subheader("🤖 AI Recommendation Panel")

recommendations = []

for _, row in df.iterrows():

    # Low battery
    if row["Battery"] < 25:
        recommendations.append(
            f"🔋 {row['Robot_Name']} battery is only {row['Battery']}%. Send it to the nearest charging station."
        )

    # Charging
    elif row["Status"] == "Charging":
        recommendations.append(
            f"⚡ {row['Robot_Name']} is currently charging. Do not assign new tasks."
        )

    # Idle
    elif row["Status"] == "Idle":
        recommendations.append(
            f"💤 {row['Robot_Name']} is idle. It is available for new assignments."
        )

    # Active
    else:
        recommendations.append(
            f"✅ {row['Robot_Name']} is performing {row['Task']} in Zone {row['Current_Zone']}."
        )

for rec in recommendations:
    st.info(rec)
    st.markdown("---")
st.subheader("🚨 Emergency Alert System")

alerts = []

# Critical Battery
for _, row in df.iterrows():
    if row["Battery"] < 15:
        alerts.append(
            ("critical",
             f"🚨 {row['Robot_Name']} battery is critically low ({row['Battery']}%).")
        )

# Low Battery
for _, row in df.iterrows():
    if 15 <= row["Battery"] < 30:
        alerts.append(
            ("warning",
             f"⚠ {row['Robot_Name']} battery is getting low ({row['Battery']}%).")
        )

# No Medical Robot Active
medical_active = len(
    df[(df["Task"] == "Medical Support") &
       (df["Status"] == "Active")]
)

if medical_active == 0:
    alerts.append(
        ("critical",
         "🚑 No Medical Support Robot is currently active!")
    )

# No Security Robot Active
security_active = len(
    df[(df["Task"] == "Security Patrol") &
       (df["Status"] == "Active")]
)

if security_active == 0:
    alerts.append(
        ("critical",
         "🛡 No Security Patrol Robot is currently active!")
    )

# Display Alerts
if alerts:
    for level, message in alerts:

        if level == "critical":
            st.error(message)

        elif level == "warning":
            st.warning(message)

else:
    st.success("✅ Stadium operations are normal. No emergency detected.")
st.markdown("---")

st.subheader("🤖 Live Robot Status")

cols = st.columns(4)

for i, row in df.iterrows():

    if row["Status"] == "Active":
        color = "🟢"
    elif row["Status"] == "Charging":
        color = "🟡"
    else:
        color = "🔵"

    with cols[i % 4]:
        st.info(
            f"""
**{row['Robot_Name']}**

Status: {color} {row['Status']}

Battery: 🔋 {row['Battery']}%

Zone: 📍 {row['Current_Zone']}

Task: {row['Task']}
"""
        )
        import plotly.graph_objects as go

st.markdown("---")
st.subheader("🏟 Live Stadium Map")

fig = go.Figure()

zone_positions = {
    "A1": (10, 60),
    "A2": (35, 60),
    "B1": (60, 60),
    "B2": (85, 60),
    "C1": (10, 20),
    "C2": (35, 20),
    "D1": (60, 20),
    "D2": (85, 20)
}

status_color = {
    "Active": "green",
    "Charging": "orange",
    "Idle": "blue"
}

for _, row in df.iterrows():

    x, y = zone_positions[row["Current_Zone"]]

    fig.add_trace(

    go.Scatter(

        x=[x],

        y=[y+7],

        mode="markers+text",

        marker=dict(
            size=28,
            color=status_color[row["Status"]],
            line=dict(color="black", width=2)
        ),

        text=f"🤖 {row['Robot_Name']}",

        textposition="top center",

        hovertemplate=
        f"""
<b>{row['Robot_Name']}</b><br>
Zone: {row['Current_Zone']}<br>
Task: {row['Task']}<br>
Battery: {row['Battery']}%<br>
Status: {row['Status']}
""",

        name=row["Robot_Name"]

    )

)

for zone, (x, y) in zone_positions.items():

    # Draw Stadium Zones
 for zone, (x, y) in zone_positions.items():

    fig.add_shape(
        type="rect",
        x0=x-5,
        y0=y-5,
        x1=x+5,
        y1=y+5,
        line=dict(color="black", width=2),
        fillcolor="white"
    )

    fig.add_annotation(
        x=x,
        y=y,
        text=f"<b>{zone}</b>",
        showarrow=False,
        font=dict(size=16)
    )

fig.update_layout(
    title="FIFA World Cup 2026 Smart Stadium",
    xaxis=dict(range=[0,100], visible=False),
    yaxis=dict(range=[0,70], visible=False),
    plot_bgcolor="#95d595",
paper_bgcolor="#111111",
    height=720,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🏆 Robot Performance Leaderboard")

leaderboard = df.sort_values(
    by="Performance",
    ascending=False
).reset_index(drop=True)

medals = ["🥇", "🥈", "🥉"]

for i, row in leaderboard.iterrows():

    if i < 3:
        medal = medals[i]
    else:
        medal = "🤖"

    st.success(
        f"{medal} {row['Robot_Name']} | "
        f"Score: {row['Performance']:.1f} | "
        f"Battery: {row['Battery']}% | "
        f"Deliveries: {row['Deliveries']} | "
        f"Distance: {row['Distance_Covered']} km"
    )
st.markdown("---")
st.subheader("🧠 AI Predictive Analytics")

# Robot that will require charging first
lowest_robot = df.loc[df["Battery"].idxmin()]

st.warning(
    f"🔋 {lowest_robot['Robot_Name']} is predicted to require charging soon "
    f"(Battery: {lowest_robot['Battery']}%)."
)

# Best delivery robot
best_delivery = df[df["Task"] == "Food Delivery"] \
                    .sort_values("Deliveries", ascending=False) \
                    .iloc[0]

st.success(
    f"📦 Best delivery robot: {best_delivery['Robot_Name']} "
    f"({best_delivery['Deliveries']} deliveries completed)."
)

# Best medical robot
medical = df[df["Task"] == "Medical Support"]

if len(medical):

    best_medical = medical.sort_values(
        "Battery",
        ascending=False
    ).iloc[0]

    st.info(
        f"🚑 Recommended Medical Support Robot: "
        f"{best_medical['Robot_Name']}"
    )

# Most efficient robot
best_robot = df.sort_values(
    "Performance",
    ascending=False
).iloc[0]

st.success(
    f"🏆 Overall Best Performing Robot: "
    f"{best_robot['Robot_Name']}"
)
st.markdown("---")
st.subheader("🎯 Live Mission Control")

for _, row in df.iterrows():

    if row["Status"] == "Active":
        progress = min(100, int((row["Deliveries"] * 10) + row["Distance_Covered"] * 5))
        eta = max(1, 10 - row["Deliveries"])

        st.info(
            f"""
### 🤖 {row['Robot_Name']}

**Mission:** {row['Task']}

📍 **Current Zone:** {row['Current_Zone']}

⏳ **ETA:** {eta} min
"""
        )

        st.progress(progress / 100)

    elif row["Status"] == "Charging":
        st.warning(
            f"⚡ {row['Robot_Name']} is charging at Zone {row['Current_Zone']} "
            f"({row['Battery']}%)"
        )

    else:
        st.success(
            f"💤 {row['Robot_Name']} is on standby at Zone {row['Current_Zone']}."
        )
        # ============================================
# 📊 LIVE ANALYTICS DASHBOARD
# ============================================

st.markdown("---")
st.header("📊 Live Analytics Dashboard")
st.subheader("📦 Deliveries Completed by Robot")

import plotly.express as px

fig = px.bar(
    df,
    x="Robot_Name",
    y="Deliveries",
    color="Deliveries",
    text="Deliveries",
    title="Robot Deliveries"
)

fig.update_layout(
    xaxis_title="Robot",
    yaxis_title="Deliveries",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================
# 🔋 Battery vs Distance Analysis
# ============================================

st.markdown("---")
st.subheader("🔋 Battery vs Distance Analysis")

fig = px.scatter(
    df,
    x="Distance_Covered",
    y="Battery",
    color="Status",
    size="Deliveries",
    hover_name="Robot_Name",
    text="Robot_Name",
    title="Robot Efficiency Analysis"
)

fig.update_traces(textposition="top center")

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Distance Covered (km)",
    yaxis_title="Battery (%)"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================
# 🤖 AI ROBOT HEALTH SCORE
# ============================================

st.markdown("---")
st.header("🤖 AI Robot Health Score")

health_df = df.copy()

health_df["Health_Score"] = (
    health_df["Battery"] * 0.45 +
    health_df["Deliveries"] * 1.8 +
    health_df["Distance_Covered"] * 2
)

health_df = health_df.sort_values(
    by="Health_Score",
    ascending=False
)

fig = px.bar(
    health_df,
    x="Robot_Name",
    y="Health_Score",
    color="Health_Score",
    text=health_df["Health_Score"].round(1),
    title="Overall Robot Health Score"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Robot",
    yaxis_title="Health Score"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================
# 🧠 AI COMMAND CENTER
# ============================================

st.markdown("---")
st.header("🧠 AI Command Center")

active = len(df[df["Status"] == "Active"])
charging = len(df[df["Status"] == "Charging"])
idle = len(df[df["Status"] == "Idle"])

avg_battery = df["Battery"].mean()

col1, col2, col3, col4 = st.columns(4)

# Threat Level
if avg_battery < 50:
    col1.error("🔴 Threat Level\n\nHIGH")
elif avg_battery < 75:
    col1.warning("🟡 Threat Level\n\nMEDIUM")
else:
    col1.success("🟢 Threat Level\n\nLOW")

# Active Robots
col2.info(f"🤖 Active Robots\n\n{active}/8")

# Charging
col3.warning(f"⚡ Charging\n\n{charging}")

# Idle
col4.success(f"💤 Idle\n\n{idle}")

st.markdown("---")

st.subheader("🤖 AI Summary")

best_robot = health_df.iloc[0]["Robot_Name"]

st.success(f"🏆 Best Performing Robot: **{best_robot}**")

low_battery = df[df["Battery"] < 40]

if len(low_battery) == 0:
    st.success("✅ No robot currently has critically low battery.")
else:
    for _, row in low_battery.iterrows():
        st.error(
            f"🔋 {row['Robot_Name']} battery is critically low ({row['Battery']}%)."
        )

medical = df[
    (df["Task"] == "Medical Support") &
    (df["Status"] == "Active")
]

if len(medical):
    st.success("🚑 Medical support coverage is available.")
else:
    st.warning("⚠ No active medical support robot!")
    st.markdown("---")

st.header("⚽ Live Match Control Center")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Home", "Argentina 🇦🇷")
col2.metric("Away", "Brazil 🇧🇷")
col3.metric("Score", "2 - 1")
col4.metric("Minute", "76'")

st.markdown("### 📊 Match Statistics")

stats1, stats2 = st.columns(2)

with stats1:
    st.progress(0.61)
    st.write("Argentina Possession : 61%")

with stats2:
    st.progress(0.39)
    st.write("Brazil Possession : 39%")

st.markdown("---")

st.subheader("📢 Live AI Event Feed")

events = [
    "⚽ Goal scored by Argentina (68')",
    "🤖 Robot Nova completed Security Patrol near North Stand.",
    "🚑 Medical Robot Bolt reached injured spectator in 24 seconds.",
    "🟨 Yellow Card issued to Brazil.",
    "🚧 Robot Echo cleared pathway for emergency vehicle.",
    "🎉 Crowd density remains within safe limits.",
    "📡 AI Surveillance reports all stadium zones secure."
]

for event in events:
    st.info(event)