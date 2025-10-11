#!/usr/bin/env Rscript
# Script R para análise de Moran (PESADA)
# Executado via subprocess do Python

# Carrega bibliotecas
suppressMessages({
  library(sf)
  library(spdep)
  library(jsonlite)
})

# Argumentos da linha de comando
args <- commandArgs(trailingOnly = TRUE)
geodata_path <- args[1]
output_path <- args[2]
column_name <- args[3]
k_neighbors <- as.numeric(args[4])

cat("🔍 Iniciando análise de Moran...\n")
cat("📁 Dados:", geodata_path, "\n")
cat("📊 Coluna:", column_name, "\n")
cat("🔗 Vizinhos:", k_neighbors, "\n")

# Carrega dados geoespaciais
tryCatch({
  crimes_sf <- st_read(geodata_path, quiet = TRUE)
  cat("✅ Dados carregados:", nrow(crimes_sf), "registros\n")
}, error = function(e) {
  cat("❌ Erro ao carregar dados:", e$message, "\n")
  quit(status = 1)
})

# Verifica se a coluna existe
if (!column_name %in% names(crimes_sf)) {
  cat("❌ Coluna", column_name, "não encontrada\n")
  quit(status = 1)
}

# Remove valores faltantes
crimes_clean <- crimes_sf[!is.na(crimes_sf[[column_name]]), ]
cat("🧹 Dados limpos:", nrow(crimes_clean), "registros\n")

if (nrow(crimes_clean) < 3) {
  cat("❌ Poucos dados para análise espacial\n")
  quit(status = 1)
}

# Cria matriz de vizinhança
tryCatch({
  # Converte para formato sp
  crimes_sp <- as(crimes_clean, "Spatial")
  
  # Cria matriz de vizinhança
  nb <- poly2nb(crimes_sp, queen = TRUE)
  listw <- nb2listw(nb, style = "W")
  
  cat("✅ Matriz de vizinhança criada\n")
}, error = function(e) {
  cat("❌ Erro na matriz de vizinhança:", e$message, "\n")
  quit(status = 1)
})

# Análise de Moran Global
tryCatch({
  moran_global <- moran.test(crimes_clean[[column_name]], listw)
  
  cat("📊 Moran's I Global:", moran_global$estimate[1], "\n")
  cat("📊 P-valor:", moran_global$p.value, "\n")
}, error = function(e) {
  cat("❌ Erro no Moran Global:", e$message, "\n")
  quit(status = 1)
})

# Análise de Moran Local (LISA)
tryCatch({
  moran_local <- localmoran(crimes_clean[[column_name]], listw)
  
  # Adiciona resultados aos dados
  crimes_clean$moran_i <- moran_local[,1]
  crimes_clean$moran_p <- moran_local[,5]
  crimes_clean$moran_z <- moran_local[,4]
  
  # Classifica padrões LISA
  crimes_clean$lisa_pattern <- "Não significativo"
  crimes_clean$lisa_pattern[crimes_clean$moran_i > 0 & crimes_clean$moran_z > 1.96] <- "Alto-Alto"
  crimes_clean$lisa_pattern[crimes_clean$moran_i > 0 & crimes_clean$moran_z < -1.96] <- "Baixo-Baixo"
  crimes_clean$lisa_pattern[crimes_clean$moran_i < 0 & crimes_clean$moran_z > 1.96] <- "Alto-Baixo"
  crimes_clean$lisa_pattern[crimes_clean$moran_i < 0 & crimes_clean$moran_z < -1.96] <- "Baixo-Alto"
  
  cat("✅ Moran Local calculado\n")
}, error = function(e) {
  cat("❌ Erro no Moran Local:", e$message, "\n")
  quit(status = 1)
})

# Prepara resultado
resultado <- list(
  moran_i = moran_global$estimate[1],
  p_value = moran_global$p.value,
  statistic = moran_global$statistic,
  n_regions = nrow(crimes_clean),
  lisa_patterns = table(crimes_clean$lisa_pattern),
  data = list(
    moran_i_values = crimes_clean$moran_i,
    moran_p_values = crimes_clean$moran_p,
    lisa_patterns = crimes_clean$lisa_pattern
  )
)

# Salva resultado
tryCatch({
  write_json(resultado, output_path, pretty = TRUE)
  cat("✅ Resultado salvo em:", output_path, "\n")
}, error = function(e) {
  cat("❌ Erro ao salvar:", e$message, "\n")
  quit(status = 1)
})

cat("🎉 Análise de Moran concluída com sucesso!\n")
