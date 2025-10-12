# Mini Distributed Warehouse Management System - Final Report

**Course**: CSE 5306 Distributed Systems  
**Semester**: Fall 2024  
**Institution**: University of Texas at Arlington
**Date**: December 2024

## Table of Contents

- [Mini Distributed Warehouse Management System - Final Report](#mini-distributed-warehouse-management-system---final-report)
  - [Table of Contents](#table-of-contents)
  - [GitHub Repository](#github-repository)
  - [System Overview](#system-overview)
    - [System Components](#system-components)
  - [Architecture Designs](#architecture-designs)
    - [Design 1: Layered Architecture (Implemented)](#design-1-layered-architecture-implemented)
    - [gRPC Communication Model (Implemented)](#grpc-communication-model-implemented)
  - [Experimental Setup](#experimental-setup)
    - [Hardware Environment](#hardware-environment)
    - [Containerized Nodes](#containerized-nodes)
    - [Workload Specifications](#workload-specifications)
    - [Latency Results](#latency-results)
    - [Throughput Results](#throughput-results)
    - [Performance Analysis](#performance-analysis)
  - [AI Tools Impact on Implementation](#ai-tools-impact-on-implementation)

## GitHub Repository

**Repository URL**: `https://github.com/zz9tf/Mini-Distributed-Warehouse-Management-System.git`

## System Overview

The **Mini Distributed Warehouse Management System** is a containerized, microservice-based distributed platform, adopting a layered architecture with gRPC-based communication.

To fulfill the five core functional requirements, each service plays a defined role within the distributed ecosystem:

**Add Item Resource** – Handled by middle-tier and bottom-tier services to register new items across product categories.

**Update Item Resource** – Propagates updates from middle-tier business logic to bottom-tier data nodes, ensuring state consistency.

**Take Item Resource** – Coordinates order fulfillment by deducting stock from the relevant bottom-tier service.

**Query Item Resource** – Exposes fast, concurrent read operations via middle-tier services that aggregate and filter warehouse data.

**Distributed Logging of Operations** – Managed by the Logger Service, which asynchronously receives and aggregates operational logs from all nodes for centralized monitoring.

### System Components

1. **API Gateway** (Port 50050) - Entry point for all client requests
2. **Middle-tier Services** - Business logic layer
   - FoodService (Port 50052)
   - ElectronicsService (Port 50051)
3. **Bottom-tier Services** - Data persistence layer
   - FreshService (Port 50053)
   - ApplianceService (Port 50054)
4. **LoggerService** (Port 50055) - Centralized logging and monitoring

## Architecture Designs

### Design 1: Layered Architecture (Implemented)

```
┌─────────────────┐
│   API Gateway   │ ← Client requests
│   (Port 50050)  │
└─────────┬───────┘
          │ gRPC
┌─────────▼───────┐
│ Middle Services │ ← Business Logic Layer
│ Food (50052)    │   (Functions 1-4)
│ Electronics(50051)│
└─────────┬───────┘
          │ gRPC
┌─────────▼───────┐
│ Bottom Services │ ← Data Persistence Layer
│ Fresh (50053)   │   (Functions 1-4)
│ Appliance(50054)│
└─────────────────┘
          │ gRPC
┌─────────▼───────┐
│ Logger Service  │ ← Centralized Logging
│ (Port 50055)    │   (Function 5)
└─────────────────┘
```

### gRPC Communication Model (Implemented)

## Experimental Setup

### Hardware Environment

**Development Environment**:

- **CPU**: Apple M4 Pro (14 cores: 10 performance + 4 efficiency cores)
- **Memory**: 24GB unified memory
- **Storage**: 926GB SSD (793GB available)
- **OS**: macOS 15.6.1 (Build 24G90)
- **Docker**: Version 28.3.2 with Docker Compose v2.39.0
- **Network**: Built-in networking with Docker bridge networking

**Container Configuration**:

- **Base Image**: Python 3.8-slim (Debian-based, ARM64 optimized for Apple Silicon)
- **Memory Limit**: 512MB per container (optimized for M4 Pro unified memory)
- **CPU Limit**: 1 core per container (utilizing M4 Pro efficiency cores)
- **Network**: Custom bridge network (warehouse-network)
- **Storage**: Container filesystem with volume mounts for logs
- **Architecture**: ARM64 (native Apple Silicon support)

### Containerized Nodes

**Total Nodes**: 6 containers

1. **api-gateway** (Port 50050)

   - **Role**: Entry point and request router
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: food-service, electronics-service, logger-service

2. **food-service** (Port 50052)

   - **Role**: Middle-tier service for food category
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: fresh-service

3. **electronics-service** (Port 50051)

   - **Role**: Middle-tier service for electronics category
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: appliance-service

4. **fresh-service** (Port 50053)

   - **Role**: Bottom-tier service for fresh products
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: None (leaf service)

5. **appliance-service** (Port 50054)

   - **Role**: Bottom-tier service for appliances
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: None (leaf service)

6. **logger-service** (Port 50055)
   - **Role**: Centralized logging and monitoring
   - **Resources**: 512MB RAM, 1 CPU core
   - **Dependencies**: None (independent service)

**Network Topology**:

```yaml
networks:
  warehouse-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

**Service Dependencies**:

```
client_test → api-gateway → food-service → fresh-service
           → electronics-service → appliance-service
           → logger-service
```

### Workload Specifications

**Test Scenarios**:

**Latency Tests**:

- **Iterations**: 30 requests per operation
- **Warmup**: 5 requests (not counted in results)
- **Operations**: ListItems, PlaceOrder, PutItem, UpdateItem
- **Data Categories**: fruits/apple, kitchen/refrigerator

**Throughput Tests**:

- **Concurrent Workers**: 5 threads
- **Duration**: 10 seconds per test
- **Target Operations**: All CRUD operations
- **Load Pattern**: Sustained concurrent load
- **Success Criteria**: 100% success rate expected

**Performance Metrics**:

- **Latency**: Average, P50, P90, P95, P99, Min, Max (milliseconds)
- **Throughput**: Requests per second (QPS)
- **Success Rate**: Percentage of successful operations
- **Error Rate**: Percentage of failed operations
- **Resource Utilization**: CPU and memory usage per container

### Latency Results

| Test Scenario      | Service    | Operation  | Count | Avg(ms) | Min(ms) | P50(ms) | P90(ms) | P95(ms) | P99(ms) | Max(ms) | Success | Failure |
| ------------------ | ---------- | ---------- | ----- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| APIGateway_NoLog   | APIGateway | ListItems  | 50    | 896.17  | 763.04  | 860.46  | 1076.30 | 1096.22 | 1160.64 | 1199.17 | 50      | 0       |
| APIGateway_NoLog   | APIGateway | PlaceOrder | 50    | 878.40  | 677.21  | 830.17  | 1054.76 | 1146.29 | 1432.43 | 1616.04 | 50      | 0       |
| APIGateway_NoLog   | APIGateway | PutItem    | 50    | 855.39  | 741.08  | 823.79  | 1005.89 | 1055.27 | 1150.68 | 1230.08 | 50      | 0       |
| APIGateway_NoLog   | APIGateway | UpdateItem | 50    | 875.76  | 757.50  | 840.94  | 1085.80 | 1121.60 | 1160.81 | 1164.62 | 50      | 0       |
| APIGateway_WithLog | APIGateway | ListItems  | 50    | 1751.47 | 1383.92 | 1704.63 | 2083.42 | 2292.09 | 2357.32 | 2359.88 | 50      | 0       |
| APIGateway_WithLog | APIGateway | PlaceOrder | 50    | 1845.20 | 1438.21 | 1646.31 | 2400.90 | 2697.49 | 2972.07 | 2981.88 | 50      | 0       |
| APIGateway_WithLog | APIGateway | PutItem    | 50    | 1819.93 | 1403.08 | 1791.37 | 2014.97 | 2089.41 | 3115.40 | 3458.42 | 50      | 0       |
| APIGateway_WithLog | APIGateway | UpdateItem | 50    | 2221.89 | 1423.58 | 2176.54 | 2482.08 | 2531.19 | 3101.35 | 3596.12 | 50      | 0       |

### Throughput Results

_Note: Throughput tests were conducted with 5 concurrent workers for 10 seconds duration. Results show the system's ability to handle concurrent requests through the API Gateway with and without logging._

| Test Scenario      | Service    | Operation  | Workers | Duration(s) | Total | Success | Failure | QPS     | LatAvg(ms) |
| ------------------ | ---------- | ---------- | ------- | ----------- | ----- | ------- | ------- | ------- | ---------- |
| APIGateway_NoLog   | APIGateway | ListItems  | 5       | 10.00       | 6616  | 6616    | 0       | 2204.17 | 2.27       |
| APIGateway_NoLog   | APIGateway | PlaceOrder | 5       | 10.00       | 6627  | 6627    | 0       | 2207.90 | 2.26       |
| APIGateway_NoLog   | APIGateway | PutItem    | 5       | 10.00       | 6634  | 6634    | 0       | 2210.22 | 2.26       |
| APIGateway_NoLog   | APIGateway | UpdateItem | 5       | 10.00       | 6593  | 6593    | 0       | 2196.46 | 2.27       |
| APIGateway_WithLog | APIGateway | ListItems  | 5       | 10.05       | 281   | 281     | 0       | 92.17   | 53.56      |
| APIGateway_WithLog | APIGateway | PlaceOrder | 5       | 10.05       | 195   | 195     | 0       | 64.03   | 77.91      |
| APIGateway_WithLog | APIGateway | PutItem    | 5       | 10.02       | 155   | 155     | 0       | 51.38   | 96.45      |
| APIGateway_WithLog | APIGateway | UpdateItem | 5       | 10.09       | 134   | 134     | 0       | 43.41   | 112.23     |

### Performance Analysis

**Key Observations**:

1. **Logging Impact on Performance**:

   **Latency Comparison (50 requests)**:

   - **No Logging**: 855-896ms average latency
   - **With Logging**: 1751-2222ms average latency
   - **Performance Impact**: 2.0-2.5x slower with logging enabled

   **Throughput Comparison (10 seconds, 5 workers)**:

   - **No Logging**: 2196-2210 QPS (extremely high performance)
   - **With Logging**: 43-92 QPS (significant performance degradation)
   - **Performance Impact**: 24-51x reduction in throughput with logging

2. **Operation Complexity Analysis**:

   **Without Logging**:

   - ListItems: 896ms avg latency, 2204 QPS
   - PlaceOrder: 878ms avg latency, 2208 QPS
   - PutItem: 855ms avg latency, 2210 QPS
   - UpdateItem: 876ms avg latency, 2196 QPS

   **With Logging**:

   - ListItems: 1751ms avg latency, 92 QPS
   - PlaceOrder: 1845ms avg latency, 64 QPS
   - PutItem: 1820ms avg latency, 51 QPS
   - UpdateItem: 2222ms avg latency, 43 QPS

3. **System Performance Characteristics**:

   - **100% success rate** across all operations in both scenarios
   - **Logging overhead is the primary bottleneck** - not operation complexity
   - **Without logging**: System achieves exceptional performance (2000+ QPS)
   - **With logging**: Performance drops dramatically due to distributed logging overhead

4. **Critical Findings**:

   - **Distributed logging adds 0.9-1.4 seconds per request** (2.0-2.5x latency increase)
   - **Logging reduces throughput by 95-98%** (from 2200+ to 43-92 QPS)
   - **Operation complexity becomes negligible** when logging is disabled
   - **LoggerService is the primary performance bottleneck** in the system

## AI Tools Impact on Implementation

AI tools can quickly help solve many problems, but I have observed that they sometimes miss certain issues. For example, when implementing logging functionality, AI occasionally overlooks specific functions, leading to code that carries risks of instability and unreliability. For complex problems, human review and adjustment remain essential to ensure system integrity and proper functionality.
