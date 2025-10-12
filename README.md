# Mini Distributed Warehouse Management System

A gRPC-based distributed warehouse management system for CSE 5306 Distributed Systems course. The system uses a layered architecture, supports 5 core functions, and runs on 6 containerized nodes.

## 🎯 Project Overview

**What is this?**

- Distributed warehouse management system
- Uses gRPC for inter-service communication
- Supports CRUD operations and order processing
- Includes centralized logging

**Architecture Design:**

```
┌─────────────────┐
│   API Gateway   │ ← Client request entry point
│   (Port 50050)  │
└─────────┬───────┘
          │ gRPC
┌─────────▼───────┐
│ Middle Services │
│ Food (50052)    │
│ Electronics(50051)│
└─────────┬───────┘
          │ gRPC
┌─────────▼───────┐
│ Bottom Services │
│ Fresh (50053)   │
│ Appliance(50054)│
└─────────────────┘
          │ gRPC
┌─────────▼───────┐
│ Logger Service  │ ← Centralized logging
│ (Port 50055)    │
└─────────────────┘
```

## 📋 Core Functions

1. **Add Item Resource** - Add new items to the warehouse system
2. **Update Item Resource** - Modify existing item information
3. **Take Item Resource** - Process orders and reduce inventory
4. **Query Item Resource** - Query items by category, stock level, etc.
5. **Distributed Logging** - Centralized logging of all operations

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- gRPC tools

### Setup Steps

1. **Clone Repository**

```bash
git clone https://github.com/zz9tf/Mini-Distributed-Warehouse-Management-System.git
cd Mini-Distributed-Warehouse-Management-System
```

2. **Generate Protocol Buffers**

```bash
./regenerate_proto.sh
```

3. **Start System**

```bash
# Full startup (cleans old containers)
./dev.sh

# Or simple startup
docker compose up
```

4. **Stop System**

```bash
# Ctrl+C to stop, or run
docker-compose down
```

5. **Performance Testing**

```bash
python test_client.py
```

## 📁 Project Structure

```
├── api_gateway.py               # API Gateway service
├── logger_service.py            # Logging service
├── test_client.py               # Performance testing client
├── services/                    # Business services
│   ├── food_service.py          # Food service
│   ├── electronics_service.py   # Electronics service
│   ├── fresh_service.py         # Fresh products service
│   └── appliance_service.py     # Appliance service
├── docker-compose.yml           # Container orchestration
├── warehouse.proto              # gRPC protocol definitions
└── dev.sh                       # Startup script
```

## 📊 Performance Results

- **No Logging Mode**: 2200+ QPS, 2.2ms latency
- **With Logging Mode**: 43-92 QPS, 53-112ms latency
- **Logging Impact**: 95-98% throughput reduction
