import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa Criminalidade Rio", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de Criminalidade - Rio de Janeiro")

# Cores por nível de criminalidade
CORES_CRIMINALIDADE = {
    "Muito Baixo": "#27ae60",
    "Baixo": "#2ecc71",
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

@st.cache_data
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
                gdf = gpd.read_file(p)
                if not gdf.empty:
                    # Garantir que temos as colunas necessárias
                    if 'cor' not in gdf.columns and 'nivel' in gdf.columns:
                        gdf['cor'] = gdf['nivel'].map(CORES_CRIMINALIDADE)
                    elif 'cor' not in gdf.columns:
                        # Atribuir cores default se não houver dados
                        gdf['cor'] = '#95a5a6'
                    return gdf
        except:
            continue
    return None

def criar_mapa_interativo(gdf):
    # Calcular centro do mapa
    bounds = gdf.total_bounds
    centro_lat = (bounds[1] + bounds[3]) / 2
    centro_lon = (bounds[0] + bounds[2]) / 2
    
    # Criar mapa base com OpenStreetMap
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=10,
        tiles='OpenStreetMap',
        attr='OpenStreetMap'
    )
    
    # Ajustar bounds para mostrar apenas o Rio
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    # Adicionar camada de criminalidade
    for idx, row in gdf.iterrows():
        # Pegar informações
        nome = row.get('nome', f'Região {idx+1}')
        nivel = row.get('nivel', 'N/A')
        cor = row.get('cor', '#95a5a6')
        populacao = row.get('populacao', 'N/A')
        
        # Criar popup com informações
        popup_html = f"""
        <div style="font-family: Arial; font-size: 14px; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{nome}</h4>
            <p style="margin: 5px 0;"><b>Nível:</b> {nivel}</p>
            <p style="margin: 5px 0;"><b>População:</b> {populacao:,} habitantes</p>
            <div style="margin-top: 10px; padding: 8px; background: {cor}; 
                        border-radius: 4px; text-align: center; color: white; font-weight: bold;">
                {nivel}
            </div>
        </div>
        """
        
        # Adicionar polígono ao mapa
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': '#2c3e50',
                'weight': 2,
                'fillOpacity': 0.6,
                'opacity': 1
            },
            highlight_function=lambda x: {
                'fillColor': '#3498db',
                'color': '#ffffff',
                'weight': 4,
                'fillOpacity': 0.8
            },
            tooltip=folium.Tooltip(nome, style="font-size: 14px; font-weight: bold;"),
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(mapa)
    
    # Adicionar legenda
    legenda_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; 
                background-color: white; z-index: 9999; border: 2px solid #2c3e50;
                border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="margin: 0 0 15px 0; text-align: center; color: #2c3e50;">
            Níveis de Criminalidade
        </h4>
    '''
    
    for nivel, cor in CORES_CRIMINALIDADE.items():
        legenda_html += f'''
        <div style="margin: 8px 0; display: flex; align-items: center;">
            <div style="width: 30px; height: 20px; background: {cor}; 
                        border: 1px solid #2c3e50; border-radius: 3px; margin-right: 10px;">
            </div>
            <span style="font-size: 13px; color: #2c3e50;">{nivel}</span>
    </div>
        '''
    
    legenda_html += '</div>'
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa

st.markdown("### 📍 Visualização Interativa com Mapa Base")

with st.spinner("🗺️ Carregando dados geográficos..."):
    gdf = carregar_dados()

if gdf is None:
    st.error("❌ Não foi possível carregar os dados do mapa")
else:
col1, col2 = st.columns([3, 1])

with col1:
        with st.spinner("🎨 Gerando visualização..."):
            mapa = criar_mapa_interativo(gdf)
            st_folium(mapa, width=None, height=600)

with col2:
        st.markdown("#### 📊 Estatísticas")
        
        for idx, row in gdf.iterrows():
            nome = row.get('nome', f'Região {idx+1}')
            nivel = row.get('nivel', 'N/A')
            cor = row.get('cor', '#95a5a6')
            
            st.markdown(f"""
            <div style="margin: 10px 0; padding: 10px; background: {cor}; 
                        border-radius: 5px; color: white;">
                <b>{nome}</b><br>
                <small>{nivel}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
        st.info("""
        **Como usar:**
        - 🖱️ Clique nas áreas para ver detalhes
        - 🔍 Zoom com scroll do mouse
        - 👆 Arraste para mover o mapa
        """)

st.markdown("---")
st.caption("Mapa de Criminalidade - Município do Rio de Janeiro")
