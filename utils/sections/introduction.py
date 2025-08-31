# utils/sections/section2_introduction.py

from utils.llm_selector import get_llm

def generate_section2_introduction(df, model_source="groq"):
    llm = get_llm(model_source)

    # Generate a prompt using dataset preview
    prompt = f"""
            You are a business analyst. Write an introduction for a data analysis report based on the dataset shown below.
            Dataset Preview (first 5 rows):
            Instructions:
            - Clearly define the background or context of the dataset.
            - Describe the scope of the analysis.
            - Infer the types of data sources used based on the column names.
            - Identify who the audience or stakeholders of this report might be.
            Format:
            Background:
            Scope:
            Data Sources:
            Stakeholders:
            """
    # Return the generated response
    return llm(prompt)
