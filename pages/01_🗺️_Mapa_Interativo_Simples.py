"""
🗺️ MAPA INTERATIVO SIMPLES - SEGURANÇA PÚBLICA RJ
================================================

Versão simplificada sem folium - apenas plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="🗺️ Mapa Interativo - Segurança Pública RJ",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================================
# DADOS SIMULADOS
# ============================================================================

@st.cache_data
def carregar_dados_mapa():
    """Carrega dados para o mapa"""
    np.random.seed(42)
    
    # Coordenadas aproximadas das regiões do RJ
    regioes_coords = {
        'Centro': {'lat': -22.9068, 'lon': -43.1729, 'populacao': 450000},
        'Zona Sul': {'lat': -22.9711, 'lon': -43.1822, 'populacao': 380000},
        'Zona Norte': {'lat': -22.8944, 'lon': -43.2400, 'populacao': 1200000},
        'Zona Oeste': {'lat': -22.8847, 'lon': -43.3300, 'populacao': 850000},
        'Baixada Fluminense': {'lat': -22.7667, 'lon': -43.4000, 'populacao': 2100000},
        'Grande Niterói': {'lat': -22.8833, 'lon': -43.1000, 'populacao': 950000}
    }
    
    # Gera dados de violência
    dados = []
    for regiao, coords in regioes_coords.items():
        # Simula dados de violência
        if regiao == 'Zona Sul':
            base_violencia = np.random.poisson(50)
        elif regiao == 'Baixada Fluminense':
            base_violencia = np.random.poisson(150)
        else:
            base_violencia = np.random.poisson(80)
        
        taxa_violencia = (base_violencia / coords['populacao']) * 100000
        
        # Classifica nível
        if taxa_violencia < 100:
            nivel = 'Muito Baixo'
            cor = '#2E8B57'
        elif taxa_violencia < 300:
            nivel = 'Baixo'
            cor = '#32CD32'
        elif taxa_violencia < 500:
            nivel = 'Médio'
            cor = '#FFD700'
        elif taxa_violencia < 1000:
            nivel = 'Alto'
            cor = '#FF8C00'
        else:
            nivel = 'Muito Alto'
            cor = '#DC143C'
        
        dados.append({
            'regiao': regiao,
            'lat': coords['lat'],
            'lon': coords['lon'],
            'populacao': coords['populacao'],
            'ocorrencias': base_violencia,
            'taxa_violencia_100k': taxa_violencia,
            'nivel_violencia': nivel,
            'cor': cor
        })
    
    return pd.DataFrame(dados)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🗺️ Mapa Interativo - Segurança Pública RJ")
    st.markdown("### Análise Geoespacial de Violência por Regiões")
    
    # Carrega dados
    dados = carregar_dados_mapa()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filtros")
        
        # Filtro de regiões
        regioes_selecionadas = st.multiselect(
            "Regiões",
            dados['regiao'].unique(),
            default=dados['regiao'].unique()
        )
        
        # Filtro de nível de violência
        niveis_selecionados = st.multiselect(
            "Níveis de Violência",
            dados['nivel_violencia'].unique(),
            default=dados['nivel_violencia'].unique()
        )
        
        st.markdown("---")
        st.info("""
        **🗺️ Mapa Interativo:**
        - Dados simulados baseados em padrões reais
        - 6 regiões do Rio de Janeiro
        - Classificação por níveis de violência
        - Visualização com Plotly
        """)
    
    # Filtra dados
    dados_filtrados = dados[
        (dados['regiao'].isin(regioes_selecionadas)) & 
        (dados['nivel_violencia'].isin(niveis_selecionados))
    ]
    
    # ==================== MAPA INTERATIVO ====================
    
    st.header("🗺️ Mapa de Violência por Região")
    
    # Cria mapa com Plotly
    fig = px.scatter_mapbox(
        dados_filtrados,
        lat='lat',
        lon='lon',
        size='ocorrencias',
        color='nivel_violencia',
        hover_name='regiao',
        hover_data={
            'lat': False,
            'lon': False,
            'ocorrencias': True,
            'taxa_violencia_100k': ':.1f',
            'populacao': True
        },
        color_discrete_map={
            'Muito Baixo': '#2E8B57',
            'Baixo': '#32CD32',
            'Médio': '#FFD700',
            'Alto': '#FF8C00',
            'Muito Alto': '#DC143C'
        },
        title='Mapa de Violência por Região',
        mapbox_style='open-street-map',
        zoom=9,
        center={'lat': -22.9068, 'lon': -43.1729}
    )
    
    fig.update_layout(
        height=600,
        title_x=0.5
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ==================== ESTATÍSTICAS ====================
    
    st.header("📊 Estatísticas por Região")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taxa de Violência")
        
        # Gráfico de barras
        fig_barras = px.bar(
            dados_filtrados,
            x='regiao',
            y='taxa_violencia_100k',
            color='nivel_violencia',
            title='Taxa de Violência por Região',
            labels={'regiao': 'Região', 'taxa_violencia_100k': 'Taxa (/100k hab)'},
            color_discrete_map={
                'Muito Baixo': '#2E8B57',
                'Baixo': '#32CD32',
                'Médio': '#FFD700',
                'Alto': '#FF8C00',
                'Muito Alto': '#DC143C'
            }
        )
        
        fig_barras.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição por Nível")
        
        # Gráfico de pizza
        nivel_counts = dados_filtrados['nivel_violencia'].value_counts()
        
        fig_pizza = px.pie(
            values=nivel_counts.values,
            names=nivel_counts.index,
            title='Distribuição por Nível de Violência',
            color_discrete_map={
                'Muito Baixo': '#2E8B57',
                'Baixo': '#32CD32',
                'Médio': '#FFD700',
                'Alto': '#FF8C00',
                'Muito Alto': '#DC143C'
            }
        )
        
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    # ==================== TABELA DE DADOS ====================
    
    st.header("📋 Dados Detalhados")
    
    # Tabela com informações
    tabela = dados_filtrados[['regiao', 'ocorrencias', 'taxa_violencia_100k', 'nivel_violencia', 'populacao']].copy()
    tabela = tabela.sort_values('taxa_violencia_100k', ascending=False)
    tabela['posicao'] = range(1, len(tabela) + 1)
    
    st.dataframe(tabela, use_container_width=True)
    
    # ==================== DOWNLOADS ====================
    
    st.header("📥 Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download dados
        csv_dados = dados_filtrados.to_csv(index=False)
        st.download_button(
            "📊 Download Dados do Mapa",
            csv_dados,
            f"mapa_seguranca_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        # Download estatísticas
        csv_stats = tabela.to_csv(index=False)
        st.download_button(
            "📈 Download Estatísticas",
            csv_stats,
            f"estatisticas_mapa_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.markdown("""
    **🗺️ Mapa Interativo - Segurança Pública RJ**
    
    *Visualização geoespacial de violência por regiões do Rio de Janeiro*
    
    **📊 Dados:** Simulados baseados em padrões reais  
    **🗺️ Regiões:** 6 regiões administrativas  
    **🎨 Visualização:** Plotly Mapbox  
    **📅 Atualização:** Tempo real
    """)

if __name__ == "__main__":
    main()
