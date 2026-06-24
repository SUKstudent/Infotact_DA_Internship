import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MTA Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("multi_touch_attribution_dataset_cleaned.csv")
    df['event_timestamp_utc'] = pd.to_datetime(df['event_timestamp_utc'], errors='coerce')
    df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    return df

df = load_data()

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("📊 MTA Dashboard")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "📡 Channel Analysis",
        "🎯 Funnel Analysis",
        "🔁 Touchpoints",
        "📢 Campaigns",
        "🌍 Device & Region",
        "🧠 Insights"
    ]
)

st.sidebar.divider()
st.sidebar.info("Multi-Touch Attribution Analytics")

# ---------------- OVERVIEW PAGE ----------------
if page == "🏠 Overview":
    st.title("📊 Overview")

    total_events = len(df)
    total_journeys = df['journey_id'].nunique()
    conversions = df['is_conversion'].sum()
    revenue = df['conversion_value'].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Events", total_events)
    col2.metric("Journeys", total_journeys)
    col3.metric("Conversions", int(conversions))
    col4.metric("Revenue", f"${revenue:,.2f}")

    st.subheader("Recent Data")
    st.dataframe(df.head(20))

# ---------------- CHANNEL ANALYSIS ----------------
elif page == "📡 Channel Analysis":
    st.title("📡 Channel Performance")

    channel_perf = df.groupby("channel").agg(
        events=("event_id", "count"),
        conversions=("is_conversion", "sum"),
        revenue=("conversion_value", "sum")
    ).reset_index()

    fig = px.bar(channel_perf, x="channel", y="revenue", color="channel",
                 title="Revenue by Channel")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FUNNEL ----------------
elif page == "🎯 Funnel Analysis":
    st.title("🎯 Funnel Analysis")

    funnel = df.groupby("funnel_stage").agg(
        events=("event_id", "count"),
        conversions=("is_conversion", "sum")
    ).reset_index()

    fig = px.bar(funnel, x="funnel_stage", y="events",
                 color="funnel_stage")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TOUCHPOINTS ----------------
elif page == "🔁 Touchpoints":
    st.title("🔁 Touchpoint Journey")

    touch = df.groupby("touchpoint_number").size().reset_index(name="events")

    fig = px.line(touch, x="touchpoint_number", y="events",
                  title="Touchpoints Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CAMPAIGNS ----------------
elif page == "📢 Campaigns":
    st.title("📢 Campaign Performance")

    campaign = df.groupby("campaign").agg(
        events=("event_id", "count"),
        revenue=("conversion_value", "sum")
    ).reset_index().sort_values(by="revenue", ascending=False)

    fig = px.bar(campaign, x="campaign", y="revenue", color="campaign")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- DEVICE & REGION ----------------
elif page == "🌍 Device & Region":
    st.title("🌍 Device & Region Split")

    col1, col2 = st.columns(2)

    with col1:
        device = df['device'].value_counts().reset_index()
        device.columns = ['device', 'count']
        fig = px.pie(device, names='device', values='count')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        region = df['region'].value_counts().reset_index()
        region.columns = ['region', 'count']
        fig = px.pie(region, names='region', values='count')
        st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
elif page == "🧠 Insights":
    st.title("🧠 Attribution Insights")

    avg_touch = df.groupby("journey_id")["touchpoint_number"].max().mean()
    conv_rate = df['is_conversion'].sum() / df['journey_id'].nunique()

    st.success(f"Average Touchpoints per Journey: {avg_touch:.2f}")
    st.success(f"Journey Conversion Rate: {conv_rate:.2%}")
