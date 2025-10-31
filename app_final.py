"""
🔄 REDIRECIONAMENTO PARA NOVA ESTRUTURA POO
==========================================

Este arquivo mantém compatibilidade com o Streamlit Cloud
que está configurado para usar app_final.py como main file.

A nova estrutura usa Home.py com arquitetura POO.
"""

# Importa e executa o novo Home.py
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importa e executa o módulo Home
import runpy
runpy.run_module('Home', run_name='__main__')

