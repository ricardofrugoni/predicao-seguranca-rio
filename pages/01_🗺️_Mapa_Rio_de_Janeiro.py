import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

st.set_page_config(page_title="Mapa Rio de Janeiro", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa do Município do Rio de Janeiro")
st.markdown("### Divisão Territorial por Bairros")

@st.cache_data
def carregar_mapa():
    caminhos = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio_limites_reais.geojson",
        Path("data/shapefiles/zonas_rio_limites_reais.geojson")
    ]
    for caminho in caminhos:
        if caminho.exists():
            gdf = gpd.read_file(caminho)
            if not gdf.empty:
                if 'nome' in gdf.columns:
                    gdf['zona'] = gdf['nome']
                else:
                    gdf['zona'] = ['Zona Norte', 'Zona Sul', 'Zona Oeste', 'Centro'][:len(gdf)]
                return gdf
    return None

cores_pastel = [
    '#FFB6C1', '#FFE4B5', '#E0BBE4', '#B4D7A8', '#A8DADC', '#F4A6B5',
    '#D4A5A5', '#FFD4A3', '#C9E4CA', '#A3C1DA', '#F8C8DC', '#E4C1F9',
    '#B5EAD7', '#FFD6BA', '#C7CEEA', '#FFDAC1', '#E2F0CB', '#B5B8D3',
    '#FFB3BA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#F0E68C', '#DDA0DD'
]

dados = carregar_mapa()

if dados is None:
    st.error("Não foi possível carregar o mapa")
else:
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    fig.patch.set_facecolor('#F5F5F5')
    ax.set_facecolor('#F5F5F5')
    
    np.random.seed(42)
    for idx, row in dados.iterrows():
        cor = np.random.choice(cores_pastel)
        dados[dados.index == idx].plot(ax=ax, color=cor, edgecolor='white', linewidth=2, alpha=0.9)
        
        if row.geometry.geom_type == 'Polygon':
            centroid = row.geometry.centroid
        else:
            largest = max(row.geometry.geoms, key=lambda p: p.area)
            centroid = largest.centroid
        
        nome = row.get('zona', f'Área {idx+1}')
        ax.text(centroid.x, centroid.y, nome.upper(), fontsize=11, ha='center', va='center',
                color='#333', weight='bold', bbox=dict(boxstyle='round,pad=0.4',
                facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax.axis('off')
    bounds = dados.total_bounds
    ax.set_xlim([bounds[0] - 0.03, bounds[2] + 0.03])
    ax.set_ylim([bounds[1] - 0.03, bounds[3] + 0.03])
    
    ax.set_title('Mapa do Município do Rio de Janeiro', fontsize=20, weight='bold', pad=20, color='#333')
    
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
    plt.close('all')
    
    st.markdown("---")
    st.info(f"📍 **{len(dados)}** divisões territoriais no município do Rio de Janeiro")

st.markdown("---")
st.caption("Mapa Geográfico - Município do Rio de Janeiro")
