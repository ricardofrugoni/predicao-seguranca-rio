#!/usr/bin/env python3
"""
🚀 DEPLOY AUTOMATIZADO PARA GITHUB
=================================

Script para automatizar o deploy do sistema de análise preditiva
no GitHub e Streamlit Cloud.

Uso:
    python deploy_github.py
    python deploy_github.py --repo-name "meu-repositorio"
    python deploy_github.py --skip-git
"""

import subprocess
import sys
import os
import json
import webbrowser
from pathlib import Path
import argparse

def print_header():
    """Imprime cabeçalho"""
    print("🚀 DEPLOY AUTOMATIZADO PARA GITHUB")
    print("Sistema de Análise Preditiva - Rio de Janeiro")
    print("=" * 50)
    print()

def check_git_installed():
    """Verifica se Git está instalado"""
    print("🔍 Verificando Git...")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git instalado: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Git não encontrado")
        return False

def check_git_configured():
    """Verifica se Git está configurado"""
    print("⚙️ Verificando configuração do Git...")
    
    try:
        # Verifica nome
        result_name = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        result_email = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
        
        if result_name.returncode == 0 and result_email.returncode == 0:
            print(f"✅ Git configurado: {result_name.stdout.strip()} <{result_email.stdout.strip()}>")
            return True
        else:
            print("❌ Git não configurado")
            print("💡 Configure com:")
            print("   git config --global user.name 'Seu Nome'")
            print("   git config --global user.email 'seu.email@exemplo.com'")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar Git: {e}")
        return False

def init_git_repo():
    """Inicializa repositório Git"""
    print("📁 Inicializando repositório Git...")
    
    try:
        # Verifica se já é um repositório
        if Path('.git').exists():
            print("✅ Repositório Git já existe")
            return True
        
        # Inicializa repositório
        subprocess.run(['git', 'init'], check=True)
        print("✅ Repositório Git inicializado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao inicializar Git: {e}")
        return False

def create_gitignore():
    """Cria .gitignore se não existir"""
    print("📝 Verificando .gitignore...")
    
    if Path('.gitignore').exists():
        print("✅ .gitignore já existe")
        return True
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/
.venv/

# Jupyter Notebook
.ipynb_checkpoints

# Data files
data/raw/
data/processed/
data/r_cache/
*.csv
*.xlsx
*.json
*.geojson
*.shp
*.dbf
*.shx
*.prj

# Model files
models/
*.pkl
*.joblib
*.h5
*.pb

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Cache
__pycache__/
*.cache
.cache/

# Temporary files
*.tmp
*.temp
temp/
tmp/

# Environment variables
.env
.env.local
.env.production
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore criado")
    return True

def create_streamlit_config():
    """Cria configuração do Streamlit"""
    print("⚙️ Criando configuração do Streamlit...")
    
    config_dir = Path('.streamlit')
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print("✅ Configuração do Streamlit criada")
    return True

def add_files_to_git():
    """Adiciona arquivos ao Git"""
    print("📦 Adicionando arquivos ao Git...")
    
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Arquivos adicionados ao Git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao adicionar arquivos: {e}")
        return False

def commit_changes():
    """Faz commit das mudanças"""
    print("💾 Fazendo commit...")
    
    try:
        subprocess.run([
            'git', 'commit', '-m', 
            'Sistema completo de análise preditiva de violência - Rio de Janeiro'
        ], check=True)
        print("✅ Commit realizado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no commit: {e}")
        return False

