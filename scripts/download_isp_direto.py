"""
📥 DOWNLOAD DIRETO - Dados ISP-RJ
==================================

Script para baixar dados diretamente do site do ISP-RJ.
Não precisa de API, faz download direto dos arquivos CSV.

USO:
    python scripts/download_isp_direto.py
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_isp_direto():
    """Baixa dados diretamente do ISP-RJ"""
    
    print("=" * 70)
    print(" 📥 DOWNLOAD DIRETO - ISP-RJ")
    print("=" * 70)
    print()
    
    # URLs dos arquivos CSV do ISP-RJ
    urls = {
        'mensal_cisp': 'http://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv',
        'municipio': 'http://www.ispdados.rj.gov.br/Arquivos/BaseMunicipioMensal.csv',
    }
    
    # Criar diretório
    save_path = Path('data/raw')
    save_path.mkdir(parents=True, exist_ok=True)
    
    dados_baixados = {}
    
    for nome, url in urls.items():
        try:
            logger.info(f"Baixando: {nome}...")
            print(f"📡 Baixando {nome}...")
            
            # Baixar CSV
            df = pd.read_csv(
                url,
                encoding='latin-1',
                sep=';',
                low_memory=False
            )
            
            logger.info(f"✅ Baixado: {len(df)} registros")
            print(f"   ✅ {len(df):,} registros")
            
            # Filtrar apenas Rio de Janeiro
            if 'munic' in df.columns:
                df_rio = df[df['munic'] == 'Rio de Janeiro'].copy()
                logger.info(f"Filtrado Rio: {len(df_rio)} registros")
                print(f"   🗺️  Rio de Janeiro: {len(df_rio):,} registros")
            else:
                df_rio = df
            
            # Salvar
            output_file = save_path / f'isp_{nome}.csv'
            df_rio.to_csv(output_file, index=False)
            logger.info(f"Salvo em: {output_file}")
            print(f"   💾 Salvo: {output_file}")
            
            dados_baixados[nome] = df_rio
            print()
            
        except Exception as e:
            logger.error(f"❌ Erro ao baixar {nome}: {e}")
            print(f"   ❌ Erro: {e}")
            print()
    
    # Resumo
    print("=" * 70)
    print(" 📊 RESUMO")
    print("=" * 70)
    print()
    
    for nome, df in dados_baixados.items():
        print(f"📁 {nome}:")
        print(f"   Registros: {len(df):,}")
        print(f"   Colunas: {len(df.columns)}")
        print(f"   Período: {df['ano'].min() if 'ano' in df.columns else 'N/A'} - {df['ano'].max() if 'ano' in df.columns else 'N/A'}")
        print()
    
    print("=" * 70)
    print(" ✅ DOWNLOAD CONCLUÍDO!")
    print("=" * 70)
    print()
    print(f"📁 Arquivos salvos em: {save_path.absolute()}/")
    print()
    print("🎯 PRÓXIMO PASSO:")
    print("   Use estes dados nos seus modelos preditivos!")
    print()
    
    return dados_baixados


if __name__ == "__main__":
    try:
        dados = download_isp_direto()
        
        # Mostrar primeiras linhas
        if dados:
            print("👀 Visualização dos dados:")
            print()
            for nome, df in list(dados.items())[:1]:  # Mostra só o primeiro
                print(f"📋 {nome} (primeiras 5 linhas):")
                print(df.head())
                print()
                print(f"📋 Colunas disponíveis:")
                print(list(df.columns))
                print()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique:")
        print("  1. Conexão com internet")
        print("  2. Site do ISP-RJ está acessível")
        print("  3. URLs ainda estão válidas")

