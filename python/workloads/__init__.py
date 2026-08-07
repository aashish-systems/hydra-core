"""
Workloads Package
Generates realistic AI power traces for thermal evaluation.
"""

from .trace_generator import generate_workload_trace, generate_all_workload_traces, WorkloadType

__all__ = ["generate_workload_trace", "generate_all_workload_traces", "WorkloadType"]
