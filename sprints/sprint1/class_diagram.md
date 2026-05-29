# Sprint 1: Class Diagram (PlantUML)

@startuml
title Sprint 1: Infrastructure Deployment

class "docker-compose.yml" as compose {
    +version: "3.8"
    +services: list
    +up()
    +down()
}

class "prometheus.yml" as prom_cfg {
    +global: dict
    +scrape_configs: list
    +rule_files: list
}

class "Node Exporter" as node_exp {
    +image: quay.io/prometheus/node-exporter
    +ports: [9100]
}

compose *-- prom_cfg : defines
compose *-- node_exp : defines
prom_cfg ..> node_exp : target
@enduml
