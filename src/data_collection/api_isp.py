"""
Módulo para coleta de dados do Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ)
Fonte: http://www.ispdados.rj.gov.br/
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
from typing import Dict, List, Optional
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ISPDadosCollector:
    """
    Classe para coleta de dados do ISP-RJ
    """
    
    def __init__(self, base_url: str = "http://www.ispdados.rj.gov.br"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_crime_data_by_month(self, start_year: int = 2020, end_year: int = 2025) -> pd.DataFrame:
        """
        Coleta dados de criminalidade por mês
        
        Args:
            start_year: Ano inicial
            end_year: Ano final
            
        Returns:
            DataFrame com dados de criminalidade
        """
        logger.info(f"Coletando dados de criminalidade de {start_year} a {end_year}")
        
        all_data = []
        
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                try:
                    # URL do ISP-RJ para dados mensais
                    url = f"{self.base_url}/Arquivos/Base{year}{month:02d}.csv"
                    
                    logger.info(f"Coletando dados de {year}-{month:02d}")
                    response = self.session.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        # Lê o CSV
                        df = pd.read_csv(url, encoding='latin-1', sep=';')
                        
                        # Adiciona colunas de ano e mês
                        df['ano'] = year
                        df['mes'] = month
                        df['data'] = pd.to_datetime(f"{year}-{month:02d}-01")
                        
                        all_data.append(df)
                        logger.info(f"Dados de {year}-{month:02d} coletados com sucesso")
                        
                    else:
                        logger.warning(f"Dados de {year}-{month:02d} não encontrados")
                        
                    # Delay para não sobrecarregar o servidor
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Erro ao coletar dados de {year}-{month:02d}: {str(e)}")
                    continue
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            logger.info(f"Total de registros coletados: {len(combined_df)}")
            return combined_df
        else:
            logger.warning("Nenhum dado foi coletado")
            return pd.DataFrame()
    
    def get_crime_data_by_region(self, year: int = 2024) -> pd.DataFrame:
        """
        Coleta dados de criminalidade por região administrativa
        
        Args:
            year: Ano dos dados
            
        Returns:
            DataFrame com dados por região
        """
        logger.info(f"Coletando dados por região para {year}")
        
        try:
            # URL para dados por região
            url = f"{self.base_url}/Arquivos/Base{year}_Regiao.csv"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                df = pd.read_csv(url, encoding='latin-1', sep=';')
                logger.info(f"Dados por região coletados: {len(df)} registros")
                return df
            else:
                logger.warning(f"Dados por região para {year} não encontrados")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados por região: {str(e)}")
            return pd.DataFrame()
    
    def get_crime_types_mapping(self) -> Dict[str, str]:
        """
        Retorna mapeamento dos tipos de crime conforme especificação
        
        Returns:
            Dicionário com mapeamento de tipos de crime
        """
        return {
            # Crimes Violentos Letais Intencionais (CVLI)
            'HOMICIDIO_DOLOSO': 'Homicídio doloso',
            'LATROCINIO': 'Latrocínio',
            'LESAO_CORPORAL_SEGUIDA_MORTE': 'Lesão corporal seguida de morte',
            
            # Crimes Violentos contra o Patrimônio
            'ROUBO_VEICULO': 'Roubo de veículo',
            'ROUBO_CARGA': 'Roubo de carga',
            'ROUBO_TRANSEUNTE': 'Roubo a transeunte',
            'ROUBO_ESTABELECIMENTO': 'Roubo em estabelecimento comercial',
            'ROUBO_CELULAR': 'Roubo de aparelho celular',
            
            # Crimes contra o Patrimônio sem Violência
            'FURTO_VEICULO': 'Furto de veículo',
            'FURTO_TRANSEUNTE': 'Furto a transeunte',
            'FURTO_ESTABELECIMENTO': 'Furto em estabelecimento',
            
            # Crimes contra Grupos Vulneráveis
            'ESTUPRO': 'Estupro',
            'VIOLENCIA_DOMESTICA': 'Violência doméstica',
            
            # Apreensões
            'APREENSAO_ARMA': 'Apreensão de arma de fogo',
            'APREENSAO_DROGA': 'Apreensão de drogas'
        }
    
    def standardize_crime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza os dados de criminalidade
        
        Args:
            df: DataFrame com dados brutos
            
        Returns:
            DataFrame padronizado
        """
        logger.info("Padronizando dados de criminalidade")
        
        # Mapeamento de colunas comuns do ISP-RJ
        column_mapping = {
            'MUNICIPIO': 'municipio',
            'REGIAO': 'regiao',
            'BAIRRO': 'bairro',
            'TIPO_CRIME': 'tipo_crime',
            'QUANTIDADE': 'quantidade',
            'MES': 'mes',
            'ANO': 'ano'
        }
        
        # Renomeia colunas se existirem
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Converte tipos de dados
        if 'quantidade' in df.columns:
            df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
        
        if 'ano' in df.columns:
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
        
        if 'mes' in df.columns:
            df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
        
        # Remove registros com dados faltantes
        df = df.dropna(subset=['quantidade', 'ano', 'mes'])
        
        # Filtra apenas dados do Rio de Janeiro
        if 'municipio' in df.columns:
            df = df[df['municipio'].str.contains('RIO DE JANEIRO', case=False, na=False)]
        
        logger.info(f"Dados padronizados: {len(df)} registros")
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str, output_dir: str = "data/raw"):
        """
        Salva dados em arquivo CSV
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo
            output_dir: Diretório de saída
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Dados salvos em: {filepath}")

def main():
    """
    Função principal para coleta de dados
    """
    collector = ISPDadosCollector()
    
    # Coleta dados mensais
    logger.info("Iniciando coleta de dados mensais...")
    monthly_data = collector.get_crime_data_by_month(2020, 2025)
    
    if not monthly_data.empty:
        # Padroniza dados
        monthly_data = collector.standardize_crime_data(monthly_data)
        
        # Salva dados
        collector.save_data(monthly_data, "isp_crime_data_monthly.csv")
        
        # Estatísticas básicas
        logger.info(f"Total de registros: {len(monthly_data)}")
        logger.info(f"Período: {monthly_data['ano'].min()} - {monthly_data['ano'].max()}")
        logger.info(f"Tipos de crime únicos: {monthly_data['tipo_crime'].nunique()}")
    
    # Coleta dados por região
    logger.info("Iniciando coleta de dados por região...")
    regional_data = collector.get_crime_data_by_region(2024)
    
    if not regional_data.empty:
        regional_data = collector.standardize_crime_data(regional_data)
        collector.save_data(regional_data, "isp_crime_data_regional.csv")

if __name__ == "__main__":
    main()

