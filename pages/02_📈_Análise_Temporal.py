"""
📈 ANÁLISE TEMPORAL - Tendências e Sazonalidade
==============================================

Página para análise temporal detalhada com decomposição, tendências e sazonalidade.
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

def load_sample_data():
    """Carrega dados de exemplo"""
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

def decompose_time_series(serie):
    """Decompõe série temporal"""
    try:
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        # Converte para série temporal
        ts = pd.Series(serie, index=pd.date_range(start='2020-01-01', periods=len(serie), freq='MS'))
        
        # Decomposição
        decomposition = seasonal_decompose(ts, model='additive', period=12)
        
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'observed': decomposition.observed
        }
    except Exception as e:
        st.warning(f"⚠️ Erro na decomposição: {str(e)}")
        return None

def create_decomposition_chart(decomposition):
    """Cria gráfico de decomposição"""
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=('Série Original', 'Tendência', 'Sazonalidade', 'Resíduos'),
        vertical_spacing=0.05
    )
    
    # Série original
    fig.add_trace(
        go.Scatter(x=decomposition['observed'].index, y=decomposition['observed'], 
                  name='Original', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Tendência
    fig.add_trace(
        go.Scatter(x=decomposition['trend'].index, y=decomposition['trend'], 
                  name='Tendência', line=dict(color='red')),
        row=2, col=1
    )
    
    # Sazonalidade
    fig.add_trace(
        go.Scatter(x=decomposition['seasonal'].index, y=decomposition['seasonal'], 
                  name='Sazonalidade', line=dict(color='green')),
        row=3, col=1
    )
    
    # Resíduos
    fig.add_trace(
        go.Scatter(x=decomposition['residual'].index, y=decomposition['residual'], 
                  name='Resíduos', line=dict(color='orange')),
        row=4, col=1
    )
    
    fig.update_layout(height=800, showlegend=False, title_text="Decomposição da Série Temporal")
    fig.update_xaxes(title_text="Data", row=4, col=1)
    
    return fig

def create_seasonality_analysis(serie):
    """Análise de sazonalidade"""
    # Agrupa por mês
    df_mes = pd.DataFrame({
        'mes': pd.date_range(start='2020-01-01', periods=len(serie), freq='MS').month,
        'valor': serie
    })
    
    # Estatísticas por mês
    stats_mes = df_mes.groupby('mes')['valor'].agg(['mean', 'std', 'count']).reset_index()
    stats_mes['mes_nome'] = stats_mes['mes'].map({
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    })
    
    # Gráfico de sazonalidade
    fig = px.bar(
        stats_mes, x='mes_nome', y='mean',
        title='Sazonalidade por Mês',
        labels={'mean': 'Média de Ocorrências', 'mes_nome': 'Mês'},
        color='mean',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400)
    
    return fig, stats_mes

def create_trend_analysis(serie):
    """Análise de tendência"""
    # Calcula médias móveis
    window_3 = pd.Series(serie).rolling(window=3).mean()
    window_6 = pd.Series(serie).rolling(window=6).mean()
    window_12 = pd.Series(serie).rolling(window=12).mean()
    
    # Cria gráfico
    fig = go.Figure()
    
    datas = pd.date_range(start='2020-01-01', periods=len(serie), freq='MS')
    
    fig.add_trace(go.Scatter(
        x=datas, y=serie,
        name='Série Original',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=datas, y=window_3,
        name='Média Móvel 3 meses',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=datas, y=window_6,
        name='Média Móvel 6 meses',
        line=dict(color='green', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=datas, y=window_12,
        name='Média Móvel 12 meses',
        line=dict(color='orange', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Análise de Tendência com Médias Móveis',
        xaxis_title='Data',
        yaxis_title='Ocorrências',
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_correlation_analysis(df):
    """Análise de correlação temporal"""
    # Pivot para análise de correlação
    df_pivot = df.pivot_table(
        index='data', 
        columns='tipo_crime', 
        values='total_ocorrencias', 
        aggfunc='sum'
    ).fillna(0)
    
    # Matriz de correlação
    corr_matrix = df_pivot.corr()
    
    # Gráfico de correlação
    fig = px.imshow(
        corr_matrix,
        title='Correlação entre Tipos de Crime',
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    fig.update_layout(height=500)
    
    return fig, corr_matrix

def create_outlier_analysis(serie):
    """Análise de outliers"""
    # Calcula IQR
    Q1 = np.percentile(serie, 25)
    Q3 = np.percentile(serie, 75)
    IQR = Q3 - Q1
    
    # Identifica outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = serie[(serie < lower_bound) | (serie > upper_bound)]
    
    # Gráfico de box plot
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=serie,
        name='Distribuição',
        boxpoints='outliers',
        marker=dict(color='red', size=8)
    ))
    
    fig.update_layout(
        title='Análise de Outliers',
        yaxis_title='Ocorrências',
        height=400
    )
    
    return fig, outliers, lower_bound, upper_bound

def main():
    """Função principal"""
    st.title("📈 Análise Temporal - Tendências e Sazonalidade")
    st.markdown("Análise detalhada de tendências, sazonalidade e padrões temporais de violência")
    
    # Carrega dados
    df = load_sample_data()
    
    # Sidebar com controles
    st.sidebar.title("🎛️ Controles")
    
    # Filtros
    crime_tipo = st.sidebar.selectbox(
        "Tipo de Crime:",
        ["Todos"] + df['tipo_crime'].unique().tolist()
    )
    
    regiao = st.sidebar.selectbox(
        "Região:",
        ["Todas"] + df['regiao_administrativa'].unique().tolist()
    )
    
    # Aplica filtros
    df_filtered = df.copy()
    
    if crime_tipo != "Todos":
        df_filtered = df_filtered[df_filtered['tipo_crime'] == crime_tipo]
    
    if regiao != "Todas":
        df_filtered = df_filtered[df_filtered['regiao_administrativa'] == regiao]
    
    # Agrega por data
    df_agg = df_filtered.groupby('data')['total_ocorrencias'].sum().reset_index()
    serie = df_agg['total_ocorrencias'].values
    
    # Métricas básicas
    st.markdown("## 📊 Métricas Temporais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", len(df_agg))
    
    with col2:
        st.metric("Média Mensal", f"{serie.mean():.1f}")
    
    with col3:
        st.metric("Desvio Padrão", f"{serie.std():.1f}")
    
    with col4:
        st.metric("Coeficiente de Variação", f"{serie.std()/serie.mean()*100:.1f}%")
    
    # Análise de decomposição
    st.markdown("## 🔍 Decomposição da Série Temporal")
    
    if st.button("🔬 Executar Decomposição"):
        decomposition = decompose_time_series(serie)
        
        if decomposition:
            fig_decomp = create_decomposition_chart(decomposition)
            st.plotly_chart(fig_decomp, use_container_width=True)
            
            # Estatísticas da decomposição
            st.markdown("### 📈 Estatísticas da Decomposição")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Variância da Tendência", f"{decomposition['trend'].var():.2f}")
            
            with col2:
                st.metric("Variância da Sazonalidade", f"{decomposition['seasonal'].var():.2f}")
            
            with col3:
                st.metric("Variância dos Resíduos", f"{decomposition['residual'].var():.2f}")
    
    # Análise de sazonalidade
    st.markdown("## 🌊 Análise de Sazonalidade")
    
    fig_season, stats_mes = create_seasonality_analysis(serie)
    st.plotly_chart(fig_season, use_container_width=True)
    
    # Tabela de sazonalidade
    st.markdown("### 📋 Estatísticas por Mês")
    st.dataframe(stats_mes, use_container_width=True)
    
    # Análise de tendência
    st.markdown("## 📈 Análise de Tendência")
    
    fig_trend = create_trend_analysis(serie)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Análise de correlação
    st.markdown("## 🔗 Análise de Correlação")
    
    fig_corr, corr_matrix = create_correlation_analysis(df_filtered)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Tabela de correlação
    st.markdown("### 📋 Matriz de Correlação")
    st.dataframe(corr_matrix, use_container_width=True)
    
    # Análise de outliers
    st.markdown("## 🎯 Análise de Outliers")
    
    fig_outlier, outliers, lower_bound, upper_bound = create_outlier_analysis(serie)
    st.plotly_chart(fig_outlier, use_container_width=True)
    
    # Estatísticas de outliers
    st.markdown("### 📊 Estatísticas de Outliers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Número de Outliers", len(outliers))
    
    with col2:
        st.metric("Limite Inferior", f"{lower_bound:.1f}")
    
    with col3:
        st.metric("Limite Superior", f"{upper_bound:.1f}")
    
    # Gráfico temporal completo
    st.markdown("## 📊 Série Temporal Completa")
    
    fig_complete = go.Figure()
    
    fig_complete.add_trace(go.Scatter(
        x=df_agg['data'],
        y=df_agg['total_ocorrencias'],
        mode='lines+markers',
        name='Ocorrências',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))
    
    # Adiciona linha de tendência
    z = np.polyfit(range(len(serie)), serie, 1)
    p = np.poly1d(z)
    fig_complete.add_trace(go.Scatter(
        x=df_agg['data'],
        y=p(range(len(serie))),
        mode='lines',
        name='Tendência',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig_complete.update_layout(
        title='Série Temporal com Tendência',
        xaxis_title='Data',
        yaxis_title='Ocorrências',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_complete, use_container_width=True)
    
    # Download
    st.markdown("## 💾 Download")
    
    csv = df_agg.to_csv(index=False)
    st.download_button(
        "📥 Download Dados Temporais CSV",
        csv,
        f"analise_temporal_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

if __name__ == "__main__":
    main()
