# Трасса `ra.miStar` вверх от `wire4F_alt` (2026-11-22)

Метод: чтение исходников в клоне `~/h12/rh` (коммит `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`), без компиляции. Пути ниже относительно `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/` (сокращение `TPS/`), если не указано иное. Уровень вопроса (L0): структурный. Статусы: `SOURCE_TRACED`, `NOT_RUN`, `OPEN`.

## Короткий ответ

В `wire4F_alt` терм `ra.miStar` **не доказывается, а берётся из предпосылки**: `hRows : RowsAtSelAlt …` — гипотеза импликации `Wire4Alt` (тип `Wire4Alt` — это `∀ … , RowsAtSelAlt … → … → ∃ C x₀, … DivisionPackageKernel'`). `ra` — запись типа `IndefiniteRealisationConstantBounds`, одно из полей которой — `miStar : MIstar2 …` для `Q = selI Fm hc x hx h i = (selB …).Q`. Конкретный терм, который эту предпосылку закрывает, строится на несколько слоёв выше и сводится к теореме `miStar2_of_allTrue_alt_alt`, питаемой 13 опубликованными утверждениями и данными семейства. `MIstar2` не является открытым входом всей конструкции. Но компиляция этого куска и аксиомы **не проверялись** (`NOT_RUN`: замыкание 45 153 модуля, 6,13 млн строк).

## Что такое `MIstar2` (`SOURCE_TRACED`)

`src/Formalism/LocalToGlobal/IndefiniteReal/IsometricPeriodsOfUnitHypotheses.lean:27`:
```
def MIstar2 (eV …) (sEE …) : Prop := ∃ d : X.MIDat fc, X.MIUnit2 d ∧ X.MIid eV sEE d ∧ X.AuNZ d
```
где `MIUnit2 d` (строка 21): V сохраняет норму на `EEl true`; матрицы `d.U u` сохраняют норму `fnorm`; `d.ζC u t ≠ 0` для всех u, t и нормирование `vw w k = 0` для единиц; `d.ζC u μ₀ = 1`. `MIid` (`IsometricPeriodsOfHypotheses.lean:99`): для всех u, t, φ, F выполнено `d.ζC u t · ι(Dc.Pt u t φ F) = d.a u · ⟪sEE (d.V (X.Θ t (X.jR t (eV t F)))), Sp.Pu u ((d.U u)·ι(φ))⟫_ℂ`, то есть алгебраический период `Pt` равен (с точностью до скаляров ζ и a) эрмитову спариванию тета-образа с U-повёрнутым столбцом; `AuNZ d := ∀ u, d.a u ≠ 0` (`:97`). Содержательно: существует согласованный набор данных (изометрия V, нормосохраняющие U_u, ненулевые скаляры ζ и a), реализующий это тождество периодов. Связь с PDF §III.7 (вход (S4), «mean of periods = log Ω_E») — по смыслу, определения PDF и Lean не сопоставлялись построчно.

## Цепочка вверх (`SOURCE_TRACED`)

