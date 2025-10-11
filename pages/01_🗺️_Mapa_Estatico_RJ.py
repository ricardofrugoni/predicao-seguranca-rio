"""
🗺️ MAPA ESTÁTICO DO MUNICÍPIO DO RIO DE JANEIRO
===============================================

Mapa estático com regiões administrativas separadas por criminalidade
Cores por intensidade de violência
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
    page_title="🗺️ Mapa Estático - Município RJ",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================================
# DADOS DAS REGIÕES ADMINISTRATIVAS DO MUNICÍPIO DO RIO
# ============================================================================

@st.cache_data
def carregar_regioes_municipio_rio():
    """Carrega dados das regiões administrativas do município do Rio"""
    
    # Regiões Administrativas do Município do Rio de Janeiro (33 RAs)
    regioes = {
        'Centro': {
            'lat': -22.9068, 'lon': -43.1729, 'populacao': 450000,
            'ocorrencias': 45, 'taxa_100k': 100, 'nivel': 'Médio'
        },
        'Zona Sul': {
            'lat': -22.9711, 'lon': -43.1822, 'populacao': 380000,
            'ocorrencias': 25, 'taxa_100k': 66, 'nivel': 'Baixo'
        },
        'Zona Norte': {
            'lat': -22.8944, 'lon': -43.2400, 'populacao': 1200000,
            'ocorrencias': 180, 'taxa_100k': 150, 'nivel': 'Médio'
        },
        'Zona Oeste': {
            'lat': -22.8847, 'lon': -43.3300, 'populacao': 850000,
            'ocorrencias': 255, 'taxa_100k': 300, 'nivel': 'Alto'
        },
        'Barra da Tijuca': {
            'lat': -23.0065, 'lon': -43.3641, 'populacao': 320000,
            'ocorrencias': 40, 'taxa_100k': 125, 'nivel': 'Médio'
        },
        'Recreio dos Bandeirantes': {
            'lat': -23.0236, 'lon': -43.4567, 'populacao': 180000,
            'ocorrencias': 20, 'taxa_100k': 111, 'nivel': 'Médio'
        },
        'Jacarepaguá': {
            'lat': -22.9500, 'lon': -43.3500, 'populacao': 280000,
            'ocorrencias': 85, 'taxa_100k': 304, 'nivel': 'Alto'
        },
        'Campo Grande': {
            'lat': -22.9000, 'lon': -43.5500, 'populacao': 320000,
            'ocorrencias': 160, 'taxa_100k': 500, 'nivel': 'Muito Alto'
        },
        'Santa Cruz': {
            'lat': -22.9167, 'lon': -43.6833, 'populacao': 250000,
            'ocorrencias': 125, 'taxa_100k': 500, 'nivel': 'Muito Alto'
        },
        'Guaratiba': {
            'lat': -23.0167, 'lon': -43.5667, 'populacao': 120000,
            'ocorrencias': 60, 'taxa_100k': 500, 'nivel': 'Muito Alto'
        },
        'Ilha do Governador': {
            'lat': -22.8167, 'lon': -43.1833, 'populacao': 180000,
            'ocorrencias': 45, 'taxa_100k': 250, 'nivel': 'Alto'
        },
        'Tijuca': {
            'lat': -22.9167, 'lon': -43.2333, 'populacao': 220000,
            'ocorrencias': 55, 'taxa_100k': 250, 'nivel': 'Alto'
        },
        'Vila Isabel': {
            'lat': -22.9167, 'lon': -43.2500, 'populacao': 150000,
            'ocorrencias': 40, 'taxa_100k': 267, 'nivel': 'Alto'
        },
        'Méier': {
            'lat': -22.9000, 'lon': -43.2833, 'populacao': 200000,
            'ocorrencias': 50, 'taxa_100k': 250, 'nivel': 'Alto'
        },
        'Madureira': {
            'lat': -22.8833, 'lon': -43.3333, 'populacao': 180000,
            'ocorrencias': 45, 'taxa_100k': 250, 'nivel': 'Alto'
        },
        'Bangu': {
            'lat': -22.8833, 'lon': -43.4667, 'populacao': 250000,
            'ocorrencias': 100, 'taxa_100k': 400, 'nivel': 'Muito Alto'
        },
        'Realengo': {
            'lat': -22.8667, 'lon': -43.4500, 'populacao': 200000,
            'ocorrencias': 80, 'taxa_100k': 400, 'nivel': 'Muito Alto'
        },
        'Padre Miguel': {
            'lat': -22.8833, 'lon': -43.4000, 'populacao': 180000,
            'ocorrencias': 70, 'taxa_100k': 389, 'nivel': 'Muito Alto'
        }
    }
    
    # Converte para DataFrame
    dados = []
    for regiao, info in regioes.items():
        # Define cor baseada no nível
        if info['nivel'] == 'Muito Baixo':
            cor = '#2E8B57'
            intensidade = 1
        elif info['nivel'] == 'Baixo':
            cor = '#32CD32'
            intensidade = 2
        elif info['nivel'] == 'Médio':
            cor = '#FFD700'
            intensidade = 3
        elif info['nivel'] == 'Alto':
            cor = '#FF8C00'
            intensidade = 4
        else:  # Muito Alto
            cor = '#DC143C'
            intensidade = 5
        
        dados.append({
            'regiao': regiao,
            'lat': info['lat'],
            'lon': info['lon'],
            'populacao': info['populacao'],
            'ocorrencias': info['ocorrencias'],
            'taxa_100k': info['taxa_100k'],
            'nivel_violencia': info['nivel'],
            'cor': cor,
            'intensidade': intensidade
        })
    
    return pd.DataFrame(dados)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🗺️ Mapa Estático - Município do Rio de Janeiro")
    st.markdown("### Regiões Administrativas por Intensidade de Criminalidade")
    
    # Carrega dados
    dados = carregar_regioes_municipio_rio()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filtros")
        
        # Filtro de regiões
        regioes_selecionadas = st.multiselect(
            "Regiões Administrativas",
            dados['regiao'].unique(),
            default=dados['regiao'].unique()
        )
        
        # Filtro de nível de violência
        niveis_selecionados = st.multiselect(
            "Níveis de Criminalidade",
            dados['nivel_violencia'].unique(),
            default=dados['nivel_violencia'].unique()
        )
        
        st.markdown("---")
        st.info("""
        **🗺️ Mapa Estático:**
        - 18 Regiões Administrativas
        - Cores por intensidade de criminalidade
        - Dados dos últimos 6 meses
        - Foco no município do Rio
        """)
    
    # Filtra dados
    dados_filtrados = dados[
        (dados['regiao'].isin(regioes_selecionadas)) & 
        (dados['nivel_violencia'].isin(niveis_selecionados))
    ]
    
    # ==================== MAPA ESTÁTICO ====================
    
    st.header("🗺️ Mapa Estático - Criminalidade por Região")
    
    # Cria mapa estático com Plotly
    fig = go.Figure()
    
    # Adiciona cada região como um círculo colorido
    for _, row in dados_filtrados.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['lon']],
            y=[row['lat']],
            mode='markers',
            marker=dict(
                size=row['ocorrencias'] * 2,  # Tamanho baseado em ocorrências
                color=row['cor'],
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            name=row['regiao'],
            text=f"{row['regiao']}<br>Ocorrências: {row['ocorrencias']}<br>Taxa: {row['taxa_100k']:.0f}/100k",
            hovertemplate="<b>%{text}</b><extra></extra>"
        ))
    
    # Configura o layout do mapa
    fig.update_layout(
        title="Mapa Estático - Criminalidade por Região Administrativa",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        height=700,
        showlegend=False,
        template='plotly_white'
    )
    
    # Define limites do município do Rio
    fig.update_xaxes(range=[-43.8, -43.0])
    fig.update_yaxes(range=[-23.2, -22.7])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ==================== MAPA CHOROPLETH ====================
    
    st.header("🎨 Mapa Choropleth - Intensidade por Cor")
    
    # Cria mapa choropleth
    fig_choropleth = px.scatter_mapbox(
        dados_filtrados,
        lat='lat',
        lon='lon',
        size='ocorrencias',
        color='intensidade',
        hover_name='regiao',
        hover_data={
            'lat': False,
            'lon': False,
            'ocorrencias': True,
            'taxa_100k': ':.0f',
            'populacao': True,
            'nivel_violencia': True
        },
        color_continuous_scale='RdYlGn_r',  # Vermelho para alto, verde para baixo
        size_max=50,
        title='Mapa Choropleth - Intensidade de Criminalidade',
        mapbox_style='open-street-map',
        zoom=10,
        center={'lat': -22.9068, 'lon': -43.1729}
    )
    
    fig_choropleth.update_layout(
        height=700,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Intensidade de Criminalidade",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
        )
    )
    
    st.plotly_chart(fig_choropleth, use_container_width=True)
    
    # ==================== LEGENDA DE CORES ====================
    
    st.header("🎨 Legenda de Cores")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background-color: #2E8B57; color: white; padding: 10px; text-align: center; border-radius: 5px;">
            <strong>Muito Baixo</strong><br>
            0-100/100k
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #32CD32; color: white; padding: 10px; text-align: center; border-radius: 5px;">
            <strong>Baixo</strong><br>
            100-200/100k
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #FFD700; color: black; padding: 10px; text-align: center; border-radius: 5px;">
            <strong>Médio</strong><br>
            200-300/100k
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #FF8C00; color: white; padding: 10px; text-align: center; border-radius: 5px;">
            <strong>Alto</strong><br>
            300-400/100k
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background-color: #DC143C; color: white; padding: 10px; text-align: center; border-radius: 5px;">
            <strong>Muito Alto</strong><br>
            400+/100k
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== ESTATÍSTICAS ====================
    
    st.header("📊 Estatísticas por Região")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taxa de Criminalidade")
        
        # Gráfico de barras
        fig_barras = px.bar(
            dados_filtrados.sort_values('taxa_100k', ascending=True),
            x='taxa_100k',
            y='regiao',
            color='nivel_violencia',
            orientation='h',
            title='Taxa de Criminalidade por Região',
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
        st.subheader("Distribuição por Nível")
        
        # Gráfico de pizza
        nivel_counts = dados_filtrados['nivel_violencia'].value_counts()
        
        fig_pizza = px.pie(
            values=nivel_counts.values,
            names=nivel_counts.index,
            title='Distribuição por Nível de Criminalidade',
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
    tabela = dados_filtrados[['regiao', 'ocorrencias', 'taxa_100k', 'nivel_violencia', 'populacao']].copy()
    tabela = tabela.sort_values('taxa_100k', ascending=False)
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
            f"mapa_estatico_rio_{datetime.now().strftime('%Y%m%d')}.csv",
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
    **🗺️ Mapa Estático - Município do Rio de Janeiro**
    
    *Visualização das regiões administrativas por intensidade de criminalidade*
    
    **📊 Dados:** Últimos 6 meses (baseados em padrões reais)  
    **🗺️ Regiões:** 18 Regiões Administrativas do Município  
    **🎨 Visualização:** Cores por intensidade de criminalidade  
    **📅 Atualização:** Dados simulados baseados em estatísticas reais
    """)

if __name__ == "__main__":
    main()
