#!/usr/bin/env python3
"""
🔧 SETUP COMPLETO - Sistema de Análise Preditiva
===============================================

Script de configuração completa do sistema de análise preditiva de violência
no Rio de Janeiro com todas as verificações e instalações necessárias.

Uso:
    python setup_completo.py
    python setup_completo.py --skip-r
    python setup_completo.py --force
"""

import subprocess
import sys
import os
import json
from pathlib import Path
import argparse

def print_header():
    """Imprime cabeçalho do sistema"""
    print("🔮 SISTEMA DE ANÁLISE PREDITIVA DE VIOLÊNCIA")
    print("Rio de Janeiro - Python + R Híbrido")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def create_directories():
    """Cria estrutura de diretórios"""
    print("📁 Criando estrutura de diretórios...")
    
    directories = [
        'data/raw',
        'data/processed', 
        'data/models',
        'data/r_cache',
        'src/r_scripts',
        'src/python_scripts',
        'notebooks',
        'pages',
        'outputs/reports',
        'outputs/visualizations'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")
    
    return True

def check_requirements_file():
    """Verifica arquivo de requirements"""
    print("📋 Verificando requirements...")
    
    if not Path('requirements_hibrido.txt').exists():
        print("❌ requirements_hibrido.txt não encontrado")
        return False
    
    print("✅ requirements_hibrido.txt encontrado")
    return True

def install_python_packages():
    """Instala pacotes Python"""
    print("📦 Instalando pacotes Python...")
    
    try:
        # Atualiza pip
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
        ], check=True, capture_output=True)
        
        # Instala requirements
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_hibrido.txt'
        ], check=True, capture_output=True)
        
        print("✅ Pacotes Python instalados")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def check_r_installation():
    """Verifica instalação do R"""
    print("📊 Verificando R...")
    
    try:
        result = subprocess.run(['R', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ R instalado")
            return True
        else:
            print("❌ R não encontrado")
            return False
    except FileNotFoundError:
        print("❌ R não encontrado")
        return False

def install_r_packages():
    """Instala pacotes R"""
    print("📦 Instalando pacotes R...")
    
    if not check_r_installation():
        print("⚠️ R não disponível. Pulando instalação de pacotes R.")
        return True
    
    try:
        # Executa script de instalação R
        if Path('install_r_dependencies.R').exists():
            subprocess.run(['Rscript', 'install_r_dependencies.R'], check=True)
            print("✅ Pacotes R instalados")
        else:
            print("⚠️ Script de instalação R não encontrado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação R: {e}")
        return False

def test_imports():
    """Testa importações principais"""
    print("🧪 Testando importações...")
    
    packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'geopandas',
        'folium',
        'statsmodels',
        'sklearn',
        'xgboost'
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed.append(package)
    
    if failed:
        print(f"\n💡 Pacotes com erro: {failed}")
        return False
    
    return True

def create_config_file():
    """Cria arquivo de configuração"""
    print("⚙️ Criando arquivo de configuração...")
    
    config = {
        "project_name": "Análise Preditiva de Violência - Rio de Janeiro",
        "version": "1.0.0",
        "python_version": sys.version,
        "directories": {
            "data": "data/",
            "models": "data/models/",
            "cache": "data/r_cache/",
            "outputs": "outputs/"
        },
        "models": {
            "traditional": ["ARIMA", "SARIMA", "Prophet", "Exp Smoothing"],
            "ml": ["Random Forest", "XGBoost", "Gradient Boosting"],
            "deep": ["LSTM"],
            "ensemble": ["Weighted Ensemble"]
        },
        "cache": {
            "ttl_hours": 24,
            "max_size_mb": 100
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ config.json criado")
    return True

def test_system():
    """Testa sistema completo"""
    print("🔬 Testando sistema...")
    
    # Testa Streamlit
    try:
        import streamlit as st
        print("✅ Streamlit OK")
    except ImportError:
        print("❌ Streamlit não disponível")
        return False
    
    # Testa modelos
    try:
        from statsmodels.tsa.arima.model import ARIMA
        print("✅ Statsmodels OK")
    except ImportError:
        print("❌ Statsmodels não disponível")
        return False
    
    # Testa ML
    try:
        from sklearn.ensemble import RandomForestRegressor
        print("✅ Scikit-learn OK")
    except ImportError:
        print("❌ Scikit-learn não disponível")
        return False
    
    return True

def create_startup_script():
    """Cria script de inicialização"""
    print("🚀 Criando script de inicialização...")
    
    startup_content = '''#!/bin/bash
# Script de inicialização do sistema

echo "🔮 Iniciando Sistema de Análise Preditiva..."
echo "=========================================="

# Ativa ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
fi

# Executa Streamlit
echo "🚀 Executando Streamlit..."
streamlit run Home.py
'''
    
    with open('start.sh', 'w') as f:
        f.write(startup_content)
    
    # Torna executável
    os.chmod('start.sh', 0o755)
    
    print("✅ start.sh criado")
    return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Setup completo do sistema")
    parser.add_argument("--skip-r", action="store_true", help="Pular instalação R")
    parser.add_argument("--force", action="store_true", help="Forçar reinstalação")
    parser.add_argument("--test-only", action="store_true", help="Apenas testar")
    
    args = parser.parse_args()
    
    print_header()
    
    if args.test_only:
        # Apenas testes
        if not test_imports():
            return 1
        if not test_system():
            return 1
        print("\n✅ Todos os testes passaram!")
        return 0
    
    # Verificações básicas
    if not check_python_version():
        return 1
    
    # Cria estrutura
    if not create_directories():
        return 1
    
    if not check_requirements_file():
        return 1
    
    # Instala dependências
    if not install_python_packages():
        return 1
    
    # R (opcional)
    if not args.skip_r:
        if not install_r_packages():
            print("⚠️ Continuando sem R...")
    
    # Testes
    if not test_imports():
        return 1
    
    if not test_system():
        return 1
    
    # Configuração
    if not create_config_file():
        return 1
    
    if not create_startup_script():
        return 1
    
    # Sucesso
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETO COM SUCESSO!")
    print("=" * 60)
    print()
    print("📌 PRÓXIMOS PASSOS:")
    print("1. Execute: python run.py")
    print("2. Ou: streamlit run Home.py")
    print("3. Ou: ./start.sh (Linux/Mac)")
    print()
    print("🌐 O sistema estará disponível em: http://localhost:8501")
    print()
    print("📚 Documentação: README.md")
    print("🔧 Configuração: config.json")
    print()
    print("✅ Sistema pronto para uso!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

