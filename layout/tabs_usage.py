# layout/tabs_usage.py

import streamlit as st
import pandas as pd
import os
import json

USAGE_LOG_PATH = "logs/usage_log.json"

def load_usage_data():
    if not os.path.exists(USAGE_LOG_PATH):
        return pd.DataFrame(columns=["user_id", "model", "timestamp", "tokens_input", "tokens_output", "total_tokens", "cost"])
    
    with open(USAGE_LOG_PATH, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def usage_tab():
    st.title("User Usage Tracker")

    df = load_usage_data()

    if df.empty:
        st.info("No usage data available yet.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.write("### Full Log")
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    st.write("---")

    st.write("### Total Usage per User")
    summary = df.groupby("user_id").agg(
        total_tokens=("total_tokens", "sum"),
        total_cost=("cost", "sum"),
        total_requests=("user_id", "count")
    ).reset_index()

    st.dataframe(summary.style.format({
        "total_tokens": "{:,.0f}",
        "total_cost": "${:,.4f}",
        "total_requests": "{:,.0f}"
    }), use_container_width=True)

    st.write("---")

    st.write("### Filter by Date Range")
    min_date, max_date = df["timestamp"].min(), df["timestamp"].max()
    start_date = st.date_input("Start date", min_value=min_date.date(), max_value=max_date.date(), value=min_date.date())
    end_date = st.date_input("End date", min_value=min_date.date(), max_value=max_date.date(), value=max_date.date())

    mask = df["timestamp"].dt.date.between(start_date, end_date)
    filtered = df[mask]
    st.write(f"Showing {len(filtered)} entries between {start_date} and {end_date}")
    st.dataframe(filtered, use_container_width=True)