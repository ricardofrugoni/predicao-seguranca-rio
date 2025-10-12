"""
Mapa de Criminalidade - Município do Rio de Janeiro
"""

import streamlit as st
import folium
import json
from pathlib import Path
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Mapa de Criminalidade - Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Mapa de Criminalidade - Município do Rio de Janeiro")
st.warning("⚠️ Apenas o município do Rio de Janeiro é exibido. Fundo escuro = áreas externas.")

CORES = {
    "Muito Baixo": "#2ecc71",
    "Baixo": "#27ae60",
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

def carregar_geojson():
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "areas_detalhadas_rio.geojson",
        Path("data/shapefiles/areas_detalhadas_rio.geojson"),
        Path("projeto_violencia_rj/data/shapefiles/areas_detalhadas_rio.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_realista.geojson",
        Path("data/shapefiles/zonas_rio_realista.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson"),
        Path("data/shapefiles/zonas_rio.geojson"),
    ]
    
    for caminho in caminhos:
        try:
            if caminho.exists():
                with open(caminho, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            continue
    return None

def criar_mapa():
    geojson = carregar_geojson()
    
    if not geojson:
        st.error("Erro ao carregar GeoJSON")
        return None
    
    mapa = folium.Map(
        location=[-22.9068, -43.4200],
        zoom_start=11,
        tiles='CartoDB dark_matter',
        min_zoom=10,
        max_zoom=14
    )
    
    for feature in geojson.get('features', []):
        nivel = feature['properties'].get('nivel', 'Médio')
        nome = feature['properties'].get('nome', '')
        cor = CORES.get(nivel, '#f39c12')
        
        folium.GeoJson(
            feature,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': cor,
                'weight': 0.5,
                'fillOpacity': 0.9
            },
            tooltip=f"{nome} - {nivel}"
        ).add_to(mapa)
    
    legenda = '''
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px;
                background-color: rgba(0,0,0,0.8); z-index:9999; padding: 15px;
                border: 2px solid white; border-radius: 5px; color: white;">
        <p style="margin:0; font-weight: bold; text-align: center;">Criminalidade</p>
        <div style="margin: 8px 0; padding: 6px; background: #2ecc71; border-radius: 3px; text-align: center;"><b>Muito Baixo</b></div>
        <div style="margin: 8px 0; padding: 6px; background: #27ae60; border-radius: 3px; text-align: center;"><b>Baixo</b></div>
        <div style="margin: 8px 0; padding: 6px; background: #f39c12; border-radius: 3px; text-align: center;"><b>Médio</b></div>
        <div style="margin: 8px 0; padding: 6px; background: #e67e22; border-radius: 3px; text-align: center;"><b>Alto</b></div>
        <div style="margin: 8px 0; padding: 6px; background: #e74c3c; border-radius: 3px; text-align: center;"><b>Muito Alto</b></div>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda))
    
    return mapa

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa do Município")
    mapa = criar_mapa()
    if mapa:
    folium_static(mapa, width=900, height=600)

with col2:
    st.markdown("#### 📊 Informações")
    st.info("""
    **Características:**
    
    ✅ Fundo escuro fora do município  
    ✅ Cores por nível de criminalidade  
    ✅ Apenas Rio de Janeiro visível
    
    🟢 Verde = Baixa  
    🟡 Laranja = Média  
    🔴 Vermelho = Alta
    """)

st.markdown("---")
st.markdown("<p style='text-align: center;'>Município do Rio de Janeiro</p>", unsafe_allow_html=True)
