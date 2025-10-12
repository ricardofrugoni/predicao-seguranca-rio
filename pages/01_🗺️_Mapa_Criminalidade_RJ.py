import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import numpy as np

st.set_page_config(page_title="Mapa Criminalidade RJ", page_icon="🗺️", layout="wide")
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
                    if 'nome' in gdf.columns:
                        gdf['nome_zona'] = gdf['nome']
                    else:
                        gdf['nome_zona'] = ['Zona Norte', 'Zona Sul', 'Zona Oeste', 'Centro'][:len(gdf)]
                    
                    dados_crime = {
                        'Zona Norte': {'total': 18543, 'roubo': 6234, 'furto': 5421, 'homicidio': 312, 'trafico': 6576, 'taxa': 75},
                        'Zona Sul': {'total': 8932, 'roubo': 3421, 'furto': 4123, 'homicidio': 87, 'trafico': 1301, 'taxa': 35},
                        'Zona Oeste': {'total': 22134, 'roubo': 7543, 'furto': 6234, 'homicidio': 523, 'trafico': 7834, 'taxa': 85},
                        'Centro': {'total': 5234, 'roubo': 2134, 'furto': 2543, 'homicidio': 234, 'trafico': 323, 'taxa': 65}
                    }
                    
                    for idx, row in gdf.iterrows():
                        nome = row['nome_zona']
                        for zona_key in dados_crime:
                            if zona_key.lower() in nome.lower():
                                for key, val in dados_crime[zona_key].items():
                                    gdf.at[idx, key] = val
                                break
                    
                    return gdf
        except:
            continue
    return None

def get_cor_crime(taxa):
    if taxa < 30:
        return '#2ECC71'
    elif taxa < 50:
        return '#F1C40F'
    elif taxa < 70:
        return '#E67E22'
    else:
        return '#E74C3C'

gdf = load_data()

if gdf is None:
    st.error("Dados não encontrados")
else:
    bounds = gdf.total_bounds
    centro = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    mapa = folium.Map(location=centro, zoom_start=11, tiles=None, dragging=False, scrollWheelZoom=False, zoomControl=False, doubleClickZoom=False, attributionControl=False)
    
    folium.TileLayer(tiles='OpenStreetMap', name='Base', overlay=False, control=False, opacity=0.3, attr='OpenStreetMap').add_to(mapa)
    
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': get_cor_crime(feature['properties'].get('taxa', 50)),
            'fillOpacity': 1.0,
            'color': 'white',
            'weight': 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_zona', 'total', 'roubo', 'furto', 'homicidio', 'trafico', 'taxa'],
            aliases=['Zona:', 'Total de Crimes:', 'Roubos:', 'Furtos:', 'Homicídios:', 'Tráfico:', 'Taxa (/100k hab):'],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
                font-size: 14px;
                padding: 10px;
            """
        )
    ).add_to(mapa)
    
    st_folium(mapa, width=1400, height=800)
    
    st.markdown("---")
    st.markdown("### Legenda - Níveis de Criminalidade")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div style="background:#2ECC71;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">BAIXO<br><small>< 30</small></div>', unsafe_allow_html=True)
    col2.markdown('<div style="background:#F1C40F;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">MÉDIO<br><small>30-50</small></div>', unsafe_allow_html=True)
    col3.markdown('<div style="background:#E67E22;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ALTO<br><small>50-70</small></div>', unsafe_allow_html=True)
    col4.markdown('<div style="background:#E74C3C;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">MUITO ALTO<br><small>> 70</small></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Dados Detalhados por Zona")
    
    for idx, row in gdf.iterrows():
        nome = row['nome_zona']
        taxa = row.get('taxa', 0)
        total = row.get('total', 0)
        cor = get_cor_crime(taxa)
        
        with st.expander(f"📍 {nome} - Taxa: {taxa}/100k hab"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de Crimes", f"{int(total):,}")
            c2.metric("Roubos", f"{int(row.get('roubo', 0)):,}")
            c3.metric("Furtos", f"{int(row.get('furto', 0)):,}")
            c4.metric("Homicídios", f"{int(row.get('homicidio', 0)):,}")

st.markdown("---")
st.caption("Dados simulados baseados em estatísticas do ISP-RJ | Apenas o Município do Rio de Janeiro")
