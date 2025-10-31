"""
📊 DATA LOADER - Carregamento de Dados com POO
===============================================

Classe responsável por carregar e gerenciar dados do projeto.
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Optional, List, Dict, Union
from abc import ABC, abstractmethod
import logging

from src.config import config

# Logger
logger = logging.getLogger(__name__)


class BaseDataLoader(ABC):
    """Classe base abstrata para carregadores de dados"""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.config = config
    
    @abstractmethod
    def load(self) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """Método abstrato para carregar dados"""
        pass
    
    def _validate_data(self, df: pd.DataFrame) -> bool:
        """Valida dados carregados"""
        if df is None or df.empty:
            return False
        return True


class CrimeDataLoader(BaseDataLoader):
    """Carregador de dados de criminalidade"""
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.data_path = self.config.paths.DATA_PROCESSED
    
    def load(self, filename: Optional[str] = None) -> pd.DataFrame:
        """
        Carrega dados de criminalidade
        
        Args:
            filename: Nome do arquivo. Se None, gera dados simulados
            
        Returns:
            DataFrame com dados de criminalidade
            
        Raises:
            FileNotFoundError: Se arquivo especificado não existe
            ValueError: Se dados carregados estão inválidos
        """
        try:
            if filename:
                file_path = self.data_path / filename
                if file_path.exists():
                    logger.info(f"Carregando dados de: {file_path}")
                    df = pd.read_csv(file_path)
                    if self._validate_data(df):
                        logger.info(f"Dados carregados com sucesso: {len(df)} linhas")
                        return df
                    else:
                        raise ValueError(f"Dados inválidos em {filename}")
                else:
                    logger.warning(f"Arquivo não encontrado: {file_path}")
            
            # Retorna dados simulados se arquivo não existe
            logger.info("Gerando dados simulados")
            return self._generate_sample_data()
            
        except FileNotFoundError as e:
            logger.error(f"Arquivo não encontrado: {e}")
            raise
        except pd.errors.EmptyDataError as e:
            logger.error(f"Arquivo vazio: {e}")
            raise ValueError("Arquivo CSV está vazio")
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Gera dados de exemplo para demonstração"""
        import numpy as np
        from datetime import datetime, timedelta
        
        np.random.seed(42)
        
        # Gera 5 anos de dados mensais
        start_date = datetime(2020, 1, 1)
        dates = pd.date_range(start=start_date, periods=60, freq='MS')
        
        data = []
        for crime_type in self.config.crimes.CRIME_TYPES:
            for region in self.config.crimes.REGIONS:
                for date in dates:
                    # Simula tendência + sazonalidade + ruído
                    trend = 100 + np.random.normal(0, 10)
                    seasonality = 20 * np.sin(date.month * 2 * np.pi / 12)
                    noise = np.random.normal(0, 5)
                    
                    value = max(0, int(trend + seasonality + noise))
                    
                    data.append({
                        'data': date,
                        'tipo_crime': crime_type,
                        'regiao_administrativa': region,
                        'total_ocorrencias': value,
                        'populacao': np.random.randint(100000, 500000),
                        'taxa_100k': (value / 300000) * 100000
                    })
        
        return pd.DataFrame(data)
    
    def filter_by_crime_type(self, df: pd.DataFrame, crime_type: str) -> pd.DataFrame:
        """Filtra dados por tipo de crime"""
        return df[df['tipo_crime'] == crime_type].copy()
    
    def filter_by_region(self, df: pd.DataFrame, region: str) -> pd.DataFrame:
        """Filtra dados por região"""
        return df[df['regiao_administrativa'] == region].copy()
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                             start_date: str, end_date: str) -> pd.DataFrame:
        """Filtra dados por período"""
        df['data'] = pd.to_datetime(df['data'])
        mask = (df['data'] >= start_date) & (df['data'] <= end_date)
        return df[mask].copy()
    
    def aggregate_by_month(self, df: pd.DataFrame) -> pd.DataFrame:
        """Agrega dados por mês"""
        df['data'] = pd.to_datetime(df['data'])
        return df.groupby('data').agg({
            'total_ocorrencias': 'sum',
            'taxa_100k': 'mean'
        }).reset_index()
    
    def aggregate_by_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """Agrega dados por região"""
        return df.groupby('regiao_administrativa').agg({
            'total_ocorrencias': 'sum',
            'taxa_100k': 'mean'
        }).reset_index()


