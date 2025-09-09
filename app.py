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
from layout.sidebar import render_sidebar
from layout.upload_area import render_upload_area
from layout.tabs_single import render_single_tabs
from layout.tabs_comparison import render_comparison_tabs
from dotenv import load_dotenv
from auth import login, signup, view_users, view_logs
from tour import render_guided_tour

load_dotenv()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.title("Authentication")
    auth_mode = st.radio("Select Option", ["Login", "Signup"], horizontal=True)
    if auth_mode == "Login":
        inject_auth_css()
        login()
    else:
        signup()
        inject_auth_css()
    st.stop()


st.set_page_config(page_title="data-2-Decision", layout="wide")

if "has_seen_tour" not in st.session_state:
    st.session_state.has_seen_tour = False

if not st.session_state.has_seen_tour:
    st.session_state.has_seen_tour = True
    st.query_params.update(page="Guided Tour")
    render_guided_tour()
    st.stop()

for key, default in {
    "mode": "single",
    "dataset_sessions": {},
    "compare_sessions": {},
    "current_session": None,
    "current_compare": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

page = st.query_params.get("page", ["Dashboard"])[0].title()

if st.session_state.role == "admin":
    nav_options = ["Dashboard", "Guided Tour", "Admin Panel", "Audit Logs"]
else:
    nav_options = ["Dashboard", "Guided Tour"]

try:
    nav_index = nav_options.index(page)
except ValueError:
    nav_index = 0

navigation = st.sidebar.radio("Navigation", nav_options, index=nav_index)

st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div[style*="overflow"] {
    scrollbar-width: thin;
    scrollbar-color: #ccc #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

if navigation == "Guided Tour":
    render_guided_tour()
    st.stop()

if navigation == "Admin Panel" and st.session_state.role == "admin":
    st.title("Admin Panel")
    view_users()

elif navigation == "Audit Logs" and st.session_state.role == "admin":
    st.title("Audit Logs")
    view_logs()

elif navigation == "Dashboard":
    st.title("data-2-Decision")
    render_sidebar()
    render_upload_area()

    if st.session_state["mode"] == "single":
        render_single_tabs()
    elif st.session_state["mode"] == "comparison":
        render_comparison_tabs()

with st.sidebar:
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.rerun()
        st.balloons()

