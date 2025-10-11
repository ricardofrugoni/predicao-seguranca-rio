# Análise Espacial Avançada - Violência no Rio de Janeiro
# Módulo R para análises espaciais complexas

# Carrega bibliotecas necessárias
library(sf)
library(sp)
library(tidyverse)
library(ggplot2)
library(spatstat)
library(spdep)
library(GWmodel)
library(mapview)
library(viridis)
library(RColorBrewer)
library(classInt)
library(leaflet)
library(htmlwidgets)

# Configuração de diretórios
base_dir <- "."
data_dir <- file.path(base_dir, "data")
processed_dir <- file.path(data_dir, "processed")
output_dir <- file.path(base_dir, "outputs", "figures")

# Cria diretório de saída se não existir
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

#' Análise de Kernel Density Estimation (KDE)
#' 
#' @param crimes_sf Objeto sf com dados de crimes
#' @param variable Variável para análise
#' @param bandwidth Largura de banda para KDE
#' @return Lista com resultados do KDE
analyze_kde <- function(crimes_sf, variable = "taxa_100k", bandwidth = 1000) {
  cat("🔍 Iniciando análise KDE...\n")
  
  # Extrai coordenadas dos centroides
  centroids <- st_centroid(crimes_sf)
  coords <- st_coordinates(centroids)
  
  # Cria objeto ppp
  crime_ppp <- ppp(coords[,1], coords[,2], 
                   window = owin(range(coords[,1]), range(coords[,2])))
  
  # Calcula KDE
  kde_result <- density(crime_ppp, sigma = bandwidth)
  
  # Identifica hotspots
  hotspots <- identify_hotspots(kde_result, threshold = 0.8)
  
  return(list(
    kde = kde_result,
    hotspots = hotspots,
    bandwidth = bandwidth
  ))
}

#' Identifica hotspots baseado em KDE
#' 
#' @param kde_result Resultado do KDE
#' @param threshold Limiar para identificação de hotspots
#' @return Lista com hotspots identificados
identify_hotspots <- function(kde_result, threshold = 0.8) {
  # Calcula percentil para threshold
  threshold_value <- quantile(kde_result$v, threshold, na.rm = TRUE)
  
  # Identifica áreas acima do threshold
  hotspots <- kde_result$v > threshold_value
  
  return(list(
    threshold_value = threshold_value,
    hotspots_mask = hotspots,
    n_hotspots = sum(hotspots, na.rm = TRUE)
  ))
}

#' Análise de Índice de Moran
#' 
#' @param crimes_sf Objeto sf com dados
#' @param variable Variável para análise
#' @param style Estilo da matriz de pesos ("W", "B", "C", "U", "S")
#' @return Lista com resultados do Moran
analyze_moran <- function(crimes_sf, variable = "taxa_100k", style = "W") {
  cat("🔍 Iniciando análise de Moran...\n")
  
  # Cria matriz de vizinhança
  nb <- poly2nb(crimes_sf, queen = TRUE)
  listw <- nb2listw(nb, style = style)
  
  # Índice de Moran Global
  moran_global <- moran.test(crimes_sf[[variable]], listw)
  
  # Índice de Moran Local (LISA)
  moran_local <- localmoran(crimes_sf[[variable]], listw)
  
  # Adiciona resultados aos dados
  crimes_sf$moran_i <- moran_local[,1]
  crimes_sf$moran_p <- moran_local[,5]
  crimes_sf$moran_z <- moran_local[,4]
  
  # Classifica padrões LISA
  crimes_sf$lisa_pattern <- classify_lisa_patterns(crimes_sf$moran_i, crimes_sf$moran_z)
  
  return(list(
    global = moran_global,
    local = moran_local,
    data = crimes_sf,
    listw = listw
  ))
}

#' Classifica padrões LISA
#' 
#' @param moran_i Valores do Moran I local
#' @param moran_z Valores Z do Moran I local
#' @return Vetor com classificação dos padrões
classify_lisa_patterns <- function(moran_i, moran_z) {
  patterns <- rep("Não significativo", length(moran_i))
  
  # Alto-Alto
  patterns[moran_i > 0 & moran_z > 1.96] <- "Alto-Alto"
  
  # Baixo-Baixo
  patterns[moran_i > 0 & moran_z < -1.96] <- "Baixo-Baixo"
  
  # Alto-Baixo
  patterns[moran_i < 0 & moran_z > 1.96] <- "Alto-Baixo"
  
  # Baixo-Alto
  patterns[moran_i < 0 & moran_z < -1.96] <- "Baixo-Alto"
  
  return(patterns)
}

