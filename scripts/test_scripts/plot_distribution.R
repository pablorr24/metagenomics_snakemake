# plot_distribution.R

args <- commandArgs(trailingOnly=TRUE)

# Check if the correct number of command line arguments is provided
if (length(args) != 4) {
  stop("Usage: Rscript plot_distribution.R input_csv output_plot.png")
}

# Load necessary libraries
library(ggplot2)

# Read penguin dataset
penguins <- read.csv(args[3])
print(head(penguins))

# Plot distribution
p <- ggplot(penguins, aes(x=species, fill=species)) +
  geom_bar() +
  labs(title="Distribution of Penguin Species", x="species", y="Count")

# Save the plot to a file
ggsave(args[4], plot = p, width = 6, height = 4, dpi = 300)
