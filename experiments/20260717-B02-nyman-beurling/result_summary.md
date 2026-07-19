# Result Summary — B-02 · Nyman–Beurling численно

**Классификация:** WEAKENED (promoted as illustration).

**Что проверяли:** приближается ли I_N·log(N) к C=2+γ−log4π для явного кандидата
V_N Bettin–Conrey–Farmer на N=10..3000.

**Что нашли:** нет, на этом диапазоне I_N растёт (ratio к C: 34.9→252.5), а не убывает.

**Почему это не FALSIFIED:** два независимых контроля (negative control V=0→I=1 верно;
no-collapse тест 4 схем квадратуры, разброс ≤0.03%) исключают баг реализации/интегрирования.
Сама статья прямо предупреждает о немонотонном виде V_N на "человеческих" N
(цитата про графики Landreau–Richards). Расхождение — пред-асимптотический эффект,
не опровержение.

**Вклад в проект:** ещё один independent пример "стены" (SYNTHESIS.md) — на этот раз
со стороны approximation theory (Nyman–Beurling), а не analytic number theory
(A-05, A-08). Усиливает главный вывод проекта другим методом.

**Время:** 1 сессия (прервана и продолжена 2026-07-19), в рамках time-box.
**Артефакты:** claim.md, estimand.md, controls.md, decision.md, caveats.md,
run_b02.py, diagnose_quad.py, исходники arXiv (txt).
