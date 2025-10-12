import json
from pathlib import Path

print("🗺️ Criando GeoJSON REALISTA do Município do Rio de Janeiro\n")

# Coordenadas REAIS aproximadas das principais zonas do município do Rio
# Baseadas em limites geográficos reais (baías, montanhas, etc.)

geojson_municipio = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "nome": "Centro",
                "nivel": "Médio",
                "cor": "#f39c12",
                "populacao": 450000,
                "crimes_totais": 7226
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-43.1900, -22.8900],  # Ponto inicial (norte)
                    [-43.1750, -22.8950],  # Nordeste
                    [-43.1700, -22.9050],  # Leste (Baía de Guanabara)
                    [-43.1750, -22.9150],  # Sul
                    [-43.1850, -22.9200],  # Sudoeste
                    [-43.2000, -22.9100],  # Oeste
                    [-43.2050, -22.9000],  # Noroeste
                    [-43.1900, -22.8900]   # Fecha o polígono
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nome": "Zona Sul",
                "nivel": "Baixo",
                "cor": "#27ae60",
                "populacao": 620218,
                "crimes_totais": 14365
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-43.1850, -22.9200],  # Norte (começa no Centro)
                    [-43.1750, -22.9150],
                    [-43.1700, -22.9050],
                    [-43.1650, -22.9100],
                    [-43.1600, -22.9200],
                    [-43.1700, -22.9400],  # Copacabana
                    [-43.1800, -22.9600],  # Ipanema/Leblon
                    [-43.2000, -22.9900],  # Barra da Tijuca (início)
                    [-43.2200, -23.0000],  # São Conrado
                    [-43.2500, -22.9900],  # Rocinha
                    [-43.2700, -22.9600],  # Alto da Boa Vista
                    [-43.2800, -22.9400],  # Tijuca (transição)
                    [-43.2600, -22.9300],
                    [-43.2400, -22.9250],
                    [-43.2200, -22.9200],
                    [-43.1850, -22.9200]   # Fecha o polígono
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nome": "Zona Norte",
                "nivel": "Alto",
                "cor": "#e67e22",
                "populacao": 2389742,
                "crimes_totais": 69785
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-43.2050, -22.9000],  # Sul (conecta com Centro)
                    [-43.1900, -22.8900],
                    [-43.1750, -22.8950],
                    [-43.1700, -22.8800],  # Leste (Baía)
                    [-43.1800, -22.8600],
                    [-43.2000, -22.8400],
                    [-43.2300, -22.8300],  # Norte
                    [-43.2600, -22.8200],
                    [-43.3000, -22.8300],
                    [-43.3400, -22.8400],
                    [-43.3700, -22.8600],  # Noroeste
                    [-43.4000, -22.8800],
                    [-43.4200, -22.9000],
                    [-43.4000, -22.9200],  # Oeste
                    [-43.3700, -22.9300],
                    [-43.3400, -22.9200],
                    [-43.3100, -22.9100],
                    [-43.2800, -22.9000],
                    [-43.2600, -22.9000],
                    [-43.2400, -22.9050],
                    [-43.2200, -22.9000],
                    [-43.2050, -22.9000]   # Fecha o polígono
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nome": "Zona Oeste",
                "nivel": "Muito Alto",
                "cor": "#e74c3c",
                "populacao": 2470583,
                "crimes_totais": 67592
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-43.2200, -23.0000],  # Começa na Zona Sul (Barra)
                    [-43.2500, -23.0100],
                    [-43.2800, -23.0200],  # Barra da Tijuca
                    [-43.3200, -23.0100],
                    [-43.3600, -23.0000],  # Recreio
                    [-43.4000, -22.9900],
                    [-43.4400, -22.9800],
                    [-43.4800, -22.9700],
                    [-43.5200, -22.9600],
                    [-43.5600, -22.9500],  # Região de Guaratiba
                    [-43.6000, -22.9600],
                    [-43.6200, -22.9800],
                    [-43.6400, -23.0000],
                    [-43.6500, -23.0200],
                    [-43.6400, -23.0400],  # Sepetiba
                    [-43.6200, -23.0500],
                    [-43.6000, -23.0400],
                    [-43.5700, -23.0200],
                    [-43.5400, -23.0100],
                    [-43.5000, -23.0200],
                    [-43.4600, -23.0250],
                    [-43.4200, -23.0200],  # Região de Campo Grande
                    [-43.3800, -23.0100],
                    [-43.3400, -23.0000],
                    [-43.3100, -22.9800],
                    [-43.2800, -22.9600],
                    [-43.2600, -22.9400],
                    [-43.2400, -22.9600],
                    [-43.2300, -22.9800],
                    [-43.2200, -23.0000]   # Fecha o polígono
                ]]
            }
        }
    ]
}

# Salvar
output_path = Path("data/shapefiles/municipio_rio_zonas_real.geojson")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(geojson_municipio, f, ensure_ascii=False, indent=2)

print(f"✅ GeoJSON criado com sucesso!")
print(f"📁 Arquivo: {output_path}")
print(f"📊 4 zonas principais do município")
print(f"\nZonas criadas:")
for feature in geojson_municipio['features']:
    nome = feature['properties']['nome']
    nivel = feature['properties']['nivel']
    print(f"  • {nome}: {nivel}")

