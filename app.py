import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MTA Dashboard", layout="wide")

st.title("📊 Multi-Touch Attribution Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("multi_touch_attribution_dataset_cleaned.csv")

    df["event_timestamp_utc"] = pd.to_datetime(df["event_timestamp_utc"], errors="coerce")
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎛 Controls")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Channel", "Funnel", "Campaign", "Insights"]
)

# CHANNEL FILTER
channels = df["channel"].unique().tolist()

selected_channels = st.sidebar.multiselect(
    "🎯 Select Channels",
    options=channels,
    default=channels
)

df = df[df["channel"].isin(selected_channels)]

st.sidebar.divider()
st.sidebar.info("Multi-Touch Attribution Analytics")

# ---------------- OVERVIEW ----------------
if page == "Overview":

    total_events = len(df)
    total_journeys = df["journey_id"].nunique()
    conversions = df["is_conversion"].sum()
    revenue = df["conversion_value"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Events", total_events)
    col2.metric("Journeys", total_journeys)
    col3.metric("Conversions", int(conversions))
    col4.metric("Revenue", f"${revenue:,.2f}")

    st.divider()

    st.subheader("📄 Sample Data")
    st.dataframe(df.head(20))

# ---------------- CHANNEL ----------------
elif page == "Channel":

    st.subheader("📡 Channel Performance")

    ch = df.groupby("channel").agg(
        revenue=("conversion_value", "sum"),
        conversions=("is_conversion", "sum"),
        events=("event_id", "count")
    ).reset_index()

    fig = px.bar(ch, x="channel", y="revenue", color="channel")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FUNNEL ----------------
elif page == "Funnel":

    st.subheader("🎯 Funnel Analysis")

    funnel = df.groupby("funnel_stage").agg(
        events=("event_id", "count"),
        conversions=("is_conversion", "sum")
    ).reset_index()

    fig = px.bar(funnel, x="funnel_stage", y="events", color="funnel_stage")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CAMPAIGN ----------------
elif page == "Campaign":

    st.subheader("📢 Campaign Performance")

    camp = df.groupby("campaign").agg(
        revenue=("conversion_value", "sum"),
        events=("event_id", "count")
    ).reset_index().sort_values("revenue", ascending=False)

    fig = px.bar(camp, x="campaign", y="revenue", color="campaign")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
elif page == "Insights":

    st.subheader("🧠 Key Insights")

    avg_touch = df.groupby("journey_id")["touchpoint_number"].max().mean()
    conv_rate = df["is_conversion"].sum() / df["journey_id"].nunique()

    st.success(f"Average Touchpoints per Journey: {avg_touch:.2f}")
    st.success(f"Journey Conversion Rate: {conv_rate:.2%}")
