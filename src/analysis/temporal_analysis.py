"""
Módulo para análise temporal de dados de criminalidade
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemporalAnalyzer:
    """
    Classe para análise temporal de dados de criminalidade
    """
    
    def __init__(self):
        self.seasonal_periods = {
            'daily': 7,      # Semana
            'monthly': 12,  # Ano
            'quarterly': 4  # Ano
        }
        
    def analyze_trends(self, df: pd.DataFrame, 
                      date_col: str, 
                      value_col: str,
                      group_col: Optional[str] = None) -> Dict:
        """
        Analisa tendências temporais
        
        Args:
            df: DataFrame com dados temporais
            date_col: Nome da coluna de data
            value_col: Nome da coluna de valores
            group_col: Coluna para agrupamento (opcional)
            
        Returns:
            Dicionário com resultados da análise
        """
        logger.info("Iniciando análise de tendências")
        
        results = {}
        
        if group_col:
            # Análise por grupo
            for group in df[group_col].unique():
                group_data = df[df[group_col] == group]
                results[group] = self._analyze_single_series(
                    group_data, date_col, value_col
                )
        else:
            # Análise geral
            results['overall'] = self._analyze_single_series(df, date_col, value_col)
        
        return results
    
    def _analyze_single_series(self, df: pd.DataFrame, 
                              date_col: str, 
                              value_col: str) -> Dict:
        """
        Analisa uma única série temporal
        
        Args:
            df: DataFrame com dados
            date_col: Nome da coluna de data
            value_col: Nome da coluna de valores
            
        Returns:
            Dicionário com resultados da análise
        """
        # Ordena por data
        df_sorted = df.sort_values(date_col)
        
        # Converte para datetime se necessário
        if not pd.api.types.is_datetime64_any_dtype(df_sorted[date_col]):
            df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
        
        # Cria série temporal
        ts = df_sorted.set_index(date_col)[value_col]
        
        # Remove valores faltantes
        ts = ts.dropna()
        
        if len(ts) < 2:
            return {'error': 'Série temporal muito curta'}
        
        # Análise de tendência
        trend_analysis = self._calculate_trend(ts)
        
        # Análise de sazonalidade
        seasonal_analysis = self._analyze_seasonality(ts)
        
        # Teste de estacionariedade
        stationarity_test = self._test_stationarity(ts)
        
        # Análise de autocorrelação
        autocorr_analysis = self._analyze_autocorrelation(ts)
        
        return {
            'trend': trend_analysis,
            'seasonality': seasonal_analysis,
            'stationarity': stationarity_test,
            'autocorrelation': autocorr_analysis,
            'series_length': len(ts),
            'date_range': (ts.index.min(), ts.index.max())
        }
    
    def _calculate_trend(self, ts: pd.Series) -> Dict:
        """
        Calcula tendência da série temporal
        
        Args:
            ts: Série temporal
            
        Returns:
            Dicionário com análise de tendência
        """
        # Regressão linear simples
        x = np.arange(len(ts))
        y = ts.values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Classifica tendência
        if p_value < 0.05:
            if slope > 0:
                trend_direction = 'crescente'
            else:
                trend_direction = 'decrescente'
        else:
            trend_direction = 'estável'
        
        return {
            'slope': slope,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'direction': trend_direction,
            'significance': p_value < 0.05
        }
    
    def _analyze_seasonality(self, ts: pd.Series) -> Dict:
        """
        Analisa sazonalidade da série temporal
        
        Args:
            ts: Série temporal
            
        Returns:
            Dicionário com análise de sazonalidade
        """
        try:
            # Decomposição sazonal
            decomposition = seasonal_decompose(ts, model='additive', period=12)
            
            # Calcula força da sazonalidade
            seasonal_strength = np.var(decomposition.seasonal) / np.var(ts)
            
            # Identifica padrões sazonais
            seasonal_pattern = self._identify_seasonal_patterns(decomposition.seasonal)
            
            return {
                'seasonal_strength': seasonal_strength,
                'seasonal_pattern': seasonal_pattern,
                'trend_component': decomposition.trend,
                'seasonal_component': decomposition.seasonal,
                'residual_component': decomposition.resid
            }
            
        except Exception as e:
            logger.warning(f"Erro na análise de sazonalidade: {e}")
            return {'error': str(e)}
    
    def _identify_seasonal_patterns(self, seasonal_component: pd.Series) -> Dict:
        """
        Identifica padrões sazonais
        
        Args:
            seasonal_component: Componente sazonal
            
        Returns:
            Dicionário com padrões identificados
        """
        # Média por mês
        monthly_avg = seasonal_component.groupby(seasonal_component.index.month).mean()
        
        # Identifica picos e vales
        peak_month = monthly_avg.idxmax()
        valley_month = monthly_avg.idxmin()
        
        # Amplitude sazonal
        seasonal_amplitude = monthly_avg.max() - monthly_avg.min()
        
        return {
            'peak_month': peak_month,
            'valley_month': valley_month,
            'amplitude': seasonal_amplitude,
            'monthly_pattern': monthly_avg.to_dict()
        }
    
    def _test_stationarity(self, ts: pd.Series) -> Dict:
        """
        Testa estacionariedade da série temporal
        
        Args:
            ts: Série temporal
            
        Returns:
            Dicionário com resultados do teste
        """
        try:
            # Teste ADF (Augmented Dickey-Fuller)
            adf_result = adfuller(ts.dropna())
            
            return {
                'adf_statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'is_stationary': adf_result[1] < 0.05
            }
            
        except Exception as e:
            logger.warning(f"Erro no teste de estacionariedade: {e}")
            return {'error': str(e)}
    
    def _analyze_autocorrelation(self, ts: pd.Series) -> Dict:
        """
        Analisa autocorrelação da série temporal
        
        Args:
            ts: Série temporal
            
        Returns:
            Dicionário com análise de autocorrelação
        """
        try:
            # Autocorrelação
            autocorr = ts.autocorr(lag=1)
            
            # Autocorrelação parcial
            from statsmodels.tsa.stattools import pacf
            pacf_values = pacf(ts.dropna(), nlags=10)
            
            return {
                'autocorrelation_lag1': autocorr,
                'partial_autocorrelation': pacf_values.tolist(),
                'significant_lags': self._find_significant_lags(ts)
            }
            
        except Exception as e:
            logger.warning(f"Erro na análise de autocorrelação: {e}")
            return {'error': str(e)}
    
    def _find_significant_lags(self, ts: pd.Series, max_lags: int = 10) -> List[int]:
        """
        Encontra lags significativos
        
        Args:
            ts: Série temporal
            max_lags: Número máximo de lags para testar
            
        Returns:
            Lista de lags significativos
        """
        significant_lags = []
        
        for lag in range(1, min(max_lags + 1, len(ts) // 4)):
            try:
                autocorr = ts.autocorr(lag=lag)
                # Teste de significância (aproximado)
                if abs(autocorr) > 2 / np.sqrt(len(ts)):
                    significant_lags.append(lag)
            except:
                continue
        
        return significant_lags
    
    def detect_anomalies(self, df: pd.DataFrame, 
                        date_col: str, 
                        value_col: str,
                        method: str = 'iqr') -> pd.DataFrame:
        """
        Detecta anomalias temporais
        
        Args:
            df: DataFrame com dados
            date_col: Nome da coluna de data
            value_col: Nome da coluna de valores
            method: Método de detecção ('iqr', 'zscore', 'isolation')
            
        Returns:
            DataFrame com anomalias identificadas
        """
        logger.info(f"Detectando anomalias usando método: {method}")
        
        if method == 'iqr':
            return self._detect_anomalies_iqr(df, value_col)
        elif method == 'zscore':
            return self._detect_anomalies_zscore(df, value_col)
        elif method == 'isolation':
            return self._detect_anomalies_isolation(df, value_col)
        else:
            raise ValueError(f"Método não suportado: {method}")
    
    def _detect_anomalies_iqr(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """
        Detecta anomalias usando IQR
        
        Args:
            df: DataFrame com dados
            value_col: Nome da coluna de valores
            
        Returns:
            DataFrame com anomalias
        """
        Q1 = df[value_col].quantile(0.25)
        Q3 = df[value_col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = df[(df[value_col] < lower_bound) | (df[value_col] > upper_bound)]
        
        return anomalies
    
    def _detect_anomalies_zscore(self, df: pd.DataFrame, value_col: str, 
                                threshold: float = 3) -> pd.DataFrame:
        """
        Detecta anomalias usando Z-score
        
        Args:
            df: DataFrame com dados
            value_col: Nome da coluna de valores
            threshold: Limiar para detecção
            
        Returns:
            DataFrame com anomalias
        """
        z_scores = np.abs(stats.zscore(df[value_col].dropna()))
        anomalies = df[z_scores > threshold]
        
        return anomalies
    
    def _detect_anomalies_isolation(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """
        Detecta anomalias usando Isolation Forest
        
        Args:
            df: DataFrame com dados
            value_col: Nome da coluna de valores
            
        Returns:
            DataFrame com anomalias
        """
        try:
            from sklearn.ensemble import IsolationForest
            
            # Prepara dados
            X = df[[value_col]].dropna()
            
            # Aplica Isolation Forest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(X)
            
            # Identifica anomalias
            anomalies = df[anomaly_labels == -1]
            
            return anomalies
            
        except ImportError:
            logger.warning("scikit-learn não disponível, usando método IQR")
            return self._detect_anomalies_iqr(df, value_col)
    
    def create_time_series_features(self, df: pd.DataFrame, 
                                   date_col: str, 
                                   value_col: str,
                                   group_col: Optional[str] = None) -> pd.DataFrame:
        """
        Cria features para análise de séries temporais
        
        Args:
            df: DataFrame com dados
            date_col: Nome da coluna de data
            value_col: Nome da coluna de valores
            group_col: Coluna para agrupamento
            
        Returns:
            DataFrame com features temporais
        """
        logger.info("Criando features temporais")
        
        df_features = df.copy()
        
        # Converte para datetime
        df_features[date_col] = pd.to_datetime(df_features[date_col])
        
        # Ordena por data
        df_features = df_features.sort_values([group_col, date_col] if group_col else [date_col])
        
        # Features temporais básicas
        df_features['ano'] = df_features[date_col].dt.year
        df_features['mes'] = df_features[date_col].dt.month
        df_features['dia'] = df_features[date_col].dt.day
        df_features['dia_semana'] = df_features[date_col].dt.dayofweek
        df_features['trimestre'] = df_features[date_col].dt.quarter
        df_features['semestre'] = df_features[date_col].dt.month.apply(lambda x: 1 if x <= 6 else 2)
        
        # Features de lag
        if group_col:
            for lag in [1, 3, 6, 12]:
                df_features[f'{value_col}_lag_{lag}'] = df_features.groupby(group_col)[value_col].shift(lag)
        else:
            for lag in [1, 3, 6, 12]:
                df_features[f'{value_col}_lag_{lag}'] = df_features[value_col].shift(lag)
        
        # Features de média móvel
        if group_col:
            for window in [3, 6, 12]:
                df_features[f'{value_col}_ma_{window}'] = df_features.groupby(group_col)[value_col].rolling(window=window).mean().reset_index(0, drop=True)
        else:
            for window in [3, 6, 12]:
                df_features[f'{value_col}_ma_{window}'] = df_features[value_col].rolling(window=window).mean()
        
        # Features de diferença
        if group_col:
            df_features[f'{value_col}_diff'] = df_features.groupby(group_col)[value_col].diff()
            df_features[f'{value_col}_diff2'] = df_features.groupby(group_col)[value_col].diff(2)
        else:
            df_features[f'{value_col}_diff'] = df_features[value_col].diff()
            df_features[f'{value_col}_diff2'] = df_features[value_col].diff(2)
        
        logger.info(f"Features temporais criadas: {len(df_features.columns)} colunas")
        return df_features
    
    def generate_insights(self, analysis_results: Dict) -> Dict:
        """
        Gera insights a partir dos resultados da análise
        
        Args:
            analysis_results: Resultados da análise temporal
            
        Returns:
            Dicionário com insights
        """
        insights = {
            'temporal_patterns': {},
            'anomalies_detected': {},
            'recommendations': []
        }
        
        for group, results in analysis_results.items():
            if 'error' in results:
                continue
            
            # Insights de tendência
            if results['trend']['significance']:
                if results['trend']['direction'] == 'crescente':
                    insights['temporal_patterns'][group] = 'Tendência crescente significativa'
                elif results['trend']['direction'] == 'decrescente':
                    insights['temporal_patterns'][group] = 'Tendência decrescente significativa'
            
            # Insights de sazonalidade
            if 'seasonal_strength' in results['seasonality']:
                if results['seasonality']['seasonal_strength'] > 0.5:
                    insights['temporal_patterns'][group] = 'Fortes padrões sazonais identificados'
            
            # Insights de estacionariedade
            if results['stationarity']['is_stationary']:
                insights['temporal_patterns'][group] = 'Série estacionária'
            else:
                insights['recommendations'].append(f'Considerar diferenciação para {group}')
        
        return insights

def main():
    """
    Função principal para teste do módulo
    """
    # Exemplo de uso
    analyzer = TemporalAnalyzer()
    
    # Cria dados de exemplo
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
    values = np.random.poisson(100, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 12) * 20
    
    df = pd.DataFrame({
        'data': dates,
        'valor': values,
        'regiao': ['Centro'] * len(dates)
    })
    
    # Análise de tendências
    results = analyzer.analyze_trends(df, 'data', 'valor', 'regiao')
    
    # Cria features temporais
    df_features = analyzer.create_time_series_features(df, 'data', 'valor', 'regiao')
    
    # Detecta anomalias
    anomalies = analyzer.detect_anomalies(df, 'data', 'valor')
    
    # Gera insights
    insights = analyzer.generate_insights(results)
    
    print("Análise temporal concluída:")
    print(f"Features criadas: {len(df_features.columns)} colunas")
    print(f"Anomalias detectadas: {len(anomalies)} registros")
    print(f"Insights: {insights}")

if __name__ == "__main__":
    main()

