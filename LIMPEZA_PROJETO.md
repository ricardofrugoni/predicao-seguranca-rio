# 🧹 LIMPEZA DO PROJETO - RELATÓRIO

## 📊 RESUMO

**Total de arquivos a remover:** 35 arquivos
**Espaço estimado:** ~15MB
**Benefícios:** Projeto mais limpo, organizado e profissional

---

## 🗑️ ARQUIVOS PARA REMOVER

### 1. Documentação MD Obsoleta (9 arquivos):
- ❌ ATUALIZACAO_MAPA_MUNICIPIO.md
- ❌ CONFIGURAR_GITHUB.md
- ❌ DEPLOY_GITHUB.md
- ❌ DEPLOY_RAPIDO.md
- ❌ ERROS_RESOLVIDOS.md
- ❌ STATUS_ERROS.md
- ❌ TROUBLESHOOTING.md
- ❌ RESUMO_FINAL.md
- ❌ INSTALAR_DEPENDENCIAS.md

### 2. Scripts de Deploy (6 arquivos):
- ❌ deploy_commands.bat
- ❌ deploy_commands.sh
- ❌ deploy.sh
- ❌ deploy_github.py
- ❌ FAZER_PUSH.bat
- ❌ push_github.py

### 3. Scripts de Download (8 arquivos):
- ❌ scripts/baixar_bairros_oficiais_completo.py
- ❌ scripts/baixar_bairros_oficiais_rio.py
- ❌ scripts/baixar_shapefile_oficial_data_rio.py
- ❌ scripts/baixar_shapefile_real_rio.py
- ❌ scripts/baixar_shapefile_rio.py
- ❌ scripts/buscar_bairros_rio_completo.py
- ❌ scripts/buscar_dados_oficiais_rio.py
- ❌ scripts/download_geojson_real.py

### 4. GeoJSON Duplicados (11 arquivos):
- ❌ data/shapefiles/areas_detalhadas_rio.geojson
- ❌ data/shapefiles/bairros_rio_completo.geojson
- ❌ data/shapefiles/bairros_rio_oficial_ibge.geojson
- ❌ data/shapefiles/bairros_rio_simulado.geojson
- ❌ data/shapefiles/limite_municipal_ibge.geojson
- ❌ data/shapefiles/limite_municipal_rio.geojson
- ❌ data/shapefiles/municipio_rio_bairros.geojson
- ❌ data/shapefiles/regioes_administrativas_rio.geojson
- ❌ data/shapefiles/rio_bairros_(tbrugz).geojson
- ❌ data/shapefiles/zonas_rio_realista.geojson
- ❌ data/shapefiles/zonas_rio.geojson

### 5. Outros (1 arquivo):
- ❌ h origin main (arquivo estranho)

---

## ✅ ARQUIVOS A MANTER

### Documentação (2):
- ✅ README.md
- ✅ REFATORACAO_POO.md

### GeoJSON (2):
- ✅ zonas_rio_limites_reais.geojson
- ✅ municipio_rio_zonas_real.geojson (backup)

### Scripts Úteis (1):
- ✅ run_local.bat

---

## 📈 MELHORIAS POO SUGERIDAS

### 1. **Separar Cache do Streamlit da Lógica**
```python
# ANTES:
class CrimeDataLoader:
    @st.cache_data
    def load(_self, filename):  # _self é workaround feio
        pass

# DEPOIS:
class CrimeDataLoader:
    def load(self, filename):  # Lógica pura
        pass

# Em pages/:
@st.cache_data
def get_crime_data(filename):
    return CrimeDataLoader().load(filename)
```

### 2. **Injeção de Dependências**
```python
# ANTES:
from src.config import config

class BaseDataLoader:
    def __init__(self):
        self.config = config  # Hard-coded

# DEPOIS:
class BaseDataLoader:
    def __init__(self, config: AppConfig = None):
        self.config = config or get_default_config()
```

### 3. **Exception Handling Específico**
```python
# ANTES:
except Exception as e:
    pass

# DEPOIS:
except (FileNotFoundError, ValueError) as e:
    logger.error(f"Error: {e}")
    raise
```

### 4. **Logging**
```python
# Adicionar:
import logging

logger = logging.getLogger(__name__)

# Usar em vez de print ou pass silencioso
```

### 5. **Interfaces Explícitas (Protocol)**
```python
from typing import Protocol

class DataLoaderProtocol(Protocol):
    def load(self) -> pd.DataFrame: ...
    def filter_by(self, **kwargs) -> pd.DataFrame: ...
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Executar limpeza** (remover 35 arquivos)
2. **Implementar melhorias POO**
3. **Adicionar logging**
4. **Atualizar README** (incorporar instruções dos MDs removidos)
5. **Commit final**

---

**Deseja prosseguir com a limpeza?**

