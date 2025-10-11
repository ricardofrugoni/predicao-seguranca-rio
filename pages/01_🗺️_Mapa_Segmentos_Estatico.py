"""
🗺️ MAPA ESTÁTICO - SEGMENTOS NUMERADOS DO RIO
============================================

Mapa estático do município do Rio com segmentos numerados (01-33)
Cores por manchas criminais
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
    page_title="🗺️ Mapa Segmentos - Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================================
# DADOS DOS SEGMENTOS NUMERADOS (01-33)
# ============================================================================

@st.cache_data
def carregar_segmentos_rio():
    """Carrega dados dos 33 segmentos numerados do Rio"""
    
    # Segmentos numerados do Rio de Janeiro (01-33)
    segmentos_rio = {
        '01': {'nome': 'Anchieta', 'lat': -22.8500, 'lon': -43.4000, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '02': {'nome': 'Bangu', 'lat': -22.8833, 'lon': -43.4667, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '03': {'nome': 'Barra da Tijuca', 'lat': -23.0065, 'lon': -43.3641, 'mancha_criminal': 2, 'cor': '#32CD32'},
        '04': {'nome': 'Botafogo', 'lat': -22.9500, 'lon': -43.1833, 'mancha_criminal': 2, 'cor': '#32CD32'},
        '05': {'nome': 'Campo Grande', 'lat': -22.9000, 'lon': -43.5500, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '06': {'nome': 'Centro', 'lat': -22.9068, 'lon': -43.1729, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '07': {'nome': 'Cidade de Deus', 'lat': -22.9500, 'lon': -43.4000, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '08': {'nome': 'Complexo Alemão', 'lat': -22.8500, 'lon': -43.2500, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '09': {'nome': 'Copacabana', 'lat': -22.9700, 'lon': -43.1833, 'mancha_criminal': 2, 'cor': '#32CD32'},
        '10': {'nome': 'Guaratiba', 'lat': -23.0167, 'lon': -43.5667, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '11': {'nome': 'Ilha de Paquetá', 'lat': -22.8167, 'lon': -43.1000, 'mancha_criminal': 1, 'cor': '#2E8B57'},
        '12': {'nome': 'Ilha do Governador', 'lat': -22.8167, 'lon': -43.1833, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '13': {'nome': 'Inhaúma', 'lat': -22.8500, 'lon': -43.3000, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '14': {'nome': 'Irajá', 'lat': -22.8167, 'lon': -43.2500, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '15': {'nome': 'Jacarepaguá', 'lat': -22.9500, 'lon': -43.3500, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '16': {'nome': 'Jacarezinho', 'lat': -22.8833, 'lon': -43.2500, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '17': {'nome': 'Lagoa', 'lat': -22.9700, 'lon': -43.2000, 'mancha_criminal': 2, 'cor': '#32CD32'},
        '18': {'nome': 'Madureira', 'lat': -22.8833, 'lon': -43.3333, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '19': {'nome': 'Maré', 'lat': -22.8500, 'lon': -43.2000, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '20': {'nome': 'Méier', 'lat': -22.9000, 'lon': -43.2833, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '21': {'nome': 'Pavuna', 'lat': -22.8167, 'lon': -43.3500, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '22': {'nome': 'Penha', 'lat': -22.8167, 'lon': -43.3000, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '23': {'nome': 'Portuária', 'lat': -22.9000, 'lon': -43.1833, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '24': {'nome': 'Ramos', 'lat': -22.8500, 'lon': -43.1833, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '25': {'nome': 'Realengo', 'lat': -22.8667, 'lon': -43.4500, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '26': {'nome': 'Rio Comprido', 'lat': -22.9167, 'lon': -43.2000, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '27': {'nome': 'Rocinha', 'lat': -22.9833, 'lon': -43.2500, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '28': {'nome': 'Santa Cruz', 'lat': -22.9167, 'lon': -43.6833, 'mancha_criminal': 5, 'cor': '#DC143C'},
        '29': {'nome': 'Santa Teresa', 'lat': -22.9167, 'lon': -43.1833, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '30': {'nome': 'São Cristóvão', 'lat': -22.9000, 'lon': -43.2167, 'mancha_criminal': 3, 'cor': '#FFD700'},
        '31': {'nome': 'Tijuca', 'lat': -22.9167, 'lon': -43.2333, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '32': {'nome': 'Vigário Geral', 'lat': -22.8500, 'lon': -43.2667, 'mancha_criminal': 4, 'cor': '#FF8C00'},
        '33': {'nome': 'Vila Isabel', 'lat': -22.9167, 'lon': -43.2500, 'mancha_criminal': 4, 'cor': '#FF8C00'}
    }
    
    # Converte para DataFrame
    dados = []
    for codigo, info in segmentos_rio.items():
        # Define nível baseado na mancha criminal
        if info['mancha_criminal'] == 1:
            nivel = 'Muito Baixo'
        elif info['mancha_criminal'] == 2:
            nivel = 'Baixo'
        elif info['mancha_criminal'] == 3:
            nivel = 'Médio'
        elif info['mancha_criminal'] == 4:
            nivel = 'Alto'
        else:  # 5
            nivel = 'Muito Alto'
        
        dados.append({
            'codigo': codigo,
            'nome': info['nome'],
            'lat': info['lat'],
            'lon': info['lon'],
            'mancha_criminal': info['mancha_criminal'],
            'cor': info['cor'],
            'nivel': nivel
        })
    
    return pd.DataFrame(dados)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

def main():
    st.title("🗺️ Mapa Estático - Segmentos do Rio de Janeiro")
    st.markdown("### Município do Rio dividido em 33 segmentos numerados com cores por manchas criminais")
    
    # Carrega dados
    dados = carregar_segmentos_rio()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filtros")
        
        # Filtro de segmentos
        segmentos_selecionados = st.multiselect(
            "Segmentos (01-33)",
            dados['codigo'].unique(),
            default=dados['codigo'].unique()
        )
        
        # Filtro de nível de mancha criminal
        niveis_selecionados = st.multiselect(
            "Níveis de Mancha Criminal",
            dados['nivel'].unique(),
            default=dados['nivel'].unique()
        )
        
        # Filtro de mancha criminal numérica
        mancha_min = st.slider(
            "Mancha Criminal Mínima",
            min_value=1,
            max_value=5,
            value=1
        )
        
        st.markdown("---")
        st.info("""
        **🗺️ Mapa Estático:**
        - 33 Segmentos numerados (01-33)
        - Cores por mancha criminal
        - Município do Rio de Janeiro
        - Dados dos últimos 6 meses
        """)
    
    # Filtra dados
    dados_filtrados = dados[
        (dados['codigo'].isin(segmentos_selecionados)) & 
        (dados['nivel'].isin(niveis_selecionados)) &
        (dados['mancha_criminal'] >= mancha_min)
    ]
    
    # ==================== MAPA ESTÁTICO PRINCIPAL ====================
    
    st.header("🗺️ Mapa Estático - Segmentos Numerados")
    
    # Cria mapa estático com segmentos numerados
    fig = go.Figure()
    
    # Adiciona cada segmento como um círculo colorido com número
    for _, row in dados_filtrados.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['lon']],
            y=[row['lat']],
            mode='markers+text',
            marker=dict(
                size=50,
                color=row['cor'],
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=row['codigo'],
            textposition='middle center',
            textfont=dict(size=12, color='white', family='Arial Black'),
            name=f"{row['codigo']} - {row['nome']}",
            hovertemplate=f"<b>Segmento {row['codigo']}</b><br>{row['nome']}<br>Mancha: {row['mancha_criminal']}/5<br>Nível: {row['nivel']}<extra></extra>"
        ))
    
    # Configura o layout do mapa
    fig.update_layout(
        title="Mapa Estático - Segmentos do Rio de Janeiro (01-33)",
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
    
    st.header("🎨 Mapa Choropleth - Manchas Criminais")
    
    # Cria mapa choropleth
    fig_choropleth = px.scatter_mapbox(
        dados_filtrados,
        lat='lat',
        lon='lon',
        size='mancha_criminal',
        color='mancha_criminal',
        hover_name='codigo',
        hover_data={
            'lat': False,
            'lon': False,
            'nome': True,
            'mancha_criminal': True,
            'nivel': True
        },
        color_continuous_scale='RdYlGn_r',  # Vermelho para alto, verde para baixo
        size_max=50,
        title='Mapa Choropleth - Manchas Criminais por Segmento',
        mapbox_style='open-street-map',
        zoom=10,
        center={'lat': -22.9068, 'lon': -43.1729}
    )
    
    fig_choropleth.update_layout(
        height=700,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Mancha Criminal",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
        )
    )
    
    st.plotly_chart(fig_choropleth, use_container_width=True)
    
    # ==================== LEGENDA DE CORES ====================
    
    st.header("🎨 Legenda de Manchas Criminais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background-color: #2E8B57; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Muito Baixo</strong><br>
            Mancha: 1<br>
            <small>Verde Escuro</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #32CD32; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Baixo</strong><br>
            Mancha: 2<br>
            <small>Verde Claro</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #FFD700; color: black; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Médio</strong><br>
            Mancha: 3<br>
            <small>Amarelo</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #FF8C00; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Alto</strong><br>
            Mancha: 4<br>
            <small>Laranja</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background-color: #DC143C; color: white; padding: 15px; text-align: center; border-radius: 8px; margin: 5px;">
            <strong>Muito Alto</strong><br>
            Mancha: 5<br>
            <small>Vermelho</small>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== TABELA DE SEGMENTOS ====================
    
    st.header("📋 Segmentos Numerados (01-33)")
    
    # Tabela com informações
    tabela = dados_filtrados[['codigo', 'nome', 'mancha_criminal', 'nivel', 'lat', 'lon']].copy()
    tabela = tabela.sort_values('codigo')
    
    st.dataframe(tabela, use_container_width=True)
    
    # ==================== ESTATÍSTICAS ====================
    
    st.header("📊 Estatísticas por Mancha Criminal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição por Nível")
        
        # Gráfico de pizza
        nivel_counts = dados_filtrados['nivel'].value_counts()
        
        fig_pizza = px.pie(
            values=nivel_counts.values,
            names=nivel_counts.index,
            title='Distribuição por Nível de Mancha Criminal',
            color_discrete_map={
                'Muito Baixo': '#2E8B57',
                'Baixo': '#32CD32',
                'Médio': '#FFD700',
                'Alto': '#FF8C00',
                'Muito Alto': '#DC143C'
            }
        )
        
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col2:
        st.subheader("Mancha Criminal por Segmento")
        
        # Gráfico de barras
        fig_barras = px.bar(
            dados_filtrados.sort_values('mancha_criminal', ascending=True),
            x='mancha_criminal',
            y='codigo',
            color='nivel',
            orientation='h',
            title='Mancha Criminal por Segmento',
            labels={'mancha_criminal': 'Mancha Criminal', 'codigo': 'Segmento'},
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
    
    # ==================== DOWNLOADS ====================
    
    st.header("📥 Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download dados
        csv_dados = dados_filtrados.to_csv(index=False)
        st.download_button(
            "📊 Download Dados dos Segmentos",
            csv_dados,
            f"segmentos_rio_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with col2:
        # Download estatísticas
        csv_stats = tabela.to_csv(index=False)
        st.download_button(
            "📈 Download Estatísticas",
            csv_stats,
            f"estatisticas_segmentos_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.markdown("""
    **🗺️ Mapa Estático - Segmentos do Rio de Janeiro**
    
    *Visualização dos 33 segmentos numerados com cores por manchas criminais*
    
    **📊 Dados:** Últimos 6 meses (baseados em padrões reais)  
    **🗺️ Segmentos:** 33 Segmentos numerados (01-33)  
    **🎨 Visualização:** Cores por mancha criminal  
    **📅 Atualização:** Dados simulados baseados em estatísticas reais
    """)

if __name__ == "__main__":
    main()
