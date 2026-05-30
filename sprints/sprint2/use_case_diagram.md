# Sprint 2 — Use Case Diagram (PlantUML)
## Period: 20 Feb – 19 Mar | US2, US3, US4

@startuml
left to right direction
skinparam packageStyle rectangle

actor Administrator as admin
actor Operator as op

rectangle "AIOps Platform — Sprint 2" {
    usecase "US2: Install Node Exporter\n(expose /metrics)" as UC2
    usecase "US3: Configure Prometheus\n& cAdvisor collection" as UC3
    usecase "US4: Create Grafana\nDashboards" as UC4
    usecase "Validate Collection\nPipeline" as UC_VAL
}

admin --> UC2
admin --> UC3
admin --> UC4
admin --> UC_VAL
op    --> UC4

UC3 ..> UC_VAL : <<include>>

@enduml
