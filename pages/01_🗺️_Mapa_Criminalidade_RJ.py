import streamlit as st
from pathlib import Path
import requests
from PIL import Image
import io

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa dos Bairros do Rio de Janeiro")

# URL da imagem do shapefile dos bairros do Rio
IMAGE_URL = "https://raw.githubusercontent.com/codigourbano/sidra-ibge/master/rio-de-janeiro/bairros.png"

# URLs alternativas
IMAGE_URLS = [
    "https://i.imgur.com/YourImageID.png",  # Placeholder
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Bairros_do_Rio_de_Janeiro.svg/1200px-Bairros_do_Rio_de_Janeiro.svg.png",
]

st.markdown("### 📍 Shapefile dos bairros da cidade do Rio de Janeiro")

# Tentar baixar imagem
image_loaded = False

for url in [IMAGE_URL] + IMAGE_URLS:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            st.image(img, use_column_width=True)
            image_loaded = True
            st.success("✅ Imagem oficial dos bairros do Rio de Janeiro")
            break
    except:
        continue

# Se não conseguir baixar, usar o mapa local
if not image_loaded:
    st.info("📥 Carregando mapa local dos bairros...")
    
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings('ignore')
    
    def carregar_bairros():
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
    
    def criar_mapa():
        gdf = carregar_bairros()
        if gdf is None:
            return None
            
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
        
        ax.set_title(
            titulo,
            fontsize=16,
            weight='bold',
            pad=20,
            color='#333'
        )
        
        plt.tight_layout()
        return fig
    
    fig = criar_mapa()
    if fig:
        st.pyplot(fig, use_container_width=True)
        plt.close()
    else:
        st.error("❌ Não foi possível carregar o mapa")

st.markdown("---")
st.markdown("#### 📝 Sobre o Mapa")
st.info("""
Este é o mapa geográfico do município do Rio de Janeiro mostrando suas divisões territoriais.

- **Município:** Rio de Janeiro
- **Estado:** Rio de Janeiro  
- **Visualização:** Apenas o município, sem áreas adjacentes
""")

st.markdown("---")
st.caption("Mapa geográfico - Município do Rio de Janeiro")
