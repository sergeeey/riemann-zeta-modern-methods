# boyko-project-radar — H-12, полный скан (весь проект)
Дата: 2026-08-27 · Сканеры: atomize, deletion-test, research-audit, sci-code-audit (все 4 реально
прогнаны, не пересказаны) · Пропущено: skill-audit (опционален)

Этот файл — персистентная запись находок, которые иначе существовали только в диалоге
сессии 2026-08-27 и были бы потеряны при следующей заморозке/сбое.

---

## atomize — 7 атомов проекта, top-3 bottleneck

| Atom | Type | Quality | Importance |
|---|---|---|---|
| Core: zeta toolkit (src/zeta/) | Core | 2/5 | 5/5 |
| Test: автоматическая верификация | Test | **1/5 (отсутствует)** | 5/5 |
| Core: research-атомы/эксперименты | Core | 4/5 | 5/5 |
| Memory: state & реестры | Memory | 4/5 | 4/5 |
| Docs: планирование/синтез | Docs | 2/5 | 3/5 |
| Infra: зависимости/CI | Infra | 2/5 | 3/5 |
| Integration: git/branch/cross-repo | Integration | 2/5 | 3/5 |

**Bottleneck #1:** Test — 0 файлов `test_*.py`, 0 `assert` во всём репо. toolkit.py (общий
код, реально 9 файлов-потребителей — см. deletion-test ниже) не защищён регрессией.
**Bottleneck #2:** Docs — ROADMAP.md/PLAN-2026H2.md/SYNTHESIS.md/LANDSCAPE-NOTE.md дрейфуют
от реальности; дрейф уже материализовался (ROADMAP показывал 0% для закрытых атомов, Track H
hygiene fix 2026-07-19).
**Bottleneck #3:** Integration — ветка `feat/h12-track-c1-evidence-gate` не запушена >месяц.

**/goal (bottleneck #1):**
```
/goal src/zeta/toolkit.py защищён pytest-регрессией на известных нулях
(γ₁≈14.134725, γ₂≈21.022040, γ₃≈25.010858 — Odlyzko/LMFDB verified) и на
функциональном уравнении ξ(s)=ξ(1-s).
Run python -m pytest tests/test_toolkit.py -v and show full output.
Output must contain: "passed" and zero "FAILED".
Do NOT modify experiments/*/run.py.
Do NOT change numerical precision (dps) defaults in toolkit.py without justification.
or stop after 15 turns.
```

---

## deletion-test — coupling

- `src/zeta/toolkit.py` — fan-in = **9** (не "14 атомов", это была самокоррекция в сессии:
  первичная оценка atomize была неточной, deletion-test её поправил grep'ом). Реальные
  потребители: A-04, A-07, A-09/compute_zeros, A-10 (×3 файла), A-12, sandbox-B06,
  sandbox-a08map. **A-05, A-06, A-08, B-02, B-07 toolkit НЕ используют** — переизобретают
  mpmath-обвязку инлайн.
- `src/zeta/reference.py` — fan-in=1 (только B-03), но 🟢 HEALTHY: маленький, честно
  задокументирован как external positive control (Odlyzko).
- `experiments/*/visualize.py` ×7 (497 строк) — 🟡 DUPLICATE: общий JSON-loading/
  figure-styling boilerplate повторяется, сама логика графиков разная и честная.
- `scripts/build_roadmap_xlsx.py` — 🔴 **вероятно DEAD**: fan-in=0, ни одного `.xlsx`
  файла в репо за 2.5 месяца существования скрипта. Требует решения: прогнать или удалить.
- `sandbox/a08_zerofree_map.py`, `kappa_theta_landscape.py` — 🟢 HEALTHY, честные RECON-
  дисклеймеры прямо в docstring.

---

## research-audit — score 8/10

**Паттерн отказов, 2 устойчивых корня:**
- Численная стена на экстремальном масштабе (3 случая: B-02, B-03-closepair, B-06) —
  precision/разрешение отказывает на малом t / большом T / близких парах.
- Циркулярность/скрытое допущение Re(s)=½ (2 случая: A-06 Li первая версия, Grant Doc A) —
  проект сам поймал этот паттерн (задокументирован в riemann_approaches.md §3 ДО того,
  как повторился в A-06 — методология предсказала собственную будущую ошибку).

**Zombie-гипотезы:** не обнаружено активных. Near-miss risk: external-100 каталог мог бы
реинтродуцировать уже убитые/запаркованные паттерны (heat-flow, NB, Weil-positivity) без
проверки — предотвращено аудитом того же дня (`20260827-external-100-audit.md`).

**Критические untested assumptions (2):** toolkit.py регрессия (см. atomize #1); Robin
inequality проверена этим проектом только до N~10⁴-10⁵ (литература — до 10¹³).

**Pearl Registry:** отсутствует полностью — минимум 2 переносимых meta-находки (численная
стена; self-caught circularity) живут только прозой в activeContext/decisions.md.

**Q4 (cheapest next test):** B-04 (Hankel-миноры Ли) — независимый, дважды подтверждён
(этот аудит + external-100-audit того же дня).

---

## sci-code-audit — verdict PROVISIONAL

10 слоёв прогнаны на `toolkit.py` (141 строк) + experiments/*/run*.py:
- Layer 2 (silent fallbacks): 1 `except Exception: continue` во всём репо (A-07
  run_speiser.py:88) — проверен, legitimate/bounded (10 стартовых точек, residual-check
  после). Не риск.
- **Layer 4 (новая находка):** `find_zeros_on_critical_line` детектирует нули по смене
  знака Z(t) на фиксированном `scan_step` — структурно не видит чётную кратность корней
  (0 или 2 нуля внутри одного интервала). Это конкретный код-механизм за паттерном
  "численная стена на близких парах" (research-audit группа А). A-04 сам явно проверял
  margin эмпирически — не скрытый баг, известное и честно ограниченное допущение.
- **Layer 5:** 0 `assert` во всём репо — 4-е независимое подтверждение находки (после
  atomize, deletion-test, research-audit) с ещё одного угла.
- Layer 6 (controls): B-07 и adversarial_checks.py — реализованы корректно.
- Layer 9: уже самоисправлено раньше (`count_zeros_expected` докстринг, 2026-07-19).
- Layer 10: requirements.txt пиннит версии, но нет `smoke_test.py`.

---

## Синтез — 4 категории (итог дня)

**🔴 Узкие места:** нет тестов (4× подтверждено); Docs дрейф; scan_step слепота к близким
парам; build_roadmap_xlsx.py вероятно DEAD; ветка не запушена >месяц.
**🟢 Сильные места:** research-методология (4/5), memory/реестры (4/5), качество кода
toolkit.py (WHY-комментарии, честный дизайн), Skeptic Engine spin-off — реальная ценность.
**🟡 Нерешённые:** Pearl Registry отсутствует; B-04 дважды подтверждён, не начат; B-05
"gated behind B-01" — снято в этот же день (см. `PLAN-2026H2.md`); Robin только до 10⁴-10⁵.
**⚫ Слепые места:** математика 85/100 карточек external-100 не проверена; синхронизация
с skeptic-engine-manuscript не перепроверена; README на собственный дрейф не сверен;
skill-audit не запускался.

**Рекомендованная цепочка (МОЙ ВЫБОР на тот момент):** #1 — тест-сьют toolkit.py
(atomize bottleneck #1), самый дешёвый и наименьший риск "увязнуть".
