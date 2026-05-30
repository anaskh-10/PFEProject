# Sprint 3 — Sequence Diagram (PlantUML)
## Period: 20 Mar – 02 Apr | US5, US10

@startuml
title Sprint 3: Alerting & Zabbix Data Collection

participant "Prometheus" as prom
participant "Alertmanager" as am
participant "Zabbix Server" as zabbix
participant "Zabbix Agent" as agent
participant "Discord" as discord
actor Operator as op

== Prometheus Alerting (US5) ==
prom -> prom : evaluate rules
prom -> am : alert firing
am -> discord : post to channel
discord --> op : notification

== Zabbix Monitoring (US10) ==
agent -> agent : collect sys metrics
zabbix -> agent : fetch metrics (passive/active)
agent --> zabbix : metric data
zabbix -> zabbix : evaluate triggers
zabbix -> zabbix : store in DB

note over zabbix, agent
  Zabbix operates independently 
  of the Prometheus stack to 
  ensure monitoring redundancy.
end note

@enduml
