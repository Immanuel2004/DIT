# import streamlit as st
# from io import BytesIO
# from utils.file_loader import load_data, clean_data

# def render_upload_area():
#     st.markdown("## Upload Dataset(s)")

#     if st.session_state["mode"] == "single":
#         col1, col2 = st.columns(2)

#         uploaded_file = col1.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"], key="upload_single")
#         file_path = col2.text_input("Or Enter File Path")

#         if st.button("Upload Dataset", key="upload_single_button"):
#             if uploaded_file is not None:
#                 file_name = uploaded_file.name
#                 file_bytes = uploaded_file.read()
#                 file_like = BytesIO(file_bytes)
#                 df, _ = load_data(file_like, file_name)
#                 st.session_state['df'] = df
#                 df = clean_data(df)

#                 if file_name not in st.session_state["dataset_sessions"]:
#                     store_dataset_session(file_name, df)


#                 st.session_state["current_session"] = file_name
#                 st.toast(f"{file_name} uploaded successfully.")
#                 st.rerun()

#             elif file_path:
#                 try:
#                     file_name = file_path.split("/")[-1]
#                     file = open(file_path, "rb")
#                     df, _ = load_data(file, file_name)
#                     df = clean_data(df)

#                     if file_name not in st.session_state["dataset_sessions"]:
#                         store_dataset_session(file_name, df)

#                     st.session_state["current_session"] = file_name
#                     st.toast(f"{file_name} uploaded successfully.")
#                     st.rerun()

#                 except Exception as e:
#                     st.error(f"File not found: {e}")
#             else:
#                 st.warning("Please upload a file or enter a valid path.")

#     # ========== Comparison Mode ==========
#     elif st.session_state["mode"] == "comparison":
#         col1, col2 = st.columns(2)

#         uploaded_file1 = col1.file_uploader("Upload Dataset 1", type=["csv", "xlsx", "json"], key="upload_compare_1")
#         uploaded_file2 = col2.file_uploader("Upload Dataset 2", type=["csv", "xlsx", "json"], key="upload_compare_2")

#         file_path1 = col1.text_input("Or Enter Path for Dataset 1")
#         file_path2 = col2.text_input("Or Enter Path for Dataset 2")

#         if st.button("Upload and Compare", key="upload_compare_button"):
#             try:
#                 if uploaded_file1 is not None and uploaded_file2 is not None:
#                     file_name1 = uploaded_file1.name
#                     file_name2 = uploaded_file2.name
#                     df1, _ = load_data(BytesIO(uploaded_file1.read()), file_name1)
#                     df2, _ = load_data(BytesIO(uploaded_file2.read()), file_name2)

#                 elif file_path1 and file_path2:
#                     file_name1 = file_path1.split("/")[-1]
#                     file_name2 = file_path2.split("/")[-1]
#                     df1, _ = load_data(open(file_path1, "rb"), file_name1)
#                     df2, _ = load_data(open(file_path2, "rb"), file_name2)

#                 else:
#                     st.warning("Please upload both datasets or provide file paths.")
#                     st.stop()

#                 df1 = clean_data(df1)
#                 df2 = clean_data(df2)

#                 compare_key = f"{file_name1} vs {file_name2}"
#                 st.session_state["compare_sessions"][compare_key] = {
#                     "df1": df1,
#                     "df2": df2,
#                     "chat_history": [],
#                     "insights": [],
#                     "visualization_history": []
#                 }
#                 st.session_state["compare_sessions"][compare_key]["name"] = compare_key


#                 st.session_state["current_compare"] = compare_key
#                 st.toast(f"Comparison loaded: {compare_key}")
#                 st.rerun()

#             except Exception as e:
#                 st.error(f"Comparison upload failed: {e}")



# def store_dataset_session(file_name, df):
#     st.session_state["dataset_sessions"][file_name] = {
#         "df": df,
#         "chat_history": [],
#         "insight_categories": [],
#         "selected_insight_results": [],
#         "visualization_history": [],
#         "column_selection": [],
#         "name": file_name
#     }

