# -*- coding: utf-8 -*-
"""A-07 RECON · Idea 3 (downgrade): landscape κ(θ) по PUBLISHED reference-точкам.
ЧЕСТНОСТЬ: это НЕ пересчёт функционала Левинсона-Конри (тот = мини-проект:
mollified second moment Conrey + вариационная оптимизация P,Q). Это карта
опубликованных нижних границ κ как функции длины mollifier θ, чтобы визуально
проверить вывод: 'все приросты застряли на θ=4/7' (structural ceiling)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (θ, κ, label) — PUBLISHED lower bounds, [VERIFIED-web]. НЕ recomputed.
pts = [
    (0.5, 0.3333, "Levinson 1974"),
    (4 / 7, 0.4077, "Conrey 1989"),
    (4 / 7, 0.4105, "BCY 2010"),
    (4 / 7, 0.4128, "Feng 2012"),
    (4 / 7, 0.4167, "PRZZ 2018 (рекорд)"),
]
fig, ax = plt.subplots(figsize=(8.5, 5.2))
for th, k, lab in pts:
    ax.scatter(th, k, s=55, zorder=3)
    ax.annotate(f"{lab}  κ={k}", (th, k), textcoords="offset points", xytext=(10, -3), fontsize=8)
# барьер θ=4/7
ax.axvline(4 / 7, ls="--", color="red", alpha=0.6)
ax.annotate(
    "θ = 4/7 барьер\n(Deshouillers–Iwaniec exp-sums)",
    (4 / 7 + 0.005, 0.345),
    color="red",
    fontsize=8,
)
# conjectural под GLH: θ→1 ⟹ κ→1
ax.scatter(1.0, 1.0, marker="*", s=160, color="gray", zorder=3)
ax.annotate(
    "",
    xy=(0.985, 0.985),
    xytext=(4 / 7, 0.4167),
    arrowprops=dict(arrowstyle="->", ls=":", color="gray"),
)
ax.annotate("conjectural (GLH):\nθ→1 ⟹ κ→1", (0.80, 0.72), color="gray", fontsize=8)
ax.set_xlabel("θ  (длина mollifier, M = T^θ)")
ax.set_ylabel("κ  (доказанная нижняя граница доли на Re=½)")
ax.set_title("A-07 RECON · κ(θ): PUBLISHED границы (reference, НЕ пересчёт функционала)")
ax.set_xlim(0.45, 1.05)
ax.set_ylim(0.30, 1.05)
ax.grid(alpha=0.3)
ax.text(
    0.455,
    0.305,
    "Все приросты 1989→2018 (+0.9%) на θ=4/7 → стена СТРУКТУРНАЯ (нули ζ' в полоске a/lnT)",
    fontsize=7.5,
    color="darkblue",
)
fig.tight_layout()
out = "sandbox/A07-kappa-theta-landscape.png"
fig.savefig(out, dpi=130)
print("saved", out)
print("вертикальный стек на θ=4/7:", [k for th, k, _ in pts if abs(th - 4 / 7) < 1e-6])
print("на θ=1/2:", [k for th, k, _ in pts if abs(th - 0.5) < 1e-6])
