"""
🗺️ ANÁLISE GEOESPACIAL - SEGURANÇA PÚBLICA RJ
==============================================

Análise geoespacial com graduação de cores por níveis de violência
Mapas interativos por regiões do Rio de Janeiro
"""

import pandas as pd
import numpy as np
import folium
from folium import plugins
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class GeospatialAnalyzer:
    """Analisador geoespacial de segurança pública"""
    
    def __init__(self):
        # Coordenadas aproximadas das regiões do RJ
        self.regioes_coords = {
            'Centro': [-22.9068, -43.1729],
            'Zona Sul': [-22.9711, -43.1822],
            'Zona Norte': [-22.8944, -43.2400],
            'Zona Oeste': [-22.8847, -43.3300],
            'Baixada Fluminense': [-22.7667, -43.4000],
            'Grande Niterói': [-22.8833, -43.1000]
        }
        
        # Cores para níveis de violência
        self.cores_violencia = {
            'Muito Baixo': '#2E8B57',    # Verde escuro
            'Baixo': '#32CD32',         # Verde claro
            'Médio': '#FFD700',         # Amarelo
            'Alto': '#FF8C00',          # Laranja
            'Muito Alto': '#DC143C'     # Vermelho
        }
    
    def criar_mapa_calor_violencia(self, indices_violencia: pd.DataFrame) -> folium.Map:
        """
        Cria mapa de calor com graduação de cores por violência
        """
        print("🗺️ Criando mapa de calor de violência...")
        
        # Centro do Rio de Janeiro
        centro_rio = [-22.9068, -43.1729]
        
        # Cria mapa base
        mapa = folium.Map(
            location=centro_rio,
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Adiciona marcadores para cada região
        for _, row in indices_violencia.iterrows():
            regiao = row['regiao']
            coords = self.regioes_coords.get(regiao, centro_rio)
            nivel = row['nivel_violencia']
            taxa = row['taxa_violencia_100k']
            cor = row['cor']
            
            # Tamanho do marcador baseado na taxa de violência
            raio = max(10, min(50, taxa / 10))
            
            folium.CircleMarker(
                location=coords,
                radius=raio,
                popup=f"""
                <b>{regiao}</b><br>
                Taxa de Violência: {taxa:.1f}/100k hab<br>
                Nível: {nivel}<br>
                Ocorrências: {row['ocorrencias']}<br>
                População: {row['populacao']:,}
                """,
                color='black',
                weight=2,
                fillColor=cor,
                fillOpacity=0.7
            ).add_to(mapa)
        
        # Adiciona legenda
        self._adicionar_legenda_mapa(mapa)
        
        print("✅ Mapa de calor criado")
        return mapa
    
    def _adicionar_legenda_mapa(self, mapa: folium.Map):
        """Adiciona legenda ao mapa"""
        legenda_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Níveis de Violência</b></p>
        <p><i class="fa fa-circle" style="color:#2E8B57"></i> Muito Baixo</p>
        <p><i class="fa fa-circle" style="color:#32CD32"></i> Baixo</p>
        <p><i class="fa fa-circle" style="color:#FFD700"></i> Médio</p>
        <p><i class="fa fa-circle" style="color:#FF8C00"></i> Alto</p>
        <p><i class="fa fa-circle" style="color:#DC143C"></i> Muito Alto</p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    def criar_mapa_clusters(self, dados_crimes: pd.DataFrame) -> folium.Map:
        """
        Cria mapa com clusters de crimes
        """
        print("🗺️ Criando mapa de clusters...")
        
        centro_rio = [-22.9068, -43.1729]
        mapa = folium.Map(location=centro_rio, zoom_start=10)
        
        # Adiciona marcadores de crimes
        for _, row in dados_crimes.iterrows():
            regiao = row['regiao']
            coords = self.regioes_coords.get(regiao, centro_rio)
            
            # Adiciona pequena variação para evitar sobreposição
            lat = coords[0] + np.random.normal(0, 0.01)
            lon = coords[1] + np.random.normal(0, 0.01)
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                popup=f"""
                <b>{row['tipo_crime']}</b><br>
                Região: {regiao}<br>
                Ocorrências: {row['ocorrencias']}<br>
                Fonte: {row['fonte']}
                """,
                color='red',
                fillColor='red',
                fillOpacity=0.6
            ).add_to(mapa)
        
        # Adiciona plugin de clusters
        marker_cluster = plugins.MarkerCluster().add_to(mapa)
        
        print("✅ Mapa de clusters criado")
        return mapa
    
    def criar_grafico_barras_regioes(self, indices_violencia: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de barras por região
        """
        print("📊 Criando gráfico de barras por região...")
        
        fig = go.Figure()
        
        # Adiciona barras para cada região
        for _, row in indices_violencia.iterrows():
            fig.add_trace(go.Bar(
                x=[row['regiao']],
                y=[row['taxa_violencia_100k']],
                name=row['regiao'],
                marker_color=row['cor'],
                text=f"{row['taxa_violencia_100k']:.1f}",
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Taxa de Violência por Região (por 100k habitantes)',
            xaxis_title='Região',
            yaxis_title='Taxa de Violência (/100k hab)',
            showlegend=False,
            height=500
        )
        
        print("✅ Gráfico de barras criado")
        return fig
    
    def criar_grafico_pizza_crimes(self, analise_crimes: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de pizza dos principais crimes
        """
        print("🥧 Criando gráfico de pizza dos crimes...")
        
        # Top 10 crimes
        top_crimes = analise_crimes.head(10)
        
        fig = go.Figure(data=[go.Pie(
            labels=top_crimes['tipo_crime'],
            values=top_crimes['total_ocorrencias'],
            hole=0.3,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Distribuição dos Principais Crimes (Últimos 12 meses)',
            height=600
        )
        
        print("✅ Gráfico de pizza criado")
        return fig
    
    def criar_heatmap_temporal(self, dados_crimes: pd.DataFrame) -> go.Figure:
        """
        Cria heatmap temporal de crimes
        """
        print("🔥 Criando heatmap temporal...")
        
        # Prepara dados para heatmap
        dados_crimes['data'] = pd.to_datetime(dados_crimes['data'])
        dados_crimes['mes'] = dados_crimes['data'].dt.month
        dados_crimes['ano'] = dados_crimes['data'].dt.year
        
        # Agrupa por mês e tipo de crime
        heatmap_data = dados_crimes.groupby(['mes', 'tipo_crime'])['ocorrencias'].sum().unstack(fill_value=0)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Reds',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Heatmap Temporal de Crimes por Mês',
            xaxis_title='Tipo de Crime',
            yaxis_title='Mês',
            height=600
        )
        
        print("✅ Heatmap temporal criado")
        return fig
    
    def criar_dashboard_geospatial(self, indices_violencia: pd.DataFrame, 
                                 dados_crimes: pd.DataFrame, 
                                 analise_crimes: pd.DataFrame) -> Dict:
        """
        Cria dashboard completo geoespacial
        """
        print("📊 Criando dashboard geoespacial completo...")
        
        dashboard = {}
        
        # 1. Mapas
        dashboard['mapa_calor'] = self.criar_mapa_calor_violencia(indices_violencia)
        dashboard['mapa_clusters'] = self.criar_mapa_clusters(dados_crimes)
        
        # 2. Gráficos
        dashboard['grafico_barras'] = self.criar_grafico_barras_regioes(indices_violencia)
        dashboard['grafico_pizza'] = self.criar_grafico_pizza_crimes(analise_crimes)
        dashboard['heatmap_temporal'] = self.criar_heatmap_temporal(dados_crimes)
        
        # 3. Estatísticas resumidas
        dashboard['estatisticas'] = {
            'total_regioes': len(indices_violencia),
            'total_crimes': dados_crimes['ocorrencias'].sum(),
            'regiao_mais_violenta': indices_violencia.loc[indices_violencia['taxa_violencia_100k'].idxmax(), 'regiao'],
            'regiao_menos_violenta': indices_violencia.loc[indices_violencia['taxa_violencia_100k'].idxmin(), 'regiao'],
            'crime_mais_comum': analise_crimes.iloc[0]['tipo_crime'],
            'media_violencia': indices_violencia['taxa_violencia_100k'].mean()
        }
        
        print("✅ Dashboard geoespacial criado")
        return dashboard
    
    def salvar_mapa_html(self, mapa: folium.Map, nome_arquivo: str):
        """Salva mapa como HTML"""
        mapa.save(f"projeto_violencia_rj/outputs/{nome_arquivo}")
        print(f"✅ Mapa salvo como {nome_arquivo}")

def main():
    """Função principal para teste"""
    from src.data_collection.security_apis import SecurityDataCollector
    
    # Coleta dados
    collector = SecurityDataCollector()
    dados = collector.consolidar_dados_seguranca(periodo_meses=12)
    indices = collector.calcular_indices_violencia(dados)
    analise = collector.analise_principais_crimes_12m(dados)
    
    # Análise geoespacial
    analyzer = GeospatialAnalyzer()
    dashboard = analyzer.criar_dashboard_geospatial(indices, dados['todos_crimes'], analise)
    
    print("\n📊 DASHBOARD GEOESPACIAL CRIADO:")
    print(f"Total de regiões: {dashboard['estatisticas']['total_regioes']}")
    print(f"Total de crimes: {dashboard['estatisticas']['total_crimes']:,}")
    print(f"Região mais violenta: {dashboard['estatisticas']['regiao_mais_violenta']}")
    print(f"Região menos violenta: {dashboard['estatisticas']['regiao_menos_violenta']}")
    print(f"Crime mais comum: {dashboard['estatisticas']['crime_mais_comum']}")

if __name__ == "__main__":
    main()
