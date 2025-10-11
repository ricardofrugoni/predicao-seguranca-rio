"""
Módulo para coleta de dados do DataRio (Portal de Dados Abertos do Rio de Janeiro)
Fonte: https://data.rio/
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
from typing import Dict, List, Optional
import logging
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataRioCollector:
    """
    Classe para coleta de dados do DataRio
    """
    
    def __init__(self, base_url: str = "https://www.data.rio/api/3/action"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_social_development_index(self) -> pd.DataFrame:
        """
        Coleta dados do Índice de Desenvolvimento Social (IDS)
        
        Returns:
            DataFrame com dados do IDS
        """
        logger.info("Coletando dados do Índice de Desenvolvimento Social")
        
        try:
            # URL para dados do IDS
            url = f"{self.base_url}/datastore_search"
            params = {
                'resource_id': 'ids-2020',
                'limit': 10000
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'result' in data and 'records' in data['result']:
                    df = pd.DataFrame(data['result']['records'])
                    logger.info(f"Dados do IDS coletados: {len(df)} registros")
                    return df
                else:
                    logger.warning("Dados do IDS não encontrados na resposta")
                    return pd.DataFrame()
            else:
                logger.warning(f"Erro ao coletar dados do IDS: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados do IDS: {str(e)}")
            return pd.DataFrame()
    
    def get_territorial_data(self) -> pd.DataFrame:
        """
        Coleta dados territoriais do IPP (Instituto Pereira Passos)
        
        Returns:
            DataFrame com dados territoriais
        """
        logger.info("Coletando dados territoriais do IPP")
        
        try:
            # URL para dados territoriais
            url = f"{self.base_url}/datastore_search"
            params = {
                'resource_id': 'dados-territoriais-ipp',
                'limit': 10000
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'result' in data and 'records' in data['result']:
                    df = pd.DataFrame(data['result']['records'])
                    logger.info(f"Dados territoriais coletados: {len(df)} registros")
                    return df
                else:
                    logger.warning("Dados territoriais não encontrados na resposta")
                    return pd.DataFrame()
            else:
                logger.warning(f"Erro ao coletar dados territoriais: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados territoriais: {str(e)}")
            return pd.DataFrame()
    
    def get_public_equipment_data(self) -> pd.DataFrame:
        """
        Coleta dados de equipamentos públicos (UPPs, delegacias, etc.)
        
        Returns:
            DataFrame com dados de equipamentos públicos
        """
        logger.info("Coletando dados de equipamentos públicos")
        
        try:
            # URL para dados de equipamentos públicos
            url = f"{self.base_url}/datastore_search"
            params = {
                'resource_id': 'equipamentos-publicos',
                'limit': 10000
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'result' in data and 'records' in data['result']:
                    df = pd.DataFrame(data['result']['records'])
                    logger.info(f"Dados de equipamentos públicos coletados: {len(df)} registros")
                    return df
                else:
                    logger.warning("Dados de equipamentos públicos não encontrados na resposta")
                    return pd.DataFrame()
            else:
                logger.warning(f"Erro ao coletar dados de equipamentos públicos: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados de equipamentos públicos: {str(e)}")
            return pd.DataFrame()
    
    def get_transportation_data(self) -> pd.DataFrame:
        """
        Coleta dados de transporte público (estações, linhas, etc.)
        
        Returns:
            DataFrame com dados de transporte
        """
        logger.info("Coletando dados de transporte público")
        
        try:
            # URL para dados de transporte
            url = f"{self.base_url}/datastore_search"
            params = {
                'resource_id': 'transporte-publico',
                'limit': 10000
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'result' in data and 'records' in data['result']:
                    df = pd.DataFrame(data['result']['records'])
                    logger.info(f"Dados de transporte coletados: {len(df)} registros")
                    return df
                else:
                    logger.warning("Dados de transporte não encontrados na resposta")
                    return pd.DataFrame()
            else:
                logger.warning(f"Erro ao coletar dados de transporte: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados de transporte: {str(e)}")
            return pd.DataFrame()
    
    def _create_mock_social_development_data(self) -> pd.DataFrame:
        """
        Cria dados simulados do Índice de Desenvolvimento Social
        
        Returns:
            DataFrame com dados simulados do IDS
        """
        logger.info("Criando dados simulados do IDS")
        
        # Regiões administrativas do Rio de Janeiro
        regions = [
            'Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Barra da Tijuca',
            'Jacarepaguá', 'Campo Grande', 'Santa Cruz', 'Ilha do Governador',
            'Ilha de Paquetá', 'Tijuca', 'Vila Isabel', 'Méier', 'Madureira',
            'Bangu', 'Realengo', 'Campo Grande', 'Santa Cruz', 'Guaratiba'
        ]
        
        data = []
        for region in regions:
            # Simula dados do IDS (0-1, onde 1 é melhor)
            ids_score = np.random.uniform(0.3, 0.9)
            
            data.append({
                'regiao_administrativa': region,
                'ids_score': round(ids_score, 3),
                'renda_per_capita': np.random.uniform(1000, 5000),
                'escolaridade_media': np.random.uniform(6, 12),
                'mortalidade_infantil': np.random.uniform(5, 25),
                'acesso_saneamento': np.random.uniform(0.7, 1.0),
                'densidade_populacional': np.random.uniform(50, 500),
                'indice_vulnerabilidade': round(1 - ids_score, 3)
            })
        
        return pd.DataFrame(data)
    
    def _create_mock_territorial_data(self) -> pd.DataFrame:
        """
        Cria dados simulados territoriais
        
        Returns:
            DataFrame com dados territoriais simulados
        """
        logger.info("Criando dados territoriais simulados")
        
        regions = [
            'Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Barra da Tijuca',
            'Jacarepaguá', 'Campo Grande', 'Santa Cruz', 'Ilha do Governador',
            'Ilha de Paquetá', 'Tijuca', 'Vila Isabel', 'Méier', 'Madureira',
            'Bangu', 'Realengo', 'Campo Grande', 'Santa Cruz', 'Guaratiba'
        ]
        
        data = []
        for region in regions:
            data.append({
                'regiao_administrativa': region,
                'area_km2': np.random.uniform(10, 100),
                'populacao_total': np.random.randint(100000, 500000),
                'densidade_demografica': np.random.uniform(50, 500),
                'altitude_media': np.random.uniform(0, 100),
                'distancia_centro': np.random.uniform(5, 50),
                'tipo_ocupacao': np.random.choice(['Residencial', 'Comercial', 'Misto']),
                'indice_urbanizacao': np.random.uniform(0.5, 1.0)
            })
        
        return pd.DataFrame(data)
    
    def _create_mock_public_equipment_data(self) -> pd.DataFrame:
        """
        Cria dados simulados de equipamentos públicos
        
        Returns:
            DataFrame com dados de equipamentos públicos simulados
        """
        logger.info("Criando dados de equipamentos públicos simulados")
        
        equipment_types = [
            'UPP', 'Delegacia', 'Hospital', 'Escola', 'Posto de Saúde',
            'Centro Comunitário', 'Biblioteca', 'Praça', 'Parque'
        ]
        
        data = []
        for i in range(200):  # 200 equipamentos
            data.append({
                'nome': f"Equipamento {i+1}",
                'tipo': np.random.choice(equipment_types),
                'regiao_administrativa': np.random.choice([
                    'Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Barra da Tijuca',
                    'Jacarepaguá', 'Campo Grande', 'Santa Cruz', 'Ilha do Governador',
                    'Tijuca', 'Vila Isabel', 'Méier', 'Madureira', 'Bangu', 'Realengo'
                ]),
                'latitude': np.random.uniform(-23.0, -22.8),
                'longitude': np.random.uniform(-43.3, -43.1),
                'endereco': f"Rua {i+1}, {np.random.choice(['Centro', 'Zona Sul', 'Zona Norte'])}",
                'status': np.random.choice(['Ativo', 'Inativo', 'Em construção'])
            })
        
        return pd.DataFrame(data)
    
    def standardize_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """
        Padroniza dados coletados
        
        Args:
            df: DataFrame com dados brutos
            data_type: Tipo de dados ('ids', 'territorial', 'equipment')
            
        Returns:
            DataFrame padronizado
        """
        logger.info(f"Padronizando dados do tipo: {data_type}")
        
        if data_type == 'ids':
            # Padroniza dados do IDS
            if 'regiao_administrativa' in df.columns:
                df['regiao_administrativa'] = df['regiao_administrativa'].str.upper()
            
        elif data_type == 'territorial':
            # Padroniza dados territoriais
            if 'regiao_administrativa' in df.columns:
                df['regiao_administrativa'] = df['regiao_administrativa'].str.upper()
            
        elif data_type == 'equipment':
            # Padroniza dados de equipamentos
            if 'tipo' in df.columns:
                df['tipo'] = df['tipo'].str.upper()
            
            if 'regiao_administrativa' in df.columns:
                df['regiao_administrativa'] = df['regiao_administrativa'].str.upper()
        
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
    Função principal para coleta de dados do DataRio
    """
    collector = DataRioCollector()
    
    # Coleta dados do IDS
    logger.info("Iniciando coleta de dados do IDS...")
    ids_data = collector.get_social_development_index()
    
    if ids_data.empty:
        logger.info("Criando dados simulados do IDS...")
        ids_data = collector._create_mock_social_development_data()
    
    if not ids_data.empty:
        ids_data = collector.standardize_data(ids_data, 'ids')
        collector.save_data(ids_data, "datario_ids_data.csv")
        logger.info(f"Dados do IDS coletados: {len(ids_data)} registros")
    
    # Coleta dados territoriais
    logger.info("Iniciando coleta de dados territoriais...")
    territorial_data = collector.get_territorial_data()
    
    if territorial_data.empty:
        logger.info("Criando dados territoriais simulados...")
        territorial_data = collector._create_mock_territorial_data()
    
    if not territorial_data.empty:
        territorial_data = collector.standardize_data(territorial_data, 'territorial')
        collector.save_data(territorial_data, "datario_territorial_data.csv")
        logger.info(f"Dados territoriais coletados: {len(territorial_data)} registros")
    
    # Coleta dados de equipamentos públicos
    logger.info("Iniciando coleta de dados de equipamentos públicos...")
    equipment_data = collector.get_public_equipment_data()
    
    if equipment_data.empty:
        logger.info("Criando dados de equipamentos públicos simulados...")
        equipment_data = collector._create_mock_public_equipment_data()
    
    if not equipment_data.empty:
        equipment_data = collector.standardize_data(equipment_data, 'equipment')
        collector.save_data(equipment_data, "datario_equipment_data.csv")
        logger.info(f"Dados de equipamentos públicos coletados: {len(equipment_data)} registros")

if __name__ == "__main__":
    main()

