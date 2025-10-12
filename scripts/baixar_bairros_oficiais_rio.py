"""
Baixar dados OFICIAIS dos bairros do município do Rio de Janeiro
Fonte: Data.Rio (Portal oficial da Prefeitura)
"""

import requests
import json
from pathlib import Path
import geopandas as gpd

print("🗺️ Buscando dados oficiais dos BAIRROS do Rio de Janeiro\n")

# URLs de fontes oficiais
sources = [
    {
        "name": "Data.Rio - Bairros Cariocas",
        "url": "https://www.data.rio/api/geospatial/c5k3-9hae?method=export&format=GeoJSON",
        "type": "geojson"
    },
    {
        "name": "IBGE - Setores Censitários RJ",
        "url": "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3304557?formato=application/vnd.geo+json&qualidade=minima",
        "type": "geojson"
    },
    {
        "name": "GitHub - Bairros RJ (tbrugz)",
        "url": "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun.json",
        "type": "geojson"
    },
    {
        "name": "Brasil.io - Rio Bairros",
        "url": "https://data.brasil.io/dataset/covid19/geojs-33-mun.json",
        "type": "geojson"
    }
]

output_dir = Path("data/shapefiles")
output_dir.mkdir(parents=True, exist_ok=True)

sucesso = False

for source in sources:
    try:
        print(f"📥 Tentando: {source['name']}")
        print(f"   URL: {source['url']}")
        
        response = requests.get(source['url'], timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('type') == 'FeatureCollection':
                features = len(data.get('features', []))
                print(f"   ✅ Sucesso! {features} features encontradas\n")
                
                # Salvar
                filename = f"bairros_rio_oficial_{source['name'].split()[0].lower()}.geojson"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"   💾 Salvo: {filepath}\n")
                sucesso = True
                break
            else:
                print(f"   ⚠️ Não é GeoJSON válido\n")
        else:
            print(f"   ❌ Status {response.status_code}\n")
            
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}\n")

