"""
ANÁLISE PREDITIVA - 100% PYTHON (SEM DEPENDÊNCIAS R)
=====================================================

Sistema completo funcionando apenas com Python.
NENHUMA dependência de R ou rpy2.

Funciona imediatamente no Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importações condicionais (para não quebrar se algo faltar)
try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    st.warning("⚠️ statsmodels não instalado. ARIMA desabilitado.")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    st.warning("⚠️ Prophet não instalado. Prophet desabilitado.")

try:
    from sklearn.ensemble import RandomForestRegressor
    import xgboost as xgb
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    st.warning("⚠️ scikit-learn ou xgboost não instalado. ML desabilitado.")

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.preprocessing import StandardScaler
    LSTM_AVAILABLE = True
except ImportError:
    LSTM_AVAILABLE = False
    st.warning("⚠️ TensorFlow não instalado. LSTM desabilitado.")

# ============================================================================
# CLASSE: PREPARAÇÃO DE DADOS
# ============================================================================

class DataPrep:
    """Prepara dados para modelos"""
    
    @staticmethod
    def create_supervised(serie, n_lags=12):
        """Cria dados supervisionados para ML"""
        X, y = [], []
        for i in range(n_lags, len(serie)):
            X.append(serie[i-n_lags:i])
            y.append(serie[i])
        return np.array(X), np.array(y)

# ============================================================================
# MODELOS CLÁSSICOS
# ============================================================================

class ClassicalModels:
    """Modelos estatísticos"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def arima_forecast(serie, horizonte=6, order=(1,1,1)):
        """ARIMA"""
        if not ARIMA_AVAILABLE:
            return {'error': 'ARIMA não disponível'}
        
        try:
            modelo = ARIMA(serie, order=order)
            fitted = modelo.fit()
            
            forecast = fitted.forecast(steps=horizonte)
            forecast_df = fitted.get_forecast(steps=horizonte).summary_frame(alpha=0.05)
            
            return {
                'modelo': 'ARIMA',
                'forecast': forecast.tolist(),
                'lower': forecast_df['mean_ci_lower'].tolist(),
                'upper': forecast_df['mean_ci_upper'].tolist(),
                'fitted': fitted.fittedvalues.tolist()
            }
        except Exception as e:
            return {'error': str(e), 'modelo': 'ARIMA'}
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def prophet_forecast(df, horizonte=6):
        """Prophet"""
        if not PROPHET_AVAILABLE:
            return {'error': 'Prophet não disponível'}
        
        try:
            df_prophet = df.copy()
            df_prophet.columns = ['ds', 'y']
            
            modelo = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False
            )
            
            modelo.fit(df_prophet)
            
            future = modelo.make_future_dataframe(periods=horizonte, freq='MS')
            forecast = modelo.predict(future)
            
            n_hist = len(df)
            
            return {
                'modelo': 'Prophet',
                'forecast': forecast['yhat'][n_hist:].tolist(),
                'lower': forecast['yhat_lower'][n_hist:].tolist(),
                'upper': forecast['yhat_upper'][n_hist:].tolist()
            }
        except Exception as e:
            return {'error': str(e), 'modelo': 'Prophet'}

# ============================================================================
# MODELOS MACHINE LEARNING
# ============================================================================

