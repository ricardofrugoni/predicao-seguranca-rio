#!/usr/bin/env Rscript
# Script para instalar dependências R do projeto
# Execute: Rscript install_r_dependencies.R

cat("🔧 Instalando dependências R para análise de violência...\n")

# Lista de pacotes necessários
packages <- c(
  # Análise espacial
  "sf",
  "sp",
  "spdep",
  "spatstat",
  
  # Análise estatística
  "tidyverse",
  "ggplot2",
  "dplyr",
  "tidyr",
  
  # Séries temporais
  "forecast",
  "tseries",
  
  # Integração Python
  "reticulate",
  
  # Visualização
  "leaflet",
  "mapview",
  
  # Análise de dados
  "corrplot",
  "cluster",
  "factoextra"
)

# Função para instalar pacotes
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE)) {
    cat("📦 Instalando", package, "...\n")
    install.packages(package, dependencies = TRUE)
  } else {
    cat("✅", package, "já instalado\n")
  }
}

# Instala pacotes
cat("📋 Verificando e instalando pacotes...\n")
for (pkg in packages) {
  tryCatch({
    install_if_missing(pkg)
  }, error = function(e) {
    cat("❌ Erro ao instalar", pkg, ":", e$message, "\n")
  })
}

# Verifica instalação
cat("\n🔍 Verificando instalação...\n")
missing_packages <- c()

for (pkg in packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    missing_packages <- c(missing_packages, pkg)
  }
}

if (length(missing_packages) == 0) {
  cat("✅ Todos os pacotes instalados com sucesso!\n")
} else {
  cat("❌ Pacotes não instalados:", paste(missing_packages, collapse = ", "), "\n")
  cat("💡 Tente instalar manualmente:\n")
  for (pkg in missing_packages) {
    cat("  install.packages('", pkg, "')\n", sep = "")
  }
}

# Testa funcionalidades básicas
cat("\n🧪 Testando funcionalidades...\n")

tryCatch({
  library(sf)
  cat("✅ sf: Análise espacial\n")
}, error = function(e) {
  cat("❌ sf: Erro -", e$message, "\n")
})

tryCatch({
  library(spdep)
  cat("✅ spdep: Análise de dependência espacial\n")
}, error = function(e) {
  cat("❌ spdep: Erro -", e$message, "\n")
})

tryCatch({
  library(forecast)
  cat("✅ forecast: Séries temporais\n")
}, error = function(e) {
  cat("❌ forecast: Erro -", e$message, "\n")
})

tryCatch({
  library(reticulate)
  cat("✅ reticulate: Integração Python\n")
}, error = function(e) {
  cat("❌ reticulate: Erro -", e$message, "\n")
})

cat("\n🎉 Instalação concluída!\n")
cat("📌 Próximos passos:\n")
cat("1. Execute o notebook 01_coleta_dados.ipynb\n")
cat("2. Execute o notebook 02_eda_python.ipynb\n")
cat("3. Execute o notebook 03_analise_espacial.Rmd\n")
cat("4. Execute o dashboard: streamlit run dashboard_hibrido.py\n")
