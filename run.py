#!/usr/bin/env python3
"""
🚀 EXECUTOR SIMPLIFICADO - Sistema de Análise Preditiva
=====================================================

Script para executar o sistema completo de análise preditiva de violência
no Rio de Janeiro com verificações automáticas.

Uso:
    python run.py
    python run.py --port 8502
    python run.py --host 0.0.0.0
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def check_dependencies():
    """Verifica dependências principais"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n💡 Instale os pacotes faltantes:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_files():
    """Verifica arquivos necessários"""
    print("📁 Verificando arquivos...")
    
    required_files = [
        'Home.py',
        'requirements_hibrido.txt'
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ {file}")
            missing.append(file)
        else:
            print(f"✅ {file}")
    
    if missing:
        print(f"\n💡 Arquivos faltantes: {missing}")
        return False
    
    return True

def install_dependencies():
    """Instala dependências se necessário"""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_hibrido.txt'
        ], check=True, capture_output=True)
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def run_streamlit(host="localhost", port=8501):
    """Executa o Streamlit"""
    print(f"🚀 Executando Streamlit em http://{host}:{port}")
    
    try:
        subprocess.run([
            'streamlit', 'run', 'Home.py',
            '--server.port', str(port),
            '--server.address', host
        ])
    except KeyboardInterrupt:
        print("\n👋 Sistema interrompido pelo usuário")
    except FileNotFoundError:
        print("❌ Streamlit não encontrado. Instale com: pip install streamlit")
        return False
    
    return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Executa o sistema de análise preditiva")
    parser.add_argument("--host", default="localhost", help="Host do servidor")
    parser.add_argument("--port", type=int, default=8501, help="Porta do servidor")
    parser.add_argument("--install", action="store_true", help="Instalar dependências")
    parser.add_argument("--skip-checks", action="store_true", help="Pular verificações")
    
    args = parser.parse_args()
    
    print("🔮 SISTEMA DE ANÁLISE PREDITIVA DE VIOLÊNCIA")
    print("=" * 50)
    
    if not args.skip_checks:
        # Verificações
        if not check_python_version():
            return 1
        
        if not check_files():
            return 1
        
        if not check_dependencies():
            if args.install:
                if not install_dependencies():
                    return 1
            else:
                print("\n💡 Execute com --install para instalar dependências automaticamente")
                return 1
    
    # Executa sistema
    print(f"\n🚀 Iniciando sistema em http://{args.host}:{args.port}")
    print("💡 Pressione Ctrl+C para parar")
    
    success = run_streamlit(args.host, args.port)
    
    if success:
        print("\n✅ Sistema executado com sucesso!")
    else:
        print("\n❌ Erro ao executar sistema")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
