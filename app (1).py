import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization",
    page_icon="🏭",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Nassau_Data.csv")

    # Create Lead Time if missing
    if "Lead Time" not in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
        df["Lead Time"] = (
            df["Ship Date"] - df["Order Date"]
        ).dt.days

    # Create Profit Margin if missing
    if "Profit Margin" not in df.columns:
        df["Profit Margin"] = (
            df["Gross Profit"] / df["Sales"]
        ) * 100

    return df

df = load_data()

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🏭 Factory Reallocation & Shipping Optimization Recommendation System")

st.markdown("""
Analyze sales, shipping performance, profit,
lead time and factory optimization using interactive charts.
""")

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

division = st.sidebar.multiselect(
    "Division",
    sorted(df["Division"].unique()),
    default=sorted(df["Division"].unique())
)

ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country/Region"].unique()),
    default=sorted(df["Country/Region"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Division"].isin(division)) &
    (df["Ship Mode"].isin(ship_mode)) &
    (df["Country/Region"].isin(country))
]

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
st.subheader("📊 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Orders",
    len(filtered_df)
)

c2.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

c3.metric(
    "Total Gross Profit",
    f"${filtered_df['Gross Profit'].sum():,.2f}"
)

c4.metric(
    "Average Lead Time",
    f"{filtered_df['Lead Time'].mean():.2f} Days"
)

c5, c6, c7 = st.columns(3)

c5.metric(
    "Average Profit Margin",
    f"{filtered_df['Profit Margin'].mean():.2f}%"
)

c6.metric(
    "Average Sales",
    f"${filtered_df['Sales'].mean():,.2f}"
)

c7.metric(
    "Average Units",
    f"{filtered_df['Units'].mean():.2f}"
)

st.divider()
streamlit run app.py

