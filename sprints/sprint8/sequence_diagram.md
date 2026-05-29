# Sprint 8: Sequence Diagram
## Goal: Optimization and Daily Summaries.

```mermaid
sequenceDiagram
    participant Cron as Cron Job
    participant App as ML Service
    participant Disc as Discord

    Cron ->> App: Trigger /api/summary
    App ->> App: Performance Evaluation
    App ->> Disc: POST "Daily AIOps Report"
```