class GeoDataLoader(BaseDataLoader):
    """Carregador de dados geoespaciais"""
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.shapefiles_path = self.config.paths.DATA_SHAPEFILES
    
    def load(self, filename: str = "zonas_rio_limites_reais.geojson") -> Optional[gpd.GeoDataFrame]:
        """
        Carrega dados geoespaciais
        
        Args:
            filename: Nome do arquivo GeoJSON
            
        Returns:
            GeoDataFrame ou None se não encontrar
            
        Raises:
            FileNotFoundError: Se arquivo não encontrado em nenhum caminho
            ValueError: Se GeoDataFrame está vazio ou inválido
        """
        # Tenta múltiplos caminhos
        possible_paths = [
            self.shapefiles_path / filename,
            Path("data/shapefiles") / filename,
            Path(__file__).parent.parent.parent / "data" / "shapefiles" / filename
        ]
        
        for path in possible_paths:
            if path.exists():
                try:
                    logger.info(f"Tentando carregar GeoJSON: {path}")
                    gdf = gpd.read_file(path)
                    if not gdf.empty:
                        logger.info(f"GeoJSON carregado: {len(gdf)} geometrias")
                        return self._process_geodataframe(gdf)
                    else:
                        logger.warning(f"GeoDataFrame vazio: {path}")
                except FileNotFoundError:
                    logger.error(f"Arquivo não encontrado: {path}")
                    continue
                except ValueError as e:
                    logger.error(f"GeoJSON inválido: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Erro ao carregar GeoJSON: {e}")
                    continue
        
        logger.error(f"Arquivo {filename} não encontrado em nenhum caminho")
        return None
    
    def _process_geodataframe(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Processa GeoDataFrame após carregamento
        
        - Filtra apenas município do Rio de Janeiro
        - Padroniza colunas
        - Garante CRS correto
        """
        # Filtra apenas município do Rio (código IBGE: 3304557)
        if 'CD_MUN' in gdf.columns:
            gdf = gdf[gdf['CD_MUN'] == '3304557'].copy()
            logger.info(f"Filtrado para município do Rio: {len(gdf)} geometrias")
        elif 'municipio' in gdf.columns:
            gdf = gdf[gdf['municipio'].str.contains('Rio de Janeiro', case=False, na=False)].copy()
            logger.info(f"Filtrado para município do Rio: {len(gdf)} geometrias")
        
        # Padroniza nome da coluna de zona SOMENTE se não existir
        if 'zona' not in gdf.columns:
            if 'nome' in gdf.columns:
                gdf['zona'] = gdf['nome']
                logger.info("Coluna 'zona' criada a partir de 'nome'")
            elif 'name' in gdf.columns:
                gdf['zona'] = gdf['name']
                logger.info("Coluna 'zona' criada a partir de 'name'")
        else:
            logger.info("Coluna 'zona' já existe, mantendo original")
        
        # Garante CRS correto (WGS84)
        if gdf.crs is None:
            gdf.set_crs('EPSG:4326', inplace=True)
            logger.info("CRS definido como EPSG:4326")
        elif gdf.crs != 'EPSG:4326':
            gdf.to_crs('EPSG:4326', inplace=True)
            logger.info(f"CRS convertido para EPSG:4326")
        
        return gdf
    
    def merge_with_crime_data(self, gdf: gpd.GeoDataFrame, 
                              crime_df: pd.DataFrame,
                              geometry_key: str = 'zona',
                              crime_key: str = 'regiao_administrativa') -> gpd.GeoDataFrame:
        """
        Faz merge de dados geoespaciais com dados de criminalidade
        
        Args:
            gdf: GeoDataFrame com geometrias
            crime_df: DataFrame com dados de crime
            geometry_key: Coluna do GeoDataFrame para junção (padrão: 'zona')
            crime_key: Coluna do crime_df para junção (padrão: 'regiao_administrativa')
            
        Returns:
            GeoDataFrame com dados de crime mesclados
        """
        # Verifica se a coluna existe no GeoDataFrame
        if geometry_key not in gdf.columns:
            logger.warning(f"Coluna '{geometry_key}' não encontrada no GeoDataFrame. Colunas disponíveis: {gdf.columns.tolist()}")
            # Tenta usar primeira coluna com nome
            for col in ['nome', 'name', 'NOME']:
                if col in gdf.columns:
                    geometry_key = col
                    logger.info(f"Usando coluna '{geometry_key}' para merge")
                    break
        
        # Agrega dados de crime por região
        crime_agg = crime_df.groupby(crime_key).agg({
            'total_ocorrencias': 'sum',
            'taxa_100k': 'mean'
        }).reset_index()
        
        logger.info(f"Regiões nos dados de crime: {crime_agg[crime_key].unique().tolist()}")
        logger.info(f"Regiões no GeoDataFrame: {gdf[geometry_key].unique().tolist()}")
        
        # Merge
        gdf_merged = gdf.merge(
            crime_agg,
            left_on=geometry_key,
            right_on=crime_key,
            how='left'
        )
        
        # Log de áreas sem dados
        missing_data = gdf_merged['taxa_100k'].isna().sum()
        if missing_data > 0:
            logger.warning(f"{missing_data} geometrias sem dados de criminalidade após merge")
            missing_areas = gdf_merged[gdf_merged['taxa_100k'].isna()][geometry_key].tolist()
            logger.warning(f"Áreas sem dados: {missing_areas}")
        
        return gdf_merged


class DataManager:
    """Gerenciador central de dados"""
    
    def __init__(self):
        self.crime_loader = CrimeDataLoader()
        self.geo_loader = GeoDataLoader()
        self.config = config
    
    def get_crime_data(self, filename: Optional[str] = None,
                       crime_type: Optional[str] = None,
                       region: Optional[str] = None) -> pd.DataFrame:
        """
        Obtém dados de criminalidade com filtros opcionais
        
        Args:
            filename: Nome do arquivo
            crime_type: Filtro por tipo de crime
            region: Filtro por região
            
        Returns:
            DataFrame filtrado
        """
        df = self.crime_loader.load(filename)
        
        if crime_type:
            df = self.crime_loader.filter_by_crime_type(df, crime_type)
        
        if region:
            df = self.crime_loader.filter_by_region(df, region)
        
        return df
    
    def get_geo_data(self, filename: str = "zonas_rio_limites_reais.geojson",
                     include_crime_data: bool = False) -> Optional[gpd.GeoDataFrame]:
        """
        Obtém dados geoespaciais
        
        Args:
            filename: Nome do arquivo GeoJSON
            include_crime_data: Se True, faz merge com dados de criminalidade
            
        Returns:
            GeoDataFrame
        """
        gdf = self.geo_loader.load(filename)
        
        if gdf is not None and include_crime_data:
            crime_df = self.crime_loader.load()
            gdf = self.geo_loader.merge_with_crime_data(gdf, crime_df)
        
        return gdf
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """Calcula estatísticas resumidas"""
        return {
            'total_occurrences': int(df['total_ocorrencias'].sum()),
            'mean_rate': float(df['taxa_100k'].mean()),
            'max_rate': float(df['taxa_100k'].max()),
            'min_rate': float(df['taxa_100k'].min()),
            'n_regions': df['regiao_administrativa'].nunique() if 'regiao_administrativa' in df.columns else 0,
            'n_crime_types': df['tipo_crime'].nunique() if 'tipo_crime' in df.columns else 0
        }

