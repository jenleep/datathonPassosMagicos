import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from utils.style import apply_global_style
from utils.components import texto, show_plot, section_title, section_intro

# =========================
# Page config
# =========================
st.set_page_config(page_title="Perfil dos Alunos e Defasagem", layout="wide")
apply_global_style()

DATA_CSV = "data/base_pede_limpa.csv"

# =========================
# Rótulos padronizados
# =========================
ROTULOS_NIVEL_ENSINO = {
    "fundamental1": "Fundamental I",
    "fundamental2": "Fundamental II",
    "medio": "Ensino Médio",
    "superior": "Ensino Superior",
}

ROTULOS_DEFASAGEM = {
    "em fase": "Em fase",
    "moderada": "Defasagem moderada",
    "severa": "Defasagem severa",
}

ROTULOS_PEDRA = {
    "quartzo": "Quartzo",
    "agata": "Ágata",
    "ametista": "Ametista",
    "topazio": "Topázio",
}

ROTULOS_REDE = {
    "publico": "Rede pública",
    "privado": "Rede privada",
    "outro": "Outro",
}

ORDEM_NIVEL_ENSINO = ["Fundamental I", "Fundamental II", "Ensino Médio", "Ensino Superior"]
ORDEM_DEFASAGEM = ["Em fase", "Defasagem moderada", "Defasagem severa"]
ORDEM_PEDRA = ["Quartzo", "Ágata", "Ametista", "Topázio"]

# =========================
# Cores
# =========================
CORES_GENERO = {"Meninos": "#145089", "Meninas": "#EC3237"}

CORES_NIVEL_ENSINO = {
    "Fundamental I": "#FDD324",
    "Fundamental II": "#EE7F33",
    "Ensino Médio": "#EC3237",
    "Ensino Superior": "#145089",
}

CORES_DEFASAGEM = {
    "Em fase": "#145089",
    "Defasagem moderada": "#FDD324",
    "Defasagem severa": "#EE7F33",
}

CORES_PEDRA = {
    "Quartzo": "#D9DDD9",
    "Ágata": "#B36B00",
    "Ametista": "#800080",
    "Topázio": "#FFD700",
}

# =========================
# Data
# =========================
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df_ = pd.read_csv(path)

    df_["genero_txt"] = df_["genero"].map({
        "masculino": "Meninos",
        "feminino": "Meninas"
    })

    for col in ["idade", "defasagem", "ian", "ipp", "ida", "iaa"]:
        if col in df_.columns:
            df_[col] = pd.to_numeric(df_[col], errors="coerce")

    df_["nivel_ensino_lbl"] = df_["nivel_ensino"].map(ROTULOS_NIVEL_ENSINO).fillna(df_["nivel_ensino"])
    df_["nivel_defasagem_lbl"] = df_["nivel_defasagem"].map(ROTULOS_DEFASAGEM).fillna(df_["nivel_defasagem"])
    df_["pedra_lbl"] = df_["pedra"].map(ROTULOS_PEDRA).fillna(df_["pedra"])
    df_["inst_ensino_lbl"] = df_["inst_ensino"].map(ROTULOS_REDE).fillna(df_["inst_ensino"])

    df_["nivel_ensino_lbl"] = pd.Categorical(
        df_["nivel_ensino_lbl"],
        categories=ORDEM_NIVEL_ENSINO,
        ordered=True
    )
    df_["nivel_defasagem_lbl"] = pd.Categorical(
        df_["nivel_defasagem_lbl"],
        categories=ORDEM_DEFASAGEM,
        ordered=True
    )
    df_["pedra_lbl"] = pd.Categorical(
        df_["pedra_lbl"],
        categories=ORDEM_PEDRA,
        ordered=True
    )

    return df_

df = load_data(DATA_CSV)
df_age = df[df["idade"].between(4, 22)].copy()

# =========================
# Header
# =========================
section_title("Perfil dos Alunos e Defasagem")
section_intro(
    "Esta seção apresenta uma visão geral do perfil dos alunos e da defasagem escolar entre 2022 e 2024, "
    "destacando como os estudantes se distribuem por características demográficas e educacionais e como a "
    "defasagem aparece ao longo do tempo."
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Visão Geral", "Defasagem (IAN)", "Autoavaliação (IAA)", "Índice Psicopedagógico (IPP)"]
)

