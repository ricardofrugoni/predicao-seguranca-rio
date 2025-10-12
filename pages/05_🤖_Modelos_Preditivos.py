"""
🤖 MODELOS PREDITIVOS - Machine Learning para Previsão de Violência
================================================================

Página com 8 modelos de machine learning para previsão de violência:
- Modelos Clássicos: ARIMA, SARIMA, Prophet, Exp Smoothing
- Machine Learning: Random Forest, XGBoost, Gradient Boosting
- Deep Learning: LSTM
- Ensemble: Combinação inteligente de todos os modelos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Modelos Preditivos - Violência RJ",
    page_icon="🤖",
    layout="wide"
)

class TraditionalModels:
    """Modelos clássicos de séries temporais"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def arima_forecast(serie, horizonte=6, order=(1,1,1)):
        """ARIMA - Auto-Regressive Integrated Moving Average"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            
            modelo = ARIMA(serie, order=order)
            fitted = modelo.fit()
            forecast = fitted.forecast(steps=horizonte)
            forecast_df = fitted.get_forecast(steps=horizonte).summary_frame(alpha=0.05)
            
            return {
                'forecast': forecast.tolist(),
                'lower': forecast_df['mean_ci_lower'].tolist(),
                'upper': forecast_df['mean_ci_upper'].tolist(),
                'aic': fitted.aic,
                'bic': fitted.bic,
                'modelo': 'ARIMA'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no ARIMA: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def sarima_forecast(serie, horizonte=6, order=(1,1,1), seasonal_order=(1,1,1,12)):
        """SARIMA - ARIMA com sazonalidade"""
        try:
            from statsmodels.tsa.statespace.sarimax import SARIMAX
            
            modelo = SARIMAX(serie, order=order, seasonal_order=seasonal_order)
            fitted = modelo.fit()
            forecast = fitted.forecast(steps=horizonte)
            forecast_df = fitted.get_forecast(steps=horizonte).summary_frame(alpha=0.05)
            
            return {
                'forecast': forecast.tolist(),
                'lower': forecast_df['mean_ci_lower'].tolist(),
                'upper': forecast_df['mean_ci_upper'].tolist(),
                'aic': fitted.aic,
                'bic': fitted.bic,
                'modelo': 'SARIMA'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no SARIMA: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def prophet_forecast(df, horizonte=6):
        """Prophet - Framework do Facebook"""
        try:
            from prophet import Prophet
            
            df_prophet = df.copy()
            df_prophet.columns = ['ds', 'y']
            
            modelo = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                interval_width=0.95
            )
            modelo.fit(df_prophet)
            
            future = modelo.make_future_dataframe(periods=horizonte, freq='MS')
            forecast = modelo.predict(future)
            
            n_hist = len(df)
            
            return {
                'forecast': forecast['yhat'][n_hist:].tolist(),
                'lower': forecast['yhat_lower'][n_hist:].tolist(),
                'upper': forecast['yhat_upper'][n_hist:].tolist(),
                'modelo': 'Prophet'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Prophet: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def exp_smoothing_forecast(serie, horizonte=6):
        """Exponential Smoothing"""
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            
            modelo = ExponentialSmoothing(serie, trend='add', seasonal='add', seasonal_periods=12)
            fitted = modelo.fit()
            forecast = fitted.forecast(steps=horizonte)
            
            return {
                'forecast': forecast.tolist(),
                'lower': [f * 0.8 for f in forecast],  # Aproximação
                'upper': [f * 1.2 for f in forecast],
                'modelo': 'Exp Smoothing'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Exp Smoothing: {str(e)}")
            return None

class MLModels:
    """Modelos de Machine Learning"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def random_forest_forecast(serie, horizonte=6, n_lags=12):
        """Random Forest"""
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_absolute_error
            
            # Prepara features
            X, y = [], []
            for i in range(n_lags, len(serie)):
                X.append(serie[i-n_lags:i])
                y.append(serie[i])
            
            X, y = np.array(X), np.array(y)
            
            if len(X) < 10:
                return None
            
            modelo = RandomForestRegressor(n_estimators=100, random_state=42)
            modelo.fit(X, y)
            
            # Previsões
            previsoes = []
            ultima_janela = serie[-n_lags:]
            
            for _ in range(horizonte):
                pred = modelo.predict([ultima_janela])[0]
                previsoes.append(max(0, pred))  # Não permite valores negativos
                ultima_janela = np.append(ultima_janela[1:], pred)
            
            # Calcula MAE
            y_pred = modelo.predict(X)
            mae = mean_absolute_error(y, y_pred)
            
            return {
                'forecast': previsoes,
                'lower': [p * 0.8 for p in previsoes],
                'upper': [p * 1.2 for p in previsoes],
                'mae': mae,
                'feature_importance': modelo.feature_importances_.tolist(),
                'modelo': 'Random Forest'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Random Forest: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def xgboost_forecast(serie, horizonte=6, n_lags=12):
        """XGBoost - Gradient Boosting otimizado"""
        try:
            import xgboost as xgb
            from sklearn.metrics import mean_absolute_error
            
            # Prepara features
            X, y = [], []
            for i in range(n_lags, len(serie)):
                X.append(serie[i-n_lags:i])
                y.append(serie[i])
            
            X, y = np.array(X), np.array(y)
            
            if len(X) < 10:
                return None
            
            modelo = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            modelo.fit(X, y)
            
            # Previsões
            previsoes = []
            ultima_janela = serie[-n_lags:]
            
            for _ in range(horizonte):
                pred = modelo.predict([ultima_janela])[0]
                previsoes.append(max(0, pred))
                ultima_janela = np.append(ultima_janela[1:], pred)
            
            # Calcula MAE
            y_pred = modelo.predict(X)
            mae = mean_absolute_error(y, y_pred)
            
            return {
                'forecast': previsoes,
                'lower': [p * 0.8 for p in previsoes],
                'upper': [p * 1.2 for p in previsoes],
                'mae': mae,
                'feature_importance': modelo.feature_importances_.tolist(),
                'modelo': 'XGBoost'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no XGBoost: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def gradient_boosting_forecast(serie, horizonte=6, n_lags=12):
        """Gradient Boosting clássico"""
        try:
            from sklearn.ensemble import GradientBoostingRegressor
            from sklearn.metrics import mean_absolute_error
            
            # Prepara features
            X, y = [], []
            for i in range(n_lags, len(serie)):
                X.append(serie[i-n_lags:i])
                y.append(serie[i])
            
            X, y = np.array(X), np.array(y)
            
            if len(X) < 10:
                return None
            
            modelo = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            modelo.fit(X, y)
            
            # Previsões
            previsoes = []
            ultima_janela = serie[-n_lags:]
            
            for _ in range(horizonte):
                pred = modelo.predict([ultima_janela])[0]
                previsoes.append(max(0, pred))
                ultima_janela = np.append(ultima_janela[1:], pred)
            
            # Calcula MAE
            y_pred = modelo.predict(X)
            mae = mean_absolute_error(y, y_pred)
            
            return {
                'forecast': previsoes,
                'lower': [p * 0.8 for p in previsoes],
                'upper': [p * 1.2 for p in previsoes],
                'mae': mae,
                'feature_importance': modelo.feature_importances_.tolist(),
                'modelo': 'Gradient Boosting'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Gradient Boosting: {str(e)}")
            return None

class DeepLearningModels:
    """Modelos de Deep Learning"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def lstm_forecast(serie, horizonte=6, n_lags=12, epochs=50):
        """LSTM - Long Short-Term Memory"""
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense
            from sklearn.preprocessing import MinMaxScaler
            from sklearn.metrics import mean_squared_error
            
            # Normaliza dados
            scaler = MinMaxScaler()
            serie_scaled = scaler.fit_transform(serie.reshape(-1, 1)).flatten()
            
            # Prepara dados para LSTM
            X, y = [], []
            for i in range(n_lags, len(serie_scaled)):
                X.append(serie_scaled[i-n_lags:i])
                y.append(serie_scaled[i])
            
            X, y = np.array(X), np.array(y)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            if len(X) < 10:
                return None
            
            # Cria modelo LSTM
            modelo = Sequential([
                LSTM(50, return_sequences=True, input_shape=(n_lags, 1)),
                LSTM(50, return_sequences=False),
                Dense(25),
                Dense(1)
            ])
            
            modelo.compile(optimizer='adam', loss='mse')
            
            # Treina modelo
            modelo.fit(X, y, epochs=epochs, batch_size=1, verbose=0)
            
            # Previsões
            previsoes = []
            ultima_janela = serie_scaled[-n_lags:]
            
            for _ in range(horizonte):
                pred = modelo.predict([ultima_janela.reshape(1, n_lags, 1)], verbose=0)[0][0]
                previsoes.append(pred)
                ultima_janela = np.append(ultima_janela[1:], pred)
            
            # Desnormaliza
            previsoes = scaler.inverse_transform(np.array(previsoes).reshape(-1, 1)).flatten()
            previsoes = np.maximum(previsoes, 0)  # Não permite valores negativos
            
            # Calcula RMSE
            y_pred = modelo.predict(X, verbose=0)
            y_pred_orig = scaler.inverse_transform(y_pred)
            y_orig = scaler.inverse_transform(y.reshape(-1, 1))
            rmse = np.sqrt(mean_squared_error(y_orig, y_pred_orig))
            
            return {
                'forecast': previsoes.tolist(),
                'lower': [p * 0.8 for p in previsoes],
                'upper': [p * 1.2 for p in previsoes],
                'rmse': rmse,
                'modelo': 'LSTM'
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no LSTM: {str(e)}")
            return None

class AdvancedEnsemble:
    """Ensemble inteligente de modelos"""
    
    @staticmethod
    def weighted_ensemble(resultados):
        """Combina modelos com pesos baseados na performance"""
        if not resultados:
            return None
        
        # Remove resultados None
        resultados_validos = [r for r in resultados if r is not None]
        
        if not resultados_validos:
            return None
        
        # Calcula pesos baseados na performance
        pesos = []
        for resultado in resultados_validos:
            if 'mae' in resultado:
                peso = 1 / (resultado['mae'] + 1)  # Inverso do MAE
            elif 'rmse' in resultado:
                peso = 1 / (resultado['rmse'] + 1)  # Inverso do RMSE
            elif 'aic' in resultado:
                peso = 1 / (resultado['aic'] + 1)  # Inverso do AIC
            else:
                peso = 1  # Peso padrão
            
            pesos.append(peso)
        
        # Normaliza pesos
        pesos = np.array(pesos)
        pesos = pesos / pesos.sum()
        
        # Combina previsões
        forecast_ensemble = []
        lower_ensemble = []
        upper_ensemble = []
        
        horizonte = len(resultados_validos[0]['forecast'])
        
        for i in range(horizonte):
            pred = sum(r['forecast'][i] * peso for r, peso in zip(resultados_validos, pesos))
            lower = sum(r['lower'][i] * peso for r, peso in zip(resultados_validos, pesos))
            upper = sum(r['upper'][i] * peso for r, peso in zip(resultados_validos, pesos))
            
            forecast_ensemble.append(pred)
            lower_ensemble.append(lower)
            upper_ensemble.append(upper)
        
        return {
            'forecast': forecast_ensemble,
            'lower': lower_ensemble,
            'upper': upper_ensemble,
            'pesos': pesos.tolist(),
            'n_modelos': len(resultados_validos),
            'modelo': 'Ensemble'
        }

def load_sample_data():
    """Carrega dados de exemplo"""
    np.random.seed(42)
    datas = pd.date_range(start='2020-01-01', end='2024-12-31', freq='MS')
    
    # Simula série temporal com tendência e sazonalidade
    tendencia = np.linspace(100, 80, len(datas))
    sazonalidade = 10 * np.sin(np.arange(len(datas)) * 2 * np.pi / 12)
    ruido = np.random.normal(0, 5, len(datas))
    
    valores = tendencia + sazonalidade + ruido
    valores = np.maximum(valores, 0)  # Não permite valores negativos
    
    return pd.DataFrame({
        'data': datas,
        'valor': valores
    })

def create_comparison_chart(resultados, datas_hist, datas_futuro):
    """Cria gráfico comparativo dos modelos"""
    fig = go.Figure()
    
    # Histórico
    fig.add_trace(go.Scatter(
        x=datas_hist,
        y=resultados[0].get('forecast', [0]) if (resultados and len(resultados) > 0 and isinstance(resultados[0], dict)) else [0],
        mode='lines',
        name='Histórico',
        line=dict(color='black', width=2)
    ))
    
    # Cores para diferentes modelos
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
    
    # Adiciona previsões de cada modelo
    for i, (nome, resultado) in enumerate(resultados):
        if resultado and 'forecast' in resultado:
            fig.add_trace(go.Scatter(
                x=datas_futuro,
                y=resultado['forecast'],
                mode='lines+markers',
                name=nome,
                line=dict(color=cores[i % len(cores)], width=2, dash='dash')
            ))
            
            # Intervalo de confiança
            if 'lower' in resultado and 'upper' in resultado:
                fig.add_trace(go.Scatter(
                    x=datas_futuro.tolist() + datas_futuro.tolist()[::-1],
                    y=resultado['upper'] + resultado['lower'][::-1],
                    fill='toself',
                    fillcolor=cores[i % len(cores)].replace(')', ', 0.2)').replace('rgb', 'rgba'),
                    line=dict(color='rgba(255,255,255,0)'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    fig.update_layout(
        title='Comparação de Modelos Preditivos',
        xaxis_title='Data',
        yaxis_title='Ocorrências',
        height=500,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def create_performance_table(resultados):
    """Cria tabela de performance dos modelos"""
    dados_tabela = []
    
    for nome, resultado in resultados:
        if resultado:
            linha = {'Modelo': nome}
            
            if 'mae' in resultado:
                linha['MAE'] = f"{resultado['mae']:.2f}"
            if 'rmse' in resultado:
                linha['RMSE'] = f"{resultado['rmse']:.2f}"
            if 'aic' in resultado:
                linha['AIC'] = f"{resultado['aic']:.2f}"
            if 'bic' in resultado:
                linha['BIC'] = f"{resultado['bic']:.2f}"
            
            dados_tabela.append(linha)
    
    return pd.DataFrame(dados_tabela)

def main():
    """Função principal"""
    st.title("🤖 Modelos Preditivos - Machine Learning")
    st.markdown("8 modelos de machine learning para previsão de violência no Rio de Janeiro")
    
    # Carrega dados
    df = load_sample_data()
    serie = df['valor'].values
    datas_hist = df['data']
    
    # Sidebar com controles
    st.sidebar.title("🎛️ Configurações")
    
    # Parâmetros
    horizonte = st.sidebar.slider("Horizonte (meses)", 1, 24, 6)
    n_lags = st.sidebar.slider("Lags (meses)", 3, 24, 12)
    epochs = st.sidebar.slider("Epochs LSTM", 10, 200, 50)
    
    # Modelos a executar
    st.sidebar.subheader("🤖 Modelos")
    
    modelos_selecionados = st.sidebar.multiselect(
        "Selecione os modelos:",
        [
            "ARIMA", "SARIMA", "Prophet", "Exp Smoothing",
            "Random Forest", "XGBoost", "Gradient Boosting", "LSTM"
        ],
        default=["Prophet", "XGBoost", "Random Forest"]
    )
    
    executar_ensemble = st.sidebar.checkbox("Executar Ensemble", value=True)
    
    # Botão de execução
    if st.sidebar.button("🚀 Executar Modelos", type="primary"):
        
        resultados = []
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Executa modelos selecionados
        total_modelos = len(modelos_selecionados)
        if executar_ensemble:
            total_modelos += 1
        
        progresso = 0
        
        # Modelos clássicos
        if "ARIMA" in modelos_selecionados:
            status_text.text("Executando ARIMA...")
            resultado = TraditionalModels.arima_forecast(serie, horizonte)
            if resultado:
                resultados.append(("ARIMA", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        if "SARIMA" in modelos_selecionados:
            status_text.text("Executando SARIMA...")
            resultado = TraditionalModels.sarima_forecast(serie, horizonte)
            if resultado:
                resultados.append(("SARIMA", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        if "Prophet" in modelos_selecionados:
            status_text.text("Executando Prophet...")
            resultado = TraditionalModels.prophet_forecast(df, horizonte)
            if resultado:
                resultados.append(("Prophet", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        if "Exp Smoothing" in modelos_selecionados:
            status_text.text("Executando Exp Smoothing...")
            resultado = TraditionalModels.exp_smoothing_forecast(serie, horizonte)
            if resultado:
                resultados.append(("Exp Smoothing", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        # Machine Learning
        if "Random Forest" in modelos_selecionados:
            status_text.text("Executando Random Forest...")
            resultado = MLModels.random_forest_forecast(serie, horizonte, n_lags)
            if resultado:
                resultados.append(("Random Forest", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        if "XGBoost" in modelos_selecionados:
            status_text.text("Executando XGBoost...")
            resultado = MLModels.xgboost_forecast(serie, horizonte, n_lags)
            if resultado:
                resultados.append(("XGBoost", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        if "Gradient Boosting" in modelos_selecionados:
            status_text.text("Executando Gradient Boosting...")
            resultado = MLModels.gradient_boosting_forecast(serie, horizonte, n_lags)
            if resultado:
                resultados.append(("Gradient Boosting", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        # Deep Learning
        if "LSTM" in modelos_selecionados:
            status_text.text("Executando LSTM... (pode levar alguns minutos)")
            resultado = DeepLearningModels.lstm_forecast(serie, horizonte, n_lags, epochs)
            if resultado:
                resultados.append(("LSTM", resultado))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        # Ensemble
        if executar_ensemble and resultados:
            status_text.text("Executando Ensemble...")
            ensemble_result = AdvancedEnsemble.weighted_ensemble([r[1] for r in resultados])
            if ensemble_result:
                resultados.append(("Ensemble", ensemble_result))
            progresso += 1
            progress_bar.progress(progresso / total_modelos)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Modelos executados com sucesso!")
        
        # Cria datas futuras
        ultima_data = datas_hist.iloc[-1]
        datas_futuro = pd.date_range(
            start=ultima_data + timedelta(days=30),
            periods=horizonte,
            freq='MS'
        )
        
        # Visualizações
        if resultados:
            st.success(f"✅ {len(resultados)} modelos executados com sucesso!")
            
            # DEBUG - Análise de resultados
            print("="*50)
            print("DEBUG - Análise de resultados")
            print("="*50)
            print(f"Tipo de resultados: {type(resultados)}")
            print(f"É lista? {isinstance(resultados, list)}")
            print(f"Tamanho: {len(resultados) if resultados else 0}")

            if resultados:
                print(f"\nPrimeiro elemento:")
                print(f"  Tipo: {type(resultados[0])}")
                print(f"  Conteúdo: {resultados[0]}")
                
                if isinstance(resultados[0], dict):
                    print(f"  Chaves disponíveis: {list(resultados[0].keys())}")
                    print(f"  Tem 'forecast'? {'forecast' in resultados[0]}")
                else:
                    print(f"  ERRO: Não é um dicionário!")
            else:
                print("\nResultados está vazio!")
            print("="*50)
            
            # Gráfico comparativo
            st.markdown("## 📊 Comparação de Modelos")
            fig_comparison = create_comparison_chart(resultados, datas_hist, datas_futuro)
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Tabela de performance
            st.markdown("## 📋 Performance dos Modelos")
            df_performance = create_performance_table(resultados)
            if not df_performance.empty:
                st.dataframe(df_performance, use_container_width=True)
            
            # Tabela de previsões
            st.markdown("## 📈 Previsões Detalhadas")
            
            df_prev = pd.DataFrame({
                'Data': datas_futuro.strftime('%Y-%m')
            })
            
            for nome, resultado in resultados:
                if resultado and 'forecast' in resultado:
                    df_prev[nome] = np.array(resultado['forecast']).round(0).astype(int)
            
            st.dataframe(df_prev, use_container_width=True)
            
            # Download
            csv = df_prev.to_csv(index=False)
            st.download_button(
                "📥 Download Previsões CSV",
                csv,
                f"previsoes_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
            
            # Feature Importance (se disponível)
            modelos_com_importance = [r for r in resultados if r[1] and 'feature_importance' in r[1]]
            if modelos_com_importance:
                st.markdown("## 🔍 Feature Importance")
                
                for nome, resultado in modelos_com_importance:
                    if resultado['feature_importance']:
                        fig_importance = px.bar(
                            x=list(range(len(resultado['feature_importance']))),
                            y=resultado['feature_importance'],
                            title=f"Feature Importance - {nome}",
                            labels={'x': 'Lag', 'y': 'Importance'}
                        )
                        st.plotly_chart(fig_importance, use_container_width=True)
        
        else:
            st.warning("⚠️ Nenhum modelo foi executado com sucesso. Verifique os dados e configurações.")
    
    # Informações sobre os modelos
    st.markdown("## 📚 Informações sobre os Modelos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Modelos Clássicos
        - **ARIMA**: Auto-Regressive Integrated Moving Average
        - **SARIMA**: ARIMA com sazonalidade
        - **Prophet**: Framework do Facebook (robusto)
        - **Exp Smoothing**: Suavização exponencial
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 Machine Learning
        - **Random Forest**: Ensemble de árvores
        - **XGBoost**: Gradient Boosting otimizado
        - **Gradient Boosting**: Boosting clássico
        - **LSTM**: Deep Learning (recorrente)
        """)
    
    st.markdown("""
    ### 💡 Recomendações de Uso
    
    **Para análise rápida:**
    - Use Prophet + XGBoost
    
    **Para máxima precisão:**
    - Use Ensemble completo
    
    **Para produção:**
    - Use Prophet (robusto e rápido)
    
    **Para apresentações:**
    - Use Ensemble (impressiona)
    """)

if __name__ == "__main__":
    main()
