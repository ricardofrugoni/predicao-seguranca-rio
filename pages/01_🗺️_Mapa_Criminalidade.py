"""
🗺️ MAPA DE CRIMINALIDADE - Rio de Janeiro
=========================================

Mapa interativo de criminalidade do município do Rio de Janeiro.
Usando POO e dados geográficos oficiais.
"""

import streamlit as st
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import DataManager, MapVisualizer
from src.config import config
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(
    page_title="Mapa Criminalidade RJ",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Mapa de Criminalidade - Município do Rio de Janeiro")
st.markdown("### Visualização geográfica dos níveis de criminalidade")

# Instancia gerenciadores
@st.cache_resource
def get_managers():
    """Retorna instâncias dos gerenciadores"""
    return DataManager(), MapVisualizer()

data_manager, map_visualizer = get_managers()

# Sidebar com controles
st.sidebar.header("⚙️ Configurações")

# Seleção de arquivo GeoJSON
geojson_files = [
    "zonas_rio_limites_reais.geojson",
    "municipio_rio_zonas_real.geojson",
    "regioes_administrativas_rio.geojson"
]

selected_geojson = st.sidebar.selectbox(
    "Arquivo GeoJSON:",
    geojson_files,
    index=0
)

# Opção de incluir dados de criminalidade
include_crime_data = st.sidebar.checkbox(
    "Incluir dados de criminalidade",
    value=True
)

# Carrega dados geoespaciais
with st.spinner("🔄 Carregando dados geográficos..."):
    gdf = data_manager.get_geo_data(
        filename=selected_geojson,
        include_crime_data=include_crime_data
    )

if gdf is None or gdf.empty:
    st.error("❌ Não foi possível carregar os dados geográficos.")
    st.info("""
    **Possíveis soluções:**
    1. Verifique se o arquivo GeoJSON existe em `data/shapefiles/`
    2. Execute os scripts de download de dados geográficos
    3. Use dados simulados (opção no sidebar)
    """)
    
    # Botão para gerar dados simulados
    if st.button("🔄 Gerar Dados Simulados"):
        st.info("Gerando dados simulados...")
        # TODO: Implementar geração de dados simulados
else:
    # Estatísticas
    st.markdown("---")
    st.markdown("### 📊 Estatísticas Gerais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        n_areas = len(gdf)
        st.metric("Áreas no Mapa", n_areas)
    
    with col2:
        if 'taxa_100k' in gdf.columns:
            mean_rate = gdf['taxa_100k'].mean()
            st.metric("Taxa Média", f"{mean_rate:.1f}/100k hab")
        else:
            st.metric("Taxa Média", "N/A")
    
    with col3:
        if 'total_ocorrencias' in gdf.columns:
            total = gdf['total_ocorrencias'].sum()
            st.metric("Total Ocorrências", f"{int(total):,}")
        else:
            st.metric("Total Ocorrências", "N/A")
    
    with col4:
        st.metric("Sistema de Coordenadas", "EPSG:4326 (WGS84)")
    
    # Mapa
    st.markdown("---")
    st.markdown("### 🗺️ Mapa Interativo")
    
    # Cria mapa
    value_col = 'taxa_100k' if 'taxa_100k' in gdf.columns else None
    name_col = 'zona' if 'zona' in gdf.columns else gdf.columns[0]
    
    if value_col:
        mapa = map_visualizer.create(
            gdf=gdf,
            value_column=value_col,
            name_column=name_col,
            title="Criminalidade por Região"
        )
    else:
        st.warning("⚠️ Dados de criminalidade não disponíveis. Mostrando apenas geometrias.")
        mapa = map_visualizer.create(
            gdf=gdf,
            name_column=name_col
        )
    
    # Renderiza mapa
    st_folium(mapa, width=1400, height=800, returned_objects=[])
    
    # Legenda
    st.markdown("---")
    st.markdown("### 🎨 Legenda - Níveis de Criminalidade")
    
    legend_cols = st.columns(5)
    
    legend_items = [
        ("MUITO BAIXO", config.maps.COLOR_VERY_LOW, "< 20/100k hab"),
        ("BAIXO", config.maps.COLOR_LOW, "20-40/100k hab"),
        ("MÉDIO", config.maps.COLOR_MEDIUM, "40-60/100k hab"),
        ("ALTO", config.maps.COLOR_HIGH, "60-80/100k hab"),
        ("MUITO ALTO", config.maps.COLOR_VERY_HIGH, "> 80/100k hab")
    ]
    
    for col, (label, color, range_text) in zip(legend_cols, legend_items):
        col.markdown(
            f'<div style="background:{color};padding:15px;border-radius:8px;'
            f'text-align:center;color:white;font-weight:bold;">'
            f'{label}<br><small>{range_text}</small></div>',
            unsafe_allow_html=True
        )
    
    # Tabela de dados
    if st.checkbox("📋 Mostrar Tabela de Dados", value=False):
        st.markdown("---")
        st.markdown("### 📋 Dados Detalhados")
        
        # Remove coluna de geometria para exibição
        display_df = gdf.drop(columns=['geometry'])
        st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download
    st.markdown("---")
    st.markdown("### 📥 Download")
    
    if st.button("💾 Baixar Dados (CSV)"):
        csv = gdf.drop(columns=['geometry']).to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name=f"criminalidade_rio_{selected_geojson.replace('.geojson', '')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.caption("""
**🔒 Sistema de Análise de Segurança Pública - Rio de Janeiro**
- Dados: Simulados para demonstração
- Geometrias: Município do Rio de Janeiro
- Sistema: EPSG:4326 (WGS84)
- As manchas criminais respeitam os limites geográficos oficiais do município
""")

# Informações técnicas (sidebar)
with st.sidebar.expander("ℹ️ Informações Técnicas"):
    st.markdown("""
    **Tecnologias:**
    - Folium para mapas
    - GeoPandas para dados geoespaciais
    - Streamlit para interface
    
    **Arquitetura:**
    - POO (Programação Orientada a Objetos)
    - DataManager para dados
    - MapVisualizer para visualizações
    - Config centralizado
    """)

with st.sidebar.expander("🎯 Sobre o Mapa"):
    st.markdown("""
    **Este mapa mostra:**
    - ✅ Apenas o município do Rio de Janeiro
    - ✅ Limites geográficos reais e oficiais
    - ✅ Cores seguem exatamente as fronteiras
    - ✅ Sistema de coordenadas WGS84
    
    **Não inclui:**
    - ❌ Municípios adjacentes (Niterói, etc)
    - ❌ Baixada Fluminense
    - ❌ Áreas fora do município
    """)

