import re
import csv

def parse_wrk_output(file):
    with open(file, 'r') as f:
        text = f.read()
    reqs = re.search(r"Requests/sec:\s+([\d\.]+)", text)
    lat = re.search(r"Latency\s+([\d\.]+)([a-zµ]+)", text)
    return {
        "requests_per_sec": float(reqs[1]) if reqs else None,
        "latency": lat[1] + lat[2] if lat else None,
    }

results = {
    "Go": parse_wrk_output("results/go.txt"),
    "Rust": parse_wrk_output("results/rust.txt")
}

with open("results/benchmark.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Language", "Requests/sec", "Latency"])
    for lang, data in results.items():
        writer.writerow([lang, data["requests_per_sec"], data["latency"]])
