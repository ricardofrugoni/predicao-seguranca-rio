# 🔧 CONFIGURAR GITHUB - Passo a Passo

## ⚠️ IMPORTANTE: Substitua "SEU-USUARIO" pelo seu nome de usuário do GitHub

### 1️⃣ Criar Repositório no GitHub

1. **Acesse**: https://github.com/new
2. **Repository name**: `violencia-rio-analise-preditiva`
3. **Description**: `Sistema de análise preditiva de violência no Rio de Janeiro`
4. **Visibility**: Public
5. **Initialize**: ❌ NÃO marque nenhuma opção
6. **Clique**: "Create repository"

### 2️⃣ Configurar Remote (Substitua SEU-USUARIO)

```bash
# Remover remote atual (se existir)
git remote remove origin

# Adicionar seu repositório (SUBSTITUA SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva.git

# Verificar se está correto
git remote -v
```

### 3️⃣ Fazer Push

```bash
# Renomear branch para main
git branch -M main

# Fazer push
git push -u origin main
```

### 4️⃣ Verificar no GitHub

- Acesse: https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva
- Verifique se todos os arquivos estão lá

### 5️⃣ Deploy no Streamlit Cloud

1. **Acesse**: https://streamlit.io/cloud
2. **Repository**: `violencia-rio-analise-preditiva`
3. **Main file**: `Home.py`
4. **Deploy!**

## 🆘 Problemas Comuns

### ❌ "Repository not found"
- Verifique se o repositório foi criado no GitHub
- Confirme o nome de usuário correto

### ❌ "Authentication failed"
- Configure suas credenciais do GitHub
- Use token de acesso pessoal se necessário

### ❌ "Permission denied"
- Verifique se você tem permissão no repositório
- Confirme se é o dono do repositório

## 📞 Suporte

Se tiver problemas, me informe:
1. Seu nome de usuário do GitHub
2. Se o repositório foi criado
3. Qual erro está aparecendo

---

**🚀 Após configurar, seu sistema estará online!**
