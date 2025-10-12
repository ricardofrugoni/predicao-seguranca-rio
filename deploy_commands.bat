@echo off
REM Script de deploy para Windows
REM Sistema de Análise Preditiva - Rio de Janeiro

echo 🚀 DEPLOY AUTOMATIZADO PARA GITHUB
echo ===================================
echo.

REM Verifica se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado. Instale primeiro: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git encontrado
echo.

REM Verifica se é um repositório Git
if not exist ".git" (
    echo 📁 Inicializando repositório Git...
    git init
    if %errorlevel% neq 0 (
        echo ❌ Erro ao inicializar Git
        pause
        exit /b 1
    )
    echo ✅ Repositório Git inicializado
) else (
    echo ✅ Repositório Git já existe
)

echo.

REM Adiciona arquivos
echo 📦 Adicionando arquivos...
git add .
if %errorlevel% neq 0 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)

echo ✅ Arquivos adicionados
echo.

REM Commit
echo 💾 Fazendo commit...
git commit -m "Sistema completo de análise preditiva de violência - Rio de Janeiro"
if %errorlevel% neq 0 (
    echo ❌ Erro no commit
    pause
    exit /b 1
)

echo ✅ Commit realizado
echo.

REM Instruções
echo 🌐 PRÓXIMOS PASSOS:
echo ==================
echo.
echo 1. Acesse: https://github.com/new
echo 2. Repository name: violencia-rio-analise-preditiva
echo 3. Description: Sistema de análise preditiva de violência no Rio de Janeiro
echo 4. Visibility: Public
echo 5. Initialize: ❌ NÃO marque nenhuma opção
echo 6. Clique em 'Create repository'
echo.
echo 7. Após criar, execute:
echo    git remote add origin https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 8. Para Streamlit Cloud:
echo    Acesse: https://streamlit.io/cloud
echo    Repository: violencia-rio-analise-preditiva
echo    Main file: Home.py
echo.

REM Abre GitHub no navegador
echo 🌐 Abrindo GitHub...
start https://github.com/new

echo.
echo ✅ Configuração local concluída!
echo 💡 Siga as instruções acima para completar o deploy
echo.
pause


