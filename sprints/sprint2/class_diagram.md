# Sprint 2 — Class Diagram (PlantUML)
## Period: 20 Feb – 19 Mar | US2, US3, US4

@startuml
title Sprint 2: Metric Collection & Visualization Architecture

package "Collection Layer" {
    class "prometheus.yml" as prom_cfg {
        +global_interval: 15s
        +scrape_configs: list
        +rule_files: list
    }

    class "Node Exporter" as node_exp {
        +image: prom/node-exporter
        +port: 9100
        +expose: [cpu, ram, disk, network]
    }

    class "cAdvisor" as cadvisor {
        +image: gcr.io/cadvisor
        +port: 8080
        +expose: [container_cpu, container_mem]
    }

    class "postgres_exporter" as pg_exp {
        +port: 9187
        +expose: [pg_connections]
    }
}

package "Visualization Layer" {
    class "Grafana" as grafana {
        +port: 3000
        +datasource: Prometheus
        +dashboards: list
    }
}

prom_cfg ..> node_exp : scrapes :9100/metrics
prom_cfg ..> cadvisor : scrapes :8080/metrics
prom_cfg ..> pg_exp : scrapes :9187/metrics
grafana ..> prom_cfg : queries PromQL

@enduml
