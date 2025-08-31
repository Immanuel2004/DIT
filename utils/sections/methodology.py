# utils/sections/section4_methodology.py

import pandas as pd
from utils.llm_selector import get_llm

def generate_section4_methodology(df: pd.DataFrame, model_source="groq") -> str:
    llm = get_llm(model_source)

    describe_str = df.describe(include="all").to_string()
    preview_str = df.head(10).to_string()

    prompt = f"""
You are generating the **Methodology** section of a data analysis report.

Here is a dataset preview:
{preview_str}

Here are summary statistics:
{describe_str}

Write a concise Methodology section covering:
- Tools and techniques used (e.g., statistical analysis, machine learning)
- Assumptions made
- Any segmentation or filtering applied
- A general explanation of how insights will be drawn

Do NOT include tables or charts.
Return a formal, structured summary as a paragraph.
"""

    try:
        return llm(prompt)
    except Exception as e:
        return f"⚠️ LLM generation failed: {e}"
