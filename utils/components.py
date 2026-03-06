import streamlit as st
import numpy as np

def hero_title(title, subtitle):
    st.markdown(f"""
    <div style="text-align: left;">
        <div class="main-title">{title}</div>
        <div class="divider"></div>
        <div class="subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def info_card(title, text):
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def texto(msg: str):
    st.markdown(
        f"""
        <p style='text-align: justify; font-size: 17px; max-width: 1000px;'>
        {msg}
        </p>
        """,
        unsafe_allow_html=True
    )

def card_bloco(titulo: str, conteudo: str, cor: str = "#145089"):
    st.markdown(
        f"""
        <div class="card" style="border-left-color:{cor};">
            <div class="card-title">{titulo}</div>
            <div class="card-text">{conteudo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card(label: str, value: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def fmt_int(n: float) -> str:
    try:
        return f"{int(n):,}".replace(",", ".")
    except Exception:
        return "—"

def fmt_pct(x: float) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x * 100:.1f}%"

def texto(text: str) -> None:
    st.markdown(
        f"""
        <p style='text-align: justify; font-size: 18px; max-width: 900px; margin: auto;'>
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )

def show_plot(fig, key: str) -> None:
    st.plotly_chart(fig, use_container_width=True, key=key)

def section_title(title: str):
    st.header(title)

def section_intro(text: str):
    st.text(text)

def insight_card(title: str, items: list[str]):
    st.markdown(f"**{title}**")
    for item in items:
        st.markdown(item)

import streamlit as st

def texto(text: str) -> None:
    st.markdown(
        f"""
        <p style='text-align: justify; font-size: 16px; max-width: 900px; margin: auto;'>
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )

def show_plot(fig, key: str) -> None:
    st.plotly_chart(fig, use_container_width=True, key=key)

def page_title(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.markdown(subtitle)