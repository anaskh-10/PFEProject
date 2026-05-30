# Global Sequence Diagram (PlantUML)

@startuml
title AIOps Platform — End-to-End Data Lifecycle

actor Operator as op
participant "Infrastructure\n(Node/cAdvisor)" as infra
participant "Prometheus" as prom
participant "ML Service" as ml
participant "Alertmanager" as am
participant "Discord" as discord
participant "MCP Agent" as mcp
participant "Zabbix" as zabbix

== Data Collection ==
infra -> prom : scrape metrics (CPU, RAM, etc.)
infra -> zabbix : push/pull metrics (redundancy)

== Automated ML Analysis ==
ml -> prom : fetch 2h history
prom --> ml : metric series
ml -> ml : Detect Anomaly (US6)
ml -> ml : Forecast Values (US7)
ml -> ml : Classify Severity
ml -> prom : export ML metrics (scores, bounds)

== Alerting & Notification ==
prom -> prom : evaluate alert rules
prom -> am : fire alert
am -> discord : post notification
discord --> op : alert received

== Intelligent Querying ==
op -> mcp : "How is the system performing?"
mcp -> prom : tool execution (PromQL)
prom --> mcp : raw metric data
mcp -> mcp : interpret data & analyze
mcp --> op : provide natural language answer\n& HTML dashboard

@enduml
