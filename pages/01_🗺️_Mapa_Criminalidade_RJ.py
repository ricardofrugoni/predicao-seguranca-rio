import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Município do Rio de Janeiro")

def carregar_dados():
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
        except Exception as e:
            continue
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
        titulo = f'Mapa dos {len(gdf)} bairros'
    elif len(gdf) > 4:
        titulo = f'Mapa das {len(gdf)} divisões'
    else:
        titulo = f'Mapa das {len(gdf)} zonas principais'
    
    ax.set_title(titulo, fontsize=16, weight='bold', pad=20, color='#333')
    plt.tight_layout()
    return fig

st.markdown("### 📍 Mapa do Município")

gdf = carregar_dados()

if gdf is None:
    st.error("❌ Dados geográficos não encontrados")
    st.code("""
    Para corrigir:
    1. Verifique se o arquivo existe em: data/shapefiles/
    2. Execute: python scripts/criar_geojson_realista_municipio.py
    """)
else:
    try:
        fig = criar_mapa(gdf)
        st.pyplot(fig)
        plt.close()
        
        st.success(f"✅ Mapa carregado: {len(gdf)} divisões")
    except Exception as e:
        st.error(f"❌ Erro ao criar mapa: {str(e)}")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Município", "Rio de Janeiro")
with col2:
    st.metric("Estado", "Rio de Janeiro")
with col3:
    if gdf is not None:
        st.metric("Divisões", len(gdf))

st.markdown("---")
st.caption("Mapa geográfico - Município do Rio de Janeiro")
