# 📦 GUIA DE INSTALAÇÃO DE DEPENDÊNCIAS

## 🎯 Objetivo

Este guia mostra como instalar todas as dependências necessárias para o projeto de Análise de Violência no Rio de Janeiro.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com a internet

## 🚀 Instalação Rápida

### Opção 1: Script Automatizado (Recomendado)

```bash
python setup_environment.py
```

Este script irá:
- ✅ Atualizar o pip
- ✅ Instalar todas as dependências
- ✅ Verificar a instalação
- ✅ Exibir relatório completo

### Opção 2: Instalação Manual

```bash
# 1. Atualizar pip
python -m pip install --upgrade pip

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar instalação
pip list
```

## 📦 Dependências Principais

### Análise de Dados
- `pandas>=2.0.0` - Manipulação de dados
- `numpy>=1.24.0` - Computação numérica

### Visualização
- `plotly>=5.17.0` - Gráficos interativos
- `folium>=0.15.0` - Mapas interativos
- `matplotlib>=3.7.0` - Gráficos estáticos
- `seaborn>=0.12.0` - Visualizações estatísticas

### Machine Learning
- `scikit-learn>=1.3.0` - Algoritmos de ML
- `xgboost>=2.0.0` - Gradient Boosting
- `statsmodels>=0.14.0` - Modelos estatísticos
- `prophet>=1.1.0` - Previsões de séries temporais

### Geoespacial
- `geopandas>=0.13.0` - Análise geoespacial
- `shapely>=2.0.0` - Geometrias geoespaciais

### Utilidades
- `requests>=2.31.0` - Requisições HTTP
- `tqdm>=4.65.0` - Barras de progresso
- `streamlit>=1.28.0` - Interface web

### Desenvolvimento
- `jupyter>=1.0.0` - Notebooks interativos
- `ipykernel>=6.25.0` - Kernel para Jupyter
- `notebook>=6.5.0` - Interface Jupyter

## 🔧 Resolução de Problemas

### Erro: "Import could not be resolved"

**Causa:** O linter não encontra as bibliotecas instaladas.

**Solução 1:** Recarregar o VS Code
```
Ctrl+Shift+P → "Developer: Reload Window"
```

**Solução 2:** Selecionar o interpretador correto
```
Ctrl+Shift+P → "Python: Select Interpreter"
```

**Solução 3:** Instalar no ambiente correto
```bash
# Verificar qual Python está sendo usado
python --version
which python  # Linux/Mac
where python  # Windows

# Instalar nesse Python específico
python -m pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError"

**Causa:** Biblioteca não está instalada.

**Solução:**
```bash
# Instalar biblioteca específica
pip install nome-da-biblioteca

# Ou reinstalar tudo
pip install -r requirements.txt --force-reinstall
```

### Erro: "DLL load failed" (Windows)

**Causa:** Problema com dependências do sistema.

**Solução:**
```bash
# Instalar Microsoft Visual C++ Redistributable
# Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Ou usar conda (alternativa)
conda install -c conda-forge geopandas shapely
```

### Erro: "Permission denied"

**Causa:** Falta de permissões.

**Solução:**
```bash
# Linux/Mac
sudo pip install -r requirements.txt

# Windows (executar como Administrador)
pip install -r requirements.txt

# Ou instalar localmente
pip install --user -r requirements.txt
```

## 🧪 Verificar Instalação

Execute o seguinte código Python:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
import sklearn
import xgboost
import statsmodels
import prophet
import geopandas as gpd
import shapely
import requests
import tqdm
import streamlit as st

print("✅ Todas as bibliotecas instaladas com sucesso!")
```

## 📊 Ambientes Virtuais (Opcional)

### Criar ambiente virtual

```bash
# Criar
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Desativar
deactivate
```

## 🆘 Suporte

Se continuar com problemas:

1. **Verifique a versão do Python:**
   ```bash
   python --version
   ```
   Deve ser 3.8 ou superior.

2. **Atualize o pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Limpe o cache do pip:**
   ```bash
   pip cache purge
   ```

4. **Reinstale tudo:**
   ```bash
   pip uninstall -y -r requirements.txt
   pip install -r requirements.txt
   ```

## 📝 Notas

- Os warnings de importação do linter (VSCode) são normais se as bibliotecas não estão instaladas no ambiente do linter.
- Use `setup_environment.py` para uma instalação automática e verificação.
- Para Streamlit Cloud, não é necessário instalar localmente - use apenas o `requirements.txt`.

## ✅ Checklist Final

- [ ] Python 3.8+ instalado
- [ ] pip atualizado
- [ ] Dependências instaladas
- [ ] Verificação executada com sucesso
- [ ] VS Code reconhece as bibliotecas
- [ ] Streamlit funciona localmente
- [ ] Notebooks abrem sem erros

---

**Última atualização:** 2025-01-12



