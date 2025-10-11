#!/bin/bash
# Script de instalação do R e dependências
# Para Streamlit Cloud e ambientes Linux

echo "🔧 Instalando R e dependências..."

# Atualiza sistema
sudo apt-get update

# Instala R
sudo apt-get install -y r-base r-base-dev

# Instala dependências do sistema
sudo apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgdal-dev \
    libproj-dev \
    libgeos-dev

# Instala pacotes R
echo "📦 Instalando pacotes R..."
Rscript -e "
install.packages(c(
    'forecast',
    'sf',
    'spdep',
    'spatstat',
    'jsonlite',
    'tidyverse',
    'ggplot2',
    'dplyr',
    'tidyr',
    'corrplot',
    'cluster',
    'factoextra'
), repos='https://cran.r-project.org/')
"

echo "✅ Instalação do R concluída!"
