#!/usr/bin/env python3
"""
🚀 PUSH PARA GITHUB - Script Personalizado
==========================================

Script para fazer push do projeto para o GitHub com seu nome de usuário.

Uso:
    python push_github.py --username SEU-USUARIO
    python push_github.py --username rfrugoni
"""

import subprocess
import sys
import argparse
import webbrowser

def print_header():
    """Imprime cabeçalho"""
    print("🚀 PUSH PARA GITHUB")
    print("Sistema de Análise Preditiva - Rio de Janeiro")
    print("=" * 50)
    print()

def check_git_status():
    """Verifica status do Git"""
    print("🔍 Verificando status do Git...")
    
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git funcionando")
            return True
        else:
            print("❌ Erro no Git")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def add_and_commit():
    """Adiciona e faz commit das mudanças"""
    print("📦 Adicionando mudanças...")
    
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Arquivos adicionados")
        
        subprocess.run([
            'git', 'commit', '-m', 
            'Sistema completo de análise preditiva de violência - Rio de Janeiro'
        ], check=True)
        print("✅ Commit realizado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no commit: {e}")
        return False

def configure_remote(username):
    """Configura remote do GitHub"""
    print(f"🔗 Configurando remote para {username}...")
    
    try:
        # Remove remote atual se existir
        subprocess.run(['git', 'remote', 'remove', 'origin'], 
                      capture_output=True)
        
        # Adiciona novo remote
        remote_url = f"https://github.com/{username}/violencia-rio-analise-preditiva.git"
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        
        print(f"✅ Remote configurado: {remote_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar remote: {e}")
        return False

def push_to_github():
    """Faz push para o GitHub"""
    print("🚀 Fazendo push para o GitHub...")
    
    try:
        # Renomeia branch para main
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("✅ Branch renomeada para main")
        
        # Faz push
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ Push realizado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no push: {e}")
        print("\n💡 Possíveis soluções:")
        print("1. Verifique se o repositório foi criado no GitHub")
        print("2. Confirme se o nome de usuário está correto")
        print("3. Verifique suas credenciais do GitHub")
        return False

def show_next_steps(username):
    """Mostra próximos passos"""
    print("\n" + "=" * 50)
    print("🎉 PUSH REALIZADO COM SUCESSO!")
    print("=" * 50)
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print()
    print("1. Verifique no GitHub:")
    print(f"   https://github.com/{username}/violencia-rio-analise-preditiva")
    print()
    print("2. Deploy no Streamlit Cloud:")
    print("   https://streamlit.io/cloud")
    print("   Repository: violencia-rio-analise-preditiva")
    print("   Main file: Home.py")
    print()
    print("3. Sua aplicação estará em:")
    print(f"   https://seguranca-rio-preditiva.streamlit.app")
    print()
    
    # Abre GitHub no navegador
    try:
        webbrowser.open(f"https://github.com/{username}/violencia-rio-analise-preditiva")
        print("🌐 Abrindo GitHub no navegador...")
    except:
        print("💡 Abra manualmente o GitHub")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Push para GitHub")
    parser.add_argument("--username", required=True, 
                       help="Seu nome de usuário do GitHub")
    parser.add_argument("--skip-commit", action="store_true",
                       help="Pular commit (apenas push)")
    
    args = parser.parse_args()
    
    print_header()
    
    # Verificações
    if not check_git_status():
        return 1
    
    # Commit (se não pular)
    if not args.skip_commit:
        if not add_and_commit():
            return 1
    
    # Configurar remote
    if not configure_remote(args.username):
        return 1
    
    # Push
    if not push_to_github():
        return 1
    
    # Próximos passos
    show_next_steps(args.username)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
