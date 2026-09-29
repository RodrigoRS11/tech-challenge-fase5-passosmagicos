import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ---------------------------------------------------------
import streamlit as st

# 1. Configuração da página
st.set_page_config(
    page_title="Dashboard | Passos Mágicos",
    page_icon="🏠",
    layout="wide"
)

# 2. Estilização CSS Personalizada
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
        margin-bottom: 25px;
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

# 3. Cabeçalho Destacado em Azul Marinho
st.markdown("""
    <div class="header-box">
        <h1>🪄 Associação Passos Mágicos</h1>
        <h5>Dashboard de Monitoramento de Impacto Educacional e Análise Preditiva</h5>
        <p>Esta plataforma centraliza os indicadores socioeducacionais dos alunos atendidos pela <b>Passos Mágicos</b>, permitindo o acompanhamento da jornada de aprendizado desde o acolhimento (Pedra Quartzo) até a autonomia (Pedra Topázio).</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# 2. CARREGAMENTO DOS DADOS COM CACHE
# ---------------------------------------------------------
@st.cache_data
def carregar_dados():
    # Caminho exato da sua pasta 'Dados'
    caminho_parquet = os.path.join("Dados", "df_limpo_passos_magicos.parquet")
    
    if os.path.exists(caminho_parquet):
        return pd.read_parquet(caminho_parquet)
    elif os.path.exists("df_limpo_passos_magicos.parquet"):
        return pd.read_parquet("df_limpo_passos_magicos.parquet")
    else:
        st.error(f"❌ Arquivo Parquet não encontrado em: {os.path.abspath(caminho_parquet)}")
        st.stop()

df_limpo = carregar_dados()

# ---------------------------------------------------------
# 3. BARRA LATERAL - FILTROS DINÂMICOS
# ---------------------------------------------------------
# Na barra lateral (Sidebar)
st.sidebar.image(
    "https://passosmagicos.org.br/wp-content/uploads/2020/10/Passos-magicos-icon-cor.png", 
    width=180
)

st.sidebar.title("Filtros Globais")

# Identificar coluna de Pedras
col_pedra = [c for c in df_limpo.columns if 'pedra' in c.lower()][0]

# Filtro de Ano
anos_disponiveis = sorted(df_limpo['Ano_Exercicio'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano de Exercício:",
    options=anos_disponiveis,
    default=anos_disponiveis
)

# Filtro de Pedras
pedras_ordem = ['Quartzo', 'Ágata', 'Ametista', 'Topázio']
pedras_existentes = [p for p in pedras_ordem if p in df_limpo[col_pedra].dropna().unique()]

pedras_selecionadas = st.sidebar.multiselect(
    "Classificação de Pedra:",
    options=pedras_existentes,
    default=pedras_existentes
)

# Aplicação dos Filtros no DataFrame
df_filtrado = df_limpo[
    (df_limpo['Ano_Exercicio'].isin(anos_selecionados)) &
    (df_limpo[col_pedra].isin(pedras_selecionadas))
].copy()

# ---------------------------------------------------------
# 4. CABEÇALHO DA PÁGINA INICIAL
# ---------------------------------------------------------

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste a barra lateral.")
    st.stop()

# ---------------------------------------------------------
# 5. CARTÕES DE KPIS EXECUTIVOS
# ---------------------------------------------------------
# Estilização CSS para os cartões de Métricas (Azul Marinho com Cantos Arredondados)
st.markdown("""
    <style>
    /* Cartão do st.metric */
    [data-testid="stMetric"] {
        background-color: #0A192F !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }

    /* Rótulo (Label) e Valor da métrica em branco/claro */
    [data-testid="stMetricLabel"] p, 
    [data-testid="stMetricValue"] div {
        color: #FFFFFF !important;
    }

    /* Garantir contraste completo nos elementos filhos */
    [data-testid="stMetric"] * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("📊 Indicadores Chave de Desempenho (KPIs)")

col1, col2, col3, col4, col5 = st.columns(5)

total_alunos = df_filtrado['RA'].nunique() if 'RA' in df_filtrado.columns else len(df_filtrado)
media_inde = df_filtrado['INDE'].mean() if 'INDE' in df_filtrado.columns else 0
media_ida = df_filtrado['IDA'].mean() if 'IDA' in df_filtrado.columns else 0
media_ieg = df_filtrado['IEG'].mean() if 'IEG' in df_filtrado.columns else 0
media_ian = df_filtrado['IAN'].mean() if 'IAN' in df_filtrado.columns else 0

col1.metric("Total de Alunos", f"{total_alunos:,}".replace(",", "."))
col2.metric("Média INDE (Geral)", f"{media_inde:.2f}")
col3.metric("Média IDA (Acadêmico)", f"{media_ida:.2f}")
col4.metric("Média IEG (Engajamento)", f"{media_ieg:.2f}")
col5.metric("Média IAN (Adequação)", f"{media_ian:.2f}")

st.divider()

# ---------------------------------------------------------
# Mapeamento de Cores Verdadeiras das Pedras
# ---------------------------------------------------------
cores_pedras = {
    'Quartzo': '#B0BEC5',   # Cinza Prata / Quartzo
    'Ágata': '#E67E22',     # Laranja / Ágata
    'Ametista': '#8E44AD', # Roxo / Ametista
    'Topázio': '#F1C40F'    # Dourado / Topázio
}

# ---------------------------------------------------------
# 6. GRÁFICOS DINÂMICOS - PANORAMA GERAL E JORNADA
# ---------------------------------------------------------
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("💎 Evolução Média por Pedra")
    cols_pilares = [c for c in ['INDE', 'IDA', 'IEG', 'IPP'] if c in df_filtrado.columns]
    
    df_pedra_grp = df_filtrado.groupby(col_pedra, observed=False)[cols_pilares].mean()
    df_pedra_grp = df_pedra_grp.reindex([p for p in pedras_ordem if p in df_pedra_grp.index]).dropna().reset_index()
    
    fig_line = px.line(
        df_pedra_grp, 
        x=col_pedra, 
        y=cols_pilares,
        markers=True,
        labels={'value': 'Nota Média', 'variable': 'Indicador', col_pedra: 'Pedra'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_line.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

with col_g2:
    st.subheader("📈 Tendência Histórica do INDE por Ano")
    df_ano_grp = df_filtrado.groupby(['Ano_Exercicio', col_pedra], observed=False)['INDE'].mean().reset_index()
    
    fig_bar = px.bar(
        df_ano_grp, 
        x='Ano_Exercicio', 
        y='INDE', 
        color=col_pedra,
        barmode='group',
        labels={'Ano_Exercicio': 'Ano', 'INDE': 'Média INDE', col_pedra: 'Pedra'},
        color_discrete_map=cores_pedras  # Aplica as cores reais das pedras
    )
    fig_bar.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# 7. DISTRIBUIÇÃO E VISUALIZAÇÃO DOS DADOS BRUTOS
# ---------------------------------------------------------
st.divider()
with st.expander("🔍 Visualizar Tabela de Dados Filtrados"):
    cols_mostrar = [c for c in ['RA', 'Nome', 'Ano_Exercicio', col_pedra, 'INDE', 'IDA', 'IEG', 'IAN', 'IPP', 'IPS'] if c in df_filtrado.columns]
    st.dataframe(df_filtrado[cols_mostrar], use_container_width=True)