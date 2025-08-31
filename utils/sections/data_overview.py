# utils/sections/section3_data_overview.py


def generate_section3_data_overview(df, model_source="groq"):
    from utils.llm_selector import get_llm
    llm = get_llm(model_source)

    # Get real shape info
    num_rows, num_cols = df.shape
    sample_data = df.head(3).to_markdown(index=False)
    column_names = ", ".join(df.columns[:10]) + ("..." if len(df.columns) > 10 else "")

    prompt = f"""
You are generating a formal 'Data Overview' section for a dataset report.

Dataset contains {num_rows} rows and {num_cols} columns.
Some of the column names are: {column_names}.

Here are some sample rows:
{sample_data}

Instructions:
- Describe the volume and structure of the data.
- Mention what kinds of data (categories) are included.
- Mention if there are visible timeframe/date columns.
- Mention any missing values or limitations.

Generate this in a formal report tone.
    """

    return llm(prompt)