# =========================
# TAB 1 — Visão Geral
# =========================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df,
            names="genero_txt",
            title="Distribuição por Gênero",
            color="genero_txt",
            color_discrete_map=CORES_GENERO,
        )
        show_plot(fig, "t1_genero")

    with col2:
        fig = px.histogram(
            df_age,
            x="idade",
            nbins=13,
            color="genero_txt",
            barmode="overlay",
            title="Distribuição por Idade",
            color_discrete_map=CORES_GENERO,
            labels={"idade": "Idade", "genero_txt": "Gênero"},
        )
        fig.update_layout(yaxis_title="Quantidade")
        show_plot(fig, "t1_idade")

    texto(
        "A base de alunos apresenta leve predominância feminina, com 53,7% de meninas e 46,3% de meninos, indicando uma distribuição relativamente equilibrada entre os gêneros. "
        "Em relação à idade, observa-se maior concentração entre 10 e 15 anos, com pico próximo aos 11–13 anos. As distribuições de meninas e meninos são bastante semelhantes ao longo das idades, sugerindo perfil etário homogêneo entre os gêneros e ausência de distorções relevantes na composição da amostra."
    )

    anos = sorted(df_age["ano"].dropna().unique())
    cols = st.columns(len(anos))

    for col, ano in zip(cols, anos):
        df_ano = df_age[df_age["ano"] == ano]
        fig = px.histogram(
            df_ano,
            x="idade",
            nbins=13,
            title=f"Idade – {ano}",
            color_discrete_sequence=["#EE7F33"],
            labels={"idade": "Idade", "count": "Quantidade"},
        )
        fig.update_layout(yaxis_title="Quantidade")
        col.plotly_chart(fig, use_container_width=True, key=f"t1_idade_{ano}")

    texto(
        "A distribuição etária ao longo dos três anos mantém um padrão consistente, com maior concentração de alunos entre 10 e 14 anos. Em 2022 e 2023, observa-se pico próximo aos 11–12 anos, enquanto em 2024 há leve ampliação da base e maior dispersão nas idades acima de 15 anos, refletindo o crescimento do número de veteranos no programa."
    )

    df_no_superior = df[df["nivel_ensino_lbl"] != "Ensino Superior"].copy()
    df_no_superior["nivel_ensino_lbl"] = df_no_superior["nivel_ensino_lbl"].cat.remove_unused_categories()

    df_media = (
        df_no_superior.groupby(["ano", "nivel_ensino_lbl"], as_index=False)["defasagem"]
        .mean()
    )

    fig = px.line(
        df_media,
        x="ano",
        y="defasagem",
        color="nivel_ensino_lbl",
        color_discrete_map=CORES_NIVEL_ENSINO,
        markers=True,
        title="Média da Defasagem por Ano e Nível de Ensino",
        labels={
            "ano": "Ano",
            "defasagem": "Defasagem (anos)",
            "nivel_ensino_lbl": "Nível de ensino"
        },
    )
    fig.update_xaxes(tickmode="array", tickvals=[2022, 2023, 2024], ticktext=["2022", "2023", "2024"])
    fig.update_yaxes(autorange="reversed")
    show_plot(fig, "t1_def_media")

