"""
DASHBOARD HÍBRIDO OTIMIZADO: PYTHON + R NO STREAMLIT
====================================================

Arquitetura recomendada:
1. Análises PESADAS em R → Executadas 1x, resultados em cache
2. Predições RÁPIDAS → Python nativo ou rpy2 leve
3. Interface 100% Python/Streamlit

Vantagens:
✅ Deploy fácil no Streamlit Cloud
✅ Performance excelente
✅ Manutenção simples
✅ Debug facilitado
✅ Melhor UX (sem travamentos)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import pickle
from functools import lru_cache
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Modelos Python
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

# ============================================================================
# CONFIGURAÇÃO DE PATHS
# ============================================================================

BASE_DIR = Path('.')
R_SCRIPTS_DIR = BASE_DIR / 'src' / 'r_scripts'
DATA_DIR = BASE_DIR / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'
CACHE_DIR = DATA_DIR / 'r_cache'
OUTPUT_DIR = BASE_DIR / 'outputs'

# Cria diretórios necessários
for dir_path in [CACHE_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CLASSE: GERENCIADOR DE CACHE R
# ============================================================================

class RCacheManager:
    """
    Gerencia cache de análises R pesadas
    Análises espaciais são executadas 1x e cacheadas
    """
    
    @staticmethod
    def get_cache_key(tipo_analise, **params):
        """Gera chave única de cache"""
        params_str = '_'.join([f"{k}={v}" for k, v in sorted(params.items())])
        return f"{tipo_analise}_{params_str}.json"
    
    @staticmethod
    def load_from_cache(cache_key):
        """Carrega resultado do cache"""
        cache_file = CACHE_DIR / cache_key
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def save_to_cache(cache_key, data):
        """Salva resultado no cache"""
        cache_file = CACHE_DIR / cache_key
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================================
# CLASSE: EXECUTOR R VIA SUBPROCESS (ANÁLISES PESADAS)
# ============================================================================

class RHeavyAnalysis:
    """
    Executa análises R PESADAS via subprocess
    Use para: Moran's I, LISA, Kernel Density, GWR
    
    Estas análises são LENTAS mas precisam rodar 1x apenas
    """
    
    @staticmethod
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def moran_analysis(geodata_path, column_name, k_neighbors=5):
        """Análise de Moran (PESADA) - Executa 1x, cacheia"""
        
        # Verifica cache
        cache_key = RCacheManager.get_cache_key(
            'moran',
            column=column_name,
            k=k_neighbors
        )
        
        cached = RCacheManager.load_from_cache(cache_key)
        if cached:
            st.info("📦 Usando resultado cacheado da análise R")
            return cached
        
        # Executa análise R
        st.info("🔄 Executando análise espacial em R... (pode levar ~30s)")
        
        temp_output = DATA_DIR / 'temp_moran.json'
        
        try:
            result = subprocess.run([
                'Rscript',
                str(R_SCRIPTS_DIR / 'moran_analysis.R'),
                geodata_path,
                str(temp_output),
                column_name,
                str(k_neighbors)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                raise Exception(f"Erro R: {result.stderr}")
            
            # Lê resultado
            with open(temp_output, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Salva no cache
            RCacheManager.save_to_cache(cache_key, data)
            
            return data
            
        except Exception as e:
            st.error(f"❌ Erro na análise R: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def kernel_density(points_geojson, bandwidth='auto'):
        """Kernel Density Estimation (PESADA)"""
        
        cache_key = RCacheManager.get_cache_key(
            'kde',
            bandwidth=bandwidth
        )
        
        cached = RCacheManager.load_from_cache(cache_key)
        if cached:
            return cached
        
        st.info("🔄 Calculando Kernel Density em R...")
        
        temp_output = DATA_DIR / 'temp_kde.json'
        
        try:
            subprocess.run([
                'Rscript',
                str(R_SCRIPTS_DIR / 'kernel_density.R'),
                points_geojson,
                str(temp_output),
                bandwidth
            ], check=True, timeout=120)
            
            with open(temp_output, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            RCacheManager.save_to_cache(cache_key, data)
            return data
            
        except Exception as e:
            st.error(f"❌ Erro no KDE: {str(e)}")
            return None

# ============================================================================
# CLASSE: PREDIÇÕES PYTHON (RÁPIDAS)
# ============================================================================

class FastPythonPredictors:
    """
    Predições em Python puro - RÁPIDAS
    Usadas em tempo real no Streamlit
    """
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def arima_forecast(serie, horizonte=6, order=(1,1,1)):
        """ARIMA Python - Rápido"""
        try:
            modelo = ARIMA(serie, order=order)
            fitted = modelo.fit()
            forecast = fitted.forecast(steps=horizonte)
            forecast_df = fitted.get_forecast(steps=horizonte).summary_frame(alpha=0.05)
            
            return {
                'forecast': forecast.tolist(),
                'lower': forecast_df['mean_ci_lower'].tolist(),
                'upper': forecast_df['mean_ci_upper'].tolist(),
                'aic': fitted.aic
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no ARIMA: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def prophet_forecast(df, horizonte=6):
        """Prophet - Rápido e preciso"""
        try:
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
                'upper': forecast['yhat_upper'][n_hist:].tolist()
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Prophet: {str(e)}")
            return None
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def random_forest_forecast(df, target_col, horizonte=6):
        """Random Forest - Rápido"""
        try:
            # Prepara features
            df_features = df.copy()
            df_features['mes'] = df_features['data'].dt.month
            df_features['ano'] = df_features['data'].dt.year
            df_features['lag_1'] = df_features[target_col].shift(1)
            df_features['lag_2'] = df_features[target_col].shift(2)
            df_features['lag_3'] = df_features[target_col].shift(3)
            
            # Remove NaN
            df_features = df_features.dropna()
            
            if len(df_features) < 10:
                return None
            
            # Treina modelo
            X = df_features[['mes', 'ano', 'lag_1', 'lag_2', 'lag_3']]
            y = df_features[target_col]
            
            modelo = RandomForestRegressor(n_estimators=100, random_state=42)
            modelo.fit(X, y)
            
            # Previsões
            ultima_data = df_features['data'].iloc[-1]
            previsoes = []
            
            for i in range(horizonte):
                proxima_data = ultima_data + timedelta(days=30 * (i + 1))
                
                features = pd.DataFrame({
                    'mes': [proxima_data.month],
                    'ano': [proxima_data.year],
                    'lag_1': [df_features[target_col].iloc[-1]],
                    'lag_2': [df_features[target_col].iloc[-2]] if len(df_features) > 1 else [0],
                    'lag_3': [df_features[target_col].iloc[-3]] if len(df_features) > 2 else [0]
                })
                
                pred = modelo.predict(features)[0]
                previsoes.append(max(0, pred))  # Não permite valores negativos
            
            return {
                'forecast': previsoes,
                'lower': [p * 0.8 for p in previsoes],  # Aproximação
                'upper': [p * 1.2 for p in previsoes]
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Random Forest: {str(e)}")
            return None

# ============================================================================
# CLASSE: PREDIÇÕES R LEVES (OPCIONAL - rpy2)
# ============================================================================

class LightRPredictors:
    """
    Predições R LEVES via rpy2
    Use apenas se necessário (ex: modelo específico do R)
    """
    
    def __init__(self):
        try:
            from rpy2.robjects import r, pandas2ri, globalenv
            from rpy2.robjects.packages import importr
            pandas2ri.activate()
            self.forecast = importr('forecast')
            self.enabled = True
        except:
            self.enabled = False
            st.warning("⚠️ rpy2 não disponível. Usando apenas Python.")
    
    @st.cache_data(show_spinner=False)
    def auto_arima_light(self, serie, horizonte=6):
        """Auto ARIMA leve do R"""
        if not self.enabled:
            return None
        
        try:
            from rpy2.robjects import r, globalenv
            import rpy2.robjects as ro
            
            ts_r = ro.FloatVector(serie)
            globalenv['ts_values'] = ts_r
            
            r_code = f"""
            suppressMessages(library(forecast))
            ts_data <- ts(ts_values, frequency=12)
            modelo <- auto.arima(ts_data, stepwise=TRUE, approximation=TRUE)
            prev <- forecast(modelo, h={horizonte})
            list(
                forecast = as.numeric(prev$mean),
                lower = as.numeric(prev$lower[,2]),
                upper = as.numeric(prev$upper[,2])
            )
            """
            
            resultado = r(r_code)
            
            return {
                'forecast': list(resultado.rx2('forecast')),
                'lower': list(resultado.rx2('lower')),
                'upper': list(resultado.rx2('upper'))
            }
        except Exception as e:
            st.warning(f"⚠️ Erro no Auto ARIMA R: {str(e)}")
            return None

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

@st.cache_data
def load_crime_data():
    """Carrega dados de criminalidade"""
    try:
        df = pd.read_csv(PROCESSED_DIR / 'crimes_consolidado.csv')
        df['data'] = pd.to_datetime(df['data'])
        return df
    except:
        return generate_sample_data()

def generate_sample_data():
    """Gera dados de exemplo"""
    np.random.seed(42)
    datas = pd.date_range(start='2020-01-01', end='2024-12-31', freq='MS')
    
    # Simula diferentes tipos de crime
    crimes = ['Homicídio Doloso', 'Roubo de Veículo', 'Roubo a Transeunte', 'Furto de Veículo']
    regioes = ['Centro', 'Zona Sul', 'Zona Norte', 'Barra da Tijuca']
    
    dados = []
    for crime in crimes:
        for regiao in regioes:
            for data in datas:
                # Tendência + sazonalidade + ruído
                tendencia = 50 + np.random.normal(0, 10)
                sazonalidade = 10 * np.sin(data.month * 2 * np.pi / 12)
                ruido = np.random.normal(0, 5)
                
                valor = max(0, tendencia + sazonalidade + ruido)
                
                dados.append({
                    'data': data,
                    'tipo_crime': crime,
                    'regiao_administrativa': regiao,
                    'total_ocorrencias': int(valor),
                    'populacao': np.random.randint(100000, 500000),
                    'taxa_100k': valor / 1000 * 100
                })
    
    return pd.DataFrame(dados)

@st.cache_data
def load_geodata():
    """Carrega dados geoespaciais"""
    try:
        return gpd.read_file(PROCESSED_DIR / 'crimes_geo.geojson')
    except:
        return None

# ============================================================================
# STREAMLIT APP: INTERFACE OTIMIZADA
# ============================================================================

def main():
    st.set_page_config(
        page_title="Análise Preditiva de Violência - Rio de Janeiro",
        page_icon="🔮",
        layout="wide"
    )
    
    st.title("🔮 Análise Preditiva de Violência no Rio de Janeiro")
    st.markdown("""
    **Arquitetura Híbrida Otimizada:**
    - ⚡ Predições rápidas em Python (tempo real)
    - 🔬 Análises espaciais pesadas em R (cacheadas)
    - 🚀 Melhor performance e UX
    """)
    
    # ==================== SIDEBAR ====================
    
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Dados
        st.subheader("📊 Dados")
        use_sample = st.checkbox("Usar dados de exemplo", value=True)
        
        if not use_sample:
            uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
            else:
                df = load_crime_data()
        else:
            df = load_crime_data()
        
        st.markdown("---")
        
        # Filtros
        st.subheader("🔍 Filtros")
        
        crime_tipo = st.selectbox(
            "Tipo de Crime",
            df['tipo_crime'].unique().tolist()
        )
        
        regiao = st.selectbox(
            "Região",
            ["Consolidado"] + df['regiao_administrativa'].unique().tolist()
        )
        
        horizonte = st.slider(
            "Horizonte (meses)",
            1, 12, 6
        )
        
        st.markdown("---")
        
        # Modelos a usar
        st.subheader("🎯 Modelos Preditivos")
        
        modelos_selecionados = st.multiselect(
            "Selecione modelos",
            ["ARIMA Python", "Prophet", "Random Forest", "Auto ARIMA R (leve)"],
            default=["ARIMA Python", "Prophet"]
        )
        
        st.markdown("---")
        
        # Análises espaciais (cache)
        st.subheader("🗺️ Análises Espaciais (R)")
        
        executar_moran = st.checkbox("Moran's I (cacheado)", value=False)
        executar_kde = st.checkbox("Kernel Density (cacheado)", value=False)
        
        if st.button("🗑️ Limpar Cache R"):
            import shutil
            if CACHE_DIR.exists():
                shutil.rmtree(CACHE_DIR)
                CACHE_DIR.mkdir()
            st.success("Cache limpo!")
            st.rerun()
    
    # ==================== FILTROS DE DADOS ====================
    
    # Aplica filtros
    df_filtered = df.copy()
    
    if crime_tipo != "Todos":
        df_filtered = df_filtered[df_filtered['tipo_crime'] == crime_tipo]
    
    if regiao != "Consolidado":
        df_filtered = df_filtered[df_filtered['regiao_administrativa'] == regiao]
    
    # Agrega por data se necessário
    if regiao == "Consolidado":
        df_agg = df_filtered.groupby('data').agg({
            'total_ocorrencias': 'sum',
            'populacao': 'sum',
            'taxa_100k': 'mean'
        }).reset_index()
    else:
        df_agg = df_filtered.groupby('data').agg({
            'total_ocorrencias': 'sum',
            'populacao': 'first',
            'taxa_100k': 'mean'
        }).reset_index()
    
    # ==================== ANÁLISES ESPACIAIS (SE SOLICITADO) ====================
    
    if executar_moran or executar_kde:
        st.markdown("## 🗺️ Análises Espaciais (R - Cacheadas)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if executar_moran:
                with st.spinner("Calculando Moran's I..."):
                    # Simula caminho do geodata
                    geodata_path = str(PROCESSED_DIR / 'crimes_geo.geojson')
                    
                    # Esta análise roda 1x e depois usa cache
                    resultado_moran = RHeavyAnalysis.moran_analysis(
                        geodata_path,
                        'taxa_100k',
                        k_neighbors=5
                    )
                    
                    if resultado_moran:
                        st.metric("Moran's I", f"{resultado_moran.get('moran_i', 0):.4f}")
                        st.metric("P-valor", f"{resultado_moran.get('p_value', 0):.4f}")
                        
                        # Mostra padrões LISA
                        if 'lisa_patterns' in resultado_moran:
                            st.markdown("**Padrões LISA:**")
                            for pattern, count in resultado_moran['lisa_patterns'].items():
                                st.write(f"- {pattern}: {count}")
        
        with col2:
            if executar_kde:
                with st.spinner("Calculando KDE..."):
                    # Esta análise roda 1x e depois usa cache
                    resultado_kde = RHeavyAnalysis.kernel_density(
                        str(PROCESSED_DIR / 'crimes_points.geojson')
                    )
                    
                    if resultado_kde:
                        st.success("✅ Kernel Density calculado")
                        st.metric("Bandwidth", f"{resultado_kde.get('bandwidth', 0):.2f}")
                        st.metric("Hotspots 95%", resultado_kde.get('hotspots_count', {}).get('hotspots_95', 0))
        
        st.markdown("---")
    
    # ==================== PREDIÇÕES (TEMPO REAL) ====================
    
    st.markdown("## 📈 Predições de Séries Temporais")
    
    if len(df_agg) < 12:
        st.warning("⚠️ Poucos dados para predição. Use pelo menos 12 meses.")
        return
    
    serie = df_agg['total_ocorrencias'].values
    datas = df_agg['data']
    
    # Mostra estatísticas dos dados
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Registros", len(df_agg))
    with col2:
        st.metric("Período", f"{datas.min().strftime('%Y-%m')} a {datas.max().strftime('%Y-%m')}")
    with col3:
        st.metric("Média Mensal", f"{serie.mean():.0f}")
    with col4:
        st.metric("Último Valor", f"{serie[-1]:.0f}")
    
    if st.button("🚀 Executar Predições", type="primary"):
        
        resultados = {}
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # ARIMA Python
        if "ARIMA Python" in modelos_selecionados:
            status_text.text("Executando ARIMA...")
            progress_bar.progress(25)
            resultado = FastPythonPredictors.arima_forecast(serie, horizonte)
            if resultado:
                resultados['arima'] = resultado
        
        # Prophet
        if "Prophet" in modelos_selecionados:
            status_text.text("Executando Prophet...")
            progress_bar.progress(50)
            df_temp = pd.DataFrame({'data': datas, 'valor': serie})
            resultado = FastPythonPredictors.prophet_forecast(df_temp, horizonte)
            if resultado:
                resultados['prophet'] = resultado
        
        # Random Forest
        if "Random Forest" in modelos_selecionados:
            status_text.text("Executando Random Forest...")
            progress_bar.progress(75)
            df_temp = pd.DataFrame({'data': datas, 'valor': serie})
            resultado = FastPythonPredictors.random_forest_forecast(df_temp, 'valor', horizonte)
            if resultado:
                resultados['random_forest'] = resultado
        
        # Auto ARIMA R (leve)
        if "Auto ARIMA R (leve)" in modelos_selecionados:
            status_text.text("Executando Auto ARIMA R...")
            progress_bar.progress(90)
            r_pred = LightRPredictors()
            resultado = r_pred.auto_arima_light(serie, horizonte)
            if resultado:
                resultados['auto_arima_r'] = resultado
        
        progress_bar.progress(100)
        status_text.text("✅ Predições concluídas!")
        
        # ==================== VISUALIZAÇÃO ====================
        
        if resultados:
            st.success("✅ Predições concluídas!")
            
            # Cria datas futuras
            ultima_data = datas.iloc[-1]
            datas_futuro = pd.date_range(
                start=ultima_data + timedelta(days=30),
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
            
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            # Predições
            for i, (nome, resultado) in enumerate(resultados.items()):
                if resultado and 'forecast' in resultado:
                    fig.add_trace(go.Scatter(
                        x=datas_futuro,
                        y=resultado['forecast'],
                        mode='lines+markers',
                        name=nome.upper(),
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
                title=f"Previsão: {crime_tipo} - {regiao}",
                xaxis_title="Data",
                yaxis_title="Ocorrências",
                height=500,
                hovermode='x unified',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de previsões
            st.markdown("### 📋 Valores Previstos")
            
            df_prev = pd.DataFrame({
                'Data': datas_futuro.strftime('%Y-%m')
            })
            
            for nome, resultado in resultados.items():
                if resultado and 'forecast' in resultado:
                    df_prev[nome.upper()] = np.array(resultado['forecast']).round(0).astype(int)
            
            st.dataframe(df_prev, use_container_width=True)
            
            # Download
            csv = df_prev.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                f"previsoes_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
            
            # Métricas
            st.markdown("### 📊 Métricas")
            
            cols = st.columns(len(resultados))
            for i, (nome, resultado) in enumerate(resultados.items()):
                if resultado:
                    with cols[i]:
                        if 'aic' in resultado:
                            st.metric(nome.upper(), f"AIC: {resultado['aic']:.2f}")
                        else:
                            media = np.mean(resultado['forecast'])
                            st.metric(nome.upper(), f"Média: {media:.0f}")
        else:
            st.warning("⚠️ Nenhuma predição foi gerada. Verifique os dados e modelos selecionados.")
    
    # ==================== MAPA INTERATIVO ====================
    
    st.markdown("## 🗺️ Mapa Interativo")
    
    gdf = load_geodata()
    if gdf is not None:
        # Cria mapa
        m = folium.Map(
            location=[-22.9, -43.2],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Adiciona camadas
        folium.Choropleth(
            geo_data=gdf,
            data=gdf,
            columns=['nome_ra', 'taxa_100k'],
            key_on='feature.properties.nome_ra',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Taxa por 100k Habitantes'
        ).add_to(m)
        
        # Adiciona popups
        for idx, row in gdf.iterrows():
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=f"""
                <b>{row['nome_ra']}</b><br>
                Taxa: {row['taxa_100k']:.2f}<br>
                Total: {row['total_ocorrencias']:.0f}
                """,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        st_folium(m, width=700, height=500)
    else:
        st.info("ℹ️ Dados geoespaciais não disponíveis. Execute a coleta de dados primeiro.")

if __name__ == "__main__":
    main()
