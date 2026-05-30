# Sprint Planning

The project followed the **Scrum** agile methodology, organized into **6 sprints** (originally planned as 9), spanning from February to June 2026. Each sprint produces a functional increment of the platform.

| Sprint | Period | US | Objectives |
|:---|:---|:---|:---|
| **Sprint 1** | 06–19 Feb | US1 | Set up the Docker environment; install and configure Docker Compose for reproducible deployment of all platform services on both virtual machines. |
| **Sprint 2** | 20 Feb–19 Mar | US2, US3, US4 | Install Node Exporter and configure Prometheus with cAdvisor for system and container metric collection; create Grafana dashboards for real-time infrastructure visualization; validate the complete metric collection pipeline and refine dashboard panels. |
| **Sprint 3** | 20 Mar–02 Apr | US5, US10 | Implement threshold-based alerting rules in Prometheus; configure Alertmanager with Discord routing and validate the end-to-end notification pipeline; deploy Zabbix as a complementary monitoring layer to provide additional infrastructure visibility alongside Prometheus. |
| **Sprint 4** | 03–30 Apr | US6, US8 | Develop the ML service architecture (`app.py`, `prom_fetcher.py`); implement data preprocessing and the `MLModelManager`; deploy Isolation Forest anomaly detection for all 8 metrics; expose anomaly scores via `ml_exporter.py`; configure the detection threshold to tune alerting sensitivity. |
| **Sprint 5** | 01–28 May | US7 | Implement ARIMA(1,1,1) forecasting; expose predictions and 95% confidence intervals to Prometheus; visualize forecast results in Grafana; optimize ML model parameters and evaluate detection performance. |
| **Sprint 6** | 29 May–06 Jun | US9 | Integrate the MCP intelligent agent for natural language querying and HTML dashboard generation; perform end-to-end testing and final report preparation. |

### Methodology Notes
- **Iteration Length**: 2–4 weeks per sprint.
- **Sprint Goal**: Each sprint produces a functional increment of the platform.
- **Total Duration**: February – June 2026.
