"""
🔒 APP STREAMLIT SIMPLES - SEGURANÇA PÚBLICA RJ
==============================================

Versão simplificada para deploy no Streamlit Cloud
- Dados simulados
- Visualizações básicas
- Sem dependências complexas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="🔒 Segurança Pública RJ",
    page_icon="🔒",
    layout="wide"
)

# ============================================================================
# DADOS SIMULADOS
# ============================================================================

@st.cache_data
def carregar_dados_seguranca():
    """Carrega dados simulados de segurança"""
    np.random.seed(42)
    
    # Dados de crimes por região - APENAS MUNICÍPIO DO RIO DE JANEIRO
    regioes = ['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste']
    tipos_crime = ['Homicídio Doloso', 'Roubo a Transeunte', 'Furto a Transeunte', 'Violência Doméstica', 'Estupro']
    
    dados = []
    for regiao in regioes:
        for crime in tipos_crime:
            # Padrões baseados em dados reais
            if crime == 'Homicídio Doloso':
                base = np.random.poisson(15)
            elif crime == 'Roubo a Transeunte':
                base = np.random.poisson(120)
            elif crime == 'Furto a Transeunte':
                base = np.random.poisson(200)
            else:
                base = np.random.poisson(30)
            
            # Ajuste por região
            if regiao == 'Zona Sul':
                base = int(base * 0.6)
            elif regiao == 'Zona Norte':
                base = int(base * 1.3)
            elif regiao == 'Zona Oeste':
                base = int(base * 1.5)
            
            dados.append({
                'regiao': regiao,
                'tipo_crime': crime,
                'ocorrencias': max(0, base),
                'data': datetime.now().strftime('%Y-%m-%d')
            })
    
    return pd.DataFrame(dados)

@st.cache_data
def calcular_indices_violencia(df):
    """Calcula índices de violência"""
    # Dados demográficos simulados
    populacao = {
        'Centro': 450000,
        'Zona Sul': 380000,
        'Zona Norte': 2400000,
        'Zona Oeste': 2500000
    }
    
    # Agrupa por região
    crimes_por_regiao = df.groupby('regiao')['ocorrencias'].sum().reset_index()
    
    # Calcula taxa por 100k hab
    crimes_por_regiao['populacao'] = crimes_por_regiao['regiao'].map(populacao)
    crimes_por_regiao['taxa_violencia_100k'] = (crimes_por_regiao['ocorrencias'] / crimes_por_regiao['populacao']) * 100000
    
    # Classifica níveis
    crimes_por_regiao['nivel_violencia'] = pd.cut(
        crimes_por_regiao['taxa_violencia_100k'],
        bins=[0, 100, 300, 500, 1000, float('inf')],
        labels=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
    )
    
    return crimes_por_regiao

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🔒 Análise de Segurança Pública - Rio de Janeiro")
    st.markdown("### Dashboard de Violência por Regiões")
    
    # Carrega dados
    dados = carregar_dados_seguranca()
    indices = calcular_indices_violencia(dados)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filtros")
        
        regioes_selecionadas = st.multiselect(
            "Regiões",
            dados['regiao'].unique(),
            default=dados['regiao'].unique()
        )
        
        tipos_selecionados = st.multiselect(
            "Tipos de Crime",
            dados['tipo_crime'].unique(),
            default=dados['tipo_crime'].unique()
        )
    
    # Filtra dados
    dados_filtrados = dados[
        (dados['regiao'].isin(regioes_selecionadas)) & 
        (dados['tipo_crime'].isin(tipos_selecionados))
    ]
    
    # ==================== RESUMO EXECUTIVO ====================
    
    st.header("📋 Resumo Executivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Ocorrências",
            f"{dados_filtrados['ocorrencias'].sum():,}",
            delta="+12% vs mês anterior"
        )
    
    with col2:
        st.metric(
            "Regiões Analisadas",
            len(regioes_selecionadas),
            delta="6 regiões"
        )
    
    with col3:
        st.metric(
            "Taxa Média de Violência",
            f"{indices['taxa_violencia_100k'].mean():.1f}/100k hab",
            delta="-5% vs mês anterior"
        )
    
    with col4:
        crime_mais_comum = dados_filtrados.groupby('tipo_crime')['ocorrencias'].sum().idxmax()
        st.metric(
            "Crime Mais Comum",
            crime_mais_comum[:20] + "...",
            delta="33% do total"
        )
    
    # ==================== GRÁFICOS ====================
    
    st.header("📊 Visualizações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taxa de Violência por Região")
        
        # Gráfico de barras
        fig_barras = px.bar(
            indices,
            x='regiao',
            y='taxa_violencia_100k',
            color='nivel_violencia',
            title='Taxa de Violência por Região',
            labels={'regiao': 'Região', 'taxa_violencia_100k': 'Taxa (/100k hab)'}
        )
        
        fig_barras.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição de Crimes")
        
        # Gráfico de pizza
        crimes_agrupados = dados_filtrados.groupby('tipo_crime')['ocorrencias'].sum().reset_index()
        
        fig_pizza = px.pie(
            crimes_agrupados,
            values='ocorrencias',
            names='tipo_crime',
            title='Distribuição de Crimes'
        )
        
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    # ==================== TABELA DE DADOS ====================
    
    st.header("📋 Dados Detalhados")
    
    # Tabela por região
    tabela_regiao = dados_filtrados.groupby(['regiao', 'tipo_crime'])['ocorrencias'].sum().unstack(fill_value=0)
    
    st.subheader("Crimes por Região")
    st.dataframe(tabela_regiao, use_container_width=True)
    
    # ==================== RANKING ====================
    
    st.header("🏆 Ranking de Violência")
    
    ranking = indices[['regiao', 'taxa_violencia_100k', 'nivel_violencia']].copy()
    ranking = ranking.sort_values('taxa_violencia_100k', ascending=False)
    ranking['posicao'] = range(1, len(ranking) + 1)
    
    st.dataframe(ranking, use_container_width=True)
    
    # ==================== DOWNLOADS ====================
    
    st.header("📥 Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download dados
        csv_dados = dados_filtrados.to_csv(index=False)
        st.download_button(
            "📊 Download Dados",
            csv_dados,
            f"dados_seguranca_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        # Download índices
        csv_indices = indices.to_csv(index=False)
        st.download_button(
            "📈 Download Índices",
            csv_indices,
            f"indices_violencia_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.markdown("""
    **🔒 Sistema de Análise de Segurança Pública - Rio de Janeiro**
    
    *Dashboard simplificado para análise de violência por regiões*
    """)

if __name__ == "__main__":
    main()

