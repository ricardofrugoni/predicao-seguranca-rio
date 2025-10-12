"""
🗺️ MAPA CHOROPLETH - CRIMINALIDADE DO MUNICÍPIO DO RIO
======================================================

Mapa do MUNICÍPIO DO RIO DE JANEIRO com áreas detalhadas.
"""

import streamlit as st
import pandas as pd
import folium
import json
from pathlib import Path
from streamlit_folium import folium_static

st.set_page_config(
    page_title="🗺️ Mapa de Criminalidade - Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Mapa de Criminalidade do Município do Rio de Janeiro")
st.markdown("### Intensidade Criminal por Região")
st.warning("⚠️ **ATENÇÃO:** Este mapa exibe APENAS o município do Rio de Janeiro.")

# Cores por nível de criminalidade
cores_nivel = {
    "Muito Baixo": "#2ecc71",
    "Baixo": "#27ae60",
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

def criar_mapa():
    """Cria mapa choropleth"""
    
    # Tentar carregar GeoJSON
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "areas_detalhadas_rio.geojson",
        Path("data/shapefiles/areas_detalhadas_rio.geojson"),
        Path("projeto_violencia_rj/data/shapefiles/areas_detalhadas_rio.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_realista.geojson",
        Path("data/shapefiles/zonas_rio_realista.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson",
        Path("data/shapefiles/zonas_rio.geojson"),
    ]
    
    geojson_data = None
    for caminho in caminhos:
        try:
            if caminho.exists():
                with open(caminho, 'r', encoding='utf-8') as f:
                    geojson_data = json.load(f)
                st.success(f"✅ Carregado: {caminho.name}")
                break
        except:
            continue
    
    if not geojson_data:
        st.error("❌ Arquivo GeoJSON não encontrado!")
        st.info("Execute: `python scripts/buscar_dados_oficiais_rio.py`")
        return None
    
    # Centro do Rio
    mapa = folium.Map(
        location=[-22.9068, -43.4200],
        zoom_start=10,
        tiles='CartoDB positron',
        min_zoom=10,
        max_zoom=14
    )
    
    # Adicionar cada feature com sua cor
    for feature in geojson_data.get('features', []):
        nivel = feature['properties'].get('nivel', 'Médio')
        nome = feature['properties'].get('nome', 'Sem nome')
        cor = cores_nivel.get(nivel, '#f39c12')
        
        folium.GeoJson(
            feature,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': '#000000',
                'weight': 1,
                'fillOpacity': 0.8
            },
            tooltip=f"{nome} - {nivel}"
        ).add_to(mapa)
    
    # Legenda
    legenda_html = '''
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px; 
                background-color: white; z-index:9999; padding: 10px;
                border:2px solid grey; border-radius: 5px;">
        <p style="margin:0; font-weight: bold;">Nível de Criminalidade</p>
        <p style="margin: 5px 0;">
            <i style="background: #2ecc71; width: 30px; height: 15px; 
               float: left; margin-right: 8px;"></i> Muito Baixo
        </p>
        <p style="margin: 5px 0;">
            <i style="background: #27ae60; width: 30px; height: 15px; 
               float: left; margin-right: 8px;"></i> Baixo
        </p>
        <p style="margin: 5px 0;">
            <i style="background: #f39c12; width: 30px; height: 15px; 
               float: left; margin-right: 8px;"></i> Médio
        </p>
        <p style="margin: 5px 0;">
            <i style="background: #e67e22; width: 30px; height: 15px; 
               float: left; margin-right: 8px;"></i> Alto
        </p>
        <p style="margin: 5px 0;">
            <i style="background: #e74c3c; width: 30px; height: 15px; 
               float: left; margin-right: 8px;"></i> Muito Alto
        </p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa

# Exibir mapa
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa do Município")
    mapa = criar_mapa()
    if mapa:
        folium_static(mapa, width=900, height=600)

with col2:
    st.markdown("#### 📊 Informações")
    st.info("""
    **🗺️ Mapa do Município do Rio**
    
    Mostra apenas o município do Rio de Janeiro dividido em regiões com níveis de criminalidade.
    
    Cores indicam intensidade criminal.
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p><b>Município do Rio de Janeiro</b></p>
    <p>Mapa com divisões por nível de criminalidade</p>
</div>
""", unsafe_allow_html=True)
