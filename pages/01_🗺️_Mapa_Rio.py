import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Criminalidade Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Criminalidade no Município do Rio de Janeiro")

@st.cache_data
def carregar():
    p1 = Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson"
    p2 = Path("data/shapefiles/zonas_rio_limites_reais.geojson")
    for p in [p1, p2]:
        if p.exists():
            gdf = gpd.read_file(p)
            if not gdf.empty:
                if 'nome' in gdf.columns:
                    gdf['zona'] = gdf['nome']
                else:
                    gdf['zona'] = ['Zona Norte', 'Zona Sul', 'Zona Oeste', 'Centro'][:len(gdf)]
                dados = {'Zona Norte': 75, 'Zona Sul': 35, 'Zona Oeste': 85, 'Centro': 65}
                gdf['taxa'] = gdf['zona'].map(dados)
                return gdf
    return None

def cor(t):
    if t < 40:
        return '#2ECC71'
    if t < 60:
        return '#F1C40F'
    if t < 75:
        return '#E67E22'
    return '#E74C3C'

dados = carregar()

if dados is None:
    st.error("Dados não encontrados")
    st.info("Arquivo GeoJSON não localizado")
else:
    b = dados.total_bounds
    c = [(b[1] + b[3]) / 2, (b[0] + b[2]) / 2]
    
    m = folium.Map(
        location=c,
        zoom_start=11,
        tiles='OpenStreetMap',
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False,
        doubleClickZoom=False,
        attributionControl=False
    )
    
    m.fit_bounds([[b[1], b[0]], [b[3], b[2]]])
    
    folium.GeoJson(
        dados,
        style_function=lambda x: {
            'fillColor': cor(x['properties']['taxa']),
            'fillOpacity': 0.65,
            'color': 'white',
            'weight': 2
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['zona', 'taxa'],
            aliases=['Região:', 'Taxa/100k hab:'],
            sticky=True
        )
    ).add_to(m)
    
    st_folium(m, width=1400, height=800)
    
    st.markdown("---")
    st.markdown("### Níveis de Criminalidade")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div style="background:#2ECC71;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">BAIXO<br>Zona Sul (35)</div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:#F1C40F;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">MÉDIO<br>Centro (65)</div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:#E67E22;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ALTO<br>Z. Norte (75)</div>', unsafe_allow_html=True)
    c4.markdown('<div style="background:#E74C3C;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">CRÍTICO<br>Z. Oeste (85)</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("As manchas respeitam os limites geográficos do município | OpenStreetMap")
