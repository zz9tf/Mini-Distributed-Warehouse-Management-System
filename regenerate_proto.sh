#!/bin/bash
# 重新生成protobuf文件

echo "🔄 Regenerating protobuf files..."

# 生成Python文件
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. warehouse.proto

echo "✅ Protobuf files regenerated successfully!"
echo "📁 Generated files:"
echo "   - warehouse_pb2.py"
echo "   - warehouse_pb2_grpc.py"
