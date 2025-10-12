import socket
import time
import statistics

SERVER = "food-service"  # or the service container name
PORT = 5000
COUNT = 1000

latencies = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER, PORT))
    print(f"Connected to {SERVER}:{PORT}")

    for i in range(COUNT):
        start = time.perf_counter_ns()  # Nanosecond precision
        s.sendall(b"x")
        s.recv(1)
        end = time.perf_counter_ns()

        latency_us = (end - start) / 1000  # Convert to microseconds
        latencies.append(latency_us)

avg = statistics.mean(latencies)
p95 = statistics.quantiles(latencies, n=20)[18]
p99 = statistics.quantiles(latencies, n=100)[98]

print(f"Total packets: {COUNT}")
print(f"Average latency: {avg:.2f} µs")
print(f"95th percentile: {p95:.2f} µs")
print(f"99th percentile: {p99:.2f} µs")