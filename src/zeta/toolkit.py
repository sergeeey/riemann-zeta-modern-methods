"""Core zeta toolkit — arbitrary-precision via mpmath.

Design note (WHY independent root-finding):
We do NOT use mpmath.zetazero() as the primary source of zeros. Instead we find
zeros via sign changes of the Hardy Z-function, which is a different code path.
mpmath.zetazero() is used ONLY as an independent cross-check (see verify.py).
This avoids circular validation: a zero is "found" by one method and "confirmed"
by two others (zetazero + direct substitution + published Odlyzko values).
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


def set_precision(dps: int = 50) -> None:
    """Set global decimal precision (digits)."""
    mp.mp.dps = dps


def zeta(s: complex | mp.mpc) -> mp.mpc:
    """Riemann zeta function ζ(s) (mpmath, analytically continued)."""
    return mp.zeta(s)


def hardy_theta(t: float | mp.mpf) -> mp.mpf:
    """Riemann–Siegel theta function θ(t).

    θ(t) = arg Γ(1/4 + it/2) − (t/2)·ln(π).
    Used to build the Hardy Z-function.
    """
    return mp.siegeltheta(t)


def hardy_Z(t: float | mp.mpf) -> mp.mpf:
    """Hardy Z-function Z(t) = e^{iθ(t)}·ζ(1/2 + it).

    WHY: Z(t) is REAL for real t, and |Z(t)| = |ζ(1/2+it)|. Therefore the zeros
    of ζ on the critical line are exactly the real zeros of Z(t) — detectable by
    sign changes, which is numerically robust.
    """
    return mp.siegelz(t)


def count_zeros_expected(T: float | mp.mpf) -> mp.mpf:
    """Riemann–von Mangoldt estimate of N(T) — number of zeros with 0<Im≤T.

    N(T) ≈ (T/2π)·ln(T/2π) − T/2π + 7/8.
    WHY: completeness check — compare against the count actually found, so we
    detect missed (closely-spaced) zeros.
    """
    T = mp.mpf(T)
    two_pi = 2 * mp.pi
    return (T / two_pi) * mp.log(T / two_pi) - T / two_pi + mp.mpf(7) / 8


@dataclass
class Zero:
    """A located nontrivial zero on the critical line."""

    index: int  # ordinal n (1-based) along increasing Im
    t: mp.mpf  # imaginary part (Im ρ)
    re: mp.mpf  # real part of s where we evaluated (should be 1/2)
    residual: mp.mpf  # |ζ(1/2 + i t)| at the located point (should be ~0)


def find_zeros_on_critical_line(
    t_max: float,
    *,
    t_min: float = 0.5,
    scan_step: float = 0.05,
    max_zeros: int | None = None,
) -> list[Zero]:
    """Find zeros of ζ on Re(s)=1/2 by sign changes of Hardy Z(t).

    Independent method: scan t in [t_min, t_max], detect Z(t) sign flips, refine
    each bracket with a root solver, then record the zero. Each zero's residual
    |ζ(1/2+it)| is computed by DIRECT substitution as a self-check.

    Args:
        t_max: upper bound on Im to search.
        t_min: lower bound (default 0.5, below the first zero at ~14.13).
        scan_step: scan resolution. Smaller = fewer missed close zeros, slower.
        max_zeros: stop after this many (None = all up to t_max).

    Returns:
        List of Zero, ordered by increasing t.
    """
    zeros: list[Zero] = []
    half = mp.mpf(1) / 2

    t_prev = mp.mpf(t_min)
    z_prev = hardy_Z(t_prev)

    t = t_prev + mp.mpf(scan_step)
    while t <= t_max:
        z = hardy_Z(t)
        # WHY: sign change of a real function brackets an odd number of roots.
        t_root = None
        if z_prev == 0:
            # Exact zero landed on the scan grid — bracket is degenerate, use it.
            t_root = t_prev
        elif z_prev * z < 0:
            # WHY two-point form [t_prev, t]: this selects a bracketing solver
            # (Illinois/Brent) that STAYS inside the interval. A single start
            # point (t_prev+t)/2 runs Muller/secant, which can run off to a
            # neighbouring root and create a duplicate or miss. (reviewer P0)
            t_root = mp.findroot(hardy_Z, [t_prev, t])
        if t_root is not None:
            residual = abs(zeta(half + 1j * t_root))
            zeros.append(
                Zero(
                    index=len(zeros) + 1,
                    t=t_root,
                    re=half,
                    residual=residual,
                )
            )
            if max_zeros is not None and len(zeros) >= max_zeros:
                break
        t_prev, z_prev = t, z
        t = t + mp.mpf(scan_step)

    return zeros


def verify_zero_on_critical_line(t: float | mp.mpf, tol: float = 1e-10) -> bool:
    """Direct check: is ζ(1/2 + i t) ≈ 0?

    Independent of how t was found. Returns True if |ζ(1/2+it)| < tol.
    """
    return abs(zeta(mp.mpf(1) / 2 + 1j * mp.mpf(t))) < tol
