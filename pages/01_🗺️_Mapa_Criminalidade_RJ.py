"""
Mapa Temático de Criminalidade - Município do Rio de Janeiro
Mapa coroplético estático com preenchimento completo por setor
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Mapa de Criminalidade - Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

# Título
st.title("🗺️ Mapa Temático de Criminalidade")
st.markdown("### Município do Rio de Janeiro")
st.warning("⚠️ **Mapa Estático** - Visualização coroplética sem interação")

# Definição de cores por nível (escala gradual)
ESCALA_CORES = {
    "Muito Baixo": "#27ae60",    # Verde escuro
    "Baixo": "#2ecc71",          # Verde claro
    "Médio": "#f39c12",          # Laranja
    "Alto": "#e67e22",           # Laranja escuro
    "Muito Alto": "#e74c3c"      # Vermelho
}

def carregar_dados_geoespaciais():
    """
    Carrega arquivo GeoJSON/Shapefile com as divisões territoriais do município.
    Prioriza arquivos mais detalhados (bairros/áreas) sobre zonas.
    """
    caminhos_possiveis = [
        # Prioridade 1: Dados detalhados (bairros/áreas)
        Path(__file__).parent.parent / "data" / "shapefiles" / "areas_detalhadas_rio.geojson",
        Path("data/shapefiles/areas_detalhadas_rio.geojson"),
        
        # Prioridade 2: Zonas do município
        Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson",
        Path("data/shapefiles/zonas_rio.geojson"),
        
        # Prioridade 3: Fallback
        Path(__file__).parent.parent / "data" / "shapefiles" / "regioes_administrativas.geojson",
        Path("data/shapefiles/regioes_administrativas.geojson")
    ]
    
    for caminho in caminhos_possiveis:
        try:
            if caminho.exists():
                gdf = gpd.read_file(caminho)
                if not gdf.empty:
                    return gdf
        except Exception as e:
            continue
    
    return None

def preparar_dados_criminalidade(gdf):
    """
    Prepara os dados adicionando cores baseadas nos níveis de criminalidade.
    Garante que cada setor tenha uma cor associada.
    """
    if 'cor' not in gdf.columns:
        if 'nivel' in gdf.columns:
            gdf['cor'] = gdf['nivel'].map(ESCALA_CORES)
        else:
            # Cor padrão se não houver dados
            gdf['cor'] = '#95a5a6'
    
    # Preencher valores nulos
    gdf['cor'].fillna('#95a5a6', inplace=True)
    
    return gdf

def criar_mapa_tematico_estatico(gdf):
    """
    Cria um mapa temático coroplético ESTÁTICO.
    
    Características:
    - Sem interação (zoom/arrastar desabilitados)
    - Preenchimento completo de cada setor
    - Respeita limites geográficos reais
    - Bordas finas entre setores
    """
    
    # Calcular bounds do município para ajustar visualização
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    centro_lat = (bounds[1] + bounds[3]) / 2
    centro_lon = (bounds[0] + bounds[2]) / 2
    
    # Criar mapa base com todas as interações DESABILITADAS
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=11,
        
        # DESABILITAR TODAS AS INTERAÇÕES
        dragging=False,              # Não pode arrastar
        scrollWheelZoom=False,       # Não pode zoom com scroll
        doubleClickZoom=False,       # Não pode zoom com duplo clique
        boxZoom=False,               # Não pode zoom com caixa
        keyboard=False,              # Não pode usar teclado
        zoomControl=False,           # Remove controles de zoom
        
        # Estilo minimalista
        tiles='CartoDB positron',    # Mapa claro e limpo
        attr='Mapa de Criminalidade'
    )
    
    # Ajustar visualização aos limites EXATOS do município
    mapa.fit_bounds([
        [bounds[1], bounds[0]],  # southwest [lat, lon]
        [bounds[3], bounds[2]]   # northeast [lat, lon]
    ])
    
    # Função de estilo para cada feature (setor)
    def estilo_setor(feature):
        """
        Define o estilo de preenchimento de cada setor.
        
        - fillColor: cor baseada no nível de criminalidade
        - color: cor da borda (preta, fina)
        - weight: espessura da borda (1px)
        - fillOpacity: opacidade do preenchimento (0.9 = 90% opaco)
        """
        cor_setor = feature['properties'].get('cor', '#95a5a6')
        
        return {
            'fillColor': cor_setor,      # Cor sólida do setor
            'color': '#000000',          # Borda preta
            'weight': 1,                 # Borda fina (1px)
            'fillOpacity': 0.9,          # Preenchimento quase opaco
            'opacity': 1                 # Borda totalmente opaca
        }
    
    # Preparar campos para tooltip (se existirem)
    campos_disponiveis = []
    aliases_campos = []
    
    if 'nome' in gdf.columns:
        campos_disponiveis.append('nome')
        aliases_campos.append('Área:')
    
    if 'nivel' in gdf.columns:
        campos_disponiveis.append('nivel')
        aliases_campos.append('Nível:')
    
    # Adicionar camada GeoJSON com setores preenchidos
        folium.GeoJson(
        gdf,
        style_function=estilo_setor,
        tooltip=folium.GeoJsonTooltip(
            fields=campos_disponiveis,
            aliases=aliases_campos,
            sticky=True,
            labels=True,
            style="""
                background-color: white;
                color: #333333;
                font-family: Arial, sans-serif;
                font-size: 12px;
                padding: 8px;
                border-radius: 3px;
            """
        ) if campos_disponiveis else None
        ).add_to(mapa)
    
    # Adicionar legenda HTML customizada
    legenda_html = f"""
    <div style="
        position: fixed;
        bottom: 40px;
        right: 40px;
        width: 200px;
        background-color: white;
        z-index: 9999;
        padding: 15px;
        border: 2px solid #333;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    ">
        <h4 style="
            margin: 0 0 12px 0;
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            color: #333;
        ">
            Nível de Criminalidade
        </h4>
    """
    
    for nivel, cor in ESCALA_CORES.items():
        legenda_html += f"""
        <div style="
            margin: 8px 0;
            padding: 8px;
            background-color: {cor};
            color: white;
            text-align: center;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {nivel}
        </div>
        """
    
    legenda_html += """
        <p style="
            margin: 12px 0 0 0;
            text-align: center;
            font-size: 10px;
            color: #666;
        ">
            Mapa Coroplético Estático
        </p>
    </div>
    """
    
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa

# ============================================
# LAYOUT PRINCIPAL
# ============================================

col_mapa, col_info = st.columns([3, 1])

with col_mapa:
    st.markdown("#### 📍 Visualização Geoespacial")
    
    # Carregar dados
    gdf = carregar_dados_geoespaciais()
    
    if gdf is None:
        st.error("❌ **Erro:** Arquivo GeoJSON/Shapefile não encontrado!")
        st.info("""
        💡 **Solução:**
        
        1. Coloque o arquivo GeoJSON na pasta:
           `data/shapefiles/areas_detalhadas_rio.geojson`
        
        2. O arquivo deve conter:
           - Geometrias dos setores (Polygon/MultiPolygon)
           - Campo 'nome' com o nome do setor
           - Campo 'nivel' com nível de criminalidade
           - Campo 'cor' (opcional) com cores hexadecimais
        """)
    else:
        # Preparar dados
        gdf = preparar_dados_criminalidade(gdf)
        
        # Criar mapa
        mapa = criar_mapa_tematico_estatico(gdf)
        
        # Renderizar mapa estático
        st_folium(
            mapa,
            width=900,
            height=600,
            returned_objects=[]  # Não retorna interações
        )
        
        # Informações técnicas
        st.caption(f"📊 Total de setores mapeados: **{len(gdf)}**")

with col_info:
    st.markdown("#### 📋 Características Técnicas")
    
    st.info("""
    **✅ Mapa Estático**
    
    🔒 Sem zoom
    🔒 Sem arrastar
    🔒 Sem interação
    
    **🗺️ Visualização**
    
    🎨 Preenchimento completo
    📐 Limites reais
    🌍 Apenas município
    
    **🎨 Estilo**
    
    • Opacidade: 90%
    • Bordas: 1px preta
    • Base: Minimalista
    """)

st.markdown("---")
    st.markdown("#### 🎨 Escala de Cores")
    
    for nivel, cor in ESCALA_CORES.items():
        st.markdown(
            f"""
            <div style="
                background-color: {cor};
                color: white;
                padding: 10px;
                margin: 6px 0;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
                font-size: 13px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                {nivel}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown("#### 📊 Tecnologias")
    st.code("""
• GeoPandas
• Folium
• Streamlit
• Shapely
    """)

# ============================================
# RODAPÉ
# ============================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p style="margin: 0; font-size: 14px;">
            <strong>Mapa Temático Coroplético</strong>
        </p>
        <p style="margin: 5px 0 0 0; font-size: 12px;">
            Município do Rio de Janeiro - Análise de Criminalidade
        </p>
        <p style="margin: 5px 0 0 0; font-size: 11px; color: #999;">
            Visualização estática com preenchimento geográfico preciso
        </p>
</div>
    """,
    unsafe_allow_html=True
)
