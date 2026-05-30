# Sprint 4 — Sequence Diagram (PlantUML)
## Period: 03 – 30 Apr | US6, US8

@startuml
title Sprint 4: Isolation Forest Inference & Export Cycle

participant "background_worker()" as Worker
participant "train_models()" as Trainer
participant "make_predictions()" as Predictor
participant "PrometheusClient" as Prom
participant "AnomalyDetector" as AD
participant "AlertClassifier" as AC
participant "MLMetricsExporter" as Exporter
participant "Grafana" as Grafana

== Training Cycle (every 300s) ==
Worker -> Trainer : train_counter == 0
loop for each metric in MONITORED_METRICS
    Trainer -> Prom : query_range(query, lookback=2h, step='1m')
    Prom --> Trainer : DataFrame(timestamp, value)
    Trainer -> AD : fit(values)
    AD --> Trainer : is_fitted = True
end
Trainer -> AC : fit(X_train, y_train)
AC --> Trainer : is_fitted = True

== Inference Cycle (every 60s) ==
Worker -> Predictor : make_predictions()
loop for each metric in MONITORED_METRICS
    Predictor -> Prom : query_range(query, lookback=3h)
    Prom --> Predictor : DataFrame
    Predictor -> AD : predict(values)
    AD --> Predictor : anomalies[] (0 or 1)
    
    alt if anomaly detected
        Predictor -> AC : predict(context_features)
        AC --> Predictor : severity (low/med/high)
    end

    Predictor -> AD : get_anomaly_score(values)
    AD --> Predictor : scores[] in [0,1]
    Predictor -> Exporter : set_anomaly(metric, anomaly, score, severity)
    Exporter -> Exporter : anomaly_score.labels().set()

== Scraping ==
Grafana -> "Flask /metrics" as Flask : GET /metrics
Flask -> Exporter : generate_latest(registry)
Exporter --> Flask : ml_anomaly_score{metric=...}
Flask --> Grafana : Prometheus text format
Grafana --> Grafana : render anomaly score panels

@enduml
