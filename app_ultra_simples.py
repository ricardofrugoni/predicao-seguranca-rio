"""
🔒 APP ULTRA-SIMPLES - SEGURANÇA PÚBLICA RJ
==========================================

Versão ultra-simplificada para garantir deploy no Streamlit Cloud
- Apenas dependências básicas
- Dados simulados
- Interface mínima
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração
st.set_page_config(
    page_title="🔒 Segurança Pública RJ",
    page_icon="🔒",
    layout="wide"
)

def main():
    st.title("🔒 Análise de Segurança Pública - Rio de Janeiro")
    st.markdown("### Dashboard de Violência por Regiões")
    
    # Dados simulados
    np.random.seed(42)
    regioes = ['Centro', 'Zona Sul', 'Zona Norte', 'Zona Oeste', 'Baixada Fluminense', 'Grande Niterói']
    tipos_crime = ['Homicídio Doloso', 'Roubo a Transeunte', 'Furto a Transeunte', 'Violência Doméstica']
    
    dados = []
    for regiao in regioes:
        for crime in tipos_crime:
            base = np.random.poisson(50)
            if regiao == 'Zona Sul':
                base = int(base * 0.6)
            elif regiao == 'Baixada Fluminense':
                base = int(base * 1.8)
            
            dados.append({
                'regiao': regiao,
                'tipo_crime': crime,
                'ocorrencias': max(0, base)
            })
    
    df = pd.DataFrame(dados)
    
    # Resumo
    st.header("📋 Resumo Executivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Ocorrências", f"{df['ocorrencias'].sum():,}")
    
    with col2:
        st.metric("Regiões Analisadas", len(regioes))
    
    with col3:
        st.metric("Tipos de Crimes", len(tipos_crime))
    
    # Gráfico
    st.header("📊 Taxa de Violência por Região")
    
    crimes_por_regiao = df.groupby('regiao')['ocorrencias'].sum().reset_index()
    
    fig = px.bar(
        crimes_por_regiao,
        x='regiao',
        y='ocorrencias',
        title='Ocorrências por Região',
        color='ocorrencias',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.header("📋 Dados Detalhados")
    
    pivot_table = df.pivot(index='regiao', columns='tipo_crime', values='ocorrencias').fillna(0)
    st.dataframe(pivot_table, use_container_width=True)
    
    # Download
    st.header("📥 Download")
    
    csv = df.to_csv(index=False)
    st.download_button(
        "📊 Download Dados",
        csv,
        f"dados_seguranca_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**🔒 Sistema de Análise de Segurança Pública - Rio de Janeiro**")

if __name__ == "__main__":
    main()


