"""
🔌 API REAL DATA - Coleta de Dados Reais
=========================================

Módulo para coletar dados reais de criminalidade do Rio de Janeiro
através de APIs oficiais (ISP-RJ, Data.Rio, IBGE).
"""

import requests
import pandas as pd
import logging
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ISPRJCollector:
    """Coletor de dados do ISP-RJ (Instituto de Segurança Pública)"""
    
    BASE_URL = "http://www.ispdados.rj.gov.br/api"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
    
    def coletar_ocorrencias(self, 
                           ano_inicio: int = 2020,
                           ano_fim: int = 2024,
                           municipio: str = "Rio de Janeiro") -> Optional[pd.DataFrame]:
        """
        Coleta registros de ocorrências criminais
        
        Args:
            ano_inicio: Ano inicial
            ano_fim: Ano final
            municipio: Nome do município
            
        Returns:
            DataFrame com ocorrências ou None se falhar
        """
        try:
            endpoint = f"{self.BASE_URL}/ocorrencias"
            
            params = {
                'municipio': municipio,
                'ano_inicio': ano_inicio,
                'ano_fim': ano_fim
            }
            
            logger.info(f"Coletando dados ISP-RJ: {ano_inicio}-{ano_fim}")
            
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            dados = response.json()
            df = pd.DataFrame(dados)
            
            logger.info(f"Coletados {len(df)} registros do ISP-RJ")
            
            return self._processar_dados_isp(df)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao coletar dados ISP-RJ: {e}")
            return None
    
    def _processar_dados_isp(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa e padroniza dados do ISP"""
        # Padronizar colunas
        df['data'] = pd.to_datetime(df['data'])
        df['municipio'] = df['municipio'].str.strip()
        
        # Calcular taxa por 100k habitantes (se tiver população)
        if 'populacao' in df.columns and 'total_ocorrencias' in df.columns:
            df['taxa_100k'] = (df['total_ocorrencias'] / df['populacao']) * 100000
        
        return df


class DataRioCollector:
    """Coletor de dados do Data.Rio (Portal de Dados Abertos do Rio)"""
    
    BASE_URL = "https://www.data.rio/api/3/action"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
    
    def listar_datasets(self) -> List[Dict]:
        """Lista todos os datasets disponíveis"""
        try:
            endpoint = f"{self.BASE_URL}/package_list"
            response = self.session.get(endpoint, timeout=self.timeout)
            response.raise_for_status()
            
            return response.json()['result']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao listar datasets: {e}")
            return []
    
    def coletar_seguranca(self, 
                         resource_id: str,
                         limit: int = 100000) -> Optional[pd.DataFrame]:
        """
        Coleta dados de segurança pública
        
        Args:
            resource_id: ID do recurso no Data.Rio
            limit: Limite de registros
            
        Returns:
            DataFrame com dados ou None
        """
        try:
            endpoint = f"{self.BASE_URL}/datastore_search"
            
            params = {
                'resource_id': resource_id,
                'limit': limit
            }
            
            logger.info(f"Coletando dados Data.Rio: {resource_id}")
            
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            dados = response.json()
            registros = dados['result']['records']
            
            df = pd.DataFrame(registros)
            
            logger.info(f"Coletados {len(df)} registros do Data.Rio")
            
            return self._processar_dados_datario(df)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao coletar Data.Rio: {e}")
            return None
    
    def _processar_dados_datario(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa dados do Data.Rio"""
        # Converter datas
        date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df


class IBGECollector:
    """Coletor de dados do IBGE (população e geografia)"""
    
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1"
    CODIGO_RIO = "3304557"  # Código IBGE do município do Rio
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
    
    def coletar_populacao(self) -> Optional[pd.DataFrame]:
        """Coleta projeção populacional do Rio de Janeiro"""
        try:
            endpoint = f"{self.BASE_URL}/projecoes/populacao/{self.CODIGO_RIO}"
            
            logger.info("Coletando população IBGE")
            
            response = self.session.get(endpoint, timeout=self.timeout)
            response.raise_for_status()
            
            dados = response.json()
            
            # Converte para DataFrame
            df = pd.DataFrame([{
                'ano': dados['projecao']['ano'],
                'populacao': dados['projecao']['populacao'],
                'municipio': 'Rio de Janeiro',
                'codigo_ibge': self.CODIGO_RIO
            }])
            
            logger.info(f"População coletada: {dados['projecao']['populacao']:,}")
            
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao coletar IBGE: {e}")
            return None


class RealDataManager:
    """Gerenciador central para coleta de dados reais"""
    
    def __init__(self):
        self.isp = ISPRJCollector()
        self.datario = DataRioCollector()
        self.ibge = IBGECollector()
    
    def coletar_dados_completos(self, 
                                ano_inicio: int = 2020,
                                ano_fim: int = 2024,
                                save_path: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
        """
        Coleta dados de todas as fontes
        
        Args:
            ano_inicio: Ano inicial
            ano_fim: Ano final
            save_path: Caminho para salvar (opcional)
            
        Returns:
            Dicionário com DataFrames de cada fonte
        """
        resultados = {}
        
        # 1. ISP-RJ
        logger.info("=" * 50)
        logger.info("COLETANDO DADOS ISP-RJ")
        df_isp = self.isp.coletar_ocorrencias(ano_inicio, ano_fim)
        if df_isp is not None:
            resultados['isp'] = df_isp
            if save_path:
                df_isp.to_csv(save_path / "isp_ocorrencias.csv", index=False)
                logger.info(f"✅ ISP salvo em: {save_path / 'isp_ocorrencias.csv'}")
        
        # 2. Data.Rio
        logger.info("=" * 50)
        logger.info("COLETANDO DADOS DATA.RIO")
        # Primeiro, listar datasets disponíveis
        datasets = self.datario.listar_datasets()
        logger.info(f"Datasets disponíveis: {len(datasets)}")
        
        # TODO: Buscar resource_id correto de segurança pública
        # Exemplo: df_datario = self.datario.coletar_seguranca('RESOURCE_ID')
        
        # 3. IBGE
        logger.info("=" * 50)
        logger.info("COLETANDO DADOS IBGE")
        df_ibge = self.ibge.coletar_populacao()
        if df_ibge is not None:
            resultados['ibge'] = df_ibge
            if save_path:
                df_ibge.to_csv(save_path / "ibge_populacao.csv", index=False)
                logger.info(f"✅ IBGE salvo em: {save_path / 'ibge_populacao.csv'}")
        
        logger.info("=" * 50)
        logger.info(f"COLETA FINALIZADA: {len(resultados)} fontes")
        
        return resultados


# Função auxiliar para uso direto
def coletar_dados_reais(ano_inicio: int = 2020,
                        ano_fim: int = 2024,
                        save_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Função principal para coletar dados reais
    
    Args:
        ano_inicio: Ano inicial
        ano_fim: Ano final  
        save_dir: Diretório para salvar
        
    Returns:
        Dicionário com dados coletados
        
    Exemplo:
        >>> dados = coletar_dados_reais(2020, 2024)
        >>> df_isp = dados['isp']
        >>> df_ibge = dados['ibge']
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    
    manager = RealDataManager()
    return manager.coletar_dados_completos(ano_inicio, ano_fim, save_path)


if __name__ == "__main__":
    # Teste
    logging.basicConfig(level=logging.INFO)
    
    print("🔌 COLETANDO DADOS REAIS...")
    print("=" * 60)
    
    dados = coletar_dados_reais(2020, 2024)
    
    print("\n📊 RESUMO:")
    for fonte, df in dados.items():
        print(f"  {fonte.upper()}: {len(df)} registros")
    
    print("\n✅ Coleta finalizada!")
    print("Arquivos salvos em: data/raw/")

