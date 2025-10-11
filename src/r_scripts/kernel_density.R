#!/usr/bin/env Rscript
# Script R para Kernel Density Estimation (PESADA)
# Executado via subprocess do Python

# Carrega bibliotecas
suppressMessages({
  library(sf)
  library(spatstat)
  library(jsonlite)
})

# Argumentos da linha de comando
args <- commandArgs(trailingOnly = TRUE)
points_geojson <- args[1]
output_path <- args[2]
bandwidth <- args[3]

cat("🔍 Iniciando Kernel Density Estimation...\n")
cat("📁 Pontos:", points_geojson, "\n")
cat("📊 Bandwidth:", bandwidth, "\n")

# Carrega dados de pontos
tryCatch({
  points_sf <- st_read(points_geojson, quiet = TRUE)
  cat("✅ Pontos carregados:", nrow(points_sf), "registros\n")
}, error = function(e) {
  cat("❌ Erro ao carregar pontos:", e$message, "\n")
  quit(status = 1)
})

# Extrai coordenadas
coords <- st_coordinates(points_sf)
cat("📍 Coordenadas extraídas:", nrow(coords), "pontos\n")

# Cria objeto ppp
tryCatch({
  # Define janela
  x_range <- range(coords[,1])
  y_range <- range(coords[,2])
  
  # Adiciona margem
  margin <- 0.1
  x_margin <- (x_range[2] - x_range[1]) * margin
  y_margin <- (y_range[2] - y_range[1]) * margin
  
  window <- owin(
    xrange = c(x_range[1] - x_margin, x_range[2] + x_margin),
    yrange = c(y_range[1] - y_margin, y_range[2] + y_margin)
  )
  
  # Cria objeto ppp
  crime_ppp <- ppp(coords[,1], coords[,2], window = window)
  
  cat("✅ Objeto ppp criado\n")
}, error = function(e) {
  cat("❌ Erro ao criar ppp:", e$message, "\n")
  quit(status = 1)
})

# Calcula KDE
tryCatch({
  if (bandwidth == "auto") {
    # Calcula bandwidth automático
    sigma <- bw.diggle(crime_ppp)
    cat("📊 Bandwidth automático:", sigma, "\n")
  } else {
    sigma <- as.numeric(bandwidth)
    cat("📊 Bandwidth fixo:", sigma, "\n")
  }
  
  # Executa KDE
  kde_result <- density(crime_ppp, sigma = sigma)
  
  cat("✅ KDE calculado\n")
}, error = function(e) {
  cat("❌ Erro no KDE:", e$message, "\n")
  quit(status = 1)
})

# Identifica hotspots
tryCatch({
  # Calcula threshold para hotspots
  threshold_80 <- quantile(kde_result$v, 0.8, na.rm = TRUE)
  threshold_90 <- quantile(kde_result$v, 0.9, na.rm = TRUE)
  threshold_95 <- quantile(kde_result$v, 0.95, na.rm = TRUE)
  
  # Identifica hotspots
  hotspots_80 <- kde_result$v > threshold_80
  hotspots_90 <- kde_result$v > threshold_90
  hotspots_95 <- kde_result$v > threshold_95
  
  cat("🔥 Hotspots identificados:\n")
  cat("  - 80%:", sum(hotspots_80, na.rm = TRUE), "células\n")
  cat("  - 90%:", sum(hotspots_90, na.rm = TRUE), "células\n")
  cat("  - 95%:", sum(hotspots_95, na.rm = TRUE), "células\n")
}, error = function(e) {
  cat("❌ Erro na identificação de hotspots:", e$message, "\n")
  quit(status = 1)
})

# Prepara resultado
resultado <- list(
  bandwidth = sigma,
  n_points = nrow(coords),
  x_range = x_range,
  y_range = y_range,
  kde_summary = list(
    min = min(kde_result$v, na.rm = TRUE),
    max = max(kde_result$v, na.rm = TRUE),
    mean = mean(kde_result$v, na.rm = TRUE),
    median = median(kde_result$v, na.rm = TRUE)
  ),
  thresholds = list(
    threshold_80 = threshold_80,
    threshold_90 = threshold_90,
    threshold_95 = threshold_95
  ),
  hotspots_count = list(
    hotspots_80 = sum(hotspots_80, na.rm = TRUE),
    hotspots_90 = sum(hotspots_90, na.rm = TRUE),
    hotspots_95 = sum(hotspots_95, na.rm = TRUE)
  ),
  kde_data = list(
    x = kde_result$x,
    y = kde_result$y,
    z = kde_result$v
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

cat("🎉 Kernel Density Estimation concluída com sucesso!\n")
