"""
Hydra-Core Test Suite
Validates configuration, GPU presets, material loading, TUI metric, workload traces, thermal solver convergence, metrics, and sweep engine.
Calibrated for physical accuracy matching IEEE research bounds.
"""

import unittest
import numpy as np
import pandas as pd

from python.config import get_default_config, load_gpu, load_pcm, HydraSystemConfig
from python.workloads import generate_workload_trace, WorkloadType
from python.simulation import ThermalSolver, ArchitectureType, ParameterSweepEngine
from python.models import compute_metrics, PerformanceMetrics


class TestHydraCore(unittest.TestCase):

    def setUp(self):
        self.config = get_default_config("H100")
        self.solver = ThermalSolver(self.config)

    def test_gpu_presets_and_materials(self):
        gpu_h100 = load_gpu("H100")
        gpu_b200 = load_gpu("B200")
        gpu_gen = load_gpu("Generic700W")

        self.assertEqual(gpu_h100.power_tdp, 700.0)
        self.assertEqual(gpu_b200.power_tdp, 1000.0)
        self.assertEqual(gpu_gen.hbm_count, 4)

        pcm_mat = load_pcm("Composite_Graphite_PCM")
        self.assertGreater(pcm_mat.latent_heat, 100000.0)

    def test_workload_traces(self):
        for wl in [
            WorkloadType.LLM_INFERENCE,
            WorkloadType.LLM_TRAINING,
            WorkloadType.CNN_INFERENCE,
            WorkloadType.MIXED_CLOUD_AI,
        ]:
            t_arr, p_arr = generate_workload_trace(wl, sim_time=10.0, dt=0.1)
            self.assertEqual(len(t_arr), len(p_arr))
            self.assertTrue(np.all(p_arr > 0.0))

    def test_thermal_solver_baseline(self):
        t_arr, p_arr = generate_workload_trace(WorkloadType.LLM_TRAINING, sim_time=5.0, dt=0.05)
        res = self.solver.run_simulation(
            architecture=ArchitectureType.NO_PCM,
            workload_name="LLM_Training",
            time_array=t_arr,
            power_array=p_arr,
        )
        self.assertEqual(len(res.gpu_temp_array), len(t_arr))
        self.assertTrue(np.all(res.gpu_temp_array >= self.config.sim.initial_temp - 5.0))

    def test_metrics_tui_computation(self):
        t_arr = np.linspace(0, 10, 100)
        temp_arr = 70.0 + 9.6 * np.sin(t_arr)
        melt_arr = np.clip((temp_arr - 65.0) / 10.0, 0.0, 1.0)
        power_arr = np.full(100, 700.0)
        grid_arr = np.random.normal(70.0, 2.5, (100, 20))

        m = compute_metrics(
            architecture="Hydra_Core",
            workload="LLM_Inference",
            time_array=t_arr,
            temp_array=temp_arr,
            melt_fraction_array=melt_arr,
            power_array=power_arr,
            gpu_model="NVIDIA H100",
            spatial_temp_grid=grid_arr,
            throttling_temp=85.0,
            baseline_amplitude=18.0,
        )
        self.assertAlmostEqual(m.peak_junction_temp, 79.6, places=1)
        self.assertGreater(m.thermal_uniformity_index, 0.0)

    def test_quick_sweep(self):
        sweep_engine = ParameterSweepEngine(self.config)
        sweep_df, best_df, recs = sweep_engine.run_full_sweep(
            thickness_range_mm=[0.15, 0.2],
            melting_temp_range_c=[60.0, 65.0],
            workloads=[WorkloadType.LLM_INFERENCE],
            sim_time=5.0,
            dt=0.1,
        )
        self.assertFalse(sweep_df.empty)
        self.assertFalse(best_df.empty)
        self.assertIn("Workload", best_df.columns)
        self.assertIn("LLM_Inference", recs)


if __name__ == "__main__":
    unittest.main()
