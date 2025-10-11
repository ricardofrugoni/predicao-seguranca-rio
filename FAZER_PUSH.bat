@echo off
REM Script para fazer push do projeto para o GitHub
REM Sistema de Análise Preditiva - Rio de Janeiro

echo 🚀 FAZER PUSH PARA GITHUB
echo =========================
echo.

REM Solicita nome de usuário
set /p USERNAME="Digite seu nome de usuário do GitHub: "

echo.
echo 🔍 Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado. Instale primeiro: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git encontrado
echo.

echo 📦 Adicionando mudanças...
git add .
if %errorlevel% neq 0 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)

echo ✅ Arquivos adicionados
echo.

echo 💾 Fazendo commit...
git commit -m "Sistema completo de análise preditiva de violência - Rio de Janeiro"
if %errorlevel% neq 0 (
    echo ❌ Erro no commit
    pause
    exit /b 1
)

echo ✅ Commit realizado
echo.

echo 🔗 Configurando remote...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%USERNAME%/violencia-rio-analise-preditiva.git
if %errorlevel% neq 0 (
    echo ❌ Erro ao configurar remote
    pause
    exit /b 1
)

echo ✅ Remote configurado
echo.

echo 🚀 Fazendo push...
git branch -M main
git push -u origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no push
    echo.
    echo 💡 Possíveis soluções:
    echo 1. Verifique se o repositório foi criado no GitHub
    echo 2. Confirme se o nome de usuário está correto
    echo 3. Verifique suas credenciais do GitHub
    echo.
    echo 📋 Crie o repositório em: https://github.com/new
    echo    Nome: violencia-rio-analise-preditiva
    echo    Descrição: Sistema de análise preditiva de violência no Rio de Janeiro
    echo    Visibility: Public
    echo    Initialize: ❌ NÃO marque nenhuma opção
    echo.
    pause
    exit /b 1
)

echo ✅ Push realizado com sucesso!
echo.

echo 🎉 DEPLOY CONCLUÍDO!
echo ===================
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Verifique no GitHub:
echo    https://github.com/%USERNAME%/violencia-rio-analise-preditiva
echo.
echo 2. Deploy no Streamlit Cloud:
echo    https://streamlit.io/cloud
echo    Repository: violencia-rio-analise-preditiva
echo    Main file: Home.py
echo.
echo 3. Sua aplicação estará em:
echo    https://violencia-rio-analise-preditiva.streamlit.app
echo.

REM Abre GitHub no navegador
echo 🌐 Abrindo GitHub...
start https://github.com/%USERNAME%/violencia-rio-analise-preditiva

echo.
echo ✅ Sistema pronto para deploy!
pause
