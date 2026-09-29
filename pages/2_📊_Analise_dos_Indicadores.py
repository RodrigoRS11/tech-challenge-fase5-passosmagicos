import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Análise dos Indicadores | Passos Mágicos",
    page_icon="📊",
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
        <h1>📊 Análise Detalhada dos Indicadores Socioeducacionais</h1>
        <h5>Associação Passos Mágicos - Diagnóstico das Dimensões</h5>
        <p>Explore as dimensões do programa (IDA, IEG, IPS, IPP e IAN) para compreender os fatores de desempenho, engajamento e desenvolvimento multidimensional dos estudantes.</p>
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
    st.error("❌ Base de dados não encontrada em 'Dados/df_limpo_passos_magicos.parquet'")
    st.stop()

df = carregar_dados()

# Identificar coluna de Pedras
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
# 5. ABAS DE NAVEGAÇÃO PARA AS PERGUNTAS DE 1 A 8
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "1. IAN (Adequação)",
    "2. IDA (Acadêmico)",
    "3. IEG (Engajamento)",
    "4. IAA (Autoavaliação)",
    "5. IPS (Psicossocial)",
    "6. IPP (Psicopedagógico)",
    "7. IPV (Ponto de Virada)",
    "8. Multidimensionalidade"
])

# ---------------------------------------------------------
# PERGUNTA 1: IAN (Adequação do Nível)
# ---------------------------------------------------------
with tab1:
    st.header("1. Adequação do Nível (IAN)")
    st.markdown("##### Perfil geral de defasagem e nivelamento dos alunos")
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_ian_hist = px.histogram(
            df_filtrado, x='IAN', nbins=10, 
            title="Distribuição das Notas de IAN",
            color_discrete_sequence=['#2ea043']
        )
        st.plotly_chart(fig_ian_hist, use_container_width=True)
    
    with col_b:
        df_ian_pedra = df_filtrado.groupby(col_pedra, observed=False)['IAN'].mean().reset_index()
        fig_ian_pedra = px.bar(
            df_ian_pedra, x=col_pedra, y='IAN', color=col_pedra,
            title="Média de IAN por Pedra", text_auto='.2f'
        )
        st.plotly_chart(fig_ian_pedra, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 2: IDA (Desempenho Acadêmico)
# ---------------------------------------------------------
with tab2:
    st.header("2. Desempenho Acadêmico (IDA)")
    st.markdown("##### Evolução das notas acadêmicas médias por ano e fase")
    
    df_ida_trend = df.groupby(['Ano_Exercicio', col_pedra], observed=False)['IDA'].mean().reset_index()
    fig_ida_trend = px.line(
        df_ida_trend, x='Ano_Exercicio', y='IDA', color=col_pedra, markers=True,
        title="Tendência Histórica do IDA por Pedra (Todos os Anos)"
    )
    st.plotly_chart(fig_ida_trend, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 3: IEG (Engajamento)
# ---------------------------------------------------------
with tab3:
    st.header("3. Engajamento nas Atividades (IEG)")
    st.markdown("##### Relação entre o engajamento (IEG) com o desempenho acadêmico (IDA) e IPV")
    
    col_c, col_d = st.columns(2)
    with col_c:
        fig_scat1 = px.scatter(
            df_filtrado, x='IEG', y='IDA', color=col_pedra,
            title="Correlação: IEG (Engajamento) vs IDA (Desempenho)"
        )
        st.plotly_chart(fig_scat1, use_container_width=True)
        
    with col_d:
        if 'IPV' in df_filtrado.columns:
            fig_scat2 = px.scatter(
                df_filtrado, x='IEG', y='IPV', color=col_pedra,
                title="Correlação: IEG (Engajamento) vs IPV (Ponto de Virada)"
            )
            st.plotly_chart(fig_scat2, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 4: IAA (Autoavaliação)
# ---------------------------------------------------------
with tab4:
    st.header("4. Autoavaliação do Aluno (IAA)")
    st.markdown("##### Comparação entre percepção própria (IAA) e desempenho real (IDA)")
    
    if 'IAA' in df_filtrado.columns and 'IDA' in df_filtrado.columns:
        df_filtrado['Vies_Autoavaliacao'] = df_filtrado['IAA'] - df_filtrado['IDA']
        
        fig_iaa = px.scatter(
            df_filtrado, x='IDA', y='IAA', color='Vies_Autoavaliacao',
            color_continuous_scale='Spectral',
            title="Dispersão: Desempenho Real (IDA) vs Autoavaliação (IAA)",
            labels={'Vies_Autoavaliacao': 'Diferença (IAA - IDA)'}
        )
        st.plotly_chart(fig_iaa, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 5: IPS (Aspectos Psicossociais)
# ---------------------------------------------------------
with tab5:
    st.header("5. Aspectos Psicossociais (IPS)")
    st.markdown("##### Identificação de padrões psicossociais que impactam o desempenho")
    
    if 'IPS' in df_filtrado.columns:
        fig_ips = px.box(
            df_filtrado, x=col_pedra, y='IPS', color=col_pedra,
            title="Distribuição do IPS (Suporte Psicossocial) por Pedra"
        )
        st.plotly_chart(fig_ips, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 6: IPP (Aspectos Psicopedagógicos)
# ---------------------------------------------------------
with tab6:
    st.header("6. Aspectos Psicopedagógicos (IPP)")
    st.markdown("##### Comparativo entre avaliação psicopedagógica (IPP) e nível de adequação (IAN)")
    
    if 'IPP' in df_filtrado.columns and 'IAN' in df_filtrado.columns:
        fig_ipp_ian = px.density_heatmap(
            df_filtrado, x='IAN', y='IPP', text_auto=True,
            title="Matriz de Densidade: IPP vs IAN",
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_ipp_ian, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 7: IPV (Ponto de Virada)
# ---------------------------------------------------------
with tab7:
    st.header("7. Ponto de Virada (IPV)")
    st.markdown("##### Fatores que mais influenciam o alcance do Ponto de Virada")
    
    if 'IPV' in df_filtrado.columns:
        cols_corr = [c for c in ['IDA', 'IEG', 'IPS', 'IPP', 'IAA', 'IAN', 'IPV'] if c in df_filtrado.columns]
        corr = df_filtrado[cols_corr].corr()[['IPV']].sort_values(by='IPV', ascending=False)
        
        fig_corr = px.bar(
            corr.reset_index(), x='index', y='IPV', color='IPV',
            title="Correlação dos Indicadores com o IPV",
            labels={'index': 'Indicador', 'IPV': 'Correlação com IPV'}
        )
        st.plotly_chart(fig_corr, use_container_width=True)

# ---------------------------------------------------------
# PERGUNTA 8: Multidimensionalidade (Composição do INDE)
# ---------------------------------------------------------
with tab8:
    st.header("8. Multidimensionalidade dos Indicadores")
    st.markdown("##### Combinação dos pilares (IDA + IEG + IPS + IPP) para a nota global (INDE)")
    
    cols_pilares = [c for c in ['IDA', 'IEG', 'IPS', 'IPP', 'INDE'] if c in df_filtrado.columns]
    
    dimensions = [
        dict(range=[df_filtrado[col].min(), df_filtrado[col].max()],
             label=col, values=df_filtrado[col])
        for col in cols_pilares
    ]
    
    fig_parallel = px.parallel_coordinates(
        df_filtrado[cols_pilares].dropna(),
        dimensions=cols_pilares,
        color='INDE',
        color_continuous_scale=px.colors.diverging.Tealrose,
        labels={
            'IDA': 'Desempenho (IDA)',
            'IEG': 'Engajamento (IEG)',
            'IPS': 'Psicossocial (IPS)',
            'IPP': 'Psicopedagógico (IPP)',
            'INDE': 'Nota Final (INDE)'
        },
        title="Coordenadas Paralelas dos Pilares com o INDE Final"
    )
    
    fig_parallel.update_layout(margin=dict(t=80, b=30, l=50, r=50))
    
    st.plotly_chart(fig_parallel, use_container_width=True)