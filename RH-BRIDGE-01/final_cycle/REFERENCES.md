# Источники H-12 (ветка bridge-discovery-01) и состояние их проверки

Метки: `[CROSSREF]` — выходные данные получены из Crossref в сессии закрытия 2026-11-23; `[READ]` — текст читался в этой работе; `[SCREENER]` — взято из отчёта скринера поиска новизны, координатором независимо не проверено; `[BIB]` — выходные данные взяты из списка литературы прочитанной работы; `[UNVERIFIED]` — не проверено.

## Ключевые для вывода о новизне B4-06

| источник | данные | состояние |
|---|---|---|
| Bannai, Kobayashi, *Integral structures on p-adic Fourier theory*, Ann. Inst. Fourier 66 (2016) 521–550 | DOI `10.5802/aif.3018`; arXiv:0804.4338 (v3) | `[CROSSREF]` `[READ]` §5, Thm 5.1, 5.2, 5.8 |
| Chellali, *Congruences entre nombres de Bernoulli-Hurwitz dans le cas supersingulier*, J. Number Theory 35 (1990) 157–179 | DOI `10.1016/0022-314x(90)90110-d` | `[CROSSREF]`; оригинал не получен (платный доступ); теорема 1.1 прочитана только в пересказе B–K |
| Katz, *Divisibilities, congruences, and Cartier duality*, J. Fac. Sci. Univ. Tokyo Sect. IA Math. 28 (1982) 667–678 (B–K цитируют как [Ka2], Thm 3.11) | без DOI | `[BIB]`; в Crossref не найден; оригинал не получен |
| Katz, *The congruences of Clausen–von Staudt and Kummer for Bernoulli–Hurwitz numbers*, Math. Ann. 216 (1975) 1–4 | DOI `10.1007/bf02547966` | `[CROSSREF]`; оригинал не читался |
| Hurwitz, *Über die Entwickelungscoefficienten der lemniscatischen Functionen*, Math. Ann. 51 (1899) | DOI `10.1007/bf01453637` (в Crossref выпуск датирован 1898) | `[CROSSREF]`; `[SCREENER]` читал стр. 196–218 из 31 по скану |
| Honda, *On the theory of commutative formal groups*, J. Math. Soc. Japan 22 (1970) 213–246 | DOI `10.2969/jmsj/02220213` | `[CROSSREF]`; эталонный набор; ни один скринер его не вернул |
| Bannai, Kobayashi, *Algebraic theta functions and the p-adic interpolation of Eisenstein–Kronecker numbers*, Duke Math. J. 153 (2010) 229–295 | DOI `10.1215/00127094-2010-024` | `[CROSSREF]`; эталонный набор |
| Blakestad, Grant, *On the universal p-adic sigma and Weierstrass zeta functions*, J. Number Theory 249 (2023) 348–376 | DOI `10.1016/j.jnt.2023.01.013` | `[CROSSREF]`; обычная редукция (цитируется в B4-05 как не применимая к суперсингулярному случаю) |
| Robert, *Congruences entre séries d'Eisenstein, dans le cas supersingulier*, Invent. Math. 61 (1980) 103–158 | DOI `10.1007/bf01390118` | `[CROSSREF]`; близкая по теме, **не читалась**, в отчётах скринеров не разобрана (`UNVERIFIED` на предмет перекрытия) |

## Из отчётов скринеров (`[SCREENER]`, координатором не проверены)

Snyder, Acta Arith. 40 (1982) 175–191; Guerzhoy, Compositio Math. 141 (2005) 583–590; Guerzhoy, arXiv 2403.02592; Ônishi, arXiv math/0406096 (Russian Math. Surveys 66 (2011) 871–932); Ônishi–Sairaiji, arXiv 2108.09013; Goto, arXiv 2204.04425; Luecke–Peterson, arXiv 2506.07420; Krattenthaler–Müller, arXiv 2304.11471; Ahlgren et al., arXiv 2502.16917; Lang, Abh. Math. Sem. Hamburg 33 (1969) 183–196 (DOI `10.1007/bf02992933`); Barsky, Groupe d'analyse ultramétrique 1975/76, exp. 17. Подробности и места в тексте: `novelty/S1_log.md`, `novelty/S2_log.md`.

## Материалы RH-проекта (источники статусов B4, SizeKRel, окна)

- Rubinstein, рабочий черновик `zeta-paper.pdf` (21.11.2026), sha256 `667d88b3c375adf0466678094f452ca966aef0f4d368f6340d2bd5328b7fb706`, §III.5 (`m(z)=log(σ_c(z)/t(z))`); URL в `unpacked/H12-PADIC-B4-05/audit.md`.
- Lean-зеркало `CocoSgt/riemann-hypothesis-lean`, коммит `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`: `src/Formalism/GaussJetBounds/Statement.lean` (`BHyp`), `…/GaussSumParity/StatementE.lean` (`BHypCurve`), `…/FrobeniusFibreCurves/CurveHyp.lean` (`phO`).
- Страница проверок Sutherland `math.mit.edu/~drew/grh` и заметки гексагональных/Zhang/Masullo: `literature_delta.md` (состояние на 22.11.2026 16:20 UTC).
- Источники архивов B4-06 с Drive и их SHA-256: `b4_06/src_zips/`, `SHA256SUMS.txt`; присланная внешняя оценка: `../external_assessment_2026-11-23.md` (`SUPERSEDED`).
