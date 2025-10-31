"""
🔧 CONFIGURAÇÃO CENTRALIZADA
============================

Arquivo central de configurações do projeto seguindo boas práticas POO.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import os


@dataclass
class PathConfig:
    """Configuração de caminhos do projeto"""
    ROOT_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = ROOT_DIR / "data"
    DATA_RAW: Path = DATA_DIR / "raw"
    DATA_PROCESSED: Path = DATA_DIR / "processed"
    DATA_SHAPEFILES: Path = DATA_DIR / "shapefiles"
    OUTPUTS_DIR: Path = ROOT_DIR / "outputs"
    OUTPUTS_FIGURES: Path = OUTPUTS_DIR / "figures"
    OUTPUTS_MAPS: Path = OUTPUTS_DIR / "maps"
    OUTPUTS_REPORTS: Path = OUTPUTS_DIR / "reports"
    
    def __post_init__(self):
        """Cria diretórios se não existirem"""
        for path in [self.DATA_RAW, self.DATA_PROCESSED, self.DATA_SHAPEFILES,
                     self.OUTPUTS_FIGURES, self.OUTPUTS_MAPS, self.OUTPUTS_REPORTS]:
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class MapConfig:
    """Configuração de mapas"""
    # Coordenadas do município do Rio de Janeiro
    RIO_CENTER_LAT: float = -22.9068
    RIO_CENTER_LON: float = -43.1729
    
    # Limites geográficos do município (bbox)
    RIO_BBOX: Dict[str, float] = None
    
    # Configurações de visualização
    DEFAULT_ZOOM: int = 11
    TILE_STYLE: str = 'CartoDB positron'
    FILL_OPACITY: float = 0.7
    LINE_WEIGHT: int = 2
    LINE_COLOR: str = '#666666'
    
    # Cores para níveis de criminalidade
    COLOR_VERY_LOW: str = '#2ECC71'  # Verde
    COLOR_LOW: str = '#F1C40F'       # Amarelo
    COLOR_MEDIUM: str = '#E67E22'    # Laranja
    COLOR_HIGH: str = '#E74C3C'      # Vermelho
    COLOR_VERY_HIGH: str = '#8B0000' # Vermelho escuro
    
    def __post_init__(self):
        if self.RIO_BBOX is None:
            self.RIO_BBOX = {
                'min_lat': -23.082741,
                'max_lat': -22.746006,
                'min_lon': -43.797142,
                'max_lon': -43.096837
            }
    
    def get_color_by_rate(self, rate: float) -> str:
        """Retorna cor baseada na taxa de criminalidade"""
        if rate < 20:
            return self.COLOR_VERY_LOW
        elif rate < 40:
            return self.COLOR_LOW
        elif rate < 60:
            return self.COLOR_MEDIUM
        elif rate < 80:
            return self.COLOR_HIGH
        else:
            return self.COLOR_VERY_HIGH


@dataclass
class CrimeConfig:
    """Configuração de tipos de crime"""
    CRIME_TYPES: List[str] = None
    REGIONS: List[str] = None
    
    def __post_init__(self):
        if self.CRIME_TYPES is None:
            self.CRIME_TYPES = [
                'Homicídio Doloso',
                'Roubo de Veículo',
                'Roubo a Transeunte',
                'Furto de Veículo',
                'Furto a Transeunte',
                'Lesão Corporal',
                'Violência Doméstica',
                'Estupro'
            ]
        
        if self.REGIONS is None:
            # Apenas município do Rio de Janeiro
            self.REGIONS = [
                'Centro',
                'Zona Sul',
                'Zona Norte',
                'Zona Oeste',
                'Barra da Tijuca'
            ]


@dataclass
class ModelConfig:
    """Configuração de modelos preditivos"""
    # ARIMA
    ARIMA_ORDER: tuple = (1, 1, 1)
    
    # SARIMA
    SARIMA_ORDER: tuple = (1, 1, 1)
    SARIMA_SEASONAL_ORDER: tuple = (1, 1, 1, 12)
    
    # Prophet
    PROPHET_YEARLY_SEASONALITY: bool = True
    PROPHET_WEEKLY_SEASONALITY: bool = False
    PROPHET_INTERVAL_WIDTH: float = 0.95
    
    # XGBoost
    XGBOOST_N_ESTIMATORS: int = 100
    XGBOOST_MAX_DEPTH: int = 5
    XGBOOST_LEARNING_RATE: float = 0.1
    
    # Random Forest
    RF_N_ESTIMATORS: int = 100
    RF_MAX_DEPTH: int = 10
    
    # LSTM
    LSTM_UNITS: int = 50
    LSTM_EPOCHS: int = 50
    LSTM_BATCH_SIZE: int = 32
    LSTM_DROPOUT: float = 0.2
    
    # Geral
    DEFAULT_FORECAST_HORIZON: int = 6  # meses
    DEFAULT_N_LAGS: int = 12
    TRAIN_TEST_SPLIT: float = 0.8


@dataclass
class APIConfig:
    """Configuração de APIs externas"""
    # ISP-RJ (Instituto de Segurança Pública)
    ISP_BASE_URL: str = "http://www.ispdados.rj.gov.br/api"
    
    # Data.Rio
    DATARIO_BASE_URL: str = "https://www.data.rio"
    
    # IBGE
    IBGE_BASE_URL: str = "https://servicodados.ibge.gov.br/api/v1"
    
    # Timeout padrão
    REQUEST_TIMEOUT: int = 30
    
    # Retry
    MAX_RETRIES: int = 3


class AppConfig:
    """Configuração principal da aplicação"""
    
    def __init__(self):
        self.paths = PathConfig()
        self.maps = MapConfig()
        self.crimes = CrimeConfig()
        self.models = ModelConfig()
        self.apis = APIConfig()
        
        # Streamlit
        self.STREAMLIT_PAGE_TITLE = "🔒 Segurança Pública RJ"
        self.STREAMLIT_PAGE_ICON = "🔒"
        self.STREAMLIT_LAYOUT = "wide"
        
        # Cache
        self.CACHE_TTL = 3600  # 1 hora
        
        # Debug
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    def __repr__(self):
        return f"AppConfig(debug={self.DEBUG})"


# Instância global
config = AppConfig()


# Funções auxiliares
def get_data_path(filename: str) -> Path:
    """Retorna caminho completo para arquivo de dados"""
    return config.paths.DATA_PROCESSED / filename


def get_shapefile_path(filename: str) -> Path:
    """Retorna caminho completo para shapefile"""
    return config.paths.DATA_SHAPEFILES / filename


def get_output_path(category: str, filename: str) -> Path:
    """Retorna caminho completo para arquivo de saída"""
    category_map = {
        'figure': config.paths.OUTPUTS_FIGURES,
        'map': config.paths.OUTPUTS_MAPS,
        'report': config.paths.OUTPUTS_REPORTS
    }
    return category_map.get(category, config.paths.OUTPUTS_DIR) / filename

