import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------

# PAGE CONFIG

# --------------------------------------------------

st.set_page_config(
page_title="Marketing Attribution Analytics",
layout="wide",
page_icon="📈"
)

st.title("📈 Marketing Attribution Analytics Dashboard")
st.markdown("Analyze customer journeys, campaign performance, and channel effectiveness.")

# --------------------------------------------------

# LOAD DATA

# --------------------------------------------------

@st.cache_data
def load_data():
df = pd.read_csv("multi_touch_attribution_dataset_cleaned.csv")

```
# Clean column names
df.columns = df.columns.str.strip()

# Convert date columns
if "event_date" in df.columns:
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

if "event_timestamp_utc" in df.columns:
    df["event_timestamp_utc"] = pd.to_datetime(
        df["event_timestamp_utc"],
        errors="coerce"
    )

return df
```

df = load_data()

# --------------------------------------------------

# SIDEBAR

# --------------------------------------------------

st.sidebar.header("Dashboard Controls")

section = st.sidebar.selectbox(
"Choose Section",
[
"Executive Summary",
"Channel Insights",
"Campaign Performance",
"Customer Journey",
"Audience Analysis",
"Recommendations"
]
)

if "channel" in df.columns:
selected_channels = st.sidebar.multiselect(
"Select Channels",
options=sorted(df["channel"].dropna().unique()),
default=sorted(df["channel"].dropna().unique())
)

```
df = df[df["channel"].isin(selected_channels)]
```

# --------------------------------------------------

# CUSTOM STYLING

# --------------------------------------------------

st.markdown("""

<style>
[data-testid="metric-container"] {
    background: #f7f9fc;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #e6eaf0;
}
</style>

""", unsafe_allow_html=True)

# --------------------------------------------------

# EXECUTIVE SUMMARY

# --------------------------------------------------

if section == "Executive Summary":

```
st.subheader("Business Overview")

total_revenue = (
    df["conversion_value"].sum()
    if "conversion_value" in df.columns else 0
)

total_events = len(df)

total_journeys = (
    df["journey_id"].nunique()
    if "journey_id" in df.columns else 0
)

total_conversions = (
    int(df["is_conversion"].sum())
    if "is_conversion" in df.columns else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"${total_revenue:,.0f}")
c2.metric("Events", total_events)
c3.metric("Journeys", total_journeys)
c4.metric("Conversions", total_conversions)

st.markdown("---")

if "event_date" in df.columns and "conversion_value" in df.columns:

    revenue_trend = (
        df.groupby("event_date")["conversion_value"]
        .sum()
        .reset_index()
    )

    fig = px.area(
        revenue_trend,
        x="event_date",
        y="conversion_value",
        title="Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)
```

# --------------------------------------------------

# CHANNEL INSIGHTS

# --------------------------------------------------

elif section == "Channel Insights":

```
st.subheader("Channel Effectiveness")

channel_perf = (
    df.groupby("channel")
    .agg(
        Revenue=("conversion_value", "sum"),
        Conversions=("is_conversion", "sum"),
        Events=("event_id", "count")
    )
    .reset_index()
)

left, right = st.columns(2)

with left:
    fig = px.bar(
        channel_perf,
        x="channel",
        y="Revenue",
        color="channel",
        title="Revenue by Channel"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.pie(
        channel_perf,
        names="channel",
        values="Revenue",
        title="Revenue Share"
    )
    st.plotly_chart(fig, use_container_width=True)
```

# --------------------------------------------------

# CAMPAIGN PERFORMANCE

# --------------------------------------------------

elif section == "Campaign Performance":

```
if "campaign" in df.columns:

    campaign_data = (
        df.groupby("campaign")
        .agg(
            Revenue=("conversion_value", "sum"),
            Events=("event_id", "count")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    fig = px.bar(
        campaign_data,
        x="campaign",
        y="Revenue",
        color="Revenue",
        title="Campaign Revenue Ranking"
    )

    st.plotly_chart(fig, use_container_width=True)
```

# --------------------------------------------------

# CUSTOMER JOURNEY

# --------------------------------------------------

elif section == "Customer Journey":

```
st.subheader("Journey Analysis")

if "touchpoint_number" in df.columns:

    touchpoints = (
        df.groupby("touchpoint_number")
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        touchpoints,
        x="touchpoint_number",
        y="Count",
        markers=True,
        title="Touchpoint Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

if "funnel_stage" in df.columns:

    funnel = (
        df.groupby("funnel_stage")
        .size()
        .reset_index(name="Events")
    )

    fig = px.bar(
        funnel,
        x="funnel_stage",
        y="Events",
        color="funnel_stage",
        title="Funnel Stage Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)
```

# --------------------------------------------------

# AUDIENCE ANALYSIS

# --------------------------------------------------

elif section == "Audience Analysis":

```
col1, col2 = st.columns(2)

with col1:

    if "device" in df.columns:

        device_data = (
            df["device"]
            .value_counts()
            .reset_index()
        )

        device_data.columns = ["Device", "Count"]

        fig = px.donut(
            device_data,
            names="Device",
            values="Count"
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:

    if "region" in df.columns:

        region_data = (
            df["region"]
            .value_counts()
            .reset_index()
        )

        region_data.columns = ["Region", "Count"]

        fig = px.bar(
            region_data,
            x="Region",
            y="Count",
            color="Region"
        )

        st.plotly_chart(fig, use_container_width=True)
```

# --------------------------------------------------

# RECOMMENDATIONS

# --------------------------------------------------

elif section == "Recommendations":

```
st.subheader("Strategic Recommendations")

if "channel" in df.columns:

    best_channel = (
        df.groupby("channel")["conversion_value"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Top Performing Channel: {best_channel}"
    )

if "campaign" in df.columns:

    best_campaign = (
        df.groupby("campaign")["conversion_value"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Highest Revenue Campaign: {best_campaign}"
    )

st.info(
    "Focus marketing spend on top-performing channels and campaigns while optimizing lower-performing touchpoints."
)
```
