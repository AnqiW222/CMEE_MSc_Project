# Load the necessary libraries
library(tidyverse)
library(dplyr)     # For data manipulation
library(tidyr)     # For data tidying
library(reshape2)  # For data reshaping
library(ggplot2)   # For plotting

# --- Current Velocity Experiments ---

# Read CSV files containing seagrass coverage data at different current velocities
data_high_v <- read.csv("../data/seagrass_coverage_high_velocity.csv")
data_medium_v <- read.csv("../data/seagrass_coverage_medium_velocity.csv")
data_low_v <- read.csv("../data/seagrass_coverage_low_velocity.csv")

# Combine data frames from different velocity categories into a single data frame
combined_data <- rbind(
  data.frame(Seagrass_Coverage = data_high_v$Seagrass_Coverage, Current_Velocity = "High"),
  data.frame(Seagrass_Coverage = data_medium_v$Seagrass_Coverage, Current_Velocity = "Medium"),
  data.frame(Seagrass_Coverage = data_low_v$Seagrass_Coverage, Current_Velocity = "Low")
)

# Perform one-way ANOVA to compare seagrass coverage across different current velocities
anova_result_v <- aov(Seagrass_Coverage ~ Current_Velocity, data = combined_data)
summary(anova_result_v)

# Add a column to individual data frames to indicate the velocity category
data_high_v$Velocity_Category <- 'High'
data_medium_v$Velocity_Category <- 'Medium'
data_low_v$Velocity_Category <- 'Low'

# Merge individual data frames into a single data frame again
combined_data <- rbind(data_high_v, data_medium_v, data_low_v)

# Plot the boxplot of seagrass coverage across different current velocities
ggplot(combined_data, aes(x=Velocity_Category, y=Seagrass_Coverage, fill=Velocity_Category)) +
  geom_boxplot() +
  labs(title="Boxplot of Seagrass Coverage Across Different Current Velocities",
       x="Current Velocity Category",
       y="Seagrass Coverage") +
  ylim(c(-1, max(combined_data$Seagrass_Coverage) + 1)) +
  theme_minimal()

# Calculate mean and standard error of seagrass coverage for each velocity category
agg_data <- aggregate(Seagrass_Coverage ~ Velocity_Category, data = combined_data, FUN = mean)
agg_data$stderr <- aggregate(Seagrass_Coverage ~ Velocity_Category, data = combined_data, FUN = function(x) sd(x) / sqrt(length(x)))$Seagrass_Coverage

# Plot the Mean Plot with Error Bars for different current velocities
ggplot(agg_data, aes(x=Velocity_Category, y=Seagrass_Coverage, fill=Velocity_Category)) +
  geom_errorbar(aes(ymin=Seagrass_Coverage-stderr, ymax=Seagrass_Coverage+stderr), width=.2) +
  geom_point(size=4) +
  labs(title="Mean Plot with Error Bars for Seagrass Coverage Across Different Current Velocities",
       x="Current Velocity Category",
       y="Mean Seagrass Coverage") +
  theme_minimal()
ggsave('velocity_expri_anova.png',dpi=400)

# --- Nutrient Level Experiments ---

# Read CSV files containing seagrass coverage data at different nutrient levels
data_high_n <- read.csv("../data/seagrass_coverage_matrix_nutrient_High.csv")
data_medium_n <- read.csv("../data/seagrass_coverage_matrix_nutrient_Medium.csv")
data_low_n <- read.csv("../data/seagrass_coverage_matrix_nutrient_Low.csv")

# Combine data frames from different nutrient levels into a single data frame
combined_data <- rbind(
  data.frame(Seagrass_Coverage = data_high_n$Seagrass_Coverage, Nutrient_Level = "High"),
  data.frame(Seagrass_Coverage = data_medium_n$Seagrass_Coverage, Nutrient_Level = "Medium"),
  data.frame(Seagrass_Coverage = data_low_n$Seagrass_Coverage, Nutrient_Level = "Low")
)

# Perform one-way ANOVA to compare seagrass coverage across different nutrient levels
anova_result_n <- aov(Seagrass_Coverage ~ Nutrient_Level, data = combined_data)
summary(anova_result_n)

# Combine ANOVA results into a list
anova_results <- list(
  Current_velocity_expri = anova_result_v,
  Nutrient_expri = anova_result_n
)

# Extract summaries of ANOVA results and combine them into a single data frame
anova_summaries <- lapply(anova_results, function(result) {
  summary_output <- summary(result)
  summary_data <- summary_output[[1]]
  summary_data <- as.data.frame(summary_data)
  colnames(summary_data) <- c("Df", "Sum Sq", "Mean Sq", "F value", "Pr(>F)")
  rownames(summary_data) <- c("Group", "Residual")
  return(summary_data)
})

# Combine all ANOVA summaries into a single data frame
combined_anova_summaries <- do.call(rbind, anova_summaries)

# Print combined ANOVA summaries
print(combined_anova_summaries)

# Export the combined ANOVA summaries to a CSV file
output_csv_file <- "combined_anova_summaries.csv"
write.csv(combined_anova_summaries, file = output_csv_file)

# Output a message to indicate that the ANOVA summaries have been exported
cat("Combined ANOVA summaries exported to", output_csv)
    