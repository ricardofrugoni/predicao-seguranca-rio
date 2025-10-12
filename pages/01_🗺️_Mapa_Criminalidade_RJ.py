import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")
st.warning("⚠️ Mapa Estático - Apenas o município")

CORES = {"Muito Baixo": "#27ae60", "Baixo": "#2ecc71", "Médio": "#f39c12", "Alto": "#e67e22", "Muito Alto": "#e74c3c"}

def carregar_geojson():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "bairros_rio_simulado.geojson",
        Path("data/shapefiles/bairros_rio_simulado.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson",
        Path("data/shapefiles/zonas_rio.geojson")
    ]
    for p in paths:
        try:
            if p.exists():
                g = gpd.read_file(p)
                if not g.empty:
                    return g
        except:
            pass
    return None

def preparar(gdf):
    if 'cor' not in gdf.columns:
        gdf['cor'] = gdf['nivel'].map(CORES) if 'nivel' in gdf.columns else '#95a5a6'
    gdf['cor'].fillna('#95a5a6', inplace=True)
    return gdf

def criar_mapa(gdf):
    b = gdf.total_bounds
    c_lat = (b[1] + b[3]) / 2
    c_lon = (b[0] + b[2]) / 2
    m = folium.Map(location=[c_lat, c_lon], zoom_start=11, dragging=False, scrollWheelZoom=False, doubleClickZoom=False, boxZoom=False, keyboard=False, zoomControl=False, tiles='CartoDB positron')
    m.fit_bounds([[b[1], b[0]], [b[3], b[2]]])
    def style(f):
        return {'fillColor': f['properties'].get('cor', '#95a5a6'), 'color': '#000000', 'weight': 1, 'fillOpacity': 0.9, 'opacity': 1}
    campos = []
    alias = []
    if 'nome' in gdf.columns:
        campos.append('nome')
        alias.append('Área:')
    if 'nivel' in gdf.columns:
        campos.append('nivel')
        alias.append('Nível:')
    tip = folium.GeoJsonTooltip(fields=campos, aliases=alias, sticky=True) if campos else None
    folium.GeoJson(gdf, style_function=style, tooltip=tip).add_to(m)
    leg = '<div style="position:fixed;bottom:40px;right:40px;width:180px;background:white;z-index:9999;padding:12px;border:2px solid #333;border-radius:8px;"><h4 style="margin:0 0 10px 0;text-align:center;font-size:13px;">Criminalidade</h4>'
    for n, c in CORES.items():
        leg += f'<div style="margin:6px 0;padding:7px;background:{c};color:white;text-align:center;border-radius:3px;font-size:11px;font-weight:bold;">{n}</div>'
    leg += '</div>'
    m.get_root().html.add_child(folium.Element(leg))
    return m

c1, c2 = st.columns([3, 1])

with c1:
    st.markdown("#### 📍 Mapa do Município")
    gdf = carregar_geojson()
    if gdf is None:
        st.error("❌ GeoJSON não encontrado")
    else:
        gdf = preparar(gdf)
        m = criar_mapa(gdf)
        st_folium(m, width=900, height=600, returned_objects=[])
        st.caption(f"📊 Setores: {len(gdf)}")

with c2:
    st.markdown("#### 📋 Info")
    st.info("✅ Mapa Estático\n🔒 Sem zoom\n🔒 Sem arrastar\n🎨 Preenchimento completo\n🌍 Apenas município")
    st.markdown("---")
    st.markdown("#### 🎨 Legenda")
    for n, c in CORES.items():
        st.markdown(f'<div style="background:{c};color:white;padding:8px;margin:4px 0;border-radius:3px;text-align:center;font-weight:bold;font-size:12px;">{n}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#666;"><p>Município do Rio de Janeiro - Mapa de Criminalidade</p></div>', unsafe_allow_html=True)
