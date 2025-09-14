# Layered Warehouse Management System

A distributed warehouse management system with layered architecture using gRPC.

## 🏗️ Architecture

```
🌐 API Gateway (50050)
├── 🍎 FoodService (50052) → 🥬 FreshService (50053)
└── 📱 ElectronicsService (50051) → 🏠 ApplianceService (50054)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Proto Code

```bash
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. warehouse.proto
```

### 3. Start All Services

```bash
python start_services.py
```

### 4. Test with Client

```bash
python test_client.py
```

## 📁 Project Structure

```
Mini-Distributed-Warehouse-Management-System/
├── README_LAYERED.md              # This file
├── warehouse.proto                # gRPC protocol definition
├── warehouse_pb2.py              # Generated proto code
├── warehouse_pb2_grpc.py         # Generated gRPC code
├── api_gateway.py                # Top layer - API Gateway
├── services/
│   ├── food_service.py           # Middle layer - FoodService
│   ├── electronics_service.py    # Middle layer - ElectronicsService
│   ├── fresh_service.py          # Bottom layer - FreshService
│   └── appliance_service.py      # Bottom layer - ApplianceService
├── test_client.py                # Frontend test client
├── start_services.py             # Service manager
├── docker-compose.yml            # Docker configuration
└── requirements.txt              # Python dependencies
```

## 🔧 Service Details

### API Gateway (Port 50050)

- **Role**: Top layer service, routes requests to appropriate services
- **Routing Logic**:
  - Food-related requests → FoodService
  - Electronics-related requests → ElectronicsService

### FoodService (Port 50052)

- **Role**: Middle layer service for food category
- **Forwards to**: FreshService
- **Handles**: All food-related operations

### ElectronicsService (Port 50051)

- **Role**: Middle layer service for electronics category
- **Forwards to**: ApplianceService
- **Handles**: All electronics-related operations

### FreshService (Port 50053)

- **Role**: Bottom layer service for fresh food inventory
- **Manages**: Fruits, vegetables, and fresh food stock
- **Direct**: No further forwarding

### ApplianceService (Port 50054)

- **Role**: Bottom layer service for appliance inventory
- **Manages**: Kitchen and living room appliances
- **Direct**: No further forwarding

## 📚 API Methods

All services implement the same gRPC interface:

### PlaceOrder

- **Request**: `OrderRequest` (category, subcategory, item)
- **Response**: `OrderResponse` (status, left)
- **Purpose**: Place an order for an item

### PutItem

- **Request**: `PutItemRequest` (category, subcategory, item)
- **Response**: `PutItemResponse` (success, message)
- **Purpose**: Add item to inventory

### GetItem

- **Request**: `GetItemRequest` (category, subcategory, item)
- **Response**: `GetItemResponse` (success, message)
- **Purpose**: Remove item from inventory

### ListItems

- **Request**: `ListItemsRequest` (category, subcategory)
- **Response**: `ListItemsResponse` (items)
- **Purpose**: List all items in a category/subcategory

## 🐳 Docker Support

### Using Docker Compose

```bash
docker-compose up --build
```

### Individual Services

```bash
# Start specific service
docker run -p 50050:50050 <image> python api_gateway.py
```

## 🧪 Testing

### Manual Testing

```bash
# Start all services
python start_services.py

# In another terminal, run tests
python test_client.py
```

### Test Scenarios

1. **Food Category Flow**: API Gateway → FoodService → FreshService
2. **Electronics Category Flow**: API Gateway → ElectronicsService → ApplianceService
3. **Inventory Management**: PutItem, GetItem, ListItems operations
4. **Order Processing**: PlaceOrder with stock management

## 🔍 Monitoring

Each service logs:

- Incoming requests
- Forwarding operations (middle layer)
- Inventory changes (bottom layer)
- Error conditions

## 🛠️ Development

### Adding New Services

1. Create service class implementing `OrderServiceServicer`
2. Add routing logic to appropriate layer
3. Update API Gateway routing if needed
4. Add to `start_services.py`

### Modifying Proto

1. Update `warehouse.proto`
2. Regenerate code: `python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. warehouse.proto`
3. Update service implementations

## 📊 Performance

- **Concurrent Requests**: Each service uses ThreadPoolExecutor
- **Connection Pooling**: gRPC channels are reused
- **Error Handling**: Graceful degradation with service unavailable responses
- **Logging**: Comprehensive request/response logging

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 50050-50054 are available
2. **Service Dependencies**: Start services in correct order
3. **Proto Generation**: Run proto generation after changes
4. **Network Issues**: Check localhost connectivity

### Debug Mode

Set `PYTHONPATH=/app` and run services individually for debugging.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
