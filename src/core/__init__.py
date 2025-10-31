"""
🎯 CORE MODULE - Módulo Central POO
===================================

Módulo central com classes POO para o projeto.
"""

from src.core.data_loader import (
    DataManager,
    CrimeDataLoader,
    GeoDataLoader
)

from src.core.visualizer import (
    VisualizationFactory,
    TimeSeriesVisualizer,
    BarChartVisualizer,
    MapVisualizer,
    DashboardVisualizer
)

__all__ = [
    'DataManager',
    'CrimeDataLoader',
    'GeoDataLoader',
    'VisualizationFactory',
    'TimeSeriesVisualizer',
    'BarChartVisualizer',
    'MapVisualizer',
    'DashboardVisualizer'
]

