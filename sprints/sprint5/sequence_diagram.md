# Sprint 5 — Sequence Diagram (PlantUML)
## Period: 01 – 28 May | US7

@startuml
title Sprint 5: ARIMA Training & Forecasting Cycle

participant "background_worker" as Worker
participant "Prometheus" as Prom
participant "TimeSeriesForecaster" as ARIMA
participant "MLMetricsExporter" as Exporter
participant "Grafana" as Grafana

== Forecasting Cycle (every 60s) ==
Worker -> Worker : check train_counter
alt model needs training
    Worker -> Prom : fetch history (lookback=2h)
    Prom --> Worker : historic values
    Worker -> ARIMA : fit(data)
    ARIMA -> ARIMA : find optimal parameters
    ARIMA --> Worker : is_fitted = True
end

Worker -> ARIMA : forecast(steps=60)
ARIMA -> ARIMA : compute mean & stderr
ARIMA --> Worker : preds, lower_ci, upper_ci

Worker -> Exporter : set_forecast(metric, preds[-1])
Worker -> Exporter : set_forecast_bounds(metric, lower, upper)

== Visualization ==
Grafana -> Prom : Query forecast metrics
Prom --> Grafana : Forecast data points
Grafana -> Grafana : Render time-series\nwith confidence ribbons

@enduml
