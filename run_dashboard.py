#!/usr/bin/env python3
"""
EXECUTOR DO DASHBOARD HÍBRIDO
=============================

Script para executar o dashboard híbrido Python + R
com configurações otimizadas.

Uso:
    python run_dashboard.py
    python run_dashboard.py --port 8502
    python run_dashboard.py --host 0.0.0.0
"""

import subprocess
import sys
import argparse
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'geopandas', 'folium', 'statsmodels'
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

def check_r_installation():
    """Verifica se R está instalado"""
    print("\n🔍 Verificando R...")
    
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

def check_dashboard_file():
    """Verifica se o arquivo do dashboard existe"""
    dashboard_file = Path("dashboard_hibrido.py")
    if dashboard_file.exists():
        print(f"✅ Dashboard encontrado: {dashboard_file}")
        return True
    else:
        print(f"❌ Dashboard não encontrado: {dashboard_file}")
        return False

def run_dashboard(host="localhost", port=8501, debug=False):
    """Executa o dashboard Streamlit"""
    print(f"\n🚀 Executando dashboard...")
    print(f"🌐 URL: http://{host}:{port}")
    
    cmd = [
        "streamlit", "run", "dashboard_hibrido.py",
        "--server.port", str(port),
        "--server.address", host
    ]
    
    if debug:
        cmd.append("--logger.level=debug")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard interrompido pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar dashboard: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Executa o dashboard híbrido")
    parser.add_argument("--host", default="localhost", help="Host do servidor")
    parser.add_argument("--port", type=int, default=8501, help="Porta do servidor")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    parser.add_argument("--skip-checks", action="store_true", help="Pula verificações")
    
    args = parser.parse_args()
    
    print("🔮 DASHBOARD HÍBRIDO PYTHON + R")
    print("=" * 50)
    
    if not args.skip_checks:
        # Verifica dependências
        if not check_dependencies():
            print("\n❌ Dependências faltando. Execute com --skip-checks para pular verificações.")
            return 1
        
        # Verifica R
        if not check_r_installation():
            print("\n⚠️ R não encontrado. Análises espaciais podem não funcionar.")
            print("💡 Instale R: https://cran.r-project.org/")
        
        # Verifica dashboard
        if not check_dashboard_file():
            print("\n❌ Arquivo do dashboard não encontrado.")
            return 1
    
    # Executa dashboard
    print(f"\n🚀 Iniciando dashboard em http://{args.host}:{args.port}")
    print("💡 Pressione Ctrl+C para parar")
    
    success = run_dashboard(args.host, args.port, args.debug)
    
    if success:
        print("\n✅ Dashboard executado com sucesso!")
    else:
        print("\n❌ Erro ao executar dashboard")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

