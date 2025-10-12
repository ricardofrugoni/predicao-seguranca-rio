import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Rio de Janeiro", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")

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
                    if 'nome' in gdf.columns:
                        gdf['nome_zona'] = gdf['nome']
                    else:
                        gdf['nome_zona'] = [f'Zona {i+1}' for i in range(len(gdf))]
                    return gdf
        except:
            continue
    return None

cores_zonas = {
    'Zona Norte': '#E57373',
    'Zona Sul': '#FFD54F',
    'Zona Oeste': '#81C784',
    'Centro': '#64B5F6'
}

def get_cor_zona(nome):
    for key in cores_zonas:
        if key.lower() in nome.lower():
            return cores_zonas[key]
    return '#90A4AE'

gdf = load_data()

if gdf is None:
    st.error("Dados não encontrados")
else:
    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    m = folium.Map(
        location=center,
        zoom_start=10,
        tiles='CartoDB positron',
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False,
        doubleClickZoom=False,
        attributionControl=False
    )
    
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
        folium.GeoJson(
        gdf,
        style_function=lambda f: {
            'fillColor': get_cor_zona(f['properties'].get('nome_zona', '')),
            'fillOpacity': 0.7,
            'color': 'white',
            'weight': 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_zona'],
            aliases=['Zona:']
        )
    ).add_to(m)
    
    st_folium(m, width=1200, height=700)
    
    st.markdown("---")
    st.markdown("### Divisão por Zonas")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div style="background:#E57373;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA NORTE</div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:#FFD54F;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA SUL</div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:#81C784;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA OESTE</div>', unsafe_allow_html=True)
    c4.markdown('<div style="background:#64B5F6;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">CENTRO</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Mapa das Zonas do Município do Rio de Janeiro")