if not sucesso:
    print("\n⚠️ Não foi possível baixar dados oficiais.")
    print("📝 Criando GeoJSON simulado com estrutura real dos bairros...\n")
    
    # Criar GeoJSON simulado mais realista
    # Vou criar com os principais bairros do Rio usando coordenadas aproximadas
    
    bairros_principais = [
        # ZONA SUL
        {"nome": "Copacabana", "zona": "Zona Sul", "lat": -22.9711, "lon": -43.1822, "nivel": "Baixo"},
        {"nome": "Ipanema", "zona": "Zona Sul", "lat": -22.9838, "lon": -43.2048, "nivel": "Muito Baixo"},
        {"nome": "Leblon", "zona": "Zona Sul", "lat": -22.9844, "lon": -43.2286, "nivel": "Muito Baixo"},
        {"nome": "Botafogo", "zona": "Zona Sul", "lat": -22.9467, "lon": -43.1829, "nivel": "Baixo"},
        {"nome": "Flamengo", "zona": "Zona Sul", "lat": -22.9311, "lon": -43.1755, "nivel": "Baixo"},
        {"nome": "Laranjeiras", "zona": "Zona Sul", "lat": -22.9343, "lon": -43.1870, "nivel": "Médio"},
        {"nome": "Gávea", "zona": "Zona Sul", "lat": -22.9794, "lon": -43.2445, "nivel": "Baixo"},
        {"nome": "Lagoa", "zona": "Zona Sul", "lat": -22.9714, "lon": -43.2056, "nivel": "Baixo"},
        
        # CENTRO
        {"nome": "Centro", "zona": "Centro", "lat": -22.9035, "lon": -43.2096, "nivel": "Médio"},
        {"nome": "Lapa", "zona": "Centro", "lat": -22.9133, "lon": -43.1796, "nivel": "Alto"},
        {"nome": "Santa Teresa", "zona": "Centro", "lat": -22.9190, "lon": -43.1890, "nivel": "Médio"},
        {"nome": "Saúde", "zona": "Centro", "lat": -22.8953, "lon": -43.1914, "nivel": "Alto"},
        
        # ZONA NORTE
        {"nome": "Tijuca", "zona": "Zona Norte", "lat": -22.9186, "lon": -43.2341, "nivel": "Médio"},
        {"nome": "Vila Isabel", "zona": "Zona Norte", "lat": -22.9169, "lon": -43.2486, "nivel": "Médio"},
        {"nome": "Maracanã", "zona": "Zona Norte", "lat": -22.9121, "lon": -43.2302, "nivel": "Alto"},
        {"nome": "Méier", "zona": "Zona Norte", "lat": -22.9025, "lon": -43.2783, "nivel": "Alto"},
        {"nome": "Engenho Novo", "zona": "Zona Norte", "lat": -22.9043, "lon": -43.2631, "nivel": "Alto"},
        {"nome": "Cachambi", "zona": "Zona Norte", "lat": -22.8965, "lon": -43.2714, "nivel": "Alto"},
        {"nome": "Penha", "zona": "Zona Norte", "lat": -22.8412, "lon": -43.2841, "nivel": "Muito Alto"},
        {"nome": "Irajá", "zona": "Zona Norte", "lat": -22.8326, "lon": -43.3263, "nivel": "Muito Alto"},
        {"nome": "Madureira", "zona": "Zona Norte", "lat": -22.8711, "lon": -43.3364, "nivel": "Muito Alto"},
        {"nome": "Cascadura", "zona": "Zona Norte", "lat": -22.8855, "lon": -43.3295, "nivel": "Alto"},
        
        # ZONA OESTE
        {"nome": "Barra da Tijuca", "zona": "Zona Oeste", "lat": -23.0051, "lon": -43.3647, "nivel": "Baixo"},
        {"nome": "Recreio", "zona": "Zona Oeste", "lat": -23.0206, "lon": -43.4647, "nivel": "Médio"},
        {"nome": "Campo Grande", "zona": "Zona Oeste", "lat": -22.9008, "lon": -43.5618, "nivel": "Muito Alto"},
        {"nome": "Bangu", "zona": "Zona Oeste", "lat": -22.8789, "lon": -43.4659, "nivel": "Muito Alto"},
        {"nome": "Realengo", "zona": "Zona Oeste", "lat": -22.8806, "lon": -43.4300, "nivel": "Alto"},
        {"nome": "Santa Cruz", "zona": "Zona Oeste", "lat": -22.9194, "lon": -43.6842, "nivel": "Muito Alto"},
        {"nome": "Jacarepaguá", "zona": "Zona Oeste", "lat": -22.9331, "lon": -43.3641, "nivel": "Alto"},
    ]
    
    # Criar features GeoJSON para cada bairro (polígonos aproximados)
    features = []
    
    cores_niveis = {
        "Muito Baixo": "#27ae60",
        "Baixo": "#2ecc71",
        "Médio": "#f39c12",
        "Alto": "#e67e22",
        "Muito Alto": "#e74c3c"
    }
    
    for bairro in bairros_principais:
        # Criar um polígono aproximado ao redor do ponto central
        offset = 0.015  # ~1.5km
        coords = [
            [bairro["lon"] - offset, bairro["lat"] - offset],
            [bairro["lon"] + offset, bairro["lat"] - offset],
            [bairro["lon"] + offset, bairro["lat"] + offset],
            [bairro["lon"] - offset, bairro["lat"] + offset],
            [bairro["lon"] - offset, bairro["lat"] - offset]
        ]
        
        feature = {
            "type": "Feature",
            "properties": {
                "nome": bairro["nome"],
                "zona": bairro["zona"],
                "nivel": bairro["nivel"],
                "cor": cores_niveis[bairro["nivel"]],
                "municipio": "Rio de Janeiro"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        }
        features.append(feature)
    
    geojson_simulado = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Salvar
    filepath = output_dir / "bairros_rio_simulado.geojson"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(geojson_simulado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ GeoJSON simulado criado!")
    print(f"📁 Arquivo: {filepath}")
    print(f"📊 {len(features)} bairros principais do município")

print("\n✅ Processo concluído!")


