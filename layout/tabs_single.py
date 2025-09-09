import streamlit as st
import os
import pandas as pd
import re
import json
from utils.column_selector import get_important_columns
from utils.visualizer import guess_and_generate_chart
from utils.visualizer import visualize_from_llm_response
from utils.insight_suggester import generate_insights, generate_insight_suggestions
from utils.llm_selector import get_llm
from utils.chat_handler import handle_user_query_dynamic
from utils.error_handler import safe_llm_call
from utils.pdf_exporter import generate_pdf_report, export_to_pptx
from utils.ml_engine import save_trained_model,run_ml,explain_model
import plotly.express as px
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# from mongo_db.mongo_handler import save_chat,load_user_chats 
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



def render_single_tabs():
    inject_auth_css()

    if st.session_state.get("current_session") is None:
        st.info("Please upload a dataset to continue.")
        return
    
    email = st.session_state.get("email") or st.session_state.get("username")

    if not email:
        st.warning("Please login to view your history.")
        return
    else:
        st.success(f"Logged in as {email}")

    session = st.session_state["dataset_sessions"][st.session_state["current_session"]]
    df = session["df"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Data Information & EDA",         
    "ML Model Training & Evaluation", 
    "Insights",              
    "Model Visualizations",          
    "Business Dashboard & Export"    
])


    with tab1:
        st.header("📊 Dataset Summary & Column Selection")


    with tab2:
        st.header("ML Model Training & Evaluation")

    with tab3:
        st.header("Insights")

        col_left, col_right = st.columns([7, 3], gap="large")

        with col_left:
            st.markdown("### Generated Insights")
            if session["selected_insight_results"]:
                for idx, insight in enumerate(session["selected_insight_results"][::-1]):
                    with st.container(border=True):
                        st.markdown(f"**{insight['question']}**")
                        st.markdown(insight["result"])
                        fig = guess_and_generate_chart(df, insight["result"])
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_chart_{idx}")
                        st.markdown("---")
            else:
                st.info("Please select an insight question from the right to view the results.")

        with col_right:
            with st.container():
             if "open_category_index_single" not in st.session_state:
                st.session_state["open_category_index_single"] = None
            
             if not session["insight_categories"]:
                try:
                    preview = df
                    llm = get_llm("groq")

                    prompt = f"""
                    You are provided with a dataset preview and some representative sample rows.
                    {preview}

                    Please generate 5-6 analytical insight categories with 4-6 detailed questions each.
                    Return strictly in JSON format:
                    [
                        {{"title": "Category Name", "questions": ["Question 1", "Question 2", "Question 3"]}},
                        ...
                    ]
                    """

                    response = llm(prompt)
                    if hasattr(response, "content"):
                        response = response.content

                    json_string = re.search(r"\[.*\]", response, re.DOTALL).group(0)
                    categories = json.loads(json_string)
                    session["insight_categories"] = categories
                    st.toast("Categories loaded successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Insight suggestion failed: {e}")
                    session["insight_categories"] = []

             for idx, category in enumerate(session["insight_categories"]):
                expanded = st.session_state["open_category_index_single"] == idx
                with st.expander(f"{category['title']}", expanded=expanded):
                    for question in category["questions"]:
                        if st.button(f"{question}", key=f"insight_{idx}_{question}"):
                            try:
                                result = generate_insights(df, question, "groq")
                                session["selected_insight_results"].append({"question": question, "result": result})

                                # 🔄 Sync with st.session_state so PDF export picks it up
                                st.session_state["selected_insight_results"] = session["selected_insight_results"]

                                st.session_state["open_category_index_single"] = idx
                                st.rerun()
                            except Exception as e:
                                 st.error(f"Insight generation failed: {e}")
             st.markdown("</div>", unsafe_allow_html=True)
    with tab4:
        st.header("Visualizations")

        if not session.get("column_selection"):
            st.warning("Please select columns in Tab 1 to visualize.")
            st.stop()

        x_axis = st.selectbox("Select X-Axis", session["column_selection"], key="single_visual_x")
        y_axis = st.selectbox("Select Y-Axis", session["column_selection"], key="single_visual_y")
        chart_type = st.selectbox("Chart Type", ["bar", "line", "scatter", "box", "violin", "area", "pie"], key="single_visual_chart")

        if x_axis and y_axis:
            try:
                llm_response = {"chart_type": chart_type, "x": x_axis, "y": y_axis, "group_by": None}
                fig, explanation = visualize_from_llm_response(df, f"{x_axis} vs {y_axis}", llm_response)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    session["visualization_history"].append(f"{chart_type} chart: {x_axis} vs {y_axis}")
                    st.caption(explanation)
            except Exception as e:
                st.error(f"Visualization failed: {e}")

    st.markdown("---")
    with st.expander("Talk with your Dataset.", expanded=True):
        st.markdown(
            """
            <style>
            .chat-container {
                max-height: 420px;
                overflow-y: auto;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                gap: 1rem;
                background-color: rgba(240, 240, 240, 0.05);
                border-radius: 12px;
            }

            .chat-row {
                display: flex;
                flex-direction: column;
                max-width: 85%;
            }

            .chat-row.user {
                align-self: flex-end;
                text-align: right;
            }

            .chat-row.assistant {
                align-self: flex-start;
                text-align: left;
            }

            .chat-label {
                font-weight: bold;
                font-size: 0.85rem;
                margin-bottom: 0.25rem;
                color: #bbb;
            }

            .chat-bubble {
                padding: 0.75rem 1rem;
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.06);
                color: white;
                word-wrap: break-word;
            }

            .chat-row.user .chat-bubble {
                background-color: rgba(180, 220, 255, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history =  []

        with st.container():
            for msg in st.session_state.chat_history:
                if "user" in msg:
                    st.markdown(
                        f"""
                        <div class="chat-row user">
                            <div class="chat-label">User</div>
                            <div class="chat-bubble">{msg["user"]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                if "assistant" in msg:
                    response = msg["assistant"].get("response", msg["assistant"])
                    st.markdown(
                        f"""
                        <div class="chat-row assistant">
                            <div class="chat-label">AI</div>
                            <div class="chat-bubble">{response}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    if "chart" in msg["assistant"]:
                        chart_type = msg["assistant"]["chart"]["type"]
                        data = msg["assistant"]["chart"]["data"]
                        x_col = msg["assistant"]["chart"].get("x")
                        y_col = msg["assistant"]["chart"].get("y")
                        chart_df = pd.DataFrame(data)

                        if chart_type == "bar":
                            st.bar_chart(chart_df.set_index(x_col)[y_col])
                        elif chart_type == "line":
                            st.line_chart(chart_df.set_index(x_col)[y_col])
                        elif chart_type == "pie":
                            fig = px.pie(chart_df, names=x_col, values=y_col, title="Pie Chart")
                            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        user_prompt = st.chat_input("Ask a question about your dataset...")
        if user_prompt:
            st.session_state.chat_history.append({"user": user_prompt})
            # save_chat(st.session_state.username, "user", user_prompt)

            with st.spinner("Thinking..."):
                result = safe_llm_call(handle_user_query_dynamic, user_prompt, df, "groq", default={"response": "No response."})

            st.session_state.chat_history.append({"assistant": result})
            # save_chat(st.session_state.username, "ai", result["response"])

            st.rerun()


    from utils.pdf_exporter import generate_pdf_report, export_to_pptx
    from utils.pdf_helpers import format_chat_for_pdf

    st.markdown("---")
    st.subheader("Export Report")

    if "report_counter" not in st.session_state:
        st.session_state["report_counter"] = 0

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export PDF Report"):
            formatted_chat = format_chat_for_pdf(st.session_state.get("chat_history", []))
            
            insights_dict = st.session_state.get("insights", {})
            insights = list(insights_dict.values()) if isinstance(insights_dict, dict) else insights_dict

            df = st.session_state.get("df")

            session = {
                "df": df,
                "name": st.session_state.get("name", "Unnamed Dataset"),
                "selected_insight_results": insights,
                "chat_history": formatted_chat
            }

            output_path = generate_pdf_report(
                session=session,
                filename="final_analysis_report.pdf",
                model_source="groq"  
            )

            with open(output_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="final_analysis_report.pdf",
                mime="application/pdf"
            )
            st.success("PDF exported successfully!")
            st.session_state["report_counter"] += 1
            st.balloons()

    with tab5:
        st.subheader('Business Dashboard')
