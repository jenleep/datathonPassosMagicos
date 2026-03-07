import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from utils.style import apply_style
from utils.components import texto, page_title

# =========================
# Page config
# =========================
st.set_page_config(page_title="Perfil dos Alunos e Defasagem", layout="wide")
apply_style()

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
# Helpers locais
# =========================
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df_ = pd.read_csv(path)

    df_["genero_txt"] = df_["genero"].map(
        {"masculino": "Meninos", "feminino": "Meninas"}
    )

    for col in ["idade", "defasagem", "ian", "ipp", "ida", "iaa"]:
        if col in df_.columns:
            df_[col] = pd.to_numeric(df_[col], errors="coerce")

    df_["nivel_ensino_lbl"] = df_["nivel_ensino"].map(ROTULOS_NIVEL_ENSINO).fillna(df_["nivel_ensino"])
    df_["nivel_defasagem_lbl"] = df_["nivel_defasagem"].map(ROTULOS_DEFASAGEM).fillna(df_["nivel_defasagem"])
    df_["pedra_lbl"] = df_["pedra"].map(ROTULOS_PEDRA).fillna(df_["pedra"])
    df_["inst_ensino_lbl"] = df_["inst_ensino"].map(ROTULOS_REDE).fillna(df_["inst_ensino"])

    df_["nivel_ensino_lbl"] = pd.Categorical(
        df_["nivel_ensino_lbl"], categories=ORDEM_NIVEL_ENSINO, ordered=True
    )
    df_["nivel_defasagem_lbl"] = pd.Categorical(
        df_["nivel_defasagem_lbl"], categories=ORDEM_DEFASAGEM, ordered=True
    )
    df_["pedra_lbl"] = pd.Categorical(
        df_["pedra_lbl"], categories=ORDEM_PEDRA, ordered=True
    )

    return df_


def show_plot(fig, key: str) -> None:
    st.plotly_chart(fig, use_container_width=True, key=key)


def eixo_ano(fig):
    fig.update_xaxes(
        tickmode="array",
        tickvals=[2022, 2023, 2024],
        ticktext=["2022", "2023", "2024"]
    )
    return fig


# =========================
# Data
# =========================
df = load_data(DATA_CSV)
df_age = df[df["idade"].between(4, 22)].copy()

