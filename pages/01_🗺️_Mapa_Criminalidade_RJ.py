import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")
st.info("📍 Visualização geográfica - Apenas o município")

def carregar_geojson():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson"),
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

def criar_mapa_municipio(gdf):
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    gdf.plot(
        ax=ax,
        color='#e8f4f8',
        edgecolor='#2c3e50',
        linewidth=1.5,
        alpha=0.7
    )
    
    for idx, row in gdf.iterrows():
        centroid = row.geometry.centroid
        nome = row.get('nome', f'Área {idx+1}')
        ax.text(
            centroid.x, centroid.y,
            nome,
            fontsize=12,
            ha='center',
            va='center',
            color='#2c3e50',
            weight='bold'
        )
    
    ax.axis('off')
    ax.set_xlim([gdf.total_bounds[0] - 0.05, gdf.total_bounds[2] + 0.05])
    ax.set_ylim([gdf.total_bounds[1] - 0.05, gdf.total_bounds[3] + 0.05])
    plt.tight_layout(pad=0)
    
    return fig

st.markdown("### 📍 Mapa do Município")

gdf = carregar_geojson()

if gdf is None:
    st.error("❌ Dados geográficos não encontrados")
    st.info("Execute o script de download dos shapefiles")
else:
    fig = criar_mapa_municipio(gdf)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Áreas Mapeadas", len(gdf))
    with col2:
        st.metric("Município", "Rio de Janeiro")
    with col3:
        st.metric("Estado", "Rio de Janeiro")

st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#7f8c8d;font-size:14px;">'
    'Mapa Geográfico do Município do Rio de Janeiro'
    '</p>',
    unsafe_allow_html=True
)
