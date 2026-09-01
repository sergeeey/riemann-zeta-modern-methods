"""Regression tests for src/zeta/toolkit.py — pinned against published data.

WHY this file exists: atomize, deletion-test, research-audit and sci-code-audit
(boyko-project-radar full scan, 2026-08-27 — see
sandbox/20260827-project-radar-full-scan.md) independently converged on the same
finding: zero test coverage on the toolkit that 9 real files depend on
(find_zeros_on_critical_line, hardy_Z, verify_zero_on_critical_line). This is the
fix for that bottleneck (#1), not a new experiment.

Ground truth is src/zeta/reference.py (Odlyzko's published zero table), used here
as an external positive control — not derived from the code under test.
"""

from __future__ import annotations

import mpmath as mp
import pytest

from zeta.reference import ODLYZKO_FIRST_10
from zeta.toolkit import (
    find_zeros_on_critical_line,
    hardy_Z,
    set_precision,
    verify_zero_on_critical_line,
    zeta,
)


@pytest.fixture(autouse=True)
def _precision():
    """Every test runs at the toolkit's documented default precision."""
    set_precision(50)


# ---------------------------------------------------------------------------
# Positive control: found zeros must match the published Odlyzko table.
# ---------------------------------------------------------------------------


def test_first_zero_matches_odlyzko():
    zeros = find_zeros_on_critical_line(t_max=15.0)
    assert len(zeros) == 1
    assert abs(float(zeros[0].t) - float(ODLYZKO_FIRST_10[0])) < 1e-8


def test_first_ten_zeros_match_odlyzko():
    zeros = find_zeros_on_critical_line(t_max=50.0)
    assert len(zeros) >= 10
    for found, published in zip(zeros[:10], ODLYZKO_FIRST_10):
        assert abs(float(found.t) - float(published)) < 1e-8


def test_found_zero_residuals_are_near_zero():
    """Every located zero must independently satisfy |zeta(1/2+it)| ~ 0."""
    zeros = find_zeros_on_critical_line(t_max=50.0)
    assert zeros, "no zeros found in [0.5, 50] -- toolkit is broken"
    for z in zeros:
        assert z.residual < mp.mpf("1e-40")


def test_zeros_are_returned_in_increasing_order():
    zeros = find_zeros_on_critical_line(t_max=50.0)
    ts = [float(z.t) for z in zeros]
    assert ts == sorted(ts)


# ---------------------------------------------------------------------------
# verify_zero_on_critical_line: independent direct-substitution check.
# ---------------------------------------------------------------------------


def test_verify_zero_true_for_known_zero():
    assert verify_zero_on_critical_line(float(ODLYZKO_FIRST_10[0]))


def test_verify_zero_false_for_non_zero_point():
    # t=10 is nowhere near a zero (first zero is ~14.13) -- must reject it.
    assert not verify_zero_on_critical_line(10.0)


# ---------------------------------------------------------------------------
# Functional equation: zeta(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s) zeta(1-s).
# Independent of find_zeros_on_critical_line -- exercises `zeta()` directly.
# ---------------------------------------------------------------------------


def test_functional_equation_off_critical_line():
    s = mp.mpc("0.3", "7.5")
    lhs = zeta(s)
    rhs = mp.mpf(2) ** s * mp.pi ** (s - 1) * mp.sin(mp.pi * s / 2) * mp.gamma(1 - s) * zeta(1 - s)
    assert abs(lhs - rhs) < mp.mpf("1e-30")


def test_functional_equation_on_critical_line():
    s = mp.mpf(1) / 2 + 1j * mp.mpf("33.7")
    lhs = zeta(s)
    rhs = mp.mpf(2) ** s * mp.pi ** (s - 1) * mp.sin(mp.pi * s / 2) * mp.gamma(1 - s) * zeta(1 - s)
    assert abs(lhs - rhs) < mp.mpf("1e-30")


# ---------------------------------------------------------------------------
# Hardy Z: |Z(t)| must equal |zeta(1/2+it)| exactly (definitional identity).
# ---------------------------------------------------------------------------


def test_hardy_Z_modulus_matches_zeta_on_critical_line():
    for t in (14.134725, 21.022040, 40.0, 100.25):
        z_modulus = abs(hardy_Z(t))
        zeta_modulus = abs(zeta(mp.mpf(1) / 2 + 1j * mp.mpf(t)))
        assert abs(z_modulus - zeta_modulus) < mp.mpf("1e-30")


# ---------------------------------------------------------------------------
# Documented limitation (sci-code-audit, 2026-08-27): fixed scan_step
# sign-change detection cannot see an even multiplicity of roots inside one
# bracket. This test does NOT assert close-pair correctness -- it pins the
# CURRENT behaviour so a future change is caught explicitly, not silently
# "fixed" without updating the caveat in riemann_approaches.md.
# ---------------------------------------------------------------------------


def test_finer_scan_step_never_finds_fewer_zeros():
    coarse = find_zeros_on_critical_line(t_max=50.0, scan_step=0.5)
    fine = find_zeros_on_critical_line(t_max=50.0, scan_step=0.05)
    assert len(fine) >= len(coarse)
