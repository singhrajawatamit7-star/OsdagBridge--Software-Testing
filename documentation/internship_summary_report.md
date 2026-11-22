# FINAL QA INTERNSHIP SUBMISSION REPORT
## Subject: Software Testing & Quality Assurance on OsdagBridge
**Project Title:** OsdagBridge Automated & Manual QA Suite  
**Student / Intern:** Software Testing & QA Intern  
**Organization:** Structural Engineering Open-Source QA Initiative  
**Date of Submission:** November 2026  
**Repository:** [singhrajawatamit7-star/OsdagBridge--Software-Testing](https://github.com/singhrajawatamit7-star/OsdagBridge--Software-Testing)  
**Application Under Test:** [osdag-admin/OsdagBridge](https://github.com/osdag-admin/OsdagBridge) (v0.1.0)  

---

### Executive Summary
During this internship, I designed and developed an end-to-end **Quality Assurance Testing Suite**, with historical execution records retained for traceability for **OsdagBridge**, an open-source structural software for Plate Girder Road Bridges compliant with Indian Standard codes (**IS 800:2007**) and Indian Roads Congress specifications (**IRC:6**, **IRC:24-2010**).

The testing program bridges the gap between software quality engineering and civil structural requirements, providing:
1. Direct integration tests discovering and exercising the official `osdagbridge` package.
2. A comprehensive repository of **50 documented test cases** categorized across 8 operational areas.
3. Automated test suites built with **Pytest** covering unit models, integration pipelines, GUI bootstrap flows, and regression assertions.
4. A defect register (`issues.csv`) documenting reported upstream defects and QA reference-utility findings; each finding must be validated against its linked reproduction test and evidence.
5. An interactive **Streamlit QA Analytics Dashboard** providing live telemetry, test filtering, and calculation verifications.
6. A multi-OS **GitHub Actions Continuous Integration** pipeline.

---

### Quantitative Testing Metrics

| Metric | Target | Achieved Result |
| :--- | :--- | :--- |
| Documented Test Cases | 50 | **50 Test Cases (`test_cases.csv`)** |
| Functional Test Categories | 8 | **8 Categories (Installation, Project, Validation, Design, Results, Reports, Errors, Regression)** |
| Automated Pytest Suite | > 60 | 105 historical result rows; not a fresh execution for this submission revision |
| Documented Matrix Pass Rate | > 85% | Historical labels only: 45 PASS, 2 FAIL, 3 BLOCKED; fresh dated execution evidence remains pending |
| Defects Identified & Documented | 5+ | **16 Findings Tracked (`OB-BUG-001` to `OB-BUG-016`): 12 open official-app defects and 4 QA-reference utility findings** |
| Average Test Execution Duration | < 0.5s | Historical runtime only; regenerate timing from the current environment before reporting. |
| Code Compliance Standard | IRC:24 / IS 800 | Standards are referenced by test specifications; this QA project is not a structural design certification or independent code-compliance approval |

---

### Selected Findings (verify scope in `issues.csv`)

1. **OB-BUG-001 [Critical]:** Documented launch command `python -m osdagbridge.desktop` fails with `No module named osdagbridge.desktop.__main__` because the entry-point module is omitted from the desktop package.
2. **OB-BUG-002 [High]:** Desktop bootstrap function `osdagbridge.desktop.main.start()` prints a placeholder message to console rather than launching a PySide6 GUI window.
3. **OB-BUG-003 [High]:** Preliminary sizing routine `preliminary_sizing(dto)` returns raw DTO string rather than calculating preliminary girder depth ($L/12$ to $L/15$).
4. **OB-BUG-004 [High, QA reference utility]:** Zero web thickness in girder section produces unhandled `ZeroDivisionError` in slenderness calculation; guarded with input validation guard `ERR_NEGATIVE_OR_ZERO_INPUT`.
5. **OB-BUG-005 [Medium, QA reference utility]:** Fast numeric entry accepts alphabetic characters before form submission; guarded via inline character sanitization.
6. **OB-BUG-006 [Low, QA reference utility]:** Silent export failure when destination path contains Unicode characters; guarded with UTF-8 encoding handlers.
7. **OB-BUG-007 [Medium, QA reference utility]:** Impact factor for spans $> 45\text{m}$ fell below statutory floor of 0.10; guarded via clamping formula per IRC:6 Clause 208.
8. **OB-BUG-008 [Critical]:** Official `src/osdagbridge/core/__init__.py` imports non-existent `models.py` (`from .models import *`), raising unhandled `ModuleNotFoundError` on package import.

---

### Civil Engineering Safety Recommendations

1. **Mandatory Hand-Calculation Cross-Checks:** Structural design calculations must never be approved based solely on software completion. All moment capacities, shear strengths, and live-load deflections must be validated against IRC:24 worked benchmarks.
2. **Strict Web Slenderness Enforcements:** When web slenderness $d/t_w$ exceeds 200, the system must enforce intermediate transverse/longitudinal stiffener requirements per IS 800:2007 Cl 8.4.2.
3. **Deflection Limits under IRC Class 70R:** Live load deflection must remain strictly below $\text{Span} / 800$ to prevent bridge deck cracking and long-term fatigue degradation.

---

*Report submitted in partial fulfillment of Software Testing & QA Internship requirements.*


### Verification status and evidence still required

This report describes the QA assets and historical records in the repository. It does not claim that this revision has completed a fresh full test run or that all manual scenarios have been executed against the official desktop application. Before final submission:

- Run the full test command from `documentation/test_execution_report.md` and retain the JUnit XML and generated CSV.
- Confirm every GitHub Actions matrix job is successful on the final commit.
- Execute accessible manual scenarios against the genuine official desktop application and attach dated screenshots; mark inaccessible scenarios BLOCKED.
- Keep upstream defects open until the official application fix is verified independently.


### Updated repository verification (2026-11-22)

The GitHub Actions workflow on main commit `d6759d22995acea5cf152c88a36c3ef9af42767f` completed successfully: Ubuntu/Python 3.11, Ubuntu/Python 3.12, Windows/Python 3.11 and Windows/Python 3.12 all passed. See [workflow run 45010909943](https://github.com/singhrajawat7-star/OsdagBridge--Software-Testing/actions/runs/45010909943). This confirms the QA repository's configured CI checks on that commit; it does not certify the official application's engineering behavior or replace a fresh local test run.

### Defect register interpretation

The register contains 16 findings. OB-BUG-001 through OB-BUG-003 and OB-BUG-008 through OB-BUG-016 describe 12 open issues in the official application. OB-BUG-004 through OB-BUG-007 concern the independent `osdagbridge_core` QA reference utility; their regression tests currently assert that the reported edge cases are handled. They must not be described as open defects in the official application.

### Manual test evidence boundary

The 50 scenario records are an inventory, not 50 verified manual executions. Historical labels (45 PASS, 2 FAIL, 3 BLOCKED) are retained for traceability only. Fresh operator, date, environment, observed result and screenshot/log evidence are required before reporting current manual results. Use `documentation/manual_execution_log.csv` to record those executions. Do not create or submit mock screenshots as application evidence.

### Submission decision

This is a conditionally verified QA portfolio. The repository CI matrix is green on the cited commit, but a fresh local full-suite run and genuine desktop/manual evidence remain outstanding. The 12 upstream application defects remain open. The project does not certify OsdagBridge as fit for structural engineering use.
