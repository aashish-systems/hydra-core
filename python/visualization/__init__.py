"""
Visualization package for generating publication figures.
"""

from .plotter import (
    plot_workload_power_traces,
    plot_transient_temperature_comparison,
    plot_pcm_melt_fraction,
    plot_burst_endurance_bar,
    plot_parameter_sweep_heatmaps,
    plot_thermal_fatigue_lifetime,
    plot_architecture_flowchart,
    plot_power_sensitivity_curve,
    plot_sensitivity_tornado_chart,
)

__all__ = [
    "plot_workload_power_traces",
    "plot_transient_temperature_comparison",
    "plot_pcm_melt_fraction",
    "plot_burst_endurance_bar",
    "plot_parameter_sweep_heatmaps",
    "plot_thermal_fatigue_lifetime",
    "plot_architecture_flowchart",
    "plot_power_sensitivity_curve",
    "plot_sensitivity_tornado_chart",
]
