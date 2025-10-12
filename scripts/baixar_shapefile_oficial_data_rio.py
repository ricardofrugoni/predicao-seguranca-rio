"""
Baixar shapefile OFICIAL dos bairros do Rio de Janeiro
Fonte: Data.Rio (Portal de Dados Abertos da Prefeitura)
"""

import requests
import json
from pathlib import Path

print("🗺️ Buscando shapefile OFICIAL dos bairros do Rio de Janeiro\n")
print("📍 Fonte: Data.Rio (Prefeitura do Rio)\n")

# URLs oficiais do Data.Rio e IPP Rio
urls_oficiais = [
    {
        "nome": "Data.Rio - Limite de Bairros (2023)",
        "url": "https://www.data.rio/api/geospatial/gm28-de72?method=export&format=GeoJSON",
        "descricao": "Limites oficiais dos bairros cariocas"
    },
    {
        "nome": "Data.Rio - Bairros",  
        "url": "https://services.arcgis.com/mRbP9SHuaFMn0Jmq/arcgis/rest/services/Limite_de_bairros/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson",
        "descricao": "ArcGIS REST API - Bairros"
    },
    {
        "nome": "GitHub - Rio Datasets",
        "url": "https://raw.githubusercontent.com/CodeForBrazil/datasets/master/rio-de-janeiro/neighborhoods.geojson",
        "descricao": "Bairros do Rio (Code for Brazil)"
    },
    {
        "nome": "Brazil GeoJSON",
        "url": "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun-3304557-neighborhoods.json",
        "descricao": "Bairros do Rio de Janeiro"
    }
]

output_dir = Path("data/shapefiles")
output_dir.mkdir(parents=True, exist_ok=True)

sucesso = False

for fonte in urls_oficiais:
    try:
        print(f"📥 Tentando: {fonte['nome']}")
        print(f"   {fonte['descricao']}")
        print(f"   URL: {fonte['url'][:80]}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, application/geo+json'
        }
        
        response = requests.get(fonte['url'], timeout=30, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Verificar se é GeoJSON válido
                if data.get('type') == 'FeatureCollection':
                    features = data.get('features', [])
                    print(f"   ✅ SUCESSO! {len(features)} bairros encontrados!\n")
                    
                    # Salvar
                    filepath = output_dir / "bairros_rio_oficial.geojson"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"💾 Salvo em: {filepath}")
                    print(f"📊 Total de bairros: {len(features)}")
                    
                    # Mostrar alguns nomes de bairros
                    print(f"\n📍 Exemplos de bairros encontrados:")
                    for i, feat in enumerate(features[:10]):
                        props = feat.get('properties', {})
                        nome = props.get('nome') or props.get('NOME') or props.get('name') or f"Bairro {i+1}"
                        print(f"   • {nome}")
                    
                    if len(features) > 10:
                        print(f"   ... e mais {len(features) - 10} bairros")
                    
                    sucesso = True
                    break
                else:
                    print(f"   ⚠️ Resposta não é GeoJSON válido\n")
                    
            except json.JSONDecodeError:
                print(f"   ⚠️ Resposta não é JSON válido\n")
        else:
            print(f"   ❌ Falha no download\n")
            
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}\n")

if sucesso:
    print("\n" + "="*60)
    print("✅ SHAPEFILE OFICIAL BAIXADO COM SUCESSO!")
    print("="*60)
    print(f"\n📁 Arquivo salvo em: data/shapefiles/bairros_rio_oficial.geojson")
    print(f"🗺️ Pronto para usar no dashboard!")
else:
    print("\n" + "="*60)
    print("⚠️ NÃO FOI POSSÍVEL BAIXAR DADOS OFICIAIS")
    print("="*60)
    print("\nMotivos possíveis:")
    print("  • APIs do Data.Rio podem estar temporariamente indisponíveis")
    print("  • URLs podem ter mudado")
    print("  • Firewall/rede bloqueando acesso")
    print("\n💡 Solução alternativa:")
    print("  • Usando os dados locais das 4 zonas principais")
    print("  • Ou fazer download manual em: https://www.data.rio")


