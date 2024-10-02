#' This Script processes all the publication date data
#' and create a cumulative frequency chart
#' Author: Yu Fan Mei 
#' Date created: September 3, 2024
#' FOR DEALLOCATING MEMORY: rm(list = ls()) (VERY DANGEROUS)

library(dplyr)
library(ggplot2)

data <- read.csv("NCDMPH_Data.csv") # opens the csv file
column_data <- data[, 15] # processes column 5 (the one w/ the dates)

# Store dates in column_data
column_data <- as.Date(column_data, format = "%m/%d/%Y")

# Create a data frame with the dates
date_data <- data.frame(Date = column_data)

# Sort the dates
date_data <- date_data %>% arrange(Date)

# Add a cumulative count column
date_data <- date_data %>%
  mutate(Cumulative_Count = row_number())

# Define the range and create a sequence of dates for breaks
start_date <- as.Date("1780-01-01")
end_date <- as.Date("2030-12-31")

# Calculate the breaks (6 major gridlines)
breaks_dates <- seq(from = start_date, to = end_date, length.out = 6)

# Create the cumulative chart with only the cumulative line
ggplot(date_data, aes(x = Date, y = Cumulative_Count)) +
  geom_line(color = "blue") +  # Line only, no points
  labs(title = "Cumulative Frequency Timeline of Statute Publication",
       x = "Date",
       y = "Cumulative Count") +
  scale_x_date(
    breaks = breaks_dates,
    date_labels = "%Y",  # Show only the year
    limits = c(start_date, end_date)
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)  # Rotate x-axis labels for better readability
  )

rm(list = ls()) # deallocates all variables (being done so all scripts can be standalone)
