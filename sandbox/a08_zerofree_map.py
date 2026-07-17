# -*- coding: utf-8 -*-
"""A-08 RECON: карта zero-free region vs реальные нули. Опирается на src/zeta (find_zeros).
ЧЕСТНОСТЬ: константы c иллюстративны (порядок Rosser–Schoenfeld); это КАРТА landscape,
не расширение region и не доказательство."""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import mpmath as mp  # noqa: E402
from zeta import find_zeros_on_critical_line  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

mp.mp.dps = 25
T = 100

# реальные нули (наш независимый поиск через смены знака Z)
zeros = find_zeros_on_critical_line(T, scan_step=0.1)
zt = [float(z.t) for z in zeros]
zsig = [float(z.re) for z in zeros]
maxRe = max(zsig)

# zero-free границы σ(t) — иллюстративные
ts = list(range(3, T + 1))
c_cl = 1 / 9.6  # классическая (Vallée Poussin / Rosser–Schoenfeld порядок)
sig_cl = [1 - c_cl / math.log(t) for t in ts]
c_vk = 1 / 5.0  # Vinogradov–Korobov форма (иллюстративный множитель)
sig_vk = [1 - c_vk / ((math.log(t)) ** (2 / 3) * (math.log(math.log(t))) ** (1 / 3)) for t in ts]

fig, ax = plt.subplots(figsize=(7.2, 8.2))
ax.fill_betweenx(
    ts,
    [0.5] * len(ts),
    sig_cl,
    color="orange",
    alpha=0.16,
    label="UNDECIDED ½<σ<1−c/lnt: НЕ доказано пусто",
)
ax.plot(sig_cl, ts, color="red", lw=1.4, label="classical zero-free (Vallée Poussin)")
ax.plot(sig_vk, ts, color="purple", lw=1.0, ls="--", label="Vinogradov–Korobov (чуть шире)")
ax.scatter(zsig, zt, s=12, color="blue", zorder=3, label=f"реальные нули (n={len(zt)}), σ=½")
ax.axvline(0.5, color="green", lw=1.2, ls=":", label="критическая прямая σ=½ (RH)")
ax.axvline(1.0, color="black", lw=0.8)
ax.set_xlim(0.4, 1.02)
ax.set_ylim(0, T)
ax.set_xlabel("σ = Re(s)")
ax.set_ylabel("t = Im(s)")
ax.set_title("A-08 RECON · zero-free region vs реальные нули: ПРОПАСТЬ")
ax.legend(fontsize=7, loc="upper right")
fig.tight_layout()
out = "sandbox/A08-zerofree-map.png"
fig.savefig(out, dpi=130)

gap = sig_cl[-1] - 0.5
print("saved", out)
print(
    f"нулей до T={T}: {len(zt)}; max Re = {maxRe} (предсказание region: нет нулей правее границы)"
)
print(f"classical zero-free граница при t=100: σ={sig_cl[-1]:.4f}")
print(
    f"ШИРИНА undecided-зоны при t=100: {gap:.4f}  (доказано пусто лишь {1 - sig_cl[-1]:.4f} от Re=1)"
)
print(f"т.е. {gap / (sig_cl[-1] - 0.5) * 100:.0f}% полосы [½, граница] — НЕ доказана пустой")
