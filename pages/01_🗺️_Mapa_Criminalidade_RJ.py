"""
🗺️ MAPA CHOROPLETH - CRIMINALIDADE DO MUNICÍPIO DO RIO
======================================================

Mapa APENAS do município do Rio de Janeiro.
Fundo escuro, áreas pintadas completamente.
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

st.title("🗺️ Mapa de Criminalidade - Município do Rio de Janeiro")
st.markdown("### Intensidade Criminal por Região")
st.warning("⚠️ **ATENÇÃO:** Este mapa exibe APENAS o município do Rio de Janeiro. As áreas externas aparecem escuras.")

# Cores por nível
cores_nivel = {
    "Muito Baixo": "#2ecc71",
    "Baixo": "#27ae60", 
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

def carregar_geojson():
    """Carrega GeoJSON das áreas"""
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "areas_detalhadas_rio.geojson",
        Path("data/shapefiles/areas_detalhadas_rio.geojson"),
        Path("projeto_violencia_rj/data/shapefiles/areas_detalhadas_rio.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_realista.geojson",
        Path("data/shapefiles/zonas_rio_realista.geojson"),
    ]
    
    for caminho in caminhos:
        try:
            if caminho.exists():
                with open(caminho, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            continue
    return None

def carregar_limite_municipal():
    """Carrega limite do município"""
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "limite_municipal_ibge.geojson",
        Path("data/shapefiles/limite_municipal_ibge.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "limite_municipal_rio.geojson",
        Path("data/shapefiles/limite_municipal_rio.geojson"),
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
    """Cria mapa focado apenas no município"""
    
    geojson_areas = carregar_geojson()
    limite_municipal = carregar_limite_municipal()
    
    if not geojson_areas:
        st.error("❌ GeoJSON das áreas não encontrado!")
        return None
    
    # Criar mapa com tiles escuro
    mapa = folium.Map(
        location=[-22.9068, -43.4200],
        zoom_start=11,
        tiles='CartoDB dark_matter',  # Fundo escuro
        min_zoom=10,
        max_zoom=14,
        max_bounds=True
    )
    
    # Adicionar limite municipal (borda do município)
    if limite_municipal:
        folium.GeoJson(
            limite_municipal,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': '#ffffff',
                'weight': 3,
                'fillOpacity': 0
            }
        ).add_to(mapa)
    
    # Adicionar cada área com preenchimento completo
    for feature in geojson_areas.get('features', []):
        nivel = feature['properties'].get('nivel', 'Médio')
        nome = feature['properties'].get('nome', '')
        cor = cores_nivel.get(nivel, '#f39c12')
        
        folium.GeoJson(
            feature,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': cor,  # Mesma cor da borda
                'weight': 0.5,
                'fillOpacity': 0.9,  # Quase opaco para parecer pintura
                'opacity': 0.9
            },
            highlight_function=lambda x: {
                'fillOpacity': 1.0,
                'weight': 2
            },
            tooltip=folium.Tooltip(f"<b>{nome}</b><br>Nível: {nivel}")
        ).add_to(mapa)
    
    # Legenda
    legenda = '''
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px;
                background-color: rgba(0, 0, 0, 0.8); z-index:9999; padding: 15px;
                border: 2px solid white; border-radius: 5px; color: white;">
        <p style="margin:0; font-weight: bold; font-size: 16px; text-align: center;">
            Nível de Criminalidade
        </p>
        <div style="margin: 10px 0; padding: 8px; background-color: #2ecc71; 
                    border-radius: 3px; text-align: center;">
            <b>Muito Baixo</b>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #27ae60; 
                    border-radius: 3px; text-align: center;">
            <b>Baixo</b>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #f39c12; 
                    border-radius: 3px; text-align: center;">
            <b>Médio</b>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #e67e22; 
                    border-radius: 3px; text-align: center;">
            <b>Alto</b>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #e74c3c; 
                    border-radius: 3px; text-align: center;">
            <b>Muito Alto</b>
        </div>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda))
    
    return mapa

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa do Município do Rio de Janeiro")
    st.info("💡 **Nota:** Fundo escuro indica áreas fora do município. Apenas o Rio de Janeiro é exibido.")
    
    mapa = criar_mapa()
    if mapa:
    folium_static(mapa, width=900, height=600)
    else:
        st.error("Erro ao carregar o mapa")
        st.code("python scripts/buscar_dados_oficiais_rio.py")

with col2:
    st.markdown("#### 📊 Informações")
    
    st.markdown("""
    **🗺️ Características do Mapa:**
    
    ✅ Apenas município do Rio  
    ✅ Fundo escuro fora do município  
    ✅ Áreas pintadas por intensidade  
    ✅ Cores sólidas (não transparentes)
    
    **📍 Regiões Incluídas:**
    - Zona Sul (verde)
    - Centro (laranja)
    - Zona Norte (laranja/vermelho)
    - Zona Oeste (vermelho)
    """)
    
    st.markdown("---")
    
    st.markdown("#### 🎨 Legenda Rápida")
    st.markdown("""
    🟢 **Verde** - Baixa criminalidade  
    🟡 **Laranja** - Média criminalidade  
    🔴 **Vermelho** - Alta criminalidade
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p><b>Município do Rio de Janeiro</b></p>
    <p>Mapa com fundo escuro mostrando apenas as áreas do município</p>
    <p><small>Áreas escuras = Fora do município (Baixada Fluminense, Niterói, etc.)</small></p>
</div>
""", unsafe_allow_html=True)
