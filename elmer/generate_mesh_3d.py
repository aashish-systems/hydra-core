#!/usr/bin/env python3
"""
3D Hexahedral Mesh Generator for Elmer FEM (Hydra-Core GPU Package)
Creates structured 3D 8-node hex elements (Elmer element type 808).
Domain: X in [0, 32mm], Y in [0, 32mm], Z in [0, 3.03mm]
Stack: Die (0.78mm) | TIM (0.05mm) | PCM Buffer (0.20mm) | Cold Plate (2.00mm)
"""

import os
import numpy as np

def generate_3d_elmer_mesh(output_dir, nx=32, ny=32, nz_layers=None):
    if nz_layers is None:
        nz_layers = {
            "die": 6,        # GPU die: 0.78 mm
            "tim": 2,        # TIM: 0.05 mm
            "pcm": 4,        # PCM: 0.20 mm
            "coldplate": 8   # Cold plate: 2.00 mm
        }

    os.makedirs(output_dir, exist_ok=True)

    Lx = 0.032  # 32 mm
    Ly = 0.032  # 32 mm
    d_die = 0.00078
    d_tim = 0.00005
    d_pcm = 0.00020
    d_cp = 0.00200

    z_interfaces = [
        0.0,
        d_die,
        d_die + d_tim,
        d_die + d_tim + d_pcm,
        d_die + d_tim + d_pcm + d_cp
    ]

    nz_per_layer = [nz_layers["die"], nz_layers["tim"], nz_layers["pcm"], nz_layers["coldplate"]]
    nz_total = sum(nz_per_layer)

    x_coords = np.linspace(0, Lx, nx + 1)
    y_coords = np.linspace(0, Ly, ny + 1)

    z_coords = []
    for i, (z_start, z_end, n) in enumerate(zip(z_interfaces[:-1], z_interfaces[1:], nz_per_layer)):
        if i == 0:
            zs = np.linspace(z_start, z_end, n + 1)
        else:
            zs = np.linspace(z_start, z_end, n + 1)[1:]
        z_coords.extend(zs)
    z_coords = np.array(z_coords)

    nx1, ny1, nz1 = nx + 1, ny + 1, nz_total + 1
    n_nodes = nx1 * ny1 * nz1
    n_elements = nx * ny * nz_total

    body_ids = []
    for layer_idx, n_layer in enumerate(nz_per_layer):
        body_ids.extend([layer_idx + 1] * n_layer)

    # Generate 3D nodes (node_id -1 x y z)
    nodes = []
    node_id = 1
    for k in range(nz1):
        for j in range(ny1):
            for i in range(nx1):
                nodes.append((node_id, -1, x_coords[i], y_coords[j], z_coords[k]))
                node_id += 1

    # Function to get 1-based node index for grid position (i, j, k)
    def node_idx(i, j, k):
        return k * (nx1 * ny1) + j * nx1 + i + 1

    # Generate 3D 8-node hex elements (808)
    elements = []
    elem_id = 1
    for k in range(nz_total):
        body = body_ids[k]
        for j in range(ny):
            for i in range(nx):
                n1 = node_idx(i, j, k)
                n2 = node_idx(i + 1, j, k)
                n3 = node_idx(i + 1, j + 1, k)
                n4 = node_idx(i, j + 1, k)
                n5 = node_idx(i, j, k + 1)
                n6 = node_idx(i + 1, j, k + 1)
                n7 = node_idx(i + 1, j + 1, k + 1)
                n8 = node_idx(i, j + 1, k + 1)
                elements.append((elem_id, body, 808, n1, n2, n3, n4, n5, n6, n7, n8))
                elem_id += 1

    # Generate boundary quad elements (404)
    boundaries = []
    bc_id = 1

    # BC 1: Top surface (z = z_max) - Coolant convection
    k_top = nz_total
    for j in range(ny):
        for i in range(nx):
            n1 = node_idx(i, j, k_top)
            n2 = node_idx(i + 1, j, k_top)
            n3 = node_idx(i + 1, j + 1, k_top)
            n4 = node_idx(i, j + 1, k_top)
            parent_elem = (k_top - 1) * (nx * ny) + j * nx + i + 1
            boundaries.append((bc_id, 1, parent_elem, 0, 404, n1, n2, n3, n4))
            bc_id += 1

    # BC 2: Bottom surface (z = 0) - Adiabatic / heat source
    for j in range(ny):
        for i in range(nx):
            n1 = node_idx(i, j, 0)
            n2 = node_idx(i + 1, j, 0)
            n3 = node_idx(i + 1, j + 1, 0)
            n4 = node_idx(i, j + 1, 0)
            parent_elem = j * nx + i + 1
            boundaries.append((bc_id, 2, parent_elem, 0, 404, n1, n4, n3, n2))
            bc_id += 1

    n_boundary = len(boundaries)

    # Write mesh.header
    with open(os.path.join(output_dir, "mesh.header"), "w") as f:
        f.write(f"{n_nodes} {n_elements} {n_boundary}\n")
        f.write("2\n")
        f.write(f"808 {n_elements}\n")
        f.write(f"404 {n_boundary}\n")

    # Write mesh.nodes
    with open(os.path.join(output_dir, "mesh.nodes"), "w") as f:
        for n in nodes:
            f.write(f"{n[0]} {n[1]} {n[2]:.10e} {n[3]:.10e} {n[4]:.10e}\n")

    # Write mesh.elements
    with open(os.path.join(output_dir, "mesh.elements"), "w") as f:
        for e in elements:
            f.write(f"{e[0]} {e[1]} {e[2]} {e[3]} {e[4]} {e[5]} {e[6]} {e[7]} {e[8]} {e[9]} {e[10]}\n")

    # Write mesh.boundary
    with open(os.path.join(output_dir, "mesh.boundary"), "w") as f:
        for b in boundaries:
            f.write(f"{b[0]} {b[1]} {b[2]} {b[3]} {b[4]} {b[5]} {b[6]} {b[7]} {b[8]}\n")

    print(f"  3D Mesh Generated: {n_nodes} nodes, {n_elements} 3D hex elements, {n_boundary} boundary quad elements")
    print(f"  Grid: {nx} x {ny} x {nz_total} ({nx1} x {ny1} x {nz1} nodes)")
    print(f"  Output: {output_dir}")

    return {
        "n_nodes": n_nodes,
        "n_elements": n_elements,
        "nx": nx,
        "ny": ny,
        "nz_total": nz_total,
    }

if __name__ == "__main__":
    mesh_dir = os.path.join(os.path.dirname(__file__), "elmer_mesh_3d")
    generate_3d_elmer_mesh(mesh_dir)
