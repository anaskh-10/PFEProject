# Global Use Case Diagram (PlantUML)

@startuml
skinparam packageStyle rectangle
left to right direction

actor "Administrator" as Admin
actor "Operator" as Op
actor "ML Service" as ML <<autonomous>>

rectangle "AIOps Platform" {
    
    package "Surveillance & Collection" {
        usecase "UC01: Configure monitoring" as UC01
        usecase "UC02: Deploy Node Exporter" as UC02
        usecase "UC03: Consult Grafana dashboards" as UC03
    }

    package "Analysis & ML Detection" {
        usecase "UC04: Launch ML analysis" as UC04
        usecase "UC05: Retrieve metrics/logs" as UC05
        usecase "UC06: Pre-process data" as UC06
        usecase "UC07: Detect anomaly & score" as UC07
    }

    package "Alerting & Recommendations" {
        usecase "UC08: Record anomaly context" as UC08
        usecase "UC09: Generate alert" as UC09
        usecase "UC11: Notify via Discord" as UC11
        usecase "UC12: Manage alerts (Ack/Close)" as UC12
        usecase "UC13: Validate alert (Feedback)" as UC13
        usecase "UC14: Re-train model periodically" as UC14
    }

    package "Administration" {
        usecase "UC15: Containerize services" as UC15
    }
}

Admin --> UC01
Admin --> UC02
Admin --> UC15

Op --> UC03
Op --> UC12
Op --> UC13

ML --> UC04
ML --> UC05
ML --> UC06
ML --> UC07
ML --> UC08
ML --> UC14

UC09 ..> UC11 : <<include>>
UC07 ..> UC09 : triggers

@enduml