#' Análise de Nearest Neighbor
#' 
#' @param crimes_sf Objeto sf com dados
#' @return Lista com resultados da análise
analyze_nearest_neighbor <- function(crimes_sf) {
  cat("🔍 Iniciando análise de Nearest Neighbor...\n")
  
  # Extrai coordenadas
  coords <- st_coordinates(st_centroid(crimes_sf))
  
  # Cria objeto ppp
  crime_ppp <- ppp(coords[,1], coords[,2], 
                   window = owin(range(coords[,1]), range(coords[,2])))
  
  # Análise de distâncias
  nn_distances <- nndist(crime_ppp)
  
  # Teste de Clark-Evans
  clark_evans <- clarkevans.test(crime_ppp)
  
  # Teste de Hopkins
  hopkins <- hopkins.test(crime_ppp)
  
  return(list(
    nn_distances = nn_distances,
    clark_evans = clark_evans,
    hopkins = hopkins,
    mean_nn_distance = mean(nn_distances),
    sd_nn_distance = sd(nn_distances)
  ))
}

#' Regressão Geograficamente Ponderada (GWR)
#' 
#' @param crimes_sf Objeto sf com dados
#' @param formula Fórmula da regressão
#' @param bandwidth Largura de banda
#' @return Lista com resultados do GWR
analyze_gwr <- function(crimes_sf, formula, bandwidth = NULL) {
  cat("🔍 Iniciando análise GWR...\n")
  
  # Converte para formato sp
  crimes_sp <- as(crimes_sf, "Spatial")
  
  # Calcula largura de banda se não fornecida
  if (is.null(bandwidth)) {
    bandwidth <- bw.gwr(formula, data = crimes_sp, approach = "CV")
  }
  
  # Executa GWR
  gwr_model <- gwr.basic(formula, data = crimes_sp, bw = bandwidth)
  
  # Extrai resultados
  gwr_results <- gwr_model$SDF
  
  return(list(
    model = gwr_model,
    results = gwr_results,
    bandwidth = bandwidth,
    r_squared = gwr_model$GW.diagnostic$GWR_R2
  ))
}

#' Análise de Hotspots
#' 
#' @param crimes_sf Objeto sf com dados
#' @param variable Variável para análise
#' @param method Método de identificação ("quantile", "zscore", "moran")
#' @return Lista com hotspots identificados
analyze_hotspots <- function(crimes_sf, variable = "taxa_100k", method = "quantile") {
  cat("🔍 Iniciando análise de hotspots...\n")
  
  if (method == "quantile") {
    # Classificação por quartis
    crimes_sf$hotspot_level <- cut(crimes_sf[[variable]], 
                                  breaks = quantile(crimes_sf[[variable]], 
                                                   probs = c(0, 0.25, 0.5, 0.75, 1),
                                                   na.rm = TRUE),
                                  labels = c("Baixo", "Médio", "Alto", "Muito Alto"),
                                  include.lowest = TRUE)
    
  } else if (method == "zscore") {
    # Classificação por Z-score
    z_scores <- scale(crimes_sf[[variable]])
    crimes_sf$hotspot_level <- case_when(
      z_scores > 2 ~ "Muito Alto",
      z_scores > 1 ~ "Alto",
      z_scores > -1 ~ "Médio",
      z_scores > -2 ~ "Baixo",
      TRUE ~ "Muito Baixo"
    )
    
  } else if (method == "moran") {
    # Usa resultados do Moran I local
    crimes_sf$hotspot_level <- case_when(
      crimes_sf$moran_i > 0 & crimes_sf$moran_z > 1.96 ~ "Hotspot",
      crimes_sf$moran_i < 0 & crimes_sf$moran_z < -1.96 ~ "Coldspot",
      TRUE ~ "Não significativo"
    )
  }
  
  # Estatísticas por nível
  hotspot_stats <- crimes_sf %>%
    group_by(hotspot_level) %>%
    summarise(
      n_regioes = n(),
      taxa_media = mean(!!sym(variable), na.rm = TRUE),
      total_ocorrencias = sum(total_ocorrencias, na.rm = TRUE),
      .groups = 'drop'
    )
  
  return(list(
    data = crimes_sf,
    stats = hotspot_stats,
    method = method
  ))
}

