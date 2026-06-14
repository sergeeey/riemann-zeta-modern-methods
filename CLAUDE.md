# H-12 · Гипотеза Римана
Тип проекта: **research** → FL Full-Ladder + EstimandOps L0 + skeptic-triggers
Начат: 2026-06-14

## Цель
Систематическое исследование Гипотезы Римана.
Метод: атомизация → изучение каждого атома отдельно → синтез.

## Стратегия (порядок строгий)
1. **ЗАФИКСИРОВАТЬ** — оригинал 1859 + что доказано (`.claude/memory/riemann_foundation.md`)
2. **АТОМИЗИРОВАТЬ** — независимые подзадачи (`.claude/memory/riemann_atoms.md`)
3. **ИССЛЕДОВАТЬ** — каждый атом: FL Full-Ladder, отдельная папка `experiments/<atom>/`
4. **АУДИТ** — Grant papers как один из подходов (`experiments/grant-audit/`)
5. **СИНТЕЗИРОВАТЬ** — объединить результаты

## Материалы в папке
- `REG-iharmonic-Riemann-Hypothesis-M2026.pdf` — Grant (2026) [HYPOTHESIS, не peer-reviewed]
- `Supplement-Proof-for-Academic-Reviewers-Referees.pdf` — Grant (2026) [HYPOTHESIS, не peer-reviewed]

## Правила проекта
- Факт = только [VERIFIED] (доказанные теоремы)
- [HYPOTHESIS] = интересно, но не факт — требует FL-аудита
- Grant papers = изучаем ПОЗЖЕ, не строим на них фундамент
- Любое "100%", "доказано", "точно" → запускать skeptic agent
- Не браться за несколько атомов одновременно

## FL Status для этого проекта
- EstimandOps L0: Structural (доказать, что утверждение о структуре нулей истинно)
- Falsification predicate: ∃ ноль с Re(s) ≠ ½ → опровергает; доказательство невозможности → доказывает
- Ladder tier: Full (математическое доказательство, высший риск)
