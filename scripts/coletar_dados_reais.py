"""
📥 SCRIPT - Coletar Dados Reais
================================

Script para coletar dados reais de criminalidade do Rio de Janeiro.

USO:
    python scripts/coletar_dados_reais.py

RESULTADO:
    - data/raw/isp_ocorrencias.csv
    - data/raw/ibge_populacao.csv
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collection.api_real_data import coletar_dados_reais
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Executa coleta de dados"""
    
    print("=" * 70)
    print(" 🔌 COLETA DE DADOS REAIS - RIO DE JANEIRO")
    print("=" * 70)
    print()
    
    # Configurações
    ano_inicio = 2020
    ano_fim = 2024
    save_dir = "data/raw"
    
    print(f"📅 Período: {ano_inicio} - {ano_fim}")
    print(f"💾 Salvando em: {save_dir}/")
    print()
    
    # Coleta
    try:
        dados = coletar_dados_reais(ano_inicio, ano_fim, save_dir)
        
        # Resumo
        print()
        print("=" * 70)
        print(" 📊 RESUMO DA COLETA")
        print("=" * 70)
        
        if dados:
            for fonte, df in dados.items():
                print(f"\n✅ {fonte.upper()}:")
                print(f"   Registros: {len(df)}")
                print(f"   Colunas: {list(df.columns)[:5]}...")
                if 'data' in df.columns:
                    print(f"   Período: {df['data'].min()} a {df['data'].max()}")
        else:
            print("❌ Nenhum dado coletado")
        
        print()
        print("=" * 70)
        print(" ✅ COLETA FINALIZADA!")
        print("=" * 70)
        print()
        print("📁 Arquivos criados:")
        save_path = Path(save_dir)
        for arquivo in save_path.glob("*.csv"):
            tamanho = arquivo.stat().st_size / 1024  # KB
            print(f"   - {arquivo.name} ({tamanho:.1f} KB)")
        
    except Exception as e:
        logger.error(f"Erro na coleta: {e}")
        print()
        print("=" * 70)
        print(" ❌ ERRO NA COLETA")
        print("=" * 70)
        print()
        print("Verifique:")
        print("  1. Conexão com internet")
        print("  2. APIs estão funcionando")
        print("  3. Credenciais (se necessário)")
        print()
        raise


if __name__ == "__main__":
    main()