import streamlit as st
from io import BytesIO
from utils.file_loader import load_data, clean_data

def render_upload_area():
    st.markdown("## Upload Dataset(s)")

    if st.session_state["mode"] == "single":
        col1, col2 = st.columns(2)

        uploaded_file = col1.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"], key="upload_single")
        file_path = col2.text_input("Or Enter File Path")

        if st.button("Upload Dataset", key="upload_single_button"):
            if uploaded_file is not None:
                file_name = uploaded_file.name
                file_like = BytesIO(uploaded_file.read())
                df, warning = load_data(file_like, file_name)
                df = clean_data(df)

                if warning:
                    st.warning(warning)

                if file_name not in st.session_state["dataset_sessions"]:
                    store_dataset_session(file_name, df)

                st.session_state["df"] = df
                st.session_state["current_session"] = file_name
                st.toast(f"{file_name} uploaded successfully.")
                st.rerun()

            elif file_path:
                try:
                    file_name = file_path.split("/")[-1]
                    with open(file_path, "rb") as f:
                        df, warning = load_data(f, file_name)
                        df = clean_data(df)

                    if warning:
                        st.warning(warning)

                    if file_name not in st.session_state["dataset_sessions"]:
                        store_dataset_session(file_name, df)

                    st.session_state["df"] = df
                    st.session_state["current_session"] = file_name
                    st.toast(f"{file_name} uploaded successfully.")
                    st.rerun()

                except Exception as e:
                    st.error(f"File not found: {e}")
            else:
                st.warning("Please upload a file or enter a valid path.")

    # ========== Comparison Mode ==========
    elif st.session_state["mode"] == "comparison":
        col1, col2 = st.columns(2)

        uploaded_file1 = col1.file_uploader("Upload Dataset 1", type=["csv", "xlsx", "json"], key="upload_compare_1")
        uploaded_file2 = col2.file_uploader("Upload Dataset 2", type=["csv", "xlsx", "json"], key="upload_compare_2")

        file_path1 = col1.text_input("Or Enter Path for Dataset 1")
        file_path2 = col2.text_input("Or Enter Path for Dataset 2")

        if st.button("Upload and Compare", key="upload_compare_button"):
            try:
                # Load datasets from uploaded files
                if uploaded_file1 and uploaded_file2:
                    file_name1 = uploaded_file1.name
                    file_name2 = uploaded_file2.name
                    df1, warn1 = load_data(BytesIO(uploaded_file1.read()), file_name1)
                    df2, warn2 = load_data(BytesIO(uploaded_file2.read()), file_name2)

                # Load datasets from path
                elif file_path1 and file_path2:
                    file_name1 = file_path1.split("/")[-1]
                    file_name2 = file_path2.split("/")[-1]
                    with open(file_path1, "rb") as f1, open(file_path2, "rb") as f2:
                        df1, warn1 = load_data(f1, file_name1)
                        df2, warn2 = load_data(f2, file_name2)

                else:
                    st.warning("Please upload both datasets or provide file paths.")
                    st.stop()

                df1 = clean_data(df1)
                df2 = clean_data(df2)

                if warn1:
                    st.warning(f"{file_name1}: {warn1}")
                if warn2:
                    st.warning(f"{file_name2}: {warn2}")

                compare_key = f"{file_name1} vs {file_name2}"
                st.session_state["compare_sessions"][compare_key] = {
                    "df1": df1,
                    "df2": df2,
                    "chat_history": [],
                    "insights": [],
                    "visualization_history": []
                }
                st.session_state["compare_sessions"][compare_key]["name"] = compare_key

                st.session_state["current_compare"] = compare_key
                st.toast(f"Comparison loaded: {compare_key}")
                st.rerun()

            except Exception as e:
                st.error(f"Comparison upload failed: {e}")

def store_dataset_session(file_name, df):
    st.session_state["dataset_sessions"][file_name] = {
        "df": df,
        "chat_history": [],
        "insight_categories": [],
        "selected_insight_results": [],
        "visualization_history": [],
        "column_selection": [],
        "name": file_name
    }
