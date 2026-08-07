"""
AI Workload Power Trace Generator
Generates representative time-dependent power profiles P(t) for AI accelerators.
"""

from enum import Enum
from typing import Dict, Tuple
import numpy as np


class WorkloadType(str, Enum):
    LLM_INFERENCE = "LLM_Inference"
    LLM_TRAINING = "LLM_Training"
    CNN_INFERENCE = "CNN_Inference"
    MIXED_CLOUD_AI = "Mixed_Cloud_AI"


def generate_workload_trace(
    workload_type: WorkloadType | str,
    sim_time: float = 60.0,
    dt: float = 0.02,
    base_tdp: float = 700.0,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates a power trace array P(t) and time array t for a given workload profile.
    """
    np.random.seed(seed)
    time_array = np.arange(0.0, sim_time + dt / 2.0, dt)
    n_steps = len(time_array)
    power_array = np.zeros(n_steps)

    w_type = WorkloadType(workload_type)

    if w_type == WorkloadType.LLM_INFERENCE:
        for i, t in enumerate(time_array):
            cycle_time = t % 10.0
            if cycle_time < 1.5:
                power = base_tdp * 1.25 + 20.0 * np.sin(2.0 * np.pi * 5.0 * t)
            elif (cycle_time - 1.5) % 0.5 < 0.15:
                power = base_tdp * 1.0 + 15.0 * np.random.randn()
            else:
                power = base_tdp * 0.55 + 10.0 * np.random.randn()
            power_array[i] = max(100.0, power)

    elif w_type == WorkloadType.LLM_TRAINING:
        for i, t in enumerate(time_array):
            sync_dip = 1.0 - 0.25 * (1.0 if (t % 4.0) < 0.3 else 0.0)
            noise = 25.0 * np.random.randn()
            power = (base_tdp * 0.95 + noise) * sync_dip
            power_array[i] = max(150.0, power)

    elif w_type == WorkloadType.CNN_INFERENCE:
        for i, t in enumerate(time_array):
            cycle_time = t % 2.0
            if cycle_time < 1.2:
                power = base_tdp * 0.92 + 15.0 * np.random.randn()
            else:
                power = base_tdp * 0.35 + 10.0 * np.random.randn()
            power_array[i] = max(100.0, power)

    elif w_type == WorkloadType.MIXED_CLOUD_AI:
        levels = [200.0, 600.0, 300.0, 900.0, 500.0, 750.0]
        step_duration = 3.0
        for i, t in enumerate(time_array):
            level_idx = int(t / step_duration) % len(levels)
            base_p = levels[level_idx]
            noise = 20.0 * np.sin(2.0 * np.pi * 2.0 * t) + 10.0 * np.random.randn()
            power_array[i] = max(100.0, base_p + noise)

    return time_array, power_array


def generate_all_workload_traces(
    sim_time: float = 60.0,
    dt: float = 0.02,
    base_tdp: float = 700.0,
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Generates all 4 representative AI workload traces.
    """
    traces = {}
    time_array = None
    for wl in WorkloadType:
        t_arr, p_arr = generate_workload_trace(wl, sim_time=sim_time, dt=dt, base_tdp=base_tdp)
        time_array = t_arr
        traces[wl.value] = p_arr

    return time_array, traces
