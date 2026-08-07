"""
Hydra-Core Dataset & Results Exporter Module
Exports CSV datasets and JSON report summaries to datasets/ and results/ directories.
Includes best_design.csv summary table for presentation & publications.
"""

import os
import json
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from ..simulation.thermal_solver import SimulationResult


def export_sweep_dataset(
    sweep_df: pd.DataFrame,
    best_design_df: pd.DataFrame,
    recommendations: Dict[str, Any],
    csv_path: str = "datasets/hydra_core_full_sweep_results.csv",
    best_csv_path: str = "results/best_design.csv",
    json_path: str = "results/workload_optimal_recommendations.json",
):
    """
    Exports full parameter sweep dataframe, best_design.csv, and optimal design recommendations to JSON.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(best_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    sweep_df.to_csv(csv_path, index=False)
    print(f"[Export] Full parameter sweep results exported to: {csv_path}")

    best_design_df.to_csv(best_csv_path, index=False)
    best_design_df.to_csv("datasets/best_design.csv", index=False)
    print(f"[Export] Executive Summary best_design.csv exported to: {best_csv_path} and datasets/best_design.csv")

    with open(json_path, "w") as f:
        json.dump(recommendations, f, indent=4)
    print(f"[Export] Workload optimal recommendations exported to: {json_path}")


def export_transient_traces(
    results_dict: Dict[str, SimulationResult],
    output_csv_path: str = "datasets/transient_temperature_traces.csv",
):
    """
    Exports time-series transient simulation traces to CSV.
    """
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    first_res = list(results_dict.values())[0]
    data_dict = {
        "Time_s": first_res.time_array,
        "Power_W": first_res.power_array,
    }

    for arch_key, res in results_dict.items():
        data_dict[f"GPU_Temp_{res.architecture}_degC"] = res.gpu_temp_array
        data_dict[f"PCM_Melt_{res.architecture}_frac"] = res.pcm_melt_array

    trace_df = pd.DataFrame(data_dict)
    trace_df.to_csv(output_csv_path, index=False)
    print(f"[Export] Transient temperature traces exported to: {output_csv_path}")


# Function Aliases
export_simulation_traces_csv = export_transient_traces


def export_sweep_results_csv(df: pd.DataFrame, path: str = "datasets/hydra_core_full_sweep_results.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def export_best_design_summary_csv(df: pd.DataFrame, path: str = "results/best_design.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    df.to_csv("datasets/best_design.csv", index=False)


def export_recommendations_json(recs: Dict[str, Any], path: str = "results/workload_optimal_recommendations.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(recs, f, indent=4)
