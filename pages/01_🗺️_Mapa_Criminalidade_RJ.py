import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mapa de Criminalidade - Rio de Janeiro", page_icon="🗺️", layout="wide")

st.title("🗺️ Mapa Temático de Criminalidade")
st.markdown("### Município do Rio de Janeiro")
st.warning("⚠️ **Mapa Estático** - Visualização coroplética sem interação")

ESCALA_CORES = {
    "Muito Baixo": "#27ae60",
    "Baixo": "#2ecc71",
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

def carregar_dados_geoespaciais():
    caminhos_possiveis = [
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_zonas_real.geojson",
        Path("data/shapefiles/municipio_rio_zonas_real.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "municipio_rio_bairros.geojson",
        Path("data/shapefiles/municipio_rio_bairros.geojson"),
        Path(__file__).parent.parent / "data" / "shapefiles" / "areas_detalhadas_rio.geojson",
        Path("data/shapefiles/areas_detalhadas_rio.geojson")
    ]
    for caminho in caminhos_possiveis:
        try:
            if caminho.exists():
                gdf = gpd.read_file(caminho)
                if not gdf.empty:
                    return gdf
        except:
            continue
    return None

def preparar_dados_criminalidade(gdf):
    if 'cor' not in gdf.columns:
        if 'nivel' in gdf.columns:
            gdf['cor'] = gdf['nivel'].map(ESCALA_CORES)
        else:
            gdf['cor'] = '#95a5a6'
    gdf['cor'].fillna('#95a5a6', inplace=True)
    return gdf

def criar_mapa_tematico_estatico(gdf):
    bounds = gdf.total_bounds
    centro_lat = (bounds[1] + bounds[3]) / 2
    centro_lon = (bounds[0] + bounds[2]) / 2
    
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=11,
        dragging=False,
        scrollWheelZoom=False,
        doubleClickZoom=False,
        boxZoom=False,
        keyboard=False,
        zoomControl=False,
        tiles='CartoDB positron'
    )
    
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    def estilo_setor(feature):
        cor_setor = feature['properties'].get('cor', '#95a5a6')
        return {
            'fillColor': cor_setor,
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.9,
            'opacity': 1
        }
    
    campos_disponiveis = []
    aliases_campos = []
    if 'nome' in gdf.columns:
        campos_disponiveis.append('nome')
        aliases_campos.append('Área:')
    if 'nivel' in gdf.columns:
        campos_disponiveis.append('nivel')
        aliases_campos.append('Nível:')
    
    tooltip_config = None
    if campos_disponiveis:
        tooltip_config = folium.GeoJsonTooltip(
            fields=campos_disponiveis,
            aliases=aliases_campos,
            sticky=True,
            labels=True,
            style="background-color: white; color: #333; font-family: Arial; font-size: 12px; padding: 8px;"
        )
    
    folium.GeoJson(gdf, style_function=estilo_setor, tooltip=tooltip_config).add_to(mapa)
    
    leg = '<div style="position:fixed;bottom:40px;right:40px;width:200px;background:white;z-index:9999;padding:15px;border:2px solid #333;border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,0.1);font-family:Arial;">'
    leg += '<h4 style="margin:0 0 12px 0;text-align:center;font-size:14px;font-weight:bold;color:#333;">Nível de Criminalidade</h4>'
    for nivel, cor in ESCALA_CORES.items():
        leg += f'<div style="margin:8px 0;padding:8px;background:{cor};color:white;text-align:center;border-radius:4px;font-size:12px;font-weight:bold;">{nivel}</div>'
    leg += '<p style="margin:12px 0 0 0;text-align:center;font-size:10px;color:#666;">Mapa Coroplético Estático</p></div>'
    mapa.get_root().html.add_child(folium.Element(leg))
    
    return mapa

col_mapa, col_info = st.columns([3, 1])

with col_mapa:
    st.markdown("#### 📍 Visualização Geoespacial")
    gdf = carregar_dados_geoespaciais()
    if gdf is None:
        st.error("❌ Arquivo GeoJSON/Shapefile não encontrado!")
        st.info("Coloque o arquivo em: data/shapefiles/areas_detalhadas_rio.geojson")
    else:
        gdf = preparar_dados_criminalidade(gdf)
        mapa = criar_mapa_tematico_estatico(gdf)
        st_folium(mapa, width=900, height=600, returned_objects=[])
        st.caption(f"📊 Total de setores mapeados: **{len(gdf)}**")

with col_info:
    st.markdown("#### 📋 Características Técnicas")
    st.info("**✅ Mapa Estático**\n\n🔒 Sem zoom\n🔒 Sem arrastar\n🔒 Sem interação\n\n**🗺️ Visualização**\n\n🎨 Preenchimento completo\n📐 Limites reais\n🌍 Apenas município\n\n**🎨 Estilo**\n\n• Opacidade: 90%\n• Bordas: 1px preta\n• Base: Minimalista")
    st.markdown("---")
    st.markdown("#### 🎨 Escala de Cores")
    for nivel, cor in ESCALA_CORES.items():
        html = f'<div style="background:{cor};color:white;padding:10px;margin:6px 0;border-radius:4px;text-align:center;font-weight:bold;font-size:13px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">{nivel}</div>'
        st.markdown(html, unsafe_allow_html=True)
st.markdown("---")
    st.markdown("#### 📊 Tecnologias")
    st.code("• GeoPandas\n• Folium\n• Streamlit\n• Shapely")

st.markdown("---")
st.markdown('<div style="text-align:center;color:#666;padding:20px;"><p style="margin:0;font-size:14px;"><strong>Mapa Temático Coroplético</strong></p><p style="margin:5px 0 0 0;font-size:12px;">Município do Rio de Janeiro - Análise de Criminalidade</p><p style="margin:5px 0 0 0;font-size:11px;color:#999;">Visualização estática com preenchimento geográfico preciso</p></div>', unsafe_allow_html=True)
