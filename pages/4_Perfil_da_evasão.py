import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

from utils.style import apply_global_style
from utils.components import texto, show_plot, page_title

# =========================
# Config / Load
# =========================
st.set_page_config(page_title="Fatores de Risco e Evasão", layout="wide")
apply_global_style()

page_title(
    "Fatores de Risco e Evasão",
    "Análise dos padrões que antecedem quedas e do perfil dos alunos em maior risco."
)

DATA_CSV = "data/base_pede_limpa.csv"
df = pd.read_csv(DATA_CSV)

# =========================
# Helpers
# =========================
def to_num(df_: pd.DataFrame, cols: list[str]) -> None:
    for c in cols:
        if c in df_.columns:
            df_[c] = pd.to_numeric(df_[c], errors="coerce")

def safe_years(series: pd.Series) -> list[int]:
    y = pd.to_numeric(series, errors="coerce").dropna()
    return sorted(y.astype(int).unique())

def eixo_ano_inteiro(fig, anos: list[int]):
    fig.update_xaxes(
        tickmode="array",
        tickvals=anos,
        ticktext=[str(a) for a in anos],
        title_text="Ano",
    )
    return fig

# =========================
# Tipagem + labels
# =========================
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
anos = safe_years(df["ano"])

to_num(df, ["ida", "ieg", "ips", "ipv", "ian", "ipp", "inde"])

if "evadido" in df.columns:
    if df["evadido"].dropna().isin([0, 1]).all():
        df["evadido"] = df["evadido"].astype(bool)

df["evadido_txt"] = df["evadido"].map({False: "Não Evadiu", True: "Evadiu"})

df["jornada_txt"] = (
    df.get("jornada", pd.Series(index=df.index, dtype="object"))
    .astype(str)
    .str.lower()
    .map({"recuo": "Recuo", "neutro": "Neutro", "avanco": "Avanço"})
)

# =========================
# Cores
# =========================
CORES_NIVEL_ENSINO = {
    "fundamental1": "#FDD324",
    "fundamental2": "#EE7F33",
    "medio": "#EC3237",
    "superior": "#145089",
}
CORES_DEFASAGEM = {"em fase": "#145089", "moderada": "#FDD324", "severa": "#EE7F33"}
CORES_EVASAO = {"Evadiu": "#7390AA", "Não Evadiu": "#EE7F33"}
CORES_QUEDA = {True: "#145089", False: "#FDD324"}
CORES_JORNADA = {"Recuo": "#145089", "Neutro": "#7390AA", "Avanço": "#FDD324"}
CORES_ESTUDANTE = {"veterano": "#EE7F33", "ingressante": "#FDD324"}

# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Perfil da Evasão",
        "Padrões Psicossociais (IPS) e Quedas",
        "Ponto de Virada (IPV)",
        "Perfil de Risco Consolidado",
    ]
)

