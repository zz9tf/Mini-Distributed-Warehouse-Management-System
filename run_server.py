#!/usr/bin/env python3
"""
Run gRPC Server with Custom Code
Example of how to use the direct gRPC server
"""

from grpc_server import add_service, start_server

# Example: Add your custom services here
# Uncomment and replace with your actual code

# from your_proto import your_service_pb2_grpc
# from your_service_implementation import YourServiceImplementation

# Add service on port 50051
# add_service(
#     port=50051,
#     service_servicer=YourServiceImplementation(),
#     service_adder_func=your_service_pb2_grpc.add_YourServiceServicer_to_server,
#     max_workers=10
# )

# Add another service on port 50052
# add_service(
#     port=50052,
#     service_servicer=YourAnotherService(),
#     service_adder_func=your_service_pb2_grpc.add_YourAnotherServiceServicer_to_server,
#     max_workers=10
# )

def main():
    """Main function"""
    print("🎯 Running gRPC Server with Custom Code")
    print("=" * 50)
    
    print("💡 Please uncomment and replace with your actual service code")
    print("🔧 Then run: python run_server.py")
    print()
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