| № | Что | Файл:строка |
|---|---|---|
| 1 | `wire4F_alt`; `⟨C, hC, x1, hr⟩ := hRows`; `⟨ra, hd⟩ := hr x hx h hx1 i`; в `CovolumeOntoIsometryConditions` поле `miStar := ra.miStar` | `TPS/Wire4F.lean:26, 45, 58, 63` |
| 2 | поле `miStar` структуры `IndefiniteRealisationConstantBounds`; `RowsAtSelAlt`, `Wire4Alt` | `TPS/IndefiniteRealisationChoice.lean:71, 77, 82, 89` |
| 3 | `wire_sel_alt`: подставляет `selI := indefiniteRealisationChoiceOfSelection selB`; предпосылка `RowsAtSelAlt` остаётся в типе `Wire4Alt` | `TPS/WireSel.lean:20, 50` |
| 4 | `indefiniteRealisationChoiceOfSelection selB := fun Fm hc x hx h i => (selB Fm hc x hx h i).Q`; `SelectionBundle` — функция в `RealTBAlt` | `TPS/TieTwRecOf.lean:22, 29` |
| 5 | `row_rRows_of_parts_alt`: собирает `IndefiniteRealisationConstantBounds` с `miStar := hM x hx (l7.trans hle) i`, где `hM` — компонента предпосылки `Row Q Lk (EvW (fun _ _ _ b => b.B.Q….MIstar2 …))` | `TPS/RowRRowsOfParts.lean:21, 60` |
| 6 | `row_rRows_stage0_alt`: эта предпосылка — `RL.RowMultiplicityCondition Q Lk` (в доказательстве имя `hMi`), передаётся как h₂ | `TPS/TupAllUsedAtPart.lean:46, 48`; `TPS/RowGood.lean:33` (определение условия) |
| 7 | `allRows_of_open0_alt`: `rRows := … row_rRows_stage0_alt …`, `o.mi` из `OpenParameterStatements` | `TPS/LinkROfIsLinked.lean:50, 80, 82`; `TPS/GeometricWeakTies.lean:39, 49` |
| 8 | `open0_of_unitary_group_hypotheses`: `mi` получает `hMi.2`, где `hMi := main_theorem_published_inputs_third_alt_alt <13 опубликованных входов, Hk3.howeUnram_holds> hL (extensionWithList hL cDep) SExt.none (geoCl anyGeometry)` | `TPS/OpenOrbitOfUnramifiedExponents.lean:50, 69, 75`; использован в `TPS/HypothesesNonemptyOfUnramifiedExponents.lean:46, 54, 57` |
| 9 | `main_theorem_published_inputs_third_alt_alt` = `miStarRow_alt_alt`; далее `main_theorem_published_inputs_variant_alt_alt` (`miStarRowClosing_alt_alt`), `main_theorem_published_results_final_alt_alt` (`miStar_row_alt_alt`) | `TPS/MainTheoremPublishedInputsThird.lean:22, 34`; `…Variant.lean:21, 31`; `…ResultsFinal.lean:24, 43` |
| 10 | `main_theorem_from_published_results_alt_alt_alt_alt := miStar2_of_allTrue_alt_alt`: для `W : RealPackAlt ex`, `AllFamilyConditions W`, `1 ≤ B.R.rS`, `PuNZ …` даёт `(packageCoefficientSpace W).MIstar2 …` | `TPS/MainTheoremFromPublishedResultsAltAltAltAlt.lean:23, 37` |
| 11 | абстрактный шаблон: `miStar2_of_anchored` строит `d := ⟨V, p/(b·c μ₀), U, c/c μ₀⟩` из `OpsUnit`, `Anchored`, `UnitAt`; `miStar2_of_families` вызывает `joint_star_product_nonvanishing` (ненулевость совместного звёздного произведения) | `src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/MiStar2OfAnchored.lean:15`, `…/StarProductNonvanishingLevels.lean:23`, `…/JointStarProductNonvanishing.lean:142` |

## Происхождение 13 опубликованных входов (`SOURCE_TRACED`)

`published_results_eigen O : UnitaryGroupThirdPlaceHypotheses` (`TPS/EveryCharacterOfLiteratureOfVWin.lean:666`) заполняет каждое поле теоремой `*_of_literature`. Для входов пункта 8 терм-доказательство таково (проверено чтением тела теоремы):

| Поле | Поставляющая теорема |
|---|---|
| `harishChandraFinite` | `PositivityTheory.RgHf.harishChandraFinite` (`src/Development/WeilBound/RepresentationTheoryGL/ConstantTermFiniteness/CuspidalConstantTerms/FiniteOfCuspOfConstTerm.lean:129`) |
| `cuspRapidDecay` | `GlobalTheory.RapidDecay.cuspRapidDecay` |
| `discreteSeriesCover`, `discreteSeriesClassification` | `CompanionTheory.RgExh.discreteSeriesCover`, `…discreteSeriesClassification` |
| `harishChandraModules` | `PositivityTheory.Stage1.PM.harishChandraModules` |
| `casselmanWallach` | `PositivityTheory.CWB.casselmanWallach` |
| `weilRepresentationUnitaryPair` | `GlobalTheory.weilRepresentationUnitaryPair` |
| `weilSiegelFormulaUnitary`, `siegelWeilUnitaryConvergent` | `UpperTheory.Lit.Sw47.weilUnitary`, `…convergent` |
| `doublingMethod` | `ResidueKilled.dm_of_two (cusp_rapid_decay_of_literature O) (siegel_eisenstein_continuation_of_literature O) trivial` (`TPS/EveryCharacterOfLiteratureOfVWin.lean:371`) |
| `unramifiedDoublingGL` | `GlobalTheory.UnramDoublingProof.unramifiedDoublingGL` |
| `strongApproxSU` | `GlobalTheory.StrongApproxSUProof.strongApproxSU` |
| `siegelWeilUnitaryConvergent2` | `GlobalTheory.CompanionTheory.SW.siegelWeilUnitaryConvergent` |
| `howeUnram` (прямо в вызове) | `GlobalTheory.Hk3.howeUnram_holds` |

