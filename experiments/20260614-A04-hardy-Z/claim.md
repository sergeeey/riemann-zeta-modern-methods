# Claim — A-04 · Hardy Z(t) + Turing verification
Date: 2026-06-14
Ladder tier: Full

## FL Step -5: Zero-Signal Gate
- Entity: нетривиальные нули ζ(s) в окне 0<Im≤300
- Falsifiable predicate: число нулей на Re=½ (смены знака Z) = число нулей в полосе (Turing count) ⟺ off-line нулей нет
- Measurable outcome: N_found == mp.nzeros(300) → PASS; ≠ → FAIL (off-line / пропущенная пара)

## FL Step -2: Question Type
[ ] Descriptive   [ ] Predictive   [x] Structural/Mathematical (верификация в конечном окне)

## FL Step 0: The Claim
> Все 138 нетривиальных нулей ζ(s) с 0<Im≤300 лежат на критической прямой Re=½;
> off-line нулей в окне нет. Подтверждено ДВУМЯ независимыми алгоритмами:
> смены знака Hardy Z(t) (Re=½) == Turing-count mp.nzeros (полоса).

## FL Step 1: Smallest Testable Hypothesis
> N_found (sign changes of Z) == N_strict (mp.nzeros) для T=300. Результат: 138 == 138. PASS.

## What this does NOT mean
1. НЕ доказывает RH — конечное окно [0,300], не ∀T (gap A-04 «некоторые ≠ все» остаётся открыт).
2. НЕ новый результат — Hutchinson 1925 проверил ровно 138 нулей до T=300. Это независимое
   современное подтверждение + рабочий НЕтавтологичный верификатор, не открытие.
3. НЕ cross-library независимо — оба алгоритма внутри mpmath (разные код-пути, одна библиотека).
   Полная независимость = argument-principle contour (Arb/Sage) — НЕ сделано.
