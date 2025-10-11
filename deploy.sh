#!/bin/bash
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
