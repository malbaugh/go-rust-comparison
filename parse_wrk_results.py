import re
import statistics
import subprocess
import time

def parse_wrk_output(file):
    with open(file, 'r') as f:
        text = f.read()
    reqs = re.search(r"Requests/sec:\s+([\d\.]+)", text)
    lat = re.search(r"Latency\s+([\d\.]+)([a-zµ]+)", text)
    return {
        "requests_per_sec": float(reqs[1]) if reqs else None,
        "latency": lat[1] + lat[2] if lat else None,
    }

def run_benchmark(num_runs=5):
    go_results = []
    rust_results = []
    
    for i in range(num_runs):
        print(f"Running benchmark iteration {i+1}/{num_runs}")
        subprocess.run(["./run_benchmarks.sh"], check=True)
        
        go_data = parse_wrk_output("results/go.txt")
        rust_data = parse_wrk_output("results/rust.txt")
        
        go_results.append(go_data)
        rust_results.append(rust_data)
        
        if i < num_runs - 1:
            time.sleep(5)  # Wait between runs
    
    return {
        "Go": {
            "requests_per_sec": statistics.mean(r["requests_per_sec"] for r in go_results),
            "latency": go_results[0]["latency"],  # Keep original format for latency
            "std_dev": statistics.stdev(r["requests_per_sec"] for r in go_results) if len(go_results) > 1 else 0
        },
        "Rust": {
            "requests_per_sec": statistics.mean(r["requests_per_sec"] for r in rust_results),
            "latency": rust_results[0]["latency"],  # Keep original format for latency
            "std_dev": statistics.stdev(r["requests_per_sec"] for r in rust_results) if len(rust_results) > 1 else 0
        }
    }

results = run_benchmark()

# Generate README.md content
readme_content = """# Go vs Rust API Benchmark Results

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
"""

for lang, data in results.items():
    readme_content += f"| {lang} | {data['requests_per_sec']:,.2f} ± {data['std_dev']:,.2f} | {data['latency']} |\n"

readme_content += """
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
"""

with open("README.md", "w") as f:
    f.write(readme_content)
