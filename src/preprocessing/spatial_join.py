"""
Módulo para processamento geoespacial e join espacial de dados
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpatialProcessor:
    """
    Classe para processamento geoespacial e join espacial
    """
    
    def __init__(self, crs: str = 'EPSG:4326'):
        self.crs = crs
        
    def load_shapefiles(self, shapefile_dir: str) -> Dict[str, gpd.GeoDataFrame]:
        """
        Carrega shapefiles de diferentes fontes
        
        Args:
            shapefile_dir: Diretório com shapefiles
            
        Returns:
            Dicionário com GeoDataFrames carregados
        """
        logger.info(f"Carregando shapefiles de: {shapefile_dir}")
        
        shapefiles = {}
        shapefile_path = Path(shapefile_dir)
        
        # Lista arquivos GeoJSON
        for file_path in shapefile_path.glob('*.geojson'):
            try:
                gdf = gpd.read_file(file_path)
                gdf = gdf.to_crs(self.crs)
                shapefiles[file_path.stem] = gdf
                logger.info(f"Shapefile carregado: {file_path.name}")
            except Exception as e:
                logger.error(f"Erro ao carregar {file_path.name}: {e}")
        
        return shapefiles
    
    def create_point_geometry(self, df: pd.DataFrame, lon_col: str, lat_col: str) -> gpd.GeoDataFrame:
        """
        Cria GeoDataFrame a partir de coordenadas
        
        Args:
            df: DataFrame com coordenadas
            lon_col: Nome da coluna de longitude
            lat_col: Nome da coluna de latitude
            
        Returns:
            GeoDataFrame com geometrias de ponto
        """
        logger.info("Criando geometrias de ponto")
        
        # Cria geometrias de ponto
        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        
        # Cria GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=self.crs)
        
        logger.info(f"GeoDataFrame criado com {len(gdf)} pontos")
        return gdf
    
    def spatial_join_crimes_regions(self, crimes_gdf: gpd.GeoDataFrame, 
                                  regions_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Faz join espacial entre crimes e regiões administrativas
        
        Args:
            crimes_gdf: GeoDataFrame com dados de crimes
            regions_gdf: GeoDataFrame com regiões administrativas
            
        Returns:
            GeoDataFrame com join espacial
        """
        logger.info("Executando join espacial entre crimes e regiões")
        
        # Garante que ambos estão no mesmo CRS
        if crimes_gdf.crs != regions_gdf.crs:
            crimes_gdf = crimes_gdf.to_crs(regions_gdf.crs)
        
        # Executa join espacial
        joined_gdf = gpd.sjoin(crimes_gdf, regions_gdf, how='left', predicate='within')
        
        logger.info(f"Join espacial concluído: {len(joined_gdf)} registros")
        return joined_gdf
    
    def calculate_spatial_features(self, gdf: gpd.GeoDataFrame, 
                                  reference_points: List[Tuple[float, float]]) -> gpd.GeoDataFrame:
        """
        Calcula features espaciais (distâncias, densidades, etc.)
        
        Args:
            gdf: GeoDataFrame com dados
            reference_points: Lista de pontos de referência (lon, lat)
            
        Returns:
            GeoDataFrame com features espaciais
        """
        logger.info("Calculando features espaciais")
        
        # Calcula distâncias para pontos de referência
        for i, (lon, lat) in enumerate(reference_points):
            ref_point = Point(lon, lat)
            gdf[f'distancia_ponto_{i+1}'] = gdf.geometry.distance(ref_point)
        
        # Calcula centroide de cada região
        if gdf.geometry.geom_type.iloc[0] in ['Polygon', 'MultiPolygon']:
            gdf['centroide_lon'] = gdf.geometry.centroid.x
            gdf['centroide_lat'] = gdf.geometry.centroid.y
        
        # Calcula área (se for polígono)
        if gdf.geometry.geom_type.iloc[0] in ['Polygon', 'MultiPolygon']:
            gdf['area_km2'] = gdf.geometry.area / 1000000  # Converte para km²
        
        # Calcula perímetro (se for polígono)
        if gdf.geometry.geom_type.iloc[0] in ['Polygon', 'MultiPolygon']:
            gdf['perimetro_km'] = gdf.geometry.length / 1000  # Converte para km
        
        logger.info("Features espaciais calculadas")
        return gdf
    
    def create_grid_cells(self, bounds: Tuple[float, float, float, float], 
                         cell_size: float = 0.01) -> gpd.GeoDataFrame:
        """
        Cria grid de células para análise espacial
        
        Args:
            bounds: Limites (minx, miny, maxx, maxy)
            cell_size: Tamanho da célula em graus
            
        Returns:
            GeoDataFrame com grid
        """
        logger.info("Criando grid de células")
        
        minx, miny, maxx, maxy = bounds
        
        # Cria grid
        x_coords = np.arange(minx, maxx, cell_size)
        y_coords = np.arange(miny, maxy, cell_size)
        
        cells = []
        for i, x in enumerate(x_coords[:-1]):
            for j, y in enumerate(y_coords[:-1]):
                # Cria polígono da célula
                cell_polygon = Polygon([
                    (x, y),
                    (x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    (x, y + cell_size),
                    (x, y)
                ])
                
                cells.append({
                    'cell_id': f"{i}_{j}",
                    'geometry': cell_polygon
                })
        
        grid_gdf = gpd.GeoDataFrame(cells, crs=self.crs)
        logger.info(f"Grid criado com {len(grid_gdf)} células")
        
        return grid_gdf
    
    def aggregate_by_region(self, gdf: gpd.GeoDataFrame, 
                           group_columns: List[str]) -> gpd.GeoDataFrame:
        """
        Agrega dados por região administrativa
        
        Args:
            gdf: GeoDataFrame com dados
            group_columns: Colunas para agrupamento
            
        Returns:
            GeoDataFrame agregado
        """
        logger.info("Agregando dados por região")
        
        # Agrupa por região e calcula estatísticas
        agg_dict = {
            'total_ocorrencias': 'sum',
            'populacao': 'first',
            'taxa_100k': 'mean'
        }
        
        # Adiciona colunas numéricas para agregação
        numeric_columns = gdf.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col not in agg_dict:
                agg_dict[col] = 'sum'
        
        # Agrega dados
        aggregated = gdf.groupby(group_columns).agg(agg_dict).reset_index()
        
        # Mantém geometria da primeira ocorrência de cada região
        geometry_dict = gdf.groupby(group_columns)['geometry'].first().to_dict()
        aggregated['geometry'] = aggregated[group_columns].apply(
            lambda x: geometry_dict[tuple(x)], axis=1
        )
        
        # Cria GeoDataFrame
        result_gdf = gpd.GeoDataFrame(aggregated, crs=gdf.crs)
        
        logger.info(f"Dados agregados: {len(result_gdf)} regiões")
        return result_gdf
    
    def calculate_density_metrics(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Calcula métricas de densidade
        
        Args:
            gdf: GeoDataFrame com dados
            
        Returns:
            GeoDataFrame com métricas de densidade
        """
        logger.info("Calculando métricas de densidade")
        
        # Densidade populacional
        if 'populacao' in gdf.columns and 'area_km2' in gdf.columns:
            gdf['densidade_populacional'] = gdf['populacao'] / gdf['area_km2']
        
        # Densidade de crimes
        if 'total_ocorrencias' in gdf.columns and 'area_km2' in gdf.columns:
            gdf['densidade_crimes'] = gdf['total_ocorrencias'] / gdf['area_km2']
        
        # Densidade de crimes por população
        if 'total_ocorrencias' in gdf.columns and 'populacao' in gdf.columns:
            gdf['densidade_crimes_pop'] = gdf['total_ocorrencias'] / gdf['populacao']
        
        logger.info("Métricas de densidade calculadas")
        return gdf
    
    def create_buffer_zones(self, gdf: gpd.GeoDataFrame, 
                          buffer_distance: float) -> gpd.GeoDataFrame:
        """
        Cria zonas de buffer
        
        Args:
            gdf: GeoDataFrame com dados
            buffer_distance: Distância do buffer em metros
            
        Returns:
            GeoDataFrame com buffers
        """
        logger.info(f"Criando buffers de {buffer_distance}m")
        
        # Converte para CRS métrico se necessário
        if gdf.crs != 'EPSG:3857':
            gdf_metric = gdf.to_crs('EPSG:3857')
        else:
            gdf_metric = gdf.copy()
        
        # Cria buffers
        gdf_metric['buffer_geometry'] = gdf_metric.geometry.buffer(buffer_distance)
        
        # Converte de volta para CRS original
        gdf_metric = gdf_metric.to_crs(gdf.crs)
        
        logger.info("Buffers criados")
        return gdf_metric
    
    def export_geodataframe(self, gdf: gpd.GeoDataFrame, 
                           output_path: str, 
                           format: str = 'geojson') -> None:
        """
        Exporta GeoDataFrame para arquivo
        
        Args:
            gdf: GeoDataFrame para exportar
            output_path: Caminho do arquivo de saída
            format: Formato de saída (geojson, shapefile, etc.)
        """
        logger.info(f"Exportando GeoDataFrame para: {output_path}")
        
        if format.lower() == 'geojson':
            gdf.to_file(output_path, driver='GeoJSON')
        elif format.lower() == 'shapefile':
            gdf.to_file(output_path, driver='ESRI Shapefile')
        else:
            raise ValueError(f"Formato não suportado: {format}")
        
        logger.info("Exportação concluída")

def main():
    """
    Função principal para teste do módulo
    """
    # Exemplo de uso
    processor = SpatialProcessor()
    
    # Cria dados de exemplo
    sample_data = {
        'regiao_administrativa': ['Centro', 'Zona Sul', 'Zona Norte'],
        'total_ocorrencias': [100, 200, 150],
        'populacao': [100000, 200000, 300000],
        'longitude': [-43.2, -43.1, -43.0],
        'latitude': [-22.9, -22.8, -22.7]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Cria GeoDataFrame
    gdf = processor.create_point_geometry(df, 'longitude', 'latitude')
    
    # Calcula features espaciais
    reference_points = [(-43.2, -22.9), (-43.1, -22.8)]
    gdf = processor.calculate_spatial_features(gdf, reference_points)
    
    print("GeoDataFrame criado:")
    print(gdf.head())
    
    print("\nFeatures espaciais:")
    print(gdf[['distancia_ponto_1', 'distancia_ponto_2']].head())

if __name__ == "__main__":
    main()