# =========================
# TAB 2 — Defasagem (IAN)
# =========================
with tab2:
    col_def1, col_def2 = st.columns(2)

    with col_def1:
        df_def = df.groupby(["ano", "nivel_defasagem_lbl"], as_index=False).size()
        df_def["proporcao"] = df_def.groupby("ano")["size"].transform(lambda x: x / x.sum())

        fig = px.bar(
            df_def,
            x="ano",
            y="proporcao",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="Distribuição Proporcional da Defasagem (IAN)",
            labels={
                "ano": "Ano",
                "proporcao": "Proporção",
                "nivel_defasagem_lbl": "Nível de defasagem"
            },
        )
        fig.update_layout(barmode="stack")
        show_plot(fig, "t2_def_prop")

    with col_def2:
        df_2024 = df[df["ano"] == 2024].copy()
        df_rede = (
            df_2024[df_2024["inst_ensino_lbl"] != "Outro"]
            .groupby(["inst_ensino_lbl", "nivel_defasagem_lbl"], as_index=False)
            .size()
        )

        fig = px.bar(
            df_rede,
            x="inst_ensino_lbl",
            y="size",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            barmode="group",
            title="Defasagem por Rede de Ensino (2024)",
            labels={
                "inst_ensino_lbl": "Rede de ensino",
                "size": "Quantidade",
                "nivel_defasagem_lbl": "Nível de defasagem"
            },
        )
        show_plot(fig, "t2_def_rede_2024")

# =========================
# TAB 3 — Autoavaliação (IAA)
# =========================
with tab3:
    col_iaa1, col_iaa2 = st.columns(2)

    with col_iaa1:
        fig = px.box(
            df,
            x="nivel_defasagem_lbl",
            y="iaa",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="Distribuição do IAA por Nível de Defasagem",
            labels={"nivel_defasagem_lbl": "Nível de defasagem", "iaa": "IAA"},
        )
        fig.update_layout(showlegend=False)
        show_plot(fig, "t3_iaa_box")

    with col_iaa2:
        fig = px.scatter(
            df,
            x="ida",
            y="iaa",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            opacity=0.6,
            title="Relação entre IDA e IAA por Nível de Defasagem",
            labels={"ida": "IDA", "iaa": "IAA", "nivel_defasagem_lbl": "Nível de defasagem"},
        )
        show_plot(fig, "t3_ida_iaa")

# =========================
# TAB 4 — IPP
# =========================
with tab4:
    col_ipp1, col_ipp2 = st.columns(2)

    with col_ipp1:
        fig = px.scatter(
            df,
            x="ian",
            y="ipp",
            title="Relação entre IPP e IAN",
            trendline="ols",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            opacity=0.5,
            labels={
                "ian": "IAN (quanto menor, mais defasado)",
                "ipp": "IPP",
                "nivel_defasagem_lbl": "Nível de defasagem"
            },
        )
        show_plot(fig, "t4_ipp_ian")

    with col_ipp2:
        df_area = df.groupby("nivel_defasagem_lbl", as_index=False)[["ian", "ipp"]].mean()
        df_area["nivel_defasagem_lbl"] = pd.Categorical(
            df_area["nivel_defasagem_lbl"],
            categories=ORDEM_DEFASAGEM,
            ordered=True
        )
        df_area = df_area.sort_values("nivel_defasagem_lbl")

        fig, ax = plt.subplots()
        ax.fill_between(df_area["nivel_defasagem_lbl"].astype(str), df_area["ian"], alpha=0.4, label="IAN")
        ax.fill_between(df_area["nivel_defasagem_lbl"].astype(str), df_area["ipp"], alpha=0.4, label="IPP")
        ax.set_xlabel("Nível de defasagem")
        ax.set_ylabel("Média do indicador")
        ax.set_title("IAN e IPP por Nível de Defasagem")
        ax.legend()
        st.pyplot(fig, use_container_width=True)

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div style="
        border-left:6px solid #145089;
        background:#f8fafc;
        padding:14px 16px;
        border-radius:10px;
        font-size:14px;
    ">
    <b>Distribuição da defasagem</b><br>
    A maior parte dos alunos está em fase ou apresenta defasagem moderada.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="
        border-left:6px solid #145089;
        background:#f8fafc;
        padding:14px 16px;
        border-radius:10px;
        font-size:14px;
    ">
    <b>Etapas críticas</b><br>
    As fases intermediárias da trajetória escolar concentram maior nível de defasagem.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style="
        border-left:6px solid #145089;
        background:#f8fafc;
        padding:14px 16px;
        border-radius:10px;
        font-size:14px;
    ">
    <b>Evolução ao longo do tempo</b><br>
    Observa-se redução dos casos de defasagem severa entre 2022 e 2024.
    </div>
    """, unsafe_allow_html=True)
