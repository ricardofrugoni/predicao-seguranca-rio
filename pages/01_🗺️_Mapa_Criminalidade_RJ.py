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
                    nivel_para_taxa = {
                        "Muito Baixo": 15,
                        "Baixo": 25,
                        "Médio": 45,
                        "Alto": 65,
                        "Muito Alto": 85
                    }
                    
                    if 'nivel' in gdf.columns:
                        gdf['taxa_criminalidade'] = gdf['nivel'].map(nivel_para_taxa)
                    else:
                        gdf['taxa_criminalidade'] = 50
                    
                    if 'nome' in gdf.columns:
                        gdf['nome_bairro'] = gdf['nome']
                    else:
                        gdf['nome_bairro'] = [f'Zona {i+1}' for i in range(len(gdf))]
                    
                    return gdf
        except Exception as e:
            continue
    return None

def get_color(valor_criminalidade):
    if valor_criminalidade < 20:
        return '#2ecc71'
    elif valor_criminalidade < 40:
        return '#f1c40f'
    elif valor_criminalidade < 60:
        return '#e67e22'
    else:
        return '#e74c3c'

gdf = load_data()

if gdf is None:
    st.error("Não foi possível carregar os dados geográficos")
else:
    bounds = gdf.total_bounds
    centro = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    mapa = folium.Map(
        location=centro,
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
        name='CartoDB Positron No Labels',
        overlay=False,
        control=False
    ).add_to(mapa)
    
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
        folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': get_color(feature['properties']['taxa_criminalidade']),
            'fillOpacity': 0.9,
            'color': 'white',
                'weight': 2,
            'dashArray': '0'
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_bairro', 'taxa_criminalidade'],
            aliases=['Área:', 'Taxa:'],
            sticky=True
            )
        ).add_to(mapa)
    
    st_folium(mapa, width=1200, height=700, returned_objects=[])
    
    st.markdown("---")
    st.markdown("### Legenda de Criminalidade")
    
    col1, col2, col3, col4 = st.columns(4)

with col1:
        st.markdown('<div style="background:#2ecc71;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Baixa</div>', unsafe_allow_html=True)

with col2:
        st.markdown('<div style="background:#f1c40f;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Média</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="background:#e67e22;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Alta</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div style="background:#e74c3c;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">Muito Alta</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Dados por Área")
    
    for idx, row in gdf.iterrows():
        nome = row['nome_bairro']
        taxa = row['taxa_criminalidade']
        cor = get_color(taxa)
        st.markdown(f'<div style="background:{cor};padding:10px;margin:5px 0;border-radius:5px;color:white;font-weight:bold;"><b>{nome}</b> - Taxa: {taxa}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Mapa de Criminalidade - Município do Rio de Janeiro")
