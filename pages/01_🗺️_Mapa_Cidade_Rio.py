"""
🗺️ MAPA DA CIDADE DO RIO DE JANEIRO
===================================

Mapa único com limite municipal e regiões administrativas
Cores por nível de periculosidade
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
    page_title="🗺️ Mapa da Cidade do Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================================
# DADOS DAS REGIÕES ADMINISTRATIVAS DA CIDADE DO RIO
# ============================================================================

@st.cache_data
def carregar_dados_cidade_rio():
    """Carrega dados das regiões administrativas da cidade do Rio"""
    
    # Regiões Administrativas da Cidade do Rio de Janeiro (33 RAs)
    regioes_cidade_rio = {
        'Centro': {
            'lat': -22.9068, 'lon': -43.1729, 'populacao': 450000,
            'ocorrencias': 45, 'taxa_100k': 100, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Zona Sul': {
            'lat': -22.9711, 'lon': -43.1822, 'populacao': 380000,
            'ocorrencias': 25, 'taxa_100k': 66, 'nivel': 'Baixo', 'periculosidade': 2
        },
        'Zona Norte': {
            'lat': -22.8944, 'lon': -43.2400, 'populacao': 1200000,
            'ocorrencias': 180, 'taxa_100k': 150, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Zona Oeste': {
            'lat': -22.8847, 'lon': -43.3300, 'populacao': 850000,
            'ocorrencias': 255, 'taxa_100k': 300, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Barra da Tijuca': {
            'lat': -23.0065, 'lon': -43.3641, 'populacao': 320000,
            'ocorrencias': 40, 'taxa_100k': 125, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Recreio dos Bandeirantes': {
            'lat': -23.0236, 'lon': -43.4567, 'populacao': 180000,
            'ocorrencias': 20, 'taxa_100k': 111, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Jacarepaguá': {
            'lat': -22.9500, 'lon': -43.3500, 'populacao': 280000,
            'ocorrencias': 85, 'taxa_100k': 304, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Campo Grande': {
            'lat': -22.9000, 'lon': -43.5500, 'populacao': 320000,
            'ocorrencias': 160, 'taxa_100k': 500, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Santa Cruz': {
            'lat': -22.9167, 'lon': -43.6833, 'populacao': 250000,
            'ocorrencias': 125, 'taxa_100k': 500, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Guaratiba': {
            'lat': -23.0167, 'lon': -43.5667, 'populacao': 120000,
            'ocorrencias': 60, 'taxa_100k': 500, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Ilha do Governador': {
            'lat': -22.8167, 'lon': -43.1833, 'populacao': 180000,
            'ocorrencias': 45, 'taxa_100k': 250, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Tijuca': {
            'lat': -22.9167, 'lon': -43.2333, 'populacao': 220000,
            'ocorrencias': 55, 'taxa_100k': 250, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Vila Isabel': {
            'lat': -22.9167, 'lon': -43.2500, 'populacao': 150000,
            'ocorrencias': 40, 'taxa_100k': 267, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Méier': {
            'lat': -22.9000, 'lon': -43.2833, 'populacao': 200000,
            'ocorrencias': 50, 'taxa_100k': 250, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Madureira': {
            'lat': -22.8833, 'lon': -43.3333, 'populacao': 180000,
            'ocorrencias': 45, 'taxa_100k': 250, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Bangu': {
            'lat': -22.8833, 'lon': -43.4667, 'populacao': 250000,
            'ocorrencias': 100, 'taxa_100k': 400, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Realengo': {
            'lat': -22.8667, 'lon': -43.4500, 'populacao': 200000,
            'ocorrencias': 80, 'taxa_100k': 400, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Padre Miguel': {
            'lat': -22.8833, 'lon': -43.4000, 'populacao': 180000,
            'ocorrencias': 70, 'taxa_100k': 389, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Botafogo': {
            'lat': -22.9500, 'lon': -43.1833, 'populacao': 120000,
            'ocorrencias': 15, 'taxa_100k': 125, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Copacabana': {
            'lat': -22.9700, 'lon': -43.1833, 'populacao': 150000,
            'ocorrencias': 20, 'taxa_100k': 133, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Lagoa': {
            'lat': -22.9700, 'lon': -43.2000, 'populacao': 80000,
            'ocorrencias': 8, 'taxa_100k': 100, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Santa Teresa': {
            'lat': -22.9167, 'lon': -43.1833, 'populacao': 60000,
            'ocorrencias': 12, 'taxa_100k': 200, 'nivel': 'Médio', 'periculosidade': 3
        },
        'Irajá': {
            'lat': -22.8167, 'lon': -43.2500, 'populacao': 180000,
            'ocorrencias': 50, 'taxa_100k': 278, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Penha': {
            'lat': -22.8167, 'lon': -43.3000, 'populacao': 160000,
            'ocorrencias': 45, 'taxa_100k': 281, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Pavuna': {
            'lat': -22.8167, 'lon': -43.3500, 'populacao': 140000,
            'ocorrencias': 40, 'taxa_100k': 286, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Ramos': {
            'lat': -22.8500, 'lon': -43.1833, 'populacao': 100000,
            'ocorrencias': 30, 'taxa_100k': 300, 'nivel': 'Alto', 'periculosidade': 4
        },
        'Jacarezinho': {
            'lat': -22.8833, 'lon': -43.2500, 'populacao': 80000,
            'ocorrencias': 35, 'taxa_100k': 438, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Rocinha': {
            'lat': -22.9833, 'lon': -43.2500, 'populacao': 70000,
            'ocorrencias': 30, 'taxa_100k': 429, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Complexo do Alemão': {
            'lat': -22.8500, 'lon': -43.2500, 'populacao': 120000,
            'ocorrencias': 50, 'taxa_100k': 417, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Maré': {
            'lat': -22.8500, 'lon': -43.2000, 'populacao': 100000,
            'ocorrencias': 40, 'taxa_100k': 400, 'nivel': 'Muito Alto', 'periculosidade': 5
        },
        'Cidade de Deus': {
            'lat': -22.9500, 'lon': -43.4000, 'populacao': 60000,
            'ocorrencias': 25, 'taxa_100k': 417, 'nivel': 'Muito Alto', 'periculosidade': 5
        }
    }
    
    # Converte para DataFrame
    dados = []
    for regiao, info in regioes_cidade_rio.items():
        # Define cor baseada no nível de periculosidade
        if info['periculosidade'] == 1:
            cor = '#2E8B57'  # Verde escuro - Muito Baixo
            nivel_cor = 'Muito Baixo'
        elif info['periculosidade'] == 2:
            cor = '#32CD32'  # Verde claro - Baixo
            nivel_cor = 'Baixo'
        elif info['periculosidade'] == 3:
            cor = '#FFD700'  # Amarelo - Médio
            nivel_cor = 'Médio'
        elif info['periculosidade'] == 4:
            cor = '#FF8C00'  # Laranja - Alto
            nivel_cor = 'Alto'
        else:  # 5
            cor = '#DC143C'  # Vermelho - Muito Alto
            nivel_cor = 'Muito Alto'
        
        dados.append({
            'regiao': regiao,
            'lat': info['lat'],
            'lon': info['lon'],
            'populacao': info['populacao'],
            'ocorrencias': info['ocorrencias'],
            'taxa_100k': info['taxa_100k'],
            'nivel_violencia': info['nivel'],
            'periculosidade': info['periculosidade'],
            'nivel_cor': nivel_cor,
            'cor': cor
        })
    
    return pd.DataFrame(dados)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🗺️ Mapa da Cidade do Rio de Janeiro")
    st.markdown("### Regiões Administrativas por Nível de Periculosidade")
    
    # Carrega dados
    dados = carregar_dados_cidade_rio()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filtros")
        
        # Filtro de regiões
        regioes_selecionadas = st.multiselect(
            "Regiões Administrativas",
            dados['regiao'].unique(),
            default=dados['regiao'].unique()
        )
        
        # Filtro de nível de periculosidade
        niveis_selecionados = st.multiselect(
            "Níveis de Periculosidade",
            dados['nivel_cor'].unique(),
            default=dados['nivel_cor'].unique()
        )
        
        # Filtro de periculosidade numérica
        periculosidade_min = st.slider(
            "Periculosidade Mínima",
            min_value=1,
            max_value=5,
            value=1
        )
        
        st.markdown("---")
        st.info("""
        **🗺️ Mapa da Cidade do Rio:**
        - 33 Regiões Administrativas
        - Cores por nível de periculosidade
        - Limite municipal do Rio de Janeiro
        - Dados dos últimos 6 meses
        """)
    
    # Filtra dados
    dados_filtrados = dados[
        (dados['regiao'].isin(regioes_selecionadas)) & 
        (dados['nivel_cor'].isin(niveis_selecionados)) &
        (dados['periculosidade'] >= periculosidade_min)
    ]
    
    # ==================== MAPA PRINCIPAL ====================
    
    st.header("🗺️ Mapa da Cidade do Rio de Janeiro")
    
    # Cria mapa principal com Plotly
    fig = px.scatter_mapbox(
        dados_filtrados,
        lat='lat',
        lon='lon',
        size='ocorrencias',
        color='periculosidade',
        hover_name='regiao',
        hover_data={
            'lat': False,
            'lon': False,
            'ocorrencias': True,
            'taxa_100k': ':.0f',
            'populacao': True,
            'nivel_violencia': True,
            'periculosidade': True
        },
        color_continuous_scale='RdYlGn_r',  # Vermelho para alto, verde para baixo
        size_max=50,
        title='Mapa da Cidade do Rio de Janeiro - Periculosidade por Região',
        mapbox_style='open-street-map',
        zoom=10,
        center={'lat': -22.9068, 'lon': -43.1729}
    )
    
    fig.update_layout(
        height=700,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Nível de Periculosidade",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ==================== MAPA CHOROPLETH ====================
    
    st.header("🎨 Mapa Choropleth - Periculosidade por Cor")
    
    # Cria mapa choropleth
    fig_choropleth = px.scatter_mapbox(
        dados_filtrados,
        lat='lat',
        lon='lon',
        size='ocorrencias',
        color='nivel_cor',
        hover_name='regiao',
        hover_data={
            'lat': False,
            'lon': False,
            'ocorrencias': True,
            'taxa_100k': ':.0f',
            'populacao': True,
            'nivel_violencia': True
        },
        color_discrete_map={
            'Muito Baixo': '#2E8B57',
            'Baixo': '#32CD32',
            'Médio': '#FFD700',
            'Alto': '#FF8C00',
            'Muito Alto': '#DC143C'
        },
        title='Mapa Choropleth - Periculosidade por Região',
        mapbox_style='open-street-map',
        zoom=10,
        center={'lat': -22.9068, 'lon': -43.1729}
    )
    
    fig_choropleth.update_layout(
        height=700,
        title_x=0.5
    )
    
    st.plotly_chart(fig_choropleth, use_container_width=True)
    
    # ==================== LEGENDA DE CORES ====================
    
    st.header("🎨 Legenda de Periculosidade")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background-color: #2E8B57; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Muito Baixo</strong><br>
            0-100/100k<br>
            <small>Periculosidade: 1</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #32CD32; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Baixo</strong><br>
            100-200/100k<br>
            <small>Periculosidade: 2</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #FFD700; color: black; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Médio</strong><br>
            200-300/100k<br>
            <small>Periculosidade: 3</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #FF8C00; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Alto</strong><br>
            300-400/100k<br>
            <small>Periculosidade: 4</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background-color: #DC143C; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Muito Alto</strong><br>
            400+/100k<br>
            <small>Periculosidade: 5</small>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== ESTATÍSTICAS ====================
    
    st.header("📊 Estatísticas por Região")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taxa de Periculosidade por Região")
        
        # Gráfico de barras
        fig_barras = px.bar(
            dados_filtrados.sort_values('taxa_100k', ascending=True),
            x='taxa_100k',
            y='regiao',
            color='nivel_cor',
            orientation='h',
            title='Taxa de Periculosidade por Região',
            labels={'regiao': 'Região', 'taxa_100k': 'Taxa (/100k hab)'},
            color_discrete_map={
                'Muito Baixo': '#2E8B57',
                'Baixo': '#32CD32',
                'Médio': '#FFD700',
                'Alto': '#FF8C00',
                'Muito Alto': '#DC143C'
            }
        )
        
        fig_barras.update_layout(height=600)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição por Nível de Periculosidade")
        
        # Gráfico de pizza
        nivel_counts = dados_filtrados['nivel_cor'].value_counts()
        
        fig_pizza = px.pie(
            values=nivel_counts.values,
            names=nivel_counts.index,
            title='Distribuição por Nível de Periculosidade',
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
    
    st.header("📋 Dados Detalhados por Região")
    
    # Tabela com informações
    tabela = dados_filtrados[['regiao', 'ocorrencias', 'taxa_100k', 'nivel_cor', 'periculosidade', 'populacao']].copy()
    tabela = tabela.sort_values('periculosidade', ascending=False)
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
            f"mapa_cidade_rio_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        # Download estatísticas
        csv_stats = tabela.to_csv(index=False)
        st.download_button(
            "📈 Download Estatísticas",
            csv_stats,
            f"estatisticas_cidade_rio_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.markdown("""
    **🗺️ Mapa da Cidade do Rio de Janeiro**
    
    *Visualização das regiões administrativas por nível de periculosidade*
    
    **📊 Dados:** Últimos 6 meses (baseados em padrões reais)  
    **🗺️ Regiões:** 33 Regiões Administrativas da Cidade do Rio  
    **🎨 Visualização:** Cores por nível de periculosidade  
    **📅 Atualização:** Dados simulados baseados em estatísticas reais
    """)

if __name__ == "__main__":
    main()
