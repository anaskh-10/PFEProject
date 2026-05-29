# Sprint 6: Class Diagram (PlantUML)

@startuml
title Sprint 6: Anomaly Detection Architecture

package "ML Service" {
    class MLModelManager {
        -anomaly_detectors: dict
        -forecasters: dict
        +load_models(path)
        +save_models(path)
    }

    class AnomalyDetector {
        -model: IsolationForest
        -scaler: StandardScaler
        -is_fitted: bool
        +fit(data)
        +predict(data)
        +get_anomaly_score(data)
    }
}

package "Exporter" {
    class MLMetricsExporter {
        -registry: CollectorRegistry
        -anomaly_score: Gauge
        +set_anomaly(metric, anomaly, score)
    }
}

MLModelManager "1" *-- "many" AnomalyDetector : manages
MLModelManager ..> MLMetricsExporter : updates
@enduml
