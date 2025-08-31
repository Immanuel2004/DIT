import pandas as pd
from io import StringIO
from utils.llm_selector import get_llm
from utils.logger import logger

def get_important_columns(csv_data: str, model_source="groq") -> list:
    """
    Extract important columns from a dataset preview using AI logic.

    Args:
        csv_data (str): Dataset as CSV string.
        model_source (str): LLM backend to use.

    Returns:
        list: List of column names.
    """
    try:
        df = pd.read_csv(StringIO(csv_data))

        # Drop fully null columns
        df = df.dropna(axis=1, how='all')

        # Drop low variance (single unique value) columns
        df = df.loc[:, df.nunique(dropna=True) > 1]

        # Take preview for LLM
        preview = df.head(100).to_csv(index=False)

        prompt = f"""
You are a senior data analyst. Based on the dataset preview below, suggest the most important columns for analysis or visualization.

Return only the column names in a Python list format like: ['Age', 'Score', 'Category']
Dataset preview:
{preview[:1200]}
"""

        llm = get_llm(model_source)
        if hasattr(llm, "invoke"):
            response = llm.invoke(prompt).content.strip()
        else:
            response = llm(prompt)

        cols = eval(response)
        if isinstance(cols, list) and all(isinstance(col, str) for col in cols):
            return cols
        else:
            logger.warning("LLM did not return a valid list of column names.")
            return df.columns[:7].tolist()

    except Exception as e:
        logger.error(f"Failed to select important columns: {e}")
        return df.columns[:7].tolist() if 'df' in locals() else []