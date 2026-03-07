# datathonPassosMagicos

# 📊 Datathon — Passos Mágicos

Projeto desenvolvido para o **Datathon Passos Mágicos**, com o objetivo de analisar a trajetória educacional de alunos participantes do programa e identificar **fatores que influenciam o Ponto de Virada (IPV)** ao longo do tempo.

A aplicação foi construída em **Python + Streamlit** e apresenta análises exploratórias, visualizações interativas e um modelo preditivo baseado nos indicadores educacionais do programa.

---

# 🎯 Objetivo do Projeto

O objetivo central do projeto é responder à seguinte pergunta:

**Quais comportamentos — acadêmicos, emocionais ou de engajamento — mais influenciam o IPV ao longo do tempo?**

Para isso, o projeto:

- Analisa a evolução dos indicadores educacionais
- Investiga padrões de desempenho e engajamento
- Identifica fatores associados ao **Ponto de Virada (IPV)**
- Desenvolve um **modelo preditivo** para estimar o IPV

---

# 📚 Sobre os Indicadores

Os dados utilizados no projeto incluem indicadores educacionais desenvolvidos pelo programa:

| Indicador | Descrição |
|---|---|
| **IAA** | Indicador de Aprendizagem Acadêmica |
| **IEG** | Indicador de Engajamento |
| **IPS** | Indicador Psicossocial |
| **IDA** | Indicador de Desempenho Acadêmico |
| **IPP** | Índice Psicopedagógico |
| **IAN** | Indicador de Adequação ao Nível |
| **IPV** | Índice de Ponto de Virada |

Esses indicadores permitem avaliar diferentes dimensões do desenvolvimento dos alunos ao longo dos anos.

---

# 📈 Estrutura da Aplicação

A aplicação está organizada em páginas no **Streamlit**, cada uma explorando uma dimensão da análise.

## 1️⃣ Perfil dos Alunos e Defasagem

Analisa características demográficas e educacionais dos alunos:

- Distribuição por idade
- Distribuição por gênero
- Rede de ensino
- Evolução da defasagem escolar
- Relação entre fase escolar e defasagem

---

## 2️⃣ Trajetória Educacional

Explora a evolução dos alunos ao longo do tempo:

- Progressão entre anos
- Evolução dos indicadores educacionais
- Mudanças na defasagem escolar
- Permanência e evasão no programa

---

## 3️⃣ Desempenho e Engajamento

Investiga a relação entre desempenho acadêmico e engajamento:

- Evolução dos indicadores **IEG, IDA e IPS**
- Comparação entre diferentes grupos de alunos
- Análise da relação entre indicadores e **IPV**

---

## 4️⃣ Modelo Preditivo

Desenvolve um modelo para estimar o **IPV** a partir dos indicadores educacionais.

O modelo analisa o impacto de fatores como:

- Engajamento (**IEG**)
- Desempenho acadêmico (**IDA**)
- Aspectos psicopedagógicos (**IPP**)

Os resultados são apresentados por meio de:

- coeficientes padronizados
- gráficos de importância dos fatores
- análise de impacto no IPV

---

# 🧠 Metodologia

O projeto segue as etapas clássicas de ciência de dados:

1. Exploração dos dados (EDA)
2. Limpeza e preparação dos dados
3. Análise longitudinal dos alunos
4. Visualização de padrões
5. Modelagem estatística e preditiva

Também foi realizada uma filtragem para acompanhar **os mesmos alunos ao longo dos anos**, permitindo análises de evolução individual.

---

# 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Statsmodels
- linearmodels

---

# 📂 Estrutura do Projeto
  datathon-passos-magicos
│
├── app.py
├── pages
│ ├── 1_Perfil_dos_alunos.py
│ ├── 2_Trajetoria.py
│ ├── 3_Desempenho_e_engajamento.py
│ └── 4_Modelo_preditivo.py
│
├── data
│ └── base_pede_limpa.csv
│
├── utils
│ ├── style.py
│ └── components.py
│
├── requirements.txt
└── README.md

---

# ▶️ Como Executar o Projeto

### 1️⃣ Clonar o repositório
git clone https://github.com/seu-usuario/datathonpassosmagicos.git

cd datathonpassosmagicos

---

### 2️⃣ Instalar dependências
pip install -r requirements.txt

---

### 3️⃣ Executar o aplicativo
streamlit run Home.py

O aplicativo abrirá automaticamente no navegador.

---

# 📊 Exemplos de Análises

O dashboard inclui visualizações como:

- Evolução dos indicadores ao longo do tempo
- Distribuição de defasagem escolar
- Relação entre indicadores educacionais
- Importância de fatores no IPV

Essas análises ajudam a identificar **quais dimensões têm maior impacto no desenvolvimento dos alunos**.

---

# 💡 Principais Insights

Entre os principais resultados encontrados:

- O **engajamento (IEG)** apresenta forte relação com o IPV
- Indicadores psicopedagógicos (**IPP**) também têm influência relevante
- A redução da **defasagem escolar** ao longo do tempo indica impacto positivo do programa
- A permanência no programa está associada a melhorias nos indicadores educacionais

---

# 👥 Equipe

Projeto desenvolvido para o **Datathon Passos Mágicos**.
