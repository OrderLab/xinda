# Overview

This repo contains the source code of ADR, a lightweight adaptive fail-slow detection library for distributed systems. ADR can be used as a plug-in when adding fail-slow handling code. ADR traces some built-in variables (e.g., syncOpLatency), automatically adapts the associated threshold variables to decide slowness, and invokes different levels of defined actions.

# Use Case
![Preview](https://raw.githubusercontent.com/OrderLab/xinda/master/adr/example.jpg)

The above figure shows the use case of ADR in HBase. Originally, HBase already includes tracing code for the WAL sync. The latest sync time is stored in timeInNanos (a tracing variable). It further defines two static threshold variables, slowSyncNs (line 2) and rollOnSyncNs (line3), and uses two statements (lines 5 and 8) to check if the sync time exceeds the thresholds. Different actions would be taken accordingly, emitting a warning (line 7) or rolling WAL (line 10).

With ADR, the original parameters inside the ''if'' conditions are retained but wrapped up using ADR’s APIs. Specifically, we call isWarn() in line 6 to compare the latest sync time with an adaptive threshold. Then we use isFatal() in line 9 to check if there is a continuous slowdown and frequency change (or if the latest value exceeds the default threshold). If so, a log roll would be triggered per developers’ design.

