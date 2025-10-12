import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path

st.set_page_config(page_title="Mapa Criminalidade", page_icon="🗺️", layout="wide")

# Título
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")

# Carregar dados
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
                    # Converter taxa de criminalidade baseada no nível
                    nivel_para_taxa = {
                        "Muito Baixo": 15,
                        "Baixo": 25,
                        "Médio": 45,
                        "Alto": 65,
                        "Muito Alto": 85
                    }
                    
                    if 'nivel' in gdf.columns:
                        gdf['taxa_criminalidade'] = gdf['nivel'].map(nivel_para_taxa)
                    else:
                        gdf['taxa_criminalidade'] = 50
                    
                    if 'nome' in gdf.columns:
                        gdf['nome_bairro'] = gdf['nome']
                    else:
                        gdf['nome_bairro'] = [f'Zona {i+1}' for i in range(len(gdf))]
                    
                    return gdf
        except Exception as e:
            continue
    return None

gdf = load_data()

if gdf is None:
    st.error("❌ Não foi possível carregar os dados geográficos")
    st.info("Execute: python scripts/criar_geojson_realista_municipio.py")
else:
    # Função de cores OBRIGATÓRIA - mapeia criminalidade para cores
    def get_color(valor_criminalidade):
        """Retorna cor baseada no nível de criminalidade"""
        if valor_criminalidade < 20:
            return '#2ecc71'  # Verde - baixa
        elif valor_criminalidade < 40:
            return '#f1c40f'  # Amarelo - média
        elif valor_criminalidade < 60:
            return '#e67e22'  # Laranja - alta
        else:
            return '#e74c3c'  # Vermelho - muito alta
    
    # Criar mapa COM tiles (mapa base)
    mapa = folium.Map(
        location=[-22.9068, -43.1729],  # Centro do Rio
        zoom_start=11,
        tiles='CartoDB positron',  # MAPA BASE - mostra ruas e geografia
        dragging=False,
        scrollWheelZoom=False,
        zoomControl=False,
        doubleClickZoom=False
    )
    
    # Adicionar GeoJSON COM cores dinâmicas
        folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': get_color(feature['properties']['taxa_criminalidade']),  # COR DINÂMICA
            'fillOpacity': 0.8,  # 80% opaco para ver o mapa base
            'color': 'white',  # Borda branca
            'weight': 1.5,  # Espessura da borda
            'dashArray': '0'
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nome_bairro', 'taxa_criminalidade'],
            aliases=['Área:', 'Taxa de Criminalidade:'],
            sticky=True
            )
        ).add_to(mapa)
    
    # Renderizar
    st_folium(mapa, width=1200, height=700, returned_objects=[])
    
    # Legenda com escala de cores
    st.markdown("---")
    st.markdown("### 📊 Legenda de Criminalidade")
    
    col1, col2, col3, col4 = st.columns(4)

with col1:
        st.markdown('''
        <div style="background:#2ecc71;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            🟢 BAIXA<br><small>< 20</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background:#f1c40f;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            🟡 MÉDIA<br><small>20 - 40</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="background:#e67e22;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            🟠 ALTA<br><small>40 - 60</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div style="background:#e74c3c;padding:15px;border-radius:8px;text-align:center;color:white;font-weight:bold;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            🔴 MUITO ALTA<br><small>> 60</small>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Estatísticas por área
    st.markdown("### 📈 Dados por Área")
    
    for idx, row in gdf.iterrows():
        nome = row['nome_bairro']
        taxa = row['taxa_criminalidade']
        cor = get_color(taxa)
        
        st.markdown(f'''
        <div style="background:{cor};padding:10px;margin:5px 0;border-radius:5px;color:white;font-weight:bold;display:flex;justify-content:space-between;">
            <span>{nome}</span>
            <span>Taxa: {taxa}</span>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("Mapa de Criminalidade - Município do Rio de Janeiro | Mapa base: CartoDB Positron")
