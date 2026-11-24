
from pathlib import Path
import pandas as pd
import plotly.express as px

BASE = Path(__file__).resolve().parents[1]

# Load dataset
df = pd.read_csv(BASE / "data/processed/it_tickets_clean.csv")

closed = df[df["status"].isin(["Closed", "Resolved"])]
backlog = df[df["status"].isin(["Open", "In Progress"])]

# Calculate KPIs
total_tickets = len(df)
open_backlog = len(backlog)
avg_resolution = closed["resolution_hours"].mean()
sla_compliance = closed["sla_met_flag"].mean() * 100
avg_satisfaction = closed["satisfaction_score"].mean()

# Chart 1: Tickets by Category
fig1 = px.bar(
    df["category"].value_counts().rename_axis("Category").reset_index(name="Tickets"),
    x="Tickets",
    y="Category",
    orientation="h",
    title="Tickets by Category"
)
fig1.update_yaxes(autorange="reversed")

# Chart 2: Tickets by Priority
fig2 = px.bar(
    df["priority"].value_counts().rename_axis("Priority").reset_index(name="Tickets"),
    x="Priority",
    y="Tickets",
    title="Tickets by Priority"
)

# Chart 3: Monthly Ticket Trend
monthly = df.groupby("opened_month").size().reset_index(name="Tickets")

fig3 = px.line(
    monthly,
    x="opened_month",
    y="Tickets",
    markers=True,
    title="Monthly Ticket Trend"
)

# Chart 4: Open Tickets by Department
fig4 = px.bar(
    backlog["department"].value_counts().rename_axis("Department").reset_index(name="Tickets"),
    x="Tickets",
    y="Department",
    orientation="h",
    title="Open Tickets by Department"
)
fig4.update_yaxes(autorange="reversed")

# Chart 5: SLA Compliance by Priority
sla = closed.groupby("priority")["sla_met_flag"].mean().reset_index()
sla["sla_met_flag"] *= 100

fig5 = px.bar(
    sla,
    x="priority",
    y="sla_met_flag",
    title="SLA Compliance by Priority"
)
fig5.update_yaxes(title="SLA Compliance (%)", range=[0, 100])

# Apply consistent chart styling
figures = [fig1, fig2, fig3, fig4, fig5]

for fig in figures:
    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=30, r=30, t=60, b=40)
    )
    fig.update_traces(
        marker=dict(color="steelblue")
    )

fig3.update_traces(line=dict(color="steelblue"))

# Build HTML dashboard
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT Service Analytics Dashboard</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #eef2f6;
    margin: 0;
    padding: 25px;
}

h1 {
    text-align: center;
    color: #1e293b;
}

.subtitle {
    text-align: center;
    color: #64748b;
}

.kpis {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 8px #00000010;
}

.card h2 {
    color: steelblue;
    font-size: 32px;
}

.card p {
    color: #64748b;
}

.charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 450px), 1fr));
    gap: 20px;
}

.chart {
    background: white;
    border-radius: 10px;
    padding: 10px;
}
</style>
</head>
<body>

<h1>IT Service Analytics Dashboard</h1>
<p class="subtitle">
    IT Support Performance | Synthetic Dataset
</p>
"""

# KPI cards
html += f"""
<div class="kpis">

<div class="card">
<p>Total Tickets</p>
<h2>{total_tickets:,}</h2>
</div>

<div class="card">
<p>Open Backlog</p>
<h2>{open_backlog:,}</h2>
</div>

<div class="card">
<p>Avg Resolution</p>
<h2>{avg_resolution:.2f} hrs</h2>
</div>

<div class="card">
<p>SLA Compliance</p>
<h2>{sla_compliance:.2f}%</h2>
</div>

<div class="card">
<p>Avg Satisfaction</p>
<h2>{avg_satisfaction:.2f}/5</h2>
</div>

</div>
<div class="charts">
"""

# Add all interactive charts
for i, fig in enumerate(figures):
    html += '<div class="chart">'
    html += fig.to_html(
        full_html=False,
        include_plotlyjs="cdn" if i == 0 else False,
        config={"responsive": True}
    )
    html += '</div>'

html += """
</div>
</body>
</html>
"""

# Add interactive filters
filter_html = """
<div style="display:flex; flex-wrap:wrap; gap:15px;
            justify-content:center; margin-bottom:25px;">

    <select id="departmentFilter">
        <option value="">All Departments</option>
    </select>

    <select id="priorityFilter">
        <option value="">All Priorities</option>
    </select>

    <select id="statusFilter">
        <option value="">All Statuses</option>
    </select>

    <button onclick="resetFilters()">Reset Filters</button>

