import pandas as pd
import io

import pandas as pd
import os

def load_data(file, file_name=None):
    try:
        if isinstance(file, str):
            if file.endswith('.csv'):
                df = pd.read_csv(file, on_bad_lines='skip')  # skip bad rows
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported file type.")
        else:
            if file_name and file_name.endswith('.csv'):
                df = pd.read_csv(file, on_bad_lines='skip')  # skip bad rows
            elif file_name and file_name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file_name and file_name.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported file type.")

        recommendation_msg = None
        if df.isnull().all(axis=1).any():
            recommendation_msg = "Some rows in your file were skipped due to formatting issues (e.g., extra or missing columns). Please review the original CSV."

        return df, recommendation_msg

    except Exception as e:
        raise RuntimeError(f"Failed to load data: {str(e)}")

    
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning: trims spaces in column names and drops fully null columns.
    """
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.dropna(axis=1, how="all")
    return df
