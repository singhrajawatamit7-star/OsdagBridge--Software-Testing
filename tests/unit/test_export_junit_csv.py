"""
Unit Tests: Pytest JUnit XML to CSV Exporter.
Verifies scripts/export_junit_csv.py under valid XML, missing XML, malformed XML,
and mixed status (PASS, FAIL, ERROR, SKIPPED) inputs.
"""
import csv
from pathlib import Path
import pytest
from scripts.export_junit_csv import convert_junit_to_csv


@pytest.fixture
def sample_junit_xml(tmp_path):
    """Generates a valid synthetic JUnit XML file containing all outcome states."""
    xml_content = """<?xml version="1.0" encoding="utf-8"?>
<testsuites>
    <testsuite name="pytest" errors="1" failures="1" skipped="1" tests="4" time="1.234">
        <testcase classname="tests.test_inputs" name="test_valid_input" time="0.012" />
        <testcase classname="tests.test_inputs" name="test_failed_case" time="0.045">
            <failure message="AssertionError: span must be positive">Traceback details here</failure>
        </testcase>
        <testcase classname="tests.test_inputs" name="test_error_case" time="0.005">
            <error message="RuntimeError: solver failure">Error details here</error>
        </testcase>
        <testcase classname="tests.test_inputs" name="test_skipped_case" time="0.000">
            <skipped message="XFAIL upstream defect">Skipped details here</skipped>
        </testcase>
    </testsuite>
</testsuites>
"""
    xml_file = tmp_path / "junit_sample.xml"
    xml_file.write_text(xml_content, encoding="utf-8")
    return xml_file


@pytest.mark.unit
def test_export_valid_junit_xml_to_csv(sample_junit_xml, tmp_path):
    """Verify standard JUnit XML converts correctly to CSV with all expected columns and rows."""
    csv_file = tmp_path / "exported_results.csv"
    convert_junit_to_csv(sample_junit_xml, csv_file)

    assert csv_file.is_file()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 4
    expected_cols = {
        "Execution_ID", "Test_ID", "Test_Name", "Category", "Module",
        "Status", "Execution_Time_sec", "Expected_Result", "Actual_Result",
        "Remarks", "Execution_Date", "Execution_Date_UTC"
    }
    assert expected_cols.issubset(set(reader.fieldnames))

    statuses = [r["Status"] for r in rows]
    assert "PASS" in statuses
    assert "FAIL" in statuses
    assert "ERROR" in statuses
    assert "SKIPPED" in statuses


@pytest.mark.unit
def test_export_missing_xml_returns_zero(tmp_path):
    """Verify exporter handles missing XML file gracefully without raising unhandled exceptions."""
    missing_xml = tmp_path / "non_existent.xml"
    csv_file = tmp_path / "out.csv"
    ret = convert_junit_to_csv(missing_xml, csv_file)
    assert ret == 0
    assert not csv_file.exists()


@pytest.mark.unit
def test_export_empty_testsuite_xml(tmp_path):
    """Verify exporter handles an empty test suite XML without error."""
    empty_xml = tmp_path / "empty_suite.xml"
    empty_xml.write_text("""<?xml version="1.0" encoding="utf-8"?><testsuites></testsuites>""", encoding="utf-8")
    csv_file = tmp_path / "empty_out.csv"
    convert_junit_to_csv(empty_xml, csv_file)

    assert csv_file.is_file()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 0
