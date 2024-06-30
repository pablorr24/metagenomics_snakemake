args <- commandArgs(trailingOnly = TRUE)
setwd(getwd())

# Load libraries
library(ggplot2)
library(dplyr)

# Read report table
kraken_report <- read.table(args[1], header = FALSE, sep = "\t", quote = "")

# Rename columns
colnames(kraken_report) <- c("Percentage", "Num_Assigned", "Num_Unassigned", "TaxLevel", "TaxonomyID", "Scientific_Name")

# Filter rows with assigned taxonomies (not unclassified)
kraken_report <- subset(kraken_report, TaxonomyID != "unclassified")

kraken_report <- kraken_report %>%
  mutate(TaxonomicLevel = case_when(
    TaxLevel == "C" ~ "Class",
    TaxLevel == "F" ~ "Family",
    TaxLevel == "G" ~ "Genus",
    TaxLevel == "P" ~ "Phylum",
    TaxLevel == "S" ~ "Species",
    TaxLevel == "U" ~ "Unassigned",
    TaxLevel == "O" ~ "Order",
    TaxLevel == "R" ~ "Root",
    TaxLevel == "D" ~ "Domain",
    TRUE ~ as.character(TaxLevel)  # Default for other cases
  ))

# Get the selected taxonomic level from the arguments
taxonomic_level_map <- c("C" = "Class", "F" = "Family", "G" = "Genus", "P" = "Phylum", "S" = "Species", "U" = "Unassigned", "O" = "Order", "R" = "Root", "D" = "Domain")
selected_taxonomic_level <- taxonomic_level_map[[args[3]]]

# Filter the data to include only the top 20 taxa with the highest abundance
kraken_report <- kraken_report %>%
  filter(TaxonomicLevel == selected_taxonomic_level) %>%
  top_n(20, wt = Percentage)

p <- ggplot(kraken_report, aes(x = reorder(Scientific_Name, -Percentage), y = Percentage)) +
  geom_bar(stat = "identity", fill = "blue") +
  labs(x = "Scientific Name", y = "Percentage Abundance", title = paste("Top 20 Abundant", selected_taxonomic_level)) +
  theme_minimal() +
  coord_flip() +
  theme(axis.text.y = element_text(size = 12),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.title = element_text(hjust = 0.5),
        # Set background color to white for the plot and all its components
        plot.background = element_rect(fill = "white"),
        legend.background = element_rect(fill = "white"),
        legend.box.background = element_rect(fill = "white"),
        panel.background = element_rect(fill = "white"),
        panel.border = element_rect(color = "black", fill = NA),
        legend.key = element_rect(fill = "white"),
        panel.spacing = unit(1, "lines"))

ggsave(filename = args[2], plot = p, width = 8, height = 4)
