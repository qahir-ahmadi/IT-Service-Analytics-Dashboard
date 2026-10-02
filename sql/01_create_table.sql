CREATE TABLE it_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    opened_date DATE NOT NULL,
    resolved_date TIMESTAMP NULL,
    department VARCHAR(50),
    location VARCHAR(50),
    category VARCHAR(50),
    priority VARCHAR(20),
    technician VARCHAR(50),
    status VARCHAR(30),
    sla_target_hours INTEGER,
    resolution_hours NUMERIC(10,2),
    sla_met BOOLEAN,
    satisfaction_score NUMERIC(3,1),
    issue_summary VARCHAR(255)
);
