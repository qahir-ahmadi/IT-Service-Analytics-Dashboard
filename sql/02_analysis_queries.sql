-- Ticket volume by category
SELECT category, COUNT(*) AS ticket_count
FROM it_tickets
GROUP BY category
ORDER BY ticket_count DESC;

-- Average resolution time by priority
SELECT priority, ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM it_tickets
WHERE status IN ('Closed', 'Resolved')
GROUP BY priority
ORDER BY avg_resolution_hours;

-- SLA compliance by priority
SELECT
    priority,
    ROUND(100.0 * AVG(CASE WHEN sla_met THEN 1 ELSE 0 END), 2) AS sla_compliance_pct
FROM it_tickets
WHERE status IN ('Closed', 'Resolved')
GROUP BY priority
ORDER BY sla_compliance_pct DESC;

-- Current backlog
SELECT priority, COUNT(*) AS open_tickets
FROM it_tickets
WHERE status IN ('Open', 'In Progress')
GROUP BY priority
ORDER BY open_tickets DESC;

-- Technician performance
SELECT
    technician,
    COUNT(*) AS tickets_closed,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM it_tickets
WHERE status IN ('Closed', 'Resolved')
GROUP BY technician
ORDER BY tickets_closed DESC;

-- Monthly ticket trend
SELECT
    DATE_TRUNC('month', opened_date) AS month,
    COUNT(*) AS tickets_opened
FROM it_tickets
GROUP BY month
ORDER BY month;