Все 13 — теоремы библиотеки, не аксиомы и не `sorry` (статический поиск `axiom`, `sorry` по репозиторию, заявленный в README зеркала, дал 0; я его повторно не запускал). Только `doublingMethod` опирается на параметр `O` (через `siegel_eisenstein_continuation_of_literature O`); `O` строится из `Row0b` (Галуа) и `recTExists` (`TPS/…`: `everyCharacter_of_row ⟨h, recTExists, h⟩`, `src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean:7`).

## Ответы на вопросы B1

- **Тип и содержание.** См. выше: существование данных `MIDat` с `MIUnit2`, `MIid`, `AuNZ`.
- **Где вводится.** Как поле `miStar` в `IndefiniteRealisationConstantBounds` (`IndefiniteRealisationChoice.lean:77`), как условие `RowMultiplicityCondition` (`RowGood.lean:33`) и как поле `mi` в `OpenParameterStatements` (`GeometricWeakTies.lean:49`).
- **Откуда терм доказательства.** `hMi.2` из `main_theorem_published_inputs_third_alt_alt` (`OpenOrbitOfUnramifiedExponents.lean:50, 69`), внутри — `miStar2_of_allTrue_alt_alt`, внутри — `miStar2_of_families` / `joint_star_product_nonvanishing`.
- **Дополнительные содержательные условия.** Для конкретной упаковки `W`: `BotHyp W`, `LevHyp W`, `FamAllQ W`, `ServedQ W`, `PuNZ D`, `AllFamilyConditions W`, `1 ≤ rS`; в варианте с `RowDiag` — `GlobalTheory.Core.Rk.RowDiag (IsScaleWithBoundedGamma ∧ RankMu)`, который берётся из `diagonalRow_of_siegelWeil_unitary hSWU` (то есть из `P.siegelWeilUnitaryConvergent2`).
- **Попадание в конечный `Q`.** `Q := (selB Fm hc x hx h i).Q` (`TieTwRecOf.lean:29`) для выбора `selB : SelectionBundle`; условие `MIstar2` сформулировано на `b.B.Q` связки `b : BundleCondition` (`RowGood.lean:33`). Что `(selB …).Q` и `b.B.Q` — один и тот же объект, видно по совпадению типов `RealTBAlt`, но я это равенство не выводил (`OPEN` на уровне имён).
- **Доказательство `MIstar2 → l1b` не принимается за доказательство `MIstar2`.** Это разные утверждения: первое — теорема `isometric_periods_of_unit_hypotheses` (ядром проверена в предыдущей миссии), второе — результат пункта 10–11.

## Что остаётся

1. Ядерная проверка куска: `main_theorem_published_inputs_third_alt_alt` и `open0_of_unitary_group_hypotheses`. Размеры замыканий (текстовый подсчёт): `MainTheoremPublishedInputsThird` — 45 153 модуля, 6 132 422 строки; `OpenOrbitOfUnramifiedExponents` — 55 541 модуль, 7 055 176 строк. По скорости 18,9 строки на процессорную секунду (1043-модульная сборка предыдущей миссии) это около 90 процессорных часов, 13 часов на 8 ядрах (`INFERRED`). Не запускалось: нет новой диагностической потребности, пока не выяснено, входит ли этот кусок в проверку внешним сертификатом (по памяти H-12 три независимых ядра приняли весь снимок, не проверено мной).
2. Верность формулировок `GlobalTheory.Published.*` относительно литературы (13 входов): семантический аудит не проводился.
3. Тождество `(selB …).Q = b.B.Q` на уровне определений.
