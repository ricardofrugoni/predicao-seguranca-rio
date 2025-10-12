import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Município do Rio de Janeiro")

st.markdown("### Mapa do Município")

centro_rio = [-22.9068, -43.1729]

mapa = folium.Map(
    location=centro_rio,
    zoom_start=11,
    tiles='OpenStreetMap',
    dragging=True,
    scrollWheelZoom=True,
    zoomControl=True,
    attributionControl=True
)

limites_rio = [
    [-22.746006, -43.797142],
    [-22.746006, -43.096837],
    [-23.082741, -43.096837],
    [-23.082741, -43.797142],
    [-22.746006, -43.797142]
]

folium.Polygon(
    locations=limites_rio,
    color='red',
    weight=3,
    fill=False,
    popup='Limites do Município do Rio de Janeiro'
).add_to(mapa)

st_folium(mapa, width=1400, height=800)

st.markdown("---")
st.info("📍 Mapa interativo do Município do Rio de Janeiro")
st.caption("OpenStreetMap | Visualização Geográfica")

