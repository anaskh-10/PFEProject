# Global Use Case Diagram (PlantUML)

@startuml
skinparam packageStyle rectangle
left to right direction

actor "Administrator" as admin
actor "Operator" as op
actor "ML Service" as ml <<autonomous>>
actor "MCP Agent" as mcp <<system>>

rectangle "AIOps Platform" {
    
    package "Infrastructure & Deployment" {
        usecase "UC01: Containerize & Deploy Services (US1)" as UC01
        usecase "UC02: Monitor via Zabbix (US10)" as UC10
        usecase "UC03: Configure Prometheus & Exporters (US2, US3)" as UC03
    }

    package "Visibility & Action" {
        usecase "UC04: Consult Grafana Dashboards (US4)" as UC04
        usecase "UC05: Receive Discord Alerts (US5)" as UC05
        usecase "UC06: Configure ML Thresholds (US8)" as UC06
    }

    package "Machine Learning Layer" {
        usecase "UC07: Detect Anomaly & Score (US6)" as UC07
        usecase "UC08: Forecast Metric Trends (US7)" as UC08
        usecase "UC08b: Classify Alert Severity" as UC08b
    }

    package "Intelligence Layer" {
        usecase "UC09: Query Metrics in NL (US9)" as UC09
        usecase "UC09b: Generate dynamic HTML Dashboards" as UC09b
    }
}

admin --> UC01
admin --> UC03
admin --> UC10

op --> UC04
op --> UC05
op --> UC06
op --> UC09

ml --> UC07
ml --> UC08
ml --> UC08b

mcp --> UC09
mcp --> UC09b

UC07 ..> UC05 : <<triggers>>
UC09 ..> UC04 : <<complements>>

@enduml
