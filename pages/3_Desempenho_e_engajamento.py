import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

from utils.style import apply_global_style
from utils.components import texto, show_plot, page_title

# =========================
# Config / Load
# =========================
st.set_page_config(page_title="Desempenho e Engajamento", layout="wide")
apply_global_style()

page_title(
    "Desempenho e Engajamento",
    "Esta seção explora a relação entre desempenho acadêmico e engajamento dos alunos ao longo do tempo, buscando identificar padrões que ajudam a explicar sua evolução no programa."
)

DATA_CSV = "data/base_pede_limpa.csv"
df = pd.read_csv(DATA_CSV)

# =========================
# Helpers
# =========================
def norm_key(x) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip().lower()
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))
    s = s.replace("_", " ").replace("-", " ")
    s = " ".join(s.split())
    return s

def safe_years(series) -> list[int]:
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

def to_num(df_: pd.DataFrame, cols: list[str]) -> None:
    for c in cols:
        if c in df_.columns:
            df_[c] = pd.to_numeric(df_[c], errors="coerce")

# =========================
# Padronização de labels
# =========================
ROTULOS_NIVEL_ENSINO = {
    "fundamental1": "Fundamental I",
    "fundamental 1": "Fundamental I",
    "fundamental i": "Fundamental I",
    "fundamental2": "Fundamental II",
    "fundamental 2": "Fundamental II",
    "fundamental ii": "Fundamental II",
    "medio": "Ensino Médio",
    "ensino medio": "Ensino Médio",
    "superior": "Ensino Superior",
    "ensino superior": "Ensino Superior",
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

ROTULOS_JORNADA = {
    "avanco": "Avanço",
    "neutro": "Neutro",
    "recuo": "Recuo",
}

ORDEM_NIVEL_ENSINO = ["Fundamental I", "Fundamental II", "Ensino Médio", "Ensino Superior"]
ORDEM_DEFASAGEM = ["Em fase", "Defasagem moderada", "Defasagem severa"]
ORDEM_PEDRA = ["Quartzo", "Ágata", "Ametista", "Topázio"]
ORDEM_JORNADA = ["Recuo", "Neutro", "Avanço"]

# =========================
# Cores
# =========================
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

CORES_JORNADA = {
    "Recuo": "#145089",
    "Neutro": "#7390AA",
    "Avanço": "#FDD324",
}

# =========================
# Tipagem + colunas *_lbl
# =========================
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
anos = safe_years(df["ano"])

to_num(df, ["ida", "ieg", "ian", "ipp", "ipv", "ips", "inde"])

df["nivel_ensino_lbl"] = (
    df["nivel_ensino"].map(norm_key).str.replace(" ", "", regex=False).map(ROTULOS_NIVEL_ENSINO)
)
df["nivel_defasagem_lbl"] = df["nivel_defasagem"].map(norm_key).map(ROTULOS_DEFASAGEM)
df["pedra_lbl"] = df["pedra"].map(norm_key).map(ROTULOS_PEDRA)
df["jornada_lbl"] = df["jornada"].map(norm_key).map(ROTULOS_JORNADA)

df["nivel_ensino_lbl"] = pd.Categorical(df["nivel_ensino_lbl"], categories=ORDEM_NIVEL_ENSINO, ordered=True)
df["nivel_defasagem_lbl"] = pd.Categorical(df["nivel_defasagem_lbl"], categories=ORDEM_DEFASAGEM, ordered=True)
df["pedra_lbl"] = pd.Categorical(df["pedra_lbl"], categories=ORDEM_PEDRA, ordered=True)
df["jornada_lbl"] = pd.Categorical(df["jornada_lbl"], categories=ORDEM_JORNADA, ordered=True)

# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Desempenho (IDA)", "Engajamento (IEG)", "Ponto de Virada (IPV)", "Multidimensionalidade", "Efetividade por Pedra"]
)

