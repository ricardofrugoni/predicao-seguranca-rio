"""
Script para configurar o ambiente Python e instalar todas as dependências
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"⚠️ {description} - AVISO")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("="*60)
    print("🚀 CONFIGURAÇÃO DO AMBIENTE - ANÁLISE DE VIOLÊNCIA RJ")
    print("="*60)
    
    # 1. Verificar versão do Python
    print(f"\n📌 Python: {sys.version}")
    
    # 2. Atualizar pip
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Atualizando pip"
    )
    
    # 3. Instalar dependências
    run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Instalando dependências do projeto"
    )
    
    # 4. Verificar instalação
    print("\n" + "="*60)
    print("🔍 VERIFICANDO INSTALAÇÃO")
    print("="*60)
    
    libs_to_check = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "plotly",
        "folium",
        "sklearn",
        "xgboost",
        "statsmodels",
        "prophet",
        "geopandas",
        "shapely",
        "requests",
        "tqdm",
        "streamlit"
    ]
    
    for lib in libs_to_check:
        try:
            __import__(lib)
            print(f"✅ {lib:20} instalado")
        except ImportError:
            print(f"❌ {lib:20} NÃO instalado")
    
    print("\n" + "="*60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📝 Próximos passos:")
    print("  1. Execute: streamlit run Home.py")
    print("  2. Ou abra os notebooks em: notebooks/")
    print("\n")

if __name__ == "__main__":
    main()




