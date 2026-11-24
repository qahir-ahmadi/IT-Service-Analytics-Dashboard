# IT Service Analytics Dashboard

A portfolio project that analyzes 5,000 synthetic IT help-desk tickets using **Python, Java, R, SQL, PostgreSQL, and Power BI**.


## Live Interactive Dashboard

[Launch Interactive Dashboard](https://qahir-ahmadi.github.io/IT-Service-Analytics-Dashboard/interactive_dashboard.html)

Explore 5,000 IT support tickets through interactive charts, KPI cards, and dynamic filters. No installation or login required.


## Project Goal

The goal is to simulate a real IT service desk and answer business questions about:

- Ticket volume
- Open backlog
- Resolution time
- SLA compliance
- Technician workload
- Department support demand
- Customer satisfaction

## Technologies

### Python
Python and Pandas are used to clean and transform the ticket dataset and create monthly KPI files.

### Java
Java is used to build a menu-driven command-line ticket analyzer using object-oriented programming, collections, file reading, and exception handling.

### R
R is used to create visualizations and summary statistics from the cleaned ticket dataset.

### SQL / PostgreSQL
SQL is used to store and analyze ticket data using business-focused queries.

### Power BI
Power BI is used for the final interactive dashboard.

## Project Structure

IT-Service-Analytics-Dashboard/
│
├── data/
│   ├── raw/
│   │   └── it_tickets_raw.csv
│   └── processed/
│       ├── it_tickets_clean.csv
│       └── monthly_kpis.csv
│
├── docs/
│   ├── interactive_dashboard.html
│   ├── dashboard_preview.png
│   ├── data_dictionary.csv
│   ├── power_bi_dashboard_plan.md
│   └── resume_bullets.md
│
├── java/
│   └── TicketAnalyzer.java
│
├── r/
│   ├── ticket_analysis.R
│   └── output/
│
├── sql/
│   ├── 01_create_table.sql
│   └── 02_analysis_queries.sql
│
├── src/
│   ├── clean_and_analyze.py
│   └── interactive_dashboard.py
│
├── powerbi/
│   └── IT_Service_Analytics_Dashboard.pbix
│
├── .gitignore
├── requirements.txt
└── README.md

## Recommended Run Order

### 1. Python

```bash
python src/clean_and_analyze.py
```

This creates the cleaned dataset used by Java, R, SQL, and Power BI.

### 2. Java

From the project root:

```bash
javac java/TicketAnalyzer.java
java -cp java TicketAnalyzer
```

### 3. R

From the project root in RStudio or R:

```r
source("r/ticket_analysis.R")
```

The charts will be saved to:

```text
r/output/
```

### 4. PostgreSQL / SQL

Create the table using:

```text
sql/01_create_table.sql
```

Then run the analysis in:

```text
sql/02_analysis_queries.sql
```

### 5. Power BI

Import:

```text
data/processed/it_tickets_clean.csv
```

and build the dashboard using:

```text
docs/power_bi_dashboard_plan.md
```

## Portfolio Summary

Built an IT service analytics solution using Python, Java, R, PostgreSQL, SQL, and Power BI to analyze 5,000 synthetic support tickets. Used Python/Pandas for data preparation, Java for a menu-driven ticket analysis application, R for statistical summaries and visualizations, SQL for operational analysis, and Power BI for KPI reporting.
