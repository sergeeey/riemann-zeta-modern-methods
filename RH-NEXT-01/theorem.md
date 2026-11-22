# theorem.md — точная постановка (заморожена до проверки, версия H1_v1)

## Исходная теорема (первоисточник, дословно из Lean)
Зеркало Deicyde/riemann-hypothesis, коммит 40e56bab026552e089d7afcfeff08d2defb9c005.

Файл `src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean` [VERIFIED: прочитан]:

```lean
def WindowHypU (g : ℝ → ℝ) (θ δ : ℝ) : Prop :=
  ∀ η : ℝ, 0 < η → ∀ U₀ : ℝ, ∃ U : ℝ, U₀ ≤ U ∧ ∃ R : ℝ → ℝ,
    IntegrableOn (fun u => R u * Real.exp (-θ * u)) (Icc U ((1 + δ) * U)) ∧
    (∀ u ∈ Icc U ((1 + δ) * U), 0 ≤ R u ∧ g u ≤ R u) ∧
    ∫ u in Icc U ((1 + δ) * U), R u * Real.exp (-θ * u) ≤ Real.exp (η * U)
```

Файл `.../LandauTheorems/landauWindow.lean` [VERIFIED: прочитан], теорема `Deduction.landau_window`:
`(hP : PoleData g Φ Z) (hθ : 0 < θ) (hθ1 : θ < 1) (hδ : 0 < δ) (hW : WindowHypU g θ δ) : ∀ ρ ∈ Z, ρ.re ≤ θ`.

`PoleData g Φ Z` (там же, в LandauZeroFreeCriterion.lean): g измерима; |g u| ≤ C·e^{2u} при u ≥ 0; Φ — преобразование Лапласа g при Re s > 2; Z дискретно, Re > 0; Φ голоморфна на {Re s > 0} \ Z; в каждой точке Z простой полюс с c ≠ 0 (для вещественного ρ: c > 0).

Поточечная версия, которую используют для ζ (`ZeroFreeOfRpowWindow.lean`):
`zeroFree_of_rpow_window (F : CharFamily) {θ δ C} (hθ : 0<θ) (hθ1 : θ<1) (hδ : 0<δ) (h : ∀ Y₀, ∃ Y ≥ Y₀, ∀ y ∈ Icc Y (Y^(1+δ)), Gm F y ≤ C*y^θ) : ZeroFree F θ`.
Она выводится через `windowHyp_of_rpow` (мажоранта R = |C|·y^θ).

## Вывод по постановке
Заключение не требует оценки «в каждой точке окна». Формальная гипотеза уже допускает любую мажоранту R ≥ max(g,0) с интегральным условием. Исключительное множество входит автоматически через выбор R.

## Замороженная формулировка H1_v1
Выбрана одна формулировка: интегральная мера (не плотность и не геометрия пропусков), потому что именно она входит в `WindowHypU`.

В координате u = log y. Пусть выполнено PoleData g Φ Z, 0 < θ < 1, δ > 0. Допустим: ∃C ∀η>0 ∀U₀ ∃U ≥ U₀ ∃ измеримое E ⊂ [U,(1+δ)U]:
- (i) g(u) ≤ C·e^{θu} для u ∈ [U,(1+δ)U] \ E;
- (ii) ∫_E max(g,0)·e^{-θu} du ≤ ½·e^{ηU}.

Тогда для всех ρ ∈ Z: Re ρ ≤ θ.
