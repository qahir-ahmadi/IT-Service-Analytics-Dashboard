# Power BI Dashboard Plan

## Page 1 — Executive Overview
Cards:
- Total Tickets
- Open Backlog
- Average Resolution Time
- SLA Compliance %
- Average Satisfaction Score

Charts:
- Tickets by Category
- Tickets by Priority
- Monthly Ticket Trend
- SLA Compliance by Priority
- Open Tickets by Department

## Page 2 — Technician Performance
- Tickets Closed by Technician
- Average Resolution Time by Technician
- Average Satisfaction by Technician
- SLA Compliance by Technician

## Page 3 — Support Demand
- Ticket Volume by Department
- Ticket Volume by Location
- Category by Department matrix
- Monthly trend slicer

## Suggested DAX Measures
Total Tickets = COUNTROWS(it_tickets)

Open Backlog =
CALCULATE(
    COUNTROWS(it_tickets),
    it_tickets[status] = "Open"
) +
CALCULATE(
    COUNTROWS(it_tickets),
    it_tickets[status] = "In Progress"
)

Avg Resolution Hours =
AVERAGE(it_tickets[resolution_hours])

SLA Compliance % =
DIVIDE(
    CALCULATE(COUNTROWS(it_tickets), it_tickets[sla_met] = TRUE()),
    CALCULATE(COUNTROWS(it_tickets), NOT ISBLANK(it_tickets[sla_met]))
)

Avg Satisfaction =
AVERAGE(it_tickets[satisfaction_score])
