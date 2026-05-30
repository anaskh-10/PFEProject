# Sprint 3 — Class Diagram (PlantUML)
## Period: 20 Mar – 02 Apr | US5, US10

@startuml
title Sprint 3: Alerting & Zabbix Integration

package "Monitoring Core" {
    class "PrometheusRule" as rule {
        +alert: string
        +expr: PromQL
        +for: duration
        +labels: severity
        +annotations: string
    }

    class "Alertmanager" as am {
        +receivers: list
        +route(alert)
    }

    class "DiscordWebhook" as discord {
        +url: string
        +send_payload(data)
    }
}

package "Complementary Layer" {
    class "ZabbixServer" as zabbix {
        +hosts: list
        +items: list
        +triggers: list
        +get_latest_data()
    }

    class "ZabbixAgent" as agent {
        +service: status
        +metrics: raw
    }
}

rule ..> am : fires alert
am --> discord : notifies via
zabbix "1" *-- "many" agent : monitors
zabbix ..> discord : alternate alerts (optional)

note bottom of zabbix
  Zabbix provides an independent 
  infrastructure monitoring layer
  alongside Prometheus.
end note

@enduml
