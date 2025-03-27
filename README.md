# Go vs Rust API Benchmark Results

This repository contains benchmark results comparing the performance of Go and Rust HTTP APIs.

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.x (for running the benchmark script)

### Building and Starting the Services
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The services will be available at:
- Go API: http://localhost:8080
- Rust API: http://localhost:8081

## Benchmark Configuration
- 12 threads
- 400 concurrent connections
- 30 seconds duration
- 5 runs averaged for each service

## Results

| Language | Requests/sec (avg ± std dev) | Latency |
|----------|-----------------------------|---------|
| Go | 41,156.88 ± 1,153.85 | 9.54ms |
| Rust | 49,911.75 ± 1,302.74 | 8.11ms |

## How to Run Benchmarks

### Using Docker Compose (Recommended)
```bash
# Start the services
docker-compose up -d --build

# Run the benchmark script
python3 parse_wrk_results.py
```

### Manual Testing
1. Start the Go API server on port 8080
2. Start the Rust API server on port 8081
3. Run `./run_benchmarks.sh` to execute the benchmarks

## Project Structure
- `Dockerfile.go` - Go API container configuration
- `Dockerfile.rust` - Rust API container configuration
- `docker-compose.yml` - Service orchestration
- `parse_wrk_results.py` - Benchmark results parser
- `run_benchmarks.sh` - Benchmark execution script
