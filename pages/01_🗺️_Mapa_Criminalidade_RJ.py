"""
🗺️ MAPA CHOROPLETH - CRIMINALIDADE POR ZONA
============================================

Mapa do MUNICÍPIO DO RIO DE JANEIRO com:
- 4 Zonas Principais (Centro, Sul, Norte, Oeste)
- Cores sólidas por intensidade de criminalidade
- Preenchimento completo das áreas
- Apenas o município (sem Baixada Fluminense, Niterói, etc.)
"""

import streamlit as st
import pandas as pd
import folium
import json
from pathlib import Path
from streamlit_folium import folium_static
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="🗺️ Mapa de Criminalidade - Rio de Janeiro",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Mapa de Criminalidade do Município do Rio de Janeiro")
st.markdown("### Intensidade Criminal por Zona")
st.warning("⚠️ **ATENÇÃO:** Este mapa exibe APENAS o município do Rio de Janeiro (4 zonas principais). Não inclui Baixada Fluminense, Niterói ou outros municípios.")

# ============================================================================
# DADOS DAS 4 ZONAS DO MUNICÍPIO
# ============================================================================

dados_zonas = {
    "Centro": {
        "populacao": 450000,
        "crimes_totais": 7226,  # Soma das RAs do Centro
        "nivel": "Médio",
        "cor": "#f39c12"  # Laranja
    },
    "Zona Sul": {
        "populacao": 620218,  # Botafogo + Copacabana + Lagoa + Rocinha
        "crimes_totais": 14365,
        "nivel": "Baixo",
        "cor": "#27ae60"  # Verde escuro
    },
    "Zona Norte": {
        "populacao": 2389742,
        "crimes_totais": 69785,
        "nivel": "Alto",
        "cor": "#e67e22"  # Laranja escuro
    },
    "Zona Oeste": {
        "populacao": 2470583,
        "crimes_totais": 67592,
        "nivel": "Muito Alto",
        "cor": "#e74c3c"  # Vermelho
    }
}

# Calcular taxas
for zona, dados in dados_zonas.items():
    dados['taxa_100k'] = round((dados['crimes_totais'] / dados['populacao']) * 100000, 1)

# ============================================================================
# CRIAR MAPA CHOROPLETH
# ============================================================================

