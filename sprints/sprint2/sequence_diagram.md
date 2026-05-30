# Sprint 2 — Sequence Diagram (PlantUML)
## Period: 20 Feb – 19 Mar | US2, US3, US4

@startuml
title Sprint 2: Metric Collection & Dashboard Validation Flow

actor Administrator as admin
participant "Docker Compose" as docker
participant "Node Exporter\n:9100" as node
participant "cAdvisor\n:8080" as cadvisor
participant "Prometheus" as prom
participant "Grafana" as grafana

admin -> docker : docker-compose up -d
docker -> node : start container
docker -> cadvisor : start container
docker -> prom : start container
docker -> grafana : start container

group Periodic Scraping (every 15s)
    prom -> node : GET /metrics
    node --> prom : cpu, memory, disk, network
    prom -> cadvisor : GET /metrics
    cadvisor --> prom : container_cpu, container_mem
end

group Dashboard Validation
    admin -> grafana : open browser :3000
    grafana -> prom : PromQL: node_cpu_seconds_total
    prom --> grafana : time series data
    grafana --> admin : renders dashboard panels
end

@enduml
