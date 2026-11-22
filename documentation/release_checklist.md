# QA Release & Submission Checklist

## Release decision
**Current status: CONDITIONALLY VERIFIED — official application blockers remain open.**
This repository is a QA portfolio and test harness; passing tests do not mean every upstream OsdagBridge feature works.

## Repository quality gates
- [x] Tests organized into unit, functional, integration, regression and UI-simulation groups.
- [x] Independent `osdagbridge_core` utility clearly separated from official application.
- [x] JUnit exporter distinguishes PASS, FAIL, ERROR, XFAIL and SKIPPED.
- [x] Exporter tests cover expected failures separately from genuine skips.
- [x] Defect IDs are unique through OB-BUG-016; root and reports issue CSVs are synchronized.
- [x] Dashboard displays XFAIL and SKIPPED separately.
- [x] CI pins official OsdagBridge at `2cb7ddc8ab2d2e33bf86721cb8a219b82d02df74`.
- [x] Duplicate workflow removed; `.github/workflows/tests.yml` is canonical.

## Required after this change
- [ ] Confirm all four OS/Python matrix jobs pass on the new commit.
- [ ] Inspect new JUnit XML, HTML and CSV artifacts.
- [ ] Launch Streamlit dashboard and verify the metrics.
- [ ] Reconcile execution report against the new CI artifact.

## Manual evidence still required
- [ ] Capture genuine screenshots from the official OsdagBridge desktop application.
- [ ] Link screenshots to test IDs, environment, application commit and observed result.
- [ ] Existing SVG files are wireframes/mockups, not actual screenshots.
- [ ] Mark untestable scenarios BLOCKED, not PASS.

## Open upstream defects
Official-application issues OB-BUG-001 through OB-BUG-003 and OB-BUG-008 through OB-BUG-016 remain open. OB-BUG-004 through OB-BUG-007 concern the independent QA reference utility.

## Sign-off
- QA portfolio: conditionally verified after a successful post-change CI run.
- Official application: upstream blockers remain.
- Manual evidence: genuine desktop screenshots still required.
- Do not label the upstream application itself release-ready.
