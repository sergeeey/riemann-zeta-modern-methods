"""Zeta toolkit for the H-12 Riemann project.

Core utilities for computing the Riemann zeta function, the Hardy Z-function,
and locating nontrivial zeros on the critical line via independent root-finding.
"""

from .toolkit import (
    zeta,
    hardy_theta,
    hardy_Z,
    count_zeros_expected,
    find_zeros_on_critical_line,
    verify_zero_on_critical_line,
)

__all__ = [
    "zeta",
    "hardy_theta",
    "hardy_Z",
    "count_zeros_expected",
    "find_zeros_on_critical_line",
    "verify_zero_on_critical_line",
]