# ==========================================================
# TAB 1 — Perfil da Evasão
# ==========================================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        df_pre_2024 = df[df["ano"] != 2024].copy()
        evasao_fase = df_pre_2024.groupby("nivel_ensino", as_index=False)["evadido"].mean()
        evasao_fase["evasao_pct"] = evasao_fase["evadido"] * 100

        fig = px.bar(
            evasao_fase,
            x="nivel_ensino",
            y="evasao_pct",
            color="nivel_ensino",
            color_discrete_map=CORES_NIVEL_ENSINO,
            text="evasao_pct",
            title="Evasão por Nível de Ensino (até 2023)",
            labels={"nivel_ensino": "Nível de ensino", "evasao_pct": "Taxa de evasão (%)"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False)
        show_plot(fig, "evasao_fase")

    with col2:
        fig = px.box(
            df.dropna(subset=["ieg", "evadido_txt"]),
            x="evadido_txt",
            y="ieg",
            color="evadido_txt",
            color_discrete_map=CORES_EVASAO,
            title="Distribuição de IEG: Evadidos vs Não Evadidos",
            points="all",
            labels={"evadido_txt": "Status de evasão", "ieg": "IEG"},
        )
        fig.update_layout(showlegend=False)
        show_plot(fig, "ieg_evasao")

    texto(
        "A taxa de evasão por nível de ensino indica maior vulnerabilidade nas etapas intermediárias e finais da educação básica. A comparação do IEG entre evadidos e não evadidos reforça o engajamento como fator protetivo: alunos que permanecem tendem a apresentar IEG mais alto e menos disperso."
    )

    col3, col4 = st.columns(2)

    comp_defasagem = (
        df.dropna(subset=["evadido_txt", "nivel_defasagem"])
        .groupby(["evadido_txt", "nivel_defasagem"])
        .size()
        .reset_index(name="contagem")
    )

    with col3:
        evadiu = comp_defasagem[comp_defasagem["evadido_txt"] == "Evadiu"]
        fig = px.pie(
            evadiu,
            names="nivel_defasagem",
            values="contagem",
            title="Composição da Defasagem – Evadiu",
            color="nivel_defasagem",
            color_discrete_map=CORES_DEFASAGEM,
            hole=0.35,
        )
        show_plot(fig, "defasagem_evadiu")

    with col4:
        nao_evadiu = comp_defasagem[comp_defasagem["evadido_txt"] == "Não Evadiu"]
        fig = px.pie(
            nao_evadiu,
            names="nivel_defasagem",
            values="contagem",
            title="Composição da Defasagem – Não Evadiu",
            color="nivel_defasagem",
            color_discrete_map=CORES_DEFASAGEM,
            hole=0.35,
        )
        show_plot(fig, "defasagem_nao_evadiu")

    texto(
        "A composição do nível de defasagem entre evadidos e não evadidos sugere que a evasão não se concentra apenas em casos de maior defasagem. Há participação relevante também de alunos em fase, indicando que fatores não acadêmicos, como vínculo e engajamento, podem ser decisivos."
    )

# ==========================================================
# TAB 2 — IPS e Quedas
# ==========================================================
with tab2:
    anos_anteriores = [2022, 2023]
    df_prev = df[df["ano"].isin(anos_anteriores)].copy()

    ips_evolucao = df_prev.groupby(["ano", "evadido"], as_index=False)["ips"].mean()

    fig = px.line(
        ips_evolucao,
        x="ano",
        y="ips",
        color="evadido",
        color_discrete_map=CORES_QUEDA,
        markers=True,
        title="Evolução do IPS antes da queda: Grupo Caiu vs Controle",
        labels={"ips": "IPS médio", "evadido": "Grupo (evadiu?)"},
    )
    fig = eixo_ano_inteiro(fig, anos_anteriores)
    show_plot(fig, "ips_pre_queda")

    texto(
        "A evolução do IPS antes da queda revela padrão semelhante entre grupos, mas com queda mais acentuada no grupo que posteriormente piora ou evade. Isso sugere que a deterioração psicossocial pode anteceder sinais mais claros de queda."
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            df.dropna(subset=["nivel_defasagem", "ips"]),
            x="nivel_defasagem",
            y="ips",
            color="nivel_defasagem",
            color_discrete_map=CORES_DEFASAGEM,
            title="Distribuição de IPS por Nível de Defasagem",
            points="all",
            labels={"nivel_defasagem": "Nível de defasagem", "ips": "IPS"},
        )
        fig.update_layout(showlegend=False)
        show_plot(fig, "ips_defasagem")

    with col2:
        ips_fase = df.groupby("nivel_ensino", as_index=False)["ips"].mean()
        fig = px.bar(
            ips_fase,
            x="nivel_ensino",
            y="ips",
            color="nivel_ensino",
            color_discrete_map=CORES_NIVEL_ENSINO,
            text="ips",
            title="IPS Médio por Nível de Ensino",
            labels={"nivel_ensino": "Nível de ensino", "ips": "IPS médio"},
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(showlegend=False)
        show_plot(fig, "ips_fase")

    texto(
        "O IPS varia moderadamente por defasagem: alunos em fase tendem a apresentar mediana ligeiramente superior. Por nível de ensino, o Ensino Superior apresenta valores mais altos, sugerindo maior estabilidade psicossocial nas etapas avançadas."
    )

# ==========================================================
# TAB 3 — Ponto de Virada (IPV)
# ==========================================================
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        dist_jornada = df["jornada_txt"].value_counts(dropna=False).reset_index()
        dist_jornada.columns = ["jornada", "contagem"]

        fig = px.bar(
            dist_jornada,
            x="jornada",
            y="contagem",
            color="jornada",
            color_discrete_map=CORES_JORNADA,
            text="contagem",
            title="Distribuição Geral de Alunos por Jornada",
            labels={"jornada": "Jornada", "contagem": "Número de alunos"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        show_plot(fig, "dist_jornada")

    with col2:
        ipv_grouped = df.groupby(["ano", "tipo_estudante"], as_index=False)["ipv"].mean().dropna()

        fig = px.bar(
            ipv_grouped,
            x="ano",
            y="ipv",
            color="tipo_estudante",
            color_discrete_map=CORES_ESTUDANTE,
            text="ipv",
            title="IPV Médio: Veterano x Ingressante",
            labels={"ipv": "IPV médio", "tipo_estudante": "Tipo de estudante"},
        )
        fig = eixo_ano_inteiro(fig, anos)
        fig.update_traces(texttemplate="%{text:.2f}", textposition="inside")
        fig.update_layout(barmode="group")
        show_plot(fig, "ipv_tipo")

    texto(
        "O IPV apresenta predominância de trajetórias neutras, seguido por avanços e menor parcela de recuos. Na comparação entre ingressantes e veteranos, as médias oscilam levemente ao longo do tempo, com tendência de convergência em 2024."
    )

    X_cols = ["ieg", "ida", "ian", "ips", "ipp"]
    dados_rf = df.dropna(subset=X_cols + ["ipv"]).copy()

    X = pd.get_dummies(dados_rf[X_cols], drop_first=True)
    y = dados_rf["ipv"]

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X, y)

    importancia = (
        pd.DataFrame({"fator": X.columns, "importancia": rf.feature_importances_})
        .sort_values(by="importancia", ascending=True)
    )

    fig = px.bar(
        importancia,
        x="importancia",
        y="fator",
        orientation="h",
        text="importancia",
        color="importancia",
        color_continuous_scale="Blues",
        title="Importância dos Fatores para o IPV utilizando Random Forest",
        labels={"importancia": "Importância", "fator": "Fator"},
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(showlegend=False)
    show_plot(fig, "rf_importancia_ipv")

    texto(
        "A importância dos fatores sugere maior peso do IPP e do IEG na explicação do IPV, seguidos por IDA. IPS e IAN tendem a ter contribuição menor no modelo, reforçando a leitura de que o ponto de virada é multidimensional e fortemente influenciado por aspectos psicopedagógicos e de engajamento."
    )

# ==========================================================
# TAB 4 — Perfil de Risco Consolidado
# ==========================================================
with tab4:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        df_risco = df.dropna(subset=["ieg", "ida"]).copy()
        cut_ieg = df_risco["ieg"].median()
        cut_ida = df_risco["ida"].median()

        def class_quadrant(row):
            if row["ieg"] >= cut_ieg and row["ida"] >= cut_ida:
                return "Alto Engajamento / Alto Desempenho"
            if row["ieg"] < cut_ieg and row["ida"] >= cut_ida:
                return "Baixo Engajamento / Alto Desempenho"
            if row["ieg"] >= cut_ieg and row["ida"] < cut_ida:
                return "Alto Engajamento / Baixo Desempenho"
            return "Baixo Engajamento / Baixo Desempenho"

        df_risco["quadrante"] = df_risco.apply(class_quadrant, axis=1)

        fig = px.scatter(
            df_risco,
            x="ieg",
            y="ida",
            color="quadrante",
            hover_data=["id_aluno"],
            title="Matriz de Risco: IEG x IDA",
            labels={"ieg": "IEG", "ida": "IDA"},
        )

        fig.add_shape(
            type="line",
            x0=cut_ieg, x1=cut_ieg,
            y0=df_risco["ida"].min(), y1=df_risco["ida"].max(),
            line=dict(color="black", dash="dash"),
        )
        fig.add_shape(
            type="line",
            y0=cut_ida, y1=cut_ida,
            x0=df_risco["ieg"].min(), x1=df_risco["ieg"].max(),
            line=dict(color="black", dash="dash"),
        )

        show_plot(fig, "matriz_risco")

    with col_p2:
        df_prof = df.dropna(subset=["nivel_defasagem", "evadido"]).copy()
        df_prof["perfil"] = df_prof["nivel_defasagem"].astype(str)

        evasao_perfil = df_prof.groupby("perfil", as_index=False)["evadido"].mean()
        evasao_perfil["evasao_pct"] = evasao_perfil["evadido"] * 100

        fig = px.bar(
            evasao_perfil,
            x="perfil",
            y="evasao_pct",
            color="perfil",
            color_discrete_map=CORES_DEFASAGEM,
            text="evasao_pct",
            title="Probabilidade de Evasão por Perfil (defasagem)",
            labels={"perfil": "Perfil do aluno", "evasao_pct": "Probabilidade de evasão (%)"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False)
        show_plot(fig, "evasao_perfil")

    texto(
        "Os gráficos indicam que o risco de evasão está associado tanto ao nível de defasagem quanto à combinação entre engajamento e desempenho. A matriz de risco mostra que alunos com baixo engajamento e baixo desempenho concentram maior vulnerabilidade, enquanto níveis mais altos de engajamento tendem a se associar a melhores resultados acadêmicos. Já a análise por perfil de defasagem revela aumento da probabilidade de evasão conforme a defasagem se torna mais severa, destacando esse grupo como prioritário para intervenções de apoio."
    )

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div style="
            border-left:6px solid #145089;
            background:#f8fafc;
            padding:14px 16px;
            border-radius:10px;
            font-size:14px;
        ">
        <b>Engajamento</b><br>
        Alunos com menor IEG apresentam maior probabilidade de evasão.
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div style="
            border-left:6px solid #145089;
            background:#f8fafc;
            padding:14px 16px;
            border-radius:10px;
            font-size:14px;
        ">
        <b>Etapas críticas</b><br>
        O risco de evasão aumenta nas transições do Fundamental II e Ensino Médio.
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    
    st.markdown(
        """
        <div style="
            border-left:6px solid #145089;
            background:#f8fafc;
            padding:14px 16px;
            border-radius:10px;
            font-size:14px;
        ">
        <b>Sinais de alerta</b><br>
        Quedas em IPS e engajamento tendem a anteceder pioras na trajetória escolar.
        </div>
        """,
        unsafe_allow_html=True
    )
    