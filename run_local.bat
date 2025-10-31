@echo off
echo ========================================
echo   Iniciando Streamlit - Violencia RJ
echo ========================================
echo.

cd /d "%~dp0"
echo Diretorio: %cd%
echo.

echo Verificando Python...
python --version
echo.

echo Verificando Streamlit...
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
echo.

echo Iniciando aplicacao...
echo Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar
echo.

python -m streamlit run Home.py --server.port 8501 --server.headless false

pause

