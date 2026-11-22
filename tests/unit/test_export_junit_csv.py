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


@pytest.mark.unit
def test_exporter_classifies_real_pytest_generated_junit_xml(tmp_path):
    """Exercise the exporter against JUnit XML produced by a real pytest process."""
    import os
    import subprocess
    import sys

    probe = tmp_path / "test_junit_probe.py"
    probe.write_text(
        """
import pytest

def test_pass():
    assert 1 == 1

def test_fail():
    assert 1 == 2

@pytest.fixture
def broken_fixture():
    # A setup-phase exception is serialized by pytest as a JUnit <error>.
    raise RuntimeError("fixture setup error")

def test_error(broken_fixture):
    assert True

@pytest.mark.xfail(strict=True, reason="expected probe xfail")
def test_xfail():
    assert 1 == 2

@pytest.mark.skip(reason="expected probe skip")
def test_skip():
    assert False
""",
        encoding="utf-8",
    )
    config = tmp_path / "pytest.ini"
    config.write_text("[pytest]\n", encoding="utf-8")
    junit = tmp_path / "pytest-generated.xml"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-c",
        str(config),
        f"--junitxml={junit}",
        str(probe),
    ]
    completed = subprocess.run(
        command,
        cwd=str(tmp_path),
        env={**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    # The intentional assertion failure and runtime error make pytest return 1.
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert junit.is_file(), completed.stdout + completed.stderr

    output = tmp_path / "pytest-generated.csv"
    assert convert_junit_to_csv(junit, output, strict=True) == 0
    with output.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    actual = {row["Test_Name"]: row["Status"] for row in rows}
    assert actual == {
        "test_pass": "PASS",
        "test_fail": "FAIL",
        "test_error": "ERROR",
        "test_xfail": "XFAIL",
        "test_skip": "SKIPPED",
    }
