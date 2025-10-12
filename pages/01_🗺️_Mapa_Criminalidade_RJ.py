import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa RJ", page_icon="🗺️", layout="wide")
st.title("🗺️ Criminalidade - Município do Rio de Janeiro")
st.warning("⚠️ APENAS o município do Rio de Janeiro")

CORES = {
    "Muito Baixo": "#27ae60",
    "Baixo": "#2ecc71", 
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

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

def criar_mapa_estatico(gdf):
    if 'cor' not in gdf.columns:
        gdf['cor'] = gdf['nivel'].map(CORES) if 'nivel' in gdf.columns else '#95a5a6'
    gdf['cor'].fillna('#95a5a6', inplace=True)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    for idx, row in gdf.iterrows():
        gdf[gdf.index == idx].plot(
            ax=ax,
            color=row['cor'],
            edgecolor='white',
            linewidth=2,
            alpha=0.9
        )
        
        centroid = row.geometry.centroid
        nome = row.get('nome', '')
        nivel = row.get('nivel', '')
        ax.text(
            centroid.x, centroid.y,
            f"{nome}\n{nivel}",
            fontsize=10,
            ha='center',
            va='center',
            color='white',
            weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor='none')
        )
    
    ax.axis('off')
    ax.set_xlim([gdf.total_bounds[0] - 0.05, gdf.total_bounds[2] + 0.05])
    ax.set_ylim([gdf.total_bounds[1] - 0.05, gdf.total_bounds[3] + 0.05])
    
    plt.tight_layout(pad=0)
    return fig

c1, c2 = st.columns([4, 1])

with c1:
    st.markdown("### 📍 Mapa do Município")
    gdf = carregar_geojson()
    if gdf is None:
        st.error("❌ Dados não encontrados")
    else:
        fig = criar_mapa_estatico(gdf)
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.caption(f"📊 {len(gdf)} zonas mapeadas")

with c2:
    st.markdown("### 🎨 Legenda")
    for n, c in CORES.items():
        st.markdown(
            f'<div style="background:{c};color:white;padding:10px;margin:5px 0;'
            f'border-radius:4px;text-align:center;font-weight:bold;font-size:12px;">{n}</div>',
            unsafe_allow_html=True
        )
    st.markdown("---")
    st.markdown("### ℹ️ Info")
    st.info("✅ Apenas município\n✅ Sem áreas adjacentes\n✅ Fundo escuro\n✅ Limites reais")

st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#888;font-size:13px;">'
    'Município do Rio de Janeiro - Mapa de Criminalidade por Zona'
    '</p>',
    unsafe_allow_html=True
)
