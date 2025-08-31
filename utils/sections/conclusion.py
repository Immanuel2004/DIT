import pandas as pd
from utils.llm_selector import get_llm

def generate_section8_conclusion(df: pd.DataFrame, insights: dict = None, model_source="groq") -> str:
    llm = get_llm(model_source)

    try:
        # Lightweight context
        preview_df = df.head(3)
        preview_str = preview_df.to_markdown(index=False)

        # Insight summary block (optional)
        insight_text = ""
        if insights:
            for key, value in insights.items():
                insight_text += f"\n### {key}\n{value.strip()}\n"

        insights_block = f"**Key Insights from Other Sections:**\n{insight_text}" if insight_text else ""

        prompt = f"""
You are generating the **Conclusion** section of a professional data analysis report.

**Objective**:
- Summarize the key takeaways without repeating the full report
- Emphasize the overall implications or strategic insights
- Suggest final thoughts or high-level next steps

**Data Preview (first 3 rows)**:
{preview_str}

{insights_block}

Write 1–2 well-structured paragraphs in a formal tone that summarize the entire analysis and provide closure.
"""

        return llm(prompt)

    except Exception as e:
        return f"Conclusion generation failed: {e}"
