import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import json

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Município do Rio de Janeiro")
st.warning("⚠️ Mapa estático - Apenas o município do Rio de Janeiro")

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
        Path("projeto_violencia_rj/data/shapefiles/areas_detalhadas_rio.geojson",
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson",
        Path("data/shapefiles/zonas_rio.geojson")
    ]
    for c in caminhos:
        try:
            if c.exists():
                return gpd.read_file(c)
        except:
            pass
    return None

def criar_mapa_estatico():
    gdf = carregar_geojson()
    if gdf is None or gdf.empty:
        st.error("GeoJSON não encontrado")
        return None
    
    # Garantir que há coluna de cor
    if 'cor' not in gdf.columns:
        if 'nivel' in gdf.columns:
            gdf['cor'] = gdf['nivel'].map(CORES)
        else:
            gdf['cor'] = '#f39c12'
    
    # Calcular bounds do município
    bounds = gdf.total_bounds
    centro = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    # Criar mapa ESTÁTICO
    mapa = folium.Map(
        location=centro,
        zoom_start=11,
        dragging=False,
        scrollWheelZoom=False,
        doubleClickZoom=False,
        boxZoom=False,
        keyboard=False,
        zoomControl=False,
        tiles='CartoDB dark_matter'
    )
    
    # Ajustar aos limites do município
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    # Adicionar setores PREENCHIDOS
        folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': feature['properties'].get('cor', '#f39c12'),
            'color': feature['properties'].get('cor', '#f39c12'),
            'weight': 0.5,
            'fillOpacity': 0.95
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome', 'nivel'] if 'nome' in gdf.columns else [],
            aliases=['Área:', 'Nível:'],
            sticky=True
            )
        ).add_to(mapa)
    
    # Legenda
    leg = '<div style="position:fixed;bottom:50px;right:50px;width:180px;background:rgba(0,0,0,0.85);z-index:9999;padding:12px;border:2px solid white;border-radius:8px;color:white;"><p style="margin:0 0 10px 0;font-weight:bold;text-align:center;font-size:14px;">Criminalidade</p>'
    for nivel, cor in CORES.items():
        leg += f'<div style="margin:6px 0;padding:6px;background:{cor};border-radius:4px;text-align:center;font-size:12px;font-weight:bold;">{nivel}</div>'
    leg += '</div>'
    mapa.get_root().html.add_child(folium.Element(leg))
    
    return mapa

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa Estático do Município")
    mapa = criar_mapa_estatico()
    if mapa:
        st_folium(
            mapa,
            width=900,
            height=600,
            returned_objects=[]
        )

with col2:
    st.markdown("#### 📊 Características")
    st.info("""
    ✅ **Mapa Estático**
    
    🔒 Não pode arrastar
    🔒 Não pode zoom
    🔒 Não pode mover
    
    🗺️ Apenas município do Rio
    🎨 Áreas 100% preenchidas
    🌑 Fundo escuro
    """)

st.markdown("---")
    st.markdown("#### 🎨 Legenda")
    for nivel, cor in CORES.items():
        st.markdown(f'<div style="background:{cor};padding:8px;margin:5px 0;border-radius:3px;text-align:center;color:white;font-weight:bold;font-size:12px;">{nivel}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;'>Município do Rio de Janeiro - Mapa Estático de Criminalidade</p>", unsafe_allow_html=True)