class MLModels:
    """Modelos ML"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def random_forest_forecast(serie, horizonte=6, n_lags=12):
        """Random Forest"""
        if not ML_AVAILABLE:
            return {'error': 'ML não disponível'}
        
        try:
            X, y = DataPrep.create_supervised(serie, n_lags)
            
            modelo = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            modelo.fit(X, y)
            
            # Previsão
            forecast = []
            last_values = serie[-n_lags:].tolist()
            
            for _ in range(horizonte):
                X_pred = np.array([last_values[-n_lags:]]).reshape(1, -1)
                pred = modelo.predict(X_pred)[0]
                forecast.append(pred)
                last_values.append(pred)
            
            return {
                'modelo': 'Random Forest',
                'forecast': forecast
            }
        except Exception as e:
            return {'error': str(e), 'modelo': 'Random Forest'}
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def xgboost_forecast(serie, horizonte=6, n_lags=12):
        """XGBoost"""
        if not ML_AVAILABLE:
            return {'error': 'XGBoost não disponível'}
        
        try:
            X, y = DataPrep.create_supervised(serie, n_lags)
            
            modelo = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            modelo.fit(X, y, verbose=False)
            
            # Previsão
            forecast = []
            last_values = serie[-n_lags:].tolist()
            
            for _ in range(horizonte):
                X_pred = np.array([last_values[-n_lags:]]).reshape(1, -1)
                pred = modelo.predict(X_pred)[0]
                forecast.append(pred)
                last_values.append(pred)
            
            return {
                'modelo': 'XGBoost',
                'forecast': forecast
            }
        except Exception as e:
            return {'error': str(e), 'modelo': 'XGBoost'}

# ============================================================================
# MODELO LSTM
# ============================================================================

class DeepLearning:
    """Deep Learning"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def lstm_forecast(serie, horizonte=6, n_lags=12, epochs=30):
        """LSTM"""
        if not LSTM_AVAILABLE:
            return {'error': 'LSTM não disponível'}
        
        try:
            # Normalização
            scaler = StandardScaler()
            serie_scaled = scaler.fit_transform(serie.reshape(-1, 1)).flatten()
            
            X, y = DataPrep.create_supervised(serie_scaled, n_lags)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            # Modelo
            modelo = Sequential([
                LSTM(50, activation='relu', input_shape=(n_lags, 1)),
                Dropout(0.2),
                Dense(1)
            ])
            
            modelo.compile(optimizer='adam', loss='mse')
            
            # Treina (silencioso)
            modelo.fit(X, y, epochs=epochs, batch_size=32, verbose=0)
            
            # Previsão
            forecast = []
            last_values = serie_scaled[-n_lags:].tolist()
            
            for _ in range(horizonte):
                X_pred = np.array([last_values[-n_lags:]]).reshape(1, n_lags, 1)
                pred_scaled = modelo.predict(X_pred, verbose=0)[0, 0]
                forecast.append(pred_scaled)
                last_values.append(pred_scaled)
            
            # Desnormaliza
            forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, 1)).flatten()
            
            return {
                'modelo': 'LSTM',
                'forecast': forecast.tolist()
            }
        except Exception as e:
            return {'error': str(e), 'modelo': 'LSTM'}

# ============================================================================
# ENSEMBLE
# ============================================================================

class Ensemble:
    """Ensemble de modelos"""
    
    @staticmethod
    def create_ensemble(resultados):
        """Ensemble simples (média)"""
        forecasts = []
        
        for resultado in resultados:
            if 'error' not in resultado and 'forecast' in resultado:
                forecasts.append(resultado['forecast'])
        
        if not forecasts:
            return None
        
        # Média simples
        ensemble = np.mean(forecasts, axis=0)
        std = np.std(forecasts, axis=0)
        
        return {
            'modelo': 'Ensemble',
            'forecast': ensemble.tolist(),
            'lower': (ensemble - 1.96 * std).tolist(),
            'upper': (ensemble + 1.96 * std).tolist()
        }

# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="Análise Preditiva",
        page_icon="🔮",
        layout="wide"
    )
    
    st.title("🔮 Análise Preditiva - Violência Rio de Janeiro")
    st.markdown("Sistema 100% Python - Sem dependências R")
    
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
        
        modelos_disponiveis = []
        
        if ARIMA_AVAILABLE:
            use_arima = st.checkbox("ARIMA", value=True)
            if use_arima:
                modelos_disponiveis.append('arima')
        
        if PROPHET_AVAILABLE:
            use_prophet = st.checkbox("Prophet", value=True)
            if use_prophet:
                modelos_disponiveis.append('prophet')
        
        if ML_AVAILABLE:
            use_rf = st.checkbox("Random Forest", value=False)
            if use_rf:
                modelos_disponiveis.append('rf')
            
            use_xgb = st.checkbox("XGBoost", value=True)
            if use_xgb:
                modelos_disponiveis.append('xgb')
        
        if LSTM_AVAILABLE:
            use_lstm = st.checkbox("LSTM", value=False)
            if use_lstm:
                modelos_disponiveis.append('lstm')
        
        use_ensemble = st.checkbox("Ensemble", value=True)
        
        if not modelos_disponiveis:
            st.error("❌ Nenhum modelo disponível! Instale as dependências.")
            st.code("pip install statsmodels prophet xgboost scikit-learn")
            st.stop()
    
    # ==================== PROCESSAMENTO ====================
    
    # Verifica estrutura do DataFrame
    if 'valor' not in df.columns or 'data' not in df.columns:
        st.error("❌ CSV deve ter colunas 'data' e 'valor'")
        st.info("Usando dados de exemplo...")
        df = gerar_dados_exemplo()
    
    serie = df['valor'].values
    datas = pd.to_datetime(df['data'])
    
    if st.button("🚀 Executar Análise", type="primary"):
        
        resultados = []
        
        with st.spinner("Executando modelos..."):
            
            # ARIMA
            if 'arima' in modelos_disponiveis:
                with st.spinner("ARIMA..."):
                    resultados.append(ClassicalModels.arima_forecast(serie, horizonte))
            
            # Prophet
            if 'prophet' in modelos_disponiveis:
                with st.spinner("Prophet..."):
                    df_temp = pd.DataFrame({'data': datas, 'valor': serie})
                    resultados.append(ClassicalModels.prophet_forecast(df_temp, horizonte))
            
            # Random Forest
            if 'rf' in modelos_disponiveis:
                with st.spinner("Random Forest..."):
                    resultados.append(MLModels.random_forest_forecast(serie, horizonte))
            
            # XGBoost
            if 'xgb' in modelos_disponiveis:
                with st.spinner("XGBoost..."):
                    resultados.append(MLModels.xgboost_forecast(serie, horizonte))
            
            # LSTM
            if 'lstm' in modelos_disponiveis:
                with st.spinner("LSTM (pode demorar 30s)..."):
                    resultados.append(DeepLearning.lstm_forecast(serie, horizonte))
            
            # Ensemble
            if use_ensemble and len(resultados) > 1:
                ensemble = Ensemble.create_ensemble(resultados)
                if ensemble:
                    resultados.append(ensemble)
        
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
            line=dict(color='black', width=2)
        ))
        
        cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        # Previsões
        for i, resultado in enumerate(resultados):
            if 'error' in resultado:
                st.warning(f"⚠️ {resultado.get('modelo', 'Modelo')}: {resultado['error']}")
                continue
            
            fig.add_trace(go.Scatter(
                x=datas_futuro,
                y=resultado['forecast'],
                mode='lines+markers',
                name=resultado['modelo'],
                line=dict(color=cores[i % len(cores)], width=2)
            ))
            
            # Intervalo de confiança
            if 'lower' in resultado and 'upper' in resultado:
                fig.add_trace(go.Scatter(
                    x=datas_futuro.tolist() + datas_futuro.tolist()[::-1],
                    y=resultado['upper'] + resultado['lower'][::-1],
                    fill='toself',
                    fillcolor=f'rgba(255,0,0,0.1)',
                    line=dict(color='rgba(255,255,255,0)'),
                    showlegend=False,
                    hoverinfo='skip'
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
        
        st.markdown("### 📋 Previsões")
        
        df_prev = pd.DataFrame({
            'Data': datas_futuro.strftime('%Y-%m')
        })
        
        for resultado in resultados:
            if 'error' not in resultado and 'forecast' in resultado:
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

def gerar_dados_exemplo():
    """Gera dados exemplo"""
    np.random.seed(42)
    datas = pd.date_range(start='2020-01-01', end='2024-12-31', freq='MS')
    
    tendencia = np.linspace(100, 80, len(datas))
    sazonalidade = 10 * np.sin(np.arange(len(datas)) * 2 * np.pi / 12)
    ruido = np.random.normal(0, 5, len(datas))
    
    valores = tendencia + sazonalidade + ruido
    valores = np.maximum(valores, 0)
    
    return pd.DataFrame({'data': datas, 'valor': valores})

if __name__ == "__main__":
    main()