"""
🔮 PREVISÃO 2026 - Com Dados Reais
==================================

Script para baixar dados atualizados (incluindo 2025) e 
fazer previsão para 2026.

USO:
    python scripts/prever_2026.py
    
RESULTADO:
    - Dados 2020-2025 baixados
    - Modelos treinados
    - Previsões para 2026 (12 meses)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


def baixar_dados_atualizados():
    """Baixa dados do ISP-RJ incluindo 2025"""
    
    print("=" * 70)
    print(" 📥 BAIXANDO DADOS ATUALIZADOS (2020-2025)")
    print("=" * 70)
    print()
    
    try:
        # URL do ISP-RJ
        url = 'http://www.ispdados.rj.gov.br/Arquivos/BaseMunicipioMensal.csv'
        
        logger.info("Baixando dados do ISP-RJ...")
        print("📡 Conectando ao ISP-RJ...")
        
        df = pd.read_csv(url, encoding='latin-1', sep=';', low_memory=False)
        
        logger.info(f"✅ Baixado: {len(df)} registros")
        print(f"✅ Baixado: {len(df):,} registros totais")
        print()
        
        # Filtrar Rio de Janeiro
        df_rio = df[df['munic'] == 'Rio de Janeiro'].copy()
        
        logger.info(f"Filtrado Rio: {len(df_rio)} registros")
        print(f"🗺️  Rio de Janeiro: {len(df_rio):,} registros")
        print()
        
        # Verificar período
        anos_disponiveis = sorted(df_rio['ano'].unique())
        print(f"📅 Anos disponíveis: {min(anos_disponiveis)} - {max(anos_disponiveis)}")
        print()
        
        # Salvar
        save_path = Path('data/raw')
        save_path.mkdir(parents=True, exist_ok=True)
        
        output_file = save_path / 'isp_rio_atualizado.csv'
        df_rio.to_csv(output_file, index=False)
        
        logger.info(f"Salvo em: {output_file}")
        print(f"💾 Salvo: {output_file}")
        print()
        
        return df_rio
        
    except Exception as e:
        logger.error(f"Erro ao baixar: {e}")
        print(f"❌ Erro: {e}")
        return None


def preparar_serie_temporal(df):
    """Prepara dados para previsão"""
    
    print("=" * 70)
    print(" 🔧 PREPARANDO DADOS")
    print("=" * 70)
    print()
    
    # Criar coluna de data
    df['data'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01')
    
    # Agregar por mês (soma de todos os tipos de crime)
    colunas_crimes = [
        'hom_doloso', 'latrocinio', 'lesao_corp_morte',
        'roubo_veiculo', 'roubo_comercio', 'roubo_transeunte',
        'furto_veiculo', 'estupro'
    ]
    
    # Selecionar apenas colunas que existem
    colunas_disponiveis = [col for col in colunas_crimes if col in df.columns]
    
    df['total_crimes'] = df[colunas_disponiveis].sum(axis=1)
    
    # Série temporal mensal
    serie = df.groupby('data')['total_crimes'].sum().sort_index()
    
    print(f"📊 Série temporal criada:")
    print(f"   Período: {serie.index.min()} até {serie.index.max()}")
    print(f"   Meses: {len(serie)}")
    print(f"   Total de crimes no período: {serie.sum():,.0f}")
    print()
    
    return serie


def prever_2026(serie):
    """Faz previsão para 2026 com múltiplos modelos"""
    
    print("=" * 70)
    print(" 🔮 PREVISÃO PARA 2026")
    print("=" * 70)
    print()
    
    resultados = {}
    
    # 1. Prophet
    print("🤖 Modelo 1: Prophet...")
    try:
        from prophet import Prophet
        
        df_prophet = pd.DataFrame({
            'ds': serie.index,
            'y': serie.values
        })
        
        modelo = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False
        )
        modelo.fit(df_prophet)
        
        # Prever 12 meses de 2026
        future = pd.date_range(
            start=serie.index.max() + pd.DateOffset(months=1),
            periods=12,
            freq='MS'
        )
        future_df = pd.DataFrame({'ds': future})
        
        previsao = modelo.predict(future_df)
        resultados['Prophet'] = previsao['yhat'].values
        
        print(f"   ✅ Prophet - Média prevista: {previsao['yhat'].mean():.0f} crimes/mês")
        
    except Exception as e:
        print(f"   ⚠️ Prophet falhou: {e}")
    
    print()
    
    # 2. ARIMA
    print("🤖 Modelo 2: ARIMA...")
    try:
        from statsmodels.tsa.arima.model import ARIMA
        
        modelo = ARIMA(serie.values, order=(1, 1, 1))
        fitted = modelo.fit()
        
        previsao = fitted.forecast(steps=12)
        resultados['ARIMA'] = previsao
        
        print(f"   ✅ ARIMA - Média prevista: {previsao.mean():.0f} crimes/mês")
        
    except Exception as e:
        print(f"   ⚠️ ARIMA falhou: {e}")
    
    print()
    
    # 3. Média Móvel Simples (fallback)
    print("🤖 Modelo 3: Média Móvel...")
    try:
        # Média dos últimos 12 meses
        media = serie.tail(12).mean()
        previsao = np.full(12, media)
        resultados['Media_Movel'] = previsao
        
        print(f"   ✅ Média Móvel - Previsão: {media:.0f} crimes/mês")
        
    except Exception as e:
        print(f"   ⚠️ Média Móvel falhou: {e}")
    
    print()
    
    # Ensemble (média dos modelos)
    if resultados:
        ensemble = np.mean(list(resultados.values()), axis=0)
        resultados['Ensemble'] = ensemble
        
        print(f"🎯 Ensemble (média) - Previsão: {ensemble.mean():.0f} crimes/mês")
        print()
    
    return resultados


def salvar_resultados(resultados, serie):
    """Salva previsões em CSV"""
    
    print("=" * 70)
    print(" 💾 SALVANDO RESULTADOS")
    print("=" * 70)
    print()
    
    # Criar DataFrame com previsões
    datas_2026 = pd.date_range(
        start=serie.index.max() + pd.DateOffset(months=1),
        periods=12,
        freq='MS'
    )
    
    df_previsoes = pd.DataFrame({
        'data': datas_2026,
        'mes': datas_2026.month,
        'ano': 2026
    })
    
    # Adicionar previsões de cada modelo
    for modelo, previsao in resultados.items():
        df_previsoes[modelo] = previsao
    
    # Salvar
    save_path = Path('data/processed')
    save_path.mkdir(parents=True, exist_ok=True)
    
    output_file = save_path / 'previsoes_2026.csv'
    df_previsoes.to_csv(output_file, index=False)
    
    print(f"✅ Previsões salvas em: {output_file}")
    print()
    
    # Mostrar tabela
    print("📊 PREVISÕES PARA 2026:")
    print()
    print(df_previsoes.to_string(index=False))
    print()
    
    return df_previsoes


def main():
    """Função principal"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🔮 PREVISÃO DE CRIMINALIDADE 2026" + " " * 20 + "║")
    print("║" + " " * 20 + "Município do Rio de Janeiro" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # 1. Baixar dados atualizados
    df = baixar_dados_atualizados()
    
    if df is None:
        print("❌ Falha ao baixar dados. Abortando...")
        return
    
    # 2. Preparar série temporal
    serie = preparar_serie_temporal(df)
    
    # 3. Fazer previsões
    resultados = prever_2026(serie)
    
    if not resultados:
        print("❌ Nenhum modelo conseguiu fazer previsão. Abortando...")
        return
    
    # 4. Salvar resultados
    df_previsoes = salvar_resultados(resultados, serie)
    
    # 5. Resumo final
    print("=" * 70)
    print(" ✅ PROCESSO CONCLUÍDO!")
    print("=" * 70)
    print()
    print("📈 TENDÊNCIA PARA 2026:")
    
    if 'Ensemble' in resultados:
        media_2026 = resultados['Ensemble'].mean()
        media_2025 = serie.tail(12).mean()
        
        variacao = ((media_2026 - media_2025) / media_2025) * 100
        
        print(f"   Média 2025: {media_2025:,.0f} crimes/mês")
        print(f"   Média prevista 2026: {media_2026:,.0f} crimes/mês")
        print(f"   Variação: {variacao:+.1f}%")
        
        if variacao > 0:
            print(f"   ⚠️  Tendência de AUMENTO")
        else:
            print(f"   ✅ Tendência de REDUÇÃO")
    
    print()
    print("📁 Arquivos gerados:")
    print("   - data/raw/isp_rio_atualizado.csv")
    print("   - data/processed/previsoes_2026.csv")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

