# parked — INDEX

Реестр **валидных, но отложенных** направлений (FL-протокол: ARCHIVE).
Отличие от `null_results/`: там — ОПРОВЕРГНУТО (не возвращаться); тут — валидно, но deprioritized (вернуться при триггере).

Перед новым заходом:
```
grep -i "keyword" parked/INDEX.md   # если совпало → прочитать заметку + revival-триггер
```

| ID | Дата | Slug | Почему отложено | Триггер возврата |
|----|------|------|-----------------|------------------|
| 20260614-hilbert-polya-zenodo-cluster | 2026-06-14 | hilbert-polya-zenodo-cluster | Кластер самопубликаций «RH через оператор» (2025–26) не peer-reviewed; предложенный вход для A-12 циркулярен | Peer-review / independent verification любой из работ ИЛИ оператор с ∞-спектром, не собранный из самих нулей |
| 20260717-B01-connes-replication | 2026-07-17 | B01-connes-replication | Репликация Connes 2026 (Letter to Riemann) реальна (source trace PASS), но точный рецепт — многоступенчатый эмпирический pipeline (скан по α + eigenvalue tracking D(α,k) + оператор D₀(α) + eigenvector-matching), не разовый скрипт; kill criterion «>2 сессии» превышен на порядок | ≥2 недели выделенного времени на эту одну репликацию, ИЛИ §4 arXiv:2106.01715 (Connes-Consani) окажется проще эмпирической части при повторном чтении |
