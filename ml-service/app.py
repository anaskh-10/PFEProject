from flask import Flask, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging
import time
from datetime import datetime, timedelta
from threading import Thread
import os

from ml_models import MLModelManager
from prom_fetcher import PrometheusClient
from ml_exporter import MLMetricsExporter

# ========================
# LOGGING
# ========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========================
# INIT
# ========================
app = Flask(__name__)

ml_manager = MLModelManager()
prom_client = PrometheusClient(
    url=os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
)
ml_exporter = MLMetricsExporter()

# ========================
# METRICS
# ========================
MONITORED_METRICS = {
    # Use min() for idle/available stats to get the MAXIMUM usage across all servers
    'cpu': '100 - (min(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
    'memory': '(1 - min(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    'disk': '(1 - min(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100',
    
    # Use sum() or max() for accumulating metrics
    'network_in': 'max(rate(node_network_receive_bytes_total{device!="lo"}[5m]))',
    'network_out': 'max(rate(node_network_transmit_bytes_total{device!="lo"}[5m]))',
    'pg_connections': 'max(pg_stat_activity_count)',
    'container_cpu': 'max(rate(container_cpu_usage_seconds_total{name!=""}[5m])) * 100',
    'container_memory': 'max(container_memory_usage_bytes{name!=""})'
}

TRAINING_INTERVAL = 300
PREDICTION_INTERVAL = 60

# ========================
# FETCH DATA
# ========================
def fetch_metric_data(metric_query, lookback_hours=2):
    try:
        end = datetime.utcnow()
        start = end - timedelta(hours=lookback_hours)
        return prom_client.query_range(metric_query, start, end, step='1m')
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return None


# ========================
# TRAIN MODELS
# ========================
def train_models():
    logger.info("=" * 50)
    logger.info("TRAINING MODELS")
    logger.info("=" * 50)

    for metric_name, query in MONITORED_METRICS.items():
        try:
            data = fetch_metric_data(query)

            if data is None or data.empty:
                logger.warning(f"No data for {metric_name}")
                ml_exporter.increment_error('training', 'no_data')
                continue

            values = data['value']

            ml_manager.anomaly_detectors[metric_name].fit(values)
            ml_manager.forecasters[metric_name].fit(values)

            ml_exporter.update_last_training('all_models', datetime.utcnow().timestamp())

            logger.info(f"✓ Trained {metric_name}")

        except Exception as e:
            logger.error(f"Training failed {metric_name}: {e}")
            ml_exporter.increment_error('training', str(type(e).__name__))

    logger.info("=" * 50)


# ========================
# PREDICTIONS
# ========================
def make_predictions():
    for metric_name, query in MONITORED_METRICS.items():
        try:
            data = fetch_metric_data(query, lookback_hours=3)

            if data is None or data.empty:
                logger.warning(f"No data for {metric_name}")
                ml_exporter.increment_error('prediction', 'no_data')
                continue

            values = data['value']

            # Anomaly detection
            anomalies = ml_manager.anomaly_detectors[metric_name].predict(values)
            scores = ml_manager.anomaly_detectors[metric_name].get_anomaly_score(values)

            if len(anomalies) > 0:
                ml_exporter.set_anomaly(
                    metric_name,
                    int(anomalies[-1]),
                    float(scores[-1])
                )

            # Forecast
            forecast = ml_manager.forecasters[metric_name].forecast(12)

            if len(forecast) > 0:
                ml_exporter.set_forecast(metric_name, float(forecast[0]), 1)

            ml_exporter.increment_processed(metric_name, 'all_models')

            logger.info(f"✓ Predictions made for {metric_name}")

        except Exception as e:
            logger.error(f"Prediction error for {metric_name}: {e}")
            ml_exporter.increment_error('prediction', str(type(e).__name__))


# ========================
# BACKGROUND WORKER
# ========================
def background_worker():
    logger.info("🚀 Background worker started")

    train_counter = 0

    while True:
        try:
            if train_counter == 0:
                train_models()

            make_predictions()

            train_counter += PREDICTION_INTERVAL
            if train_counter >= TRAINING_INTERVAL:
                train_counter = 0

            time.sleep(PREDICTION_INTERVAL)

        except Exception as e:
            logger.error(f"Worker error: {e}")
            time.sleep(10)


# ========================
# ROUTES
# ========================
@app.route('/health')
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})


@app.route('/metrics')
def metrics():
    return generate_latest(ml_exporter.registry), 200, {
        'Content-Type': CONTENT_TYPE_LATEST
    }


@app.route('/api/anomalies')
def anomalies():
    result = []

    for metric in MONITORED_METRICS:
        try:
            result.append({
                "metric": metric,
                "score": float(ml_exporter.anomaly_score.labels(metric_name=metric)._value.get()),
                "is_anomaly": int(ml_exporter.anomaly_detected.labels(metric_name=metric)._value.get())
            })
        except:
            pass

    return jsonify(result)


@app.route('/api/forecast/<metric_name>')
def forecast(metric_name):

    if metric_name not in MONITORED_METRICS:
        return jsonify({"error": "unknown metric"}), 400

    forecast = ml_manager.forecasters[metric_name].forecast(12)

    return jsonify({
        "metric": metric_name,
        "forecast": forecast.tolist() if len(forecast) > 0 else []
    })


@app.route('/api/status')
def status():
    return jsonify({
        "status": "running",
        "models": {
            "anomaly_detectors": {
                k: v.is_fitted for k, v in ml_manager.anomaly_detectors.items()
            },
            "forecasters": {
                k: v.is_fitted for k, v in ml_manager.forecasters.items()
            }
        },
        "metrics": list(MONITORED_METRICS.keys())
    })


# ========================
# MAIN
# ========================
def main():
    logger.info("🚀 Starting ML Service")

    Thread(target=background_worker, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
