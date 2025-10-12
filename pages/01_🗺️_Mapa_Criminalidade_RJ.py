import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Município do Rio de Janeiro")

@st.cache_data
def carregar_dados():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson")
    ]
    
    for i, p in enumerate(paths):
        try:
            if p.exists():
                st.info(f"✓ Tentando carregar: {p.name}")
                g = gpd.read_file(p)
                if not g.empty:
                    st.success(f"✅ Arquivo carregado: {p.name} ({len(g)} zonas)")
                    return g
        except Exception as e:
            st.warning(f"✗ Erro em {p.name}: {str(e)[:50]}")
            continue
    
    st.error("❌ Nenhum arquivo encontrado!")
    return None

def criar_mapa(gdf):
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Plot do mapa
    gdf.plot(
        ax=ax,
        color='#d4b5b5',
        edgecolor='#5a4a4a',
        linewidth=1.5,
        alpha=0.9
    )
    
    # Labels das zonas
    for idx, row in gdf.iterrows():
        centroid = row.geometry.centroid
        nome = row.get('nome', f'Zona {idx+1}')
        ax.text(
            centroid.x, 
            centroid.y, 
            nome,
            fontsize=14,
            ha='center',
            va='center',
            weight='bold',
            color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='none')
        )
    
    ax.axis('off')
    ax.set_xlim([gdf.total_bounds[0] - 0.05, gdf.total_bounds[2] + 0.05])
    ax.set_ylim([gdf.total_bounds[1] - 0.05, gdf.total_bounds[3] + 0.05])
    
    ax.set_title(
        f'Mapa das {len(gdf)} zonas principais',
        fontsize=18,
        weight='bold',
        pad=20,
        color='#2c3e50'
    )
    
    plt.tight_layout()
    return fig

st.markdown("### 📍 Mapa do Município do Rio de Janeiro")

with st.spinner("Carregando dados geográficos..."):
    gdf = carregar_dados()

if gdf is None:
    st.error("❌ **Erro:** Não foi possível carregar o mapa")
    st.info("""
    **Possíveis soluções:**
    1. Verifique se os arquivos GeoJSON existem
    2. Execute: `python scripts/criar_geojson_realista_municipio.py`
    3. Faça commit e push dos arquivos para o GitHub
    """)
else:
    with st.spinner("Gerando visualização..."):
        try:
            fig = criar_mapa(gdf)
            st.pyplot(fig, clear_figure=True)
            plt.close('all')
        except Exception as e:
            st.error(f"❌ Erro ao gerar mapa: {str(e)}")
            st.code(str(e))

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏙️ Município", "Rio de Janeiro")
with col2:
    st.metric("📍 Estado", "RJ")
with col3:
    if gdf is not None:
        st.metric("🗺️ Zonas", len(gdf))
    else:
        st.metric("🗺️ Zonas", "N/A")

st.markdown("---")
st.caption("Mapa geográfico do município do Rio de Janeiro")
