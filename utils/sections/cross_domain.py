# utils/sections/section6_cross_domain.py

import pandas as pd
from utils.llm_selector import get_llm
import textwrap

def generate_section6_cross_domain(df: pd.DataFrame, model_source="groq") -> str:
    llm = get_llm(model_source)

    try:
        # Reduce table preview size
        preview_df = df.head(5)
        if df.shape[1] > 10:
            preview_df = preview_df.iloc[:, :10]  # cap at 10 columns

        preview_str = preview_df.to_markdown(index=False)

        # Summarize column types
        column_types = df.dtypes.astype(str).to_dict()
        column_types_str = "\n".join([f"- {col}: {dtype}" for col, dtype in column_types.items()])

        # Describe numeric + first 3 categorical columns (if any)
        numeric_desc = df.describe().round(2).to_string()

        cat_cols = df.select_dtypes(include="object").columns[:3]
        cat_stats = df[cat_cols].describe().to_string() if len(cat_cols) > 0 else ""

        # Construct prompt parts
        prompt = textwrap.dedent(f"""
        You are generating the **Cross-Domain Insights** section of a formal data report.

        **Objective**:
        - Identify correlations, combined patterns, or interactions across domains (columns)
        - Focus on compounding effects or relationships
        - Write in a professional, business-oriented tone

        **Column Types**:
        {column_types_str}

        **Dataset Preview (First 5 rows, up to 10 columns)**:
        {preview_str}

        **Numerical Summary**:
        {numeric_desc}
        """)

        # Append categorical stats separately if available
        if cat_stats:
            prompt += f"\n**Categorical Summary:**\n{cat_stats}"

        prompt += "\n\nWrite 2–3 paragraphs of cross-domain insights in a formal report style."

        return llm(prompt)

    except Exception as e:
        return f"⚠️ Cross-Domain Insight generation failed: {e}"
