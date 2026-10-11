# PFEProject
# Intelligent AIOps Platform for Proactive Infrastructure Monitoring

An end-to-end anomaly detection and forecasting platform built to monitor server infrastructure in real time, flag abnormal behavior before it causes downtime, and let operators query infrastructure state in natural language.

Developed as a final-year project (PFE) during an internship at Maison du Web, in collaboration with Youssef Sleti.

## Overview

The platform monitors two virtualized Ubuntu servers and tracks 8 infrastructure metrics (CPU, memory, network, and more) across both. It combines classical monitoring tools with a custom machine learning service to catch anomalies that static thresholds miss, and forecasts short-term trends so issues can be caught before they become incidents.

## Architecture

The system runs as a set of Docker Compose services across two Ubuntu VirtualBox VMs:

- **Prometheus** — metrics collection and time-series storage
- **Grafana** — dashboards and visualization, including a dedicated ML dashboard
- **Loki + Promtail** — log aggregation
- **Alertmanager** — alert routing
- **cAdvisor + Node Exporter** — container and host-level metrics
- **Custom Python ML service** — anomaly detection and forecasting (see below)
- **Sentinel AI** — a custom HTML/CSS/JS dashboard for infrastructure overview, powered by Groq's Llama 3.3 70B
- **MCP (Model Context Protocol) agent** — lets an operator query infrastructure state in natural language (via `prometheus-mcp-server`)
- **Discord webhook integration** — automated real-time alerts and daily status reports

## Machine Learning

- **Anomaly detection:** Isolation Forest, trained per metric
- **Forecasting:** ARIMA, with forecasts exported back into Prometheus so they're visible alongside live metrics
- Each of the 8 monitored metrics has its own model instance, managed through a dedicated `MLModelManager`, rather than sharing a single model across metrics

## Key engineering challenges solved

- Fixed a critical bug where all 8 metrics shared a single ARIMA model instance, causing cross-contamination between unrelated metrics; resolved with a per-metric model manager
- Resolved Loki integration issues (missing port mappings, deprecated config fields, Promtail setup)
- Fixed Alertmanager routing conflicts caused by Docker's internal DNS/networking
- Fixed a Unicode handling bug in the metrics exporter (`ml_exporter.py`)

## Tech stack

Python · Scikit-learn · Docker · Docker Compose · Prometheus · Grafana · Loki · Alertmanager · Chart.js · Groq (Llama 3.3 70B) · MCP

## Author

**Anas Khiari** — Machine Learning & Backend Developer Intern, Maison du Web
[LinkedIn](https://www.linkedin.com/in/anas-khiari-78828519a/)

Built with Youssef Sleti as part of our final-year engineering project.
