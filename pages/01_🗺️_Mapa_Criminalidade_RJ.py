import streamlit as st
import plotly.graph_objects as go
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Criminalidade - Município do Rio de Janeiro")
st.warning("⚠️ Visualização: APENAS o município do Rio")

CORES = {"Muito Baixo": "#27ae60", "Baixo": "#2ecc71", "Médio": "#f39c12", "Alto": "#e67e22", "Muito Alto": "#e74c3c"}

def carregar_geojson():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson")
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

def criar_mapa_apenas_municipio(gdf):
    if 'cor' not in gdf.columns:
        gdf['cor'] = gdf['nivel'].map(CORES) if 'nivel' in gdf.columns else '#95a5a6'
    gdf['cor'].fillna('#95a5a6', inplace=True)
    
    fig = go.Figure()
    
    for idx, row in gdf.iterrows():
        geom = row.geometry
        nome = row.get('nome', f'Área {idx+1}')
        nivel = row.get('nivel', 'N/A')
        cor = row.get('cor', '#95a5a6')
        
        if geom.geom_type == 'Polygon':
            coords = list(geom.exterior.coords)
        elif geom.geom_type == 'MultiPolygon':
            coords = list(geom.geoms[0].exterior.coords)
        else:
            continue
        
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode='lines',
            fill='toself',
            fillcolor=cor,
            line=dict(width=2, color='white'),
            name=nome,
            text=f"{nome}<br>Nível: {nivel}",
            hoverinfo='text',
            showlegend=False
        ))
    
    bounds = gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=9.5
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=700,
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a'
    )
    
    return fig

c1, c2 = st.columns([4, 1])

with c1:
    gdf = carregar_geojson()
    if gdf is None:
        st.error("❌ Dados não encontrados")
    else:
        fig = criar_mapa_apenas_municipio(gdf)
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': False, 'displayModeBar': False})

with c2:
    st.markdown("### 🎨 Legenda")
    for n, c in CORES.items():
        st.markdown(f'<div style="background:{c};color:white;padding:8px;margin:4px 0;border-radius:3px;text-align:center;font-weight:bold;font-size:11px;">{n}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.info("📍 **Apenas Município**\n\nSem municípios vizinhos\nFundo escuro\nÁreas preenchidas")

st.markdown("---")
st.markdown('<p style="text-align:center;color:#888;">Município do Rio de Janeiro</p>', unsafe_allow_html=True)
