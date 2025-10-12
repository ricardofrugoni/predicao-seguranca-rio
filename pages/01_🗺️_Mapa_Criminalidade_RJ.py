import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")

def carregar_dados():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "bairros_rio_oficial.geojson",
        Path("data/shapefiles/bairros_rio_oficial.geojson"),
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

def criar_mapa(gdf):
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    gdf.plot(
        ax=ax,
        color='#d4b5b5',
        edgecolor='#5a4a4a',
        linewidth=0.8,
        alpha=0.85
    )
    
    ax.axis('off')
    ax.set_xlim([gdf.total_bounds[0] - 0.02, gdf.total_bounds[2] + 0.02])
    ax.set_ylim([gdf.total_bounds[1] - 0.02, gdf.total_bounds[3] + 0.02])
    
    if len(gdf) > 20:
        titulo = f'Shapefile dos {len(gdf)} bairros da cidade do Rio de Janeiro'
    elif len(gdf) > 4:
        titulo = f'Mapa com {len(gdf)} divisões do município do Rio de Janeiro'
    else:
        titulo = f'Mapa das {len(gdf)} zonas principais do Rio de Janeiro'
    
    ax.set_title(titulo, fontsize=16, weight='bold', pad=20, color='#333')
    plt.tight_layout()
    return fig

gdf = carregar_dados()

if gdf is None:
    st.error("❌ Dados geográficos não encontrados")
    st.info("Execute: `python scripts/baixar_shapefile_oficial_data_rio.py`")
else:
    fig = criar_mapa(gdf)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Divisões", len(gdf))
    with col2:
        st.metric("Município", "Rio de Janeiro")
    with col3:
        st.metric("Estado", "RJ")

st.markdown("---")
st.caption("Mapa geográfico - Município do Rio de Janeiro")
