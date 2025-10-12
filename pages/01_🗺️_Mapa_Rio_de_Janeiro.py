import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Rio de Janeiro", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")

@st.cache_data
def carregar_mapa():
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson")
    ]
    for caminho in caminhos:
        if caminho.exists():
            gdf = gpd.read_file(caminho)
            if not gdf.empty:
                if 'nome' in gdf.columns:
                    gdf['zona'] = gdf['nome']
                else:
                    gdf['zona'] = ['Zona Norte', 'Zona Sul', 'Zona Oeste', 'Centro'][:len(gdf)]
                return gdf
    return None

cores_zona = {
    'zona norte': '#E8B4B8',
    'zona sul': '#FFE4A3',
    'zona oeste': '#B4D3B2',
    'centro': '#A8C5DD'
}

def get_cor_zona(nome):
    nome_lower = nome.lower()
    for chave, cor in cores_zona.items():
        if chave in nome_lower:
            return cor
    return '#D3D3D3'

dados = carregar_mapa()

if dados is None:
    st.error("Não foi possível carregar o mapa")
    st.info("Arquivo GeoJSON não encontrado")
else:
    limites = dados.total_bounds
    centro = [(limites[1] + limites[3]) / 2, (limites[0] + limites[2]) / 2]
    
    mapa = folium.Map(
        location=centro,
        zoom_start=11,
        tiles='OpenStreetMap',
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False,
        doubleClickZoom=False,
        attributionControl=False
    )
    
    mapa.fit_bounds([[limites[1], limites[0]], [limites[3], limites[2]]])
    
    folium.GeoJson(
        dados,
        style_function=lambda feature: {
            'fillColor': get_cor_zona(feature['properties'].get('zona', '')),
            'fillOpacity': 0.6,
            'color': 'white',
            'weight': 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['zona'],
            aliases=['Região:'],
            sticky=True
        )
    ).add_to(mapa)
    
    st_folium(mapa, width=1400, height=800)
    
    st.markdown("---")
    st.markdown("### Divisão Territorial do Município")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.markdown(
        '<div style="background:#E8B4B8;padding:20px;border-radius:10px;text-align:center;color:#333;font-weight:bold;font-size:16px;">ZONA NORTE</div>',
        unsafe_allow_html=True
    )
    
    col2.markdown(
        '<div style="background:#FFE4A3;padding:20px;border-radius:10px;text-align:center;color:#333;font-weight:bold;font-size:16px;">ZONA SUL</div>',
        unsafe_allow_html=True
    )
    
    col3.markdown(
        '<div style="background:#B4D3B2;padding:20px;border-radius:10px;text-align:center;color:#333;font-weight:bold;font-size:16px;">ZONA OESTE</div>',
        unsafe_allow_html=True
    )
    
    col4.markdown(
        '<div style="background:#A8C5DD;padding:20px;border-radius:10px;text-align:center;color:#333;font-weight:bold;font-size:16px;">CENTRO</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.caption("Mapa Geográfico do Município do Rio de Janeiro | OpenStreetMap")

