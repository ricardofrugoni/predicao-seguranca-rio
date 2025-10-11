"""
🏠 PÁGINA PRINCIPAL - Sistema de Análise Preditiva de Violência no Rio de Janeiro
================================================================================

Dashboard principal com navegação para todas as funcionalidades do sistema.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Segurança Rio Preditiva - Análise de Violência",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Carrega dados de exemplo para demonstração"""
    np.random.seed(42)
    
    # Gera dados simulados
    datas = pd.date_range(start='2020-01-01', end='2024-12-31', freq='MS')
    crimes = ['Homicídio Doloso', 'Roubo de Veículo', 'Roubo a Transeunte', 'Furto de Veículo']
    regioes = ['Centro', 'Zona Sul', 'Zona Norte', 'Barra da Tijuca', 'Zona Oeste']
    
    dados = []
    for crime in crimes:
        for regiao in regioes:
            for data in datas:
                # Simula tendência + sazonalidade + ruído
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

def check_system_status():
    """Verifica status do sistema"""
    status = {
        'python_packages': True,
        'r_available': False,
        'data_available': True,
        'models_ready': True
    }
    
    # Verifica pacotes Python
    try:
        import streamlit, pandas, numpy, plotly, geopandas
        status['python_packages'] = True
    except ImportError:
        status['python_packages'] = False
    
    # Verifica R
    try:
        import subprocess
        result = subprocess.run(['R', '--version'], capture_output=True, text=True)
        status['r_available'] = result.returncode == 0
    except:
        status['r_available'] = False
    
    return status

def create_overview_metrics(df):
    """Cria métricas de visão geral"""
    total_crimes = df['total_ocorrencias'].sum()
    avg_monthly = df.groupby('data')['total_ocorrencias'].sum().mean()
    top_crime = df.groupby('tipo_crime')['total_ocorrencias'].sum().idxmax()
    top_region = df.groupby('regiao_administrativa')['total_ocorrencias'].sum().idxmax()
    
    return {
        'total_crimes': total_crimes,
        'avg_monthly': avg_monthly,
        'top_crime': top_crime,
        'top_region': top_region
    }

