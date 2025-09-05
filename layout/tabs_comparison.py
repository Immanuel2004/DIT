import streamlit as st
from utils.visualizer import visualize_comparison_overlay, visualize_comparison_side_by_side
from utils.insight_suggester import generate_insights
from utils.chat_handler import handle_user_query_dynamic
from utils.error_handler import safe_llm_call
import pandas as pd
from utils.column_selector import get_important_columns
from utils.llm_selector import get_llm
import re
import json
# from mongo_db.mongo_handler import save_chat, load_user_chats
import plotly.express as px
import os
from utils.visualizer import visualize_comparison_overlay, visualize_comparison_side_by_side
from utils.insight_suggester import generate_insights
from utils.chat_handler import handle_user_query_dynamic
from utils.error_handler import safe_llm_call
import pandas as pd
from utils.column_selector import get_important_columns
from utils.llm_selector import get_llm
from utils.pdf_exporter_comparision import generate_pdf_report_comparison
import matplotlib.pylab as plt
import hashlib
from utils.visualizer import visualize_comparison_overlay  



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




def generate_comparison_plot_from_insight(df1, df2, question, result, dataset1_name="Dataset 1", dataset2_name="Dataset 2"):
    """
    Automatically generates and saves a comparison plot based on LLM-suggested insight.

    Parameters:
        df1 (pd.DataFrame): First dataset
        df2 (pd.DataFrame): Second dataset
        question (str): Insight question
        result (str): LLM response (may contain '[Insert graph here]')
        dataset1_name (str): Custom name of dataset 1
        dataset2_name (str): Custom name of dataset 2

    Returns:
        image_path (str): Path to saved image if generated, else None
    """

    if "[Insert graph here]" not in result:
        return None

    common_cols = list(set(df1.columns).intersection(set(df2.columns)))
    if not common_cols:
        return None

    x_axis = common_cols[0]
    y_axis = common_cols[1] if len(common_cols) > 1 else common_cols[0]

    try:
        fig, explanation = visualize_comparison_overlay(df1, df2, x_axis, y_axis, dataset1_name, dataset2_name, chart_type="bar")

        os.makedirs("generated_plots", exist_ok=True)
        hash_name = hashlib.md5((question + x_axis + y_axis).encode()).hexdigest()
        image_path = f"generated_plots/{hash_name}.png"
        fig.write_image(image_path)

        return image_path

    except Exception as e:
        print(f"[Error in plot generation]: {e}")
        return None


