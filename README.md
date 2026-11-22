# 🌉 OsdagBridge – Automated & Manual QA Suite
### Software Testing, Input Validation, Structural Verification & Issue Reporting for Plate Girder Road Bridges

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Testing-Pytest%209.2-orange.svg)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](https://github.com/features/actions)
[![Standards](https://img.shields.io/badge/Standards-IRC%3A24%20%7C%20IRC%3A6%20%7C%20IS%20800-purple.svg)](https://www.irc.nic.in/)
[![Status](https://img.shields.io/badge/Status-Conditionally_Verified-yellow.svg)](#quickstart-setup-instructions)

---

## 📌 Executive Summary

This repository is the complete **Software Testing & Quality Assurance Portfolio Project** for **[OsdagBridge](https://github.com/osdag-admin/OsdagBridge)**, the open-source structural-engineering software for bridge analysis developed under the Osdag initiative at IIT Bombay.

The project demonstrates end-to-end QA capabilities expected of a **Software Testing / QA Engineer**:

| Deliverable | Detail |
|---|---|
| **Official Application Integration** | Real integration tests executing CLI entry points, unit conversions, code registries, desktop entry points, and strictly isolating upstream blockers (`tests/integration/`) |
| **50 Documented Test Cases** | Detailed scenarios covering Installation, Project Management, Validation, Design, Results, Reporting, Error Handling, and Regression (`test_cases.csv` — **45 Passed, 2 Failed, 3 Blocked, 90.0% Pass Rate**) |
| **105 Automated Pytest Tests** | Real Pytest suite across `tests/unit/`, `tests/functional/`, `tests/integration/`, `tests/ui_simulation/`, `tests/regression/` (`test_results.csv` exported from `reports/test_results/junit.xml` — **96 Passed, 9 XFailed upstream blockers with strict enforcement**) |
| **16 Defect Records** | 12 open official-application findings and 4 regression records scoped to the independent QA utility (`issues.csv`) |
| **Interactive QA Dashboard** | Streamlit web application reading live CSV telemetry, dynamic KPIs, real-time Pytest subprocess runner, and reference calculation verifier (`app.py`) |
| **Continuous Integration** | Multi-OS GitHub Actions workflow (Ubuntu + Windows, Python 3.11/3.12) executing single-pass JUnit/HTML reporting with strict failure exit codes (`.github/workflows/tests.yml`) |

> **Official OsdagBridge Source Verification:**
> CI checks out the official repository of **[osdag-admin/OsdagBridge](https://github.com/osdag-admin/OsdagBridge)** at **Commit `2cb7ddc8ab2d2e33bf86721cb8a219b82d02df74`** (`Refactor`).

> **Independent QA Reference Utility (`osdagbridge_core`):**
> This repository contains an independent **QA Reference Utility** (`osdagbridge_core/`) that provides validated bridge calculations for the Streamlit dashboard's verification engine and reference benchmarking against IRC:24 and IS 800:2007. It is **not** the official OsdagBridge calculation engine and is never presented as such.

> **Confirmed Upstream Blocker — `osdagbridge.core.models` (OB-BUG-008):**
> In the official repository at commit `2cb7ddc`, `src/osdagbridge/core/__init__.py` line 2 executes `from .models import *`, but `models.py` does not physically exist in `src/osdagbridge/core/`. Standard import `import osdagbridge.core` immediately raises `ModuleNotFoundError: No module named 'osdagbridge.core.models'`. This is catalogued as **OB-BUG-008** and asserted in `tests/integration/test_plate_girder_pipeline.py`.

---

## 🏗️ Project Architecture

```
                               +------------------------------------------+
                               |       Official OsdagBridge Source        |
                               |    (osdag-admin/OsdagBridge @ 2cb7ddc)   |
                               +------------------------------------------+
                                                     |
                        +----------------------------+----------------------------+
                        |                                                         |
                        v                                                         v
      +----------------------------------+                   +----------------------------------+
      |         Manual Testing           |                   |       Automated Pytest Suite     |
      | - Form navigation & UI inputs    |                   | - Unit tests (models, validator) |
      | - Desktop bootstrap verification |                   | - Integration (package imports)  |
      | - IRC:24 benchmark verification  |                   | - UI State Simulation            |
      | - Visual validation banners      |                   | - Regression tests (OB-BUG-001+) |
      +----------------------------------+                   +----------------------------------+
                        |                                                         |
                        +----------------------------+----------------------------+
                        |
                        v
      +-------------------------------------------------------------------------+
      |                       Defect Tracking & Reports                         |
      | - test_cases.csv   (50 manual scenarios: 45 Pass, 2 Fail, 3 Blocked)    |
      | - test_results.csv (105 automated test executions: 96 Pass, 9 XFail)    |
      | - issues.csv       (16 documented defects with reproducible evidence)   |
      | - UI Wireframe mockups (reports/screenshots/*.svg)                      |
      +-------------------------------------------------------------------------+
                        |
                        v
      +-------------------------------------------------------------------------+
      |                    Interactive Streamlit QA Dashboard                   |
      |                                (app.py)                                 |
      | - Real-time KPIs computed from actual CSV telemetry                     |
      | - Live Pytest subprocess runner with stdout/stderr capture              |
      | - Independent IRC:24 / IS 800:2007 calculation verification engine      |
      | - Deployable to Streamlit Community Cloud                               |
      +-------------------------------------------------------------------------+
```

---

## 🗂️ Repository Structure

```
OsdagBridge--Software-Testing/
├── .github/
│   └── workflows/
│       └── tests.yml                  # Single pinned multi-OS CI workflow
│
├── .gitignore                         # Excludes caches, temporary reports, local envs
├── pytest.ini                         # Pytest configuration with strict markers
├── requirements.txt                   # Deployment dependencies
├── app.py                             # Streamlit QA Dashboard
├── run_tests.py                       # Automated Pytest runner & report exporter
├── README.md
│
├── test_cases.csv                     # 50 documented test cases across 8 categories
├── test_results.csv                   # 105 automated test execution records (JUnit export)
├── issues.csv                         # 16 documented defect records with reproduction evidence
│
├── scripts/
│   └── export_junit_csv.py            # Converts JUnit XML → test_results.csv with --strict
│
├── documentation/                     # Formal QA documentation deliverables
│   ├── installation_guide.md
│   ├── test_strategy.md
│   ├── test_plan.md
│   ├── test_execution_report.md
│   ├── bug_report_guide.md
│   ├── bug_report_template.md
│   ├── internship_summary_report.md
│   ├── test_environment.md
│   ├── known_limitations.md
│   ├── test_data_description.md
│   └── release_checklist.md
│
├── tests/
│   ├── conftest.py                    # Session fixtures & CI environment verification
│   ├── test_repository_layout.py      # Repository integrity & deliverable checks
│   ├── test_design.py                 # Structural solver verification
│   ├── test_environment.py           # Python runtime & file existence verification
│   ├── test_inputs.py                # Input validation & edge cases
│   ├── test_project.py               # Project JSON serialization & deserialization
│   ├── test_reports.py               # Markdown & HTML design report verification
│   ├── functional/                    # End-to-end workflows & code standards
│   │   ├── test_e2e_workflow.py       # Full input -> sizing -> solver -> report pipeline
│   │   └── test_irc_standards.py      # IRC:6 vehicle loads, impact factor, deflection
│   ├── integration/                   # Official OsdagBridge integration
│   │   ├── test_official_application.py   # CLI entry point, units, IRC stubs, desktop
│   │   └── test_plate_girder_pipeline.py  # Plate girder pipeline & upstream blockers
│   ├── regression/                    # Regression guards for verified bugs
│   │   └── test_regression.py         # OB-BUG-004 through OB-BUG-007 guards
│   ├── ui_simulation/                 # UI state machine simulations
│   │   └── test_ui_state_simulation.py
│   └── unit/                          # Unit validation & models
│       ├── test_models.py             # QA bridge data structures
│       ├── test_validation.py         # Geometric boundary limits
│       ├── test_unit_conversions.py   # Unit conversion engine tests
│       ├── test_export_junit_csv.py   # JUnit XML-to-CSV exporter tests
│       └── test_upstream_scenarios.py # Scenarios 43-48 (null inputs, load scaling, reload)
│
├── test_data/
│   ├── valid_inputs/                  # Valid 16m/24m plate girder JSON payloads
│   ├── invalid_inputs/                # Negative fixtures (negative span, boundary violations)
│   ├── sample_projects/               # Complete project payloads
│   └── reference_design_irc.json      # IRC:24 reference benchmark tolerances
│
├── osdagbridge_core/                  # Independent QA Reference Utility (NOT official OsdagBridge)
│   ├── models.py
│   ├── validator.py
│   ├── solver.py
│   └── report_generator.py
│
└── reports/
    ├── logs/                          # Test execution logs
    ├── screenshots/                   # Visual wireframes and UI mockups (SVG)
    └── test_results/                  # Generated JUnit XML & HTML reports
```

---

## 🚀 Quickstart Setup Instructions

### 1. Prerequisites
- **Python 3.11+** (`python --version`)
- **Git** (`git --version`)

### 2. Set Up the QA Repository
```bash
git clone https://github.com/singhrajawatamit7-star/OsdagBridge--Software-Testing.git
cd OsdagBridge--Software-Testing
pip install -r requirements.txt
```

### 3. Set Up the Official OsdagBridge Application (For Integration Tests)
Clone the official OsdagBridge repository side-by-side or into a custom location:
```bash
# From the parent directory of OsdagBridge--Software-Testing:
git clone https://github.com/osdag-admin/OsdagBridge.git
cd OsdagBridge
pip install -e .
cd ../OsdagBridge--Software-Testing
```

*(Optional) If cloned to a non-standard location, set `OSDAGBRIDGE_ROOT`:*
```powershell
# Windows PowerShell
$env:OSDAGBRIDGE_ROOT = "C:\path\to\OsdagBridge"

# Linux / macOS Bash
export OSDAGBRIDGE_ROOT="/path/to/OsdagBridge"
```

---

## 🧪 Executing the Test Suite

```bash
# Run the complete test suite with automated report export
python run_tests.py

# Or run pytest directly
python -m pytest tests -v

# Run with HTML coverage report
python -m pytest tests --cov=osdagbridge_core --html=reports/test_results/test_report.html --self-contained-html
```

### Test Suite Execution Summary (Verified Local Run)
- **Execution Date:** 2026-11-21
- **Python Version:** Python 3.13.7 (MSC v.1944 64-bit on Windows 11)
- **Official OsdagBridge Commit:** `2cb7ddc8ab2d2e33bf86721cb8a219b82d02df74`
- **Total Tests Collected:** 105
- **Passed:** 96
- **XFailed:** 9 (strictly enforced upstream defects, exit code 0)
- **Failed / Errors:** 0

---

## 📋 Documented Test Cases (50 Scenarios)

The test matrix in `test_cases.csv` and `reports/test_results.csv` tracks 50 scenarios across all functional domains, distinguishing passing features from upstream defects:

| Category | Cases | Focus | Execution Summary | Pass Rate |
|:---|:---:|:---|:---:|:---:|
| Installation & Launch | 5 | Python compatibility, pip install, core import, CLI, desktop runnable | 3 Pass, 1 Fail (OB-005), 1 Blocked (OB-003) | 60.0% |
| Project Management | 5 | DTO instantiation, modification, JSON serialization, corrupted file handling | 5 Pass | 100.0% |
| Input Validation | 10 | Valid spans, empty fields, negatives, boundaries [5m–60m], type errors | 10 Pass | 100.0% |
| Design Execution | 8 | Preliminary sizing, analyser, designer, dead/live loads, moment, shear | 5 Pass, 1 Fail (OB-021), 2 Blocked (OB-022, OB-023) | 62.5% |
| Results & Visualization | 7 | Deflection (L/800), extreme spans, steel grade scaling, 3D CAD, summary cards | 7 Pass | 100.0% |
| Report Generation | 5 | Markdown, HTML, compliance table, CSV export, Unicode path writing | 5 Pass | 100.0% |
| Error Handling | 5 | Missing girder, single-girder error, slenderness warning, corrupted input | 5 Pass | 100.0% |
| Regression Testing | 5 | Alpha injection, zero web thickness, Unicode export, impact factor floor | 5 Pass | 100.0% |
| **Total** | **50** | **Comprehensive QA verification matrix (`test_cases.csv`)** | **45 Pass, 2 Fail, 3 Blocked** | **90.0%** |

*(Calculation: $45 / 50 = 90.0\%$ pass rate; 2 failed and 3 blocked scenarios correspond to open upstream defects in the official application).*

---

## 🐞 Defect Register (16 Documented Defects)

Tracked in `issues.csv` — 12 open official-application findings and 4 regression records scoped to the independent QA utility:

| Bug ID | Title | Scope | Severity | Status | Verification & Evidence |
|:---|:---|:---:|:---:|:---:|:---|
| **OB-BUG-001** | `python -m osdagbridge.desktop` fails with `No module named ...__main__` | Official App | Critical | Open | `tests/integration/test_official_application.py::test_official_desktop_missing_main_module_execution` |
| **OB-BUG-002** | Desktop bootstrap `main.py` is an unlinked console stub lacking Qt GUI | Official App | High | Open | `tests/integration/test_official_application.py::test_official_desktop_launch_message_stub` |
| **OB-BUG-003** | Preliminary sizing routine returns raw DTO string `{"depth_m": dto.name}` | Official App | High | Open | `tests/integration/test_plate_girder_pipeline.py::test_preliminary_sizing_upstream_defect_reproduction_ob_bug_003` |
| **OB-BUG-004** | Zero web thickness produces unhandled `ZeroDivisionError` in slenderness | QA Core | High | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_004_zero_web_thickness_division_guard` |
| **OB-BUG-005** | Numeric inputs permit alphabetic characters during rapid typing | QA Core | Medium | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_005_alpha_characters_handling` |
| **OB-BUG-006** | PDF report export fails silently when destination path contains Unicode | QA Core | Low | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_006_unicode_path_in_reports` |
| **OB-BUG-007** | Impact factor for spans > 45m falls below IRC:6 statutory floor of 0.10 | QA Core | Medium | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_007_impact_factor_clamping_for_large_spans` |
| **OB-BUG-008** | Missing `models.py` in `osdagbridge.core` causes `ModuleNotFoundError` on import | Official App | Critical | Open | `tests/integration/test_plate_girder_pipeline.py::test_official_core_import_blocked_by_missing_models` |
| **OB-BUG-009** | CLI `analyze_cmd` is a console print stub without structural evaluation | Official App | High | Open | `tests/integration/test_official_application.py::test_official_cli_analyze_produces_engineering_results` |
| **OB-BUG-010** | Desktop `start()` has no `QApplication` or `QMainWindow` initialization | Official App | High | Open | `tests/integration/test_official_application.py::test_official_desktop_gui_window_instantiation` |
| **OB-BUG-011** | `to_si` helper is a dummy function returning input without metric conversion | Official App | Medium | Open | `tests/integration/test_official_application.py::test_official_units_conversion_metric` |
| **OB-BUG-012** | `get_vehicle_loads()` in `irc6_2017.py` returns empty list instead of IRC:6 vehicles | Official App | Medium | Open | `tests/integration/test_official_application.py::test_official_code_irc6_vehicle_loads_populated` |
| **OB-BUG-013** | `export_step` writes plain text string instead of ISO-10303-21 STEP structure | Official App | High | Open | `tests/integration/test_plate_girder_pipeline.py::test_plate_girder_cad_export_iso_step_format` |
| **OB-BUG-014** | Official validation accepts negative span | Official App | High | Open | `tests/integration/test_official_application.py::test_repro_ob_bug_014_official_validation_accepts_negative_span` |
| **OB-BUG-015** | Plate-girder designer returns placeholder output | Official App | Critical | Open | `tests/integration/test_plate_girder_pipeline.py` |
| **OB-BUG-016** | Plate-girder analyser returns placeholder output | Official App | Critical | Open | `tests/integration/test_plate_girder_pipeline.py` |

---

## Evidence and scope limitations

- The 50-row manual scenario matrix is separate from automated Pytest results.
- SVGs in `reports/screenshots/` are wireframes/mockups, not screenshots from the official desktop application.
- UI simulation tests do not prove that the official Qt desktop GUI works.
- `osdagbridge_core` is an independent QA reference utility, not the official OsdagBridge calculation engine.
- Open official-application defects remain upstream blockers.

## 📊 Interactive QA Dashboard

Run the dashboard locally:
```bash
streamlit run app.py
```

### Dashboard Features:
1. **QA Executive Dashboard** — Real-time KPIs calculated from actual CSV telemetry.
2. **Test Case Repository** — Searchable and filterable matrix of all 50 documented scenarios.
3. **Defect Tracker** — Defect register with severity, status, steps to reproduce, and interactive defect persistence form.
4. **Automated Test Runner** — Executes `pytest` subprocess live from the browser and captures terminal output.
5. **Interactive Bridge Verification** — Powered by `osdagbridge_core`, verifying IRC:24 and IS 800:2007 limits.
6. **Documentation Center** — Integrated Markdown reader for all formal deliverables.

---

## 🌐 Deployment to Streamlit Community Cloud

1. Fork or push this repository to GitHub.
2. Log into [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** → select:
   - **Repository:** `singhrajawatamit7-star/OsdagBridge--Software-Testing`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!**

---

## ⚙️ Continuous Integration

`.github/workflows/tests.yml` executes on every push and pull request across a multi-OS matrix:
- **Operating Systems:** `ubuntu-latest`, `windows-latest`
- **Python Runtimes:** `3.11`, `3.12`
- **Steps:** Checkouts, dependency installation, official source validation, JUnit XML and HTML report generation, and artifact archiving.
- **Fail-Safe:** CI strictly fails if tests produce unexpected errors or if the official application checkout is missing.

---

## 📜 License & Acknowledgments
- **Software Under Test:** [OsdagBridge](https://github.com/osdag-admin/OsdagBridge) — Osdag initiative, IIT Bombay.
- **Standards:** Indian Roads Congress (IRC:6, IRC:24) and Bureau of Indian Standards (IS 800:2007).
- **QA Framework:** Open-source educational and portfolio submission under the MIT License.
