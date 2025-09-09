# utils/insight_suggester.py
import json
from utils.llm_selector import get_llm
from utils.json_utils import extract_json_list
from utils.logger import logger

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
        return "⚠️ Insight generation failed. Please try again."


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
