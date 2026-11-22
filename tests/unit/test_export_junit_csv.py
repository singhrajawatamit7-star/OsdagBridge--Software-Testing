"""Unit tests for Pytest JUnit XML to CSV outcome classification."""
import csv
import pytest
from scripts.export_junit_csv import convert_junit_to_csv


@pytest.mark.unit
def test_export_distinguishes_pass_fail_error_xfail_and_skip(tmp_path):
    xml = tmp_path / "junit.xml"
    xml.write_text("""<testsuites><testsuite>
      <testcase classname="sample" name="passed"/>
      <testcase classname="sample" name="failed"><failure message="assertion failed"/></testcase>
      <testcase classname="sample" name="errored"><error message="runtime error"/></testcase>
      <testcase classname="sample" name="expected_failure"><skipped type="pytest.xfail" message="known upstream defect"/></testcase>
      <testcase classname="sample" name="skipped"><skipped type="pytest.skip" message="not applicable"/></testcase>
    </testsuite></testsuites>""", encoding="utf-8")
    output = tmp_path / "results.csv"
    assert convert_junit_to_csv(xml, output, strict=True) == 0
    with output.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["Status"] for row in rows] == ["PASS", "FAIL", "ERROR", "XFAIL", "SKIPPED"]


@pytest.mark.unit
def test_missing_xml_strict_mode_fails(tmp_path):
    assert convert_junit_to_csv(tmp_path / "missing.xml", tmp_path / "out.csv", strict=True) == 1
    assert not (tmp_path / "out.csv").exists()


@pytest.mark.unit
def test_malformed_xml_strict_mode_fails(tmp_path):
    source = tmp_path / "broken.xml"
    source.write_text("<testsuites>", encoding="utf-8")
    assert convert_junit_to_csv(source, tmp_path / "out.csv", strict=True) == 1


@pytest.mark.unit
def test_empty_testsuite_creates_header_only_csv(tmp_path):
    source, output = tmp_path / "empty.xml", tmp_path / "empty.csv"
    source.write_text("<testsuites/>", encoding="utf-8")
    assert convert_junit_to_csv(source, output, strict=True) == 0
    with output.open(encoding="utf-8", newline="") as handle:
        assert list(csv.DictReader(handle)) == []
