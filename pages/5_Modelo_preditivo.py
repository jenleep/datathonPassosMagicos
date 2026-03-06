import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.edu_pipeline import SchoolRiskPipeline
from sklearn.metrics import classification_report

# =========================
# Config / Load
# =========================
st.set_page_config(page_title="Classificador de Risco Escolar", layout="wide")
st.title("Classificador de Risco Escolar")
st.caption("Preencha os campos e clique em **Classificar** para estimar a probabilidade de piora da defasagem.")


data_path = r"C:/Users/jenil/OneDrive/Documents/Faculdade/Tech Challenge 5/datathon/data/base_pede_modelo.csv"
df = pd.read_csv(data_path)

def risk_style(risk: float):
    if risk < 0.33:
        return ("Baixo", "#2A9D8F", "#E7F6F3")  # teal
    elif risk < 0.66:
        return ("Médio", "#F4A261", "#FFF3E8")  # laranja suave
    return ("Alto", "#E63946", "#FFE9EC")      # vermelho suave

def risk_card(risk: float):
    faixa, cor, fundo = risk_style(risk)
    st.markdown(
        f"""
        <div style="
            border-left: 10px solid {cor};
            background:{fundo};
            padding:16px 18px;
            border-radius:14px;
            box-shadow: 0 1px 0 rgba(0,0,0,0.03);
        ">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="font-size:18px; font-weight:700;">Risco: {faixa}</div>
            <div style="
                padding:6px 10px;
                border-radius:999px;
                background:{cor};
                color:white;
                font-weight:700;
                font-size:12px;
            "> {faixa.upper()} </div>
          </div>
          <div style="margin-top:10px; font-size:34px; font-weight:800;">
            {risk*100:.1f}%
          </div>
          <div style="margin-top:6px; color:#334155; font-size:14px;">
            Probabilidade estimada de piora da defasagem.
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# Treino pipeline (mantive sua lógica)
# =========================
DESIRED_FEATURES = ["fase", "ano_ingresso", "ipv", "ian", "ipp", "matematica", "portugues", "defasagem"]
FEATURE_COLS = [c for c in DESIRED_FEATURES if c in df.columns]
if len(FEATURE_COLS) != len(DESIRED_FEATURES):
    missing = [c for c in DESIRED_FEATURES if c not in FEATURE_COLS]
    st.warning(f"Colunas ausentes no CSV: {missing}. Usando: {FEATURE_COLS}")

pipeline = SchoolRiskPipeline(n_components=4)
pipeline.fit_from_df(df, feature_cols=FEATURE_COLS)

# =========================
# UI — Card com formulário + resultado ao lado
# =========================
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.subheader("Entrada do aluno")

    with st.form("form_risco", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Contexto**")
            fase = st.number_input("Fase", min_value=0, max_value=8, value=6, step=1)
            ano_ingresso = st.number_input("Ano de ingresso", min_value=2016, max_value=2024, value=2022, step=1)

        with c2:
            st.markdown("**Defasagem**")
            # Se defasagem for negativa (ex.: -2 a 0), slider faz sentido
            defasagem = st.slider("Defasagem (anos)", min_value=-2, max_value=0, value=0, step=1)

        with c3:
            st.markdown("**Notas**")
            matematica = st.number_input("Matemática", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
            portugues = st.number_input("Português", min_value=0.0, max_value=10.0, value=6.0, step=0.1)

        st.divider()
        st.markdown("**Indicadores**")
        c4, c5, c6 = st.columns(3)

        with c4:
            ipv = st.number_input("IPV", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
        with c5:
            ian = st.number_input("IAN", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
        with c6:
            ipp = st.number_input("IPP", min_value=0.0, max_value=10.0, value=6.0, step=0.1)

        submitted = st.form_submit_button("Classificar")

    dados_usuario = pd.DataFrame([{
        "fase": fase,
        "ano_ingresso": ano_ingresso,
        "ipv": ipv,
        "ian": ian,
        "ipp": ipp,
        "matematica": matematica,
        "portugues": portugues,
        "defasagem": defasagem,
    }])

with right:
    st.subheader("Resultado")
    st.info("Clique em **Classificar** para ver a probabilidade e a faixa de risco.")

    if submitted:
        with st.spinner("Avaliando..."):
            try:
                proba = pipeline.predict_risk(dados_usuario)
                risk = float(proba[0])

                # faixa simples (ajuste como preferir)
                if risk < 0.33:
                    faixa = "Baixo"
                    st.success(f"Risco: **{faixa}**")
                elif risk < 0.66:
                    faixa = "Médio"
                    st.warning(f"Risco: **{faixa}**")
                else:
                    faixa = "Alto"
                    st.error(f"Risco: **{faixa}**")

                st.metric("Probabilidade de piora", f"{risk:.1%}")

                # barra simples de progresso (bom pra UI)
                st.progress(min(max(risk, 0.0), 1.0))

                # detalhes (opcional) — mostra a entrada resumida
                with st.expander("Ver dados inseridos"):
                    st.dataframe(dados_usuario, use_container_width=True)

            except ValueError as e:
                msg = str(e)
                st.error(f"Erro ao obter previsão: {msg}")

# =========================
# Report (colapsado para não “quebrar” a página)
# =========================
with st.expander("Relatório de classificação (dados de treino)"):
    X_train = df[pipeline.feature_names_]
    y_train = df["piorou_defasagem"]
    X_train_prepared = pipeline._prepare_features(X_train, fit=False)
    y_pred = pipeline.predict(X_train_prepared)

    report = classification_report(y_train, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.dataframe(report_df, use_container_width=True)