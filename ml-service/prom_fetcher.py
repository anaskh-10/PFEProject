import requests
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PrometheusClient:

    def __init__(self, url='http://localhost:9090'):
        self.url = url
        self.session = requests.Session()

    def query_instant(self, query):
        try:
            params = {'query': query}
            response = self.session.get(
                f"{self.url}/api/v1/query",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if not result.get('data') or not result['data'].get('result'):
                return 0

            data = result['data']['result']

            values = []
            for item in data:
                values.append(float(item['value'][1]))

            # Take maximum across all series
            return max(values)

        except Exception as e:
            logger.error(f"Instant query failed: {e}")
            return 0

    def query_range(self, query, start, end, step='1m'):
        """
        Query Prometheus range API and return a single-column DataFrame
        with a 'value' column (averaged across series if multiple).
        """
        try:
            params = {
                'query': query,
                'start': start.timestamp(),
                'end': end.timestamp(),
                'step': step,
            }
            response = self.session.get(
                f"{self.url}/api/v1/query_range",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if not result.get('data') or not result['data'].get('result'):
                return pd.DataFrame()

            series_list = result['data']['result']
            if not series_list:
                return pd.DataFrame()

            # Build a dict of {timestamp -> [values across all series]}
            ts_values: dict = {}
            for series in series_list:
                for ts, val in series['values']:
                    ts_values.setdefault(ts, []).append(float(val))

            if not ts_values:
                return pd.DataFrame()

            # Aggregate multiple series by taking the max
            records = [
                {'timestamp': ts, 'value': max(vals)}
                for ts, vals in sorted(ts_values.items())
            ]

            df = pd.DataFrame(records)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
            df.set_index('timestamp', inplace=True)

            logger.info(f"✓ Fetched {len(df)} data points from Prometheus")
            return df

        except Exception as e:
            logger.error(f"Range query failed: {e}")
            return pd.DataFrame()


METRIC_QUERIES = {
    # SYSTEM
    'cpu': '100 - (min(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
    'memory': '(1 - min(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    'disk': '(1 - min(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100',

    # NETWORK — sum() ensures a single scalar series
    'network_in': 'max(rate(node_network_receive_bytes_total{device!="lo"}[5m]))',
    'network_out': 'max(rate(node_network_transmit_bytes_total{device!="lo"}[5m]))',

    # CONTAINERS (cadvisor required) — sum() ensures single series
    'container_cpu': 'max(rate(container_cpu_usage_seconds_total{name!=""}[5m])) * 100',
    'container_memory': 'max(container_memory_usage_bytes{name!=""})',

    # POSTGRES (postgres exporter required)
    'pg_connections': 'max(pg_stat_activity_count)',
}
