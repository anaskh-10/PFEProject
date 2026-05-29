# Sprint 6: Sequence Diagram (PlantUML)

@startuml
title Sequence Diagram — Sprint 6: Isolation Forest Inference and Export Cycle

participant "background_worker()" as Worker
participant "train_models()" as Trainer
participant "make_predictions()" as Predictor
participant "PrometheusClient" as Prom
participant "AnomalyDetector" as AD
participant "MLMetricsExporter" as Exporter
participant "Grafana" as Grafana

== Training Cycle (every 300s) ==
Worker -> Trainer : train_counter == 0
loop for each metric in MONITORED_METRICS
    Trainer -> Prom : query_range(query, lookback=2h, step='1m')
    Prom --> Trainer : DataFrame(timestamp, value)
    Trainer -> AD : fit(values)
    AD -> AD : scaler.fit_transform(values.reshape(-1,1))
    AD -> AD : IsolationForest.fit(X)
    AD --> Trainer : is_fitted = True
    Trainer -> Exporter : update_last_training('all_models', timestamp)
end

== Inference Cycle (every 60s) ==
Worker -> Predictor : make_predictions()
loop for each metric in MONITORED_METRICS
    Predictor -> Prom : query_range(query, lookback=3h)
    Prom --> Predictor : DataFrame
    Predictor -> AD : predict(values)
    AD -> AD : scaler.transform(values)
    AD -> AD : model.predict(X) → -1 or 1
    AD --> Predictor : anomalies[] (0=normal, 1=anomaly)
    Predictor -> AD : get_anomaly_score(values)
    AD -> AD : -model.score_samples(X)
    AD -> AD : normalize: (s-smin)/(smax-smin)
    AD --> Predictor : scores[] in [0,1]
    Predictor -> Exporter : set_anomaly(metric, anomalies[-1], scores[-1])
    Exporter -> Exporter : anomaly_detected.labels().set()
    Exporter -> Exporter : anomaly_score.labels().set()
    Predictor -> Exporter : increment_processed(metric, 'all_models')
end

== Scraping ==
Grafana -> "Flask /metrics" as Flask : GET /metrics
Flask -> Exporter : generate_latest(registry)
Exporter --> Flask : ml_anomaly_score{metric=...}
Flask --> Grafana : Prometheus text format
Grafana --> Grafana : render anomaly score panels

@enduml
