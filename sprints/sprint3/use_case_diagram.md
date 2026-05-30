# Sprint 3 — Use Case Diagram (PlantUML)
## Period: 20 Mar – 02 Apr | US5, US10

@startuml
left to right direction
skinparam packageStyle rectangle

actor Administrator as admin
actor Operator as op

rectangle "AIOps Platform — Sprint 3" {
    package "Alerting (US5)" {
        usecase "Configure Alertmanager\n& Discord Routing" as UC5a
        usecase "Define Prometheus\nAlert Rules" as UC5b
        usecase "Receive Discord\nAlert" as UC5d
    }
    
    package "Complementary (US10)" {
        usecase "US10: Deploy Zabbix\nMonitoring Layer" as UC10
        usecase "Configure Zabbix\nHosts & Triggers" as UC10a
    }
}

admin --> UC5a
admin --> UC5b
admin --> UC10
admin --> UC10a
op    --> UC5d

UC5b ..> UC5a : <<triggers>>
UC10a ..> UC10 : <<include>>

@enduml
