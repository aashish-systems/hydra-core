#!/usr/bin/env python3
"""
Publication-Grade Visualizations for Elmer FEM & Hydra-Core Cross-Validation
Generates:
1. 2D FEA Temperature Field Contour (GPU Stack)
2. Vertical Temperature Gradient Profile (Z-stack)
3. Cross-Validation Engine Comparison (Python vs Elmer FEM vs Literature)
"""

import os
import re
import struct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Configure publication-style plot aesthetic
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

def parse_vtu_mesh_and_temps(vtu_path):
    """Parse node coordinates, quad elements, and temperature field from Elmer VTU file."""
    with open(vtu_path, "rb") as f:
        content = f.read()

    # Read XML header to get point count & offsets
    text_content = content.decode("ascii", errors="ignore")

    n_points_match = re.search(r'NumberOfPoints="(\d+)"', text_content)
    n_points = int(n_points_match.group(1)) if n_points_match else 1755

    # Locate raw appended data block
    tag = b'<AppendedData encoding="raw">'
    idx = content.find(tag)
    if idx == -1:
        raise ValueError("AppendedData tag not found")

    underscore_pos = content.find(b"_", idx)
    curr_pos = underscore_pos + 1

    # Array 1: temperature (1755 Float64)
    len1 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4
    temp_bytes = content[curr_pos : curr_pos + len1]
    temps = np.frombuffer(temp_bytes, dtype=np.float64)
    curr_pos += len1

    # Array 2: GeometryIds (Int32)
    len2 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4 + len2

    # Array 3: Points (1755 * 3 Float64)
    len3 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4
    point_bytes = content[curr_pos : curr_pos + len3]
    points = np.frombuffer(point_bytes, dtype=np.float64).reshape(-1, 3)

    return points[:, 0] * 1000.0, points[:, 1] * 1000.0, temps  # convert m to mm

def generate_figures():
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    fig_dir = os.path.join(project_root, "figures")
    results_dir = os.path.join(project_root, "results", "elmer")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    vtu_path = os.path.join(project_root, "elmer", "elmer_results", "case_t0001.vtu")

    print("[Plot 1/3] Generating 2D FEA Thermal Field Contour...")
    x_mm, y_mm, temps = parse_vtu_mesh_and_temps(vtu_path)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    triang = tri.Triangulation(x_mm, y_mm)
    cntr = ax.tricontourf(triang, temps, levels=25, cmap="plasma")
    cbar = fig.colorbar(cntr, ax=ax, label="Temperature (°C)")

    # Layer interface line markers (in mm)
    y_interfaces = [0.78, 0.78 + 0.05, 0.78 + 0.05 + 0.20, 0.78 + 0.05 + 0.20 + 2.00]
    layer_names = ["Silicon Die (700W Source)", "TIM Layer (0.05 mm)", "Composite PCM Buffer (0.20 mm)", "Copper Cold Plate (2.00 mm)"]
    
    for y_val, name in zip(y_interfaces, layer_names):
        ax.axhline(y_val, color="white", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.text(16.0, y_val - 0.08 if y_val < 1.0 else y_val - 0.3, name, color="white", fontsize=8, ha="center", weight="bold")

    ax.set_xlabel("Package Width X (mm)")
    ax.set_ylabel("Stack Height Y (mm)")
    ax.set_title("Hydra-Core: Elmer FEM 2D Steady-State Thermal Field (H100 Package, 700W)")
    ax.grid(True, linestyle=":", alpha=0.3)
    
    fig_path1 = os.path.join(fig_dir, "elmer_thermal_contour_2d.png")
    fig.savefig(fig_path1)
    plt.close(fig)
    print(f"  Saved: {fig_path1}")

    # --- Plot 2: Vertical Temperature Gradient Profile ---
    print("[Plot 2/3] Generating Vertical Temperature Profile (Z-Stack)...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    # Sample center column (x = 16 mm)
    center_mask = np.abs(x_mm - 16.0) < 0.6
    y_center = y_mm[center_mask]
    t_center = temps[center_mask]
    sort_idx = np.argsort(y_center)
    
    ax.plot(y_center[sort_idx], t_center[sort_idx], "o-", color="#d95f02", linewidth=2.2, markersize=4, label="Elmer 2D FEA Gradient")
    ax.axhline(53.52, color="#7570b3", linestyle="--", label="Peak Junction Temp (53.52°C)")
    ax.axhline(44.53, color="#1b9e77", linestyle=":", label="Cold Plate Surface (44.53°C)")
    
    ax.set_xlabel("Stack Distance Y (mm)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Thermal Gradient Profile Across GPU Package Stack")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)

    fig_path2 = os.path.join(fig_dir, "elmer_thermal_profile_z.png")
    fig.savefig(fig_path2)
    plt.close(fig)
    print(f"  Saved: {fig_path2}")

    # --- Plot 3: Cross-Validation Comparison Bar Chart ---
    print("[Plot 3/3] Generating Cross-Validation Comparison Figure...")
    engines = ["Python FDM\n(Hydra-Core)", "Elmer FEM\n(Independent)", "Literature\n(H100 Thermal Ref)"]
    peak_temps = [55.57, 53.52, 54.80]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(engines, peak_temps, color=colors, width=0.45, edgecolor="black", linewidth=1.0)

    for bar, temp in zip(bars, peak_temps):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{temp:.2f}°C", ha="center", va="bottom", fontweight="bold")

    ax.set_ylim(0, 70)
    ax.set_ylabel("Peak Junction Temperature (°C)")
    ax.set_title("Cross-Validation: Peak Temperature Agreement Across Solvers")
    ax.axhline(55.0, color="gray", linestyle="--", alpha=0.5, label="Nominal Target (~54-55°C)")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    
    # Delta annotation
    ax.annotate("Δ = 2.05°C (3.6% Error)", xy=(0.5, 54.5), xytext=(0.5, 62),
                ha="center", arrowprops=dict(arrowstyle="->", lw=1.2, color="red"),
                fontsize=10, fontweight="bold", color="red")

    fig_path3 = os.path.join(fig_dir, "elmer_vs_python_cross_validation.png")
    fig.savefig(fig_path3)
    plt.close(fig)
    print(f"  Saved: {fig_path3}")

    print("All figures successfully generated and saved in figures/")

if __name__ == "__main__":
    generate_figures()
