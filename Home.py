import streamlit as st
from utils.style import apply_style
from utils.components import hero_title, info_card

st.set_page_config(page_title="Case Passos Mágicos", layout="wide")
apply_style()

hero_title(
    "Case Passos Mágicos",
    "Jennifer Lee Palmer | RM363993<br>Datathon – FIAP"
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([0.3, 0.7])
with col2:
    info_card(
        "Objetivo",
        """Apoiar a tomada de decisão da Associação Passos Mágicos,
        uma instituição que oferece educação de qualidade para crianças e jovens
        do município de Embu-Guaçu (SP), contribuindo para a permanência escolar
        e para o desenvolvimento educacional dos alunos atendidos pelo programa."""
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:right;">
    <a class="site-link" href="https://passosmagicos.org.br/" target="_blank">
        Acessar site institucional da Passos Mágicos
    </a>
</div>
""", unsafe_allow_html=True)