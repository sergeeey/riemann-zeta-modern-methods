# Decision — A-04
Date: 2026-06-14

## Verdict: PROMOTE (SOLID-IN-WINDOW)
Claim прошёл positive control + negative control + skeptic (после усиления).

## Обоснование
- N_found == mp.nzeros(300) = 138 — два независимых алгоритма сошлись
- off-line нулей до T=300 нет (строгий вывод, не эвристика)
- positive control Odlyzko ✓ (9.4e-19), residual ✓ (1e-28)
- skeptic NEEDS-STRICTER → усилено → SOLID

## Caveats (приняты, см. claim.md «What this does NOT mean»)
- Конечное окно ≠ доказательство RH
- Известный результат (Hutchinson 1925)
- Не cross-library (оба алгоритма mpmath)

## Артефакты
- run.py — воспроизводимый скрипт (≈23 c, dps=30)
- note.md — исходный sandbox-черновик + Zero-Signal Gate
- claim.md, controls.md — FL

## Next (опционально, отдельный заход)
- Расширить окно (T=1000+)
- argument-principle contour → cross-library независимость (закрыть последний caveat)
