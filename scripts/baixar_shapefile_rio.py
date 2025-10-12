"""
🗺️ Baixar Shapefiles Oficiais do Rio de Janeiro
===============================================

Tenta baixar dados geográficos oficiais das divisões do município.
"""

import requests
import json
from pathlib import Path

def tentar_baixar_geojson():
    """
    Tenta baixar GeoJSON de várias fontes oficiais
    """
    
    # URLs de fontes com dados do Rio de Janeiro
    urls = [
        {
            "nome": "Bairros Rio (GeoSampa)",
            "url": "https://raw.githubusercontent.com/codinginbrazil/br-atlas/master/data/rio-de-janeiro/bairros.geojson"
        },
        {
            "nome": "Limite Municipal IBGE",
            "url": "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3304557?formato=application/vnd.geo+json"
        },
        {
            "nome": "Data Rio - Limite Municipal",
            "url": "https://www.data.rio/api/geospatial/2qwa-jpkh?method=export&format=GeoJSON"
        }
    ]
    
    resultados = {}
    
    for fonte in urls:
        try:
            print(f"\n📥 Tentando: {fonte['nome']}")
            print(f"   URL: {fonte['url']}")
            
            response = requests.get(fonte['url'], timeout=30)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('type') == 'FeatureCollection':
                        print(f"   ✅ Sucesso! Features: {len(data.get('features', []))}")
                        resultados[fonte['nome']] = data
                    else:
                        print(f"   ⚠️ Resposta não é GeoJSON válido")
                except:
                    print(f"   ⚠️ Erro ao processar JSON")
            else:
                print(f"   ❌ Status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return resultados

def criar_geojson_simplificado_realista():
    """
    Cria um GeoJSON mais realista baseado em coordenadas aproximadas
    das principais regiões do município do Rio de Janeiro
    """
    
    # GeoJSON com polígonos mais realistas para as 4 zonas
    # Baseado em coordenadas aproximadas reais
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nome": "Centro",
                    "zona_id": 1,
                    "nivel": "Médio"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.20, -22.89],
                        [-43.17, -22.89],
                        [-43.16, -22.91],
                        [-43.17, -22.93],
                        [-43.19, -22.94],
                        [-43.21, -22.93],
                        [-43.22, -22.91],
                        [-43.20, -22.89]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Sul",
                    "zona_id": 2,
                    "nivel": "Baixo"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.19, -22.94],
                        [-43.17, -22.93],
                        [-43.16, -22.95],
                        [-43.165, -22.98],
                        [-43.19, -23.01],
                        [-43.24, -23.00],
                        [-43.26, -22.99],
                        [-43.24, -22.96],
                        [-43.22, -22.94],
                        [-43.19, -22.94]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Norte",
                    "zona_id": 3,
                    "nivel": "Alto"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.45, -22.75],
                        [-43.11, -22.75],
                        [-43.10, -22.79],
                        [-43.11, -22.83],
                        [-43.14, -22.86],
                        [-43.17, -22.89],
                        [-43.20, -22.89],
                        [-43.25, -22.88],
                        [-43.30, -22.87],
                        [-43.35, -22.85],
                        [-43.40, -22.82],
                        [-43.43, -22.79],
                        [-43.45, -22.75]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Oeste",
                    "zona_id": 4,
                    "nivel": "Muito Alto"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.73, -22.85],
                        [-43.45, -22.75],
                        [-43.43, -22.79],
                        [-43.40, -22.82],
                        [-43.35, -22.85],
                        [-43.30, -22.87],
                        [-43.25, -22.88],
                        [-43.22, -22.91],
                        [-43.21, -22.93],
                        [-43.22, -22.94],
                        [-43.24, -22.96],
                        [-43.26, -22.99],
                        [-43.30, -23.01],
                        [-43.36, -23.03],
                        [-43.45, -23.06],
                        [-43.55, -23.08],
                        [-43.65, -23.08],
                        [-43.73, -23.05],
                        [-43.75, -22.98],
                        [-43.73, -22.90],
                        [-43.73, -22.85]
                    ]]
                }
            }
        ]
    }
    
    return geojson

def salvar_geojson(data, caminho):
    """Salva GeoJSON em arquivo"""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Salvo: {caminho}")

if __name__ == "__main__":
    print("🗺️ Buscando dados geográficos do Rio de Janeiro...\n")
    
    # Tentar baixar dados oficiais
    dados = tentar_baixar_geojson()
    
    output_dir = Path(__file__).parent.parent / "data" / "shapefiles"
    
    # Salvar dados baixados
    for nome, geojson in dados.items():
        filename = nome.lower().replace(" ", "_").replace("-", "_") + ".geojson"
        salvar_geojson(geojson, output_dir / filename)
    
    # Criar versão simplificada mas mais realista
    print("\n📐 Criando GeoJSON simplificado realista...")
    geojson_realista = criar_geojson_simplificado_realista()
    salvar_geojson(geojson_realista, output_dir / "zonas_rio_realista.geojson")
    
    print("\n✅ Processo concluído!")
    print(f"📁 Arquivos salvos em: {output_dir}")


