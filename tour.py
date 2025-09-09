import streamlit as st
import pandas as pd
def inject_auth_css():
    st.markdown("""
        <style>
        html, body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            font-family: 'Segoe UI', sans-serif;
        }

        .stApp {
            background: transparent;
        }

        .bg-container {
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            z-index: -1;
        }

        .bg-container img {
            object-fit: cover;
            width: 100%;
            height: 100%;
            opacity: 0.25;
            filter: blur(6px) brightness(1.1);
        }

        .auth-box {
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            max-width: 400px;
            margin: 8vh auto;
        }

        @media screen and (max-width: 600px) {
            .auth-box {
                width: 90% !important;
                padding: 1.5rem;
                margin: 5vh auto;
                border-radius: 12px;
            }

            .auth-title {
                font-size: 1.4rem !important;
            }

            .stTextInput > div > input {
                font-size: 16px !important;
            }

            button[kind="primary"] {
                font-size: 16px !important;
                padding: 0.6rem 1.2rem !important;
            }
        }

        .auth-title {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 1.2rem;
            font-weight: 700;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="bg-container">
            <img src="https://images.unsplash.com/photo-1503264116251-35a269479413?auto=format&fit=crop&w=1950&q=80" />
        </div>
    """, unsafe_allow_html=True)


import streamlit as st

def render_guided_tour():
    inject_auth_css()
    st.title("Welcome to the Data2Decision Guided Tour")
    st.markdown("""
    ### What is Data2Decision?
    **Data2Decision** is an LLM-powered data exploration and decision support platform for structured datasets.  
    It enables analysts, business users, and researchers to quickly derive actionable insights, build predictive models, and generate stakeholder-ready reports.  
    The platform supports both **single dataset workflows** and **comparison between datasets**, making it versatile for various business scenarios.

    **Use Cases in Industry:**  
    - Customer segmentation and churn analysis  
    - Sales and revenue forecasting  
    - Operational performance monitoring  
    - Comparative market analysis  
    - Data-driven decision-making for strategy and operations
    """)


    # --- Structured Overview Table ---
    st.markdown("### Key Features and Workflow Overview")
    table_data = [
        {
            "Tab": "Data Information & EDA",
            "Workflow": "Single / Comparison",
            "Key Features": "Data summary, column selection, missing values, outliers, schema alignment",
            "Practical Application": "Prepares datasets for analysis, harmonizes multiple datasets for comparison"
        },
        {
            "Tab": "ML Model Training & Evaluation",
            "Workflow": "Single / Comparison",
            "Key Features": "Problem type detection, model training, metric evaluation, SHAP-based interpretation",
            "Practical Application": "Enables selection of optimal models and predictive analysis across datasets"
        },
        {
            "Tab": "Insights",
            "Workflow": "Single / Comparison",
            "Key Features": "LLM-driven trend detection, anomalies, correlations, cross-dataset insights",
            "Practical Application": "Turns raw data into actionable knowledge for strategic decisions"
        },
        {
            "Tab": "Visualizations",
            "Workflow": "Single / Comparison",
            "Key Features": "Interactive charts (bar, line, scatter, box, pie), side-by-side comparison",
            "Practical Application": "Supports data storytelling and visual pattern recognition"
        },
        {
            "Tab": "Business Dashboard & Export",
            "Workflow": "Single / Comparison",
            "Key Features": "Report compilation, PDF/PPT export, comparative dashboards",
            "Practical Application": "Communicates insights to stakeholders and supports decision-making"
        },
    ]

    st.table(table_data)

    # --- Guided Tour Explanation ---


    with st.expander("Step 1: Data Information & EDA", expanded=False):
        st.markdown("""
        **Single Dataset Workflow:**  
        - View dataset summary, row and column counts, and data types.  
        - Detect missing values, outliers, and distribution anomalies.  
        - Select relevant columns for analysis.  

        **Comparison Workflow:**  
        - Upload and align multiple datasets.  
        - Identify schema mismatches, missing columns, and data inconsistencies.  
        - Prepare datasets for side-by-side analysis.  

        **Practical Application:** Helps analysts clean, understand, and harmonize data before deeper exploration.
        """)
        st.info("This tab ensures that datasets are ready for analysis, whether single or comparative, providing a robust foundation for downstream tasks.")

    with st.expander("Step 2: ML Model Training & Evaluation", expanded=False):
        st.markdown("""
        **Single Dataset Workflow:**  
        - Automatically detect problem type (classification, regression, clustering).  
        - Train multiple models and compare performance metrics.  
        - Use SHAP-based feature importance to interpret models.  

        **Comparison Workflow:**  
        - Train models on multiple datasets and evaluate cross-dataset performance.  
        - Compare predictive accuracy, RMSE, R², or silhouette scores across datasets.  

        **Practical Application:** Empowers data teams to select optimal algorithms and tune models for business-relevant predictions.
        """)
        st.warning("This tab provides a comprehensive machine learning workflow for both single and comparison datasets, enabling predictive analytics and actionable insights.")

    with st.expander("Step 3: Generate Insights", expanded=False):
        st.markdown("""
        **Single Dataset Workflow:**  
        - Generate structured insights using LLM-driven analysis.  
        - Surface trends, anomalies, correlations, and recommendations automatically.  

        **Comparison Workflow:**  
        - Compare key metrics and trends across datasets.  
        - Identify divergences, improvements, or risks between datasets.  

        **Practical Application:** Converts raw data into actionable knowledge for strategic and operational decisions.
        """)
        st.success("Insights are generated programmatically using LLMs to highlight patterns, anomalies, and actionable takeaways.")

    with st.expander("Step 4: Build Visualizations", expanded=False):
        st.markdown("""
        **Single Dataset Workflow:**  
        - Create charts (bar, line, scatter, box, pie) for exploratory analysis.  
        - Interactive plotting helps detect patterns, clusters, or outliers.  

        **Comparison Workflow:**  
        - Visualize side-by-side dataset trends and differences.  
        - Overlay charts for easy comparative analysis.  

        **Practical Application:** Supports data-driven storytelling, reporting, and stakeholder presentations.
        """)
        st.info("Visualizations are dynamically generated and fully interactive, aiding deeper understanding of dataset relationships and trends.")

    with st.expander("Step 5: Business Dashboard & Export", expanded=False):
        st.markdown("""
        **Single Dataset Workflow:**  
        - Compile insights, metrics, and visualizations into a comprehensive report.  
        - Export to PDF or PowerPoint for presentations and documentation.  

        **Comparison Workflow:**  
        - Generate comparative dashboards highlighting differences and trends.  
        - Export comparative reports to support strategic decision-making.  

        **Practical Application:** Enables seamless communication of findings and supports executive-level decision-making.
        """)
        st.success("Reports are LLM-driven, structured, and ready for stakeholder consumption with both single and comparative analyses integrated.")

    st.markdown("---")
    st.info("You are now ready to navigate through the tabs and explore the full capabilities of Data2Decision.")
    if st.button("Go to Dashboard"):
        st.query_params.update(page="Dashboard")
        st.rerun()
