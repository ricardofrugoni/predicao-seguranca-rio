"""
📊 VISUALIZER - Visualizações com POO
=====================================

Classes responsáveis por criar visualizações interativas.
"""

import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from typing import Optional, Dict, List, Tuple
from abc import ABC, abstractmethod

from src.config import config


class BaseVisualizer(ABC):
    """Classe base abstrata para visualizadores"""
    
    def __init__(self):
        self.config = config
    
    @abstractmethod
    def create(self, data, **kwargs):
        """Método abstrato para criar visualização"""
        pass


class TimeSeriesVisualizer(BaseVisualizer):
    """Visualizador de séries temporais"""
    
    def create(self, df: pd.DataFrame, 
               x_col: str = 'data',
               y_col: str = 'total_ocorrencias',
               title: str = 'Série Temporal',
               **kwargs) -> go.Figure:
        """
        Cria gráfico de série temporal
        
        Args:
            df: DataFrame com dados
            x_col: Coluna do eixo X (datas)
            y_col: Coluna do eixo Y (valores)
            title: Título do gráfico
            
        Returns:
            Figure do Plotly
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=y_col,
            line=dict(color='#3498db', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Data',
            yaxis_title=y_col,
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def create_decomposition(self, decomposition: Dict) -> go.Figure:
        """
        Cria gráfico de decomposição de série temporal
        
        Args:
            decomposition: Dicionário com componentes (trend, seasonal, residual)
            
        Returns:
            Figure do Plotly
        """
        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=('Série Original', 'Tendência', 'Sazonalidade', 'Resíduos'),
            vertical_spacing=0.08
        )
        
        # Original
        fig.add_trace(
            go.Scatter(x=decomposition['observed'].index, 
                      y=decomposition['observed'],
                      name='Original', line=dict(color='#3498db')),
            row=1, col=1
        )
        
        # Tendência
        fig.add_trace(
            go.Scatter(x=decomposition['trend'].index,
                      y=decomposition['trend'],
                      name='Tendência', line=dict(color='#e74c3c')),
            row=2, col=1
        )
        
        # Sazonalidade
        fig.add_trace(
            go.Scatter(x=decomposition['seasonal'].index,
                      y=decomposition['seasonal'],
                      name='Sazonalidade', line=dict(color='#2ecc71')),
            row=3, col=1
        )
        
        # Resíduos
        fig.add_trace(
            go.Scatter(x=decomposition['residual'].index,
                      y=decomposition['residual'],
                      name='Resíduos', line=dict(color='#95a5a6')),
            row=4, col=1
        )
        
        fig.update_layout(height=800, showlegend=False, template='plotly_white')
        
        return fig
    
    def create_comparison(self, df: pd.DataFrame,
                         x_col: str,
                         y_col: str,
                         color_col: str,
                         title: str = 'Comparação') -> go.Figure:
        """Cria gráfico comparativo entre categorias"""
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            template='plotly_white'
        )
        
        fig.update_layout(height=500, hovermode='x unified')
        
        return fig


class BarChartVisualizer(BaseVisualizer):
    """Visualizador de gráficos de barras"""
    
    def create(self, df: pd.DataFrame,
               x_col: str,
               y_col: str,
               title: str = 'Gráfico de Barras',
               orientation: str = 'v',
               color_scale: str = 'Reds',
               **kwargs) -> go.Figure:
        """
        Cria gráfico de barras
        
        Args:
            df: DataFrame
            x_col: Coluna do eixo X
            y_col: Coluna do eixo Y
            title: Título
            orientation: 'v' (vertical) ou 'h' (horizontal)
            color_scale: Escala de cores
            
        Returns:
            Figure do Plotly
        """
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            color=y_col,
            color_continuous_scale=color_scale,
            orientation=orientation,
            template='plotly_white'
        )
        
        fig.update_layout(height=500, showlegend=False)
        
        return fig
    
    def create_grouped(self, df: pd.DataFrame,
                      x_col: str,
                      y_col: str,
                      color_col: str,
                      title: str = 'Gráfico Agrupado') -> go.Figure:
        """Cria gráfico de barras agrupadas"""
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            barmode='group',
            template='plotly_white'
        )
        
        fig.update_layout(height=500)
        
        return fig


class MapVisualizer(BaseVisualizer):
    """Visualizador de mapas"""
    
    def create(self, gdf: gpd.GeoDataFrame,
               value_column: str = 'taxa_100k',
               name_column: str = 'zona',
               title: str = 'Mapa de Calor',
               **kwargs) -> folium.Map:
        """
        Cria mapa coroplético com Folium
        
        Args:
            gdf: GeoDataFrame com geometrias
            value_column: Coluna com valores para colorir
            name_column: Coluna com nomes das áreas
            title: Título do mapa
            
        Returns:
            Mapa Folium
        """
        if gdf is None or gdf.empty:
            return self._create_empty_map()
        
        # Calcula centro e bounds
        bounds = gdf.total_bounds
        center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
        
        # Cria mapa
        m = folium.Map(
            location=center,
            zoom_start=self.config.maps.DEFAULT_ZOOM,
            tiles=self.config.maps.TILE_STYLE,
            dragging=False,
            scrollWheelZoom=False,
            zoomControl=False,
            doubleClickZoom=False,
            attributionControl=True
        )
        
        # Ajusta bounds
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
        
        # Adiciona camada GeoJSON
        folium.GeoJson(
            gdf,
            style_function=lambda feature: {
                'fillColor': self._get_color(
                    feature['properties'].get(value_column, 50)
                ),
                'fillOpacity': self.config.maps.FILL_OPACITY,
                'color': self.config.maps.LINE_COLOR,
                'weight': self.config.maps.LINE_WEIGHT,
                'dashArray': '0'
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[name_column, value_column],
                aliases=['Região:', 'Taxa/100k hab:'],
                sticky=True
            )
        ).add_to(m)
        
        return m
    
    def _get_color(self, value: float) -> str:
        """Retorna cor baseada no valor"""
        return self.config.maps.get_color_by_rate(value)
    
    def _create_empty_map(self) -> folium.Map:
        """Cria mapa vazio centralizado no Rio"""
        return folium.Map(
            location=[self.config.maps.RIO_CENTER_LAT, 
                     self.config.maps.RIO_CENTER_LON],
            zoom_start=self.config.maps.DEFAULT_ZOOM,
            tiles=self.config.maps.TILE_STYLE
        )


class DashboardVisualizer(BaseVisualizer):
    """Visualizador para dashboards completos"""
    
    def __init__(self):
        super().__init__()
        self.time_series = TimeSeriesVisualizer()
        self.bar_chart = BarChartVisualizer()
        self.map = MapVisualizer()
    
    def create(self, data, visualization_type: str, **kwargs):
        """
        Cria visualização baseada no tipo
        
        Args:
            data: Dados para visualização
            visualization_type: Tipo ('time_series', 'bar', 'map')
            **kwargs: Argumentos adicionais
            
        Returns:
            Visualização correspondente
        """
        visualizers = {
            'time_series': self.time_series.create,
            'bar': self.bar_chart.create,
            'map': self.map.create
        }
        
        visualizer = visualizers.get(visualization_type)
        if visualizer:
            return visualizer(data, **kwargs)
        else:
            raise ValueError(f"Tipo de visualização '{visualization_type}' não suportado")
    
    def create_kpi_cards(self, stats: Dict) -> List[Dict]:
        """
        Cria dados para cards de KPI
        
        Args:
            stats: Dicionário com estatísticas
            
        Returns:
            Lista de dicionários com dados dos cards
        """
        return [
            {
                'title': 'Total de Ocorrências',
                'value': f"{stats.get('total_occurrences', 0):,}",
                'icon': '🚨'
            },
            {
                'title': 'Taxa Média',
                'value': f"{stats.get('mean_rate', 0):.1f}",
                'icon': '📊'
            },
            {
                'title': 'Regiões Analisadas',
                'value': str(stats.get('n_regions', 0)),
                'icon': '📍'
            },
            {
                'title': 'Tipos de Crimes',
                'value': str(stats.get('n_crime_types', 0)),
                'icon': '🔍'
            }
        ]


class VisualizationFactory:
    """Factory para criar visualizações"""
    
    @staticmethod
    def create_visualizer(viz_type: str) -> BaseVisualizer:
        """
        Cria visualizador baseado no tipo
        
        Args:
            viz_type: Tipo de visualizador
            
        Returns:
            Instância do visualizador
        """
        visualizers = {
            'time_series': TimeSeriesVisualizer,
            'bar': BarChartVisualizer,
            'map': MapVisualizer,
            'dashboard': DashboardVisualizer
        }
        
        visualizer_class = visualizers.get(viz_type)
        if visualizer_class:
            return visualizer_class()
        else:
            raise ValueError(f"Tipo '{viz_type}' não suportado")

