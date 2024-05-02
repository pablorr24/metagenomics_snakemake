# Load ggplot2 package
library(ggplot2)

tryCatch({
  # Read the CSV file
  data <- read.csv(snakemake$input)

  # Create a scatter plot using ggplot2
  plot <- ggplot(data, aes(x = bill_length_mm, y = bill_depth_mm)) +
    geom_point() +
    labs(title = "Penguins: Bill Length vs. Bill Depth",
         x = "Bill Length (mm)", y = "Bill Depth (mm)")

  # Print the plot to the RStudio Plots pane
  print(plot)

  # Save the plot
  ggsave(snakemake$output[1], plot, device = "png")
}, error = function(e) {
  cat("Error: ", conditionMessage(e), "\n")
  cat("Traceback:\n")
  print(sys.calls())
  cat("Session Info:\n")
  print(sessionInfo())
  q(status = 1, save = "no")
})
