"""
Hydra-Core Validation Suite Command-Line Executable
Runs Analytical 1D Model, Multi-Engine Comparison, 200-Run Sensitivity Study, and 500-Run Monte Carlo Simulation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from python.validation import ValidationSuite


def main():
    print("================================================================================")
    print("   HYDRA-CORE: Multi-Engine Validation & Statistical Robustness Suite")
    print("================================================================================")

    val = ValidationSuite()

    # 1. Analytical 1D Thermal Resistance Calculation
    print("\n[Engine 1/4] Running Analytical 1D Thermal Resistance Calculation...")
    t_base, t_hydra, r_dict = val.run_analytical_model(700.0)
    print(f"  -> Total Package Thermal Resistance: R_th = {r_dict['R_total']:.4f} °C/W")
    print(f"  -> Analytical Baseline Peak Temp (700W): {t_base:.1f} °C")
    print(f"  -> Analytical Hydra-Core Peak Temp (700W): {t_hydra:.1f} °C")

    # 2. Multi-Engine FEM Comparison Table
    print("\n[Engine 2/4] Generating Multi-Engine FEM Cross-Validation Table...")
    df_fem = val.run_multi_engine_comparison()
    print(df_fem.to_string(index=False))

    # 3. 200-Run Sensitivity Study
    print("\n[Engine 3/4] Executing 200-Run Parameter Sensitivity Study (+/-20% Variations)...")
    df_sens = val.run_sensitivity_study(200)
    print(f"  -> Mean Temperature Reduction: {df_sens['Temperature_Reduction_degC'].mean():.2f} °C")
    print(f"  -> Min Reduction: {df_sens['Temperature_Reduction_degC'].min():.2f} °C, Max Reduction: {df_sens['Temperature_Reduction_degC'].max():.2f} °C")

    # 4. 500-Run Monte Carlo Robustness Analysis
    print("\n[Engine 4/4] Executing 500-Run Monte Carlo Stochastic Robustness Analysis...")
    stats = val.run_monte_carlo_analysis(500, "figures/monte_carlo_robustness_histogram.png")
    print(f"  -> Baseline Mean: {stats['baseline_mean']:.2f} °C (Std: {stats['baseline_std']:.2f} °C)")
    print(f"  -> Hydra-Core Mean: {stats['hydra_mean']:.2f} °C (Std: {stats['hydra_std']:.2f} °C)")
    print(f"  -> Statistical Confidence Win Rate: {stats['confidence_win_rate_pct']:.1f}%")
    print("  -> Saved plot: figures/monte_carlo_robustness_histogram.png")

    print("\n================================================================================")
    print("  MULTI-ENGINE VALIDATION SUITE COMPLETED SUCCESSFULLY!")
    print("================================================================================\n")


if __name__ == "__main__":
    main()
