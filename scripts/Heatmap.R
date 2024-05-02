if (!require("gplots")) {
  install.packages("gplots", dependencies = TRUE)
  library(gplots)
}

args <- commandArgs(trailingOnly = TRUE)

width <- 15
height <- 10

# Set format to "jpg" directly
format <- "jpg"

# Read matrix file
distance_matrix <- as.matrix(read.table(file = args[1], sep = ";", header = TRUE, row.names = 1))

# Ensure matrix is symmetric (if needed)
distance_matrix[lower.tri(distance_matrix)] <- t(distance_matrix)[lower.tri(distance_matrix)]

# Normalize matrix (if needed)
# Example: Scale Bray-Curtis dissimilarity values to range [0, 1]
normalized_matrix <- (distance_matrix - min(distance_matrix)) / (max(distance_matrix) - min(distance_matrix))

# Generate Heatmap
cr3_norm <- normalized_matrix

distance_name <- basename(args[1])
distance_name <- unlist(strsplit(distance_name, "[.]"))[1]
distance_name <- gsub("mat_", "", distance_name)

use_metadata <- FALSE
if (length(args) == 5) {
  use_metadata <- TRUE
  metadata_table <- as.matrix(read.table(file = args[4], sep = ";", header = TRUE, row.names = 1))
  metadata_variable <- args[5]
  variables <- metadata_table[, metadata_variable]
  
  meatadata_index <- list()
  dataset_ids <- rownames(metadata_table)
  for (i in 1:length(dataset_ids)) {
    dataset_id <- dataset_ids[i]
    meatadata_index[[dataset_id]] <- variables[[i]]
  }
  
  colors <- c()
  dataset_ids <- rownames(cr3_norm)
  for (i in 1:dim(cr3_norm)[1]) {
    dataset_id <- dataset_ids[i]
    colors <- c(colors, meatadata_index[[dataset_id]])
  }
  colors_numeric_temp <- c()
  colors_numeric <- as.numeric(as.factor(colors))
  for (i in 1:length(colors_numeric)) {
    colors_numeric_temp <- c(colors_numeric_temp, colors_numeric[i] + 1)
  }
  colors_numeric <- colors_numeric_temp
}

n <- 100 # number of steps between 2 colors

## Transforming 0-1 distances in 0-100 similarity measure
if (grepl("chord", args[1]) || grepl("hellinger", args[1])) {
  cr3 <- (sqrt(2) - normalized_matrix) * 100
} else {
  cr3 <- (1 - normalized_matrix) * 100
}

## Computing mini-maxi for colour palette
mini <- min(cr3[])
maxi <- max(cr3[row(cr3) != col(cr3)]) # ignoring the diagonal
trueMax <- max(cr3[]) # typically the value in the diagonal = 100
q25 <- quantile(cr3[row(cr3) != col(cr3)], 0.25, 1)
q50 <- quantile(cr3[row(cr3) != col(cr3)], 0.5, 1)
q75 <- quantile(cr3[row(cr3) != col(cr3)], 0.75, 1)

## We use the quantiles to ignore some outlier values in the matrix (values<mini will have colour of mini and values>maxi will have a colour between brown and grey23)
mini <- max(q25 - 1.5 * (q75 - q25), 0)
maxi <- min(q75 + 1.5 * (q75 - q25), trueMax)

palette <- colorRampPalette(c("green", "yellow", "red", "brown", "grey23"))(n = 5 * n - 1)

## Checking if maxi = trueMax
trueMax.needed <- ifelse(maxi < trueMax, "T", "F")

if (trueMax.needed) {
  breaks <- c(seq(mini, maxi, length = 4 * n), seq(maxi + 1e-5, trueMax, length = n))
  # breaks are equally distributed in the range mini-maxi (intervals can be different in the range maxi-trueMax, containing very few points)
} else {

  breaks <- c(seq(mini, maxi, length = 5 * n))
}

# Dendrogram is obtained with the symetric matrix
distance <- dist(cr3_norm)
cluster <- hclust(distance, method = "average")
dendrogram <- as.dendrogram(cluster)

# Heatmap 
par(fig = c(0.2, 1, 0, 0.8), mar = rep(1, 4))

if (use_metadata) {
  
  colors_numeric <- as.character(colors_numeric)
  heatmap.2(cr3,
            trace = "none",
            dendrogram = "row",
            key = FALSE,
            Rowv = dendrogram,
            Colv = rev(dendrogram),
            col = palette,
            breaks = breaks,
            margins = c(10, 10),
            main = paste0("Simka heatmap\n", distance_name), sub = "", cexRow = 0.8, cexCol = 0.8, RowSideColors = colors_numeric, ColSideColors = colors_numeric)
  
} else {
  heatmap.2(cr3,
            trace = "none", dendrogram = "row", key = FALSE, Rowv = dendrogram,
            Colv = rev(dendrogram), col = palette, breaks = breaks, margins = c(10, 10),
            main = paste0("Simka heatmap\n", distance_name), sub = "", cexRow = 0.8, cexCol = 0.8)
}

if (use_metadata) {
  par(lend = 1)           # square line ends for the color legend
  legend("topright", title = metadata_variable, legend = unique(colors), 
         col = unique(colors_numeric), pch = 16, lty = 1, lwd = 10)
}

# Adding the colour scale
par(fig = c(0.05, 0.4, 0.8, 1), mar = rep(2, 4), new = TRUE)

if (trueMax.needed) {
  
  diff <- maxi - mini
  breaksToMaxi <- breaks[1:(4 * n)] # using only breaks from mini to maxi
  black.width <- max(diff / 9)
  black.space <- max(diff / 9)
  
  plot(c(mini, maxi + black.width + black.space), c(0, 2), type = "n", yaxt = "n", ylab = "", xlab = "", xaxt = "n", xaxs = "i", yaxs = "i")
  rect(breaksToMaxi[-length(breaksToMaxi)], 0, breaksToMaxi[-1], 2, col = palette, border = NA)
  
  ti <- pretty(breaksToMaxi)
  ti <- ti[ti < maxi]
  axis(1, at = c(ti, maxi + black.space + black.width / 2), label = c(ti, trueMax))
  
  # Here plotting the TrueMax colour with a white space
  rect(maxi + black.space, 0, maxi + black.space + black.width, 2, col = palette[5 * n - 1], border = NA)
  rect(maxi, -0.1, maxi + black.space, 2.1, col = "white", border = NA)
  
} else {
  plot(range(breaks), c(0, 2), type = "n", yaxt = "n", ylab = "", xlab = "", xaxs = "i", yaxs = "i")
  rect(breaks[-length(breaks)], 0, breaks[-1], 2, col = palette, border = NA)
}

jpeg(file = "output_heatmap.jpg", width = width, height = height, quality = 100)
dev.off()
