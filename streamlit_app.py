from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Data file sits next to this script, so the app runs from any folder
DATA_PATH = Path(__file__).parent / "data" / "sugar_cleaned.csv"

# ---------- Page setup ----------
st.set_page_config(page_title="Sugar Cosmetics Instagram Dashboard", layout="wide")
st.title("Sugar Cosmetics - Instagram Performance Dashboard")

PINK = "#E6007E"
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------- Load data (cached so it loads only once) ----------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["Post_Date"])


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

min_d, max_d = df["Post_Date"].min().date(), df["Post_Date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)

post_types = st.sidebar.multiselect("Post type", sorted(df["Post_Type"].unique()), default=sorted(df["Post_Type"].unique()))
campaigns = st.sidebar.multiselect("Campaign type", sorted(df["Campaign_Type"].unique()), default=sorted(df["Campaign_Type"].unique()))
sources = st.sidebar.multiselect("Engagement source", sorted(df["Engagement_Source"].unique()), default=sorted(df["Engagement_Source"].unique()))
emotions = st.sidebar.multiselect("Audience emotion", sorted(df["Audience_Emotion"].unique()), default=sorted(df["Audience_Emotion"].unique()))

all_tags = sorted(df["Hashtags"].str.split(", ").explode().unique())
tags = st.sidebar.multiselect("Hashtag (post has any of these)", all_tags, default=all_tags)

# ---------- Apply filters ----------
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start, end = pd.to_datetime(min_d), pd.to_datetime(max_d)

has_tag = df["Hashtags"].apply(lambda x: any(t in x.split(", ") for t in tags))
f = df[
    df["Post_Date"].between(start, end)
    & df["Post_Type"].isin(post_types)
    & df["Campaign_Type"].isin(campaigns)
    & df["Engagement_Source"].isin(sources)
    & df["Audience_Emotion"].isin(emotions)
    & has_tag
]

if f.empty:
    st.warning("No posts match these filters. Please change the filters.")
    st.stop()

# ---------- KPI cards ----------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total posts", f"{len(f):,}")
k2.metric("Total likes", f"{f['Likes'].sum():,}")
k3.metric("Total comments", f"{f['Comments'].sum():,}")
k4.metric("Total reach", f"{f['Reach'].sum():,}")
k5.metric("Avg engagement rate", f"{f['Engagement_Rate'].mean():.2f}%")
k6.metric("Total follows", f"{f['Follows'].sum():,}")

st.divider()

# ---------- Tabs ----------
t1, t2, t3, t4, t5, t6 = st.tabs(
    ["Trends", "Top posts", "Post types", "Days of week", "Funnel", "Hashtags and campaigns"]
)

# --- Tab 1: monthly posting trend and engagement trend ---
with t1:
    monthly = f.groupby("Month_Year").agg(
        Posts=("Post_ID", "count"), Avg_ER=("Engagement_Rate", "mean"), Reach=("Reach", "sum")
    ).reset_index()
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.line(monthly, x="Month_Year", y="Posts", markers=True, title="Posts per month",
                            color_discrete_sequence=[PINK]), use_container_width=True)
    c2.plotly_chart(px.line(monthly, x="Month_Year", y="Avg_ER", markers=True, title="Average engagement rate by month (%)",
                            color_discrete_sequence=[PINK]), use_container_width=True)
    st.caption("April 2024 and April 2025 are partial months, so their post counts look lower.")

# --- Tab 2: top 10 posts ---
with t2:
    show_cols = ["Post_ID", "Post_Date", "Post_Type", "Campaign_Type", "Hashtags", "Likes", "Reach", "Engagement_Rate"]
    c1, c2 = st.columns(2)
    c1.subheader("Top 10 posts by likes")
    c1.dataframe(f.nlargest(10, "Likes")[show_cols], hide_index=True)
    c2.subheader("Top 10 posts by engagement rate")
    c2.dataframe(f.nlargest(10, "Engagement_Rate")[show_cols], hide_index=True)

