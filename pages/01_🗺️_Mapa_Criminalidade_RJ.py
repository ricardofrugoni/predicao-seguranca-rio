import streamlit as st
from pathlib import Path
import requests
from PIL import Image
import io

st.set_page_config(page_title="Mapa Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Município do Rio de Janeiro")

st.markdown("### 📍 Mapa Oficial do Município")

# URLs de mapas oficiais do Rio de Janeiro
mapas_oficiais = [
    {
        "nome": "Wikimedia - Mapa do Município RJ",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/RiodeJaneiro_MunicipioMacro.svg/1200px-RiodeJaneiro_MunicipioMacro.svg.png"
    },
    {
        "nome": "Limite Municipal - IBGE",
        "url": "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3304557?formato=image/png&qualidade=maxima&intrarregiao=municipio"
    },
    {
        "nome": "Mapa Bairros RJ",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Bairros_do_Municipio_do_Rio_de_Janeiro.svg/1280px-Bairros_do_Municipio_do_Rio_de_Janeiro.svg.png"
    }
]

mapa_carregado = False

for mapa in mapas_oficiais:
    try:
        st.info(f"Carregando: {mapa['nome']}...")
        response = requests.get(mapa['url'], timeout=15)
        
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            st.image(img, caption=f"Município do Rio de Janeiro - {mapa['nome']}", use_column_width=True)
            mapa_carregado = True
            st.success(f"✅ {mapa['nome']}")
            break
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar {mapa['nome']}")
        continue

# Se não conseguir carregar mapa externo, usar o local
if not mapa_carregado:
    st.warning("📥 Usando mapa local...")
    
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings('ignore')
    
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
                    return gpd.read_file(p)
            except:
                pass
        return None
    
    gdf = carregar_dados()
    
    if gdf is not None:
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        gdf.plot(ax=ax, color='#d4b5b5', edgecolor='#5a4a4a', linewidth=0.8, alpha=0.85)
        
        ax.axis('off')
        ax.set_xlim([gdf.total_bounds[0] - 0.02, gdf.total_bounds[2] + 0.02])
        ax.set_ylim([gdf.total_bounds[1] - 0.02, gdf.total_bounds[3] + 0.02])
        ax.set_title('Município do Rio de Janeiro', fontsize=16, weight='bold', pad=20, color='#333')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.error("❌ Não foi possível carregar nenhum mapa")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ℹ️ Informações")
    st.info("""
    **Município:** Rio de Janeiro  
    **Estado:** Rio de Janeiro  
    **Região:** Sudeste  
    **População:** ~6.7 milhões  
    **Área:** 1.200 km²
    """)

with col2:
    st.markdown("#### 🗺️ Sobre o Mapa")
    st.info("""
    Visualização geográfica do município do Rio de Janeiro.
    
    - Apenas o território municipal
    - Sem municípios adjacentes
    - Limites oficiais
    """)

st.markdown("---")
st.caption("Fonte: Dados oficiais - IBGE / Prefeitura do Rio")
