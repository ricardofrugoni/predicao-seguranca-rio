import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Mapa Rio de Janeiro", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")

@st.cache_data
def load_data():
    paths = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson")
    ]
    for p in paths:
        try:
            if p.exists():
                gdf = gpd.read_file(p)
                if not gdf.empty:
                    if 'nome' in gdf.columns:
                        gdf['nome_zona'] = gdf['nome']
                    else:
                        gdf['nome_zona'] = ['Zona Norte', 'Zona Sul', 'Zona Oeste', 'Centro'][:len(gdf)]
                    return gdf
        except:
            continue
    return None

cores = {
    'Zona Norte': '#E57373',
    'Zona Sul': '#FFD54F',
    'Zona Oeste': '#81C784',
    'Centro': '#64B5F6'
}

def get_cor(nome):
    for key in cores:
        if key.lower() in nome.lower():
            return cores[key]
    return '#B0BEC5'

gdf = load_data()

if gdf is None:
    st.error("Dados não encontrados")
else:
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    fig.patch.set_facecolor('#F5F5F5')
    ax.set_facecolor('#F5F5F5')
    
    for idx, row in gdf.iterrows():
        nome = row.get('nome_zona', '')
        cor = get_cor(nome)
        gdf[gdf.index == idx].plot(ax=ax, color=cor, edgecolor='white', linewidth=2.5, alpha=0.8)
        
        if row.geometry.geom_type == 'Polygon':
            centroid = row.geometry.centroid
        else:
            largest = max(row.geometry.geoms, key=lambda p: p.area)
            centroid = largest.centroid
        
        ax.text(centroid.x, centroid.y, nome.upper(), fontsize=11, ha='center', va='center', 
                color='#333', weight='bold', bbox=dict(boxstyle='round,pad=0.5', 
                facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax.axis('off')
    bounds = gdf.total_bounds
    margin = 0.05
    ax.set_xlim([bounds[0] - margin, bounds[2] + margin])
    ax.set_ylim([bounds[1] - margin, bounds[3] + margin])
    
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
    plt.close('all')
    
    st.markdown("---")
    st.markdown("### Divisão por Zonas")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div style="background:#E57373;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA NORTE</div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:#FFD54F;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA SUL</div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:#81C784;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">ZONA OESTE</div>', unsafe_allow_html=True)
    c4.markdown('<div style="background:#64B5F6;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;">CENTRO</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Mapa Estático - Município do Rio de Janeiro")
