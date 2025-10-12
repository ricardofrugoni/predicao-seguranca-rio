import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa dos Bairros do Rio de Janeiro")

def carregar_bairros():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "bairros_rio_completo.geojson",
        Path("data/shapefiles/bairros_rio_completo.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "bairros_rio_simulado.geojson",
        Path("data/shapefiles/bairros_rio_simulado.geojson")
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

def criar_mapa_bairros(gdf):
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
    
    ax.set_title(
        f'Shapefile dos {len(gdf)} bairros da cidade do Rio de Janeiro',
        fontsize=16,
        weight='bold',
        pad=20,
        color='#333'
    )
    
    plt.tight_layout()
    return fig

gdf = carregar_bairros()

if gdf is None:
    st.error("❌ Dados dos bairros não encontrados")
else:
    fig = criar_mapa_bairros(gdf)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    
    st.markdown("---")
    st.info(f"📊 **{len(gdf)} bairros** mapeados no município do Rio de Janeiro")

st.markdown("---")
st.caption("Mapa geográfico dos bairros - Município do Rio de Janeiro")
