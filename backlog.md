# Product Backlog

This backlog captures the functional requirements as user stories, prioritized and estimated using Story Points (SP).

| ID | Epic | User Story | SP | Priority |
|:---|:---|:---|:---:|:---|
| **US1** | Collection | As an administrator, I want to configure Prometheus in order to collect server metrics automatically. | 8 | High |
| **US2** | Collection | As an administrator, I want to install Node Exporter in order to expose system metrics (CPU, RAM, Disk, Network). | 5 | High |
| **US3** | Visualization | As an operator, I want to visualize real-time infrastructure metrics on Grafana dashboards with anomaly/forecast panels. | 8 | High |
| **US4** | Machine Learning | As an administrator, I want to detect anomalies in real time (Isolation Forest) and forecast values (ARIMA). | 13 | High |
| **US5** | Machine Learning | As an administrator, I want to configure the anomaly detection threshold to tune sensitivity. | 5 | Medium |
| **US6** | Alerting | As an operator, I want to receive a formatted alert notification on Discord when an anomaly is detected. | 8 | High |
| **US7** | Feedback | As an operator, I want to validate an alert as a true or false positive to improve the model. | 5 | Medium |
| **US8** | Deployment | As an administrator, I want all services to be containerized using Docker and Docker Compose. | 8 | High |
| **US9** | MCP Agent | As an operator, I want to query the platform in natural language via an MCP-powered agent. | 8 | Medium |
| **US10** | Complementary | As an administrator, I want to deploy Zabbix as a complementary monitoring layer. | 5 | Medium |

**Total SP: 73**

> [!IMPORTANT]
> **Minimum Viable Product (MVP)**: US1, US2, US3, US4, US6, US8. These core features were addressed in Sprints 1–6.
