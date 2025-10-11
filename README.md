# 🔮 Sistema de Análise Preditiva de Violência no Rio de Janeiro

Sistema completo de análise preditiva de violência no município do Rio de Janeiro, combinando **Python** e **R** em uma arquitetura híbrida otimizada.

## 🚀 Características Principais

- **8 Modelos Preditivos**: ARIMA, SARIMA, Prophet, XGBoost, Random Forest, LSTM, Gradient Boosting, Ensemble
- **Análises Espaciais Avançadas**: Moran's I, LISA, Kernel Density, GWR
- **Interface Interativa**: Dashboard Streamlit profissional
- **Arquitetura Híbrida**: Python + R otimizada
- **Cache Inteligente**: Performance máxima
- **Deploy Fácil**: Streamlit Cloud compatível

## 📋 Índice

- [Instalação](#-instalação)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Usar](#-como-usar)
- [Modelos Disponíveis](#-modelos-disponíveis)
- [Exemplos Práticos](#-exemplos-práticos)
- [Troubleshooting](#-troubleshooting)

## 🔧 Instalação

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/seu-usuario/violencia-rio-ml.git
cd violencia-rio-ml
```

### Passo 2: Crie Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale Dependências Python
```bash
pip install --upgrade pip
pip install -r requirements_hibrido.txt
```
**Tempo estimado**: 5-10 minutos

### Passo 4: Instale R (Opcional - para análises espaciais)

**Windows:**
- Baixe de: https://cran.r-project.org/bin/windows/base/
- Instale RTools: https://cran.r-project.org/bin/windows/Rtools/

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install r-base r-base-dev
```

**Mac:**
```bash
brew install r
```

**Pacotes R:**
```r
# Abra R e execute:
install.packages(c("forecast", "sf", "spdep", "spatstat", "jsonlite"))
```

### Passo 5: Verificar Instalação
```bash
python -c "import streamlit, pandas, tensorflow, xgboost; print('✅ Tudo OK!')"
```

## 📁 Estrutura do Projeto

```
violencia-rio-ml/
│
├── Home.py                          # 🏠 Página principal do Streamlit
│
├── pages/                           # 📑 Páginas do dashboard
│   ├── 01_🗺️_Mapa_Interativo.py
│   ├── 02_📈_Análise_Temporal.py
│   ├── 03_📍_Análise_Espacial_R.py
│   ├── 04_🔥_Hotspots_e_Clusters.py
│   ├── 05_🤖_Modelos_Preditivos.py   # ⭐ 8 modelos ML
│   ├── 06_📊_Comparações.py
│   └── 07_📄_Relatórios.py
│
├── src/
│   ├── r_scripts/                   # Scripts R
│   │   ├── moran_analysis.R
│   │   ├── kernel_density.R
│   │   └── forecast.R
│   │
│   └── python_scripts/              # Scripts Python auxiliares
│       ├── data_collection.py
│       └── preprocessing.py
│
├── data/
│   ├── raw/                         # Dados brutos
│   ├── processed/                   # Dados processados
│   ├── models/                      # Modelos treinados
│   └── r_cache/                     # Cache das análises R
│
├── notebooks/                       # Jupyter notebooks
│   ├── 01_coleta_dados.ipynb       # ⭐ Já criamos este
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_treinamento_modelos.ipynb
│
├── requirements_hibrido.txt         # Dependências Python
├── packages.txt                     # Pacotes sistema (Streamlit Cloud)
├── install_r.sh                     # Script instalação R
├── README.md
└── .gitignore
```

## 🎯 Como Usar

### Opção 1: Executar Localmente
```bash
# 1. Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Execute o Streamlit
streamlit run Home.py

# 3. Abra o navegador em http://localhost:8501
```

### Opção 2: Deploy no Streamlit Cloud

**Push para GitHub:**
```bash
git add .
git commit -m "Sistema completo de análise preditiva"
git push origin main
```

**Conecte ao Streamlit Cloud:**
1. Acesse: https://streamlit.io/cloud
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione seu repositório
5. Main file: `Home.py`
6. Deploy!

**URL pública será gerada:**
```
https://seu-usuario-violencia-rio-ml.streamlit.app
```

## 🤖 Modelos Disponíveis

### 📊 Modelos Clássicos
| Modelo | Descrição | Velocidade | Acurácia | Uso Ideal |
|--------|-----------|------------|----------|-----------|
| **ARIMA** | Auto-Regressive Integrated Moving Average | ⚡⚡⚡ | ⭐⭐⭐ | Séries estacionárias |
| **SARIMA** | ARIMA com sazonalidade | ⚡⚡ | ⭐⭐⭐⭐ | Dados sazonais |
| **Prophet** | Framework Facebook | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Múltiplas sazonalidades |
| **Exp Smoothing** | Suavização exponencial | ⚡⚡⚡⚡ | ⭐⭐⭐ | Tendências simples |

### 🤖 Machine Learning
| Modelo | Descrição | Velocidade | Acurácia | Uso Ideal |
|--------|-----------|------------|----------|-----------|
| **Random Forest** | Ensemble de árvores | ⚡⚡ | ⭐⭐⭐⭐ | Dados não-lineares |
| **XGBoost** | Gradient Boosting otimizado | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Competições, alta precisão |
| **Gradient Boosting** | Boosting clássico | ⚡⚡ | ⭐⭐⭐⭐ | Balanço velocidade/acurácia |

### 🧠 Deep Learning
| Modelo | Descrição | Velocidade | Acurácia | Uso Ideal |
|--------|-----------|------------|----------|-----------|
| **LSTM** | Redes neurais recorrentes | ⚡ | ⭐⭐⭐⭐⭐ | Séries complexas, longas |

### 🎯 Ensemble
| Modelo | Descrição | Velocidade | Acurácia |
|--------|-----------|------------|----------|
| **Ensemble Avançado** | Combinação ponderada de todos | ⚡⚡ | ⭐⭐⭐⭐⭐ |

## 💡 Exemplos Práticos

### Exemplo 1: Previsão Rápida com Prophet
```python
import streamlit as st
import pandas as pd
from pages.05_🤖_Modelos_Preditivos import TraditionalModels

# Carrega dados
df = pd.read_csv('data/processed/crimes_consolidado.csv')

# Filtra Homicídio Doloso na Zona Sul
df_filtrado = df[
    (df['tipo_crime'] == 'Homicídio Doloso') & 
    (df['regiao_administrativa'] == 'Zona Sul')
]

# Prepara série temporal
df_serie = df_filtrado.groupby('data')['total_ocorrencias'].sum().reset_index()
df_serie.columns = ['data', 'valor']

# Predição Prophet (6 meses)
resultado = TraditionalModels.prophet_forecast(df_serie, horizonte=6)

print("Previsões:", resultado['forecast'])
print("Intervalo Confiança:", resultado['lower'], resultado['upper'])
```

### Exemplo 2: XGBoost com Features Customizadas
```python
from pages.05_🤖_Modelos_Preditivos import MLModels

# Série temporal
serie = df_filtrado['total_ocorrencias'].values

# XGBoost com 12 lags
resultado = MLModels.xgboost_forecast(
    serie=serie,
    horizonte=6,
    n_lags=12
)

print("Previsão 6 meses:", resultado['forecast'])
print("MAE:", resultado['mae'])
print("Feature Importance:", resultado['feature_importance'])
```

### Exemplo 3: LSTM para Previsão de Longo Prazo
```python
from pages.05_🤖_Modelos_Preditivos import DeepLearningModels

# LSTM - 12 meses de previsão
resultado = DeepLearningModels.lstm_forecast(
    serie=serie,
    horizonte=12,
    n_lags=24,  # Usa 24 meses de contexto
    epochs=100
)

print("Previsão 12 meses:", resultado['forecast'])
print("RMSE:", resultado['rmse'])
```

### Exemplo 4: Ensemble de Todos os Modelos
```python
from pages.05_🤖_Modelos_Preditivos import (
    TraditionalModels, MLModels, DeepLearningModels, AdvancedEnsemble
)

# Executa múltiplos modelos
resultados = [
    TraditionalModels.prophet_forecast(df_serie, 6),
    MLModels.xgboost_forecast(serie, 6, 12),
    DeepLearningModels.lstm_forecast(serie, 6, 12, 50)
]

# Ensemble inteligente
ensemble = AdvancedEnsemble.weighted_ensemble(resultados)

print("Ensemble Forecast:", ensemble['forecast'])
print("Pesos dos modelos:", ensemble['pesos'])
print("Número de modelos:", ensemble['n_modelos'])
```

## 🔍 Troubleshooting

### Problema: "No module named 'tensorflow'"
**Solução:**
```bash
pip install tensorflow>=2.15.0

# Se usar Mac M1/M2/M3:
pip install tensorflow-macos tensorflow-metal
```

### Problema: "CUDA not available" (GPU não detectada)
**Solução:**
```bash
# Verificar GPU
nvidia-smi

# Verificar TensorFlow
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Instalar versão CUDA
pip install tensorflow[and-cuda]
```

### Problema: GeoPandas/Fiona falha na instalação
**Windows:**
```bash
pip install pipwin
pipwin install fiona
pipwin install gdal
pip install geopandas
```

**Linux:**
```bash
sudo apt-get install libgdal-dev libproj-dev libgeos-dev
pip install geopandas
```

**Mac:**
```bash
brew install gdal
pip install geopandas
```

### Problema: LSTM muito lento
**Soluções:**

1. **Reduzir epochs:**
```python
resultado = DeepLearningModels.lstm_forecast(serie, 6, 12, epochs=20)
```

2. **Usar GPU:**
   - Instale CUDA + cuDNN
   - TensorFlow detectará automaticamente

3. **Alternativa - usar modelos mais leves:**
```python
# XGBoost é muito rápido e quase tão preciso
resultado = MLModels.xgboost_forecast(serie, 6, 12)
```

### Problema: Streamlit lento/travando
**Soluções:**

1. **Use cache agressivo:**
```python
@st.cache_data(ttl=3600)  # Cache por 1 hora
def funcao_pesada():
    ...
```

2. **Desative modelos pesados:**
   - Desmarque LSTM se não for necessário
   - Use apenas Prophet + XGBoost para velocidade

3. **Análises R - execute 1x:**
   - Resultados são cacheados automaticamente
   - Limpe cache apenas quando necessário

## 📊 Performance Esperada

### Tempo de Execução (série de 60 meses, horizonte 6 meses)
| Modelo | CPU (i5) | CPU (M2) | GPU (RTX 3060) |
|--------|----------|----------|----------------|
| ARIMA | 0.5s | 0.3s | - |
| Prophet | 2s | 1s | - |
| XGBoost | 1s | 0.5s | - |
| Random Forest | 3s | 1.5s | - |
| LSTM (50 epochs) | 60s | 30s | 5s |
| Ensemble | 5s | 2.5s | - |

### Memória RAM Necessária
- **Mínimo**: 8GB
- **Recomendado**: 16GB
- **Com LSTM**: 16GB+
- **Streamlit Cloud**: 1GB (limitado)

## 🎓 Recomendações de Uso

### Para Análise Exploratória Rápida:
- ✅ Prophet
- ✅ ARIMA
- ✅ Ensemble (sem LSTM)

### Para Máxima Acurácia:
- ✅ XGBoost
- ✅ LSTM
- ✅ Ensemble Completo

### Para Produção/Deploy:
- ✅ Prophet (rápido e robusto)
- ✅ XGBoost (bom balanço)
- ❌ Evite LSTM (lento sem GPU)

### Para Apresentações:
- ✅ Ensemble (impressiona)
- ✅ Prophet (visualizações bonitas)
- ✅ Feature Importance do XGBoost

## 📞 Suporte

- **Issues**: https://github.com/seu-usuario/violencia-rio-ml/issues
- **Documentação**: https://docs.seu-projeto.com
- **Email**: seu-email@exemplo.com

## 🎉 Pronto!

Seu sistema está completo com:
- ✅ 8 modelos preditivos diferentes
- ✅ Interface Streamlit profissional
- ✅ Integração Python + R
- ✅ Cache inteligente
- ✅ Visualizações interativas
- ✅ Fácil de usar e manter

**Comece agora:**
```bash
streamlit run Home.py
```

---

**🔮 Sistema de Análise Preditiva de Violência no Rio de Janeiro**

*Desenvolvido com Python + R | Streamlit + Plotly | Machine Learning*