# Sprint 6 — Use Case Diagram (PlantUML)
## Period: 29 May – 06 Jun | US9

@startuml
left to right direction
skinparam packageStyle rectangle

actor Operator as op
actor "MCP Agent" as agent <<system>>

rectangle "AIOps Platform — Sprint 6" {
    usecase "US9: Query metrics via\nNatural Language" as UC9
    usecase "Perform statistical analysis\nof system health" as UC9a
    usecase "Generate dynamic\nHTML Dashboards" as UC9b
    usecase "Execute PromQL queries\nautonomously" as UC9c
}

op --> UC9
op --> UC9b
agent --> UC9c
agent --> UC9a

UC9 ..> UC9c : <<include>>
UC9b ..> UC9c : <<include>>

@enduml
