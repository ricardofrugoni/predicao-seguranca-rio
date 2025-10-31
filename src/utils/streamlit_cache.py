"""
💾 STREAMLIT CACHE - Wrappers com Cache
========================================

Wrappers para funções com cache do Streamlit, separando
a lógica de negócio do framework.
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
from typing import Optional

from src.core.data_loader import CrimeDataLoader, GeoDataLoader, DataManager


@st.cache_data(ttl=3600, show_spinner=False)
def get_crime_data(filename: Optional[str] = None,
                   crime_type: Optional[str] = None,
                   region: Optional[str] = None) -> pd.DataFrame:
    """
    Wrapper com cache para carregar dados de criminalidade
    
    Args:
        filename: Nome do arquivo
        crime_type: Filtro por tipo de crime
        region: Filtro por região
        
    Returns:
        DataFrame com dados
    """
    loader = CrimeDataLoader()
    df = loader.load(filename)
    
    if crime_type:
        df = loader.filter_by_crime_type(df, crime_type)
    
    if region:
        df = loader.filter_by_region(df, region)
    
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def get_geo_data(filename: str = "zonas_rio_limites_reais.geojson",
                 include_crime_data: bool = False) -> Optional[gpd.GeoDataFrame]:
    """
    Wrapper com cache para carregar dados geoespaciais
    
    Args:
        filename: Nome do arquivo GeoJSON
        include_crime_data: Se True, faz merge com dados de criminalidade
        
    Returns:
        GeoDataFrame
    """
    geo_loader = GeoDataLoader()
    gdf = geo_loader.load(filename)
    
    if gdf is not None and include_crime_data:
        crime_loader = CrimeDataLoader()
        crime_df = crime_loader.load()
        gdf = geo_loader.merge_with_crime_data(gdf, crime_df)
    
    return gdf


@st.cache_resource
def get_data_manager() -> DataManager:
    """
    Wrapper com cache para instanciar DataManager
    
    Returns:
        Instância única de DataManager
    """
    return DataManager()

