# Sprint 9: Class Diagram

```mermaid
classDiagram
    class MCPAgent {
        +tools
        +prompts
        +process_query(text)
    }
    class ZabbixServer {
        +hosts
        +items
        +triggers
    }
    class AIOpsPlatform {
        +Prometheus
        +MLService
        +Zabbix
    }

    MCPAgent ..> AIOpsPlatform : interacts with
    AIOpsPlatform *-- ZabbixServer : integrates
```
