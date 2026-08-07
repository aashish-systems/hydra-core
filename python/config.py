"""
Hydra-Core v1.0 Configuration Module
Defines system parameters for AI GPU package, TIM, PCM, cold plate, and numerical simulation.
Includes Material & GPU Database Loaders (H100, B200, Generic700W).
Calibrated for realistic package thermal resistance & microchannel liquid cooling (35°C idle to 86.4°C peak baseline).
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import pandas as pd


@dataclass
class GPUConfig:
    name: str = "NVIDIA H100"
    power_tdp: float = 700.0  # W
    die_length: float = 0.032  # m (32 mm)
    die_width: float = 0.025  # m (25 mm)
    thickness: float = 0.00078  # m (0.78 mm silicon die)
    density: float = 2330.0  # kg/m^3
    specific_heat: float = 700.0  # J/kg*K
    thermal_conductivity: float = 130.0  # W/m*K
    hbm_count: int = 6
    hbm_power: float = 10.0  # W per HBM stack

    @property
    def die_area(self) -> float:
        return self.die_length * self.die_width


@dataclass
class TIMConfig:
    name: str = "Metallic PCM TIM"
    thickness: float = 50e-6  # m (0.05 mm)
    thermal_conductivity: float = 15.0  # W/m*K
    density: float = 2500.0  # kg/m^3
    specific_heat: float = 500.0  # J/kg*K


@dataclass
class PCMConfig:
    name: str = "Composite Graphite PCM"
    thickness: float = 0.0002  # m (0.2 mm / 200 µm)
    melting_temp: float = 65.0  # °C
    melting_window: float = 2.0  # °C (phase transition delta)
    latent_heat: float = 220000.0  # J/kg
    density: float = 1200.0  # kg/m^3
    thermal_conductivity_solid: float = 45.0  # W/m*K (Uniform PCM)
    thermal_conductivity_liquid: float = 40.0  # W/m*K
    specific_heat_solid: float = 1800.0  # J/kg*K
    specific_heat_liquid: float = 2000.0  # J/kg*K

    @property
    def thermal_conductivity_avg(self) -> float:
        return (self.thermal_conductivity_solid + self.thermal_conductivity_liquid) / 2.0


@dataclass
class ColdPlateConfig:
    name: str = "Microchannel Direct Liquid Cold Plate"
    thickness: float = 0.002  # m (2 mm copper base)
    thermal_conductivity: float = 400.0  # W/m*K
    density: float = 8960.0  # kg/m^3
    specific_heat: float = 385.0  # J/kg*K
    coolant_temp: float = 25.0  # °C
    convection_coeff: float = 35000.0  # W/m^2*K (High-performance microchannel cooling)


@dataclass
class SimulationConfig:
    sim_time: float = 60.0  # seconds
    time_step: float = 0.05  # seconds
    initial_temp: float = 35.0  # °C (Realistic Idle Temperature)
    throttling_temp: float = 85.0  # °C
    spatial_nodes_per_layer: int = 15  # discretization grid nodes per layer


@dataclass
class HydraSystemConfig:
    gpu: GPUConfig = field(default_factory=GPUConfig)
    tim: TIMConfig = field(default_factory=TIMConfig)
    pcm: PCMConfig = field(default_factory=PCMConfig)
    cold_plate: ColdPlateConfig = field(default_factory=ColdPlateConfig)
    sim: SimulationConfig = field(default_factory=SimulationConfig)


def load_gpu(gpu_name: str = "H100", csv_path: str = "datasets/gpu/gpus.csv") -> GPUConfig:
    """Loads GPU parameters from database CSV or falls back to preset."""
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        sub = df[df["name"].str.upper() == gpu_name.upper()]
        if not sub.empty:
            row = sub.iloc[0]
            display_name = f"NVIDIA {row['name']}" if row['name'] in ['H100', 'B200'] else row['name']
            return GPUConfig(
                name=display_name,
                power_tdp=float(row["power_tdp_W"]),
                die_length=float(row["die_length_m"]),
                die_width=float(row["die_width_m"]),
                thickness=float(row["thickness_m"]),
                density=float(row["density_kg_m3"]),
                specific_heat=float(row["specific_heat_J_kgK"]),
                thermal_conductivity=float(row["thermal_conductivity_W_mK"]),
                hbm_count=int(row["hbm_count"]),
                hbm_power=float(row["hbm_power_W"]),
            )
    if gpu_name.upper() == "B200":
        return GPUConfig(name="NVIDIA B200", power_tdp=1000.0, die_length=0.040, die_width=0.030, hbm_count=8)
    elif gpu_name.upper() == "GENERIC700W":
        return GPUConfig(name="Generic700W AI Accelerator", power_tdp=700.0, die_length=0.030, die_width=0.030, hbm_count=4)
    return GPUConfig(name="NVIDIA H100", power_tdp=700.0, die_length=0.032, die_width=0.025, hbm_count=6)


def load_pcm(pcm_name: str = "Composite_Graphite_PCM", csv_path: str = "datasets/materials/pcm.csv") -> PCMConfig:
    """Loads PCM material parameters from database CSV."""
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        sub = df[df["name"].str.lower() == pcm_name.lower()]
        if not sub.empty:
            row = sub.iloc[0]
            return PCMConfig(
                name=row["name"].replace("_", " "),
                latent_heat=float(row["latent_heat_J_kg"]),
                density=float(row["density_kg_m3"]),
                thermal_conductivity_solid=float(row["k_solid_W_mK"]),
                thermal_conductivity_liquid=float(row["k_liquid_W_mK"]),
                specific_heat_solid=float(row["cp_solid_J_kgK"]),
                specific_heat_liquid=float(row["cp_liquid_J_kgK"]),
            )
    return PCMConfig(name="Composite Graphite PCM")


def get_default_config(gpu_type: str = "H100") -> HydraSystemConfig:
    """Returns the default Hydra-Core system configuration for a specific GPU model."""
    gpu_cfg = load_gpu(gpu_type)
    pcm_cfg = load_pcm("Composite_Graphite_PCM")
    return HydraSystemConfig(gpu=gpu_cfg, pcm=pcm_cfg)
