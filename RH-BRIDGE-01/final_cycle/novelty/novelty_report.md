# Новизна конгруэнции B4-06: результат поиска (2026-11-23)

**Вердикт: `not_novel` — `known_by_specialization`.** Конгруэнция `p·a_{n1} ≡ −a_{n0} (mod p)` для коэффициентов ℘ кривой `y²=x³−x` (`p ≡ 3 mod 4`, `n0=(p+1)/4`, `n1=p·n0`) следует из опубликованных конгруэнций Катца и Челлали для чисел Бернулли–Гурвица в суперсингулярном случае подстановкой индексов (случай `l=0`, `n=p−1`). Как результат о конгруэнции она не новая. Уверенность: **средняя–высокая**, оговорки ниже.

L0: описательный/структурный вопрос о литературе. Критерий столкновения заморожен до поиска: `frozen_claim.md`.

## 1. Как получен вердикт

Два скринера, слепых друг к другу: **S1** (собственные термины; 11 раундов; `S1_log.md`) и **S2** (смежные словари: числа Гурвица, формальные группы, p-адические числа Эйзенштейна–Кронекера, лемнискатические функции; 12 раундов; `S2_log.md`). **Независимо пришли к одной и той же ближайшей работе** (`independent = true`, `agreed = true`).

Ключевой источник, прочитанный мной в первоисточнике (arXiv, полный текст раздела 5):

- Bannai–Kobayashi, *Integral structures on p-adic Fourier theory*, arXiv:0804.4338, §5. Модель `y²=4x³−g2x−g3`, CM по `O_K`, `p` инертно в `K`, хорошая суперсингулярная редукция; `℘(z)=z⁻²+Σ_{n≥2} BH(n+2)/(n+2)·zⁿ/n!`;
  `L(n) = (1−b^{n+2})(1−pⁿ)/(γⁿ·p^{[np/(p²−1)]}) · BH(n+2)/(n+2)`, `γ^{p²−1} = −ε⁻¹·(p²)!/(p^{p+1}(p²−1))`, `−εp` — Фробениус над `F_{p²}`.
- **Теорема 5.1 (Katz [Ka2, Thm 3.11])**: `L(n)` целое; `L(n+p^l(p²−1)) ≡ L(n) mod p^l`.
- **Теорема 5.2 / 5.8 (Chellali [Ch, Thm 1.1])**: при `n ≢ 0 mod p²−1`: `L(n+p^l(p²−1)) ≡ L(n) mod p^{l+1}`. Теорему 5.8 авторы B–K доказывают сами.

## 2. Моя проверка вывода (не со слов агентов)

Подстановка: коэффициент при `z^{4m−2}` равен `a_m = BH(4m)/(4m·(4m−2)!)`, то есть `BH(n+2)/(n+2) = a_m·n!` при `n = 4m−2`.

| шаг | значение | проверка |
|---|---|---|
| `m = n0` | `n = p−1` | точная арифметика, все `p ≡ 3 mod 4`, `p ≤ 59` |
| `m = n1 = p·n0` | `n' = p²+p−2 = n + (p²−1)` | то же |
| условие Челлали | `n = p−1 ≢ 0 mod p²−1` | то же |
| показатели `p` в знаменателях | `[np/(p²−1)] = 0`, `[n'p/(p²−1)] = p` | то же |
| факториалы | `v_p(n!)=0`, `(p−1)! ≡ −1`; `v_p(n'!)=p+1`, `n'!/p^{p+1} ≡ (p−2)! ≡ 1` | то же (и аналитически по Лежандру) |
| `γ` | `v_p((p²)!)=p+1`, `(p²)!/p^{p+1} ≡ 1`, `(p²−1) ≡ −1`, `ε=1` ⇒ `γ^{p²−1} ≡ 1` | то же; `ε=1`, так как Фробениус над `F_{p²}` для `y²=x³−x` есть `−p` (суперсингулярная, след 0) |
| `b` | `b^{p²+p} ≡ b^{p+1} (mod p)` для `b ∈ Z[i]`, так как `b^{p+1}=N(b) ∈ F_p` | перебор всех `b` mod `p` |

Итог: `L(n') ≡ L(n) (mod p)` превращается в `(1−b^{p+1})·(p·a_{n1} + a_{n0}) ≡ 0 (mod p)` (знак: `n!≡−1`). Для `b ∈ Z[i]` с `N(b) ≢ 1 mod p` (такой есть при `p ≥ 3`) множитель `(1−b^{p+1})` — единица, откуда `p·a_{n1} ≡ −a_{n0}`. Целость обоих чисел следует из целости `L(n)` (теорема 5.1). Все константы и показатели проверены точной арифметикой: `check_reduction.py`, `check_reduction.log` (0 расхождений для `p ≤ 59`). Независимо: исходная конгруэнция проверена точно для `p=3,7,11,19` (S1, S2, аудитор) и доказана в Lean (`b4_06_kernel_report.md`).

