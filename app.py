# Deployment link : https://multitouchattribution.streamlit.app/
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Multi-Touch Attribution Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Multi-Touch Attribution Dashboard")
st.markdown("Analyze customer journeys, marketing channels, and conversion performance.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("multi_touch_attribution_dataset_cleaned.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Channel filter
if "channel" in df.columns:
    channels = st.sidebar.multiselect(
        "Select Marketing Channel",
        options=df["channel"].dropna().unique(),
        default=df["channel"].dropna().unique()
    )
    df = df[df["channel"].isin(channels)]

# Customer status filter
if "customer_status" in df.columns:
    status = st.sidebar.multiselect(
        "Select Customer Status",
        options=df["customer_status"].unique(),
        default=df["customer_status"].unique()
    )
    df = df[df["customer_status"].isin(status)]

# KPI Cards
total_customers = df["customer_id"].nunique()
total_conversions = df["converted"].sum()
conversion_rate = (total_conversions / total_customers) * 100 if total_customers > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total_customers)
col2.metric("Total Conversions", total_conversions)
col3.metric("Conversion Rate", f"{conversion_rate:.2f}%")

# Customer Status Pie Chart
if "customer_status" in df.columns:
    st.subheader("Customer Conversion Status")
    fig1 = px.pie(
        df,
        names="customer_status",
        title="Customer Status Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Marketing Channel Performance
if "channel" in df.columns:
    st.subheader("Marketing Channel Performance")

    channel_data = (
        df.groupby("channel")["converted"]
        .sum()
        .reset_index()
        .sort_values(by="converted", ascending=False)
    )

    fig2 = px.bar(
        channel_data,
        x="channel",
        y="converted",
        title="Conversions by Marketing Channel",
        text="converted"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Touchpoint Analysis
if "touchpoint" in df.columns:
    st.subheader("Customer Touchpoint Analysis")

    touch_data = (
        df["touchpoint"]
        .value_counts()
        .reset_index()
    )
    touch_data.columns = ["touchpoint", "count"]

    fig3 = px.bar(
        touch_data,
        x="touchpoint",
        y="count",
        title="Customer Touchpoint Distribution",
        text="count"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Conversion Trend
if "conversion_timestamp_utc" in df.columns:
    st.subheader("Conversion Trend Over Time")

    temp_df = df.copy()
    temp_df["conversion_timestamp_utc"] = pd.to_datetime(
        temp_df["conversion_timestamp_utc"],
        errors="coerce"
    )

    trend = (
        temp_df.dropna(subset=["conversion_timestamp_utc"])
        .groupby(temp_df["conversion_timestamp_utc"].dt.date)["converted"]
        .sum()
        .reset_index()
    )

    fig4 = px.line(
        trend,
        x="conversion_timestamp_utc",
        y="converted",
        markers=True,
        title="Daily Conversion Trend"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Show dataset
with st.expander("View Cleaned Dataset"):
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown("Created using Streamlit | Multi-Touch Attribution Project")
