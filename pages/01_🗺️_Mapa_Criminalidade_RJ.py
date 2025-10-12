import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Criminalidade", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")

@st.cache_data
def load_data():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson")
    ]
    for p in paths:
        try:
            if p.exists():
                gdf = gpd.read_file(p)
                if not gdf.empty:
                    nivel_map = {"Muito Baixo": 15, "Baixo": 25, "Médio": 45, "Alto": 65, "Muito Alto": 85}
                    if 'nivel' in gdf.columns:
                        gdf['taxa_criminalidade'] = gdf['nivel'].map(nivel_map)
                    else:
                        gdf['taxa_criminalidade'] = 50
                    if 'nome' in gdf.columns:
                        gdf['nome_bairro'] = gdf['nome']
                    else:
                        gdf['nome_bairro'] = [f'Zona {i+1}' for i in range(len(gdf))]
                    return gdf
        except:
            continue
    return None

def get_color(val):
    if val < 20:
        return '#2ecc71'
    elif val < 40:
        return '#f1c40f'
    elif val < 60:
        return '#e67e22'
    return '#e74c3c'

gdf = load_data()

if gdf is None:
    st.error("Dados não encontrados")
else:
    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    m = folium.Map(
        location=center,
        zoom_start=10,
        tiles=None,
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False,
        doubleClickZoom=False,
        attributionControl=False
    )
    
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
        attr='CartoDB',
        overlay=False,
        control=False
    ).add_to(m)
    
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    folium.GeoJson(
        gdf,
        style_function=lambda f: {
            'fillColor': get_color(f['properties']['taxa_criminalidade']),
            'fillOpacity': 0.9,
            'color': 'white',
            'weight': 2
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_bairro', 'taxa_criminalidade'],
            aliases=['Área:', 'Taxa:']
        )
    ).add_to(m)
    
    st_folium(m, width=1200, height=700)
    
    st.markdown("---")
    st.markdown("### Legenda")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div style="background:#2ecc71;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Baixa</div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:#f1c40f;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Média</div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:#e67e22;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Alta</div>', unsafe_allow_html=True)
    c4.markdown('<div style="background:#e74c3c;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Muito Alta</div>', unsafe_allow_html=True)
