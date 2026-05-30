# Sprint 4 — Use Case Diagram (PlantUML)
## Period: 03 – 30 Apr | US6, US8

@startuml
left to right direction
skinparam packageStyle rectangle

actor Administrator as admin
actor "ML Service" as ml <<autonomous>>

rectangle "AIOps Platform — Sprint 4" {
    usecase "US6: Detect anomalies\nvia Isolation Forest" as UC6
    usecase "US8: Configure Detection\nThreshold" as UC8
    usecase "US8b: Classify Alert\nSeverity (Random Forest)" as UC8b
    usecase "Train AnomalyDetector\nper metric" as UC_T
    usecase "Expose anomaly scores\nvia ml_exporter.py" as UC_E
    usecase "Fetch metric history\nfrom Prometheus" as UC_F
}

admin --> UC8
admin --> UC6
ml    --> UC_T
ml    --> UC_E
ml    --> UC_F
ml    --> UC8b

UC6 ..> UC_T : <<include>>
UC6 ..> UC_F : <<include>>
UC8 ..> UC6 : <<extends>>
UC8b ..> UC6 : <<after>>

@enduml
