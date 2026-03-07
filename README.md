# Datathon — Passos Mágicos

Projeto desenvolvido para a última fase da Pós Tech Data Analytics com o objetivo de analisar a trajetória educacional de alunos participantes do programa da Associação Passos Mágicos e identificar fatores que influenciam a defasagem ao longo do tempo, além de responder a outras questões propostas.

A aplicação foi construída em Python e Streamlit e apresenta análises exploratórias, visualizações interativas e um modelo preditivo baseado em indicadores educacionais do programa.

---

# Sobre os Indicadores

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

# Estrutura da Aplicação

A aplicação está organizada em páginas no Streamlit, cada uma explorando uma dimensão da análise.

## Perfil dos Alunos e Defasagem

Analisa características demográficas e educacionais dos alunos:

- Distribuição por idade
- Distribuição por gênero
- Rede de ensino
- Evolução da defasagem escolar
- Relação entre fase escolar e defasagem

---

## Trajetória Educacional

Explora a evolução dos alunos ao longo do tempo:

- Progressão entre anos
- Evolução dos indicadores educacionais
- Mudanças na defasagem escolar
- Permanência e evasão no programa

---

## Desempenho e Engajamento

Investiga a relação entre desempenho acadêmico e engajamento:

- Evolução dos indicadores IEG, IDA e IPS
- Comparação entre diferentes grupos de alunos
- Análise da relação entre indicadores e IPV

---

## Modelo Preditivo

Desenvolve um modelo para estimar o IPV a partir dos indicadores educacionais.

O modelo analisa o impacto de fatores como:

- Engajamento (IEG)
- Desempenho acadêmico (IDA)
- Aspectos psicopedagógicos (IPP)

Os resultados são apresentados por meio de:

- coeficientes padronizados
- gráficos de importância dos fatores
- análise de impacto no IPV

---

# Metodologia

O projeto segue as etapas clássicas de ciência de dados:

1. Exploração dos dados (EDA)
2. Limpeza e preparação dos dados
3. Análise longitudinal dos alunos
4. Visualização de padrões
5. Modelagem estatística e preditiva

Também foi realizada uma filtragem para acompanhar os mesmos alunos ao longo dos anos, permitindo análises de evolução individual.

---

# Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Statsmodels
- linearmodels

---

# Estrutura do Projeto
  ```
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
```

---

# Como Executar o Projeto

### Clonar o repositório
git clone https://github.com/seu-usuario/datathonpassosmagicos.git

cd datathonpassosmagicos

---

### Instalar dependências
pip install -r requirements.txt

---

### Executar o aplicativo
streamlit run Home.py

O aplicativo abrirá automaticamente no navegador.

---

# Principais Insights

Entre os principais resultados encontrados:

- O engajamento (IEG apresenta forte relação com o IPV
- Indicadores psicopedagógicos (IPP) também têm influência relevante
- A redução da defasagem escolar ao longo do tempo indica impacto positivo do programa
- A permanência no programa está associada a melhorias nos indicadores educacionais

---
