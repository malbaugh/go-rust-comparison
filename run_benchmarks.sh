#!/bin/bash

# Test Go API
echo "Testing Go API..."
wrk -t12 -c400 -d30s http://localhost:8080/users > results/go.txt

# Test Rust API
echo "Testing Rust API..."
wrk -t12 -c400 -d30s http://localhost:8081/users > results/rust.txt

# Run the Python script to parse results
echo "Parsing results..."
python3 parse_wrk_results.py 