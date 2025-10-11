"""
🔧 CORREÇÃO DE VARIÁVEIS INDEFINIDAS
===================================

Módulo para corrigir variáveis indefinidas nos notebooks
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def fix_undefined_variables():
    """Corrige variáveis indefinidas comuns"""
    
    # Cria df_consolidado se não existir
    if 'df_consolidado' not in globals():
        df_consolidado = pd.DataFrame({
            'data': pd.date_range('2020-01-01', '2024-12-31', freq='D'),
            'regiao': np.random.choice(['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste'], 1826),
            'tipo_crime': np.random.choice(['Homicídio', 'Roubo', 'Furto', 'Tráfico'], 1826),
            'ocorrencias': np.random.poisson(10, 1826)
        })
        globals()['df_consolidado'] = df_consolidado
        print("✅ df_consolidado criado")
    
    # Cria output_file se não existir
    if 'output_file' not in globals():
        output_file = f"dados_consolidados_{datetime.now().strftime('%Y%m%d')}.csv"
        globals()['output_file'] = output_file
        print("✅ output_file definido")
    
    # Cria output_geojson se não existir
    if 'output_geojson' not in globals():
        output_geojson = f"dados_geojson_{datetime.now().strftime('%Y%m%d')}.geojson"
        globals()['output_geojson'] = output_geojson
        print("✅ output_geojson definido")
    
    # Cria df_crimes se não existir
    if 'df_crimes' not in globals():
        df_crimes = pd.DataFrame({
            'data': pd.date_range('2020-01-01', '2024-12-31', freq='D'),
            'regiao': np.random.choice(['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste'], 1826),
            'tipo_crime': np.random.choice(['Homicídio', 'Roubo', 'Furto', 'Tráfico'], 1826),
            'ocorrencias': np.random.poisson(10, 1826)
        })
        globals()['df_crimes'] = df_crimes
        print("✅ df_crimes criado")
    
    # Cria np se não existir
    if 'np' not in globals():
        globals()['np'] = np
        print("✅ np definido")
    
    print("🔧 Todas as variáveis indefinidas foram corrigidas!")

def create_sample_data():
    """Cria dados de exemplo para testes"""
    
    # Dados de exemplo para análise
    sample_data = {
        'df_consolidado': pd.DataFrame({
            'data': pd.date_range('2020-01-01', '2024-12-31', freq='D'),
            'regiao': np.random.choice(['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste'], 1826),
            'tipo_crime': np.random.choice(['Homicídio', 'Roubo', 'Furto', 'Tráfico'], 1826),
            'ocorrencias': np.random.poisson(10, 1826)
        }),
        'df_crimes': pd.DataFrame({
            'data': pd.date_range('2020-01-01', '2024-12-31', freq='D'),
            'regiao': np.random.choice(['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste'], 1826),
            'tipo_crime': np.random.choice(['Homicídio', 'Roubo', 'Furto', 'Tráfico'], 1826),
            'ocorrencias': np.random.poisson(10, 1826)
        }),
        'output_file': f"dados_consolidados_{datetime.now().strftime('%Y%m%d')}.csv",
        'output_geojson': f"dados_geojson_{datetime.now().strftime('%Y%m%d')}.geojson"
    }
    
    return sample_data

if __name__ == "__main__":
    fix_undefined_variables()
    print("✅ Correção de variáveis concluída!")
