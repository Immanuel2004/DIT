import pandas as pd
import re
import streamlit as st
from utils.llm_selector import get_llm
from utils.data_cleaner import clean_data  # Keep this if needed for optional re-cleaning

def parse_recommendations(raw_text: str):
    """
    Parses LLM-generated text into a list of structured recommendation dicts.
    Assumes a format like:
    1. Insight: ...
       Recommended Action: ...
       Priority: ...
       Owner/Team: ...
       Timeline: ...
    """
    pattern = re.compile(
        r"(?P<idx>\d+)\.\s*Insight:\s*(?P<insight>.*?)\n\s*Recommended Action:\s*(?P<action>.*?)\n\s*Priority:\s*(?P<priority>.*?)\n\s*Owner/Team:\s*(?P<owner>.*?)\n\s*Timeline:\s*(?P<timeline>.*?)\n",
        re.DOTALL,
    )
    matches = pattern.finditer(raw_text)
    recommendations = []

    for match in matches:
        rec = {
            "Insight": match.group("insight").strip(),
            "Recommended Action": match.group("action").strip(),
            "Priority": match.group("priority").strip(),
            "Owner": match.group("owner").strip(),
            "Timeline": match.group("timeline").strip(),
        }
        recommendations.append(rec)

    # Fallback: if no matches, return raw text
    return recommendations if recommendations else [raw_text]

def generate_section7_recommendations(insights: dict = None, model_source="groq") -> list:
    # Retrieve the dataframe from session state
    df = st.session_state.get("df")

    if df is None:
        return [f"Recommendation generation failed: No dataset found in session."]

    # Optionally re-clean the dataset (uncomment if needed)
    # df = clean_data(df)

    llm = get_llm(model_source)

    try:
        # Trim dataset for preview
        preview_df = df.head(5)
        if df.shape[1] > 10:
            preview_df = preview_df.iloc[:, :10]

        preview_str = preview_df.to_markdown(index=False)

        # Column summary
        column_types = df.dtypes.astype(str).to_dict()
        column_types_str = "\n".join([f"- {col}: {dtype}" for col, dtype in column_types.items()])

        # Descriptive stats
        numeric_summary = df.describe().round(2).to_string()

        # Insight text
        insight_text = ""
        if insights:
            for key, value in insights.items():
                insight_text += f"\n### {key}\n{value}\n"

        prompt = f"""
You are generating the **Recommendations & Actionable Items** section of a professional data report.

**Objective**:
- Suggest clear, data-driven actions based on the dataset and insights.
- Use the format:
  1. Insight: ...
     Recommended Action: ...
     Priority: High/Medium/Low
     Owner/Team: ...
     Timeline: ...

**Column Types**:
{column_types_str}

**Data Preview (first 5 rows, max 10 cols)**:
{preview_str}

**Numeric Summary**:
{numeric_summary}
"""

        if insight_text:
            prompt += f"\n**Relevant Insights from Other Sections:**\n{insight_text}"

        prompt += "\nGenerate 3 to 5 recommendations using the specified format."

        # Call LLM and parse result
        raw_response = llm(prompt)
        return parse_recommendations(raw_response)

    except Exception as e:
        return [f"Recommendation generation failed: {e}"]
