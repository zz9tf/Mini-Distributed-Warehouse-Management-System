# Simple gRPC Server Framework

A simple and clean gRPC server framework that supports custom proto-generated code.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Your Proto Code

```bash
python -m grpc_tools.protoc -I your_proto_dir --python_out=. --grpc_python_out=. your_proto_file.proto
```

### 3. Create Service Implementation

```python
# your_service.py
import your_proto_pb2
import your_proto_pb2_grpc

class YourService(your_proto_pb2_grpc.YourServiceServicer):
    def YourMethod(self, request, context):
        return your_proto_pb2.YourResponse(message="Hello from your service!")
```

### 4. Start Server

```python
# main.py
from simple_grpc_server import SimpleGRPCServer
from your_service import YourService
import your_proto_pb2_grpc

# Create server
server = SimpleGRPCServer()

# Add service
server.add_service(
    port=50051,
    service_servicer=YourService(),
    service_adder_func=your_proto_pb2_grpc.add_YourServiceServicer_to_server
)

# Run server
server.run()
```

### 5. Test with Client

```python
# test_client.py
from simple_grpc_client import SimpleGRPCClient
import your_proto_pb2_grpc
import your_proto_pb2

# Create client
client = SimpleGRPCClient(host='localhost', port=50051)

# Connect to service
client.connect(your_proto_pb2_grpc.YourServiceStub)

# Test health check
client.test_health_check(
    your_proto_pb2.HealthCheckRequest,
    your_proto_pb2.HealthCheckResponse
)

# Test custom method
request = your_proto_pb2.YourRequest(message="Hello from client!")
client.test_custom_method("YourMethod", request)

# Close connection
client.close()
```

## 📁 Project Structure

```
Mini-Distributed-Warehouse-Management-System/
├── README.md
├── LICENSE
├── requirements.txt               # Python dependencies
├── simple_grpc_server.py         # Main gRPC server framework
├── simple_grpc_client.py         # Simple gRPC client for testing
├── example_usage.py              # Usage examples
└── Dockerfile                    # Docker configuration
```

## 🔧 Available Ports

- **Port 50051**: Available for your custom service
- **Port 50052**: Available for your custom service

## 📚 API Reference

### SimpleGRPCServer Class

#### `add_service(port, service_servicer, service_adder_func, max_workers=10)`

Add gRPC service to specified port

**Parameters:**

- `port`: Service port number
- `service_servicer`: Your service implementation instance
- `service_adder_func`: Proto-generated service adder function
- `max_workers`: Maximum worker threads (optional, default 10)

**Example:**

```python
server.add_service(
    port=50051,
    service_servicer=MyService(),
    service_adder_func=my_proto_pb2_grpc.add_MyServiceServicer_to_server
)
```

#### `start_all_servers()`

Start all added services

#### `stop_all_servers()`

Stop all services

#### `run()`

Run server (blocking call)

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Communication**: gRPC
- **Containerization**: Docker
- **Testing**: Unit tests, integration tests

## 💡 Usage Tips

1. **Port Selection**: Use any available port, framework handles automatically
2. **Multiple Services**: Add multiple services to different ports
3. **Error Handling**: Framework includes basic error and signal handling
4. **Thread Safety**: Each service uses independent thread pool

## 🛑 Stop Services

Use `Ctrl+C` or send `SIGTERM` signal to stop all services.

## 📝 Notes

- Ensure your proto files generate Python code correctly
- Service implementation must inherit from proto-generated Servicer base class
- Ports cannot be reused
- Framework handles gRPC low-level details automatically

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
