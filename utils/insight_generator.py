# utils/insight_generator.py
import pandas as pd
from utils.groq_handler import call_groq_model
from utils.logger import logger
from utils.llm_selector import get_llm
import re
import json


def generate_comparison_insight_suggestions(df1, df2, model_source="groq"):
    """
    Generate comparison insight suggestions between two datasets using the LLM.
    """
    llm = get_llm(model_source)

    # Merge datasets with labels
    merged_df = df1.assign(dataset="Dataset 1").append(df2.assign(dataset="Dataset 2"), ignore_index=True)
    preview = merged_df.head(10).to_csv(index=False)[:2048]

    prompt = f"""
    You are acting as a senior Machine Learning Engineer and Data Scientist.
    I have two datasets merged with a 'dataset' column identifying each. Here's a sample:

    {preview}

    Task:
    - Generate exactly 5–6 comparison insight categories.  
    - Each category must contain 4–6 advanced analytical questions focusing on:
      • statistical differences  
      • correlations and distributions  
      • feature importance shifts  
      • predictive performance gaps  
      • business impact differences  

    IMPORTANT:
    Return the response strictly in this JSON format:
    [
        {{
            "title": "Category Name",
            "questions": ["Question 1", "Question 2", "Question 3"]
        }},
        ...
    ]

    Do not include any explanation or extra text or code. Only return the JSON array.
    """

    try:
        response = llm(prompt)

        if hasattr(response, "content"):
            response = response.content

        json_string = re.search(r"\[.*\]", response, re.DOTALL).group(0)
        categories = json.loads(json_string)
        return categories

    except Exception as e:
        raise RuntimeError(f"Failed to generate comparison insight suggestions: {str(e)}")


def generate_insights(df: pd.DataFrame, insight_type: str, model_source: str = "groq") -> str:
    preview = df.head(100).to_csv(index=False)

    prompt = f"""
You are a senior ML Engineer tasked with deriving insights from structured datasets.  
The user has selected this insight type: '{insight_type}'.

Dont include code 

From the dataset preview below, generate a **detailed analytical insight** (4–6 lines).  
Focus on:
- Statistical and ML-relevant findings  
- Correlations or anomalies  
- Predictive potential  
- Possible business or operational implications  

Data Preview (first 100 rows):
{preview[:1500]}
"""

    try:
        if model_source == "groq":
            return call_groq_model("Generate Insight", prompt)
        
    except Exception as e:
        logger.error(f"Insight generation failed: {e}")
        return "Insight generation failed."


def generate_comparison_insights(df1: pd.DataFrame, df2: pd.DataFrame, model_source: str = "groq") -> list:
    try:
        merged_preview = pd.concat([
            df1.head(50).assign(dataset="Dataset 1"),
            df2.head(50).assign(dataset="Dataset 2")
        ])
        prompt = f"""
You are an experienced Data Scientist.  
Analyze the two datasets below and propose **3–5 high-value comparison insights**.  
Don't include code 

Each insight should highlight:
- Differences in statistical distributions or correlations  
- Shifts in feature importance  
- Possible changes in predictive power  
- Business or strategic implications  

Return them strictly as a JSON list of dicts with 'title' and 'description'.

Data Preview:
{merged_preview.to_csv(index=False)[:3000]}
"""

        if model_source == "groq":
            response = call_groq_model("Suggest Comparison Insights", prompt)
        
        import json
        return json.loads(response)
    except Exception as e:
        logger.warning(f"Comparison insight generation failed: {e}")
        return []
