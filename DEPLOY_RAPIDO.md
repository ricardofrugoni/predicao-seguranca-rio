# 🚀 DEPLOY RÁPIDO - GitHub + Streamlit Cloud

## ⚡ Deploy em 5 minutos

### 1️⃣ Preparar Local
```bash
# Windows
deploy_commands.bat

# Linux/Mac
chmod +x deploy_commands.sh
./deploy_commands.sh
```

### 2️⃣ Criar Repositório GitHub
1. Acesse: https://github.com/new
2. **Nome**: `violencia-rio-analise-preditiva`
3. **Descrição**: `Sistema de análise preditiva de violência no Rio de Janeiro`
4. **Visibilidade**: Public
5. **Initialize**: ❌ NÃO marque
6. Clique **"Create repository"**

### 3️⃣ Conectar ao GitHub
```bash
git remote add origin https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva.git
git branch -M main
git push -u origin main
```

### 4️⃣ Deploy Streamlit Cloud
1. Acesse: https://streamlit.io/cloud
2. **Repository**: `violencia-rio-analise-preditiva`
3. **Main file**: `Home.py`
4. Clique **"Deploy!"**

### 5️⃣ Pronto! 🎉
Sua aplicação estará em:
```
https://violencia-rio-analise-preditiva.streamlit.app
```

## 🔄 Atualizações Futuras
```bash
# Fazer mudanças nos arquivos
# ...

# Deploy automático
git add .
git commit -m "Atualização"
git push origin main
# Streamlit Cloud atualiza automaticamente!
```

## 🆘 Problemas Comuns

### ❌ "Git não encontrado"
**Windows**: Baixe em https://git-scm.com/
**Linux**: `sudo apt-get install git`
**Mac**: `brew install git`

### ❌ "Repository not found"
Verifique se o repositório foi criado no GitHub

### ❌ "Streamlit Cloud error"
Verifique se o arquivo `Home.py` existe na raiz

### ❌ "Dependencies error"
Adicione dependências em `requirements_hibrido.txt`

## 📞 Suporte
- **GitHub Issues**: Para bugs
- **Streamlit Community**: Para dúvidas
- **Documentação**: README.md

---

**🚀 Deploy realizado com sucesso!**
