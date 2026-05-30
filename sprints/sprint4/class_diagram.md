# Sprint 4 — Class Diagram (PlantUML)
## Period: 03 – 30 Apr | US6, US8

@startuml
title Sprint 4: ML Service Architecture — Isolation Forest

package "ml-service" {

    class "app.py (Flask)" as app {
        +MONITORED_METRICS: dict
        +TRAINING_INTERVAL: 300
        +PREDICTION_INTERVAL: 60
        +background_worker()
        +train_models()
        +make_predictions()
        --
        +GET /health
        +GET /metrics
        +GET /api/anomalies
        +GET /api/status
    }

    class "PrometheusClient" as prom_client {
        -url: string
        -session: Session
        +query_instant(query): float
        +query_range(query, start, end, step): DataFrame
    }

    class "MLModelManager" as mgr {
        -anomaly_detectors: dict
        -forecasters: dict
        -classifier: AlertClassifier
        +save_models()
        +load_models()
    }

    class "AnomalyDetector" as ad {
        -model: IsolationForest
        -scaler: StandardScaler
        -is_fitted: bool
        +fit(data): bool
        +predict(data): int
        +get_anomaly_score(data): float
    }

    class "AlertClassifier" as classifier {
        -model: RandomForestClassifier
        -classes: dict
        -is_fitted: bool
        +fit(X, y): bool
        +predict(X): list
        +get_severity_name(pred): str
    }

    class "MLMetricsExporter" as exporter {
        -registry: CollectorRegistry
        -anomaly_detected: Gauge
        -anomaly_score: Gauge
        +set_anomaly(metric, val, score)
        +update_last_training(model, ts)
        +increment_processed(metric, type)
        +increment_error(type, error)
    }
}

app --> prom_client : fetches data
app --> mgr : trains & predicts
app --> exporter : exports results
mgr "1" *-- "8" ad : manages (per metric)
mgr "1" *-- "1" classifier : manages (global)
mgr --> exporter : updates metrics

@enduml
