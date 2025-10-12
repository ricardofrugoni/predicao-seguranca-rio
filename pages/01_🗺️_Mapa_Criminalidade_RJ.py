import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Criminalidade", page_icon="🗺️", layout="wide")

# Título
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")

# Carregar dados
@st.cache_data
def load_data():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson",
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson")
    ]
    
    for p in paths:
        try:
            if p.exists():
                gdf = gpd.read_file(p)
                if not gdf.empty:
                    # Adicionar taxa de criminalidade baseada no nível
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
                    
                    # Garantir coluna nome_bairro
                    if 'nome' in gdf.columns:
                        gdf['nome_bairro'] = gdf['nome']
                    else:
                        gdf['nome_bairro'] = [f'Zona {i+1}' for i in range(len(gdf))]
                    
                    return gdf
        except:
            continue
    return None

gdf = load_data()

if gdf is None:
    st.error("❌ Não foi possível carregar os dados")
else:
    # Função para mapear cores
    def get_color(taxa):
        if taxa < 20:
            return '#2ecc71'  # Verde
        elif taxa < 40:
            return '#f1c40f'  # Amarelo
        elif taxa < 60:
            return '#e67e22'  # Laranja
        else:
            return '#e74c3c'  # Vermelho
    
    # Criar mapa
    m = folium.Map(
        location=[-22.9068, -43.1729],
        zoom_start=11,
        tiles='CartoDB positron',
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False
    )
    
    # Adicionar polígonos
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': get_color(feature['properties']['taxa_criminalidade']),
            'fillOpacity': 0.85,
            'color': 'white',
            'weight': 1.5
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_bairro', 'taxa_criminalidade'],
            aliases=['Bairro:', 'Criminalidade:']
        )
    ).add_to(m)
    
    # Exibir
    st_folium(m, width=1000, height=600)
    
    # Legenda
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div style="background:#2ecc71;padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;">Baixo (< 20)</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:#f1c40f;padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;">Médio (20-40)</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:#e67e22;padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;">Alto (40-60)</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="background:#e74c3c;padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;">Muito Alto (> 60)</div>', unsafe_allow_html=True)
