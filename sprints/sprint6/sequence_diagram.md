# Sprint 6 — Sequence Diagram (PlantUML)
## Period: 29 May – 06 Jun | US9

@startuml
title Sprint 6: MCP Agent Query Processing

actor Operator as op
participant "MCPAgent" as Agent
participant "PrometheusQueryTool" as Tool
participant "Prometheus" as Prom
participant "DashboardGenerator" as Dash

op -> Agent : "Analyze CPU usage for the last 1h"
Agent -> Agent : process NL text
Agent -> Tool : execute_range_query(cpu_query, 1h)
Tool -> Prom : HTTP GET /api/v1/query_range
Prom --> Tool : JSON data points
Tool --> Agent : statistical summary (avg, max, std)

Agent -> Dash : generate_html_dashboard(data)
Dash --> Agent : HTML string

Agent --> op : Respond with analysis text\nand HTML dashboard
@enduml
