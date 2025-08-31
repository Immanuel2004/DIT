# utils/sections/section1_summary.py

from utils.llm_selector import get_llm

def generate_section1_summary(df, model_source="groq"):
    llm = get_llm(model_source)
    prompt = f"""
    You are a senior data analyst. Analyze the dataset provided below and generate an executive summary.

    Dataset Summary (df.describe()):
    {df.describe(include='all').to_string()}

    Instructions:
    1. Start with the **Objective of the analysis**
    2. Mention an **overview of key insights** you observe
    3. Provide **high-level recommendations**

    Structure:
    - Objective:
    - Key Insights:
    - Recommendations:
    """
    return llm(prompt)
