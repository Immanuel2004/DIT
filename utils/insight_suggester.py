# utils/insight_suggester.py
import json
from utils.llm_selector import get_llm
from utils.json_utils import extract_json_list
from utils.logger import logger
import streamlit as st
import  re

def generate_insight_suggestions(preview_data, model_source="groq"):
    """
    Generate categorized insight suggestions using the selected LLM.
    Returns a list of categories, each with a list of questions.
    """
    llm = get_llm(model_source)

    prompt = f"""
    You are acting as a **Senior Data Scientist & ML Engineer**.
    The following is a dataset preview:
    {preview_data}

    Task:
    - Propose 5–6 high-level analytical categories that combine both statistical/ML 
      (Regression, Classification, Clustering, Time-Series, Anomaly Detection) 
      and business-driven perspectives (Trend Analysis, Performance Drivers, Customer Segmentation).
    - For each category, generate 4–6 meaningful analytical questions 
      that a data/ML team should explore to extract business value.

    IMPORTANT:
    Return the response strictly in JSON format:
    [
        {{"title": "Category Name", "questions": ["Question 1", "Question 2", "Question 3"]}},
        ...
    ]
    """

    try:
        response = llm(prompt)

        # Ensure raw text extraction
        if hasattr(response, "content"):
            response = response.content

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return extract_json_list(response)

    except Exception as e:
        logger.warning(f"Insight suggestion failed: {e}")
        # Fallback suggestions
        return [
            {
                "title": "Regression Opportunities",
                "questions": [
                    "Can we predict revenue/sales based on features like region, category, or time?",
                    "Which independent variables are most correlated with the target?",
                    "How well do linear vs. tree-based models perform on this dataset?"
                ]
            },
            {
                "title": "Classification Analysis",
                "questions": [
                    "Can we classify customers into churn vs. non-churn?",
                    "Which factors most influence whether a transaction is successful?",
                    "Which ML algorithms (Logistic Regression, Random Forest, XGBoost) give the best performance?"
                ]
            },
            {
                "title": "Clustering & Segmentation",
                "questions": [
                    "What are the natural customer segments in the dataset?",
                    "Do clusters align with business categories like region or product line?",
                    "How can clustering help improve personalization?"
                ]
            },
            {
                "title": "Trend & Anomaly Detection",
                "questions": [
                    "Are there significant seasonal or daily revenue patterns?",
                    "Where do anomalies occur (sudden spikes or drops)?",
                    "Which business events explain anomalies?"
                ]
            },
        ]


def generate_insights(df, title, model_source="groq"):
    llm = get_llm(model_source)

    preview = df.head(100).to_csv(index=False)

    prompt = f"""
    You are a **Senior ML Engineer**.
    Based on the dataset preview and the selected insight title: "{title}",
    generate a **deep analytical insight** in markdown format (4–6 bullet points).

    Dataset Preview:
    {preview[:3000]}

    - Do not invent columns; use the ones from the dataset.
    - Provide both ML/Statistical perspective (e.g., regression, classification, clustering, correlations) 
      and business interpretation (e.g., sales growth, churn drivers, risk factors).
    """

    try:
        response = llm(prompt)
        return response if isinstance(response, str) else getattr(response, "content", str(response))
    except Exception as e:
        logger.error(f"Insight generation failed: {e}")
        return "Insight generation failed. Please try again."


def generate_comparison_analysis(df1, df2, title, model_source="groq"):
    llm = get_llm(model_source)

    sample1 = df1.head(100).to_csv(index=False)
    sample2 = df2.head(100).to_csv(index=False)

    prompt = f"""
    You are a **Data Scientist** tasked with comparing two datasets.
    Title: "{title}"

    Dataset 1 (sample):
    {sample1}

    Dataset 2 (sample):
    {sample2}

    Provide 3–5 insightful **comparisons** a business/ML team may want to explore.
    Format the response strictly as JSON list of dicts:
    [
        {{"title": "Insight Title", "description": "Detailed description"}},
        ...
    ]
    """

    try:
        response = llm(prompt)
        if hasattr(response, "content"):
            response = response.content
        return json.loads(response)
    except Exception:
        return extract_json_list(response)

import re
import json
import re
import json

def extract_json(text: str):
    """Extract the first {...} block from a string."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        return {}


def data_information(df, model_source="groq"):
    llm = get_llm(model_source)
    preview = df.to_csv(index=False)

    column_selection = st.session_state.get("column_selection", [])
    eda_info = st.session_state.get("eda_info", {})
    ml_info = st.session_state.get("ml_ready_features", [])

    prompt = f"""
    You are a helpful Data Analyst.

    Dataset Preview:
    {preview}

    Columns: {column_selection}
    EDA Info: {eda_info}
    ML Info: {ml_info}

    Return ONLY a JSON object with:
    - summary
    - insights
    - visualizations
    - business_value
    """

    response = llm(prompt)
    if hasattr(response, "content"):
        response = response.content

    clean_response = re.sub(r"^```(?:json)?", "", response.strip(), flags=re.IGNORECASE)
    clean_response = re.sub(r"```$", "", clean_response.strip())

    try:
        return extract_json(clean_response)
    except Exception as e:
        st.error(f"JSON parsing failed: {e}")
        st.text_area("Raw LLM response", response, height=300)
        return {
            "summary": {"dataset_size": "N/A", "feature_columns": "N/A", "target_class": "N/A"},
            "insights": [],
            "visualizations": [],
            "business_value": []
        }
