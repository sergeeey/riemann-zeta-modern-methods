# Controls — A-04

## Positive control
- Первые 10 нулей vs опубликованные Odlyzko (`src/zeta/reference.py`): max err = **9.42e-19**. PASS.
- Self-check: max |ζ(½+it)| в найденных точках = **1.08e-28** (это реальные нули). PASS.

## Negative control (off-line detection)
Метод РАЗЛИЧАЕТ on-line и off-line по построению:
- смены знака Z(t) ловят ТОЛЬКО нули на Re=½;
- `mp.nzeros` (Turing) считает ВСЕ нули в полосе 0<Im≤T, не предполагая Re.
- Off-line ноль → N_found < N_strict → FAIL. Наблюдаемо: 138 == 138 → off-line нулей нет.
- Зазор-контроль: мин. зазор соседних нулей 0.608 при scan_step=0.05 (запас ×12) →
  близкие пары не пропущены сканом.

## Skeptic (FL context-asymmetry: дан только claim + числа)
- Вердикт v1: **NEEDS-STRICTER** — точечный S(T)=+0.29 на сетке ≠ интеграл Тьюринга;
  off-line ноль + пропущенная пара дали бы похожий S.
- Усиление: эвристика θ/π+1 заменена на `mp.nzeros` (строгий Turing count) → **SOLID-IN-WINDOW**.
- Остаточный caveat (ACCEPTED): cross-library независимость не достигнута → см. claim.md «NOT mean» п.3.
