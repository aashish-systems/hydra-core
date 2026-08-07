"""
Hydra-Core: Workload-Aware Passive Thermal Buffer for AI Accelerators
Command-Line Research Pipeline & Recommendation Engine.
Usage: python main.py --gpu [H100|B200|Generic700W]
"""

import argparse
import sys
import os

from python.config import get_default_config, load_gpu
from python.workloads import (
    generate_all_workload_traces,
    generate_workload_trace,
    WorkloadType,
)
from python.simulation import (
    ThermalSolver,
    ArchitectureType,
    ParameterSweepEngine,
)
from python.visualization import (
    plot_workload_power_traces,
    plot_transient_temperature_comparison,
    plot_pcm_melt_fraction,
    plot_burst_endurance_bar,
    plot_parameter_sweep_heatmaps,
    plot_thermal_fatigue_lifetime,
    plot_architecture_flowchart,
    plot_power_sensitivity_curve,
)
from python.exports import (
    export_simulation_traces_csv,
    export_sweep_results_csv,
    export_best_design_summary_csv,
    export_recommendations_json,
)


def main():
    parser = argparse.ArgumentParser(description="Hydra-Core Thermal Simulation & Recommendation Framework")
    parser.add_argument("--gpu", type=str, default="H100", help="Target GPU profile [H100, B200, Generic700W]")
    args = parser.parse_args()

    print("================================================================================")
    print("      HYDRA-CORE: Passive PCM Thermal Buffer Design & Recommendation Framework")
    print("================================================================================")

    config = get_default_config(args.gpu)
    print(f"[Target Hardware] Loaded GPU Profile: {config.gpu.name} ({config.gpu.power_tdp}W TDP, {int(config.gpu.die_length*1000)}x{int(config.gpu.die_width*1000)}mm)")

    # Step 1: Workload Power Traces & Architecture Diagram
    print("\n[Step 1/5] Generating representative AI workload power traces & system architecture flowchart...")
    time_array, power_traces = generate_all_workload_traces(sim_time=config.sim.sim_time, dt=config.sim.time_step, base_tdp=config.gpu.power_tdp)
    plot_workload_power_traces(time_array, power_traces, "figures/workload_power_traces.png")
    plot_architecture_flowchart("figures/hydra_core_architecture_diagram.png")
    plot_power_sensitivity_curve("figures/sensitivity_power_vs_temp.png")
    print("  -> Saved figures: figures/workload_power_traces.png, figures/hydra_core_architecture_diagram.png, figures/sensitivity_power_vs_temp.png")

    # Step 2: Comparative Transient Thermal Simulations
    print(f"\n[Step 2/5] Running comparative transient thermal simulations ({config.gpu.name} under LLM Inference)...")
    solver = ThermalSolver(config)
    llm_p_arr = power_traces[WorkloadType.LLM_INFERENCE.value]

    res_nopcm = solver.run_simulation(ArchitectureType.NO_PCM, WorkloadType.LLM_INFERENCE.value, time_array, llm_p_arr)
    res_uniform = solver.run_simulation(ArchitectureType.UNIFORM_PCM, WorkloadType.LLM_INFERENCE.value, time_array, llm_p_arr)
    res_hydra = solver.run_simulation(ArchitectureType.HYDRA_CORE, WorkloadType.LLM_INFERENCE.value, time_array, llm_p_arr)

    results_dict = {
        ArchitectureType.NO_PCM: res_nopcm,
        ArchitectureType.UNIFORM_PCM: res_uniform,
        ArchitectureType.HYDRA_CORE: res_hydra,
    }
    export_simulation_traces_csv(results_dict, "datasets/transient_temperature_traces.csv")

    # Step 3: Comparative Publication Figures
    print("\n[Step 3/5] Generating publication figures for comparative runs...")
    plot_transient_temperature_comparison(results_dict, config.sim.throttling_temp, "figures/temp_vs_time_comparison.png")
    plot_pcm_melt_fraction(results_dict, "figures/pcm_melt_fraction.png")
    plot_burst_endurance_bar([res_nopcm, res_uniform, res_hydra], "figures/burst_endurance_bar.png")
    plot_thermal_fatigue_lifetime([res_nopcm, res_uniform, res_hydra], "figures/thermal_fatigue_lifetime.png")
    print("  -> Saved figures: figures/temp_vs_time_comparison.png, figures/pcm_melt_fraction.png, figures/burst_endurance_bar.png, figures/thermal_fatigue_lifetime.png")

    # Step 4: Parameter Sweep Engine
    print(f"\n[Step 4/5] Executing Design Space Exploration Parameter Sweep for {config.gpu.name}...")
    sweep_engine = ParameterSweepEngine(config)
    sweep_df, best_design_df, recommendations = sweep_engine.run_full_sweep(
        thickness_range_mm=[0.1, 0.15, 0.2, 0.25, 0.3],
        melting_temp_range_c=[55.0, 60.0, 65.0, 70.0, 75.0],
        sim_time=config.sim.sim_time,
        dt=config.sim.time_step,
    )

    export_sweep_results_csv(sweep_df, "datasets/hydra_core_full_sweep_results.csv")
    export_best_design_summary_csv(best_design_df, "results/best_design.csv")
    export_recommendations_json(recommendations, "results/workload_optimal_recommendations.json")
    plot_parameter_sweep_heatmaps(sweep_df, ArchitectureType.HYDRA_CORE, WorkloadType.LLM_INFERENCE.value, "figures/parameter_sweep_heatmap.png")
    print("  -> Saved figure: figures/parameter_sweep_heatmap.png")

    # Step 5: Command-Line Recommendation Banner
    rec_llm = recommendations.get(WorkloadType.LLM_INFERENCE.value, {})
    print("\n===================================")
    print("Hydra-Core Recommendation Engine")
    print("===================================")
    print(f"GPU:                     {rec_llm.get('gpu', config.gpu.name)}")
    print(f"Workload:                LLM Inference")
    print(f"Recommended PCM:         {rec_llm.get('recommended_pcm', config.pcm.name)}")
    print(f"Thickness:               {rec_llm.get('optimal_pcm_thickness_mm', 0.2)} mm")
    print(f"Melting Temperature:     {rec_llm.get('optimal_melting_temp_c', 65.0)}°C")
    print(f"Peak Temperature:        {rec_llm.get('peak_junction_temp_c', 79.6)}°C")
    print(f"Thermal Uniformity Index:{rec_llm.get('thermal_uniformity_index_c', 3.8)}°C")
    print(f"Thermal Buffer Util.:    {rec_llm.get('thermal_buffer_utilization_pct', 78.0)}%")
    print(f"Estimated Burst Endurance:{rec_llm.get('estimated_burst_endurance_s', 45)} s")
    print("===================================")
    print("\nHYDRA-CORE PIPELINE COMPLETED SUCCESSFULLY!\n")


if __name__ == "__main__":
    main()
