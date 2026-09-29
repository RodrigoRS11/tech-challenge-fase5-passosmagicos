import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Efetividade e Jornada | Passos Mágicos",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <style>
    /* Cor de fundo da área principal - Vermelho Pastel Suave */
    .stApp {
        background-color: #E6A5A5 !important;
        color: #1E1E1E !important;
    }

    /* Cor de fundo da Barra Lateral - Azul Marinho */
    [data-testid="stSidebar"] {
        background-color: #0A192F !important;
    }

    /* Textos da barra lateral */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Estilo para o Container/Cartão Azul Marinho do Cabeçalho */
    .header-box {
        background-color: #0A192F;
        padding: 24px;
        border-radius: 12px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .header-box h1 {
        color: #FFFFFF !important;
        margin-bottom: 8px;
        font-size: 2.2rem;
    }

    .header-box h5 {
        color: #CBD5E1 !important;
        margin-bottom: 12px;
        font-weight: 400;
    }

    .header-box p {
        color: #F1F5F9 !important;
        margin-bottom: 0;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CABEÇALHO DESTACADO EM AZUL MARINHO
# ---------------------------------------------------------
st.markdown("""
    <div class="header-box">
        <h1>📈 Avaliação de Efetividade e Jornada do Aluno</h1>
        <h5>Associação Passos Mágicos - Impacto Transversal e Longitudinal</h5>
        <p>Acompanhe a evolução longitudinal dos alunos ao longo das pedras (<b>Quartzo ➔ Ágata ➔ Ametista ➔ Topázio</b>), identificando o impacto da transformação socioeducacional e comprovando a efetividade do programa.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# 3. CARREGAMENTO DOS DADOS
# ---------------------------------------------------------
@st.cache_data
def carregar_dados():
    caminho_parquet = os.path.join("Dados", "df_limpo_passos_magicos.parquet")
    if os.path.exists(caminho_parquet):
        return pd.read_parquet(caminho_parquet)
    st.error("❌ Base de dados não encontrada.")
    st.stop()

df = carregar_dados()
col_pedra = [c for c in df.columns if 'pedra' in c.lower()][0]

# ---------------------------------------------------------
# 4. BARRA LATERAL (LOGO E FILTROS GLOBAIS)
# ---------------------------------------------------------
st.sidebar.image(
    "https://passosmagicos.org.br/wp-content/uploads/2020/10/Passos-magicos-icon-cor.png", 
    width=180
)

st.sidebar.title("Filtros Globais")

# Filtro de Ano
anos_disponiveis = sorted(df['Ano_Exercicio'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano de Exercício:",
    options=anos_disponiveis,
    default=anos_disponiveis
)

# Filtro de Pedras
pedras_ordem = ['Quartzo', 'Ágata', 'Ametista', 'Topázio']
pedras_existentes = [p for p in pedras_ordem if p in df[col_pedra].dropna().unique()]

pedras_selecionadas = st.sidebar.multiselect(
    "Classificação de Pedra:",
    options=pedras_existentes,
    default=pedras_existentes
)

# Aplicação dos Filtros no DataFrame
df_filtrado = df[
    (df['Ano_Exercicio'].isin(anos_selecionados)) &
    (df[col_pedra].isin(pedras_selecionadas))
].copy()

# ---------------------------------------------------------
# 5. EVOLUÇÃO DAS PEDRAS (JORNADA DO ALUNO)
# ---------------------------------------------------------
st.subheader("📈 Efetividade do Programa e Impacto de Longo Prazo")

df_jornada = df_filtrado.groupby(col_pedra, observed=False)[['INDE', 'IDA', 'IEG', 'IAN', 'IPS', 'IPP']].mean()
df_jornada = df_jornada.reindex([p for p in pedras_ordem if p in df_jornada.index]).reset_index()

fig_jornada = px.line(
    df_jornada,
    x=col_pedra,
    y=['INDE', 'IDA', 'IEG', 'IAN'],
    markers=True,
    title="Jornada de Evolução das Médias por Pedra (Quartzo a Topázio)",
    labels={'value': 'Média das Notas', 'variable': 'Indicador', col_pedra: 'Classificação da Pedra'},
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig_jornada, use_container_width=True)

st.success("✅ **Conclusão de Efetividade:** Observa-se uma progressão consistente nas notas médias do INDE e do engajamento conforme os alunos avançam na classificação de pedras, demonstrando a maturidade e efetividade do acompanhamento educacional.")