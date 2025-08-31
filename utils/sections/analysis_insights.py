import pandas as pd
import streamlit as st  

def generate_section5_analysis_insights(df: pd.DataFrame, model_source="groq") -> str:
    insights = st.session_state.get("selected_insight_results", [])
    # st.write("DEBUG: selected_insight_results = ", st.session_state.get("selected_insight_results", []))

    if not insights:
        return "No insights available for this dataset."

    formatted_insights = ""
    for idx, item in enumerate(insights, start=1):
        question = item.get("question", "No question")
        result = item.get("result", "No result")
        formatted_insights += f"Insight {idx}:\n"
        formatted_insights += f"Question: {question}\n"
        formatted_insights += f"Insight: {result}\n"
        formatted_insights += "----------------------------------------\n"

    return formatted_insights