# =========================
# Header
# =========================
page_title(
    "Perfil dos Alunos e Defasagem",
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
        "Em relação à idade, observa-se maior concentração entre 10 e 15 anos, com pico próximo aos 11–13 anos. As distribuições "
        "de meninas e meninos são bastante semelhantes ao longo das idades, sugerindo perfil etário homogêneo entre os gêneros e ausência de distorções relevantes na composição da amostra."
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
            labels={"idade": "Idade"},
        )
        fig.update_layout(yaxis_title="Quantidade")
        col.plotly_chart(fig, use_container_width=True, key=f"t1_idade_{ano}")

    texto(
        "A distribuição etária ao longo dos três anos mantém um padrão consistente, com maior concentração de alunos entre 10 e 14 anos. Em 2022 e 2023, observa-se pico próximo aos 11–12 anos, "
        "enquanto em 2024 há leve ampliação da base e maior dispersão nas idades acima de 15 anos, refletindo o crescimento do número de veteranos no programa. De modo geral, não há mudanças abruptas "
        "no perfil etário, mas sim um aumento gradual do volume de alunos, mantendo o foco predominante no público pré-adolescente."
    )

    df_no_superior = df[df["nivel_ensino_lbl"] != "Ensino Superior"].copy()
    if pd.api.types.is_categorical_dtype(df_no_superior["nivel_ensino_lbl"]):
        df_no_superior["nivel_ensino_lbl"] = (
            df_no_superior["nivel_ensino_lbl"].cat.remove_unused_categories()
        )

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
            "nivel_ensino_lbl": "Nível de ensino",
        },
    )
    fig = eixo_ano(fig)
    fig.update_yaxes(autorange="reversed")
    show_plot(fig, "t1_def_media")

    texto(
        "A média da defasagem apresenta trajetória de melhora consistente entre 2022 e 2024 em todos os níveis de ensino, aproximando-se quase a zero, indicando redução da defasagem. "
        "O avanço é mais expressivo no Ensino Médio e no Fundamental II, que demonstram queda contínua ao longo dos três anos. Já o Fundamental I apresenta melhora entre 2022 e 2023, com leve estabilização em 2024. "
        "De forma geral, os dados sugerem evolução positiva no desempenho acadêmico e indicam impacto consistente do programa na redução da defasagem escolar."
    )

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
                "nivel_defasagem_lbl": "Nível de defasagem",
            },
        )
        fig.update_layout(barmode="stack")
        fig = eixo_ano(fig)
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
                "nivel_defasagem_lbl": "Nível de defasagem",
            },
        )
        show_plot(fig, "t2_def_rede_2024")

    texto(
        "A análise proporcional da defasagem evidencia melhora consistente ao longo dos anos. A parcela de alunos em fase cresce de forma contínua entre 2022 e 2024, enquanto a defasagem moderada "
        "reduz progressivamente e a severa permanece residual. Ao observar a rede de ensino em 2024, nota-se que a maior parte dos alunos da rede pública concentra-se na categoria moderada, embora também "
        "apresente volume expressivo em fase. Já na rede privada, predomina a categoria em fase, com baixa incidência de defasagem severa. Os dados sugerem avanço geral no enfrentamento da defasagem, "
        "mas indicam que, ou o desafio permanece mais intenso entre estudantes da rede pública, ou esse efeito pode estar associada a um efeito de seleção de bolsa."
    )

    col_def3, col_def4 = st.columns(2)

    with col_def3:
        df_idade = (
            df.groupby("nivel_defasagem_lbl", as_index=False)["idade"]
            .mean()
            .rename(columns={"idade": "Idade média"})
        )

        fig = px.bar(
            df_idade,
            x="nivel_defasagem_lbl",
            y="Idade média",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="Idade Média por Nível de Defasagem",
            labels={
                "nivel_defasagem_lbl": "Nível de defasagem",
                "Idade média": "Idade média",
            },
        )
        show_plot(fig, "t2_idade_def")

    with col_def4:
        df_fase = df.groupby(["nivel_ensino_lbl", "nivel_defasagem_lbl"], as_index=False).size()
        df_fase["proporcao"] = df_fase.groupby("nivel_ensino_lbl")["size"].transform(lambda x: x / x.sum())

        fig = px.bar(
            df_fase,
            x="nivel_ensino_lbl",
            y="proporcao",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="Distribuição Proporcional da Defasagem por Nível de Ensino",
            labels={
                "nivel_ensino_lbl": "Nível de ensino",
                "proporcao": "Proporção",
                "nivel_defasagem_lbl": "Nível de defasagem",
            },
        )
        fig.update_layout(barmode="stack")
        show_plot(fig, "t2_def_nivel")

    texto(
        "Ao analisar conjuntamente a idade média por nível de defasagem e a distribuição proporcional por nível de ensino, observa-se um padrão consistente: a defasagem mais severa está associada a alunos mais velhos "
        "e concentra-se, proporcionalmente, nas etapas mais avançadas da trajetória escolar. No Fundamental I, predomina a defasagem moderada, indicando que as dificuldades surgem já nas fases iniciais. No Fundamental II "
        "e no Ensino Médio, há aumento da proporção de alunos em fase, mas ainda se mantém parcela relevante em defasagem moderada. A categoria severa permanece residual, porém mais associada a idades mais elevadas, sugerindo "
        "acúmulo de dificuldades ao longo do tempo."
    )

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
            labels={
                "ida": "IDA",
                "iaa": "IAA",
                "nivel_defasagem_lbl": "Nível de defasagem",
            },
        )
        show_plot(fig, "t3_ida_iaa")

    texto(
        "A análise da autoavaliação (IAA), em relação ao nível de defasagem indica que, embora as medianas permaneçam elevadas em todos os grupos, alunos em defasagem severa apresentam leve redução na autoavaliação "
        "quando comparados aos que estão em fase ou com defasagem moderada. A dispersão entre IDA e IAA reforça a tendência positiva entre desempenho acadêmico e autoavaliação, embora haja forte sobreposição entre "
        "os grupos."
    )

    col_iaa3, col_iaa4 = st.columns(2)

    with col_iaa3:
        df_iaa_ano = df.groupby(["ano", "nivel_defasagem_lbl"], as_index=False)["iaa"].mean()
        df_iaa_ano = df_iaa_ano.rename(columns={"iaa": "IAA médio"})

        fig = px.line(
            df_iaa_ano,
            x="ano",
            y="IAA médio",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            markers=True,
            title="Evolução do IAA por Ano e Nível de Defasagem",
            labels={
                "ano": "Ano",
                "IAA médio": "IAA médio",
                "nivel_defasagem_lbl": "Nível de defasagem",
            },
        )
        fig = eixo_ano(fig)
        show_plot(fig, "t3_iaa_linha")

    with col_iaa4:
        df_iaa_pedra = (
            df.groupby("pedra_lbl", as_index=False)["iaa"]
            .mean()
            .rename(columns={"iaa": "IAA médio"})
        )

        fig = px.bar(
            df_iaa_pedra,
            x="pedra_lbl",
            y="IAA médio",
            color="pedra_lbl",
            color_discrete_map=CORES_PEDRA,
            title="IAA Médio por Pedra",
            labels={"pedra_lbl": "Pedra", "IAA médio": "IAA médio"},
        )
        fig.update_layout(showlegend=False)
        show_plot(fig, "t3_iaa_pedra")

    texto(
        "A evolução do IAA ao longo dos anos evidencia queda em 2023, seguida de recuperação em 2024 para todos os níveis de defasagem. O aumento é mais expressivo entre alunos em defasagem severa, sugerindo fortalecimento "
        "da percepção de autoeficácia. Por pedra, há progressão consistente, com Topázio apresentando a maior média e Quartzo a menor, sugerindo amadurecimento socioemocional ao longo da trajetória no programa."
    )

