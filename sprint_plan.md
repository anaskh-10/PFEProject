# Sprint Planning

The project followed the **Scrum** methodology across **9 sprints** (2 weeks each) from February to June 2026.

| Sprint | Period | US | Objectives |
|:---|:---|:---|:---|
| **Sprint 1** | 06–19 Feb | US8 | Set up Docker environment; configure Prometheus and Node Exporter on VMs. |
| **Sprint 2** | 20 Feb–05 Mar | US2, US3 | Configure cAdvisor and postgres_exporter; create first Grafana dashboards. |
| **Sprint 3** | 06–19 Mar | US1, US3 | Validate collection pipeline; supervision tests and refine Grafana panels. |
| **Sprint 4** | 20 Mar–02 Apr | US6 | Implement threshold-based alerting; configure Alertmanager with Discord routing. |
| **Sprint 5** | 03–16 Apr | US4 | Develop ML service architecture (`app.py`, `prom_fetcher.py`, `MLModelManager`). |
| **Sprint 6** | 17–30 Apr | US4, US5 | Implement Isolation Forest on 8 metrics; expose scores via `ml_exporter.py`. |
| **Sprint 7** | 01–14 May | US4 | Implement ARIMA(1,1,1) forecasting; expose 95% confidence intervals to Prometheus. |
| **Sprint 8** | 15–28 May | US4, US7 | Optimize ML parameters; evaluate performance; implement daily summary cron job. |
| **Sprint 9** | 29 May–06 Jun | US9, US10 | Deploy Zabbix; integrate MCP intelligent agent; final testing and report. |

### Methodology Notes
- **Iteration Length**: 2 Weeks.
- **Sprint Goal**: Each sprint produces a functional increment of the platform.
- **Total Duration**: February – June 2026.
