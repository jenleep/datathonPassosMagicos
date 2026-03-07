import streamlit as st
from utils.style import apply_global_style

st.set_page_config(page_title="Recomendações", layout="wide")
apply_global_style()

# =========================
# Helpers
# =========================
def texto(msg: str):
    st.markdown(
        f"""
        <p style='text-align: justify; font-size: 17px; max-width: 1000px;'>
        {msg}
        </p>
        """,
        unsafe_allow_html=True
    )

def card_recomendacao(titulo, achado, acao, objetivo, cor):
    st.markdown(
        f"""
        <div style="
            border-left: 8px solid {cor};
            background: #f8fafc;
            padding: 18px 20px;
            border-radius: 12px;
            margin-bottom: 16px;
        ">
            <div style="font-size:18px; font-weight:700; color:#0f172a;">
                {titulo}
            </div>
            <div style="margin-top:8px; font-size:15px;">
                {achado}
            </div>            
            <div style="margin-top:8px; font-size:15px;">
                <b>Ação:</b> {acao}
            </div>
            <div style="margin-top:6px; font-size:15px;">
                <b>Objetivo:</b> {objetivo}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def card_direcionamento(titulo, texto, cor):
    st.markdown(
        f"""
        <div style="
            border-left: 8px solid {cor};
            background: #f8fafc;
            padding: 18px 20px;
            border-radius: 12px;
            margin-bottom: 16px;
        ">
            <div style="font-size:18px; font-weight:700; color:#0f172a;">
                {titulo}
            </div>
            <div style="margin-top:6px; font-size:15px;">
                {texto}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# Header
# =========================
st.title("Recomendações de Intervenção")
st.divider()

# =========================
# Cards principais
# =========================
col1, col2 = st.columns(2)

with col1:
    card_recomendacao(
        "Fortalecimento do Engajamento",
        "Os alunos evadidos apresentam, em média, menor IEG e maior dispersão, indicando que o engajamento funciona como fator protetivo.",
        "Implementar acompanhamento mais próximo da participação dos alunos, com monitoramento de frequência, metas de curto prazo e estratégias de reforço de vínculo com o programa.",
        "Reduzir o risco de evasão e sustentar a permanência dos estudantes com menor adesão às atividades.",
        "#EC3237"
    )

    card_recomendacao(
        "Intensificação do Suporte Psicopedagógico",
        "O IPP apareceu como o fator mais influente na explicação do IPV, indicando forte peso dos aspectos psicopedagógicos na trajetória dos alunos.",
        "Priorizar acompanhamento psicopedagógico para alunos com sinais de maior vulnerabilidade, com foco em barreiras de aprendizagem, autonomia e rotina de estudos.",
        "Atuar sobre fatores estruturais que influenciam o ponto de virada e aumentar a chance de evolução consistente.",
        "#EC3237"
    )

with col2:
    card_recomendacao(
        "Atenção Especial ao Fundamental II",
        "A análise da evasão mostra maior vulnerabilidade no Fundamental II, indicando que essa etapa exige monitoramento mais intensivo.",
        "Criar ações preventivas específicas para alunos dessa fase, com reforço acadêmico, acompanhamento individual e iniciativas de permanência.",
        "Conter o avanço da evasão em uma das etapas mais críticas da trajetória escolar.",
        "#EE7F33"
    )

    card_recomendacao(
        "Identificação Precoce de Alunos em Risco",
        "A matriz de risco mostra que alunos com baixo engajamento e baixo desempenho formam o grupo mais vulnerável, enquanto a defasagem severa está associada a maior probabilidade de evasão.",
        "Usar a combinação entre IEG, IDA e nível de defasagem para classificar alunos em maior risco e priorizar intervenções preventivas antes do agravamento do quadro.",
        "Antecipar situações de piora e direcionar recursos para os perfis com maior probabilidade de evasão ou retrocesso.",
        "#EE7F33"
    )

st.divider()

# =========================
# Achados complementares
# =========================
card_direcionamento("Direcionamento Estratégico",
    "Além das ações prioritárias, os resultados sugerem que o acompanhamento dos alunos deve ser integrado e contínuo. "
    "Os indicadores apontam que mudanças nos aspectos psicossociais podem anteceder quedas de desempenho, enquanto o engajamento "
    "e o suporte psicopedagógico aparecem como dimensões centrais para a permanência e evolução acadêmica. "
    "Assim, a atuação mais eficaz tende a combinar três frentes: prevenção, monitoramento e intervenção focalizada.",
    "#145089"
)

