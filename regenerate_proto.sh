#!/bin/bash
# Regenerate protobuf files

echo "🔄 Regenerating protobuf files..."

# Generate Python files
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. warehouse.proto

echo "✅ Protobuf files regenerated successfully!"
echo "📁 Generated files:"
echo "   - warehouse_pb2.py"
echo "   - warehouse_pb2_grpc.py"