## 3. Что остаётся без перекрытия

- **`a_{n0}` — p-адическая единица.** Это утверждение в найденных теоремах не содержится (конгруэнция его не даёт). Элементарно (Куммер + Вильсон), в Lean доказано (`L5_phi_n0_unit`); как отдельный факт малосодержателен. Статус: `no_overlap_found` в границах поиска.
- **Элементарное доказательство без p-адического преобразования Фурье** (Лагранж–Бюрман + Фробениус + Вильсон) — метод, отличный от Катца и Бананя–Кобаяси; его новизна не оценивалась. **Формализация в Lean** этого частного случая — отдельный факт, не научный результат.
- **Критерий `c^{(p²−1)/4} ≡ −1` для первого резонанса Дворка** (шаг B4-05/B4-06) не искался: это свойство конкретной конструкции авторов RH-доказательства, не классической конгруэнции.

## 4. Другие найденные работы (`related`, перекрытия нет)

Hurwitz 1899 (Math. Ann. 51, лемнискатические коэффициенты, те же нормировки, но нет связи `n0 ↔ p·n0`); Katz, Math. Ann. 216 (1975) 1–4; Snyder, Acta Arith. 40 (1982) 175–191 (конгруэнции Куммера, шаг `p−1`); Guerzhoy, Compositio 141 (2005) (кривая `y²=x³−δ`, `p ≡ 2 mod 3`); Ônishi (arXiv math/0406096) и Ônishi–Sairaiji (arXiv 2108.09013), Goto (arXiv 2204.04425) — только расщепимые простые; Barsky 1975/76 — ординарный случай; Krattenthaler–Müller (arXiv 2304.11471), Ahlgren et al. (arXiv 2502.16917), Guerzhoy (arXiv 2403.02592), Luecke–Peterson (arXiv 2506.07420) — смежные.

## 5. Формат протокола

```json
{
  "decision": "not_novel",
  "classification": "known_by_specialization",
  "confidence": "medium-high",
  "vocabularies_searched": ["own", "Hurwitz numbers / Eisenstein sums over Z[i]", "formal groups (Honda, ASD, Dwork)", "p-adic Eisenstein–Kronecker / sigma", "lemniscatic function coefficients"],
  "screeners": {
    "S1_own_phrasing": {"rounds": 11, "overlapping_found": 1},
    "S2_adjacent_vocab": {"rounds": 12, "overlapping_found": 1},
    "independent": true,
    "agreed": true
  },
  "relative_recall": {
    "benchmark_prespecified": ["Hurwitz 1899", "Katz 1975", "Honda 1970", "Bannai–Kobayashi 2010 (Duke)"],
    "benchmark_returned": 3,
    "score": 0.75,
    "missed": ["Honda 1970, J. Math. Soc. Japan 22"],
    "note": "recall < 1.0: the search would not support a 'novel' verdict; the verdict here is not_novel, which does not depend on recall"
  },
  "citation_chase": {"performed": false,
    "skipped_reason": "not required for not_novel (overlap found); OpenAlex and Semantic Scholar rate-limited (429) in this session"},
  "most_similar_papers": [
    {"title": "Congruences entre nombres de Bernoulli-Hurwitz dans le cas supersingulier", "author": "Chellali", "year": 1990, "venue": "J. Number Theory 35, 157-179", "doi": "10.1016/0022-314X(90)90110-D", "overlap": "Thm 1.1 at l=0, n=p-1", "fulltext_read": false, "restatement_read_in_primary": "Bannai-Kobayashi arXiv:0804.4338 Thm 5.2/5.8"},
    {"title": "Divisibilities, congruences, and Cartier duality", "author": "Katz", "year": 1982, "venue": "J. Fac. Sci. Univ. Tokyo IA 28, 667-678", "overlap": "Thm 3.11, integrality and base congruence", "fulltext_read": false},
    {"title": "Integral structures on p-adic Fourier theory", "author": "Bannai, Kobayashi", "year": 2008, "venue": "arXiv:0804.4338", "overlap": "Thm 5.1, 5.2, 5.8 (statements and proof)", "fulltext_read": true}
  ],
  "limits": "Original texts of Katz 1982 and Chellali 1990 not obtained (paywall); conventions (eps, gamma, model) taken from the Bannai–Kobayashi restatement; Carlitz 1941/49/62, Lang 1969, Gunji 1976 not opened; no German/French queries in S1; no patents; no citation chase."
}
```

## 6. Решение

`CLOSE` для направления «B4-06 как публикуемая конгруэнция». Lean-теорема остаётся как независимая формальная проверка частного случая известного результата Катца–Челлали (полезна как формализация, не как новизна). Чтобы поднять уверенность до «высокой», достаточно получить оригинал Chellali 1990 (J. Number Theory 35) или Katz 1982 (J. Fac. Sci. Univ. Tokyo IA 28) и сверить соглашения `ε`, `γ`, модель.
