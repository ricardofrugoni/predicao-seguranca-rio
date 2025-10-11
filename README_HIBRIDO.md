# 🔮 Arquitetura Híbrida Python + R - Análise de Violência no Rio de Janeiro

Este projeto implementa uma arquitetura híbrida otimizada que combina Python e R para análise de violência no município do Rio de Janeiro, oferecendo o melhor dos dois mundos: **performance** e **facilidade de uso**.

## 🏗️ Arquitetura Híbrida

### Componentes Principais

1. **🐍 Python (Interface e Predições Rápidas)**
   - **Streamlit**: Interface web interativa
   - **Plotly**: Visualizações dinâmicas
   - **Pandas/NumPy**: Manipulação de dados
   - **Scikit-learn**: Machine Learning
   - **Statsmodels**: Séries temporais

2. **📊 R (Análises Espaciais Pesadas)**
   - **spdep**: Análise de dependência espacial
   - **spatstat**: Estatística espacial
   - **sf**: Manipulação de dados geoespaciais
   - **forecast**: Séries temporais avançadas

3. **🔗 Integração**
   - **subprocess**: Execução de scripts R
   - **rpy2**: Integração Python-R (opcional)
   - **JSON**: Troca de dados
   - **Cache**: Resultados persistentes

## ⚡ Vantagens da Arquitetura

### Performance
- **Análises pesadas**: Executadas 1x, resultados em cache
- **Predições rápidas**: Tempo real (< 1s)
- **Interface responsiva**: Nunca trava

### Manutenção
- **Debug simples**: Python para interface, R para análises
- **Deploy fácil**: Streamlit Cloud compatível
- **Flexibilidade**: Use Python ou R conforme necessário

### UX
- **Interface intuitiva**: Streamlit nativo
- **Visualizações interativas**: Plotly + Folium
- **Cache inteligente**: Resultados persistem entre sessões

## 🚀 Instalação e Configuração

### 1. Instalação Básica

```bash
# Clone o repositório
git clone <repository-url>
cd projeto_violencia_rj

# Instala dependências Python
pip install -r requirements_hibrido.txt

# Instala dependências R
Rscript install_r_dependencies.R

# Configura ambiente híbrido
python setup_hibrido.py
```

### 2. Verificação do Ambiente

```bash
# Verifica Python
python -c "import streamlit, pandas, plotly; print('✅ Python OK')"

# Verifica R
R --version

# Verifica integração
python -c "import rpy2; print('✅ rpy2 OK')"
```

### 3. Execução do Dashboard

```bash
# Método 1: Script otimizado
python run_dashboard.py

# Método 2: Streamlit direto
streamlit run dashboard_hibrido.py

# Método 3: Com parâmetros
python run_dashboard.py --port 8502 --host 0.0.0.0
```

## 📊 Funcionalidades

### Análises Espaciais (R - Cacheadas)
- **Moran's I**: Autocorrelação espacial global
- **LISA**: Autocorrelação espacial local
- **Kernel Density**: Estimação de densidade
- **GWR**: Regressão geograficamente ponderada

### Predições (Python - Tempo Real)
- **ARIMA**: Modelos autorregressivos
- **Prophet**: Séries temporais com sazonalidade
- **Random Forest**: Machine Learning
- **Auto ARIMA**: Seleção automática de parâmetros

### Visualizações
- **Mapas interativos**: Folium + Streamlit
- **Gráficos dinâmicos**: Plotly
- **Dashboards**: Streamlit nativo
- **Relatórios**: Exportação automática

## 🔧 Configuração Avançada

### Cache Inteligente

```python
# Configuração do cache
CACHE_CONFIG = {
    "cache_dir": "data/r_cache",
    "ttl_hours": 24,
    "max_size_mb": 100,
    "compression": True
}
```

### Integração Python-R

```python
# Método 1: subprocess (recomendado)
result = subprocess.run(['Rscript', 'script.R'], capture_output=True)

# Método 2: rpy2 (opcional)
import rpy2.robjects as ro
result = ro.r('R_function()')
```

### Deploy em Produção

```dockerfile
# Dockerfile híbrido
FROM python:3.9-slim

# Instala R
RUN apt-get update && apt-get install -y r-base

# Instala dependências
COPY requirements_hibrido.txt .
RUN pip install -r requirements_hibrido.txt

# Executa dashboard
CMD ["streamlit", "run", "dashboard_hibrido.py"]
```

## 📈 Casos de Uso

### Análise de Violência
- **Hotspots**: Identificação de áreas críticas
- **Tendências**: Evolução temporal
- **Predições**: Previsão de ocorrências
- **Correlações**: Fatores socioeconômicos

### Políticas Públicas
- **Alocação de recursos**: Baseada em dados
- **Monitoramento**: Acompanhamento em tempo real
- **Avaliação**: Impacto de intervenções
- **Planejamento**: Estratégias preventivas

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
projeto_violencia_rj/
├── dashboard_hibrido.py          # Dashboard principal
├── run_dashboard.py              # Executor otimizado
├── setup_hibrido.py             # Configuração do ambiente
├── requirements_hibrido.txt     # Dependências Python
├── install_r_dependencies.R     # Dependências R
├── src/
│   └── r_scripts/               # Scripts R
│       ├── moran_analysis.R      # Análise de Moran
│       └── kernel_density.R      # KDE
├── data/
│   └── r_cache/                 # Cache de análises R
└── notebooks/
    └── 05_demo_hibrido.ipynb    # Demonstração
```

### Adicionando Novas Análises

1. **Crie script R** em `src/r_scripts/`
2. **Adicione classe Python** em `dashboard_hibrido.py`
3. **Implemente cache** para performance
4. **Teste integração** Python-R

### Debugging

```python
# Debug Python
import logging
logging.basicConfig(level=logging.DEBUG)

# Debug R
Rscript --verbose script.R

# Debug integração
python -c "import rpy2; print(rpy2.__version__)"
```

## 📚 Documentação Adicional

- **Notebooks**: `notebooks/05_demo_hibrido.ipynb`
- **Scripts R**: `src/r_scripts/`
- **Dashboard**: `dashboard_hibrido.py`
- **Configuração**: `setup_hibrido.py`

## 🤝 Contribuição

1. **Fork** o repositório
2. **Crie** branch para feature
3. **Implemente** funcionalidade
4. **Teste** integração Python-R
5. **Submeta** pull request

## 📄 Licença

Este projeto está sob licença MIT. Veja `LICENSE` para detalhes.

## 🆘 Suporte

- **Issues**: GitHub Issues
- **Documentação**: README files
- **Exemplos**: Notebooks de demonstração
- **Comunidade**: Discussões do GitHub

---

**🎉 Arquitetura Híbrida Otimizada para Análise de Violência no Rio de Janeiro!**

*Combine o poder do Python com a precisão do R para análises espaciais avançadas.*
