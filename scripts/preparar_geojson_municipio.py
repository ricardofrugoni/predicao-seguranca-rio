import geopandas as gpd
import json
from pathlib import Path

# Carregar bairros
gdf = gpd.read_file('data/shapefiles/rio_bairros_(tbrugz).geojson')

print(f"Total de bairros: {len(gdf)}")
print(f"Bounds originais: {gdf.total_bounds}")

# Filtrar apenas município do Rio de Janeiro (coordenadas aproximadas)
# Rio de Janeiro município: lat -23.08 a -22.74, lon -43.80 a -43.09
rio_bounds = {
    'min_lon': -43.80,
    'max_lon': -43.09,
    'min_lat': -23.08,
    'max_lat': -22.74
}

# Filtrar geometrias dentro dos bounds do município
gdf_rio = gdf.cx[rio_bounds['min_lon']:rio_bounds['max_lon'], rio_bounds['min_lat']:rio_bounds['max_lat']]

print(f"\nBairros do município do Rio: {len(gdf_rio)}")
print(f"Bounds do município: {gdf_rio.total_bounds}")

# Adicionar dados de criminalidade fictícios por bairro
# Você pode substituir por dados reais depois
import random
random.seed(42)

niveis = ["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"]
cores = {
    "Muito Baixo": "#27ae60",
    "Baixo": "#2ecc71",
    "Médio": "#f39c12",
    "Alto": "#e67e22",
    "Muito Alto": "#e74c3c"
}

gdf_rio['nivel'] = [random.choice(niveis) for _ in range(len(gdf_rio))]
gdf_rio['cor'] = gdf_rio['nivel'].map(cores)
gdf_rio['nome'] = gdf_rio['name']

# Selecionar apenas colunas necessárias
gdf_final = gdf_rio[['nome', 'nivel', 'cor', 'geometry']]

# Salvar
output_path = Path('data/shapefiles/municipio_rio_bairros.geojson')
gdf_final.to_file(output_path, driver='GeoJSON')

print(f"\n✅ Arquivo salvo: {output_path}")
print(f"📊 {len(gdf_final)} bairros com dados de criminalidade")


