#!/usr/bin/env python3
"""Parse Elmer FEM VTU output to extract temperature field statistics."""

import os
import struct
import numpy as np

def parse_vtu_temperatures(vtu_path):
    with open(vtu_path, "rb") as f:
        content = f.read()

    # Locate raw appended data block
    tag = b'<AppendedData encoding="raw">'
    idx = content.find(tag)
    if idx == -1:
        return None

    # Find the '_' marker after tag
    underscore_pos = content.find(b"_", idx)
    if underscore_pos == -1:
        return None

    start_pos = underscore_pos + 1
    # First 4 bytes (UInt32) store the size of the array in bytes
    num_bytes = struct.unpack("<I", content[start_pos : start_pos + 4])[0]

    data = content[start_pos + 4 : start_pos + 4 + num_bytes]
    temps = np.frombuffer(data, dtype=np.float64)

    return {
        "temp_min": float(np.min(temps)),
        "temp_max": float(np.max(temps)),
        "temp_mean": float(np.mean(temps)),
        "temp_std": float(np.std(temps)),
        "n_points": len(temps),
        "temps": temps,
    }

if __name__ == "__main__":
    vtu_path = os.path.join(os.path.dirname(__file__), "elmer_results", "case_t0001.vtu")
    res = parse_vtu_temperatures(vtu_path)
    if res:
        print("Temperature Field Extracted Natively from Elmer VTU:")
        print(f"  Points: {res['n_points']}")
        print(f"  T_min:  {res['temp_min']:.2f} degC")
        print(f"  T_max:  {res['temp_max']:.2f} degC")
        print(f"  T_mean: {res['temp_mean']:.2f} degC")
        print(f"  T_std:  {res['temp_std']:.2f} degC")
    else:
        print("Failed to parse VTU file.")