def criar_mapa_choropleth():
    """Cria mapa choropleth com as 4 zonas do Rio de Janeiro"""
    
    # Carregar GeoJSON das zonas
    geojson_path = Path(__file__).parent.parent / "data" / "shapefiles" / "zonas_rio.geojson"
    
    if geojson_path.exists():
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_zonas = json.load(f)
    else:
        st.error("❌ Arquivo GeoJSON das zonas não encontrado!")
        return None
    
    # Preparar DataFrame para o choropleth
    df_mapa = pd.DataFrame([
        {
            'zona': zona,
            'taxa_100k': dados['taxa_100k'],
            'nivel': dados['nivel'],
            'crimes': dados['crimes_totais'],
            'populacao': dados['populacao']
        }
        for zona, dados in dados_zonas.items()
    ])
    
    # Centro do Rio
    RIO_CENTER = [-22.9068, -43.3729]
    
    # Criar mapa base
    mapa = folium.Map(
        location=RIO_CENTER,
        zoom_start=10,
        tiles='CartoDB positron',
        min_zoom=9,
        max_zoom=13
    )
    
    # Adicionar Choropleth
    folium.Choropleth(
        geo_data=geojson_zonas,
        name='choropleth',
        data=df_mapa,
        columns=['zona', 'taxa_100k'],
        key_on='feature.properties.nome',
        fill_color='YlOrRd',
        fill_opacity=1.0,  # Preenchimento total
        line_opacity=1.0,
        line_weight=2,
        line_color='#000000',
        legend_name='Taxa de Criminalidade (por 100k hab)',
        smooth_factor=0
    ).add_to(mapa)
    
    # Adicionar tooltips personalizados
    style_function = lambda x: {
        'fillColor': dados_zonas[x['properties']['nome']]['cor'],
        'color': '#000000',
        'weight': 2,
        'fillOpacity': 1.0
    }
    
    highlight_function = lambda x: {
        'weight': 4,
        'fillOpacity': 1.0
    }
    
    # Adicionar GeoJson com tooltips
    folium.GeoJson(
        geojson_zonas,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['nome'],
            aliases=['Zona:'],
            style="""
                background-color: white;
                color: #333333;
                font-family: arial;
                font-size: 12px;
                padding: 10px;
            """
        )
    ).add_to(mapa)
    
    # Adicionar rótulos nas zonas
    for feature in geojson_zonas['features']:
        nome = feature['properties']['nome']
        coords = feature['geometry']['coordinates'][0]
        
        # Calcular centro do polígono (aproximação simples)
        lats = [c[1] for c in coords]
        lons = [c[0] for c in coords]
        centro = [sum(lats) / len(lats), sum(lons) / len(lons)]
        
        dados = dados_zonas[nome]
        
        # Adicionar marcador com informações
        folium.Marker(
            location=centro,
            icon=folium.DivIcon(html=f"""
                <div style="
                    background-color: white;
                    border: 2px solid {dados['cor']};
                    border-radius: 5px;
                    padding: 5px 10px;
                    font-size: 12px;
                    font-weight: bold;
                    color: #333;
                    text-align: center;
                    box-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    white-space: nowrap;
                ">
                    {nome}<br>
                    <span style="color: {dados['cor']};">{dados['nivel']}</span><br>
                    <small>{dados['taxa_100k']:.0f}/100k</small>
                </div>
            """)
        ).add_to(mapa)
    
    # Adicionar legenda customizada
    legenda_html = """
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 220px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 15px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <p style="margin-top:0; font-weight: bold; text-align: center; font-size: 16px;">
            Nível de Criminalidade
        </p>
        <div style="margin: 10px 0; padding: 8px; background-color: #27ae60; color: white; border-radius: 3px;">
            <b>Zona Sul - Baixo</b><br>
            <small>2.315 crimes/100k hab</small>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #f39c12; color: white; border-radius: 3px;">
            <b>Centro - Médio</b><br>
            <small>1.606 crimes/100k hab</small>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #e67e22; color: white; border-radius: 3px;">
            <b>Zona Norte - Alto</b><br>
            <small>2.920 crimes/100k hab</small>
        </div>
        <div style="margin: 10px 0; padding: 8px; background-color: #e74c3c; color: white; border-radius: 3px;">
            <b>Zona Oeste - Muito Alto</b><br>
            <small>2.736 crimes/100k hab</small>
        </div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa

# ============================================================================
# EXIBIR MAPA E ESTATÍSTICAS
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa Choropleth do Município")
    st.info("💡 **Nota:** Mapa com preenchimento completo das 4 zonas do município do Rio de Janeiro.")
    
    mapa = criar_mapa_choropleth()
    
    if mapa:
        folium_static(mapa, width=900, height=600)
    else:
        st.error("Erro ao carregar o mapa. Execute o script: `python scripts/criar_mapa_zonas.py`")

with col2:
    st.markdown("#### 📊 Estatísticas por Zona")
    
    for zona, dados in dados_zonas.items():
        with st.expander(f"**{zona}**", expanded=False):
            st.markdown(f"""
            **Nível:** {dados['nivel']}  
            **População:** {dados['populacao']:,}  
            **Crimes Totais:** {dados['crimes_totais']:,}  
            **Taxa:** {dados['taxa_100k']:.1f}/100k hab
            """)
    
    st.markdown("---")
    st.markdown("#### 📈 Estatísticas Gerais")
    
    total_pop = sum(d['populacao'] for d in dados_zonas.values())
    total_crimes = sum(d['crimes_totais'] for d in dados_zonas.values())
    taxa_media = (total_crimes / total_pop) * 100000
    
    st.metric("População Total", f"{total_pop:,}")
    st.metric("Crimes Totais", f"{total_crimes:,}")
    st.metric("Taxa Média", f"{taxa_media:.1f}/100k")

# ============================================================================
# TABELA COMPARATIVA
# ============================================================================

st.markdown("---")
st.markdown("### 📋 Comparação Entre Zonas")

df_comparacao = pd.DataFrame([
    {
        'Zona': zona,
        'População': dados['populacao'],
        'Crimes': dados['crimes_totais'],
        'Taxa/100k': dados['taxa_100k'],
        'Nível': dados['nivel']
    }
    for zona, dados in dados_zonas.items()
])

# Ordenar por taxa
df_comparacao = df_comparacao.sort_values('Taxa/100k', ascending=False)

# Aplicar cores
def highlight_row(row):
    cor = dados_zonas[row['Zona']]['cor']
    return [f'background-color: {cor}; color: white; font-weight: bold'] * len(row)

st.dataframe(
    df_comparacao.style.apply(highlight_row, axis=1),
    use_container_width=True
)

# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p><b>🗺️ Mapa Choropleth do Município do Rio de Janeiro</b></p>
    <p>Mapa com preenchimento completo das 4 zonas principais.</p>
    <p><b>⚠️ Nota:</b> Os dados são baseados em estatísticas oficiais agregadas por zona.</p>
    <p><b>✅ Município do Rio de Janeiro</b> - Não inclui Baixada Fluminense, Niterói ou outros municípios.</p>
</div>
""", unsafe_allow_html=True)
