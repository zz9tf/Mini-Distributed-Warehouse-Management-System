# Mini Distributed Warehouse Management System

A distributed warehouse management system designed and implemented for CSE 5306 Distributed Systems course. This project demonstrates two distinct system architectures with different communication models, supporting five functional requirements across five containerized nodes.

## 🎯 Project Overview

This distributed system implements a warehouse management solution with two different architectural approaches:

1. **Layered Architecture** - Traditional 3-tier architecture with API Gateway, Middle-tier services, and Bottom-tier services
2. **Microservice Architecture** - Service-oriented architecture with independent, loosely-coupled services

## 🏗️ System Architecture

### Architecture 1: Layered Architecture (gRPC)

```
┌─────────────────┐
│   API Gateway   │ ← Client requests
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
```

## 📋 Functional Requirements

1. **Add Item Resource** - Add new inventory items to the warehouse system
2. **Update Item Resource** - Modify details of existing inventory items
3. **Take Item Resource** - Process and deduct items from inventory during order fulfillment
4. **Query Item Resource** - Retrieve and filter inventory data by category, stock level, or other attributes
5. **Distributed Logging of Operations** - Implement centralized logging, service discovery, and monitoring for all operations

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- gRPC tools

### 1. Clone Repository

```bash
git clone <repository-url>
cd Mini-Distributed-Warehouse-Management-System
```

### 2. Generate Protocol Buffers

```bash
./regenerate_proto.sh
```

### 3. Build and Run System

```bash
# It will clean your old containers, images, and caches
./dev.sh
```

If you just want to start it, you may want to try:

```bash
docker compose up
```

### 4. Stop System

Try to ctrl+c to stop the `docker compose up` command

```bash
docker-compose down
```

## 📁 Project Structure

```
Mini-Distributed-Warehouse-Management-System/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── docker-compose.yml           # Multi-container orchestration
├── Dockerfile                   # Container configuration
├── warehouse.proto              # gRPC service definitions
├── warehouse_pb2.py             # Generated Python protobuf classes
├── warehouse_pb2_grpc.py        # Generated gRPC service stubs
├── api_gateway.py               # API Gateway service
├── logger_service.py            # Centralized logging service
├── warehouse_logger.py          # Unified logging utility
├── test_client.py               # Performance testing client
├── services/                    # Service implementations
│   ├── food_service.py          # Food category service
│   ├── electronics_service.py   # Electronics service
│   ├── fresh_service.py         # Fresh products service
│   └── appliance_service.py     # Appliance service
├── dev.sh                       # Development helper script
└── regenerate_proto.sh          # Protocol buffer generation
```

## 🔧 Service Configuration

### Port Allocation

- **50050**: API Gateway
- **50051**: Electronics Service
- **50052**: Food Service
- **50053**: Fresh Service
- **50054**: Appliance Service
- **50055**: Logger Service

### Environment Variables

- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `SERVICE_NAME`: Service identifier for logging
- `MAX_WORKERS`: gRPC server thread pool size

## 🧪 Performance Testing

The system includes comprehensive performance testing capabilities:

### Test Scenarios

1. **Single Bottom Container** - Direct access to one bottom-tier service
2. **Two Bottom Containers** - Concurrent access to two bottom-tier services
3. **Single Middle Container** - Direct access to one middle-tier service
4. **Two Middle Containers** - Concurrent access to two middle-tier services
5. **API Gateway Performance** - End-to-end testing through API Gateway
6. **Logger Service Operations** - Logging service performance

### Metrics Measured

- **Latency**: Average, P50, P90, P95, P99, Min, Max response times
- **Throughput**: Requests per second (QPS) under concurrent load
- **Success Rate**: Percentage of successful vs failed requests
- **Resource Utilization**: CPU, memory, and network usage

### Running Tests

```bash
# Run all performance tests
docker-compose up test-client

# Run specific test scenario
docker-compose exec test-client python test_client.py --scenario single_bottom

# View detailed results
docker-compose logs -f test-client
```

## 📊 Performance Results

### Sample Results (Layered Architecture)

```
测试场景                 服务              操作          Count  Avg(ms)  P50(ms)  P90(ms)  P95(ms)  P99(ms)
SingleBottom         FreshService    ListItems     30     1.57     1.53     2.00     2.41     4.27
SingleBottom         FreshService    PlaceOrder    30     1.50     1.29     2.52     2.83     3.09
APIGateway           APIGateway      ListItems     30     2.15     2.10     2.85     3.20     4.50
APIGateway           APIGateway      PlaceOrder    30     2.45     2.30     3.10     3.55     4.80
```

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Communication**: gRPC, HTTP
- **Containerization**: Docker, Docker Compose
- **Protocol Buffers**: gRPC service definitions
- **Logging**: Structured logging with multiple levels
- **Testing**: Performance benchmarking and load testing

## 🔍 System Design Trade-offs

### Layered Architecture (gRPC)

**Advantages:**

- Clear separation of concerns
- Efficient binary protocol
- Strong typing with Protocol Buffers
- Built-in load balancing

**Disadvantages:**

- Tight coupling between layers
- Complex error handling
- Limited HTTP compatibility

### Microservice Architecture (HTTP)

**Advantages:**

- Loose coupling between services
- HTTP compatibility
- Easy debugging and monitoring
- Technology diversity

**Disadvantages:**

- Higher latency overhead
- JSON parsing overhead
- Less efficient than binary protocols

## 🤖 AI Tools Usage

This project extensively leveraged AI tools for:

1. **Code Generation**: Automated service implementations and boilerplate code
2. **Architecture Design**: System design recommendations and trade-off analysis
3. **Performance Optimization**: Code optimization and bottleneck identification
4. **Testing**: Automated test case generation and performance analysis
5. **Documentation**: README generation and code documentation

## 📈 Scalability Analysis

### Horizontal Scaling

- Each service can be independently scaled
- Load balancing through API Gateway
- Stateless service design enables easy replication

### Vertical Scaling

- Configurable thread pools per service
- Memory and CPU optimization per container
- Resource monitoring and alerting

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 50050-50055 are available
2. **Docker Issues**: Run `docker system prune -f` to clean up
3. **gRPC Errors**: Regenerate protobuf files with `./regenerate_proto.sh`
4. **Performance Issues**: Check container resource limits

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up

# View detailed logs
docker-compose logs -f api-gateway
```

## 📚 API Documentation

### gRPC Services

- **WarehouseService**: Core warehouse operations
- **LoggerService**: Centralized logging operations

### HTTP Endpoints (Microservice Architecture)

- `GET /api/items/{category}`: List items by category
- `POST /api/orders`: Place new order
- `PUT /api/items/{id}`: Update item information
- `GET /api/logs`: Query operation logs

## 🎓 Educational Objectives

This project demonstrates:

- Distributed system design principles
- Communication model trade-offs
- Performance evaluation methodologies
- Container orchestration
- Service-oriented architecture patterns
- Load testing and benchmarking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Course**: CSE 5306 Distributed Systems
- **Semester**: Fall 2024
- **Institution**: [Your University]

## 📞 Support

For questions or issues, please refer to the course documentation or contact the development team.
