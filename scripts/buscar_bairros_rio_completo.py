import requests
import json
from pathlib import Path

print("🗺️ Buscando dados completos dos bairros do Rio de Janeiro\n")

# Tentar diferentes fontes
sources = [
    {
        "name": "Brasil.io - Bairros RJ",
        "url": "https://raw.githubusercontent.com/turicas/covid19-br/master/data/geodata/rio-de-janeiro/bairros.geojson"
    },
    {
        "name": "GeoSampa - Rio Bairros",
        "url": "https://raw.githubusercontent.com/codinginbrazil/br-atlas/master/data/rio-de-janeiro/bairros.geojson"
    },
    {
        "name": "Pris Maps - Rio",
        "url": "https://raw.githubusercontent.com/prismaps/br-atlas/master/data/rio-de-janeiro/bairros.geojson"
    }
]

output_dir = Path("data/shapefiles")
output_dir.mkdir(parents=True, exist_ok=True)

for source in sources:
    try:
        print(f"📥 Tentando: {source['name']}")
        print(f"   URL: {source['url']}")
        
        response = requests.get(source['url'], timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('type') == 'FeatureCollection':
                features = len(data.get('features', []))
                print(f"   ✅ Sucesso! {features} features\n")
                
                # Salvar
                filename = source['name'].lower().replace(" ", "_").replace("-", "_") + ".geojson"
                filepath = output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"   💾 Salvo: {filepath}\n")
            else:
                print(f"   ⚠️ Não é GeoJSON válido\n")
        else:
            print(f"   ❌ Status {response.status_code}\n")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")

print("✅ Processo concluído!")


