# Global Class Diagram (PlantUML)

@startuml
title AIOps Platform — Unified Architecture

package "Observation Layer" {
    class "NodeExporter" as node
    class "cAdvisor" as cadvisor
    class "ZabbixAgent" as z_agent
}

package "Core Monitoring" {
    class "Prometheus" as prom {
        +scrape()
        +query()
    }
    class "Alertmanager" as am {
        +route()
    }
    class "ZabbixServer" as z_server {
        +monitor()
    }
}

package "Machine Learning Service" {
    class "MLModelManager" as mgr {
        -anomaly_detectors: dict
        -forecasters: dict
        -classifier: AlertClassifier
        +save_models()
        +load_models()
    }

    class "AnomalyDetector" as ad {
        +fit()
        +predict()
    }

    class "TimeSeriesForecaster" as forecaster {
        +fit()
        +forecast()
    }
    
    class "AlertClassifier" as classifier {
        +predict_severity()
    }

    class "MLMetricsExporter" as exporter {
        +anomaly_score: Gauge
        +forecast_value: Gauge
    }
}

package "Intelligence Layer" {
    class "MCPAgent" as mcp {
        +process_query()
    }
    class "PrometheusTool" as tool {
        +execute_promql()
    }
}

node --> prom : metrics
cadvisor --> prom : metrics
z_agent --> z_server : metrics

mgr *-- ad
mgr *-- forecaster
mgr *-- classifier
mgr --> exporter : exports results

prom --> mgr : training data
exporter --> prom : ML metrics
prom --> am : fires alerts

mcp --> tool : uses
tool --> prom : queries

@enduml
