import streamlit as st
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

def render_guided_tour():
    st.balloons()
    inject_auth_css()
    st.title("Welcome to the Dynamic Impact Tool Tour")

    st.markdown("""
    ### What is the Dynamic Impact Tool?
    The **Dynamic Impact Tool** is an AI-powered data exploration and insight generation platform designed for rapid and intuitive analysis of structured datasets.  
    Whether you're a data analyst, business user, or student — this tool helps you:
    - Upload and preview datasets easily.
    - Generate actionable insights using LLMs.
    - Visualize trends and patterns with a few clicks.
    - Chat with your data for instant answers.
    - Export professional-grade reports.

    This quick tour will walk you through the main features of the app so you can get the most out of your data.
    """)

    with st.expander("Step 1: Upload Your Dataset", expanded=False):
        st.markdown("""
        - Go to the **Upload Area** in the sidebar.
        - Upload a `.csv`, `.xlsx`, or `.json` file.
        - You'll be able to select important columns after upload.
        """)
        st.info("After uploading, check the 'Dataset Preview' tab for summary.")

    with st.expander("Step 2: Generate Smart Insights", expanded=False):
        st.markdown("""
        - Visit the **Insights** tab.
        - Select an insight question from AI-generated suggestions.
        - Visual + text insights will be created for you.
        """)
        st.success("AI will analyze patterns and surface key observations.")

    with st.expander("Step 3: Build Visualizations", expanded=False):
        st.markdown("""
        - Use the **Visualizations** tab.
        - Pick X and Y columns and choose a chart type.
        - Interactive charts will help you spot trends easily.
        """)
        st.warning("Charts include bar, line, scatter, box, and pie charts.")

    with st.expander("Bonus: Chat with Your Data", expanded=False):
        st.markdown("""
        - Use the **Chat** input at the bottom of the app.
        - Ask anything like "Which region had the highest sales?"
        - Get Amazing Output via LLM
        """)
        st.info("The chat uses the same engine as the insights tab — but fully freeform!")

    with st.expander("Export Reports", expanded=False):
        st.markdown("""
        - Export your insights and visuals to PDF or PowerPoint.
        - Use the **Export Report** section at the bottom of the app.
        """)
        st.success("Great for stakeholder presentations.")

    st.markdown("---")
    st.success("You're all set! Head over to the **Dashboard** tab to explore for real.")
    if st.button("Go to Dashboard"):
        st.query_params.update(page="Dashboard")
        st.rerun()