# layout/sidebar.py
import streamlit as st

def render_sidebar():
    st.sidebar.title("Choose your Analysis")

    if st.session_state.get("logged_in", False):
        mode = st.sidebar.radio(
            "Select Mode",
            ["Single Dataset", "Compare Datasets"],
            index=0 if st.session_state["mode"] == "single" else 1
        )

        if mode == "Single Dataset" and st.session_state["mode"] != "single":
            st.session_state["mode"] = "single"
            st.session_state["current_compare"] = None
            st.rerun()

        elif mode == "Compare Datasets" and st.session_state["mode"] != "comparison":
            st.session_state["mode"] = "comparison"
            st.session_state["current_session"] = None
            st.rerun()

        st.sidebar.markdown("---")

        if st.session_state["mode"] == "single":
            st.sidebar.markdown("## Dataset History")
            if st.session_state["dataset_sessions"]:
                for i, dataset in enumerate(st.session_state["dataset_sessions"].keys()):
                    if st.sidebar.button(dataset, key=f"dataset_{i}"):
                        st.session_state["current_session"] = dataset
                        st.rerun()
            else:
                st.sidebar.info("No datasets uploaded yet.")

        elif st.session_state["mode"] == "comparison":
            st.sidebar.markdown("## Comparison History")
            if st.session_state["compare_sessions"]:
                for i, comparison in enumerate(st.session_state["compare_sessions"].keys()):
                    if st.sidebar.button(comparison, key=f"compare_{i}"):
                        st.session_state["current_compare"] = comparison
                        st.rerun()
            else:
                st.sidebar.info("No comparisons uploaded yet.")

        st.sidebar.markdown("---")

        if st.sidebar.button("Clear All Sessions"):
            st.session_state["dataset_sessions"] = {}
            st.session_state["compare_sessions"] = {}
            st.session_state["current_session"] = None
            st.session_state["current_compare"] = None
            st.rerun()
