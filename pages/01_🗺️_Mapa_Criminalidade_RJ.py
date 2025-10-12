import streamlit as st
import folium
import json
from pathlib import Path
from streamlit_folium import folium_static

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")
st.warning("⚠️ Apenas o município do Rio de Janeiro")

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
        Path("projeto_violencia_rj/data/shapefiles/areas_detalhadas_rio.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson",
        Path("data/shapefiles/zonas_rio.geojson")
    ]
    for c in caminhos:
        try:
            if c.exists():
                with open(c, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
    return None

def criar_mapa():
    geo = carregar_geojson()
    if not geo:
        st.error("GeoJSON não encontrado")
        return None
    
    m = folium.Map(
        location=[-22.9068, -43.4200],
        zoom_start=11,
        tiles='CartoDB dark_matter',
        min_zoom=10,
        max_zoom=14
    )
    
    for f in geo.get('features', []):
        nivel = f['properties'].get('nivel', 'Médio')
        nome = f['properties'].get('nome', '')
        cor = CORES.get(nivel, '#f39c12')
        folium.GeoJson(
            f,
            style_function=lambda x, c=cor: {'fillColor': c, 'color': c, 'weight': 0.5, 'fillOpacity': 0.9},
            tooltip=f"{nome} - {nivel}"
        ).add_to(m)
    
    leg = '<div style="position:fixed;bottom:50px;right:50px;width:200px;background:rgba(0,0,0,0.8);z-index:9999;padding:15px;border:2px solid white;border-radius:5px;color:white;"><p style="margin:0;font-weight:bold;text-align:center;">Criminalidade</p>'
    for n, c in CORES.items():
        leg += f'<div style="margin:8px 0;padding:6px;background:{c};border-radius:3px;text-align:center;"><b>{n}</b></div>'
    leg += '</div>'
    m.get_root().html.add_child(folium.Element(leg))
    return m

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("#### 📍 Mapa do Município")
    mapa = criar_mapa()
    if mapa:
        folium_static(mapa, width=900, height=600)

with col2:
    st.markdown("#### 📊 Info")
    st.info("✅ Fundo escuro\n✅ Apenas Rio\n🟢 Verde = Baixa\n🟡 Laranja = Média\n🔴 Vermelho = Alta")

st.markdown("---")
st.markdown("<p style='text-align:center;'>Município do Rio de Janeiro</p>", unsafe_allow_html=True)
