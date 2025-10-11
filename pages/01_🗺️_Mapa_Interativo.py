"""
🗺️ MAPA INTERATIVO - Análise Geoespacial de Violência
=====================================================

Página para visualização geoespacial com hotspots, clusters e análises espaciais.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Point
import json
from datetime import datetime

def load_sample_geodata():
    """Carrega dados geoespaciais de exemplo"""
    # Coordenadas aproximadas das regiões do Rio
    regioes_coords = {
        'Centro': (-22.9068, -43.1729),
        'Zona Sul': (-22.9711, -43.1822),
        'Zona Norte': (-22.8798, -43.2500),
        'Barra da Tijuca': (-23.0065, -43.3641),
        'Zona Oeste': (-22.8844, -43.2356)
    }
    
    # Gera dados simulados
    np.random.seed(42)
    dados = []
    
    for regiao, (lat, lon) in regioes_coords.items():
        # Simula variação espacial
        for i in range(20):  # 20 pontos por região
            lat_var = lat + np.random.normal(0, 0.01)
            lon_var = lon + np.random.normal(0, 0.01)
            
            # Simula intensidade de crime
            intensidade = np.random.exponential(2)
            
            dados.append({
                'regiao': regiao,
                'latitude': lat_var,
                'longitude': lon_var,
                'intensidade': intensidade,
                'tipo_crime': np.random.choice(['Homicídio', 'Roubo', 'Furto']),
                'data': pd.date_range('2024-01-01', '2024-12-31', freq='M')[np.random.randint(0, 12)]
            })
    
    return pd.DataFrame(dados)

def create_choropleth_map(df):
    """Cria mapa de coropleth por região"""
    # Agrupa por região
    df_region = df.groupby('regiao').agg({
        'intensidade': 'sum',
        'latitude': 'mean',
        'longitude': 'mean'
    }).reset_index()
    
    # Cria mapa
    m = folium.Map(
        location=[-22.9068, -43.1729],  # Centro do Rio
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Adiciona marcadores por região
    for _, row in df_region.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['intensidade'] * 5,
            popup=f"""
            <b>{row['regiao']}</b><br>
            Intensidade: {row['intensidade']:.2f}<br>
            Total: {row['intensidade']:.0f}
            """,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.6
        ).add_to(m)
    
    return m

def create_heatmap(df):
    """Cria mapa de calor"""
    # Cria mapa base
    m = folium.Map(
        location=[-22.9068, -43.1729],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Adiciona pontos de calor
    heat_data = [[row['latitude'], row['longitude'], row['intensidade']] 
                 for _, row in df.iterrows()]
    
    from folium.plugins import HeatMap
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)
    
    return m

def create_cluster_map(df):
    """Cria mapa com clusters"""
    from folium.plugins import MarkerCluster
    
    m = folium.Map(
        location=[-22.9068, -43.1729],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Cria cluster de marcadores
    marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"""
            <b>{row['tipo_crime']}</b><br>
            Região: {row['regiao']}<br>
            Intensidade: {row['intensidade']:.2f}
            """,
            icon=folium.Icon(
                color='red' if row['tipo_crime'] == 'Homicídio' else 'orange',
                icon='info-sign'
            )
        ).add_to(marker_cluster)
    
    return m

def create_analysis_charts(df):
    """Cria gráficos de análise espacial"""
    
    # Gráfico 1: Distribuição por região
    df_region = df.groupby('regiao')['intensidade'].sum().reset_index()
    
    fig1 = px.bar(
        df_region, 
        x='regiao', 
        y='intensidade',
        title='Intensidade de Crime por Região',
        color='intensidade',
        color_continuous_scale='Reds'
    )
    fig1.update_layout(height=400)
    
    # Gráfico 2: Distribuição por tipo de crime
    df_crime = df.groupby('tipo_crime')['intensidade'].sum().reset_index()
    
    fig2 = px.pie(
        df_crime,
        values='intensidade',
        names='tipo_crime',
        title='Distribuição por Tipo de Crime',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig2.update_layout(height=400)
    
    # Gráfico 3: Scatter plot lat/lon
    fig3 = px.scatter(
        df,
        x='longitude',
        y='latitude',
        size='intensidade',
        color='tipo_crime',
        title='Distribuição Espacial dos Crimes',
        hover_data=['regiao', 'intensidade']
    )
    fig3.update_layout(height=400)
    
    return fig1, fig2, fig3

def main():
    """Função principal"""
    st.title("🗺️ Mapa Interativo - Análise Geoespacial")
    st.markdown("Visualização geoespacial com hotspots, clusters e análises espaciais de violência no Rio de Janeiro.")
    
    # Carrega dados
    df = load_sample_geodata()
    
    # Sidebar com controles
    st.sidebar.title("🎛️ Controles")
    
    # Filtros
    st.sidebar.subheader("🔍 Filtros")
    
    regioes_selecionadas = st.sidebar.multiselect(
        "Regiões:",
        df['regiao'].unique(),
        default=df['regiao'].unique()
    )
    
    tipos_selecionados = st.sidebar.multiselect(
        "Tipos de Crime:",
        df['tipo_crime'].unique(),
        default=df['tipo_crime'].unique()
    )
    
    # Aplica filtros
    df_filtrado = df[
        (df['regiao'].isin(regioes_selecionadas)) &
        (df['tipo_crime'].isin(tipos_selecionados))
    ]
    
    # Tipo de visualização
    st.sidebar.subheader("🗺️ Tipo de Mapa")
    tipo_mapa = st.sidebar.selectbox(
        "Selecione o tipo de visualização:",
        ["Coropleth", "Heatmap", "Clusters", "Todos"]
    )
    
    # Métricas
    st.markdown("## 📊 Métricas Espaciais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Pontos", len(df_filtrado))
    
    with col2:
        st.metric("Intensidade Média", f"{df_filtrado['intensidade'].mean():.2f}")
    
    with col3:
        st.metric("Região Mais Afetada", df_filtrado.groupby('regiao')['intensidade'].sum().idxmax())
    
    with col4:
        st.metric("Crime Mais Comum", df_filtrado['tipo_crime'].mode().iloc[0])
    
    # Mapas
    st.markdown("## 🗺️ Visualizações Geoespaciais")
    
    if tipo_mapa == "Coropleth" or tipo_mapa == "Todos":
        st.subheader("📊 Mapa de Coropleth")
        mapa_coropleth = create_choropleth_map(df_filtrado)
        st_folium(mapa_coropleth, width=700, height=500)
    
    if tipo_mapa == "Heatmap" or tipo_mapa == "Todos":
        st.subheader("🔥 Mapa de Calor")
        mapa_heatmap = create_heatmap(df_filtrado)
        st_folium(mapa_heatmap, width=700, height=500)
    
    if tipo_mapa == "Clusters" or tipo_mapa == "Todos":
        st.subheader("📍 Mapa com Clusters")
        mapa_clusters = create_cluster_map(df_filtrado)
        st_folium(mapa_clusters, width=700, height=500)
    
    # Análises
    st.markdown("## 📈 Análises Espaciais")
    
    fig1, fig2, fig3 = create_analysis_charts(df_filtrado)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Tabela de dados
    st.markdown("## 📋 Dados Detalhados")
    
    if st.checkbox("Mostrar dados brutos"):
        st.dataframe(df_filtrado, use_container_width=True)
    
    # Download
    st.markdown("## 💾 Download")
    
    csv = df_filtrado.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        csv,
        f"dados_geoespaciais_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

if __name__ == "__main__":
    main()
