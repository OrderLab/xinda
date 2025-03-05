# Development Guide

In this guide, we will walk you through how to extend Xinda to support a new fault injection method, a new benchmark, or a new distributed system. This guide can act as a checkbox for future development.

## Basics

```log
🏠 xinda
  ┣ ...
  ┣ main.py                 (main entry of Xinda)
  ┣ 📈 data-analysis/       (data analysis scripts)
  ┣ 🔧 tools/               (binaries and utilities)
  ┣ xinda                   (source files of Xinda)
    ┣ 🤖️ systems
      ┣ container.yaml      (container meta info)
      ┣ TestSystem.py       (base class for distributed systems)
      ┣ hbase.py            (hbase support based on TestSystem)
      ┣ crdb.py             (crdb support based on TestSystem)
      ┣ ...
    ┣ 📒 configs            (main Xinda configurations)
      ┣ benchmark.py        (benchmark configs)
      ┣ logging.py          (data collection configs)
      ┣ slow_fault.py       (slow fault attributes)
      ┣ tool.py             (a collection of binaries and utilities)
      ┣ reslim.py           (base class to enforce resource limits)
```

Above showcases the main structure and modules of Xinda. Let's go through them one by one:

* [main.py](../main.py) is the main entry of Xinda. All configurations, including the system under test, the benchmarks to be run, and slow-fault attributes, are passed through here

* [data-analysis/](../data-analysis) contains scripts to parse and analyze the runtime logs and stats collected by Xinda

* [tools/](../tools/) contains the requried binaries and utilities .

* [container.yaml](../xinda/systems/container.yaml) records legal container names of all supported distributed systems. It is used by a sanity check to ensure the user input of `--fault_location` is valid

* [TestSystem](../xinda/systems/TestSystem.py) is the base class to implement all distributed systems in Xinda. It has already implemented basic functions like:
    + `docker_up()` and `docker_down()` to bring up/down the cluster
    + `blockade_up()` and `blockade_down()` to init/shut down Blockade (which is used to inject network-related slow faults)
    + `charybdefs_up()` and `charybdefs_down()` to init/shut down CharybdeFS (which is used to inject filesystem-related slow faults)
    + `inject()` to inject slow faults at a specific time, wait for a duration, and then clear the fault
    + `info()` to log INFO messages
    + `cleanup()` to clean up the system (e.g., docker containers, Blockade, CharybdeFS, etc.) for next test

* [Benchmark](../xinda/configs/benchmark.py) and its subclasses are used to pass benchmark-related configurations to the system

* [Logging](../xinda/configs/logging.py) records the path to runtime logs and stats that we want to collect. System-specific logs are also implemented here

* [SlowFault](../xinda/configs/slow_fault.py) is the base class to record slow-fault attributes, like fault type, location, start time, duration, etc.

* [Tool](../xinda/configs/tool.py) records the path to important binaries and utilities that are used by Xinda, like the Blockade binary, YCSB binary, etc.

* [ResourceLimit](../xinda/configs/reslim.py) is the base class to record CPU/memory limits of each container instance. It can be used as a reference if you want to control other conditions in the future

## 1. Support a New Fault Injection Tool

The following modules should be adapted: 
* [TestSystem](../xinda/systems/TestSystem.py): shell commands to initilize the tool, inject faults, clear faults, and gracefully shut down the tool should be added. This means that we shall at least implement two new functions: `tool_up()` and `tool_down()` for initilization and shutdown. We also need to modify the `inject()` function to invoke proper `cmd_inject` and `cmd_clear` commands

* [tools/](../tools/) and [Tool](../xinda/configs/tool.py): update binaries of the new tool

* (Optional) [Logging](../xinda/configs/logging.py): if needed, log paths of the new tool should be added. However, fault injection tools usually do not generate useful logs for our analysis

## 2. Support a New Benchmark

Suppose we want to support a new benchmark in system `DummySys`. At least the following modules should be adapted:

* [main.py](../main.py) and [Benchmark](../xinda/configs/benchmark.py): add new benchmark flags and configurations

* [Logging](../xinda/configs/logging.py): add new path to record runtime logs of the benchmark

* [tools/](../tools/) and [Tool](../xinda/configs/tool.py): update binaries and utilities of the benchmark

* DummySys.py: in the `DummySys` class, we need to add function support to bring up the new benchmark, run the benchmark with different parameters, collect benchmark logs, and shut down the benchmark. Let's take YCSB in [etcd](../xinda/systems/etcd.py) as an example. We have implemented the following functions:
    + `_load_ycsb()` and `_run_ycsb()` to initialize and run YCSB workloads. [Benchmark](../xinda/configs/benchmark.py) configs will be passed here. Benchmark binaries or utilities from [Tool](../xinda/configs/tool.py) and [tools/](../tools/) will be invoked here. Runtime logs will be redirected to the path in [Logging](../xinda/configs/logging.py)
    + (Optional) `_wait_till_ycsb_ends()` to wait till benchmark ends. Some benchmarks can be configured to run for a specific duration and thus do not need to add this function

* [main.py](../main.py): new benchmark flags and configurations should be addded to the argument parser

* [data-analysis](../data-analysis/): a new benchmark log parser should be implemented here. The parser is mostly a collection of regular expressions to extract useful information like timestamp, throughput, latency, etc.


## 3. Support a New System

Suppose we want to support a new system named `DummySys`. At least the following modules should be adapted:

* DummySys.py: we should create a new DummySys class inherited from [TestSystem](../xinda/systems/TestSystem.py). In this class, we need to implement functions to initilize the system/benchmark/fault injection tool, run the benchmark, inject faults, collect logs, and gracefully shutdown eveything. We have already provided a few examples in implementing existing systems, including [Cassandra](../xinda/systems/cassandra.py), [HBase](../xinda/systems/hbase.py), [CRDB](../xinda/systems/crdb.py), [etcd](../xinda/systems/etcd.py), [Hadoop](../xinda/systems/mapred.py), and [Kafka](../xinda/systems/kafka.py)

*  [tools/](../tools/) and [Tool](../xinda/configs/tool.py): update binaries (if needed) of the new system. We also need to add a workable  `docker-compose` file under `tools/docker-DummySys`, similar to what we have done for [docker-hbase](../tools/docker-hbase/), [docker-etcd](../tools/docker-etcd/), etc.

*  [main.py](../main.py): create an instance of the new system with all configuration flags in the main function 

* [container.yaml](../xinda/systems/container.yaml): add the new system container names to the container list for sanity checks