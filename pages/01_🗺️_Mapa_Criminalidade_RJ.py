import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Município do Rio de Janeiro")
st.warning("⚠️ Mapa estático - Apenas o município do Rio de Janeiro")

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

def criar_mapa_estatico():
    geo = carregar_geojson()
    if not geo:
        st.error("GeoJSON não encontrado")
        return None
    
    fig = go.Figure()
    
    # Adicionar cada área como um polígono preenchido
    for feature in geo.get('features', []):
        nivel = feature['properties'].get('nivel', 'Médio')
        nome = feature['properties'].get('nome', '')
        cor = CORES.get(nivel, '#f39c12')
        
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            coords = geom['coordinates'][0]
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            
            fig.add_trace(go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode='lines',
                fill='toself',
                fillcolor=cor,
                line=dict(width=1, color='black'),
                name=nome,
                hovertemplate=f"<b>{nome}</b><br>Nível: {nivel}<extra></extra>",
                showlegend=False
            ))
    
    # Configurar layout - mapa estático focado no Rio
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            center=dict(lat=-22.9068, lon=-43.4200),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        showlegend=False,
        hovermode='closest',
        dragmode=False  # Desabilitar arrastar
    )
    
    return fig

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa Estático do Município")
    fig = criar_mapa_estatico()
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

with col2:
    st.markdown("#### 📊 Legenda")
    st.markdown("**Níveis de Criminalidade:**")
    for nivel, cor in CORES.items():
        st.markdown(f'<div style="background:{cor};padding:8px;margin:5px 0;border-radius:3px;text-align:center;color:white;font-weight:bold;">{nivel}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("🗺️ **Mapa Estático**\n\n✅ Apenas município\n✅ Não interativo\n✅ Áreas preenchidas")

st.markdown("---")
st.markdown("<p style='text-align:center;'>Município do Rio de Janeiro - Mapa Estático por Nível de Criminalidade</p>", unsafe_allow_html=True)
