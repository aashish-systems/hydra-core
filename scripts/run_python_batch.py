"""
Hydra-Core Multi-GPU Batch Python Execution Script
Runs thermal simulations and parameter sweeps across H100, B200, and Generic700W GPUs.
Exports comprehensive result datasets to results/python/ and datasets/.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import json
import pandas as pd
from python.config import get_default_config, load_gpu
from python.simulation import ParameterSweepEngine, ThermalSolver, ArchitectureType
from python.workloads import generate_workload_trace, WorkloadType
from python.models import compute_metrics
from python.exports import export_sweep_dataset, export_transient_traces


def run_batch():
    gpus = ["H100", "B200", "Generic700W"]
    os.makedirs("results/python", exist_ok=True)
    os.makedirs("datasets", exist_ok=True)

    all_best_rows = []

    for gpu_name in gpus:
        print(f"\n=======================================================")
        print(f"  Running Hydra-Core Python Research Batch: {gpu_name}")
        print(f"=======================================================")
        cfg = get_default_config(gpu_name)
        sweep_engine = ParameterSweepEngine(cfg)

        sweep_df, best_df, recommendations = sweep_engine.run_full_sweep(
            thickness_range_mm=[0.2, 0.3, 0.4, 0.5, 0.6],
            melting_temp_range_c=[55.0, 60.0, 65.0, 70.0, 75.0],
            sim_time=60.0,
            dt=0.08,
        )

        all_best_rows.append(best_df)

        sweep_df.to_csv(f"results/python/sweep_results_{gpu_name}.csv", index=False)
        best_df.to_csv(f"results/python/best_design_{gpu_name}.csv", index=False)
        with open(f"results/python/recommendations_{gpu_name}.json", "w") as f:
            json.dump(recommendations, f, indent=4)

    combined_best_df = pd.concat(all_best_rows, ignore_index=True)
    combined_best_df.to_csv("results/best_design.csv", index=False)
    combined_best_df.to_csv("datasets/best_design.csv", index=False)

    print("\n[Batch Complete] Exported all multi-GPU results to results/python/ and results/best_design.csv")


if __name__ == "__main__":
    run_batch()