# ==========================================================
# TAB 1 — Desempenho (IDA)
# ==========================================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        df_ida_evol = (
            df.groupby("ano", as_index=False)["ida"]
            .mean()
            .sort_values("ano")
            .dropna()
        )

        fig = px.line(
            df_ida_evol,
            x="ano",
            y="ida",
            markers=True,
            title="Média do IDA por Ano",
            labels={"ida": "IDA médio"},
        )
        fig = eixo_ano_inteiro(fig, anos)
        show_plot(fig, "ida_media_ano")

    with col2:
        df_box = df[["ano", "ida"]].dropna()
        fig = px.box(
            df_box,
            x="ano",
            y="ida",
            title="Distribuição do IDA por Ano",
            labels={"ida": "IDA"},
        )
        fig = eixo_ano_inteiro(fig, anos)
        show_plot(fig, "ida_box_ano")

    texto(
        "A média do IDA apresenta crescimento de 2022 para 2023, indicando melhora no desempenho acadêmico no período, seguida de leve recuo em 2024, embora mantendo patamar superior ao observado em 2022. A distribuição confirma relativa estabilidade ao longo dos anos, com medianas próximas e dispersão semelhante."
    )

    df_filtrado = df[df["nivel_ensino_lbl"] != "Ensino Superior"].copy()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_2022 = df_filtrado[df_filtrado["ano"] == 2022]
        df_fase_2022 = df_2022.groupby("nivel_ensino_lbl", as_index=False)["ida"].mean()

        fig_2022 = px.bar(
            df_fase_2022,
            x="nivel_ensino_lbl",
            y="ida",
            title="IDA por Nível de Ensino – 2022",
            color="nivel_ensino_lbl",
            color_discrete_map=CORES_NIVEL_ENSINO,
            labels={"ida": "IDA médio", "nivel_ensino_lbl": "Nível de ensino"},
        )
        show_plot(fig_2022, "ida_fase_2022")

    with col_b:
        df_2024 = df_filtrado[df_filtrado["ano"] == 2024]
        df_fase_2024 = df_2024.groupby("nivel_ensino_lbl", as_index=False)["ida"].mean()

        fig_2024 = px.bar(
            df_fase_2024,
            x="nivel_ensino_lbl",
            y="ida",
            title="IDA por Nível de Ensino – 2024",
            color="nivel_ensino_lbl",
            color_discrete_map=CORES_NIVEL_ENSINO,
            labels={"ida": "IDA médio", "nivel_ensino_lbl": "Nível de ensino"},
        )
        show_plot(fig_2024, "ida_fase_2024")

    with col_c:
        df_def = df.groupby("nivel_defasagem_lbl", as_index=False)["ida"].mean().dropna()
        fig = px.bar(
            df_def,
            x="nivel_defasagem_lbl",
            y="ida",
            title="Média do IDA por Nível de Defasagem",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            labels={"ida": "IDA médio", "nivel_defasagem_lbl": "Nível de defasagem"},
        )
        show_plot(fig, "ida_defasagem")

    texto(
        "A comparação do IDA entre 2022 e 2024 indica avanço transversal entre as etapas de ensino. Por nível de defasagem, alunos em fase apresentam as maiores médias, seguidos por defasagem moderada, enquanto a categoria de defasagem severa concentra os menores valores."
    )

# ==========================================================
# TAB 2 — Engajamento (IEG)
# ==========================================================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        df_scatter = df[["ieg", "ida", "nivel_defasagem_lbl"]].dropna()
        fig = px.scatter(
            df_scatter,
            x="ieg",
            y="ida",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="IEG x IDA por Nível de Defasagem",
            opacity=0.7,
            labels={"ieg": "IEG (Engajamento)", "ida": "IDA", "nivel_defasagem_lbl": "Nível de defasagem"},
        )
        show_plot(fig, "ieg_ida_scatter")

    with col2:
        df_box_ieg = df[["nivel_defasagem_lbl", "ieg"]].dropna()
        fig = px.box(
            df_box_ieg,
            x="nivel_defasagem_lbl",
            y="ieg",
            color="nivel_defasagem_lbl",
            color_discrete_map=CORES_DEFASAGEM,
            category_orders={"nivel_defasagem_lbl": ORDEM_DEFASAGEM},
            title="Distribuição do IEG por Nível de Defasagem",
            labels={"ieg": "IEG", "nivel_defasagem_lbl": "Nível de defasagem"},
        )
        show_plot(fig, "ieg_box_def")

    texto(
        "A relação entre IEG e IDA evidencia tendência positiva. A distribuição do IEG por nível de defasagem indica medianas mais altas entre alunos em fase e em defasagem moderada, enquanto defasagem severa apresenta maior dispersão."
    )

    df_pedra_ieg = df.groupby("pedra_lbl", as_index=False)["ieg"].mean().dropna()
    fig = px.bar(
        df_pedra_ieg,
        x="pedra_lbl",
        y="ieg",
        color="pedra_lbl",
        color_discrete_map=CORES_PEDRA,
        title="IEG Médio por Pedra",
        labels={"pedra_lbl": "Pedra", "ieg": "IEG médio"},
    )
    fig.update_layout(showlegend=False)
    show_plot(fig, "ieg_pedra")

    texto(
        "O IEG médio por pedra revela progressão clara ao longo das fases do programa. Topázio apresenta o maior nível de engajamento, seguido por Ametista, enquanto Ágata e Quartzo registram médias inferiores."
    )

