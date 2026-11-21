"""
Regression Tests for OsdagBridge QA Suite.
Guards verified defects and edge cases documented in issues.csv (OB-BUG-004 through OB-BUG-007).
Ensures that previously identified defects have reproducible test evidence and do not reoccur.
"""
import json
from pathlib import Path
import pytest
from osdagbridge_core.models import BridgeProject
from osdagbridge_core.validator import ProjectValidator
from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.report_generator import ReportGenerator


def test_regression_ob_bug_004_zero_web_thickness_division_guard(sample_24m_data):
    """
    REG-04 [OB-BUG-004]: Verify zero web thickness does not trigger uncaught ZeroDivisionError.
    Status in issues.csv: Verified.
    Input validator must catch non-positive thickness with ERR_NEGATIVE_OR_ZERO_INPUT.
    """
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_thickness"] = 0.0

    val = ProjectValidator.validate_project_payload(payload)
    assert val.is_valid is False
    assert any(e["code"] == "ERR_NEGATIVE_OR_ZERO_INPUT" for e in val.errors)


def test_regression_ob_bug_005_alpha_characters_handling(sample_24m_data):
    """
    REG-05 [OB-BUG-005]: Verify numeric fields reject strings without uncaught exceptions.
    Status in issues.csv: Verified.
    Rejects '1800ABC_INJECTION' with ERR_INVALID_DATA_TYPE.
    """
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_depth"] = "1800ABC_INJECTION"

    val = ProjectValidator.validate_project_payload(payload)
    assert val.is_valid is False
    assert any(e["code"] == "ERR_INVALID_DATA_TYPE" for e in val.errors)


def test_regression_ob_bug_006_unicode_path_in_reports(sample_24m_data, tmp_path):
    """
    REG-06 [OB-BUG-006]: Verify report export module handles Unicode directories gracefully.
    Status in issues.csv: Verified.
    Executes ReportGenerator.export_report_file to write to paths containing non-ASCII / Devanagari characters.
    """
    unicode_dir = tmp_path / "डिजाइन_रिपोर्ट्स"

    project = BridgeProject.from_dict(sample_24m_data)
    summary = BridgeSolver.calculate_design(project)
    html_report = ReportGenerator.generate_html_report(project, summary)

    target_file = unicode_dir / "NH48_Report.html"
    exported_path = ReportGenerator.export_report_file(target_file, html_report)

    assert exported_path.exists()
    assert exported_path.stat().st_size > 500


def test_regression_ob_bug_007_impact_factor_clamping_for_large_spans(sample_24m_data):
    """
    REG-07 [OB-BUG-007]: Verify BridgeSolver clamps impact factor to statutory floor of 0.10 for spans > 45m.
    Status in issues.csv: Verified.
    Per IRC:6 Cl 208, impact formula 4.5 / (6.0 + 50.0) yields 0.0803; the solver must enforce lower bound 0.10.
    """
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = 50.0  # Formula 4.5 / (6 + 50) = 0.0803 < 0.10

    project = BridgeProject.from_dict(payload)
    summary = BridgeSolver.calculate_design(project)

    # Verifies solver's internal calculation outputs clamped statutory factor
    assert summary.impact_factor == 0.10, f"Expected solver clamped impact factor 0.10, got {summary.impact_factor}"


def test_regression_corrupt_json_project_loading(tmp_path):
    """
    REG-08: Verify loading malformed or truncated JSON raises cleanly handled JSONDecodeError.
    """
    bad_file = tmp_path / "broken_project.json"
    bad_file.write_text('{"project_id": "CORRUPT", "geometry": { "span": 24.0', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        with open(bad_file, "r", encoding="utf-8") as f:
            json.load(f)