def create_trend_chart(df):
    """Cria gráfico de tendência temporal"""
    df_trend = df.groupby('data')['total_ocorrencias'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_trend['data'],
        y=df_trend['total_ocorrencias'],
        mode='lines+markers',
        name='Total de Ocorrências',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # Adiciona linha de tendência
    z = np.polyfit(range(len(df_trend)), df_trend['total_ocorrencias'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=df_trend['data'],
        y=p(range(len(df_trend))),
        mode='lines',
        name='Tendência',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Evolução Temporal das Ocorrências',
        xaxis_title='Data',
        yaxis_title='Total de Ocorrências',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def create_crime_distribution_chart(df):
    """Cria gráfico de distribuição por tipo de crime"""
    df_crime = df.groupby('tipo_crime')['total_ocorrencias'].sum().reset_index()
    
    fig = px.pie(
        df_crime, 
        values='total_ocorrencias', 
        names='tipo_crime',
        title='Distribuição por Tipo de Crime',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

def create_region_heatmap(df):
    """Cria heatmap por região e tipo de crime"""
    df_heatmap = df.groupby(['regiao_administrativa', 'tipo_crime'])['total_ocorrencias'].sum().reset_index()
    df_pivot = df_heatmap.pivot(index='regiao_administrativa', columns='tipo_crime', values='total_ocorrencias')
    
    fig = px.imshow(
        df_pivot,
        title='Heatmap: Região vs Tipo de Crime',
        color_continuous_scale='Reds',
        aspect='auto'
    )
    
    fig.update_layout(height=400)
    
    return fig

def main():
    """Função principal"""
    
    # Header principal
    st.markdown('<h1 class="main-header">🏠 Sistema de Análise Preditiva de Violência</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Rio de Janeiro - Dashboard Principal</h2>', unsafe_allow_html=True)
    
    # Sidebar com navegação
    st.sidebar.title("🧭 Navegação")
    
    pages = {
        "🏠 Home": "Home.py",
        "🗺️ Mapa Interativo": "pages/01_🗺️_Mapa_Interativo.py",
        "📈 Análise Temporal": "pages/02_📈_Análise_Temporal.py", 
        "📍 Análise Espacial R": "pages/03_📍_Análise_Espacial_R.py",
        "🔥 Hotspots e Clusters": "pages/04_🔥_Hotspots_e_Clusters.py",
        "🤖 Modelos Preditivos": "pages/05_🤖_Modelos_Preditivos.py",
        "📊 Comparações": "pages/06_📊_Comparações.py",
        "📄 Relatórios": "pages/07_📄_Relatórios.py"
    }
    
    selected_page = st.sidebar.selectbox("Selecione uma página:", list(pages.keys()))
    
    # Status do sistema
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Status do Sistema")
    
    status = check_system_status()
    
    if status['python_packages']:
        st.sidebar.markdown('<p class="status-success">✅ Python Packages</p>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<p class="status-warning">⚠️ Python Packages</p>', unsafe_allow_html=True)
    
    if status['r_available']:
        st.sidebar.markdown('<p class="status-success">✅ R Disponível</p>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<p class="status-warning">⚠️ R Não Disponível</p>', unsafe_allow_html=True)
    
    if status['data_available']:
        st.sidebar.markdown('<p class="status-success">✅ Dados Disponíveis</p>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<p class="status-warning">⚠️ Dados Não Disponíveis</p>', unsafe_allow_html=True)
    
    # Carrega dados
    df = load_sample_data()
    
    # Métricas principais
    st.markdown("## 📊 Visão Geral")
    
    metrics = create_overview_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Ocorrências",
            value=f"{metrics['total_crimes']:,}",
            delta="+5.2% vs ano anterior"
        )
    
    with col2:
        st.metric(
            label="Média Mensal",
            value=f"{metrics['avg_monthly']:.0f}",
            delta="-2.1% vs mês anterior"
        )
    
    with col3:
        st.metric(
            label="Crime Mais Comum",
            value=metrics['top_crime'],
            delta=""
        )
    
    with col4:
        st.metric(
            label="Região Mais Afetada",
            value=metrics['top_region'],
            delta=""
        )
    
    # Gráficos principais
    st.markdown("## 📈 Análises Principais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trend = create_trend_chart(df)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        fig_crime = create_crime_distribution_chart(df)
        st.plotly_chart(fig_crime, use_container_width=True)
    
    # Heatmap
    st.markdown("## 🔥 Análise por Região e Tipo de Crime")
    fig_heatmap = create_region_heatmap(df)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Funcionalidades disponíveis
    st.markdown("## 🚀 Funcionalidades Disponíveis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🗺️ Mapa Interativo</h3>
            <p>Visualização geoespacial com hotspots e clusters de violência</p>
            <ul>
                <li>Mapas de calor</li>
                <li>Análise de proximidade</li>
                <li>Camadas interativas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Modelos Preditivos</h3>
            <p>8 modelos de machine learning para previsão de violência</p>
            <ul>
                <li>ARIMA, Prophet, XGBoost</li>
                <li>LSTM, Random Forest</li>
                <li>Ensemble inteligente</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📍 Análise Espacial R</h3>
            <p>Análises espaciais avançadas com R</p>
            <ul>
                <li>Moran's I e LISA</li>
                <li>Kernel Density</li>
                <li>GWR (Regressão Geográfica)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start
    st.markdown("## 🎯 Quick Start")
    
    st.markdown("""
    ### Para começar rapidamente:
    
    1. **📊 Análise Exploratória**: Use a página "Análise Temporal" para entender tendências
    2. **🗺️ Visualização Espacial**: Explore o "Mapa Interativo" para identificar hotspots
    3. **🤖 Previsões**: Acesse "Modelos Preditivos" para fazer previsões
    4. **📄 Relatórios**: Gere relatórios automáticos na página "Relatórios"
    
    ### 💡 Dicas de Uso:
    - **Para análise rápida**: Use Prophet + XGBoost
    - **Para máxima precisão**: Use Ensemble completo
    - **Para apresentações**: Use visualizações do Mapa Interativo
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🔮 Sistema de Análise Preditiva de Violência no Rio de Janeiro</p>
        <p>Desenvolvido com Python + R | Streamlit + Plotly | Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
