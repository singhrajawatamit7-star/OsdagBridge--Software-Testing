# Test Execution Report: OsdagBridge QA Suite

**Report Reference:** OB-QA-TER-001  
**Historical result snapshot:** 2026-11-21 14:59:50 UTC  
**Recorded environment:** Windows 11, Python 3.13.7, Pytest 9.2.0  
**Official checkout:** `2cb7ddc8ab2d2e33bf86721cb8a219b82d02df74`  
**Important:** The results below are historical. A fresh CI run is required after this commit; these values are not a result for the current changes.

## 1. Recorded automated results
The committed CSV contains 105 records: 96 PASS and 9 XFAIL. The nine XFAIL statuses were normalized from the committed result reasons for known upstream blockers; this status correction is not a new test run.
| Outcome | Count |
|---|---:|
| PASS | 96 |
| XFAIL | 9 |
| SKIPPED | 0 |
| FAIL / ERROR | 0 |
| Total | 105 |

The previous CI run for commit `360dd0ccdc8ae5ddea5c3b326a682c29c78eb443` completed all four jobs (Ubuntu/Windows × Python 3.11/3.12). This does not verify the current patch.

## 2. Test scope
- `tests/unit/`: QA utility, validation, conversions and exporter.
- `tests/functional/`: independent reference-utility workflows and engineering-rule checks.
- `tests/integration/`: selected official source-file checks and documented upstream blockers.
- `tests/regression/`: regression checks scoped to independent `osdagbridge_core`.
- `tests/ui_simulation/`: UI-state simulation, not live desktop GUI automation.
A smoke test that confirms a stub's output does not establish that the intended application feature works.

## 3. Generate a fresh report
```bash
python -m pytest tests -v --tb=short --junitxml=reports/test_results/junit.xml --html=reports/test_results/test_report.html --self-contained-html
python scripts/export_junit_csv.py reports/test_results/junit.xml test_results.csv --strict
```
The exporter maps `type=pytest.xfail` to XFAIL and ordinary skips to SKIPPED.

## 4. Separate manual scenario matrix
The separate `reports/test_results.csv` contains 50 documented scenarios: 45 PASS, 2 FAIL and 3 BLOCKED. These recorded statuses are not the automated Pytest results. SVG files under `reports/screenshots/` are wireframes/mockups, not genuine screenshots of the official desktop application.

## 5. Defect scope
OB-BUG-001 through OB-BUG-003 and OB-BUG-008 through OB-BUG-016 are documented official-application findings and remain open upstream. OB-BUG-004 through OB-BUG-007 are scoped to the independent QA reference utility. Defect reproduction tests confirm observed behavior; they do not repair the official application.

## 6. CI and conclusion
See [GitHub Actions](https://github.com/singhrajawatamit7-star/OsdagBridge--Software-Testing/actions). A new successful run is required before using this as final post-change evidence. The repository is a QA portfolio, not proof that all OsdagBridge features are operational.
