# Sequence Diagram: Isolation Forest Inference & Export Cycle

This diagram details the internal software execution flow for Sprint 6, covering the training, inference, and visualization cycles.

```mermaid
sequenceDiagram
    participant Worker as background_worker()
    participant Trainer as train_models()
    participant Predictor as make_predictions()
    participant Prom as PrometheusClient
    participant AD as AnomalyDetector
    participant Exporter as MLMetricsExporter
    participant Flask as Flask /metrics
    participant Grafana as Grafana

    rect rgb(240, 240, 240)
    Note over Worker, Exporter: Training Cycle (every 300s)
    Worker ->> Trainer: train_counter == 0
    loop for each metric in MONITORED_METRICS
        Trainer ->> Prom: query_range(lookback=2h)
        Prom -->> Trainer: DataFrame (timestamp, value)
        Trainer ->> AD: fit(values)
        AD ->> AD: scaler.fit_transform()
        AD ->> AD: IsolationForest.fit(X)
        AD -->> Trainer: is_fitted = True
        Trainer ->> Exporter: update_last_training()
    end
    end

    rect rgb(245, 245, 255)
    Note over Worker, Exporter: Inference Cycle (every 60s)
    Worker ->> Predictor: make_predictions()
    loop for each metric in MONITORED_METRICS
        Predictor ->> Prom: query_range(lookback=3h)
        Prom -->> Predictor: DataFrame
        Predictor ->> AD: predict(values)
        AD ->> AD: scaler.transform()
        AD ->> AD: model.predict(X)
        AD -->> Predictor: anomalies[] (0/1)
        Predictor ->> AD: get_anomaly_score(values)
        AD ->> AD: score_samples(X)
        AD ->> AD: normalize score [0,1]
        AD -->> Predictor: scores[]
        Predictor ->> Exporter: set_anomaly(metric, anomaly, score)
        Exporter ->> Exporter: update anomaly gauges
        Predictor ->> Exporter: increment_processed()
    end
    end

    rect rgb(240, 255, 240)
    Note over Flask, Grafana: Visualization & Scraping
    Grafana ->> Flask: GET /metrics
    Flask ->> Exporter: generate_latest(registry)
    Exporter -->> Flask: Prometheus text format
    Flask -->> Grafana: ml_anomaly_score{...}
    Grafana ->> Grafana: render dashboard panels
    end
```

### Key Logic Steps:
- **Normalization**: Data is scaled using `StandardScaler` before both training and inference.
- **Scoring**: Anomaly scores are calculated using `-model.score_samples(X)` and then normalized to a 0-1 range.
- **Persistence**: The results are stored in Prometheus Gauges, which are then exposed via a Flask endpoint for Grafana to consume.
