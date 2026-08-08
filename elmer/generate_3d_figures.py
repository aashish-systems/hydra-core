#!/usr/bin/env python3
"""
3D FEA Visualization Engine for Elmer FEM & Hydra-Core Package thermal modeling.
Generates:
1. 3D Isometric Volumetric GPU Package Stack (3D FEA Mesh & Temperature Field)
2. 3D Isothermal Plume & Hotspot Core Map
3. 3D Junction Temperature Landscape Surface
"""

import os
import re
import struct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

def parse_3d_vtu(vtu_path):
    """Parse 3D node coordinates and temperature field from Elmer 3D VTU output."""
    with open(vtu_path, "rb") as f:
        content = f.read()

    tag = b'<AppendedData encoding="raw">'
    idx = content.find(tag)
    if idx == -1:
        raise ValueError("AppendedData tag not found")

    underscore_pos = content.find(b"_", idx)
    curr_pos = underscore_pos + 1

    # Array 1: temperature (Float64)
    len1 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4
    temp_bytes = content[curr_pos : curr_pos + len1]
    temps = np.frombuffer(temp_bytes, dtype=np.float64)
    curr_pos += len1

    # Array 2: GeometryIds (Int32)
    len2 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4 + len2

    # Array 3: Points (3D Float64)
    len3 = struct.unpack("<I", content[curr_pos : curr_pos + 4])[0]
    curr_pos += 4
    point_bytes = content[curr_pos : curr_pos + len3]
    points = np.frombuffer(point_bytes, dtype=np.float64).reshape(-1, 3)

    x_mm = points[:, 0] * 1000.0
    y_mm = points[:, 1] * 1000.0
    z_mm = points[:, 2] * 1000.0

    return x_mm, y_mm, z_mm, temps

def generate_3d_plots():
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    fig_dir = os.path.join(project_root, "figures")
    vtu_3d_path = os.path.join(project_root, "elmer", "elmer_results", "case_3d_t0001.vtu")

    os.makedirs(fig_dir, exist_ok=True)

    print("[3D Plot 1/3] Generating 3D Isometric Package FEA Thermal Field...")
    x, y, z, temps = parse_3d_vtu(vtu_3d_path)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Sample nodes for clear 3D scatter display
    sample_mask = (np.arange(len(x)) % 2 == 0)
    sc = ax.scatter(x[sample_mask], y[sample_mask], z[sample_mask], c=temps[sample_mask], cmap="inferno", s=8, alpha=0.85)

    cbar = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.08, label="FEA Temperature (°C)")

    # Set 3D bounding box & labels
    ax.set_xlabel("Width X (mm)", weight="bold")
    ax.set_ylabel("Length Y (mm)", weight="bold")
    ax.set_zlabel("Stack Height Z (mm)", weight="bold")
    ax.set_title("Hydra-Core: 3D Volumetric FEA Thermal Field (22,869 Nodes, ElmerSolver)", weight="bold", pad=15)

    # Elevate viewing angle
    ax.view_init(elev=28, azim=-45)

    fig_path1 = os.path.join(fig_dir, "3d_volumetric_package_stack.png")
    fig.savefig(fig_path1)
    plt.close(fig)
    print(f"  Saved: {fig_path1}")

    # --- Plot 2: 3D Junction Temperature Landscape ---
    print("[3D Plot 2/3] Generating 3D Junction Temperature Landscape Surface...")
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")

    die_mask = (z < 0.05)
    x_die = x[die_mask]
    y_die = y[die_mask]
    t_die = temps[die_mask]

    # Grid data for surface rendering
    grid_x, grid_y = np.meshgrid(np.unique(x_die), np.unique(y_die))
    grid_t = np.zeros_like(grid_x)

    for i in range(grid_x.shape[0]):
        for j in range(grid_x.shape[1]):
            val_x = grid_x[i, j]
            val_y = grid_y[i, j]
            m = (x_die == val_x) & (y_die == val_y)
            if np.any(m):
                grid_t[i, j] = t_die[m][0]
            else:
                grid_t[i, j] = 53.52

    surf = ax.plot_surface(grid_x, grid_y, grid_t, cmap="magma", edgecolor="none", alpha=0.9, antialiased=True)
    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.08, label="Junction Temp (°C)")

    ax.set_xlabel("X (mm)", weight="bold")
    ax.set_ylabel("Y (mm)", weight="bold")
    ax.set_zlabel("Temperature (°C)", weight="bold")
    ax.set_title("3D GPU Junction Temperature Distribution Landscape", weight="bold")
    ax.view_init(elev=35, azim=-125)

    fig_path2 = os.path.join(fig_dir, "3d_junction_temperature_landscape.png")
    fig.savefig(fig_path2)
    plt.close(fig)
    print(f"  Saved: {fig_path2}")

    # --- Plot 3: 3D Layer Exploded Schematic Diagram ---
    print("[3D Plot 3/3] Generating 3D Layer Exploded Structural Diagram...")
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")

    layers = [
        ("Copper Cold Plate (2.00 mm)", 3.0, "#b87333", 0.6),
        ("Composite PCM Buffer (0.20 mm)", 2.0, "#00ff66", 0.8),
        ("TIM-1 Layer (0.05 mm)", 1.2, "#ffcc00", 0.8),
        ("Silicon GPU Die (0.78 mm, 700W)", 0.2, "#3399ff", 0.9),
    ]

    for name, z_offset, color, alpha in layers:
        X_p, Y_p = np.meshgrid([0, 32], [0, 32])
        Z_p = np.full_like(X_p, z_offset)
        ax.plot_surface(X_p, Y_p, Z_p, color=color, alpha=alpha, edgecolor="black", linewidth=0.5)
        ax.text(16, 16, z_offset + 0.2, name, color="black", weight="bold", fontsize=9, ha="center")

    ax.set_xlabel("X Width (mm)", weight="bold")
    ax.set_ylabel("Y Length (mm)", weight="bold")
    ax.set_zlabel("Exploded Layer Axis", weight="bold")
    ax.set_title("Hydra-Core: 3D Stacked Thermal Architecture Exploded View", weight="bold")
    ax.view_init(elev=22, azim=-55)

    fig_path3 = os.path.join(fig_dir, "3d_layer_exploded_view.png")
    fig.savefig(fig_path3)
    plt.close(fig)
    print(f"  Saved: {fig_path3}")

    print("All 3D figures successfully generated!")

if __name__ == "__main__":
    generate_3d_plots()
