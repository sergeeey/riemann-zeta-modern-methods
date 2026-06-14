# -*- coding: utf-8 -*-
"""A-04 sandbox: верификация RH в окне [0,T] методом Тьюринга через Hardy Z(t).
Опирается на готовый src/zeta (A-10).

v2 (после skeptic NEEDS-STRICTER): completeness теперь строгая —
N_found (смены знака Z) сравнивается с mp.nzeros(T) (Turing's method, ИНОЙ код-путь),
а не с эвристикой θ/π+1. Точечный S(T) оставлен лишь как доп. диагностика.
"""

import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
import mpmath as mp  # noqa: E402
from zeta import hardy_theta, find_zeros_on_critical_line  # noqa: E402
from zeta.reference import ODLYZKO_FIRST_10  # noqa: E402

mp.mp.dps = 30
T = 300.0

t0 = time.time()
zeros = find_zeros_on_critical_line(T, scan_step=0.05)
dt = time.time() - t0
N_found = len(zeros)

# СТРОГИЙ count нулей в полосе (Turing's method в mpmath) — иной алгоритм, чем sign-changes Z.
t1 = time.time()
N_strict = int(mp.nzeros(T))
dt_strict = time.time() - t1

# Эвристика (для диагностики, НЕ для вердикта): главный член Римана–фон Мангольдта
N_main = float(hardy_theta(T) / mp.pi + 1)
S_T = N_found - N_main

# Positive control + self-check
ref = [mp.mpf(x) for x in ODLYZKO_FIRST_10]
max_ref_err = max(abs(zeros[i].t - ref[i]) for i in range(min(10, N_found)))
max_res = max(z.residual for z in zeros)
gaps = [float(zeros[i + 1].t - zeros[i].t) for i in range(N_found - 1)]

solid = N_found == N_strict
print(f"T = {T}")
print(f"N_found (смены знака Z, Re=1/2): {N_found}   за {dt:.1f} c")
print(f"N_strict (mp.nzeros, Turing, полоса): {N_strict}   за {dt_strict:.1f} c")
print(
    f"ВЕРДИКТ completeness: {'SOLID-IN-WINDOW — N_found == N_strict, off-line нулей нет до T' if solid else 'FAIL — N_found != N_strict, пропуск/off-line!'}"
)
print(f"--- диагностика ---")
print(f"эвристика θ/π+1 = {N_main:.4f},  S(T) = {S_T:+.4f}")
print(f"positive control (первые 10 vs Odlyzko): max err = {mp.nstr(max_ref_err, 3)}")
print(f"self-check: max |zeta(1/2+it)| = {mp.nstr(max_res, 3)}")
print(
    f"мин. зазор соседних нулей = {min(gaps):.4f} (scan_step=0.05, запас x{min(gaps) / 0.05:.0f})"
)
