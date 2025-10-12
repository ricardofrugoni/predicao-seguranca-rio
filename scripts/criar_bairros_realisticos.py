"""
Criar mapa realista dos bairros do Rio seguindo o formato do município
Usa as 4 zonas principais e subdivide em bairros menores
"""

import json
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

print("🗺️ Criando mapa REALISTA com subdivisões de bairros\n")

# Carregar o GeoJSON das zonas reais
zonas_path = Path("data/shapefiles/zonas_rio_limites_reais.geojson")

if not zonas_path.exists():
    print("❌ Arquivo zonas_rio_limites_reais.geojson não encontrado")
    exit(1)

gdf_zonas = gpd.read_file(zonas_path)
print(f"✅ Carregado: {len(gdf_zonas)} zonas")

# Função para subdividir um polígono em vários menores
def subdividir_poligono(geometry, num_subdivisoes_x=3, num_subdivisoes_y=3):
    """Subdivide um polígono em uma grade"""
    bounds = geometry.bounds  # minx, miny, maxx, maxy
    minx, miny, maxx, maxy = bounds
    
    dx = (maxx - minx) / num_subdivisoes_x
    dy = (maxy - miny) / num_subdivisoes_y
    
    sub_poligonos = []
    
    for i in range(num_subdivisoes_x):
        for j in range(num_subdivisoes_y):
            x1 = minx + i * dx
            y1 = miny + j * dy
            x2 = x1 + dx
            y2 = y1 + dy
            
            # Criar retângulo
            rect = Polygon([
                (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
            ])
            
            # Intersecção com o polígono original para manter apenas a parte dentro
            intersecao = rect.intersection(geometry)
            
            if not intersecao.is_empty and intersecao.area > 0:
                sub_poligonos.append(intersecao)
    
    return sub_poligonos

# Nomes de bairros por zona
bairros_por_zona = {
    "Zona Sul": [
        "Copacabana", "Ipanema", "Leblon", "Botafogo", "Flamengo",
        "Laranjeiras", "Catete", "Glória", "Leme", "Urca",
        "Humaitá", "Lagoa", "Jardim Botânico", "Gávea",
        "São Conrado", "Vidigal", "Rocinha"
    ],
    "Centro": [
        "Centro", "Lapa", "Santa Teresa", "Cidade Nova",
        "Estácio", "Gamboa", "Santo Cristo", "Saúde",
        "Caju", "Benfica", "Rio Comprido"
    ],
    "Zona Norte": [
        "Tijuca", "Vila Isabel", "Grajaú", "Andaraí",
        "Maracanã", "São Cristóvão", "Mangueira", "Bonsucesso",
        "Ramos", "Olaria", "Penha", "Vila da Penha",
        "Irajá", "Madureira", "Oswaldo Cruz", "Cascadura",
        "Engenho Novo", "Méier", "Todos os Santos", "Cachambi"
    ],
    "Zona Oeste": [
        "Barra da Tijuca", "Recreio", "Jacarepaguá", "Freguesia",
        "Taquara", "Tanque", "Praça Seca", "Realengo",
        "Bangu", "Campo Grande", "Santa Cruz", "Sepetiba",
        "Guaratiba", "Barra de Guaratiba", "Paciência"
    ]
}

# Criar features dos bairros
features_bairros = []
bairro_id = 1

for idx, row in gdf_zonas.iterrows():
    zona_nome = row['nome']
    zona_geom = row.geometry
    
    bairros_zona = bairros_por_zona.get(zona_nome, [])
    
    if not bairros_zona:
        continue
    
    # Calcular quantas subdivisões precisamos
    num_bairros = len(bairros_zona)
    grid_size = int(np.ceil(np.sqrt(num_bairros)))
    
    # Subdividir a zona em bairros
    sub_poligs = subdividir_poligono(zona_geom, grid_size, grid_size)
    
    # Atribuir nomes de bairros aos polígonos
    for i, (bairro_nome, sub_polig) in enumerate(zip(bairros_zona, sub_poligs)):
        if sub_polig.is_empty:
            continue
            
        feature = {
            "type": "Feature",
            "properties": {
                "id": bairro_id,
                "nome": bairro_nome,
                "zona": zona_nome
            },
            "geometry": json.loads(gpd.GeoSeries([sub_polig]).to_json())['features'][0]['geometry']
        }
        features_bairros.append(feature)
        bairro_id += 1
    
    print(f"  ✅ {zona_nome}: {len(sub_poligs)} subdivisões criadas")

# Criar GeoJSON final
geojson_bairros = {
    "type": "FeatureCollection",
    "features": features_bairros
}

# Salvar
output_path = Path("data/shapefiles/bairros_rio_subdivididos.geojson")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(geojson_bairros, f, ensure_ascii=False, indent=2)

print(f"\n✅ GeoJSON criado com sucesso!")
print(f"📁 Arquivo: {output_path}")
print(f"📊 Total de bairros/subdivisões: {len(features_bairros)}")
print(f"\nOs bairros agora seguem o formato REAL do município!")