</div>

<style>
select, button {
    padding: 12px 18px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 15px;
    background: white;
    cursor: pointer;
}

button {
    background: steelblue;
    color: white;
}
</style>
"""

html = html.replace(
    '<div class="kpis">',
    filter_html + '<div class="kpis">',
    1
)

# Convert Python data into browser-readable JSON
columns = [
    "department", "priority", "status", "category",
    "opened_month", "resolution_hours",
    "sla_met_flag", "satisfaction_score"
]

ticket_json = df[columns].to_json(orient="records")

# JavaScript makes the dashboard respond to filters
filter_script = "<script>const tickets = " + ticket_json + ";\n" + """
const fields = {
    departmentFilter: "department",
    priorityFilter: "priority",
    statusFilter: "status"
};

for (const [id, field] of Object.entries(fields)) {
    const select = document.getElementById(id);
    const values = [...new Set(tickets.map(t => t[field]))].sort();

    values.forEach(value => {
        select.add(new Option(value, value));
    });

    select.addEventListener("change", updateDashboard);
}

function average(rows, field) {
    const values = rows.map(r => r[field])
        .filter(Number.isFinite);

    return values.length
        ? values.reduce((a, b) => a + b, 0) / values.length
        : null;
}

function countBy(rows, field) {
    const counts = {};

    rows.forEach(row => {
        const key = row[field];
        counts[key] = (counts[key] || 0) + 1;
    });

    return Object.entries(counts);
}

function updateDashboard() {
    const filtered = tickets.filter(ticket =>
        Object.entries(fields).every(([id, field]) => {
            const value = document.getElementById(id).value;
            return !value || ticket[field] === value;
        })
    );

    const closed = filtered.filter(t =>
        ["Closed", "Resolved"].includes(t.status)
    );

    const backlog = filtered.filter(t =>
        ["Open", "In Progress"].includes(t.status)
    );

    const resolution = average(closed, "resolution_hours");
    const sla = average(closed, "sla_met_flag");
    const satisfaction = average(closed, "satisfaction_score");

    // Update KPI cards
    const cards = document.querySelectorAll(".card h2");

    cards[0].textContent = filtered.length.toLocaleString();
    cards[1].textContent = backlog.length.toLocaleString();

    cards[2].textContent = resolution === null
        ? "N/A" : resolution.toFixed(2) + " hrs";

    cards[3].textContent = sla === null
        ? "N/A" : (sla * 100).toFixed(2) + "%";

    cards[4].textContent = satisfaction === null
        ? "N/A" : satisfaction.toFixed(2) + "/5";

    // Find the five Plotly charts
    const charts = document.querySelectorAll(".plotly-graph-div");

    // Chart 1: Category
    const categories = countBy(filtered, "category")
        .sort((a, b) => b[1] - a[1]);

    Plotly.restyle(charts[0], {
        x: [categories.map(r => r[1])],
        y: [categories.map(r => r[0])]
    });

    // Chart 2: Priority
    const priorities = countBy(filtered, "priority");

    Plotly.restyle(charts[1], {
        x: [priorities.map(r => r[0])],
        y: [priorities.map(r => r[1])]
    });

    // Chart 3: Monthly trend
    const months = countBy(filtered, "opened_month")
        .sort((a, b) => a[0].localeCompare(b[0]));

    Plotly.restyle(charts[2], {
        x: [months.map(r => r[0])],
        y: [months.map(r => r[1])]
    });

    // Chart 4: Department backlog
    const departments = countBy(backlog, "department")
        .sort((a, b) => b[1] - a[1]);

    Plotly.restyle(charts[3], {
        x: [departments.map(r => r[1])],
        y: [departments.map(r => r[0])]
    });

    // Chart 5: SLA compliance
    const levels = ["Critical", "High", "Medium", "Low"];

    const rates = levels.map(priority => {
        const rows = closed.filter(t => t.priority === priority);
        const rate = average(rows, "sla_met_flag");
        return rate === null ? null : rate * 100;
    });

    Plotly.restyle(charts[4], {
        x: [levels],
        y: [rates]
    });
}

function resetFilters() {
    Object.keys(fields).forEach(id => {
        document.getElementById(id).value = "";
    });

    updateDashboard();
}
</script>
"""

html = html.replace("</body>", filter_script + "</body>")

# Save dashboard
output = BASE / "docs" / "interactive_dashboard.html"

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(html, encoding="utf-8")

print(f"Dashboard saved to: {output}")
