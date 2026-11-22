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
    <testsuite name="pytest" errors="1" failures="1" skipped="2" tests="5" time="1.234">
        <testcase classname="tests.test_inputs" name="test_valid_input" time="0.012" />
        <testcase classname="tests.test_inputs" name="test_failed_case" time="0.045"><failure message="AssertionError: span must be positive">Traceback</failure></testcase>
        <testcase classname="tests.test_inputs" name="test_error_case" time="0.005"><error message="RuntimeError: solver failure">Error</error></testcase>
        <testcase classname="tests.test_inputs" name="test_expected_failure" time="0.000"><skipped type="pytest.xfail" message="Upstream defect OB-BUG-009">Expected failure</skipped></testcase>
        <testcase classname="tests.test_inputs" name="test_genuine_skip" time="0.000"><skipped type="pytest.skip" message="Requires optional GUI environment">Skipped</skipped></testcase>
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

    assert len(rows) == 5
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
    assert statuses == ["PASS", "FAIL", "ERROR", "XFAIL", "SKIPPED"]


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


@pytest.mark.unit
def test_export_xfail_and_skip_are_distinguished(sample_junit_xml, tmp_path):
    """An expected failure must not be reported as a genuine skip."""
    csv_file = tmp_path / "outcomes.csv"
    convert_junit_to_csv(sample_junit_xml, csv_file)
    with csv_file.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    by_name = {row["Test_Name"]: row["Status"] for row in rows}
    assert by_name["test_expected_failure"] == "XFAIL"
    assert by_name["test_genuine_skip"] == "SKIPPED"


@pytest.mark.unit
def test_export_malformed_xml_returns_nonzero_in_strict_mode(tmp_path):
    """Strict CI export must fail when the JUnit XML is malformed."""
    malformed_xml = tmp_path / "malformed.xml"
    malformed_xml.write_text("<testsuites><testcase>", encoding="utf-8")
    assert convert_junit_to_csv(malformed_xml, tmp_path / "out.csv", strict=True) == 1
