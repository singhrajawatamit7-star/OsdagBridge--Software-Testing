# 🌉 OsdagBridge – Automated & Manual QA Suite
### Software Testing, Input Validation, Structural Verification & Issue Reporting for Plate Girder Road Bridges

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Testing-Pytest%209.2-orange.svg)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](https://github.com/features/actions)
[![Standards](https://img.shields.io/badge/Standards-IRC%3A24%20%7C%20IRC%3A6%20%7C%20IS%20800-purple.svg)](https://www.irc.nic.in/)
[![Status](https://img.shields.io/badge/Status-Submission_Ready-success.svg)](#deployment-guide)

---

## 📌 Executive Summary

This repository is the complete **Software Testing & Quality Assurance Portfolio Project** for **[OsdagBridge](https://github.com/osdag-admin/OsdagBridge)**, the open-source structural-engineering software for bridge analysis developed under the Osdag initiative at IIT Bombay.

The project demonstrates end-to-end QA capabilities expected of a **Software Testing / QA Engineer**:

| Deliverable | Detail |
|---|---|
| **Official Application Integration** | Functional & smoke tests that execute CLI commands, SI unit conversions, code registry lookups, desktop stubs, and isolate upstream blockers (`tests/integration/`) |
| **50 Documented Test Cases** | Detailed scenarios covering Installation, Project Management, Validation, Design, Results, Reporting, Error Handling, and Regression (`test_cases.csv` & `reports/test_results.csv` — **45 Passed, 2 Failed, 3 Blocked, 90.0% Pass Rate**) |
| **77 Automated Pytest Tests** | Real Pytest suite across `tests/unit/`, `tests/integration/`, `tests/ui_simulation/`, `tests/regression/` (`test_results.csv` exported directly from `reports/test_results/junit.xml` — **74 Passed, 3 XFailed upstream blockers**) |
| **8 Documented Defects Tracked** | 4 Open upstream blockers in official application, and 4 Verified regression-guarded defects with reproducible test evidence (`issues.csv`) |
| **Interactive QA Dashboard** | Streamlit web app reading live CSV telemetry, dynamic KPIs, real-time Pytest subprocess runner, and calculation verifier |
| **Continuous Integration** | Multi-OS GitHub Actions workflow (Ubuntu + Windows, Python 3.11/3.12) executing single-pass JUnit/HTML reporting with strict failure exit codes |

> **Important — `osdagbridge_core`:** This repository contains an independent
> **QA Reference Utility** (`osdagbridge_core/`) that provides validated bridge
> calculations for the Streamlit dashboard's verification engine. It is **not**
> the official OsdagBridge calculation engine and is never presented as such.

> **Upstream Blocker Isolation — `osdagbridge.core.models` (OB-BUG-008):** The official
> `src/osdagbridge/core/__init__.py` executes `from .models import *` but
> `models.py` does not exist in the official repository. This raises
> `ModuleNotFoundError: No module named 'osdagbridge.core.models'` on any
> standard attempt to import `osdagbridge.core`. This upstream defect
> is catalogued in `issues.csv` as **OB-BUG-008**. The integration test suite
> (`tests/integration/test_plate_girder_pipeline.py`) explicitly asserts this
> failure condition with `pytest.raises(ModuleNotFoundError)` so the upstream blocker
> is honestly documented rather than masked by fake module shims or silent skips.

---

## 🏗️ Project Architecture

```
                              +------------------------------------------+
                              |       Official OsdagBridge Source        |
                              |       (osdag-admin/OsdagBridge)          |
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
                              +------------------------------------------+
                              |       Defect Tracking & Reports          |
                              | - test_cases.csv  (50 scenarios)         |
                              | - test_results.csv (77 executions)       |
                              | - issues.csv (8 documented defects)      |
                              | - SVG UI mockups & log artifacts         |
                              +------------------------------------------+
                                                    |
                                                    v
                              +------------------------------------------+
                              |     Interactive Streamlit Dashboard      |
                              |             (app.py)                     |
                              | - Real-time KPIs from actual CSV data    |
                              | - Live Pytest subprocess runner          |
                              | - Bridge Calculation Verification        |
                              | - Streamlit Community Cloud deployable   |
                              +------------------------------------------+
```

---

## 🗂️ Repository Structure

```
OsdagBridge-Software-Testing/
├── .github/
│   └── workflows/
│       └── qa.yml                     # Multi-OS CI (Ubuntu & Windows, Python 3.11/3.12)
│
├── .gitignore
├── pytest.ini                         # Pytest configuration with custom markers
├── requirements.txt                   # Deployment dependencies
├── app.py                             # Streamlit QA Dashboard
├── run_tests.py                       # Pytest subprocess runner
├── README.md
│
├── test_cases.csv                     # 50 documented test cases across 8 categories
├── test_results.csv                   # 77 execution records (JUnit XML export)
├── issues.csv                         # Defect tracker with 8 defects & evidence
│
├── scripts/
│   └── export_junit_csv.py            # Converts JUnit XML → test_results.csv
│
├── documentation/                     # Formal QA deliverables
│   ├── installation_guide.md
│   ├── test_strategy.md
│   ├── test_plan.md
│   ├── test_execution_report.md
│   ├── bug_report_guide.md
│   ├── internship_summary_report.md
│   ├── test_environment.md
│   ├── known_limitations.md
│   ├── test_data_description.md
│   └── release_checklist.md
│
├── tests/
│   ├── conftest.py                    # Shared fixtures, official source resolution
│   ├── test_repository_layout.py     # Deliverables integrity checks
│   ├── unit/
│   │   ├── test_validation.py        # Input validation boundary checks
│   │   └── test_models.py            # QA reference model unit tests
│   ├── integration/
│   │   ├── test_official_application.py   # Official package functional tests
│   │   └── test_plate_girder_pipeline.py  # Upstream blocker documentation
│   ├── ui_simulation/
│   │   └── test_ui_state_simulation.py    # UI state machine simulation tests
│   └── regression/
│       └── test_regression.py        # Regression guards for verified defects
│
├── test_data/
│   ├── valid_inputs/                  # Valid 16m/24m plate girder payloads
│   ├── invalid_inputs/                # Negative fixtures (negative span, type errors)
│   └── sample_projects/               # IRC:24 reference benchmark projects
│
├── osdagbridge_core/                  # Independent QA Reference Utility (NOT official OsdagBridge)
│   ├── models.py
│   ├── validator.py
│   ├── solver.py
│   └── report_generator.py
│
└── reports/
    ├── logs/
    ├── screenshots/                   # SVG UI mockup & wireframe artifacts (OB-001 through OB-012)
    └── test_results/                  # JUnit XML & HTML reports
```

---

## 🚀 Quickstart Setup Instructions

### 1. Prerequisites
- **Python 3.9+** (`python --version`)
- **Git** (`git --version`)

### 2. Clone Both Repositories Side-by-Side

```bash
mkdir OsdagQAWork && cd OsdagQAWork

# Official OsdagBridge application (required for integration tests)
git clone https://github.com/osdag-admin/OsdagBridge.git

# This QA repository
git clone https://github.com/rutujakharode6-max/OsdagBridge-Software-Testing.git
```

### 3. Install the Official Application

```bash
cd OsdagBridge
pip install -e .
cd ..
```

### 4. Install QA Dependencies

```bash
cd OsdagBridge-Software-Testing
pip install -r requirements.txt
```

### 5. Point tests at the Official Source (optional — auto-detected if cloned side-by-side)

```bash
# Powershell
$env:OSDAGBRIDGE_ROOT = "..\OsdagBridge"

# Bash
export OSDAGBRIDGE_ROOT="../OsdagBridge"
```

---

## 🧪 Executing the Test Suite

```bash
# Run all 77 automated tests
python -m pytest tests -v

# Run with HTML report
python -m pytest tests --html=reports/test_results/test_report.html --self-contained-html

# Individual suites
python -m pytest tests/integration -v     # Official application functional & blocker tests
python -m pytest tests/unit -v            # Validation & model unit tests
python -m pytest tests/ui_simulation -v   # UI state simulation tests
python -m pytest tests/regression -v      # Regression guards for verified bugs
```

**Regenerate `test_results.csv` from real execution:**
```bash
python -m pytest tests --junitxml=reports/test_results/junit.xml
python scripts/export_junit_csv.py reports/test_results/junit.xml test_results.csv
```

---

## 📊 Interactive QA Dashboard

```bash
streamlit run app.py
# Open http://localhost:8501
```

**Dashboard sections:**
1. **QA Executive Dashboard** — KPIs computed from real CSV data, pass-rate gauges
2. **Test Case Repository** — 50 scenarios with filterable category, status, and execution type
3. **Defect Tracker** — 8 defects with severity/priority filter, evidence images, live append form
4. **Automated Test Runner** — Triggers real `pytest` subprocess from the browser; shows live stdout
5. **Bridge Verification Engine** — Powered by `osdagbridge_core` (independent QA reference)
6. **Documentation Center** — Full-text viewer for all 10 QA deliverables

---

## 📋 Documented Test Cases (50 Scenarios)

The test matrix in `test_cases.csv` and `reports/test_results.csv` tracks 50 scenarios across all functional domains, honestly distinguishing passing features from upstream application defects:

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

---

## 🐞 Defect Register

Tracked defects in `issues.csv` — detailing upstream defects in `osdag-admin/OsdagBridge` alongside verified regression guards:

| Bug ID | Title | Severity | Priority | Status | Verification & Evidence |
|:---|:---|:---:|:---:|:---:|:---|
| **OB-BUG-001** | `python -m osdagbridge.desktop` fails — no `__main__.py` | Critical | P1 | Open | `tests/integration/test_official_application.py::test_official_desktop_missing_main_module_execution` |
| **OB-BUG-002** | Desktop `main.py` is a console stub — no PySide6 GUI | High | P1 | Open | `tests/integration/test_official_application.py::test_official_desktop_main_start` |
| **OB-BUG-003** | Preliminary sizing returns raw DTO string `{"depth_m": dto.name}` instead of numeric depth | High | P2 | Open | `tests/integration/test_plate_girder_pipeline.py::test_preliminary_sizing_upstream_defect_reproduction_ob_bug_003` |
| **OB-BUG-004** | Zero web thickness causes unhandled `ZeroDivisionError` in slenderness check | High | P1 | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_004_zero_web_thickness_division_guard` |
| **OB-BUG-005** | Numeric input fields accept alphabetic characters during rapid typing | Medium | P2 | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_005_alpha_characters_handling` |
| **OB-BUG-006** | PDF/HTML export fails silently for Unicode destination paths | Low | P3 | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_006_unicode_path_in_reports` |
| **OB-BUG-007** | Impact factor drops below IRC:6 statutory floor of 0.10 for spans > 45 m | Medium | P2 | Verified | `tests/regression/test_regression.py::test_regression_ob_bug_007_impact_factor_clamping_for_large_spans` |
| **OB-BUG-008** | Missing `models.py` in `osdagbridge.core` causes `ModuleNotFoundError` on package import | Critical | P1 | Open | `tests/integration/test_plate_girder_pipeline.py::test_official_core_import_blocked_by_missing_models` |

---

## ⚙️ Continuous Integration

`.github/workflows/qa.yml` runs on every push and pull request:

- Checks out the QA suite **and** the official `osdag-admin/OsdagBridge` repository
- Matrix: **Ubuntu + Windows** × **Python 3.11 / 3.12**
- Installs official application (`pip install -e .`) and QA dependencies
- Runs `python -m pytest tests --junitxml=...` — **exits non-zero on failure** (no `|| true` suppression)
- Uploads JUnit XML and HTML reports as build artefacts

---

## 🌐 Deployment Guide (Streamlit Community Cloud)

1. Push repository to GitHub (all files committed)
2. Log into [share.streamlit.io](https://share.streamlit.io/) with GitHub
3. Click **New app** → select `rutujakharode6-max/OsdagBridge-Software-Testing`, branch `main`, file `app.py`
4. Click **Deploy**

---

## 🎓 Internship Deliverables Checklist

- [x] **Official OsdagBridge integration** — `tests/integration/` functional & blocker tests with honest fail/skip handling
- [x] **50 documented test cases** — `test_cases.csv` with preconditions, steps, and expected results (90.0% application pass rate, isolating 5 failed/blocked scenarios)
- [x] **77 automated Pytest tests** — comprehensive suite (74 passed, 3 xfailed); `test_results.csv` regenerated from real JUnit XML
- [x] **UI state simulation** — desktop & form workflow state machine in `tests/ui_simulation/`
- [x] **8 reproducible defects** — `issues.csv` with severity, priority, evidence, reproduction steps, and regression guards
- [x] **77 real execution records** — `test_results.csv` exported by `scripts/export_junit_csv.py`
- [x] **CI pipeline** — multi-OS GitHub Actions, fails on test failure (no `|| true` suppression)
- [x] **Streamlit QA dashboard** — dynamic KPIs from live data, live Pytest runner, calculation verifier
- [x] **10 documentation deliverables** — `documentation/` (plan, strategy, environment, limitations, checklist…)
- [x] **Honest README** — all metrics traceable to actual artefacts in this repository

---

## 📜 License & Acknowledgments
- **Project Under Test:** [OsdagBridge](https://github.com/osdag-admin/OsdagBridge) — Osdag initiative, IIT Bombay
- **Standards:** Indian Roads Congress (IRC:6, IRC:24) and Bureau of Indian Standards (IS 800:2007)
- **QA Framework:** Open-source educational and portfolio submission under the MIT License
