import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import os

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Previsão de Risco Futuro | Passos Mágicos",
    page_icon="🔮",
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

# Cabeçalho Destacado em Azul Marinho
st.markdown("""
    <div class="header-box">
        <h1>🔮 Modelo Preditivo de Risco de Defasagem (Ciclo t+1)</h1>
        <h5>Associação Passos Mágicos - Monitoramento Preditivo</h5>
        <p>Esta página utiliza o modelo de Machine Learning <b>Gradient Boosting</b> para <b>antecipar a probabilidade de risco futuro</b> do estudante no ciclo seguinte (t+1), prevenindo a queda no desempenho (IDA &lt; 6.0) ou defasagem (IAN &lt; 7.0).</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# 2. CARREGAMENTO DOS ARTEFATOS (DADOS E MODELO)
# ---------------------------------------------------------
@st.cache_data
def carregar_dados():
    caminho_parquet = os.path.join("Dados", "df_limpo_passos_magicos.parquet")
    if os.path.exists(caminho_parquet):
        return pd.read_parquet(caminho_parquet)
    st.error(f"❌ Base de dados não encontrada em '{caminho_parquet}'")
    st.stop()

@st.cache_resource
def carregar_modelo():
    caminho_modelo = os.path.join("Modelo", "modelo_risco_passos_magicos.pkl")
    if os.path.exists(caminho_modelo):
        artefatos = joblib.load(caminho_modelo)
        return artefatos['modelo'], artefatos.get('scaler', None), artefatos['features']
    else:
        st.error(f"❌ Modelo não encontrado em '{caminho_modelo}'")
        st.stop()

df_limpo = carregar_dados()
modelo, scaler, features_puras = carregar_modelo()

# ---------------------------------------------------------
# 3. BARRA LATERAL (LOGO E FILTROS GLOBAIS)
# ---------------------------------------------------------
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
df_calc = df_limpo[
    (df_limpo['Ano_Exercicio'].isin(anos_selecionados)) &
    (df_limpo[col_pedra].isin(pedras_selecionadas))
].sort_values(['RA', 'Ano_Exercicio']).copy()

# ---------------------------------------------------------
# 4. PREPARAÇÃO E PREDIÇÃO NA BASE COMPLETA
# ---------------------------------------------------------
# Garantir Deltas
if 'Delta_IDA' not in df_calc.columns:
    df_calc['Delta_IDA'] = df_calc.groupby('RA')['IDA'].diff().fillna(0)
if 'Delta_IEG' not in df_calc.columns:
    df_calc['Delta_IEG'] = df_calc.groupby('RA')['IEG'].diff().fillna(0)
if 'Delta_IPS' not in df_calc.columns:
    df_calc['Delta_IPS'] = df_calc.groupby('RA')['IPS'].diff().fillna(0)

# Vício de Autoavaliação
if 'Vies_Autoavaliacao' not in df_calc.columns and 'IAA' in df_calc.columns and 'IDA' in df_calc.columns:
    df_calc['Vies_Autoavaliacao'] = df_calc['IAA'] - df_calc['IDA']

# Mapeamento de Fase
mapeamento_fase = {
    'Alfa': 0, 'Fase 1': 1, 'Fase 2': 2, 'Fase 3': 3, 
    'Fase 4': 4, 'Fase 5': 5, 'Fase 6': 6, 'Fase 7': 7, 'Fase 8': 8
}
if 'Fase_Num' not in df_calc.columns:
    if 'Fase_Clean' in df_calc.columns:
        df_calc['Fase_Num'] = df_calc['Fase_Clean'].map(mapeamento_fase).fillna(0)
    elif 'Fase' in df_calc.columns:
        df_calc['Fase_Num'] = df_calc['Fase'].map(mapeamento_fase).fillna(0)
    else:
        df_calc['Fase_Num'] = 0

# Garantir que todas as features existem no DF
for feat in features_puras:
    if feat not in df_calc.columns:
        df_calc[feat] = 0.0

# Previsão das Probabilidades
X_full = df_calc[features_puras].fillna(0)
df_calc['Probabilidade_Risco_%'] = (modelo.predict_proba(X_full)[:, 1] * 100).round(1)

def classificar_nivel(prob):
    if prob >= 60.0:
        return '🚨 Alto Risco (Prioritário)'
    elif prob >= 30.0:
        return '⚠️ Médio Risco (Atenção)'
    else:
        return '✅ Baixo Risco (Estável)'

df_calc['Nivel_Prioridade'] = df_calc['Probabilidade_Risco_%'].apply(classificar_nivel)

# ---------------------------------------------------------
# 5. METRICAS DE RISCO
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

    /* Rótulo (Label) e Valor da métrica em branco */
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

st.subheader("📊 Panorama do Risco Futuro")

c1, c2, c3, c4 = st.columns(4)

total = len(df_calc)
alto = len(df_calc[df_calc['Probabilidade_Risco_%'] >= 60])
medio = len(df_calc[(df_calc['Probabilidade_Risco_%'] >= 30) & (df_calc['Probabilidade_Risco_%'] < 60)])
baixo = len(df_calc[df_calc['Probabilidade_Risco_%'] < 30])

c1.metric("Alunos Avaliados", f"{total:,}".replace(",", "."))
c2.metric("🚨 Alto Risco (>60%)", f"{alto} ({(alto/total*100) if total>0 else 0:.1f}%)")
c3.metric("⚠️ Médio Risco (30-60%)", f"{medio} ({(medio/total*100) if total>0 else 0:.1f}%)")
c4.metric("✅ Baixo Risco (<30%)", f"{baixo} ({(baixo/total*100) if total>0 else 0:.1f}%)")

st.divider()

# ---------------------------------------------------------
# 6. GRÁFICOS VISUAIS
# ---------------------------------------------------------
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("##### Distribuição das Faixas de Risco")
    if total > 0:
        fig_pie = px.pie(
            df_calc, 
            names='Nivel_Prioridade', 
            color='Nivel_Prioridade',
            color_discrete_map={
                '🚨 Alto Risco (Prioritário)': '#e74c3c',
                '⚠️ Médio Risco (Atenção)': '#f39c12',
                '✅ Baixo Risco (Estável)': '#2ecc71'
            },
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col_g2:
    st.markdown("##### Relação: Engajamento (IEG) x Risco Futuro")
    if total > 0:
        fig_scatter = px.scatter(
            df_calc,
            x='IEG',
            y='Probabilidade_Risco_%',
            color='Nivel_Prioridade',
            size='IDA',
            hover_data=['RA', col_pedra, 'IDA'],
            labels={'IEG': 'Nota IEG (Engajamento)', 'Probabilidade_Risco_%': 'Probabilidade de Risco (%)'},
            color_discrete_map={
                '🚨 Alto Risco (Prioritário)': '#e74c3c',
                '⚠️ Médio Risco (Atenção)': '#f39c12',
                '✅ Baixo Risco (Estável)': '#2ecc71'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# 7. TABELA DE PRIORIDADE
# ---------------------------------------------------------
st.subheader("🚨 Lista de Alunos Prioritários para Intervenção Psicopedagógica")

cols_tab = [c for c in ['RA', 'Nome', col_pedra, 'IDA', 'IEG', 'IAN', 'IPP', 'Probabilidade_Risco_%', 'Nivel_Prioridade'] if c in df_calc.columns]
df_prioridade = df_calc[cols_tab].sort_values(by='Probabilidade_Risco_%', ascending=False)

st.dataframe(
    df_prioridade,
    column_config={
        "Probabilidade_Risco_%": st.column_config.ProgressColumn(
            "Risco Futuro (%)",
            help="Probabilidade calculada pelo modelo de Machine Learning",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    use_container_width=True
)

# ---------------------------------------------------------
# 8. SIMULADOR EM TEMPO REAL (COM FORMULÁRIO E BOTÃO)
# ---------------------------------------------------------
st.divider()
st.subheader("🎛️ Simulador Preditivo de Aluno (Cenários 'What-If')")
st.caption("Ajuste os indicadores e clique no botão para calcular o risco do aluno:")

with st.form("form_simulador_risco"):
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        s_ida = st.number_input("IDA (Desempenho)", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
        s_ieg = st.number_input("IEG (Engajamento)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

    with col_s2:
        s_ips = st.number_input("IPS (Psicossocial)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        s_ipp = st.number_input("IPP (Psicopedagógico)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

    with col_s3:
        s_iaa = st.number_input("IAA (Autoavaliação)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        s_ian = st.number_input("IAN (Adequação Nível)", min_value=0.0, max_value=10.0, value=10.0, step=0.5)

    with col_s4:
        s_delta_ieg = st.number_input("Variação IEG (Delta_IEG)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)
        s_delta_ida = st.number_input("Variação IDA (Delta_IDA)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)
        s_fase = st.selectbox("Fase", options=[0, 1, 2, 3, 4, 5, 6, 7, 8], index=0)

    btn_calcular = st.form_submit_button("🔮 Calcular Previsão de Risco", use_container_width=True)

if btn_calcular:
    vies_auto = s_iaa - s_ida

    dados_simulacao = pd.DataFrame([{
        'IDA': s_ida,
        'IEG': s_ieg,
        'IPS': s_ips,
        'IPP': s_ipp,
        'IAA': s_iaa,
        'IAN': s_ian,
        'Delta_IDA': s_delta_ida,
        'Delta_IEG': s_delta_ieg,
        'Delta_IPS': 0.0,
        'Vies_Autoavaliacao': vies_auto,
        'Fase_Num': s_fase
    }])[features_puras]

    proba_simulada = modelo.predict_proba(dados_simulacao)[:, 1][0] * 100

    st.markdown("#### Resultado da Simulação:")
    if proba_simulada >= 60.0:
        st.error(f"🚨 **Probabilidade de Risco Futuro: {proba_simulada:.1f}%** - ALTO RISCO: Recomenda-se acompanhamento psicopedagógico (IPP).")
    elif proba_simulada >= 30.0:
        st.warning(f"⚠️ **Probabilidade de Risco Futuro: {proba_simulada:.1f}%** - MÉDIO RISCO: Monitorar assiduidade e engajamento (IEG).")
    else:
        st.success(f"✅ **Probabilidade de Risco Futuro: {proba_simulada:.1f}%** - BAIXO RISCO: Aluno em trajetória saudável no programa.")