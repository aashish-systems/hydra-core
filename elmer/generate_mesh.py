#!/usr/bin/env python3
"""
Elmer FEM Mesh Generator for Hydra-Core GPU Package
Creates a structured 2D quad mesh compatible with ElmerGrid format.
Generates mesh.header, mesh.nodes, mesh.elements, mesh.boundary files.

Package Geometry (bottom to top):
  Body 1: GPU Die      (y = 0.0 to 0.78 mm)
  Body 2: TIM Layer    (y = 0.78 to 0.83 mm)  
  Body 3: PCM Buffer   (y = 0.83 to 1.03 mm)
  Body 4: Cold Plate   (y = 1.03 to 3.03 mm)

Boundary Conditions:
  BC 1: Top surface (coolant convection, h = 35000 W/m^2*K)
  BC 2: Bottom surface (heat source / insulated)
  BC 3: Left side (insulated)
  BC 4: Right side (insulated)
"""

import os
import numpy as np


def generate_elmer_mesh(output_dir, nx=64, ny_layers=None):
    """
    Generate a structured 2D quad mesh for the GPU package stack.
    
    Args:
        output_dir: Directory to write mesh files
        nx: Number of elements in x-direction
        ny_layers: Dict with number of elements per layer
    """
    if ny_layers is None:
        ny_layers = {
            "die": 8,      # GPU die: 0.78 mm
            "tim": 2,       # TIM: 0.05 mm
            "pcm": 4,       # PCM: 0.20 mm 
            "coldplate": 12  # Cold plate: 2.00 mm
        }
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Package dimensions in meters
    L = 0.032       # 32 mm width
    d_die = 0.00078  # 0.78 mm
    d_tim = 0.00005  # 0.05 mm  
    d_pcm = 0.00020  # 0.20 mm
    d_cp = 0.00200   # 2.00 mm
    
    # Layer boundaries (y-coordinates)
    y_interfaces = [
        0.0,
        d_die,
        d_die + d_tim,
        d_die + d_tim + d_pcm,
        d_die + d_tim + d_pcm + d_cp,
    ]
    
    ny_per_layer = [ny_layers["die"], ny_layers["tim"], ny_layers["pcm"], ny_layers["coldplate"]]
    ny_total = sum(ny_per_layer)
    
    # Generate x coordinates
    x_coords = np.linspace(0, L, nx + 1)
    
    # Generate y coordinates per layer with grading
    y_coords = []
    for i, (y_start, y_end, n) in enumerate(zip(y_interfaces[:-1], y_interfaces[1:], ny_per_layer)):
        if i == 0:
            ys = np.linspace(y_start, y_end, n + 1)
        else:
            ys = np.linspace(y_start, y_end, n + 1)[1:]  # Skip first (shared with previous)
        y_coords.extend(ys)
    y_coords = np.array(y_coords)
    
    n_nodes_x = nx + 1
    n_nodes_y = ny_total + 1
    n_nodes = n_nodes_x * n_nodes_y
    n_elements = nx * ny_total
    
    # Body IDs for each row of elements
    body_ids = []
    cumulative = 0
    for layer_idx, n_layer in enumerate(ny_per_layer):
        body_ids.extend([layer_idx + 1] * n_layer)
        cumulative += n_layer
    
    # Generate nodes
    # Format: node_id x y z
    nodes = []
    node_id = 1
    for j in range(n_nodes_y):
        for i in range(n_nodes_x):
            nodes.append((node_id, -1, x_coords[i], y_coords[j], 0.0))
            node_id += 1
    
    # Generate 2D quad elements (404 = 4-node quad in Elmer)
    elements = []
    elem_id = 1
    for j in range(ny_total):
        for i in range(nx):
            n1 = j * n_nodes_x + i + 1
            n2 = n1 + 1
            n3 = n2 + n_nodes_x
            n4 = n1 + n_nodes_x
            body = body_ids[j]
            elements.append((elem_id, body, 404, n1, n2, n3, n4))
            elem_id += 1
    
    # Generate boundary elements (202 = 2-node line in Elmer)
    boundaries = []
    bc_id = 1
    
    # BC 1: Top surface (y = y_max) - Coolant convection (counter-clockwise: n2 -> n1)
    j_top = ny_total
    for i in range(nx):
        n1 = j_top * n_nodes_x + i + 1
        n2 = n1 + 1
        # Find parent element (top row)
        parent_elem = (j_top - 1) * nx + i + 1
        boundaries.append((bc_id, 1, parent_elem, 0, 202, n2, n1))
        bc_id += 1
    
    # BC 2: Bottom surface (y = 0) - Insulated / heat source (counter-clockwise: n1 -> n2)
    for i in range(nx):
        n1 = i + 1
        n2 = i + 2
        parent_elem = i + 1
        boundaries.append((bc_id, 2, parent_elem, 0, 202, n1, n2))
        bc_id += 1
    
    # BC 3: Left side (x = 0) - Insulated (counter-clockwise: n2 -> n1)
    for j in range(ny_total):
        n1 = j * n_nodes_x + 1
        n2 = n1 + n_nodes_x
        parent_elem = j * nx + 1
        boundaries.append((bc_id, 3, parent_elem, 0, 202, n2, n1))
        bc_id += 1
    
    # BC 4: Right side (x = L) - Insulated (counter-clockwise: n1 -> n2)
    for j in range(ny_total):
        n1 = (j + 1) * n_nodes_x
        n2 = n1 + n_nodes_x
        parent_elem = (j + 1) * nx
        boundaries.append((bc_id, 4, parent_elem, 0, 202, n1, n2))
        bc_id += 1
    
    n_boundary = len(boundaries)
    
    # Write mesh.header
    with open(os.path.join(output_dir, "mesh.header"), "w") as f:
        f.write(f"{n_nodes} {n_elements} {n_boundary}\n")
        f.write("2\n")  # 2 element types
        f.write(f"404 {n_elements}\n")  # quad elements
        f.write(f"202 {n_boundary}\n")  # line boundary elements
    
    # Write mesh.nodes
    with open(os.path.join(output_dir, "mesh.nodes"), "w") as f:
        for n in nodes:
            f.write(f"{n[0]} {n[1]} {n[2]:.10e} {n[3]:.10e} {n[4]:.10e}\n")
    
    # Write mesh.elements
    with open(os.path.join(output_dir, "mesh.elements"), "w") as f:
        for e in elements:
            f.write(f"{e[0]} {e[1]} {e[2]} {e[3]} {e[4]} {e[5]} {e[6]}\n")
    
    # Write mesh.boundary
    with open(os.path.join(output_dir, "mesh.boundary"), "w") as f:
        for b in boundaries:
            f.write(f"{b[0]} {b[1]} {b[2]} {b[3]} {b[4]} {b[5]} {b[6]}\n")
    
    print(f"  Mesh generated: {n_nodes} nodes, {n_elements} elements, {n_boundary} boundary elements")
    print(f"  Grid: {nx} x {ny_total} ({n_nodes_x} x {n_nodes_y} nodes)")
    print(f"  Layers: Die({ny_per_layer[0]}) | TIM({ny_per_layer[1]}) | PCM({ny_per_layer[2]}) | ColdPlate({ny_per_layer[3]})")
    print(f"  Output: {output_dir}")
    
    return {
        "n_nodes": n_nodes,
        "n_elements": n_elements,
        "n_boundary": n_boundary,
        "nx": nx,
        "ny_total": ny_total,
        "y_interfaces": y_interfaces,
    }


if __name__ == "__main__":
    mesh_dir = os.path.join(os.path.dirname(__file__), "elmer_mesh")
    info = generate_elmer_mesh(mesh_dir)
    print(f"\nMesh generation complete: {info}")
