# Test Execution Report: OsdagBridge QA Suite

## Evidence status

**This document is a reporting template and historical-record summary, not proof of a fresh local run performed by this revision.** The repository previously recorded a run dated 2026-11-21 20:15 UTC on Windows 11 / Python 3.13.7 / Pytest 9.2.0. That historical report stated 105 automated tests: 96 passed and 9 strict expected failures. Those numbers have not been independently re-executed during this repository edit and must be treated as historical until regenerated.

## Reproduce the current run

From the repository root, in a clean environment:

```bash
python -m pip install -r requirements.txt
python -m pytest tests -v --tb=short --junitxml=reports/test_results/junit.xml
python scripts/export_junit_csv.py reports/test_results/junit.xml test_results.csv --strict
```

The CSV exporter records five distinct outcomes:

| Status | Meaning |
|---|---|
| PASS | Test completed successfully |
| FAIL | Assertion failure |
| ERROR | Test raised an unexpected error |
| XFAIL | Test failed as expected under an explicit pytest xfail marker |
| SKIPPED | Test did not execute because of a skip condition |

A strict XPASS is a CI failure and must be investigated. Never count XFAIL as a pass or merge XFAIL with SKIPPED.

## Test scope

The suite contains both tests of the official OsdagBridge checkout and tests of the separate `osdagbridge_core` reference utility. These scopes must be reported separately. A successful test of the reference utility is not evidence that the official application calculation engine works. Tests that assert the behavior of a placeholder or stub reproduce a defect; they do not verify functional completion.

## Manual execution evidence

The project tracks 50 manual scenarios in `test_cases.csv`. The previously recorded matrix reported 45 PASS, 2 FAIL and 3 BLOCKED. Treat these as historical records only; regenerate the manual execution log with date, environment, operator, observed result and linked evidence before using these figures as current results. SVG wireframes are design artifacts, not screenshots of the running official application.

## Defect tracking

The authoritative defect register is `issues.csv`. Keep issue IDs unique and synchronize test markers, evidence references and documentation whenever an ID changes. Upstream defects must remain OPEN until a fix is confirmed in the official OsdagBridge source and a regression test passes.

## Release decision

**Conditionally verified as a QA portfolio; not fully release-approved.** A release claim requires a fresh test run, matching JUnit/CSV counts, successful CI matrix, verified defect references and genuine manual evidence. See `documentation/release_checklist.md`.


## GitHub Actions verification (2026-11-22)

The main-branch workflow run [45010909943](https://github.com/singhrajawat7-star/OsdagBridge--Software-Testing/actions/runs/45010909943) completed with success on all four configured jobs: Ubuntu/Python 3.11, Ubuntu/Python 3.12, Windows/Python 3.11 and Windows/Python 3.12. The tested commit was `d6759d22995acea5cf152c88a36c3ef9af42767f`. Any subsequent commit requires checking its own workflow run.

This CI result is distinct from a fresh local execution of the complete test suite and from manual execution of the official desktop application. The latter two remain outstanding until the operator runs them and records the outputs.
