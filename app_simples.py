"""
🔮 ANÁLISE PREDITIVA - VERSÃO ULTRA-SIMPLES
============================================

Funciona com APENAS: streamlit, pandas, numpy, plotly
SEM dependências externas problemáticas.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# MODELOS SIMPLES (SEM DEPENDÊNCIAS EXTERNAS)
# ============================================================================

class SimpleModels:
    """Modelos simples usando apenas numpy"""
    
    @staticmethod
    def media_movel(serie, horizonte=6, janela=3):
        """Média móvel simples"""
        ultima_media = np.mean(serie[-janela:])
        forecast = [ultima_media] * horizonte
        return {
            'modelo': 'Média Móvel',
            'forecast': forecast
        }
    
    @staticmethod
    def tendencia_linear(serie, horizonte=6):
        """Tendência linear simples"""
        x = np.arange(len(serie))
        coef = np.polyfit(x, serie, 1)
        
        forecast = []
        for i in range(1, horizonte + 1):
            pred = coef[0] * (len(serie) + i) + coef[1]
            forecast.append(max(0, pred))  # Não pode ser negativo
        
        return {
            'modelo': 'Tendência Linear',
            'forecast': forecast
        }
    
    @staticmethod
    def sazonalidade_simples(serie, horizonte=6):
        """Sazonalidade simples (média por mês)"""
        # Assumindo dados mensais
        if len(serie) >= 12:
            sazonalidade = []
            for i in range(12):
                indices = [j for j in range(len(serie)) if j % 12 == i]
                if indices:
                    sazonalidade.append(np.mean([serie[j] for j in indices]))
        else:
            sazonalidade = [np.mean(serie)] * 12
        
        forecast = []
        for i in range(horizonte):
            mes = (len(serie) + i) % 12
            forecast.append(sazonalidade[mes])
        
        return {
            'modelo': 'Sazonalidade',
            'forecast': forecast
        }
    
    @staticmethod
    def ensemble_simples(serie, horizonte=6):
        """Ensemble simples (média dos modelos)"""
        modelos = [
            SimpleModels.media_movel(serie, horizonte),
            SimpleModels.tendencia_linear(serie, horizonte),
            SimpleModels.sazonalidade_simples(serie, horizonte)
        ]
        
        forecasts = [m['forecast'] for m in modelos]
        ensemble = np.mean(forecasts, axis=0)
        
        return {
            'modelo': 'Ensemble Simples',
            'forecast': ensemble.tolist()
        }

# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="Análise Preditiva Simples",
        page_icon="🔮",
        layout="wide"
    )
    
    st.title("🔮 Análise Preditiva - Violência Rio de Janeiro")
    st.markdown("**Versão Ultra-Simples - Sem dependências externas**")
    
    # ==================== SIDEBAR ====================
    
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Upload
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
                df = gerar_dados_exemplo()
        else:
            df = gerar_dados_exemplo()
        
        st.markdown("---")
        
        # Parâmetros
        crime_tipo = st.selectbox(
            "Tipo de Crime",
            ["Homicídio Doloso", "Roubo de Veículo", "Roubo a Transeunte"]
        )
        
        regiao = st.selectbox(
            "Região",
            ["Consolidado", "Centro", "Zona Sul", "Zona Norte"]
        )
        
        horizonte = st.slider("Horizonte (meses)", 1, 12, 6)
        
        st.markdown("---")
        
        # Modelos
        st.subheader("🎯 Selecione Modelos")
        
        use_media = st.checkbox("Média Móvel", value=True)
        use_tendencia = st.checkbox("Tendência Linear", value=True)
        use_sazonal = st.checkbox("Sazonalidade", value=True)
        use_ensemble = st.checkbox("Ensemble", value=True)
        
        modelos_selecionados = []
        if use_media:
            modelos_selecionados.append('media')
        if use_tendencia:
            modelos_selecionados.append('tendencia')
        if use_sazonal:
            modelos_selecionados.append('sazonal')
        if use_ensemble:
            modelos_selecionados.append('ensemble')
        
        if not modelos_selecionados:
            st.warning("⚠️ Selecione pelo menos um modelo!")
            st.stop()
    
    # ==================== PROCESSAMENTO ====================
    
    # Verifica estrutura do DataFrame
    if 'valor' not in df.columns or 'data' not in df.columns:
        st.error("❌ CSV deve ter colunas 'data' e 'valor'")
        st.info("Usando dados de exemplo...")
        df = gerar_dados_exemplo()
    
    serie = df['valor'].values
    datas = pd.to_datetime(df['data'])
    
    # Mostra dados
    st.subheader("📊 Dados Históricos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total de Registros", len(serie))
        st.metric("Média", f"{np.mean(serie):.1f}")
        st.metric("Último Valor", f"{serie[-1]:.1f}")
    
    with col2:
        st.metric("Mínimo", f"{np.min(serie):.1f}")
        st.metric("Máximo", f"{np.max(serie):.1f}")
        st.metric("Desvio Padrão", f"{np.std(serie):.1f}")
    
    if st.button("🚀 Executar Análise", type="primary"):
        
        resultados = []
        
        with st.spinner("Executando modelos..."):
            
            # Média Móvel
            if 'media' in modelos_selecionados:
                resultados.append(SimpleModels.media_movel(serie, horizonte))
            
            # Tendência Linear
            if 'tendencia' in modelos_selecionados:
                resultados.append(SimpleModels.tendencia_linear(serie, horizonte))
            
            # Sazonalidade
            if 'sazonal' in modelos_selecionados:
                resultados.append(SimpleModels.sazonalidade_simples(serie, horizonte))
            
            # Ensemble
            if 'ensemble' in modelos_selecionados:
                resultados.append(SimpleModels.ensemble_simples(serie, horizonte))
        
        st.success(f"✅ {len(resultados)} modelo(s) executado(s)!")
        
        # ==================== VISUALIZAÇÃO ====================
        
        # Datas futuras
        ultima_data = datas.iloc[-1]
        datas_futuro = pd.date_range(
            start=ultima_data + pd.DateOffset(months=1),
            periods=horizonte,
            freq='MS'
        )
        
        # Gráfico
        fig = go.Figure()
        
        # Histórico
        fig.add_trace(go.Scatter(
            x=datas,
            y=serie,
            mode='lines',
            name='Histórico',
            line=dict(color='black', width=3)
        ))
        
        cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        # Previsões
        for i, resultado in enumerate(resultados):
            fig.add_trace(go.Scatter(
                x=datas_futuro,
                y=resultado['forecast'],
                mode='lines+markers',
                name=resultado['modelo'],
                line=dict(color=cores[i % len(cores)], width=2)
            ))
        
        fig.update_layout(
            title=f"Previsão: {crime_tipo} - {regiao}",
            xaxis_title="Data",
            yaxis_title="Ocorrências",
            height=600,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ==================== TABELA ====================
        
        st.subheader("📋 Previsões")
        
        df_prev = pd.DataFrame({
            'Data': datas_futuro.strftime('%Y-%m')
        })
        
        for resultado in resultados:
            df_prev[resultado['modelo']] = np.array(resultado['forecast']).round(0).astype(int)
        
        st.dataframe(df_prev, use_container_width=True)
        
        # Download
        csv = df_prev.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            f"previsoes_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
        
        # ==================== MÉTRICAS ====================
        
        st.subheader("📈 Análise dos Resultados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Modelos Executados", len(resultados))
        
        with col2:
            if resultados:
                media_prev = np.mean([np.mean(r['forecast']) for r in resultados])
                st.metric("Média das Previsões", f"{media_prev:.1f}")
        
        with col3:
            if resultados:
                max_prev = np.max([np.max(r['forecast']) for r in resultados])
                st.metric("Máxima Previsão", f"{max_prev:.1f}")

def gerar_dados_exemplo():
    """Gera dados exemplo"""
    np.random.seed(42)
    datas = pd.date_range(start='2020-01-01', end='2024-12-31', freq='MS')
    
    # Tendência decrescente
    tendencia = np.linspace(100, 80, len(datas))
    
    # Sazonalidade (mais crimes no verão)
    sazonalidade = 10 * np.sin(np.arange(len(datas)) * 2 * np.pi / 12)
    
    # Ruído
    ruido = np.random.normal(0, 5, len(datas))
    
    valores = tendencia + sazonalidade + ruido
    valores = np.maximum(valores, 0)  # Não pode ser negativo
    
    return pd.DataFrame({'data': datas, 'valor': valores})

if __name__ == "__main__":
    main()


