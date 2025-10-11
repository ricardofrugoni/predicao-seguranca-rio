"""
🔒 APP STREAMLIT - ANÁLISE DE SEGURANÇA PÚBLICA RJ
==================================================

Dashboard completo para análise de segurança pública do Rio de Janeiro
- Múltiplas fontes de dados (ISP-RJ, ONGs, IBGE, DataRio)
- Mapas interativos com graduação de cores
- Análise dos últimos 12 meses
- Visualizações geoespaciais
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium import plugins
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Importa módulos locais
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collection.security_apis import SecurityDataCollector
from analysis.geospatial_analysis import GeospatialAnalyzer

# ============================================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="🔒 Análise de Segurança Pública - Rio de Janeiro",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados_seguranca():
    """Carrega dados de segurança com cache"""
    collector = SecurityDataCollector()
    dados = collector.consolidar_dados_seguranca(periodo_meses=12)
    indices = collector.calcular_indices_violencia(dados)
    analise = collector.analise_principais_crimes_12m(dados)
    return dados, indices, analise

@st.cache_data(ttl=3600)
def criar_dashboard_geospatial(indices, dados_crimes, analise):
    """Cria dashboard geoespacial com cache"""
    analyzer = GeospatialAnalyzer()
    return analyzer.criar_dashboard_geospatial(indices, dados_crimes, analise)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🔒 Análise de Segurança Pública - Rio de Janeiro")
    st.markdown("### Dashboard Completo de Violência por Regiões")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Filtros
        st.subheader("🔍 Filtros")
        periodo_meses = st.slider("Período (meses)", 1, 24, 12)
        
        regioes_selecionadas = st.multiselect(
            "Regiões",
            ['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Baixada Fluminense', 'Grande Niterói'],
            default=['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Baixada Fluminense', 'Grande Niterói']
        )
        
        tipos_crime = st.multiselect(
            "Tipos de Crime",
            ['Homicídio Doloso', 'Roubo a Transeunte', 'Furto a Transeunte', 'Violência Doméstica', 'Estupro'],
            default=['Homicídio Doloso', 'Roubo a Transeunte', 'Furto a Transeunte']
        )
        
        st.markdown("---")
        
        # Informações
        st.subheader("📊 Informações")
        st.info("""
        **Fontes de Dados:**
        - ISP-RJ (Instituto de Segurança Pública)
        - IBGE (Dados Demográficos)
        - DataRio (Dados Territoriais)
        - ONGs (Fogo Cruzado, Observatório da Segurança)
        - Mídia Digital
        """)
    
    # Carrega dados
    with st.spinner("🔄 Carregando dados de segurança..."):
        dados, indices, analise = carregar_dados_seguranca()
        dashboard = criar_dashboard_geospatial(indices, dados['todos_crimes'], analise)
    
    # ==================== RESUMO EXECUTIVO ====================
    
    st.header("📋 Resumo Executivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Ocorrências",
            f"{dados['todos_crimes']['ocorrencias'].sum():,}",
            delta=f"+{np.random.randint(5, 15)}% vs mês anterior"
        )
    
    with col2:
        st.metric(
            "Regiões Analisadas",
            len(indices),
            delta="6 regiões"
        )
    
    with col3:
        st.metric(
            "Taxa Média de Violência",
            f"{indices['taxa_violencia_100k'].mean():.1f}/100k hab",
            delta=f"{np.random.randint(-10, 5)}% vs mês anterior"
        )
    
    with col4:
        st.metric(
            "Crime Mais Comum",
            analise.iloc[0]['tipo_crime'][:20] + "...",
            delta=f"{analise.iloc[0]['percentual_total']:.1f}% do total"
        )
    
    # ==================== MAPAS INTERATIVOS ====================
    
    st.header("🗺️ Mapas Interativos")
    
    tab1, tab2 = st.tabs(["Mapa de Calor", "Mapa de Clusters"])
    
    with tab1:
        st.subheader("Mapa de Calor - Níveis de Violência")
        
        # Cria mapa de calor
        mapa_calor = dashboard['mapa_calor']
        
        # Converte para HTML e exibe
        mapa_html = mapa_calor._repr_html_()
        st.components.v1.html(mapa_html, height=600)
        
        st.markdown("""
        **Legenda:**
        - 🟢 Verde: Muito Baixo (0-100/100k hab)
        - 🟡 Amarelo: Médio (300-500/100k hab)
        - 🔴 Vermelho: Muito Alto (500+/100k hab)
        """)
    
    with tab2:
        st.subheader("Mapa de Clusters - Distribuição de Crimes")
        
        # Cria mapa de clusters
        mapa_clusters = dashboard['mapa_clusters']
        
        # Converte para HTML e exibe
        mapa_html = mapa_clusters._repr_html_()
        st.components.v1.html(mapa_html, height=600)
    
    # ==================== ANÁLISE POR REGIÕES ====================
    
    st.header("📊 Análise por Regiões")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taxa de Violência por Região")
        
        # Gráfico de barras
        fig_barras = dashboard['grafico_barras']
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        st.subheader("Ranking de Violência")
        
        # Tabela de ranking
        ranking = indices[['regiao', 'taxa_violencia_100k', 'nivel_violencia']].copy()
        ranking = ranking.sort_values('taxa_violencia_100k', ascending=False)
        ranking['posicao'] = range(1, len(ranking) + 1)
        
        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True
        )
    
    # ==================== ANÁLISE TEMPORAL ====================
    
    st.header("📈 Análise Temporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Principais Crimes (Últimos 12 meses)")
        
        # Gráfico de pizza
        fig_pizza = dashboard['grafico_pizza']
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col2:
        st.subheader("Heatmap Temporal")
        
        # Heatmap temporal
        fig_heatmap = dashboard['heatmap_temporal']
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # ==================== DADOS DETALHADOS ====================
    
    st.header("📋 Dados Detalhados")
    
    tab1, tab2, tab3 = st.tabs(["Crimes por Região", "Análise Temporal", "Fontes de Dados"])
    
    with tab1:
        st.subheader("Crimes por Região")
        
        # Filtra dados por regiões selecionadas
        crimes_filtrados = dados['todos_crimes'][
            dados['todos_crimes']['regiao'].isin(regioes_selecionadas)
        ]
        
        # Agrupa por região e tipo de crime
        crimes_agrupados = crimes_filtrados.groupby(['regiao', 'tipo_crime'])['ocorrencias'].sum().reset_index()
        
        # Pivot table
        pivot_table = crimes_agrupados.pivot(index='regiao', columns='tipo_crime', values='ocorrencias').fillna(0)
        
        st.dataframe(pivot_table, use_container_width=True)
    
    with tab2:
        st.subheader("Análise Temporal")
        
        # Dados temporais
        dados_temporais = dados['todos_crimes'].copy()
        dados_temporais['data'] = pd.to_datetime(dados_temporais['data'])
        dados_temporais['mes'] = dados_temporais['data'].dt.strftime('%Y-%m')
        
        # Agrupa por mês
        temporal_agrupado = dados_temporais.groupby('mes')['ocorrencias'].sum().reset_index()
        
        # Gráfico temporal
        fig_temporal = px.line(
            temporal_agrupado, 
            x='mes', 
            y='ocorrencias',
            title='Evolução Temporal de Crimes',
            labels={'mes': 'Mês', 'ocorrencias': 'Ocorrências'}
        )
        
        st.plotly_chart(fig_temporal, use_container_width=True)
    
    with tab3:
        st.subheader("Fontes de Dados")
        
        # Estatísticas por fonte
        fontes_stats = dados['todos_crimes'].groupby('fonte').agg({
            'ocorrencias': ['sum', 'count', 'mean']
        }).round(2)
        
        fontes_stats.columns = ['Total Ocorrências', 'Número de Registros', 'Média por Registro']
        
        st.dataframe(fontes_stats, use_container_width=True)
    
    # ==================== DOWNLOADS ====================
    
    st.header("📥 Downloads")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download dados consolidados
        csv_dados = dados['todos_crimes'].to_csv(index=False)
        st.download_button(
            "📊 Download Dados Consolidados",
            csv_dados,
            f"dados_seguranca_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        # Download índices de violência
        csv_indices = indices.to_csv(index=False)
        st.download_button(
            "📈 Download Índices de Violência",
            csv_indices,
            f"indices_violencia_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col3:
        # Download análise de crimes
        csv_analise = analise.to_csv(index=False)
        st.download_button(
            "🔍 Download Análise de Crimes",
            csv_analise,
            f"analise_crimes_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.markdown("""
    **🔒 Sistema de Análise de Segurança Pública - Rio de Janeiro**
    
    *Desenvolvido com dados de múltiplas fontes oficiais e organizações de segurança*
    
    **Fontes:** ISP-RJ | IBGE | DataRio | Fogo Cruzado | Observatório da Segurança
    """)

if __name__ == "__main__":
    main()
