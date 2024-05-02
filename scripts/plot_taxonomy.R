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
    TaxLevel == "U" ~ "Unassigned",
    TaxLevel == "O" ~ "Order",
    TaxLevel == "R" ~ "Root",
    TaxLevel == "D" ~ "Domain",
    TRUE ~ as.character(TaxLevel)  # Default for other cases
  ))

p <- ggplot(kraken_report, aes(x = reorder(Scientific_Name, -Percentage), y = Percentage, fill = TaxonomicLevel)) +
  geom_bar(stat = "identity") +
  labs(x = "Scientific Name", y = "Percentage Abundance", title = "Relative Abundance of Species") +
  theme_minimal() +
  coord_flip() +
  theme(axis.text.y = element_text(size = 12),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.title = element_text(hjust = 0.5)) +
  scale_fill_manual(values = c("Phylum" = "blue", "Class" = "green", "Order" = "red", "Family" = "purple", 
                               "Genus" = "orange", "Species" = "pink", "R" = "black", "Unassigned"="grey"))

ggsave(filename = args[2], plot = p, width = 8, height = 4)