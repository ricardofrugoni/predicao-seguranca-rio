"""
🗺️ Buscar Dados Oficiais do Município do Rio de Janeiro
=======================================================

Busca shapefiles/GeoJSON oficiais com divisões administrativas reais.
"""

import requests
import json
from pathlib import Path
import time

def buscar_data_rio():
    """Busca no portal Data.Rio (oficial da Prefeitura)"""
    
    # IDs conhecidos de datasets do Data.Rio
    datasets = {
        "limite_bairros": "https://www.data.rio/api/views/g42k-v7r8/rows.geojson",
        "regioes_planejamento": "https://www.data.rio/api/geospatial/g42k-v7r8?method=export&format=GeoJSON",
        "limite_municipal_2": "https://www.data.rio/api/geospatial/2qwa-jpkh?method=export&format=GeoJSON",
    }
    
    resultados = {}
    
    for nome, url in datasets.items():
        try:
            print(f"\n📥 Tentando baixar: {nome}")
            print(f"   URL: {url}")
            
            response = requests.get(url, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and data.get('type') == 'FeatureCollection':
                        features = len(data.get('features', []))
                        print(f"   ✅ Sucesso! {features} features encontradas")
                        resultados[nome] = data
                    else:
                        print(f"   ⚠️ Formato não reconhecido")
                except Exception as e:
                    print(f"   ❌ Erro ao processar: {e}")
            else:
                print(f"   ❌ Falha no download")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        time.sleep(1)  # Pausa entre requisições
    
    return resultados

def buscar_github_brasil():
    """Busca em repositórios do GitHub com dados do Brasil"""
    
    repos = [
        {
            "nome": "Rio Bairros (tbrugz)",
            "url": "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun.json"
        },
        {
            "nome": "Brasil Geodata",
            "url": "https://raw.githubusercontent.com/datasets-br/state-codes/master/data/br-rj-cities.csv"
        }
    ]
    
    resultados = {}
    
    for repo in repos:
        try:
            print(f"\n📥 Tentando: {repo['nome']}")
            response = requests.get(repo['url'], timeout=30)
            
            if response.status_code == 200:
                print(f"   ✅ Baixado!")
                # Processar conforme formato
                if repo['url'].endswith('.json') or repo['url'].endswith('.geojson'):
                    try:
                        data = response.json()
                        resultados[repo['nome']] = data
                    except:
                        pass
                        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return resultados

def criar_geojson_bairros_simplificado():
    """
    Cria GeoJSON com divisões mais detalhadas do município
    Baseado nas Regiões de Planejamento e principais bairros
    """
    
    # Vou criar polígonos mais detalhados para principais áreas
    # Estas são aproximações das áreas reais
    
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Definir áreas principais com mais detalhes
    areas = [
        # ZONA SUL
        {
            "nome": "Copacabana/Leme",
            "nivel": "Médio",
            "coords": [
                [-43.190, -22.960], [-43.165, -22.960], [-43.165, -22.975],
                [-43.175, -22.985], [-43.190, -22.980], [-43.190, -22.960]
            ]
        },
        {
            "nome": "Ipanema/Leblon",
            "nivel": "Baixo",
            "coords": [
                [-43.230, -22.975], [-43.190, -22.975], [-43.190, -22.995],
                [-43.220, -23.010], [-43.240, -23.000], [-43.230, -22.975]
            ]
        },
        {
            "nome": "Botafogo/Flamengo",
            "nivel": "Baixo",
            "coords": [
                [-43.195, -22.935], [-43.170, -22.935], [-43.165, -22.955],
                [-43.175, -22.965], [-43.195, -22.960], [-43.195, -22.935]
            ]
        },
        {
            "nome": "Lagoa/Jardim Botânico",
            "nivel": "Baixo",
            "coords": [
                [-43.230, -22.960], [-43.205, -22.960], [-43.200, -22.975],
                [-43.215, -22.985], [-43.230, -22.980], [-43.230, -22.960]
            ]
        },
        {
            "nome": "Rocinha/São Conrado",
            "nivel": "Muito Alto",
            "coords": [
                [-43.260, -22.985], [-43.240, -22.985], [-43.240, -23.005],
                [-43.255, -23.010], [-43.260, -23.000], [-43.260, -22.985]
            ]
        },
        
        # CENTRO
        {
            "nome": "Centro Histórico",
            "nivel": "Alto",
            "coords": [
                [-43.195, -22.900], [-43.170, -22.900], [-43.170, -22.915],
                [-43.185, -22.920], [-43.195, -22.915], [-43.195, -22.900]
            ]
        },
        {
            "nome": "Zona Portuária",
            "nivel": "Médio",
            "coords": [
                [-43.190, -22.885], [-43.165, -22.885], [-43.165, -22.900],
                [-43.180, -22.905], [-43.190, -22.900], [-43.190, -22.885]
            ]
        },
        {
            "nome": "Santa Teresa/Lapa",
            "nivel": "Médio",
            "coords": [
                [-43.195, -22.915], [-43.180, -22.915], [-43.175, -22.930],
                [-43.185, -22.935], [-43.195, -22.930], [-43.195, -22.915]
            ]
        },
        
        # ZONA NORTE
        {
            "nome": "Tijuca",
            "nivel": "Médio",
            "coords": [
                [-43.250, -22.920], [-43.225, -22.920], [-43.220, -22.940],
                [-43.235, -22.945], [-43.250, -22.940], [-43.250, -22.920]
            ]
        },
        {
            "nome": "Vila Isabel/Grajaú",
            "nivel": "Médio",
            "coords": [
                [-43.265, -22.910], [-43.240, -22.910], [-43.240, -22.930],
                [-43.255, -22.935], [-43.265, -22.930], [-43.265, -22.910]
            ]
        },
        {
            "nome": "Maracanã/São Cristóvão",
            "nivel": "Médio",
            "coords": [
                [-43.235, -22.900], [-43.210, -22.900], [-43.210, -22.920],
                [-43.225, -22.925], [-43.235, -22.920], [-43.235, -22.900]
            ]
        },
        {
            "nome": "Méier/Todos os Santos",
            "nivel": "Médio",
            "coords": [
                [-43.300, -22.890], [-43.270, -22.890], [-43.265, -22.915],
                [-43.285, -22.920], [-43.300, -22.910], [-43.300, -22.890]
            ]
        },
        {
            "nome": "Madureira/Cascadura",
            "nivel": "Alto",
            "coords": [
                [-43.360, -22.860], [-43.330, -22.860], [-43.325, -22.885],
                [-43.345, -22.895], [-43.360, -22.885], [-43.360, -22.860]
            ]
        },
        {
            "nome": "Penha/Complexo do Alemão",
            "nivel": "Muito Alto",
            "coords": [
                [-43.295, -22.840], [-43.265, -22.840], [-43.260, -22.870],
                [-43.280, -22.880], [-43.295, -22.870], [-43.295, -22.840]
            ]
        },
        {
            "nome": "Maré",
            "nivel": "Muito Alto",
            "coords": [
                [-43.260, -22.840], [-43.230, -22.840], [-43.225, -22.865],
                [-43.245, -22.870], [-43.260, -22.865], [-43.260, -22.840]
            ]
        },
        {
            "nome": "Ilha do Governador",
            "nivel": "Médio",
            "coords": [
                [-43.240, -22.790], [-43.200, -22.790], [-43.195, -22.825],
                [-43.220, -22.830], [-43.240, -22.820], [-43.240, -22.790]
            ]
        },
        
        # ZONA OESTE
        {
            "nome": "Barra da Tijuca",
            "nivel": "Baixo",
            "coords": [
                [-43.370, -22.985], [-43.300, -22.985], [-43.295, -23.025],
                [-43.340, -23.035], [-43.370, -23.020], [-43.370, -22.985]
            ]
        },
        {
            "nome": "Jacarepaguá",
            "nivel": "Alto",
            "coords": [
                [-43.395, -22.910], [-43.350, -22.910], [-43.345, -22.950],
                [-43.375, -22.960], [-43.395, -22.945], [-43.395, -22.910]
            ]
        },
        {
            "nome": "Cidade de Deus",
            "nivel": "Muito Alto",
            "coords": [
                [-43.380, -22.935], [-43.355, -22.935], [-43.350, -22.955],
                [-43.370, -22.960], [-43.380, -22.950], [-43.380, -22.935]
            ]
        },
        {
            "nome": "Bangu/Realengo",
            "nivel": "Muito Alto",
            "coords": [
                [-43.490, -22.850], [-43.425, -22.850], [-43.420, -22.900],
                [-43.465, -22.910], [-43.490, -22.890], [-43.490, -22.850]
            ]
        },
        {
            "nome": "Campo Grande",
            "nivel": "Muito Alto",
            "coords": [
                [-43.590, -22.875], [-43.520, -22.875], [-43.515, -22.930],
                [-43.565, -22.940], [-43.590, -22.920], [-43.590, -22.875]
            ]
        },
        {
            "nome": "Santa Cruz",
            "nivel": "Muito Alto",
            "coords": [
                [-43.720, -22.895], [-43.650, -22.895], [-43.645, -22.955],
                [-43.695, -22.965], [-43.720, -22.940], [-43.720, -22.895]
            ]
        },
        {
            "nome": "Guaratiba",
            "nivel": "Médio",
            "coords": [
                [-43.620, -23.035], [-43.555, -23.035], [-43.550, -23.085],
                [-43.595, -23.090], [-43.620, -23.070], [-43.620, -23.035]
            ]
        },
    ]
    
    # Converter para GeoJSON
    for area in areas:
        feature = {
            "type": "Feature",
            "properties": {
                "nome": area["nome"],
                "nivel": area["nivel"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [area["coords"]]
            }
        }
        geojson["features"].append(feature)
    
    return geojson

def salvar(data, caminho):
    """Salva JSON"""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Salvo: {caminho}")

if __name__ == "__main__":
    print("🗺️ Buscando Dados Oficiais do Rio de Janeiro\n")
    
    output_dir = Path(__file__).parent.parent / "data" / "shapefiles"
    
    # Tentar Data.Rio
    print("=" * 60)
    print("📍 Data.Rio (Portal Oficial)")
    print("=" * 60)
    dados_datario = buscar_data_rio()
    
    for nome, data in dados_datario.items():
        salvar(data, output_dir / f"{nome}.geojson")
    
    # Tentar GitHub
    print("\n" + "=" * 60)
    print("🐙 Repositórios GitHub")
    print("=" * 60)
    dados_github = buscar_github_brasil()
    
    for nome, data in dados_github.items():
        filename = nome.lower().replace(" ", "_") + ".geojson"
        salvar(data, output_dir / filename)
    
    # Criar versão detalhada
    print("\n" + "=" * 60)
    print("📐 Criando GeoJSON Detalhado")
    print("=" * 60)
    geojson_detalhado = criar_geojson_bairros_simplificado()
    salvar(geojson_detalhado, output_dir / "areas_detalhadas_rio.geojson")
    
    print("\n✅ Processo concluído!")
    print(f"📁 {output_dir}")