def create_github_repo_instructions(repo_name):
    """Cria instruções para criar repositório no GitHub"""
    print("🌐 Instruções para criar repositório no GitHub:")
    print("=" * 50)
    print()
    print("1. Acesse: https://github.com/new")
    print("2. Repository name:", repo_name)
    print("3. Description: Sistema de análise preditiva de violência no Rio de Janeiro")
    print("4. Visibility: Public")
    print("5. Initialize: ❌ NÃO marque nenhuma opção")
    print("6. Clique em 'Create repository'")
    print()
    print("7. Após criar, execute:")
    print(f"   git remote add origin https://github.com/SEU-USUARIO/{repo_name}.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    
    # Abre GitHub no navegador
    try:
        webbrowser.open('https://github.com/new')
        print("🌐 Abrindo GitHub no navegador...")
    except:
        print("💡 Abra manualmente: https://github.com/new")

def create_streamlit_instructions(repo_name):
    """Cria instruções para Streamlit Cloud"""
    print("🚀 Instruções para Streamlit Cloud:")
    print("=" * 50)
    print()
    print("1. Acesse: https://streamlit.io/cloud")
    print("2. Clique em 'Sign in with GitHub'")
    print("3. Clique em 'New app'")
    print("4. Repository:", repo_name)
    print("5. Branch: main")
    print("6. Main file path: Home.py")
    print("7. App URL:", repo_name)
    print("8. Clique em 'Deploy!'")
    print()
    print("Sua aplicação estará disponível em:")
    print(f"https://{repo_name}.streamlit.app")
    print()
    
    # Abre Streamlit Cloud no navegador
    try:
        webbrowser.open('https://streamlit.io/cloud')
        print("🌐 Abrindo Streamlit Cloud no navegador...")
    except:
        print("💡 Abra manualmente: https://streamlit.io/cloud")

def create_deploy_script():
    """Cria script de deploy"""
    print("📝 Criando script de deploy...")
    
    deploy_script = """#!/bin/bash
# Script de deploy automático

echo "🚀 Fazendo deploy do sistema..."

# Verifica se há mudanças
if [ -n "$(git status --porcelain)" ]; then
    echo "📦 Adicionando mudanças..."
    git add .
    git commit -m "Atualização automática - $(date)"
    git push origin main
    echo "✅ Deploy realizado!"
else
    echo "ℹ️ Nenhuma mudança detectada"
fi
"""
    
    with open('deploy.sh', 'w') as f:
        f.write(deploy_script)
    
    # Torna executável
    os.chmod('deploy.sh', 0o755)
    
    print("✅ Script de deploy criado: deploy.sh")
    return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Deploy automático para GitHub")
    parser.add_argument("--repo-name", default="violencia-rio-analise-preditiva", 
                       help="Nome do repositório no GitHub")
    parser.add_argument("--skip-git", action="store_true", 
                       help="Pular configuração do Git")
    parser.add_argument("--instructions-only", action="store_true",
                       help="Apenas mostrar instruções")
    
    args = parser.parse_args()
    
    print_header()
    
    if args.instructions_only:
        create_github_repo_instructions(args.repo_name)
        create_streamlit_instructions(args.repo_name)
        return 0
    
    # Verificações
    if not check_git_installed():
        print("\n💡 Instale Git primeiro: https://git-scm.com/")
        return 1
    
    if not args.skip_git:
        if not check_git_configured():
            print("\n💡 Configure Git primeiro:")
            print("git config --global user.name 'Seu Nome'")
            print("git config --global user.email 'seu.email@exemplo.com'")
            return 1
    
    # Configuração
    if not init_git_repo():
        return 1
    
    if not create_gitignore():
        return 1
    
    if not create_streamlit_config():
        return 1
    
    if not add_files_to_git():
        return 1
    
    if not commit_changes():
        return 1
    
    if not create_deploy_script():
        return 1
    
    # Instruções
    print("\n" + "=" * 50)
    print("🎉 CONFIGURAÇÃO LOCAL CONCLUÍDA!")
    print("=" * 50)
    print()
    
    create_github_repo_instructions(args.repo_name)
    print()
    create_streamlit_instructions(args.repo_name)
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Siga as instruções acima")
    print("2. Execute: ./deploy.sh (para futuras atualizações)")
    print("3. Sua aplicação estará online!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

