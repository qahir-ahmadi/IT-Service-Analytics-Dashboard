# IT Service Analytics - R Visualizations
# Reads the same cleaned CSV produced by Python.

tickets <- read.csv("data/processed/it_tickets_clean.csv", stringsAsFactors = FALSE)

dir.create("r/output", showWarnings = FALSE, recursive = TRUE)

cat("Rows loaded:", nrow(tickets), "\n")
cat("Open or In Progress tickets:",
    sum(tickets$status %in% c("Open", "In Progress")), "\n")

# 1. Tickets by category
category_counts <- sort(table(tickets$category), decreasing = TRUE)

png("r/output/tickets_by_category.png", width = 1000, height = 700)
barplot(
  category_counts,
  main = "IT Support Tickets by Category",
  xlab = "Category",
  ylab = "Number of Tickets",
  las = 2,
  col = "steelblue"
)
dev.off()

# 2. Average resolution time by priority
closed_tickets <- tickets[tickets$status %in% c("Closed", "Resolved"), ]

avg_resolution <- aggregate(
  resolution_hours ~ priority,
  data = closed_tickets,
  FUN = mean
)

png("r/output/avg_resolution_by_priority.png", width = 900, height = 650)
barplot(
  avg_resolution$resolution_hours,
  names.arg = avg_resolution$priority,
  main = "Average Resolution Time by Priority",
  xlab = "Priority",
  ylab = "Average Resolution Hours",
  col = "steelblue"
)
dev.off()

# 3. Ticket status distribution
status_counts <- table(tickets$status)

png("r/output/ticket_status_distribution.png", width = 900, height = 650)
barplot(
  status_counts,
  main = "Ticket Status Distribution",
  xlab = "Status",
  ylab = "Number of Tickets",
  las = 2,
  col = "steelblue"
)
dev.off()

# 4. Department demand
department_counts <- sort(table(tickets$department), decreasing = TRUE)

png("r/output/tickets_by_department.png", width = 1000, height = 700)
barplot(
  department_counts,
  main = "IT Support Demand by Department",
  xlab = "Department",
  ylab = "Number of Tickets",
  las = 2,
  col = "steelblue"
)
dev.off()

cat("\nCharts saved in r/output/\n")
