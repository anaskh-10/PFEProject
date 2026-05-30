# Sprint 5 — Class Diagram (PlantUML)
## Period: 01 – 28 May | US7

@startuml
title Sprint 5: ARIMA Forecasting Architecture

package "ml-service" {

    class "MLModelManager" as mgr {
        -forecasters: dict
        -anomaly_detectors: dict
    }

    class "TimeSeriesForecaster" as forecaster {
        -model: ARIMA
        -order: (1, 1, 1)
        -is_fitted: bool
        +fit(data): bool
        +forecast(steps): ndarray
        +forecast_with_confidence(steps, ci): tuple
    }

    class "MLMetricsExporter" as exporter {
        -forecast_value: Gauge
        -forecast_lower_bound: Gauge
        -forecast_upper_bound: Gauge
        +set_forecast(metric, value, steps)
        +set_forecast_bounds(metric, lower, upper)
    }
}

mgr "1" *-- "8" forecaster : manages (per metric)
mgr --> exporter : exports forecasts

@enduml
