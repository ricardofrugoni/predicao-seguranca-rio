# 🚀 DEPLOY NO GITHUB - Guia Completo

Guia passo a passo para fazer deploy do Sistema de Análise Preditiva no GitHub e Streamlit Cloud.

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Git instalado
- ✅ Projeto funcionando localmente
- ✅ Conta no Streamlit Cloud (gratuita)

## 🔧 Passo 1: Preparar o Repositório Local

### 1.1 Inicializar Git (se não foi feito)
```bash
cd "C:\Users\frugo\Desktop\Ricardo\Projetos\ML\Violência no Mun Rio de Janeiro\projeto_violencia_rj"
git init
```

### 1.2 Configurar Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 1.3 Adicionar arquivos
```bash
git add .
git commit -m "Sistema completo de análise preditiva de violência - Rio de Janeiro"
```

## 🌐 Passo 2: Criar Repositório no GitHub

### 2.1 Acesse GitHub
- Vá para: https://github.com
- Faça login na sua conta

### 2.2 Criar novo repositório
1. Clique em **"New repository"** (botão verde)
2. **Repository name**: `violencia-rio-analise-preditiva`
3. **Description**: `Sistema de análise preditiva de violência no Rio de Janeiro com Python + R`
4. **Visibility**: Public (para Streamlit Cloud gratuito)
5. **Initialize**: ❌ NÃO marque nenhuma opção
6. Clique em **"Create repository"**

### 2.3 Conectar repositório local
```bash
git remote add origin https://github.com/SEU-USUARIO/violencia-rio-analise-preditiva.git
git branch -M main
git push -u origin main
```

## 🚀 Passo 3: Deploy no Streamlit Cloud

### 3.1 Acessar Streamlit Cloud
- Vá para: https://streamlit.io/cloud
- Clique em **"Sign in with GitHub"**
- Autorize o acesso

### 3.2 Criar nova aplicação
1. Clique em **"New app"**
2. **Repository**: Selecione `violencia-rio-analise-preditiva`
3. **Branch**: `main`
4. **Main file path**: `Home.py`
5. **App URL**: `violencia-rio-analise-preditiva` (será gerado automaticamente)

### 3.3 Configurações avançadas (opcional)
```yaml
# streamlit/config.toml (criar se necessário)
[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false
```

### 3.4 Deploy
- Clique em **"Deploy!"**
- Aguarde a compilação (2-5 minutos)
- Sua aplicação estará disponível em: `https://violencia-rio-analise-preditiva.streamlit.app`

## 🔧 Passo 4: Configurações Específicas

### 4.1 Arquivo de configuração Streamlit
Crie o arquivo `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### 4.2 Arquivo de secrets (se necessário)
Crie `.streamlit/secrets.toml` para variáveis sensíveis:

```toml
# Exemplo de secrets
[api_keys]
isp_rj = "sua_chave_aqui"
ibge = "sua_chave_aqui"

[database]
url = "sua_url_aqui"
```

## 📝 Passo 5: Documentação do Repositório

### 5.1 README.md (já criado)
O arquivo README.md já está completo com:
- ✅ Instruções de instalação
- ✅ Guia de uso
- ✅ Documentação dos modelos
- ✅ Exemplos práticos
- ✅ Troubleshooting

### 5.2 Adicionar badges
Adicione no topo do README.md:

```markdown
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://violencia-rio-analise-preditiva.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)](https://r-project.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
```

## 🔄 Passo 6: Atualizações Futuras

### 6.1 Fazer mudanças
```bash
# Editar arquivos
# ...

# Commit das mudanças
git add .
git commit -m "Descrição da mudança"
git push origin main
```

### 6.2 Streamlit Cloud atualiza automaticamente
- O Streamlit Cloud detecta mudanças automaticamente
- Redeploy acontece em 1-2 minutos
- Não é necessário fazer nada manual

## 🛠️ Passo 7: Troubleshooting

### 7.1 Erro de dependências
Se houver erro de instalação:
```bash
# Adicione ao requirements_hibrido.txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
# ... outras dependências
```

### 7.2 Erro de R
Se R não funcionar no Streamlit Cloud:
- Adicione `packages.txt` com dependências do sistema
- Use apenas análises Python
- R é opcional para o funcionamento básico

### 7.3 Erro de memória
Se houver erro de memória:
- Reduza o tamanho dos dados
- Use cache mais agressivo
- Desative modelos pesados (LSTM)

### 7.4 Logs de erro
Para ver logs detalhados:
1. Acesse o Streamlit Cloud
2. Clique na sua aplicação
3. Vá para "Logs"
4. Verifique erros específicos

## 📊 Passo 8: Monitoramento

### 8.1 Métricas do Streamlit Cloud
- **Uptime**: Disponível 24/7
- **Performance**: Monitoramento automático
- **Logs**: Acesso completo aos logs

### 8.2 Analytics (opcional)
Adicione Google Analytics:
```python
# No Home.py, adicione:
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

## 🎯 Passo 9: Compartilhamento

### 9.1 URL da aplicação
```
https://violencia-rio-analise-preditiva.streamlit.app
```

### 9.2 Compartilhar no LinkedIn
```
🔮 Sistema de Análise Preditiva de Violência no Rio de Janeiro

✅ 8 modelos de Machine Learning
✅ Análises espaciais avançadas
✅ Dashboard interativo
✅ Python + R híbrido

Acesse: https://violencia-rio-analise-preditiva.streamlit.app

#DataScience #MachineLearning #Python #R #ViolenceAnalysis #RioDeJaneiro
```

### 9.3 Compartilhar no Twitter
```
🚀 Sistema completo de análise preditiva de violência no Rio de Janeiro!

✅ 8 modelos ML (ARIMA, Prophet, XGBoost, LSTM...)
✅ Análises espaciais com R
✅ Dashboard Streamlit profissional
✅ Deploy automático

🔗 https://violencia-rio-analise-preditiva.streamlit.app

#DataScience #ML #Python #R
```

## ✅ Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Código enviado para GitHub
- [ ] Streamlit Cloud configurado
- [ ] Aplicação funcionando online
- [ ] README.md atualizado
- [ ] Badges adicionados
- [ ] URL compartilhada
- [ ] Testes realizados

## 🎉 Pronto!

Seu sistema estará disponível publicamente em:
**https://violencia-rio-analise-preditiva.streamlit.app**

### 📞 Suporte
- **GitHub Issues**: Para bugs e melhorias
- **Streamlit Community**: Para dúvidas sobre Streamlit
- **Documentação**: README.md completo

---

**🚀 Deploy realizado com sucesso!**
