#!/bin/bash
# Script de deploy para Linux/Mac
# Sistema de Análise Preditiva - Rio de Janeiro

echo "🚀 DEPLOY AUTOMATIZADO PARA GITHUB"
echo "==================================="
echo

# Verifica se Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Instale primeiro:"
    echo "   Ubuntu/Debian: sudo apt-get install git"
    echo "   Mac: brew install git"
    exit 1
fi

echo "✅ Git encontrado"
echo

# Verifica se é um repositório Git
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao inicializar Git"
        exit 1
    fi
    echo "✅ Repositório Git inicializado"
else
    echo "✅ Repositório Git já existe"
fi

echo

# Adiciona arquivos
echo "📦 Adicionando arquivos..."
git add .
if [ $? -ne 0 ]; then
    echo "❌ Erro ao adicionar arquivos"
    exit 1
fi

echo "✅ Arquivos adicionados"
echo

# Commit
echo "💾 Fazendo commit..."
git commit -m "Sistema completo de análise preditiva de violência - Rio de Janeiro"
if [ $? -ne 0 ]; then
    echo "❌ Erro no commit"
    exit 1
fi

echo "✅ Commit realizado"
echo

# Instruções
echo "🌐 PRÓXIMOS PASSOS:"
echo "=================="
echo
echo "1. Acesse: https://github.com/new"
echo "2. Repository name: violencia-rio-analise-preditiva"
echo "3. Description: Sistema de análise preditiva de violência no Rio de Janeiro"
echo "4. Visibility: Public"
echo "5. Initialize: ❌ NÃO marque nenhuma opção"
echo "6. Clique em 'Create repository'"
echo
echo "7. Após criar, execute:"
echo "   git remote add origin https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo
echo "8. Para Streamlit Cloud:"
echo "   Acesse: https://streamlit.io/cloud"
echo "   Repository: violencia-rio-analise-preditiva"
echo "   Main file: Home.py"
echo

# Abre GitHub no navegador
echo "🌐 Abrindo GitHub..."
if command -v xdg-open &> /dev/null; then
    xdg-open https://github.com/new
elif command -v open &> /dev/null; then
    open https://github.com/new
else
    echo "💡 Abra manualmente: https://github.com/new"
fi

echo
echo "✅ Configuração local concluída!"
echo "💡 Siga as instruções acima para completar o deploy"
echo