def render_comparison_tabs():
    inject_auth_css()
    if "current_compare" not in st.session_state or st.session_state["current_compare"] is None:
        st.info("Please upload two datasets to compare.")
        return

    compare_key = st.session_state["current_compare"]
    compare_session = st.session_state["compare_sessions"][compare_key]

    df1 = compare_session["df1"]
    df2 = compare_session["df2"]

    st.success(f"Currently Comparing: {compare_key}")

    tab1, tab2, tab3 = st.tabs(["Dataset Previews", "Comparison Insights", "Visualizations"])

    with tab1:
        st.header("Dataset Previews")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Dataset 1")
            st.dataframe(df1.head(), use_container_width=True)
        with col2:
            st.markdown("#### Dataset 2")
            st.dataframe(df2.head(), use_container_width=True)

        st.subheader("AI + User Column Selector")

        ai_cols1 = get_important_columns(df1.to_csv(index=False), "groq")
        ai_cols1 = [col.strip().lower() for col in ai_cols1]

        matched_in_df2 = [col for col in ai_cols1 if col in df2.columns]
        missing_in_df2 = list(set(ai_cols1) - set(matched_in_df2))
        st.info(f"Missing in Dataset 2: {', '.join(missing_in_df2) if missing_in_df2 else 'None'}")

        col1, col2 = st.columns(2)
        with col1:
            user_cols1 = st.multiselect("Select Additional Columns from Dataset 1", df1.columns.tolist(), default=ai_cols1, key="manual_cols_1")
            final_cols1 = list(set(ai_cols1 + user_cols1))
            st.success(f"Selected Columns in Dataset 1: {final_cols1}")
        with col2:
            final_cols2 = [col for col in final_cols1 if col in df2.columns]
            st.success(f"Matched Columns in Dataset 2: {final_cols2}")
            if not final_cols2:
                st.warning("No common columns between selected Dataset 1 columns and Dataset 2.")

        df1 = df1[final_cols1] if final_cols1 else df1
        df2 = df2[final_cols2] if final_cols2 else df2

        compare_session["final_cols1"] = final_cols1
        compare_session["final_cols2"] = final_cols2

        
        common_cols = list(set(df1.columns).intersection(set(df2.columns)))

        if not common_cols:
            st.warning("No common columns found between both datasets.")
            st.stop()
      

    with tab3:
        st.header("Comparison Visualizations")
        x_axis = st.selectbox("Select X-Axis for Comparison", common_cols, key="compare_x_axis")
        y_axis = st.selectbox("Select Y-Axis for Comparison", common_cols, key="compare_y_axis")
        chart_type = st.selectbox("Chart Type", ["bar", "line", "scatter"], key="compare_chart")
        layout = st.radio("Layout", ["Overlay", "Side-by-Side"], horizontal=True, key="compare_layout")

        if x_axis and y_axis:
            try:
                if layout == "Overlay":
                    fig, explanation = visualize_comparison_overlay(df1, df2, x_axis, y_axis, "Dataset 1", "Dataset 2", chart_type)
                    st.plotly_chart(fig, use_container_width=True)
                    compare_session["visualization_history"].append(f"{chart_type} chart: {x_axis} vs {y_axis} (Overlay)")
                    st.caption(explanation)
                else:
                    fig1, fig2 = visualize_comparison_side_by_side(df1, df2, x_axis, y_axis, chart_type)
                    col1, col2 = st.columns(2)
                    col1.plotly_chart(fig1, use_container_width=True)
                    col2.plotly_chart(fig2, use_container_width=True)
                    compare_session["visualization_history"].append(f"{chart_type} chart: {x_axis} vs {y_axis} (Side-by-Side)")
            except Exception as e:
                st.error(f"Comparison visualization failed: {e}")

    with tab2:
     st.header("Comparison Insights")

     merged_df = pd.concat([df1.assign(dataset="Dataset 1"), df2.assign(dataset="Dataset 2")])

     col_left, col_right = st.columns([7, 3], gap="large")

     with col_left:
        st.markdown("### Generated Comparison Insights")
        if compare_session["insights"]:
            for insight in compare_session["insights"][::-1]:
                with st.container(border=True):
                    st.markdown(f"**{insight['question']}**")
                    st.markdown(insight["result"])
                    if any(term in insight["result"].lower() for term in ["graph", "visual", "chart", "plot"]):
                    # if "graph" in insight["result"].lower() or "visual" in insight["result"].lower() or "chart" in insight["result"].lower() or "plot" in insight["result"].lower():
                            try:
                                # Very basic detection of x/y axis from the answer text
                                x_axis, y_axis = None, None
                                for col in compare_session["final_cols1"]:
                                    if col.lower() in insight["result"].lower():
                                        if not x_axis:
                                            x_axis = col
                                        elif not y_axis and col != x_axis:
                                            y_axis = col

                                if x_axis and y_axis:
                                    fig1, fig2 = visualize_comparison_side_by_side(
                                         compare_session["df1"],
                                         compare_session["df2"],
                                         x_axis,
                                         y_axis,
                                         "bar"
                                    )
                                    col1, col2 = st.columns(2)
                                    col1.plotly_chart(fig1, use_container_width=True)
                                    col2.plotly_chart(fig2, use_container_width=True)
                                    import plotly.io as pio
                                    import hashlib
                                    os.makedirs("generated_plots", exist_ok=True)
                                    
                                    hash_name = hashlib.md5(insight["question"].encode()).hexdigest()
                                    image_path_1 = f"generated_plots/{hash_name}_1.png"
                                    pio.write_image(fig1, image_path_1)

                                    image_path_2 = f"generated_plots/{hash_name}_2.png"
                                    pio.write_image(fig2, image_path_2)

                                    # image_path_1 = f"generated_plots/{hashlib.md5(insight['question'].encode()).hexdigest()}.png"
                                    # image_path_2 = f"generated_plots/{hashlib.md5((insight['question'] + '_2').encode()).hexdigest()}.png"
                                    # pio.write_image(fig1, image_path_1)  # save first plot as representation\
                                    # pio.write_image(fig2, image_path_2.replace(".png", "_2.png"))  # save second plot as representation

                                    insight["image_path_1"] = image_path_1
                                    insight["image_path_2"] = image_path_2
                            except Exception as e:
                                st.warning(f"Graph rendering failed: {e}")
        else:
            st.info("Please select a comparison insight question from the right to view the results.")

     with col_right:
        st.markdown("### Comparison Insight Categories")

        if not compare_session.get("insight_categories"):
            try:
                preview = merged_df.to_csv(index=False)[:10000]
                llm = get_llm("groq")

                prompt = f"""
                You are provided with the following combined dataset preview:
                {preview}

                The dataset contains records from two sources:
                - Dataset 1
                - Dataset 2

                Please generate 5-6 analytical comparison insight categories.
                For each category, provide 4-6 detailed comparison-based analytical questions that compare Dataset 1 and Dataset 2.

                Example questions:
                - How do the average values of column X compare between Dataset 1 and Dataset 2?
                - Which dataset has higher variability in column Y?
                - Is there a noticeable difference in trends for column Z across datasets?

                IMPORTANT:
                Return strictly in the following JSON format:
                [
                    {{
                        "title": "Category Name",
                        "questions": ["Question 1", "Question 2", "Question 3"]
                    }},
                    ...
                ]

                Do not include any introduction, explanation, or extra text. Only return the JSON array.
                """

                response = llm(prompt)
                if hasattr(response, "content"):
                    response = response.content

                json_string = re.search(r"\[.*\]", response, re.DOTALL).group(0)
                categories = json.loads(json_string)
                compare_session["insight_categories"] = categories
                st.toast("Comparison insight categories loaded successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"Comparison insight suggestion failed: {e}")
                compare_session["insight_categories"] = []

        for idx, category in enumerate(compare_session.get("insight_categories", [])):
            with st.expander(f"{category['title']}", expanded=False):
                for question in category.get("questions", []):
                    if st.button(f"{question}", key=f"compare_insight_{idx}_{question}"):
                        try:
                            result = generate_insights(merged_df, question, "groq")


                            if "[Insert graph here]" in result:
                                fig, ax = plt.subplots()
                                merged_df[merged_df.columns[0]].value_counts().plot(kind="bar", ax=ax)
                                ax.set_title("Auto-generated Plot")

                                os.makedirs("generated_plots", exist_ok=True)
                                hash_name = hashlib.md5(question.encode()).hexdigest()
                                image_path = f"generated_plots/{hash_name}.png"
                                fig.savefig(image_path)
                                plt.close(fig)

                                compare_session["insights"].append({
                                    "question": question,
                                    "result": result,
                                    "image_path_1": None,
                                    "image_path_2": None
                                })
                            else:
                                compare_session["insights"].append({
                                    "question": question,
                                    "result": result
                                })
                            st.session_state["comparison_insight_results"] = compare_session["insights"]

                            st.rerun()
                        except Exception as e:
                            st.error(f"Comparison insight generation failed: {e}")

    st.markdown("---")
    with st.expander("Chat About This Comparison", expanded=True):
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

        if "compare_chat_history" not in st.session_state:
            st.session_state.compare_chat_history =  []


        with st.container():
            for msg in st.session_state.compare_chat_history:
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

        compare_prompt = st.chat_input("Ask a question about this comparison...", key="comparison_chat_input")
        if compare_prompt:
            st.session_state.compare_chat_history.append({"user": compare_prompt})
            with st.spinner("Thinking..."):
                result = safe_llm_call(handle_user_query_dynamic, compare_prompt, merged_df, "groq", default={"response": "No response."})
            st.session_state.compare_chat_history[-1]["assistant"] = result

            # save_chat(st.session_state.username + "_comparison", compare_prompt, result)
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Export Report")
        if st.button("Export Comparison Report", key="export_pdf_compare"):
            try:
                compare_session["name"] = st.session_state["current_compare"] 
                st.session_state["comparison_insight_results"] = compare_session.get("insights", [])

                if " vs " in compare_key:
                    dataset1_name, dataset2_name = compare_key.split(" vs ")
                else:
                    dataset1_name, dataset2_name = "Dataset 1", "Dataset 2"

                compare_session["dataset1_name"] = dataset1_name
                compare_session["dataset2_name"] = dataset2_name
                compare_session["comparison_insight_results"] = compare_session.get("insights", [])
                compare_session["comparison_recommendations"] = compare_session.get("recommendations", [])

                pdf_path = generate_pdf_report_comparison(compare_session, filename="comparison_summary.pdf")

                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button("Download PDF", f, file_name="comparison_summary.pdf")
                        st.balloons()
                else:
                    st.error("PDF generation failed. Please ensure datasets and insights are available.")
            except Exception as e:
                st.error(f"Failed to export PDF: {e}")
