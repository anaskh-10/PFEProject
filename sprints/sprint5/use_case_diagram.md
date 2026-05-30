# Sprint 5 — Use Case Diagram (PlantUML)
## Period: 01 – 28 May | US7

@startuml
left to right direction
skinparam packageStyle rectangle

actor "ML Service" as ml <<autonomous>>
actor Operator as op

rectangle "AIOps Platform — Sprint 5" {
    usecase "US7: Forecast future metrics\nvia ARIMA" as UC7
    usecase "Expose predictions\nwith 95% CI" as UC7a
    usecase "Visualize forecasts\nin Grafana" as UC7b
    usecase "Identify capacity issues\nin advance" as UC7c
}

ml --> UC7
ml --> UC7a
op --> UC7b
op --> UC7c

UC7a ..> UC7 : <<include>>
UC7b ..> UC7a : <<consumes>>
UC7c ..> UC7b : <<extends>>

@enduml
