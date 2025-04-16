#!/usr/bin/env python
"""
Benchmarking script for Hallucination Detection Model.
Runs at least 500 inference calls to measure latency characteristics.
"""

import argparse
import logging
from hdm2.analysis import evaluate_hallucination_detector

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark the Hallucination Detection Model")
    parser.add_argument("--repo-id", type=str, default="your-repo-id",
                      help="HuggingFace repository ID for the model")
    parser.add_argument("--min-calls", type=int, default=500,
                      help="Minimum number of calls to make to hdm.apply()")
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("benchmark.log"),
            logging.StreamHandler()
        ]
    )
    
    # Log configuration
    logging.info(f"Starting benchmark with repo_id={args.repo_id}, min_calls={args.min_calls}")
    
    # Run evaluation
    results, confusion, precision, recall, f1, latencies, word_counts = evaluate_hallucination_detector(
        min_calls=args.min_calls,
        repo_id=args.repo_id
    )
    
    # Log completion
    logging.info(f"Benchmark completed. Processed {len(latencies)} calls.") 