# Product Backlog

This backlog captures the functional requirements as user stories, prioritized and estimated using Story Points (SP).

| ID | Epic | User Story | SP | Priority |
|:---|:---|:---|:---:|:---|
| **US1** | Deployment | As an administrator, I want all platform services to be containerized using Docker and Docker Compose for reproducible, portable deployment. | 8 | High |
| **US2** | Collection | As an administrator, I want to install Node Exporter in order to expose system metrics (CPU, RAM, Disk, Network) via the `/metrics` endpoint. | 5 | High |
| **US3** | Collection | As an administrator, I want to configure Prometheus and cAdvisor in order to collect server and container metrics automatically. | 8 | High |
| **US4** | Visualization | As an operator, I want to visualize real-time infrastructure metrics on Grafana dashboards in order to monitor system health at a glance. | 5 | High |
| **US5** | Alerting | As an operator, I want to receive a formatted alert notification on Discord when a threshold is exceeded or an anomaly is detected, so that I can react promptly. | 8 | High |
| **US6** | Machine Learning | As an administrator, I want to detect anomalies in real time using Isolation Forest on Prometheus metrics, so that abnormal behavior is flagged automatically. | 13 | High |
| **US7** | Machine Learning | As an administrator, I want to forecast future metric values using ARIMA and expose predictions with confidence intervals to Grafana, so that capacity issues are anticipated. | 8 | High |
| **US8** | Machine Learning | As an administrator, I want to configure the anomaly detection threshold in order to tune the sensitivity of the alerting pipeline. | 5 | Medium |
| **US9** | MCP Agent | As an operator, I want to query the monitoring platform in natural language via an MCP-powered agent that returns statistical analysis and HTML dashboards. | 13 | Medium |
| **US10** | Complementary | As an administrator, I want to deploy Zabbix as a complementary monitoring layer to provide additional infrastructure visibility alongside Prometheus. | 5 | Low |

**Total SP: 78**

> [!IMPORTANT]
> **Minimum Viable Product (MVP)**: US1, US2, US3, US4, US5, US6, US7. These core features were addressed in Sprints 1–6.
