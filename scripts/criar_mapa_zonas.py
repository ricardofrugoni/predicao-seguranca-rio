"""
🗺️ Criar Mapa de Zonas do Rio de Janeiro
========================================

Cria um GeoJSON simplificado com as 4 zonas do município
usando o limite municipal do IBGE como base.
"""

import requests
import json
from pathlib import Path

def baixar_limite_municipal():
    """Baixa limite municipal do Rio de Janeiro do IBGE"""
    url = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3304557?formato=application/vnd.geo+json"
    
    print("📥 Baixando limite municipal do Rio de Janeiro (IBGE)...")
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        print("✅ Limite municipal baixado com sucesso!")
        return response.json()
    else:
        print(f"❌ Erro: {response.status_code}")
        return None

def criar_zonas_simplificadas(limite_municipal):
    """
    Cria GeoJSON com as 4 zonas principais do Rio
    Divide o município em quadrantes aproximados
    """
    
    # Coordenadas aproximadas para dividir as zonas
    # Centro: região central
    # Zona Sul: sul do centro
    # Zona Norte: norte do centro  
    # Zona Oeste: oeste
    
    zonas_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nome": "Centro",
                    "zona_id": 1,
                    "populacao": 450000,
                    "nivel": "Médio"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.23, -22.88],
                        [-43.16, -22.88],
                        [-43.16, -22.94],
                        [-43.23, -22.94],
                        [-43.23, -22.88]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Sul",
                    "zona_id": 2,
                    "populacao": 380000,
                    "nivel": "Baixo"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.30, -22.94],
                        [-43.16, -22.94],
                        [-43.16, -23.02],
                        [-43.30, -23.02],
                        [-43.30, -22.94]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Norte",
                    "zona_id": 3,
                    "populacao": 2400000,
                    "nivel": "Alto"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.50, -22.75],
                        [-43.10, -22.75],
                        [-43.10, -22.88],
                        [-43.50, -22.88],
                        [-43.50, -22.75]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nome": "Zona Oeste",
                    "zona_id": 4,
                    "populacao": 2500000,
                    "nivel": "Muito Alto"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-43.75, -22.85],
                        [-43.30, -22.85],
                        [-43.30, -23.10],
                        [-43.75, -23.10],
                        [-43.75, -22.85]
                    ]]
                }
            }
        ]
    }
    
    return zonas_geojson

def salvar_geojson(geojson_data, caminho):
    """Salva GeoJSON em arquivo"""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Salvo em: {caminho}")

if __name__ == "__main__":
    # Baixar limite municipal
    limite = baixar_limite_municipal()
    
    if limite:
        # Salvar limite municipal
        output_dir = Path(__file__).parent.parent / "data" / "shapefiles"
        salvar_geojson(limite, output_dir / "limite_municipal_rio.geojson")
    
    # Criar zonas simplificadas
    zonas = criar_zonas_simplificadas(limite)
    salvar_geojson(zonas, output_dir / "zonas_rio.geojson")
    
    print("\n🎉 GeoJSONs criados com sucesso!")
    print("✅ limite_municipal_rio.geojson - Limite do município")
    print("✅ zonas_rio.geojson - 4 zonas principais")

