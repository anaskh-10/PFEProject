"""
ML Models for AIOps Platform
- Anomaly Detection
- Time Series Forecasting
- Alert Classification
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
import joblib
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================
# ANOMALY DETECTION
# =========================
class AnomalyDetector:
    """Detect anomalies using Isolation Forest"""

    def __init__(self, contamination=0.05):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, data):
        if len(data) < 20:
            logger.warning("Not enough data to train anomaly detector")
            return False

        try:
            X = self.scaler.fit_transform(data.values.reshape(-1, 1))
            self.model.fit(X)
            self.is_fitted = True
            logger.info(f"✓ Anomaly detector trained on {len(data)} samples")
            return True
        except Exception as e:
            logger.error(f"✗ Anomaly detector training failed: {e}")
            return False

    def predict(self, data):
        if not self.is_fitted:
            return np.zeros(len(data))

        try:
            X = self.scaler.transform(data.values.reshape(-1, 1))
            predictions = self.model.predict(X)
            return (predictions == -1).astype(int)
        except Exception as e:
            logger.error(f"✗ Prediction failed: {e}")
            return np.zeros(len(data))

    def get_anomaly_score(self, data):
        if not self.is_fitted:
            return np.zeros(len(data))

        try:
            X = self.scaler.transform(data.values.reshape(-1, 1))
            scores = -self.model.score_samples(X)

            min_score, max_score = scores.min(), scores.max()
            if max_score - min_score == 0:
                return np.zeros(len(data))

            return (scores - min_score) / (max_score - min_score)
        except Exception as e:
            logger.error(f"✗ Score calculation failed: {e}")
            return np.zeros(len(data))


# =========================
# TIME SERIES FORECASTING
# =========================
class TimeSeriesForecaster:
    """Forecast time series using ARIMA"""

    def __init__(self, order=(2, 1, 2)):
        self.order = order
        self.model = None
        self.is_fitted = False

    def fit(self, data):
        if len(data) < 20: #if we have less than 20 data points or 20 min of history, we can't train the model
            logger.warning("Not enough data for ARIMA training")
            return False

        try:
            self.model = ARIMA(data, order=self.order).fit()
            self.is_fitted = True
            logger.info("✓ ARIMA model trained")
            return True
        except Exception as e:
            logger.error(f"✗ ARIMA training failed: {e}")
            return False

    def forecast(self, steps=12):
        if not self.is_fitted or self.model is None:
            return np.array([])

        try:
            forecast = self.model.get_forecast(steps=steps)
            return forecast.predicted_mean.values
        except Exception as e:
            logger.error(f"✗ Forecasting failed: {e}")
            return np.array([])

    def forecast_with_confidence(self, steps=12, confidence=0.95):
        if not self.is_fitted or self.model is None:
            return None, None, None

        try:
            forecast = self.model.get_forecast(steps=steps)
            ci = forecast.conf_int(alpha=1 - confidence)#let the model calculate the upper and lower bounds of the forecast with 5% room for error

            return (
                forecast.predicted_mean.values,
                ci.iloc[:, 0].values,
                ci.iloc[:, 1].values
            )
        except Exception as e:
            logger.error(f"✗ Forecasting with CI failed: {e}")
            return None, None, None


# =========================
# ALERT CLASSIFIER
# =========================
class AlertClassifier:
    """Classify alerts by severity"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_fitted = False
        self.classes = {0: 'low', 1: 'medium', 2: 'high', 3: 'critical'}

    def fit(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
            logger.info("✓ Alert classifier trained")
            return True
        except Exception as e:
            logger.error(f"✗ Classifier training failed: {e}")
            return False

    def predict(self, X):
        if not self.is_fitted:
            return np.zeros(len(X), dtype=int)
        return self.model.predict(X)

    def get_severity_name(self, pred):
        return self.classes.get(pred, 'unknown')


# =========================
# MODEL MANAGER (FIXED)
# =========================
class MLModelManager:
    """Manage all ML models"""

    def __init__(self):
        # Anomaly detectors
        self.anomaly_detectors = {
            'cpu': AnomalyDetector(),
            'memory': AnomalyDetector(),
            'disk': AnomalyDetector(),
            'network_in': AnomalyDetector(),
            'network_out': AnomalyDetector(),
            'pg_connections': AnomalyDetector(),
            'container_cpu': AnomalyDetector(),
            'container_memory': AnomalyDetector()
        }

        # Forecasters
        self.forecasters = {
            'cpu': TimeSeriesForecaster(),
            'memory': TimeSeriesForecaster(),
            'disk': TimeSeriesForecaster(),
            'network_in': TimeSeriesForecaster(),
            'network_out': TimeSeriesForecaster(),
            'pg_connections': TimeSeriesForecaster(),
            'container_cpu': TimeSeriesForecaster(),
            'container_memory': TimeSeriesForecaster()
        }

        # Alert classifier (kept ✅)
        self.classifier = AlertClassifier()

    def save_models(self, path='./models'):
        import os
        os.makedirs(path, exist_ok=True)

        joblib.dump(self.anomaly_detectors, f'{path}/anomaly_detectors.pkl')
        joblib.dump(self.forecasters, f'{path}/forecasters.pkl')
        joblib.dump(self.classifier, f'{path}/classifier.pkl')

        logger.info(f"✓ Models saved to {path}")

    def load_models(self, path='./models'):
        try:
            self.anomaly_detectors = joblib.load(f'{path}/anomaly_detectors.pkl')
            self.forecasters = joblib.load(f'{path}/forecasters.pkl')
            self.classifier = joblib.load(f'{path}/classifier.pkl')

            logger.info(f"✓ Models loaded from {path}")
            return True
        except Exception as e:
            logger.warning(f"Could not load models: {e}")
            return False