#' Análise de Distâncias
#' 
#' @param crimes_sf Objeto sf com dados
#' @param reference_points Pontos de referência
#' @return Lista com análises de distância
analyze_distances <- function(crimes_sf, reference_points) {
  cat("🔍 Iniciando análise de distâncias...\n")
  
  # Converte pontos de referência para sf
  ref_sf <- st_as_sf(reference_points, coords = c("lon", "lat"), crs = 4326)
  ref_sf <- st_transform(ref_sf, st_crs(crimes_sf))
  
  # Calcula distâncias
  distances <- st_distance(crimes_sf, ref_sf)
  
  # Adiciona distâncias aos dados
  for (i in 1:nrow(ref_sf)) {
    crimes_sf[[paste0("dist_ref_", i)]] <- as.numeric(distances[,i])
  }
  
  # Distância média
  crimes_sf$dist_media <- rowMeans(distances)
  
  # Análise de correlação
  correlations <- cor(crimes_sf$taxa_100k, crimes_sf$dist_media, use = "complete.obs")
  
  return(list(
    data = crimes_sf,
    distances = distances,
    correlations = correlations
  ))
}

#' Cria visualizações espaciais
#' 
#' @param crimes_sf Objeto sf com dados
#' @param variable Variável para visualização
#' @param title Título do mapa
#' @return Objeto leaflet
create_spatial_map <- function(crimes_sf, variable = "taxa_100k", title = "Mapa Espacial") {
  # Cria paleta de cores
  pal <- colorNumeric(palette = "Reds", domain = crimes_sf[[variable]])
  
  # Cria mapa
  map <- leaflet(crimes_sf) %>%
    addTiles() %>%
    addPolygons(
      fillColor = ~pal(crimes_sf[[variable]]),
      fillOpacity = 0.7,
      color = "white",
      weight = 1,
      popup = ~paste0(
        "<b>", nome_ra, "</b><br/>",
        "Taxa: ", round(crimes_sf[[variable]], 2), "<br/>",
        "Total: ", total_ocorrencias
      )
    ) %>%
    addLegend(
      pal = pal,
      values = crimes_sf[[variable]],
      title = title,
      position = "bottomright"
    )
  
  return(map)
}

#' Salva resultados da análise
#' 
#' @param results Resultados da análise
#' @param filename Nome do arquivo
#' @param output_dir Diretório de saída
save_analysis_results <- function(results, filename, output_dir) {
  filepath <- file.path(output_dir, filename)
  saveRDS(results, filepath)
  cat("✅ Resultados salvos em:", filepath, "\n")
}

#' Função principal de análise espacial
#' 
#' @param crimes_sf Objeto sf com dados de crimes
#' @param output_dir Diretório de saída
#' @return Lista com todos os resultados
run_spatial_analysis <- function(crimes_sf, output_dir) {
  cat("🚀 Iniciando análise espacial completa...\n")
  
  # Análise KDE
  kde_results <- analyze_kde(crimes_sf)
  save_analysis_results(kde_results, "kde_results.rds", output_dir)
  
  # Análise de Moran
  moran_results <- analyze_moran(crimes_sf)
  save_analysis_results(moran_results, "moran_results.rds", output_dir)
  
  # Análise de Nearest Neighbor
  nn_results <- analyze_nearest_neighbor(crimes_sf)
  save_analysis_results(nn_results, "nn_results.rds", output_dir)
  
  # Análise de Hotspots
  hotspot_results <- analyze_hotspots(crimes_sf)
  save_analysis_results(hotspot_results, "hotspot_results.rds", output_dir)
  
  # Análise de Distâncias
  reference_points <- data.frame(
    nome = c("Centro", "Zona Sul", "Zona Norte"),
    lon = c(-43.2, -43.1, -43.0),
    lat = c(-22.9, -22.8, -22.7)
  )
  
  distance_results <- analyze_distances(crimes_sf, reference_points)
  save_analysis_results(distance_results, "distance_results.rds", output_dir)
  
  # Cria mapas
  map_taxa <- create_spatial_map(crimes_sf, "taxa_100k", "Taxa de Crimes")
  map_moran <- create_spatial_map(moran_results$data, "moran_i", "Índice de Moran Local")
  
  # Salva mapas
  saveWidget(map_taxa, file.path(output_dir, "mapa_taxa_crimes.html"))
  saveWidget(map_moran, file.path(output_dir, "mapa_moran.html"))
  
  # Compila resultados
  all_results <- list(
    kde = kde_results,
    moran = moran_results,
    nearest_neighbor = nn_results,
    hotspots = hotspot_results,
    distances = distance_results,
    maps = list(taxa = map_taxa, moran = map_moran)
  )
  
  # Salva resultados completos
  save_analysis_results(all_results, "spatial_analysis_complete.rds", output_dir)
  
  cat("🎉 Análise espacial concluída com sucesso!\n")
  return(all_results)
}

# Exemplo de uso
if (FALSE) {
  # Carrega dados
  crimes_sf <- st_read(file.path(processed_dir, "crimes_geo.geojson"))
  
  # Executa análise completa
  results <- run_spatial_analysis(crimes_sf, output_dir)
  
  # Visualiza resultados
  print(results$moran$global)
  print(results$hotspots$stats)
}