# ==========================================================
# TAB 3 — Ponto de Virada (IPV)
# ==========================================================
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        df_trans = df["jornada_lbl"].value_counts(dropna=False).reindex(ORDEM_JORNADA).reset_index()
        df_trans.columns = ["Tipo", "Qtd"]

        fig = px.bar(
            df_trans,
            x="Tipo",
            y="Qtd",
            text="Qtd",
            color="Tipo",
            color_discrete_map=CORES_JORNADA,
            title="Distribuição de Avanços, Recuos e Neutros no IPV",
        )
        fig.update_traces(textposition="outside")
        show_plot(fig, "ipv_trans")

    with col2:
        df_vinc = df.groupby(["nivel_ensino_lbl", "jornada_lbl"], as_index=False).size().rename(columns={"size": "Qtd"})
        piv = df_vinc.pivot(index="nivel_ensino_lbl", columns="jornada_lbl", values="Qtd").fillna(0)
        piv["Total"] = piv.sum(axis=1)
        piv["% Recuaram"] = (piv.get("Recuo", 0) / piv["Total"] * 100).replace([float("inf"), -float("inf")], pd.NA)
        df_plot = piv.reset_index()

        fig = px.bar(
            df_plot,
            x="nivel_ensino_lbl",
            y="% Recuaram",
            text=df_plot["% Recuaram"].round(1),
            color="nivel_ensino_lbl",
            color_discrete_map=CORES_NIVEL_ENSINO,
            title="% que Recuaram por Nível de Ensino",
            labels={"nivel_ensino_lbl": "Nível de ensino", "% Recuaram": "% que recuaram"},
        )
        fig.update_traces(textposition="outside")
        show_plot(fig, "ipv_recuo_nivel")

    texto(
        "A distribuição do IPV indica predominância de trajetórias neutras, seguida por avanços e menor parcela de recuos. O percentual de recuos tende a ser maior nas etapas iniciais, reforçando a importância de acompanhamento mais intensivo no começo da trajetória."
    )

    indicadores = ["ida", "ieg", "ian", "ipp", "ipv", "ips", "inde"]
    corr = df[indicadores].corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Heatmap de Correlação dos Indicadores",
    )
    show_plot(fig, "heatmap_corr")

    texto(
        "O heatmap de correlação evidencia a natureza multidimensional do desenvolvimento dos alunos. Observa-se que o IPV apresenta associação moderada a forte com IPP, IDA e IEG, indicando influência combinada de fatores psicopedagógicos, desempenho acadêmico e engajamento."
    )

    st.divider()
    st.subheader("Influência de Comportamentos no IPV ao Longo do Tempo (Painel com Efeitos Fixos)")

    anos_interesse = [2022, 2023, 2024]
    df_tmp = df[df["ano"].isin(anos_interesse)].copy()

    contagem = df_tmp.groupby("id_aluno")["ano"].nunique()
    alunos_completos = contagem[contagem == len(anos_interesse)].index
    df_painel = df_tmp[df_tmp["id_aluno"].isin(alunos_completos)].copy()

    variaveis = ["ida", "ieg", "ipp"]
    df_painel = df_painel.sort_values(["id_aluno", "ano"])
    df_painel[variaveis] = df_painel.groupby("ano")[variaveis].transform(lambda x: (x - x.mean()) / x.std())

    df_panel = df_painel.set_index(["id_aluno", "ano"])
    X = sm.add_constant(df_panel[variaveis])
    y = df_panel["ipv"]

    modelo = PanelOLS(y, X, entity_effects=True, time_effects=True)
    resultado = modelo.fit()

    coef = resultado.params.drop("const", errors="ignore").sort_values(ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig_coef, ax = plt.subplots()

        coef.plot(kind="bar", ax=ax)

        # remover fundo branco
        fig_coef.patch.set_alpha(0)
        ax.set_facecolor("none")

        # remover bordas (frame)
        for spine in ax.spines.values():
            spine.set_visible(False)

        # título e label
        ax.set_title("Coeficientes Padronizados (efeitos fixos)", loc="left", pad=20)
        ax.set_ylabel("Impacto no IPV")
        coef.plot(kind="bar", ax=ax, color="#145089")

        # grid leve (opcional, melhora leitura)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        st.pyplot(fig_coef, use_container_width=True)

    with c2:
        fig3d = px.scatter_3d(
            df_painel.dropna(subset=["ieg", "ida", "ipp", "pedra_lbl"]),
            x="ieg",
            y="ida",
            z="ipp",
            color="pedra_lbl",
            title="Dispersão 3D – IEG, IDA e IPP por Pedra",
            color_discrete_map=CORES_PEDRA,
        )
        fig3d.update_layout(scene=dict(xaxis_title="IEG", yaxis_title="IDA", zaxis_title="IPP"))
        show_plot(fig3d, "scatter3d")

    texto(
        "Os coeficientes padronizados sugerem maior influência do IPP sobre variações no IPV ao longo do tempo, seguido por IEG e IDA, reforçando que o ponto de virada depende de dimensões acadêmicas e psicopedagógicas em conjunto."
    )

# ==========================================================
# TAB 4 — Multidimensionalidade
# ==========================================================
with tab4:
    evolucao = df.groupby(["ano", "pedra_lbl"], as_index=False)["ida"].mean().dropna()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            evolucao,
            x="ano",
            y="ida",
            color="pedra_lbl",
            color_discrete_map=CORES_PEDRA,
            markers=True,
            title="Evolução do IDA por Pedra",
            labels={"ida": "IDA médio", "pedra_lbl": "Pedra"},
        )
        fig = eixo_ano_inteiro(fig, anos)
        show_plot(fig, "ida_pedra_linha")

    with col2:
        df_sorted = df.sort_values(["id_aluno", "ano"]).copy()
        df_sorted["ipv_avanco"] = df_sorted.groupby("id_aluno")["ipv"].diff().fillna(0) > 0

        percent_avanco = df_sorted.groupby("pedra_lbl", as_index=False)["ipv_avanco"].mean()
        percent_avanco["ipv_avanco"] *= 100

        fig = px.bar(
            percent_avanco,
            x="pedra_lbl",
            y="ipv_avanco",
            color="pedra_lbl",
            color_discrete_map=CORES_PEDRA,
            title="% de Avanços no IPV por Pedra",
            text=percent_avanco["ipv_avanco"].round(1),
            labels={"ipv_avanco": "% de avanços", "pedra_lbl": "Pedra"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(showlegend=False)
        show_plot(fig, "ipv_avanco_pedra")

    texto(
        "A análise multidimensional evidencia evolução heterogênea entre as pedras: fases mais avançadas tendem a concentrar melhores resultados acadêmicos e maior taxa de avanço no IPV, enquanto etapas iniciais apresentam maior vulnerabilidade."
    )

# ==========================================================
# TAB 5 — Efetividade por Pedra
# ==========================================================
with tab5:
    indicador = "inde"

    df_long = df.groupby(["ano", "pedra_lbl"], as_index=False)[indicador].mean().dropna()

    fig = px.line(
        df_long,
        x="ano",
        y=indicador,
        color="pedra_lbl",
        color_discrete_map=CORES_PEDRA,
        markers=True,
        title=f"Evolução do {indicador.upper()} por Pedra",
        labels={indicador: f"{indicador.upper()} médio", "pedra_lbl": "Pedra"},
    )
    fig = eixo_ano_inteiro(fig, anos)
    show_plot(fig, "efetividade_inde")

    ian_medio = df.groupby(["ano", "pedra_lbl"], as_index=False)["ian"].mean().dropna()

    fig2 = px.bar(
        ian_medio,
        x="ano",
        y="ian",
        color="pedra_lbl",
        color_discrete_map=CORES_PEDRA,
        barmode="group",
        title="Média de IAN por Pedra ao Longo dos Anos",
        labels={"ian": "IAN médio", "pedra_lbl": "Pedra"},
    )
    fig2 = eixo_ano_inteiro(fig2, anos)
    show_plot(fig2, "ian_pedra_bar")

    texto(
        "A evolução do INDE por pedra sugere estabilidade com leve tendência de crescimento nas fases mais avançadas. A média do IAN melhora progressivamente entre 2022 e 2024, indicando avanço na adequação escolar ao longo do tempo."
    )

# =========================
# Footer
# =========================
st.divider()

st.markdown(
"""
<div style="font-size:18px; font-weight:700; margin-bottom:10px;">
Principais insights
</div>
""",
unsafe_allow_html=True
)

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
    <b>Engajamento e desempenho</b><br>
    Alunos com maior IEG tendem a apresentar melhores resultados acadêmicos.
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
    <b>Evolução na trajetória</b><br>
    Fases mais avançadas do programa concentram maiores níveis de engajamento e desempenho.
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
    <b>Ponto de virada</b><br>
    O IPV é influenciado por fatores acadêmicos, psicopedagógicos e de engajamento.
    </div>
    """, unsafe_allow_html=True)
