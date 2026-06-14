# parked — Hilbert–Pólya через Zenodo/Marchenko-кластер (вход для A-12)
ID: 20260614-hilbert-polya-zenodo-cluster
Date: 2026-06-14
Verdict: **ARCHIVE (parked — валидно, но deprioritized)**
Связь: атом **A-12** (Гильберт–Пойя, спектральный подход)

## Что именно отложено
НЕ сам атом A-12 (он остаётся активным) — отложен КОНКРЕТНЫЙ ВХОД: кластер
самопубликованных «доказательств RH через самосопряжённый оператор» 2025–26
как фундамент. Центральная работа — Lawrence Ip, Marchenko-инверсия из ξ(s).

## Почему parked, а не reject
Сам подход Hilbert–Pólya / inverse-scattering → RH **легитимен и рецензируем**
(Springer 2002). Отложен не подход, а пригодность САМОПУБЛИКАЦИЙ-2025 как
фундамента. Это deprioritize источника, не фальсификация направления.

## Находки [VERIFIED-web 2026-06-14]
- Ip, «A Classical Proof of RH via Self-Adjoint Spectral Theory» (Zenodo 15393055,
  май 2025) = self-deposited preprint, НЕ peer-reviewed, independent verification — нет.
- Конструкция: ξ(s) → Marchenko → V с finite-prime-sum cutoff. **Вход инверсии из
  абстракта НЕ ясен → циркулярность не разрешена.** Авторский caveat «no zeros lost
  in norm-resolvent limit» = их же признанный незакрытый атом M-06.
- Ещё ≥5 конкурирующих самопубликаций того же жанра (Zenodo 15334802 / 17220910 /
  19203882, preprints.org 202507.1370, Souto 2026). Ни одна не рецензирована.
- Консенсус даже в поисковой выжимке: «do not prove RH, reformulate as spectral problem».
- Предложенный numeric (спектр H₅₀ vs нули Одлызко) = **ТАВТОЛОГИЧЕН** (independent
  skeptic verdict + Validation Theater Guard): Marchenko строит V из данных →
  спектр = вход by construction. Тест не может провалиться → ничего не подтверждает.

## Триггер возврата (revival)
Вернуться к конкретной работе ТОЛЬКО если: (a) прошла peer-review, ИЛИ
(b) появилась independent verification, ИЛИ (c) построен оператор с **бесконечным**
спектром в биекции с нулями, **не собранный из самих нулей**.

## Смена входа для A-12 (что делать вместо)
Входить через РЕЦЕНЗИРУЕМОЕ, не через Zenodo-2025:
1. **Bender–Brody–Müller 2017** (PRL 118.130201) + критика **Bellissard** (arXiv
   1704.02644) — разобрать ПОЧЕМУ PT-подход провалился (оператор не самосопряжён).
   Учиться на вскрытой попытке > верить самопубликации.
2. **Inverse-scattering → RH: Springer 2002** (10.1023/A:1015813727650) — настоящий
   корень метода Ip, на 23 года старше и рецензирован.
3. **Connes 1999** (trace formula), **Berry–Keating 1999** (H=xp, полуклассика).
- Первый шаг A-12: разбор Bellissard-критики как «карты мин» (почему конечный
  спектр / не-самосопряжённость убивают кандидатов).

## Honest-тесты (если дойдёт до numeric — НЕ тавтологичный)
- **T1 negative control:** прогнать конвейер на GUE-последовательности vs нули ζ.
  Одинаковый результат → метод не различает → тавтология вскрыта.
- **T2 out-of-sample:** построить из первых 25 нулей → предсказать нули 26–100.
- **T3 self-adjointness (deficiency indices)** — свойство НЕ закодировано во входе.

## Источники
Zenodo 15393055 (Ip), 15334802, 17220910, 19203882; preprints.org 202507.1370;
PRL 118.130201 (BBM); arXiv 1704.02644 (Bellissard); arXiv 2404.00583;
Springer 10.1023/A:1015813727650 (inverse scattering & RH, 2002).
