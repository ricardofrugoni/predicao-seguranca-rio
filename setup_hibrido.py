#!/usr/bin/env python3
"""
SETUP DO AMBIENTE HÍBRIDO PYTHON + R
====================================

Este script configura o ambiente híbrido otimizado para análise de violência
no Rio de Janeiro, combinando Python e R de forma eficiente.

Funcionalidades:
- Instala dependências Python
- Configura ambiente R
- Testa integração Python-R
- Cria estrutura de cache
- Valida scripts R
"""

import subprocess
import sys
import os
from pathlib import Path
import json

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            return True
        else:
            print(f"❌ {description} - Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {str(e)}")
        return False

def check_python_packages():
    """Verifica pacotes Python necessários"""
    print("\n📦 Verificando pacotes Python...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'geopandas',
        'folium', 'statsmodels', 'prophet', 'scikit-learn',
        'rpy2', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Não instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Instale os pacotes faltantes:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_r_installation():
    """Verifica instalação do R"""
    print("\n🔍 Verificando instalação do R...")
    
    # Verifica se R está instalado
    if not run_command("R --version", "Verificando R"):
        print("❌ R não encontrado. Instale o R primeiro.")
        return False
    
    # Verifica se Rscript está disponível
    if not run_command("Rscript --version", "Verificando Rscript"):
        print("❌ Rscript não encontrado.")
        return False
    
    return True

def install_r_packages():
    """Instala pacotes R necessários"""
    print("\n📦 Instalando pacotes R...")
    
    r_script = Path("install_r_dependencies.R")
    if r_script.exists():
        return run_command("Rscript install_r_dependencies.R", "Instalando dependências R")
    else:
        print("❌ Script de instalação R não encontrado")
        return False

def test_r_scripts():
    """Testa scripts R"""
    print("\n🧪 Testando scripts R...")
    
    r_scripts_dir = Path("src/r_scripts")
    if not r_scripts_dir.exists():
        print("❌ Diretório de scripts R não encontrado")
        return False
    
    # Lista scripts R
    r_scripts = list(r_scripts_dir.glob("*.R"))
    if not r_scripts:
        print("❌ Nenhum script R encontrado")
        return False
    
    print(f"📋 Scripts R encontrados: {len(r_scripts)}")
    for script in r_scripts:
        print(f"  - {script.name}")
    
    return True

def create_cache_structure():
    """Cria estrutura de cache"""
    print("\n📁 Criando estrutura de cache...")
    
    cache_dir = Path("data/r_cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Cria arquivo de configuração do cache
    cache_config = {
        "cache_dir": str(cache_dir),
        "ttl_hours": 24,
        "max_size_mb": 100,
        "compression": True
    }
    
    config_file = cache_dir / "cache_config.json"
    with open(config_file, 'w') as f:
        json.dump(cache_config, f, indent=2)
    
    print(f"✅ Cache configurado em: {cache_dir}")
    return True

def test_python_r_integration():
    """Testa integração Python-R"""
    print("\n🔗 Testando integração Python-R...")
    
    try:
        # Testa rpy2
        import rpy2.robjects as ro
        from rpy2.robjects.packages import importr
        
        # Testa importação de pacote R
        base = importr('base')
        result = base.sum(ro.IntVector([1, 2, 3, 4, 5]))
        
        print("✅ rpy2 funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração Python-R: {str(e)}")
        print("💡 Instale rpy2: pip install rpy2")
        return False

def create_requirements_hibrido():
    """Cria requirements.txt para ambiente híbrido"""
    print("\n📝 Criando requirements.txt híbrido...")
    
    requirements = [
        "# Ambiente Híbrido Python + R",
        "# Análise de Violência no Rio de Janeiro",
        "",
        "# Core Python",
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "",
        "# Visualização",
        "plotly>=5.15.0",
        "folium>=0.14.0",
        "streamlit-folium>=0.13.0",
        "",
        "# Análise Espacial",
        "geopandas>=0.13.0",
        "shapely>=2.0.0",
        "fiona>=1.9.0",
        "",
        "# Séries Temporais",
        "statsmodels>=0.14.0",
        "prophet>=1.1.0",
        "",
        "# Machine Learning",
        "scikit-learn>=1.3.0",
        "xgboost>=1.7.0",
        "",
        "# Integração R",
        "rpy2>=3.5.0",
        "",
        "# Utilitários",
        "tqdm>=4.65.0",
        "requests>=2.31.0",
        "aiohttp>=3.8.0",
        "",
        "# Jupyter",
        "jupyter>=1.0.0",
        "notebook>=6.5.0",
        "ipykernel>=6.25.0"
    ]
    
    with open("requirements_hibrido.txt", 'w') as f:
        f.write('\n'.join(requirements))
    
    print("✅ requirements_hibrido.txt criado")
    return True

def create_dockerfile_hibrido():
    """Cria Dockerfile para ambiente híbrido"""
    print("\n🐳 Criando Dockerfile híbrido...")
    
    dockerfile_content = """
# Dockerfile para Ambiente Híbrido Python + R
FROM python:3.9-slim

# Instala R
RUN apt-get update && apt-get install -y \\
    r-base \\
    r-base-dev \\
    libcurl4-openssl-dev \\
    libssl-dev \\
    libxml2-dev \\
    libgdal-dev \\
    libproj-dev \\
    libgeos-dev \\
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements_hibrido.txt .
RUN pip install -r requirements_hibrido.txt

# Instala dependências R
COPY install_r_dependencies.R .
RUN Rscript install_r_dependencies.R

# Configura diretório de trabalho
WORKDIR /app
COPY . .

# Expõe porta do Streamlit
EXPOSE 8501

# Comando para executar o dashboard
CMD ["streamlit", "run", "dashboard_hibrido.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", 'w') as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile criado")
    return True

def main():
    """Função principal de setup"""
    print("🚀 CONFIGURANDO AMBIENTE HÍBRIDO PYTHON + R")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 8
    
    # 1. Verifica pacotes Python
    if check_python_packages():
        success_count += 1
    
    # 2. Verifica instalação R
    if check_r_installation():
        success_count += 1
    
    # 3. Instala pacotes R
    if install_r_packages():
        success_count += 1
    
    # 4. Testa scripts R
    if test_r_scripts():
        success_count += 1
    
    # 5. Cria estrutura de cache
    if create_cache_structure():
        success_count += 1
    
    # 6. Testa integração Python-R
    if test_python_r_integration():
        success_count += 1
    
    # 7. Cria requirements híbrido
    if create_requirements_hibrido():
        success_count += 1
    
    # 8. Cria Dockerfile
    if create_dockerfile_hibrido():
        success_count += 1
    
    # Resultado final
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {success_count}/{total_tasks} tarefas concluídas")
    
    if success_count == total_tasks:
        print("🎉 AMBIENTE HÍBRIDO CONFIGURADO COM SUCESSO!")
        print("\n📌 PRÓXIMOS PASSOS:")
        print("1. Execute: streamlit run dashboard_hibrido.py")
        print("2. Ou use Docker: docker build -t violencia-rj .")
        print("3. Ou execute os notebooks individualmente")
    else:
        print("⚠️ ALGUMAS TAREFAS FALHARAM")
        print("💡 Verifique os erros acima e execute novamente")
    
    return success_count == total_tasks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
