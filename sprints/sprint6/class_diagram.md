# Sprint 6 — Class Diagram (PlantUML)
## Period: 29 May – 06 Jun | US9

@startuml
title Sprint 6: MCP Intelligent Agent

package "MCP Agent" {
    class "MCPAgent" as mcp {
        +tools: list
        +prompts: list
        +process_query(text): str
        +generate_html_dashboard(): str
    }

    class "PrometheusQueryTool" as pq_tool {
        +execute_query(promql): dict
        +execute_range_query(promql, start, end): dict
        +list_metrics(): list
    }
}

package "AIOps Platform" {
    class "Prometheus" as prom {
        +query()
    }
    class "MLService" as ml {
        +metrics: PrometheusFormat
    }
}

mcp --> pq_tool : delegates queries
pq_tool --> prom : executes PromQL
mcp ..> ml : reads anomaly/forecast metrics

note right of mcp
  The MCP Agent enables 
  Natural Language interaction
  with the monitoring stack.
end note

@enduml
