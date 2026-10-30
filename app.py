"""First Call: the Streamlit app. Run it with: streamlit run app.py"""

import streamlit as st

from src.gemma import BUSY_MESSAGE, LOCAL_DOWN_MESSAGE, ask, ask_local, load_regions
from src.safety import EMERGENCY_MESSAGE, NDIS_MESSAGE, is_emergency, mentions_ndis

PLACEHOLDER = (
    "For example: Mum is 84 and lives alone. She has had a few falls, "
    "finds showering hard and has stopped cooking proper meals. We don't know where to start."
)
FOOTER = (
    "General information only, not medical, legal or financial advice. "
    "Data is from 2024-25, before Support at Home began on 1 November 2025. "
    "My Aged Care: 1800 200 422 / myagedcare.gov.au"
)
CREDIT = (
    "Source: Australian Institute of Health and Welfare, GEN Aged Care Data, "
    "My aged care region supplementary tables 2024-25 (CC BY 4.0). "
    "We filtered and summarised this data."
)

st.set_page_config(page_title="First Call", page_icon="📞")
st.markdown(
    """
    <style>
    html, body, [class*="css"], .stMarkdown, .stTextArea textarea, .stSelectbox { font-size: 1.15rem; }
    .stMarkdown p, .stMarkdown li { font-size: 1.15rem; line-height: 1.6; }
    .emergency {
        background: #b00020; color: #ffffff; font-weight: 700; font-size: 1.4rem;
        padding: 1rem 1.25rem; border-radius: 0.5rem; margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("First Call")
st.write("Get ready for your first call to My Aged Care about help at home in South Australia.")

offline = st.sidebar.checkbox("Offline mode (local Gemma via Ollama)")

regions = load_regions()
region_name = st.selectbox("Which region do they live in?", regions["name"])
description = st.text_area(
    "Tell us what's going on, in your own words.", placeholder=PLACEHOLDER, height=180
)

if st.button("Make my plan", type="primary"):
    if not description.strip():
        st.warning("Please write a few sentences about the person who needs help.")
    else:
        region_row = regions[regions["name"] == region_name].iloc[0]
        with st.spinner("Preparing your plan..."):
            st.session_state["plan"] = (ask_local if offline else ask)(description, region_row)
        st.session_state["text"] = description

plan = st.session_state.get("plan")
if plan:
    text = st.session_state["text"]
    if is_emergency(text):
        st.markdown(
            f'<div class="emergency" role="alert">🚨 {EMERGENCY_MESSAGE}</div>',
            unsafe_allow_html=True,
        )
    if mentions_ndis(text):
        st.info(NDIS_MESSAGE)
    st.markdown(plan)
    if plan not in (BUSY_MESSAGE, LOCAL_DOWN_MESSAGE):
        st.download_button(
            "Download my plan",
            data=f"{plan}\n\n---\n{FOOTER}\n\n{CREDIT}\n",
            file_name="first-call-plan.md",
            mime="text/markdown",
        )

st.divider()
st.caption(FOOTER)
st.caption(CREDIT)
