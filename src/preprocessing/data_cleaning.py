"""
Módulo para limpeza e padronização de dados de criminalidade
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Dict, List, Optional, Tuple

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    """
    Classe para limpeza e padronização de dados de criminalidade
    """
    
    def __init__(self):
        self.crime_types_mapping = self._get_crime_types_mapping()
        self.region_mapping = self._get_region_mapping()
        
    def _get_crime_types_mapping(self) -> Dict[str, str]:
        """
        Retorna mapeamento dos tipos de crime conforme especificação
        
        Returns:
            Dicionário com mapeamento de tipos de crime
        """
        return {
            # Crimes Violentos Letais Intencionais (CVLI)
            'HOMICIDIO_DOLOSO': 'Homicídio Doloso',
            'LATROCINIO': 'Latrocínio',
            'LESAO_CORPORAL_SEGUIDA_MORTE': 'Lesão Corporal Seguida de Morte',
            
            # Crimes Violentos contra o Patrimônio
            'ROUBO_VEICULO': 'Roubo de Veículo',
            'ROUBO_CARGA': 'Roubo de Carga',
            'ROUBO_TRANSEUNTE': 'Roubo a Transeunte',
            'ROUBO_ESTABELECIMENTO': 'Roubo em Estabelecimento Comercial',
            'ROUBO_CELULAR': 'Roubo de Aparelho Celular',
            
            # Crimes contra o Patrimônio sem Violência
            'FURTO_VEICULO': 'Furto de Veículo',
            'FURTO_TRANSEUNTE': 'Furto a Transeunte',
            'FURTO_ESTABELECIMENTO': 'Furto em Estabelecimento',
            
            # Crimes contra Grupos Vulneráveis
            'ESTUPRO': 'Estupro',
            'VIOLENCIA_DOMESTICA': 'Violência Doméstica',
            
            # Apreensões
            'APREENSAO_ARMA': 'Apreensão de Arma de Fogo',
            'APREENSAO_DROGA': 'Apreensão de Drogas'
        }
    
    def _get_region_mapping(self) -> Dict[str, str]:
        """
        Retorna mapeamento das regiões administrativas
        
        Returns:
            Dicionário com mapeamento de regiões
        """
        return {
            'CENTRO': 'Centro',
            'ZONA_SUL': 'Zona Sul',
            'ZONA_NORTE': 'Zona Norte',
            'ZONA_OESTE': 'Zona Oeste',
            'BARRA_DA_TIJUCA': 'Barra da Tijuca',
            'JACAREPAGUA': 'Jacarepaguá',
            'CAMPO_GRANDE': 'Campo Grande',
            'SANTA_CRUZ': 'Santa Cruz',
            'ILHA_DO_GOVERNADOR': 'Ilha do Governador',
            'ILHA_DE_PAQUETA': 'Ilha de Paquetá',
            'TIJUCA': 'Tijuca',
            'VILA_ISABEL': 'Vila Isabel',
            'MEIER': 'Méier',
            'MADUREIRA': 'Madureira',
            'BANGU': 'Bangu',
            'REALENGO': 'Realengo',
            'GUARATIBA': 'Guaratiba'
        }
    
    def clean_crime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa e padroniza dados de criminalidade
        
        Args:
            df: DataFrame com dados brutos de criminalidade
            
        Returns:
            DataFrame limpo e padronizado
        """
        logger.info("Iniciando limpeza de dados de criminalidade")
        
        # Cria cópia para não modificar original
        df_clean = df.copy()
        
        # 1. Padroniza tipos de crime
        df_clean = self._standardize_crime_types(df_clean)
        
        # 2. Padroniza regiões administrativas
        df_clean = self._standardize_regions(df_clean)
        
        # 3. Limpa e converte tipos de dados
        df_clean = self._clean_data_types(df_clean)
        
        # 4. Remove registros inválidos
        df_clean = self._remove_invalid_records(df_clean)
        
        # 5. Adiciona colunas derivadas
        df_clean = self._add_derived_columns(df_clean)
        
        logger.info(f"Dados limpos: {len(df_clean)} registros")
        return df_clean
    
    def _standardize_crime_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza tipos de crime
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com tipos de crime padronizados
        """
        if 'tipo_crime' in df.columns:
            # Mapeia tipos de crime para padronização
            df['tipo_crime'] = df['tipo_crime'].str.upper().str.strip()
            
            # Aplica mapeamento
            df['tipo_crime'] = df['tipo_crime'].map(self.crime_types_mapping).fillna(df['tipo_crime'])
            
            logger.info(f"Tipos de crime únicos: {df['tipo_crime'].nunique()}")
        
        return df
    
    def _standardize_regions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza regiões administrativas
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com regiões padronizadas
        """
        if 'regiao_administrativa' in df.columns:
            # Padroniza nomes das regiões
            df['regiao_administrativa'] = df['regiao_administrativa'].str.upper().str.strip()
            
            # Aplica mapeamento
            df['regiao_administrativa'] = df['regiao_administrativa'].map(self.region_mapping).fillna(df['regiao_administrativa'])
            
            logger.info(f"Regiões únicas: {df['regiao_administrativa'].nunique()}")
        
        return df
    
    def _clean_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa e converte tipos de dados
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com tipos de dados corretos
        """
        # Converte colunas numéricas
        numeric_columns = ['total_ocorrencias', 'populacao', 'taxa_100k']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Converte colunas de data
        if 'ano' in df.columns:
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
        
        if 'mes' in df.columns:
            df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
        
        # Cria coluna de data completa
        if 'ano' in df.columns and 'mes' in df.columns:
            df['data'] = pd.to_datetime(df[['ano', 'mes']].assign(day=1))
        
        return df
    
    def _remove_invalid_records(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove registros inválidos
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame sem registros inválidos
        """
        initial_count = len(df)
        
        # Remove registros com valores faltantes críticos
        critical_columns = ['ano', 'mes', 'regiao_administrativa', 'tipo_crime']
        df = df.dropna(subset=critical_columns)
        
        # Remove registros com valores negativos em ocorrências
        if 'total_ocorrencias' in df.columns:
            df = df[df['total_ocorrencias'] >= 0]
        
        # Remove registros com anos inválidos
        if 'ano' in df.columns:
            df = df[(df['ano'] >= 2020) & (df['ano'] <= 2025)]
        
        # Remove registros com meses inválidos
        if 'mes' in df.columns:
            df = df[(df['mes'] >= 1) & (df['mes'] <= 12)]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            logger.info(f"Registros removidos: {removed_count}")
        
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adiciona colunas derivadas
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com colunas derivadas
        """
        # Adiciona trimestre
        if 'mes' in df.columns:
            df['trimestre'] = df['mes'].apply(lambda x: (x - 1) // 3 + 1)
        
        # Adiciona semestre
        if 'mes' in df.columns:
            df['semestre'] = df['mes'].apply(lambda x: 1 if x <= 6 else 2)
        
        # Adiciona estação do ano
        if 'mes' in df.columns:
            def get_season(month):
                if month in [12, 1, 2]:
                    return 'Verão'
                elif month in [3, 4, 5]:
                    return 'Outono'
                elif month in [6, 7, 8]:
                    return 'Inverno'
                else:
                    return 'Primavera'
            
            df['estacao'] = df['mes'].apply(get_season)
        
        # Adiciona categoria de crime
        if 'tipo_crime' in df.columns:
            def get_crime_category(crime_type):
                cvli_crimes = ['Homicídio Doloso', 'Latrocínio', 'Lesão Corporal Seguida de Morte']
                violent_property = ['Roubo de Veículo', 'Roubo de Carga', 'Roubo a Transeunte', 
                                  'Roubo em Estabelecimento Comercial', 'Roubo de Aparelho Celular']
                non_violent_property = ['Furto de Veículo', 'Furto a Transeunte', 'Furto em Estabelecimento']
                vulnerable_groups = ['Estupro', 'Violência Doméstica']
                
                if crime_type in cvli_crimes:
                    return 'CVLI'
                elif crime_type in violent_property:
                    return 'Crime Violento contra Patrimônio'
                elif crime_type in non_violent_property:
                    return 'Crime contra Patrimônio sem Violência'
                elif crime_type in vulnerable_groups:
                    return 'Crime contra Grupos Vulneráveis'
                else:
                    return 'Outros'
            
            df['categoria_crime'] = df['tipo_crime'].apply(get_crime_category)
        
        return df
    
    def calculate_crime_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula taxas de criminalidade
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com taxas calculadas
        """
        if 'total_ocorrencias' in df.columns and 'populacao' in df.columns:
            # Taxa por 100 mil habitantes
            df['taxa_100k'] = (df['total_ocorrencias'] / df['populacao'] * 100000).round(2)
            
            # Taxa por 10 mil habitantes
            df['taxa_10k'] = (df['total_ocorrencias'] / df['populacao'] * 10000).round(2)
            
            # Taxa por mil habitantes
            df['taxa_1k'] = (df['total_ocorrencias'] / df['populacao'] * 1000).round(2)
        
        return df
    
    def create_time_series_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria features para análise de séries temporais
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            DataFrame com features temporais
        """
        if 'data' in df.columns:
            # Adiciona features temporais
            df['ano'] = df['data'].dt.year
            df['mes'] = df['data'].dt.month
            df['dia_semana'] = df['data'].dt.dayofweek
            df['dia_mes'] = df['data'].dt.day
            df['semana_ano'] = df['data'].dt.isocalendar().week
            
            # Adiciona lags temporais
            df = df.sort_values(['regiao_administrativa', 'tipo_crime', 'data'])
            
            for lag in [1, 3, 6, 12]:  # 1, 3, 6 e 12 meses
                if 'total_ocorrencias' in df.columns:
                    df[f'ocorrencias_lag_{lag}m'] = df.groupby(['regiao_administrativa', 'tipo_crime'])['total_ocorrencias'].shift(lag)
                
                if 'taxa_100k' in df.columns:
                    df[f'taxa_lag_{lag}m'] = df.groupby(['regiao_administrativa', 'tipo_crime'])['taxa_100k'].shift(lag)
        
        return df
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Valida qualidade dos dados
        
        Args:
            df: DataFrame com dados de criminalidade
            
        Returns:
            Dicionário com métricas de qualidade
        """
        quality_report = {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_records': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict(),
            'numeric_stats': {},
            'categorical_stats': {}
        }
        
        # Estatísticas numéricas
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            quality_report['numeric_stats'][col] = {
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'std': df[col].std(),
                'median': df[col].median()
            }
        
        # Estatísticas categóricas
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            quality_report['categorical_stats'][col] = {
                'unique_values': df[col].nunique(),
                'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'frequency': df[col].value_counts().iloc[0] if not df[col].empty else 0
            }
        
        return quality_report

def main():
    """
    Função principal para teste do módulo
    """
    # Exemplo de uso
    cleaner = DataCleaner()
    
    # Cria dados de exemplo
    sample_data = {
        'ano': [2023, 2023, 2023],
        'mes': [1, 2, 3],
        'regiao_administrativa': ['CENTRO', 'ZONA_SUL', 'ZONA_NORTE'],
        'tipo_crime': ['HOMICIDIO_DOLOSO', 'ROUBO_VEICULO', 'FURTO_VEICULO'],
        'total_ocorrencias': [10, 25, 15],
        'populacao': [100000, 200000, 300000]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Limpa dados
    df_clean = cleaner.clean_crime_data(df)
    
    # Calcula taxas
    df_clean = cleaner.calculate_crime_rates(df_clean)
    
    # Cria features temporais
    df_clean = cleaner.create_time_series_features(df_clean)
    
    # Valida qualidade
    quality_report = cleaner.validate_data_quality(df_clean)
    
    print("Dados limpos:")
    print(df_clean.head())
    
    print("\nRelatório de qualidade:")
    print(quality_report)

if __name__ == "__main__":
    main()
