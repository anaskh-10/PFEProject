# Sprint 1: Use Case Diagram (PlantUML)

@startuml
left to right direction
skinparam packageStyle rectangle

actor Administrator as admin

rectangle "AIOps Platform (Sprint 1)" {
  usecase "US8: Containerize Services" as UC1
  usecase "US1: Configure Collection" as UC2
  usecase "US2: Deploy Node Exporter" as UC3
}

admin --> UC1
admin --> UC2
admin --> UC3

@enduml
