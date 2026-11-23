# final_cycle/ — индекс (H-12: CLOSED, 2026-11-23)

Порядок чтения: `final_assessment.md` → `checkpoint.json` → нужный отчёт ниже.

| файл / каталог | что внутри | статус результатов |
|---|---|---|
| `final_assessment.md` | итог: что доказано / проверено ядром / известно / открыто; условия повторного открытия R1–R5 | единственный авторитетный итог |
| `checkpoint.json` | состояние, коммиты, закреплённые статусы, открытые обязательства, восстановление | — |
| `b4_06_kernel_report.md` | B4-06: компиляция четырёх присланных кандидатов, универсальная теорема, аудит формулировки, чего нет в Lean | `KERNEL_CHECKED` (только `lagA`) |
| `b4_06/lean/` | `B4_06_Universal.lean` (итог), модули `L1`, `L2`, `L3a`, `L3b`, `Final.lean`; `dev/` — каркас с `sorry` и бриф исполнителям (не результат) | — |
| `b4_06/candidates/` | четыре присланных файла «как получены» (`original/`) и после правок (`fixed/`) | — |
| `b4_06/logs/`, `b4_06/scripts/` | журналы компиляций/аксиом/Python-проверок и скрипты | — |
| `b4_06/src_zips/`, `b4_06/unpacked/` | присланные архивы Drive (с SHA-256) и их распаковка; чужой материал, не изменялся | внешний |
| `novelty/` | замороженный критерий, логи двух скринеров, `novelty_report.md`, `check_reduction.py/.log` | `NOT_NOVEL` |
| `rh_mathematical_skeleton.md`, `skeleton/` | карта каркаса доказательства `riemannHypothesis` | `SOURCE_TRACED` |
| `zplus_applicability.md`, `zplus/` | применимость Lemma Z+ к `TheoremFSharp` | `CONDITIONAL / NOT_APPLICABLE_WITH_CURRENT_ASSUMPTIONS` |
| `closure/closure_verification.log` | новые проверки при закрытии: хэши, компиляция, аксиомы, архив | `KERNEL_CHECKED` |
| `REFERENCES.md` | источники и состояние их проверки | — |
| `SHA256SUMS.txt` | суммы файлов этого каталога; все четыре папки архива (`RH-BRIDGE-01`, `RH-NEXT-01/02/03`): `../SHA256SUMS-ALL.txt` (пути от корня worktree, проверка `sha256sum -c RH-BRIDGE-01/SHA256SUMS-ALL.txt` из корня) | — |
| архив `../H12-FINAL-CYCLE-01-2026-11-23.zip` | всё `RH-BRIDGE-01` + отрицательные результаты серии B (`RH-NEXT-01/02/03`); распаковывать в корень worktree | — |

Вне `final_cycle/` (ранние миссии): `../rh_attribution.md`, `../verification/refgraph/` (граф ссылок), `../critical_dependencies.md`, `../candidate_lemma.md`, `../literature_delta.md`, `../proof_or_counterexample/` и др.; их устаревшие места помечены в `../checkpoint.json` (`state_2026_11_23`).

Проверка самого архива (распаковка, обе таблицы сумм, побайтовое сравнение с деревом) записана после его сборки в `../closure_archive_verification.log`; этот файл в архив не входит (иначе его сумма была бы неверна).

Воспроизведение главного результата (WSL, Lean 4.33.1, Mathlib `0df444a3…`, проект `~/h12/rh`):
`cd ~/h12/rh && lake env lean <путь>/final_cycle/b4_06/lean/B4_06_Universal.lean` — код 0, аксиомы `[propext, Classical.choice, Quot.sound]`.
