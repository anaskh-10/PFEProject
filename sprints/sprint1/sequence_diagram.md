# Sprint 1: Sequence Diagram (PlantUML)

@startuml
title Sprint 1: Initial Scrape Lifecycle

actor Administrator as admin
participant "Docker Compose" as docker
participant Prometheus as prom
participant "Node Exporter" as node

admin -> docker : docker-compose up -d
docker -> node : launch container
docker -> prom : launch container

group Periodic Metric Collection
    prom -> node : GET /metrics
    node --> prom : HTTP 200 (metrics text)
end

@enduml
