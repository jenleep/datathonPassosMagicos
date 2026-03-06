import streamlit as st

def apply_style():
    st.markdown("""
    <style>

    .block-container {
        padding-top: 4rem;
    }

    [data-testid="stSidebar"] {
        width: 235px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        width: 235px !important;
    }

    .main-title {
        font-size: 50px;
        font-weight: 700;
        color: #052035;
        margin-bottom: 0.2rem;
    }

    .divider {
        height: 3px;
        width: 300px;
        background-color: #FDD324;
        margin: 12px 12px;
    }

    .subtitle {
        font-size: 14px;
        color: #6B7280;
    }

    .context-box {
        max-width: 900px;
        margin: auto;
        font-size: 16px;
        line-height: 1.6;
        color: #374151;
    }

    .card {
        border-left: 8px solid #145089;
        background: #f8fafc;
        padding: 18px 20px;
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
    }

    .card-text {
        font-size: 15px;
        margin-top: 8px;
        color: #374151;
    }

    .site-link {
        display: inline-block;
        margin-top: 25px;
        padding: 8px 18px;
        border: 1px solid #145089;
        color: #145089 !important;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 500;
    }

    .site-link:hover {
        background-color: #145089;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)

def apply_global_style():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 230px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        width: 230px !important;
    }

    p {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)