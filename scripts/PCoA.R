# This script is used in the post analysis workflow to generate a PCoA
# on the classified results. It uses metadata file to categorize the samples
# based on a variable

args <- commandArgs(trailingOnly = TRUE)
argsList <- list()
for (arg in args) {
  arg <- gsub("^--", "", arg)
  keyval <- strsplit(arg, "=")[[1]]
  if (length(keyval) == 2) {
    argsList[[keyval[1]]] <- keyval[2]
  }
}

options(warn=-1)

# Ensuring the 'file' arguments are correctly assigned
distanceMatrixFilename <- argsList[['input']]
outputFilename <- argsList[['output']]
metadataFilename <- argsList[['metadata']]
metadataVariable <- argsList[['variable']]

# Check if the file names are character strings
if (!is.character(distanceMatrixFilename) || nchar(distanceMatrixFilename) == 0) {
  stop("'input' must be a character string specifying the file name.")
}
if (!is.character(outputFilename) || nchar(outputFilename) == 0) {
  stop("'output' must be a character string specifying the file name.")
}

# Parameters for output
width <- 15
height <- 10

# Use JPG function with fixed size and format
jpeg(file=outputFilename, width=width, height=height, units="in", res=72)

distanceMatrix <- as.matrix(read.table(file=distanceMatrixFilename, sep=",", header=TRUE, row.names=1))
distanceMatrix[lower.tri(distanceMatrix)] <- t(distanceMatrix)[lower.tri(distanceMatrix)]
#print(distanceMatrix)

suppressPackageStartupMessages(library(dendextend))

metadata_table <- as.data.frame(read.table(file = metadataFilename, sep = ",", header = TRUE, row.names = 1))
#print(metadata_table)
metadata_variable <- argsList[['variable']]
metadata_index <- metadata_table[[metadata_variable]]

#colors <- as.character(metadata_index[rownames(distanceMatrix)])
colors <- as.character(metadata_index)

colors_factor <- as.factor(colors)
colors_numeric <- as.numeric(colors_factor)

# Perform PCoA and plot only the first 2 PCs
distances <- as.dist(distanceMatrix)
pcoa <- cmdscale(distances, k = 2, eig = TRUE) #PC1 PC2
plotData <- data.frame(pcoa$points)
relEig <- (100 * pcoa$eig / sum(abs(pcoa$eig)) )[1:2]
colnames(plotData) <- c("PC1", "PC2")

x <- plotData$PC1
y <- plotData$PC2

par(mar=c(5.1, 4.1, 4.1, 12.1), xpd=TRUE)
plot(x, y, type='n',
     xlab=paste0("PC1 (", round(relEig[1], 2), "%)"),
     ylab=paste0("PC2 (", round(relEig[2], 2), "%)")
)

text(x, y, labels=rownames(plotData), col=colors_numeric, font=2, cex=1.2)
legend("right", title=metadata_variable, legend=unique(colors), col=unique(colors_numeric), pch=16, inset=c(-0.2, 0))

title("PCoA of Selected Samples using Bray-Curtis Distance")

# Close the JPG device
dev.off()


#Rscript /home/pablorr24/snake_folder/scripts/PCoA.R --input=/home/pablorr24/snake_folder/output/post_analysis/testtest/beta_diversity.csv --output=PCOA_plot.jpg --metadata=/home/pablorr24/snake_folder/data/metadata_23Apr.csv --variable=Species