# =========================
# TAB 4 — Índice Psicopedagógico (IPP)
# =========================
with tab4:
    col_ipp1, col_ipp2 = st.columns(2)

    with col_ipp1:
        fig = px.scatter(
            df,
            x="ian",
            y="ipp",
            title="Relação entre IPP e IAN",
            height=420,
            trendline="ols",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            opacity=0.5,
            labels={
                "ian": "IAN (quanto menor, mais defasado)",
                "ipp": "IPP",
                "nivel_defasagem_lbl": "Nível de defasagem",
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

        fig, ax = plt.subplots(figsize=(6, 4))

        # remover fundo branco
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        # gráfico
        ax.fill_between(df_area["nivel_defasagem_lbl"], df_area["ian"], alpha=0.4, label="IAN")
        ax.fill_between(df_area["nivel_defasagem_lbl"], df_area["ipp"], alpha=0.4, label="IPP")

        # labels
        ax.set_xlabel("Nível de defasagem")
        ax.set_ylabel("Média do indicador")
        ax.set_title(
        "IAN e IPP por Nível de Defasagem",
        loc="left",   # alinha à esquerda
        pad=80        # espaço acima do título
    )

        # remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)

        # legenda
        ax.legend()

        st.pyplot(fig, use_container_width=True)

    texto(
        "A relação entre IPP e IAN mostra que a adequação acadêmica se deteriora claramente conforme aumenta a defasagem, enquanto o IPP varia de forma mais moderada entre os grupos. Esse comportamento sugere que o "
        "indicador psicopedagógico captura dimensões complementares à defasagem e pode atuar como fator de proteção."
    )

# =========================
# Footer insights
# =========================
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