# --- Tab 3: post type comparison ---
with t3:
    by_type = f.groupby("Post_Type")[["Likes", "Comments", "Saves", "Shares"]].mean().round(1).reset_index()
    long = by_type.melt(id_vars="Post_Type", var_name="Metric", value_name="Average")
    st.plotly_chart(px.bar(long, x="Post_Type", y="Average", color="Metric", barmode="group",
                           title="Average likes, comments, saves and shares by post type"), use_container_width=True)
    er_type = f.groupby("Post_Type")["Engagement_Rate"].mean().round(2).reset_index()
    st.plotly_chart(px.bar(er_type, x="Post_Type", y="Engagement_Rate", text="Engagement_Rate",
                           title="Average engagement rate by post type (%)", color_discrete_sequence=[PINK]),
                    use_container_width=True)

# --- Tab 4: day of week ---
with t4:
    by_day = f.groupby("Day_Name")["Engagement_Rate"].mean().reindex(DAY_ORDER).round(2).reset_index()
    st.plotly_chart(px.bar(by_day, x="Day_Name", y="Engagement_Rate", text="Engagement_Rate",
                           title="Average engagement rate by weekday (%)", color_discrete_sequence=[PINK]),
                    use_container_width=True)

# --- Tab 5: engagement funnel ---
with t5:
    steps = ["Impressions", "Reach", "Likes", "Comments", "Shares", "Saves"]
    funnel = pd.DataFrame({"Step": steps, "Total": [f[s].sum() for s in steps]})
    st.plotly_chart(px.funnel(funnel, x="Total", y="Step", title="Engagement funnel"), use_container_width=True)
    p = f["Profile_Visits"].sum()
    st.write(f"Reach to profile visits: **{p / f['Reach'].sum() * 100:.1f}%**  |  Profile visits to follows: **{f['Follows'].sum() / p * 100:.1f}%**")

# --- Tab 6: hashtags, campaigns, emotion, source ---
with t6:
    tag_df = f[["Hashtags", "Engagement_Rate", "Reach"]].copy()
    tag_df["Hashtag"] = tag_df["Hashtags"].str.split(", ")
    tag_df = tag_df.explode("Hashtag")
    tag_sum = tag_df.groupby("Hashtag").agg(Uses=("Hashtag", "count"), Avg_ER=("Engagement_Rate", "mean"),
                                            Avg_Reach=("Reach", "mean")).round(2).reset_index()
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(tag_sum, x="Hashtag", y="Uses", title="Hashtag usage", color_discrete_sequence=[PINK]),
                    use_container_width=True)
    c2.plotly_chart(px.bar(tag_sum, x="Hashtag", y="Avg_ER", title="Average engagement rate by hashtag (%)",
                           color_discrete_sequence=[PINK]), use_container_width=True)

    c3, c4 = st.columns(2)
    camp = f.groupby("Campaign_Type")["Engagement_Rate"].mean().round(2).reset_index()
    c3.plotly_chart(px.bar(camp, x="Campaign_Type", y="Engagement_Rate", title="Engagement rate by campaign type (%)",
                           color_discrete_sequence=[PINK]), use_container_width=True)
    emo = f.groupby("Audience_Emotion")["Engagement_Rate"].mean().round(2).reset_index()
    c4.plotly_chart(px.bar(emo, x="Audience_Emotion", y="Engagement_Rate", title="Engagement rate by audience emotion (%)",
                           color_discrete_sequence=[PINK]), use_container_width=True)

    src = f.groupby("Engagement_Source").agg(Avg_ER=("Engagement_Rate", "mean"), Follows=("Follows", "sum")).round(2).reset_index()
    st.plotly_chart(px.pie(src, names="Engagement_Source", values="Follows", title="Share of follows by engagement source"),
                    use_container_width=True)
