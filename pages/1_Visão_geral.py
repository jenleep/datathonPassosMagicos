import streamlit as st
import pandas as pd
import numpy as np

from utils.style import apply_style
from utils.components import texto, card_bloco, kpi_card, fmt_int, fmt_pct

st.set_page_config(page_title="Visão Geral", layout="wide")
apply_style()

# =========================
# Load
# =========================
DATA_CSV = "data/base_pede_limpa.csv"
df = pd.read_csv(DATA_CSV)

df["ano"] = pd.to_numeric(df.get("ano", np.nan), errors="coerce")

# =========================
# KPIs
# =========================
total_alunos = df["id_aluno"].nunique() if "id_aluno" in df.columns else len(df)

taxa_evasao = np.nan
if "evadido" in df.columns:
    df_evasao = df.dropna(subset=["ano"]).copy()
    if (df_evasao["ano"] == 2024).any():
        df_evasao = df_evasao[df_evasao["ano"] != 2024]
    taxa_evasao = df_evasao["evadido"].mean()

prop_defasagem = np.nan
if "nivel_defasagem" in df.columns:
    prop_defasagem = df["nivel_defasagem"].isin(["moderada", "severa"]).mean()

# =========================
# Header
# =========================
st.title("Visão Geral do Projeto")

st.divider()

# =========================
# Card principal
# =========================
card_bloco(
    "",
    """
    Este dashboard apresenta uma análise exploratória e preditiva dos dados educacionais,
    com foco na identificação de fatores associados à evasão, à defasagem escolar e à evolução
    do desempenho acadêmico ao longo do tempo.
    """
)

# =========================
# Cards secundários
# =========================
col1, col2 = st.columns(2)

with col1:
    card_bloco(
        "Contexto do projeto",
        """
        A Associação Passos Mágicos atua no apoio educacional de crianças e jovens em situação de vulnerabilidade 
        social, utilizando a educação como ferramenta para ampliar oportunidades e promover transformação social.
        A partir de uma base de dados que acompanha o desenvolvimento educacional dos alunos entre 2022 e 2024, este 
        projeto busca aplicar técnicas de análise de dados e modelagem preditiva para compreender padrões na trajetória dos estudantes.
        """,
        cor="#EE7F33"
    )

with col2:
    card_bloco(
        "Glossário dos indicadores",
        """
        <b>IDA</b>: Indicador de Desempenho Acadêmico<br>
        <b>IAN</b>: Indicador de Adequação ao Nível<br>
        <b>IAA</b>: Indicador de Autoavaliação Acadêmica<br>
        <b>IEG</b>: Indicador de Engajamento<br>
        <b>IPV</b>: Indicador de Ponto de Virada<br>
        <b>IPS</b>: Indicador Psicossocial<br>
        <b>IPP</b>: Indicador Psicopedagógico<br>
        <b>INDE</b>: Indicador de Desenvolvimento Educacional
        """,
        cor="#EE7F33"
    )


st.divider()

# =========================
# KPIs
# =========================
k1, k2, k3 = st.columns(3)

with k1:
    kpi_card(
        "Total de alunos acompanhados",
        fmt_int(total_alunos),
        "Base consolidada (alunos únicos)"
    )

with k2:
    kpi_card(
        "Taxa média de evasão",
        fmt_pct(taxa_evasao),
        "Calculada com anos anteriores (até 2023)"
    )

with k3:
    kpi_card(
        "Defasagem moderada ou severa",
        fmt_pct(prop_defasagem),
        "Proporção na base total"
    )

st.divider()

st.subheader("Glossário Expandido")

with st.expander("IDA — Indicador de Desempenho Acadêmico"):
    st.write(
        """
        Mede o desempenho acadêmico do aluno a partir da média de suas notas.
        Esse indicador ajuda a identificar o nível de aproveitamento nas atividades
        e permite acompanhar a evolução do rendimento ao longo do tempo.
        """
    )

with st.expander("IAN — Indicador de Adequação ao Nível"):
    st.write(
        """
        Indica o quanto o aluno está adequado ao nível de ensino esperado para sua etapa escolar.
        Valores mais baixos sugerem maior defasagem entre a série/ano cursado e o desempenho esperado.
        """
    )

with st.expander("IAA — Indicador de Autoavaliação Acadêmica"):
    st.write(
        """
        Representa a percepção do próprio aluno sobre sua trajetória e seu desempenho acadêmico.
        Esse indicador complementa as métricas objetivas ao incorporar a visão subjetiva do estudante
        sobre seu processo de aprendizagem.
        """
    )

with st.expander("IEG — Indicador de Engajamento"):
    st.write(
        """
        Mede o nível de participação, envolvimento e compromisso do aluno com as atividades do programa.
        Em geral, níveis mais altos de engajamento estão associados a maior permanência e melhores resultados acadêmicos.
        """
    )

with st.expander("IPV — Indicador de Ponto de Virada"):
    st.write(
        """
        Captura mudanças relevantes na trajetória do aluno ao longo do tempo,
        indicando avanços, estabilidade ou recuos em seu desenvolvimento.
        É um indicador importante para entender transições e identificar momentos críticos na jornada educacional.
        """
    )

with st.expander("IPS — Indicador Psicossocial"):
    st.write(
        """
        Reflete aspectos emocionais, comportamentais e sociais que podem influenciar
        o desempenho e a permanência do aluno no programa.
        Alterações nesse indicador podem sinalizar risco antes mesmo de quedas acadêmicas mais visíveis.
        """
    )

with st.expander("IPP — Indicador Psicopedagógico"):
    st.write(
        """
        Sintetiza fatores relacionados ao acompanhamento psicopedagógico e ao processo de aprendizagem.
        Esse indicador ajuda a identificar barreiras cognitivas, comportamentais ou pedagógicas
        que podem afetar a evolução escolar do aluno.
        """
    )

with st.expander("INDE — Indicador de Desenvolvimento Educacional"):
    st.write(
        """
        Consolida diferentes dimensões do desenvolvimento do aluno em uma medida mais ampla.
        Funciona como um indicador global da trajetória educacional, integrando aspectos de desempenho,
        adequação, engajamento e suporte.
        """
    )
