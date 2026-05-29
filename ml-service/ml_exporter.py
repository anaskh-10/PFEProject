"""
Export ML predictions to Prometheus
"""
from prometheus_client import Counter, Gauge, CollectorRegistry
import logging

logger = logging.getLogger(__name__)


class MLMetricsExporter:
    """Export ML metrics to Prometheus"""

    def __init__(self):
        self.registry = CollectorRegistry()

        # Anomaly Detection
        self.anomaly_detected = Gauge(
            'ml_anomaly_detected',
            'Is current value anomalous (0=normal, 1=anomaly)',
            labelnames=['metric_name'],
            registry=self.registry
        )

        self.anomaly_score = Gauge(
            'ml_anomaly_score',
            'Anomaly score 0-1 (higher = more anomalous)',
            labelnames=['metric_name'],
            registry=self.registry
        )

        # Forecasting
        self.forecast_value = Gauge(
            'ml_forecast_next_value',
            'Forecasted value for next period',
            labelnames=['metric_name', 'steps_ahead'],
            registry=self.registry
        )

        self.forecast_lower_bound = Gauge(
            'ml_forecast_lower_bound',
            'Forecast confidence lower bound',
            labelnames=['metric_name'],
            registry=self.registry
        )

        self.forecast_upper_bound = Gauge(
            'ml_forecast_upper_bound',
            'Forecast confidence upper bound',
            labelnames=['metric_name'],
            registry=self.registry
        )

        # Model Health
        self.model_last_update = Gauge(
            'ml_model_last_update_timestamp',
            'Unix timestamp of last model update',
            labelnames=['model_name'],
            registry=self.registry
        )

        self.data_points_processed = Counter(
            'ml_data_points_processed_total',
            'Total data points processed',
            labelnames=['metric_name', 'model_type'],
            registry=self.registry
        )

        self.processing_errors = Counter(
            'ml_processing_errors_total',
            'Total processing errors',
            labelnames=['model_type', 'error_type'],
            registry=self.registry
        )

    def set_anomaly(self, metric_name, is_anomaly, score):
        """Record anomaly detection result"""
        self.anomaly_detected.labels(metric_name=metric_name).set(is_anomaly)
        self.anomaly_score.labels(metric_name=metric_name).set(score)

    def set_forecast(self, metric_name, value, steps_ahead=1):
        """Record forecast value"""
        self.forecast_value.labels(
            metric_name=metric_name,
            steps_ahead=str(steps_ahead)
        ).set(value)

    def set_forecast_bounds(self, metric_name, lower, upper):
        """Record forecast bounds"""
        self.forecast_lower_bound.labels(metric_name=metric_name).set(lower)
        self.forecast_upper_bound.labels(metric_name=metric_name).set(upper)

    def update_last_training(self, model_name, timestamp):
        """Update last training timestamp"""
        self.model_last_update.labels(model_name=model_name).set(timestamp)

    def increment_processed(self, metric_name, model_type):
        """Increment processed counter"""
        self.data_points_processed.labels(
            metric_name=metric_name,
            model_type=model_type
        ).inc()

    def increment_error(self, model_type, error_type):
        """Increment error counter"""
        self.processing_errors.labels(
            model_type=model_type,
            error_type=error_type
        ).inc()
