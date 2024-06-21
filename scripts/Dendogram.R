#This script is used in the post analysis workflow to generate a Dendogram
#on the classified results. It uses metadata file to categorize the samples
#based on a variable

#This script was adapted from https://github.com/GATB/simka/blob/master/scripts/visualization/dendro.r

#libraries
library(magrittr)
library(dendextend)

# parse args
parse_args <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  args_list <- list()
  for (arg in args) {
    arg <- gsub("^--", "", arg)
    keyval <- strsplit(arg, "=")[[1]]
    if (length(keyval) == 2) {
      args_list[[keyval[1]]] <- keyval[2]
    }
  }
  return(args_list)
}

options(warn=-1)

# Validate file names
validate_filenames <- function(filename) {
  if (!is.character(filename) || nchar(filename) == 0) {
    stop(paste("'", filename, "' must be a character string specifying the file name.", sep = ""))
  }
}

# Read distance matrix
process_distance_matrix <- function(filename) {
  distance_matrix <- as.matrix(read.table(file = filename, sep = ",", header = TRUE, row.names = 1))
  distance_matrix <- apply(distance_matrix, 2, as.numeric)
  distance_matrix[lower.tri(distance_matrix)] <- t(distance_matrix)[lower.tri(distance_matrix)]
  return(distance_matrix)
}

# metadata handling
handle_metadata <- function(metadata_filename, metadata_variable) {
  if (!is.na(metadata_filename) && !is.na(metadata_variable) && nchar(metadata_filename) > 0 && nchar(metadata_variable) > 0) {
    metadata_table <- as.matrix(read.table(file = metadata_filename, sep = ",", header = TRUE, row.names = 1))
    colors <- sapply(rownames(metadata_table), function(id) metadata_table[id, metadata_variable])
    colors_numeric <- as.numeric(as.factor(colors))
    return(list(colors = colors, colors_numeric = colors_numeric))
  } else {
    return(NULL)
  }
}

plot_clustering <- function(distance_matrix, metadata = NULL, legend_title = "Variable") {
  options(warn = -1)
  output_filename <- args_list[['output']]
  jpeg(file = output_filename, width = 15, height = 10, units = "in", res = 72)
  
  suppressMessages({
    commet_distance <- as.dist(distance_matrix)
    hc <- hclust(commet_distance, method = "average")
    dendo <- as.dendrogram(hc)
    
    if (!is.null(metadata)) {
      colors_numeric_hc <- metadata$colors_numeric[hc$order]
      dendo %>% set("labels_col", colors_numeric_hc) %>% set("branches_k_color", colors_numeric_hc) %>% 
        plot(main = "Hierarchical Clustering of  selected samples using Bray-Curtis Distance\n", cex = 0.3, xlab = "", ylab = "Bray-Curtis Distance", sub = "")
      
      legend("topright", title = legend_title, legend = levels(factor(metadata$colors)), fill = palette()[1:length(levels(factor(metadata$colors)))])
      
    } else {
      plot(dendo, main = "Hierarchical Clustering of selected samples using Bray-Curtis Distance\n", cex = 0.3, xlab = "", ylab = "Bray-Curtis Distance", sub = "")
    }
  })
  
  dev.off()
}

# Main script logic
args_list <- parse_args()
validate_filenames(args_list[['input']])
validate_filenames(args_list[['output']])
distance_matrix <- process_distance_matrix(args_list[['input']])
metadata <- handle_metadata(args_list[['metadata']], args_list[['variable']])
plot_clustering(distance_matrix, metadata, args_list[['variable']])
