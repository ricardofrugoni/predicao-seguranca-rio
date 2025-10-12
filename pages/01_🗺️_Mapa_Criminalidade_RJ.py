"""
🗺️ MAPA CHOROPLETH - CRIMINALIDADE POR REGIÃO ADMINISTRATIVA
============================================================

Mapa estático do MUNICÍPIO DO RIO DE JANEIRO com:
- 33 Regiões Administrativas (RAs)
- Cores por intensidade de criminalidade
- Preenchimento completo (não bolhas)
- Apenas o município (sem Baixada Fluminense, Niterói, etc.)
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium import plugins
import json
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
st.markdown("### Intensidade Criminal por Região Administrativa")

# ============================================================================
# DADOS DAS 33 REGIÕES ADMINISTRATIVAS DO MUNICÍPIO DO RIO
# ============================================================================

# Dados reais das RAs com taxas de criminalidade simuladas realistas
dados_ras = {
    1: {"nome": "Portuária", "zona": "Centro", "pop": 39773, "crimes": 1847, "nivel": "Médio"},
    2: {"nome": "Centro", "zona": "Centro", "pop": 41142, "crimes": 2514, "nivel": "Alto"},
    3: {"nome": "Rio Comprido", "zona": "Centro", "pop": 79647, "crimes": 2789, "nivel": "Médio"},
    4: {"nome": "Botafogo", "zona": "Zona Sul", "pop": 239729, "crimes": 3841, "nivel": "Baixo"},
    5: {"nome": "Copacabana", "zona": "Zona Sul", "pop": 146392, "crimes": 4672, "nivel": "Médio"},
    6: {"nome": "Lagoa", "zona": "Zona Sul", "pop": 164936, "crimes": 2198, "nivel": "Baixo"},
    7: {"nome": "São Cristóvão", "zona": "Zona Norte", "pop": 85135, "crimes": 2876, "nivel": "Médio"},
    8: {"nome": "Tijuca", "zona": "Zona Norte", "pop": 181839, "crimes": 3654, "nivel": "Médio"},
    9: {"nome": "Vila Isabel", "zona": "Zona Norte", "pop": 187362, "crimes": 3328, "nivel": "Médio"},
    10: {"nome": "Ramos", "zona": "Zona Norte", "pop": 147236, "crimes": 4487, "nivel": "Alto"},
    11: {"nome": "Penha", "zona": "Zona Norte", "pop": 183561, "crimes": 5214, "nivel": "Alto"},
    12: {"nome": "Inhaúma", "zona": "Zona Norte", "pop": 134743, "crimes": 4863, "nivel": "Alto"},
    13: {"nome": "Méier", "zona": "Zona Norte", "pop": 391124, "crimes": 6542, "nivel": "Médio"},
    14: {"nome": "Irajá", "zona": "Zona Norte", "pop": 192346, "crimes": 5789, "nivel": "Alto"},
    15: {"nome": "Madureira", "zona": "Zona Norte", "pop": 360869, "crimes": 7234, "nivel": "Alto"},
    16: {"nome": "Jacarepaguá", "zona": "Zona Oeste", "pop": 573896, "crimes": 9876, "nivel": "Alto"},
    17: {"nome": "Bangu", "zona": "Zona Oeste", "pop": 732437, "crimes": 12543, "nivel": "Muito Alto"},
    18: {"nome": "Campo Grande", "zona": "Zona Oeste", "pop": 542080, "crimes": 11287, "nivel": "Muito Alto"},
    19: {"nome": "Santa Cruz", "zona": "Zona Oeste", "pop": 434753, "crimes": 9654, "nivel": "Muito Alto"},
    20: {"nome": "Ilha do Governador", "zona": "Zona Norte", "pop": 211018, "crimes": 3876, "nivel": "Médio"},
    21: {"nome": "Paquetá", "zona": "Zona Norte", "pop": 3361, "crimes": 42, "nivel": "Muito Baixo"},
    22: {"nome": "Anchieta", "zona": "Zona Norte", "pop": 128386, "crimes": 4321, "nivel": "Alto"},
    23: {"nome": "Santa Teresa", "zona": "Centro", "pop": 40926, "crimes": 876, "nivel": "Baixo"},
    24: {"nome": "Barra da Tijuca", "zona": "Zona Oeste", "pop": 300823, "crimes": 4567, "nivel": "Baixo"},
    25: {"nome": "Pavuna", "zona": "Zona Norte", "pop": 227729, "crimes": 8234, "nivel": "Muito Alto"},
    26: {"nome": "Guaratiba", "zona": "Zona Oeste", "pop": 110049, "crimes": 2876, "nivel": "Médio"},
    27: {"nome": "Rocinha", "zona": "Zona Sul", "pop": 69161, "crimes": 3654, "nivel": "Muito Alto"},
    28: {"nome": "Jacarezinho", "zona": "Zona Norte", "pop": 37839, "crimes": 2987, "nivel": "Muito Alto"},
    29: {"nome": "Complexo do Alemão", "zona": "Zona Norte", "pop": 69143, "crimes": 4321, "nivel": "Muito Alto"},
    30: {"nome": "Maré", "zona": "Zona Norte", "pop": 140003, "crimes": 7654, "nivel": "Muito Alto"},
    31: {"nome": "Vigário Geral", "zona": "Zona Norte", "pop": 35859, "crimes": 2543, "nivel": "Alto"},
    32: {"nome": "Realengo", "zona": "Zona Oeste", "pop": 245025, "crimes": 6789, "nivel": "Alto"},
    33: {"nome": "Cidade de Deus", "zona": "Zona Oeste", "pop": 36515, "crimes": 2987, "nivel": "Muito Alto"}
}

# Calcular taxa por 100k habitantes
for ra_id, dados in dados_ras.items():
    dados['taxa_100k'] = round((dados['crimes'] / dados['pop']) * 100000, 1)

# ============================================================================
# GEOJSON DAS REGIÕES ADMINISTRATIVAS DO MUNICÍPIO DO RIO
# ============================================================================

def criar_geojson_rio_municipio():
    """
    Cria GeoJSON com polígonos das 33 RAs do município do Rio de Janeiro
    Coordenadas aproximadas para visualização
    """
    
    # GeoJSON com polígonos simplificados das RAs do município
    # Cada RA tem um polígono que representa sua área geográfica aproximada
    geojson = {
        "type": "FeatureCollection",
        "features": [
            # ZONA SUL
            {
                "type": "Feature",
                "id": "4",
                "properties": {"ra_id": 4, "nome": "Botafogo", "zona": "Zona Sul"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.195, -22.945], [-43.175, -22.945], [-43.175, -22.960],
                        [-43.195, -22.960], [-43.195, -22.945]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "5",
                "properties": {"ra_id": 5, "nome": "Copacabana", "zona": "Zona Sul"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.195, -22.960], [-43.175, -22.960], [-43.175, -22.980],
                        [-43.195, -22.980], [-43.195, -22.960]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "6",
                "properties": {"ra_id": 6, "nome": "Lagoa", "zona": "Zona Sul"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.215, -22.960], [-43.195, -22.960], [-43.195, -22.980],
                        [-43.215, -22.980], [-43.215, -22.960]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "27",
                "properties": {"ra_id": 27, "nome": "Rocinha", "zona": "Zona Sul"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.255, -22.985], [-43.245, -22.985], [-43.245, -22.995],
                        [-43.255, -22.995], [-43.255, -22.985]
                    ]]
                }
            },
            
            # CENTRO
            {
                "type": "Feature",
                "id": "1",
                "properties": {"ra_id": 1, "nome": "Portuária", "zona": "Centro"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.185, -22.895], [-43.175, -22.895], [-43.175, -22.905],
                        [-43.185, -22.905], [-43.185, -22.895]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "2",
                "properties": {"ra_id": 2, "nome": "Centro", "zona": "Centro"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.195, -22.905], [-43.185, -22.905], [-43.185, -22.915],
                        [-43.195, -22.915], [-43.195, -22.905]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "3",
                "properties": {"ra_id": 3, "nome": "Rio Comprido", "zona": "Centro"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.210, -22.915], [-43.195, -22.915], [-43.195, -22.930],
                        [-43.210, -22.930], [-43.210, -22.915]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "23",
                "properties": {"ra_id": 23, "nome": "Santa Teresa", "zona": "Centro"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.195, -22.920], [-43.185, -22.920], [-43.185, -22.930],
                        [-43.195, -22.930], [-43.195, -22.920]
                    ]]
                }
            },
            
            # ZONA NORTE
            {
                "type": "Feature",
                "id": "7",
                "properties": {"ra_id": 7, "nome": "São Cristóvão", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.230, -22.900], [-43.220, -22.900], [-43.220, -22.910],
                        [-43.230, -22.910], [-43.230, -22.900]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "8",
                "properties": {"ra_id": 8, "nome": "Tijuca", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.250, -22.920], [-43.230, -22.920], [-43.230, -22.940],
                        [-43.250, -22.940], [-43.250, -22.920]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "9",
                "properties": {"ra_id": 9, "nome": "Vila Isabel", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.260, -22.920], [-43.250, -22.920], [-43.250, -22.935],
                        [-43.260, -22.935], [-43.260, -22.920]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "10",
                "properties": {"ra_id": 10, "nome": "Ramos", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.225, -22.850], [-43.210, -22.850], [-43.210, -22.865],
                        [-43.225, -22.865], [-43.225, -22.850]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "11",
                "properties": {"ra_id": 11, "nome": "Penha", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.295, -22.840], [-43.275, -22.840], [-43.275, -22.855],
                        [-43.295, -22.855], [-43.295, -22.840]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "12",
                "properties": {"ra_id": 12, "nome": "Inhaúma", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.285, -22.870], [-43.265, -22.870], [-43.265, -22.885],
                        [-43.285, -22.885], [-43.285, -22.870]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "13",
                "properties": {"ra_id": 13, "nome": "Méier", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.295, -22.895], [-43.275, -22.895], [-43.275, -22.915],
                        [-43.295, -22.915], [-43.295, -22.895]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "14",
                "properties": {"ra_id": 14, "nome": "Irajá", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.335, -22.845], [-43.315, -22.845], [-43.315, -22.865],
                        [-43.335, -22.865], [-43.335, -22.845]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "15",
                "properties": {"ra_id": 15, "nome": "Madureira", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.355, -22.865], [-43.330, -22.865], [-43.330, -22.885],
                        [-43.355, -22.885], [-43.355, -22.865]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "20",
                "properties": {"ra_id": 20, "nome": "Ilha do Governador", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.230, -22.800], [-43.205, -22.800], [-43.205, -22.825],
                        [-43.230, -22.825], [-43.230, -22.800]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "21",
                "properties": {"ra_id": 21, "nome": "Paquetá", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.115, -22.755], [-43.105, -22.755], [-43.105, -22.765],
                        [-43.115, -22.765], [-43.115, -22.755]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "22",
                "properties": {"ra_id": 22, "nome": "Anchieta", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.415, -22.815], [-43.395, -22.815], [-43.395, -22.835],
                        [-43.415, -22.835], [-43.415, -22.815]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "25",
                "properties": {"ra_id": 25, "nome": "Pavuna", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.375, -22.805], [-43.355, -22.805], [-43.355, -22.825],
                        [-43.375, -22.825], [-43.375, -22.805]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "28",
                "properties": {"ra_id": 28, "nome": "Jacarezinho", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.270, -22.878], [-43.255, -22.878], [-43.255, -22.893],
                        [-43.270, -22.893], [-43.270, -22.878]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "29",
                "properties": {"ra_id": 29, "nome": "Complexo do Alemão", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.270, -22.855], [-43.250, -22.855], [-43.250, -22.875],
                        [-43.270, -22.875], [-43.270, -22.855]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "30",
                "properties": {"ra_id": 30, "nome": "Maré", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.255, -22.845], [-43.235, -22.845], [-43.235, -22.865],
                        [-43.255, -22.865], [-43.255, -22.845]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "31",
                "properties": {"ra_id": 31, "nome": "Vigário Geral", "zona": "Zona Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.365, -22.795], [-43.345, -22.795], [-43.345, -22.815],
                        [-43.365, -22.815], [-43.365, -22.795]
                    ]]
                }
            },
            
            # ZONA OESTE
            {
                "type": "Feature",
                "id": "16",
                "properties": {"ra_id": 16, "nome": "Jacarepaguá", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.385, -22.915], [-43.355, -22.915], [-43.355, -22.945],
                        [-43.385, -22.945], [-43.385, -22.915]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "17",
                "properties": {"ra_id": 17, "nome": "Bangu", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.485, -22.860], [-43.450, -22.860], [-43.450, -22.890],
                        [-43.485, -22.890], [-43.485, -22.860]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "18",
                "properties": {"ra_id": 18, "nome": "Campo Grande", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.580, -22.885], [-43.540, -22.885], [-43.540, -22.920],
                        [-43.580, -22.920], [-43.580, -22.885]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "19",
                "properties": {"ra_id": 19, "nome": "Santa Cruz", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.710, -22.905], [-43.670, -22.905], [-43.670, -22.940],
                        [-43.710, -22.940], [-43.710, -22.905]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "24",
                "properties": {"ra_id": 24, "nome": "Barra da Tijuca", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.360, -22.990], [-43.310, -22.990], [-43.310, -23.020],
                        [-43.360, -23.020], [-43.360, -22.990]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "26",
                "properties": {"ra_id": 26, "nome": "Guaratiba", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.610, -23.040], [-43.560, -23.040], [-43.560, -23.075],
                        [-43.610, -23.075], [-43.610, -23.040]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "32",
                "properties": {"ra_id": 32, "nome": "Realengo", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.450, -22.860], [-43.425, -22.860], [-43.425, -22.885],
                        [-43.450, -22.885], [-43.450, -22.860]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "33",
                "properties": {"ra_id": 33, "nome": "Cidade de Deus", "zona": "Zona Oeste"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.375, -22.935], [-43.355, -22.935], [-43.355, -22.955],
                        [-43.375, -22.955], [-43.375, -22.935]
                    ]]
                }
            }
        ]
    }
    
    return geojson

# ============================================================================
# FUNÇÃO PARA DETERMINAR COR POR NÍVEL DE CRIMINALIDADE
# ============================================================================

def obter_cor_criminalidade(nivel):
    """Retorna cor baseada no nível de criminalidade"""
    cores = {
        "Muito Baixo": "#2ecc71",  # Verde
        "Baixo": "#27ae60",         # Verde escuro
        "Médio": "#f39c12",         # Laranja
        "Alto": "#e67e22",          # Laranja escuro
        "Muito Alto": "#e74c3c"     # Vermelho
    }
    return cores.get(nivel, "#95a5a6")

# ============================================================================
# CRIAR MAPA CHOROPLETH
# ============================================================================

@st.cache_data
def criar_mapa_criminalidade():
    """Cria mapa choropleth com preenchimento de regiões"""
    
    # Centro do município do Rio de Janeiro
    mapa = folium.Map(
        location=[-22.9068, -43.1729],
        zoom_start=10,
        tiles='CartoDB positron'
    )
    
    # Obter GeoJSON
    geojson_data = criar_geojson_rio_municipio()
    
    # Adicionar camada choropleth
    folium.Choropleth(
        geo_data=geojson_data,
        name='Criminalidade',
        data=pd.DataFrame([(ra_id, dados['taxa_100k']) for ra_id, dados in dados_ras.items()], 
                         columns=['ra_id', 'taxa']),
        columns=['ra_id', 'taxa'],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        legend_name='Taxa de Crimes por 100k habitantes',
        highlight=True
    ).add_to(mapa)
    
    # Adicionar marcadores com informações
    for feature in geojson_data['features']:
        ra_id = int(feature['id'])
        dados = dados_ras[ra_id]
        
        # Calcular centroide aproximado
        coords = feature['geometry']['coordinates'][0]
        lats = [c[1] for c in coords]
        lons = [c[0] for c in coords]
        centroid_lat = sum(lats) / len(lats)
        centroid_lon = sum(lons) / len(lons)
        
        # Criar popup com informações
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 0; color: #2c3e50;">{dados['nome']}</h4>
            <hr style="margin: 5px 0;">
            <b>Zona:</b> {dados['zona']}<br>
            <b>População:</b> {dados['pop']:,}<br>
            <b>Crimes (ano):</b> {dados['crimes']:,}<br>
            <b>Taxa/100k hab:</b> {dados['taxa_100k']}<br>
            <hr style="margin: 5px 0;">
            <b>Nível:</b> <span style="color: {obter_cor_criminalidade(dados['nivel'])}; 
                                      font-weight: bold;">{dados['nivel']}</span>
        </div>
        """
        
        folium.Marker(
            location=[centroid_lat, centroid_lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.DivIcon(html=f"""
                <div style="font-size: 10px; color: #2c3e50; font-weight: bold; 
                            background-color: white; padding: 2px 5px; border-radius: 3px;
                            border: 1px solid #7f8c8d;">
                    {dados['nome']}
                </div>
            """)
        ).add_to(mapa)
    
    return mapa

# ============================================================================
# EXIBIR MAPA E ESTATÍSTICAS
# ============================================================================

# Criar colunas para layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### 📍 Mapa Interativo")
    mapa = criar_mapa_criminalidade()
    folium_static(mapa, width=900, height=600)

with col2:
    st.markdown("#### 📊 Legenda")
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
        <h5 style="margin-top: 0;">Níveis de Criminalidade</h5>
        <div style="margin: 10px 0;">
            <span style="background-color: #2ecc71; padding: 3px 10px; border-radius: 3px; color: white;">
                Muito Baixo
            </span><br>
            <small>0 - 2.000 crimes/100k</small>
        </div>
        <div style="margin: 10px 0;">
            <span style="background-color: #27ae60; padding: 3px 10px; border-radius: 3px; color: white;">
                Baixo
            </span><br>
            <small>2.000 - 4.000 crimes/100k</small>
        </div>
        <div style="margin: 10px 0;">
            <span style="background-color: #f39c12; padding: 3px 10px; border-radius: 3px; color: white;">
                Médio
            </span><br>
            <small>4.000 - 6.000 crimes/100k</small>
        </div>
        <div style="margin: 10px 0;">
            <span style="background-color: #e67e22; padding: 3px 10px; border-radius: 3px; color: white;">
                Alto
            </span><br>
            <small>6.000 - 8.000 crimes/100k</small>
        </div>
        <div style="margin: 10px 0;">
            <span style="background-color: #e74c3c; padding: 3px 10px; border-radius: 3px; color: white;">
                Muito Alto
            </span><br>
            <small>Acima de 8.000 crimes/100k</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📈 Estatísticas Gerais")
    
    total_pop = sum(d['pop'] for d in dados_ras.values())
    total_crimes = sum(d['crimes'] for d in dados_ras.values())
    taxa_media = (total_crimes / total_pop) * 100000
    
    st.metric("População Total", f"{total_pop:,}")
    st.metric("Crimes Totais (ano)", f"{total_crimes:,}")
    st.metric("Taxa Média (100k)", f"{taxa_media:.1f}")

# ============================================================================
# TABELA DE DADOS
# ============================================================================

st.markdown("---")
st.markdown("### 📋 Dados Detalhados por Região Administrativa")

# Criar DataFrame
df_tabela = pd.DataFrame([
    {
        'RA': ra_id,
        'Nome': dados['nome'],
        'Zona': dados['zona'],
        'População': dados['pop'],
        'Crimes': dados['crimes'],
        'Taxa/100k': dados['taxa_100k'],
        'Nível': dados['nivel']
    }
    for ra_id, dados in dados_ras.items()
])

# Ordenar por taxa de criminalidade
df_tabela = df_tabela.sort_values('Taxa/100k', ascending=False)

# Aplicar estilo
def highlight_nivel(row):
    cor = obter_cor_criminalidade(row['Nível'])
    return ['']*6 + [f'background-color: {cor}; color: white; font-weight: bold']

st.dataframe(
    df_tabela.style.apply(highlight_nivel, axis=1),
    use_container_width=True,
    height=400
)

# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p><b>Nota:</b> Os dados apresentados são baseados em estatísticas oficiais e simulações para fins de visualização.</p>
    <p>Município do Rio de Janeiro - 33 Regiões Administrativas</p>
</div>
""", unsafe_allow_html=True)

