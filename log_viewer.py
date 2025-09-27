#!/usr/bin/env python3
"""
Log Viewer gRPC - 使用gRPC调用日志服务
"""

import sys
import argparse
from logger_client import logger_client


def print_timeline(logs, limit=20):
    """打印时间线日志"""
    print("\n" + "="*80)
    print("📊 OPERATION TIMELINE LOG")
    print("="*80)
    
    for i, log in enumerate(logs[:limit], 1):
        timestamp = log.timestamp
        service = log.service_name
        operation = log.operation
        success = log.success
        client_ip = log.client_ip
        
        status_emoji = "✅" if success else "❌"
        print(f"{i:2d}. {status_emoji} [{timestamp}] {service} - {operation}")
        print(f"    📍 Client: {client_ip}")
        
        if log.request_data:
            try:
                import json
                request_data = json.loads(log.request_data)
                print(f"    📥 Request: {request_data}")
            except:
                print(f"    📥 Request: {log.request_data}")
        
        if log.response_data:
            try:
                import json
                response_data = json.loads(log.response_data)
                print(f"    📤 Response: {response_data}")
            except:
                print(f"    📤 Response: {log.response_data}")
        
        if log.error_message:
            print(f"    ❌ Error: {log.error_message}")
        print()


def print_statistics(stats):
    """打印统计信息"""
    print("\n" + "="*80)
    print("📈 OPERATION STATISTICS")
    print("="*80)
    
    print(f"📊 Total Operations: {stats['total_operations']}")
    print(f"✅ Successful: {stats['successful_operations']}")
    print(f"❌ Failed: {stats['failed_operations']}")
    print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
    
    print("\n🏢 Service Statistics:")
    for service_stat in stats['service_stats']:
        print(f"  {service_stat['service_name']}: {service_stat['total']} total, {service_stat['success']} success, {service_stat['failed']} failed ({service_stat['success_rate']:.1f}%)")
    
    print("\n🔧 Operation Statistics:")
    for operation_stat in stats['operation_stats']:
        print(f"  {operation_stat['operation']}: {operation_stat['total']} total, {operation_stat['success']} success, {operation_stat['failed']} failed ({operation_stat['success_rate']:.1f}%)")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='查看操作日志 (gRPC版本)')
    parser.add_argument('--timeline', '-t', action='store_true', help='显示时间线日志')
    parser.add_argument('--stats', '-s', action='store_true', help='显示统计信息')
    parser.add_argument('--service', help='显示特定服务的日志')
    parser.add_argument('--operation', help='显示特定操作的日志')
    parser.add_argument('--limit', '-l', type=int, default=20, help='显示记录数量限制')
    
    args = parser.parse_args()
    
    if args.timeline or args.service or args.operation:
        print("📊 查询日志...")
        logs = logger_client.query_logs(
            service_name=args.service or "",
            operation=args.operation or "",
            limit=args.limit
        )
        print_timeline(logs, args.limit)
    
    if args.stats:
        print("📈 查询统计信息...")
        stats = logger_client.get_stats()
        if stats:
            print_statistics(stats)
        else:
            print("❌ 无法获取统计信息")
    
    # 如果没有指定任何参数，显示时间线
    if not any([args.timeline, args.stats, args.service, args.operation]):
        print("📊 显示最近的操作日志...")
        logs = logger_client.query_logs(limit=args.limit)
        print_timeline(logs, args.limit)


if __name__ == "__main__":
    main()
