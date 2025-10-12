"""
🗺️ Download de GeoJSON Oficial do Rio de Janeiro
=================================================

Script para baixar dados geográficos oficiais das Regiões Administrativas
do município do Rio de Janeiro.
"""

import requests
import json
from pathlib import Path

def download_regioes_administrativas():
    """
    Tenta baixar GeoJSON oficial das Regiões Administrativas do Rio de Janeiro
    Fontes: Data.Rio, GitHub do IPP, outros repositórios oficiais
    """
    
    # URLs alternativas de fontes oficiais
    urls_alternativas = [
        # Data.Rio (Prefeitura do Rio)
        "https://www.data.rio/datasets/49d8e983fe3944a9bb42c3f1c5d39e8c_0.geojson",
        "https://opendata.arcgis.com/datasets/49d8e983fe3944a9bb42c3f1c5d39e8c_0.geojson",
        
        # GitHub IPP Rio
        "https://raw.githubusercontent.com/prefeitura-rio/storage/master/layers/regioes_administrativas.geojson",
        
        # Brasil.io
        "https://raw.githubusercontent.com/turicas/covid19-br/master/data/geodata/rio-de-janeiro/regioes-administrativas.geojson",
    ]
    
    print("🔍 Tentando baixar GeoJSON oficial das Regiões Administrativas...")
    
    for idx, url in enumerate(urls_alternativas, 1):
        try:
            print(f"\n📥 Tentativa {idx}/{len(urls_alternativas)}")
            print(f"URL: {url}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                geojson_data = response.json()
                
                # Verificar se é um GeoJSON válido
                if geojson_data.get('type') == 'FeatureCollection':
                    print(f"✅ GeoJSON baixado com sucesso!")
                    print(f"📊 Número de features: {len(geojson_data.get('features', []))}")
                    return geojson_data
                    
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    print("\n⚠️ Não foi possível baixar dados oficiais.")
    print("💡 Usando GeoJSON simplificado local.")
    return None

def salvar_geojson(geojson_data, output_path):
    """Salva GeoJSON em arquivo"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 GeoJSON salvo em: {output_path}")

if __name__ == "__main__":
    # Caminho de saída
    output_dir = Path(__file__).parent.parent / "data" / "shapefiles"
    output_file = output_dir / "regioes_administrativas_oficial.geojson"
    
    # Tentar baixar
    geojson = download_regioes_administrativas()
    
    if geojson:
        salvar_geojson(geojson, output_file)
        print("\n🎉 Download concluído com sucesso!")
    else:
        print("\n❌ Download falhou. Mantenha o GeoJSON simplificado atual.")


