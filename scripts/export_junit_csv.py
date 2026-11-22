"""Convert a real Pytest JUnit XML report into CSV."""
import csv
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def classify_skipped_case(skipped_element):
    """Distinguish pytest xfails from genuine skipped tests in JUnit XML."""
    skipped_type = skipped_element.attrib.get("type", "").strip().lower()
    message = skipped_element.attrib.get("message", "Test skipped")
    if skipped_type in {"pytest.xfail", "xfail"} or "xfail" in skipped_type:
        return "XFAIL"
    if re.match(r"^\s*xfail(?:\b|:)", message, flags=re.IGNORECASE):
        return "XFAIL"
    return "SKIPPED"


def convert_junit_to_csv(xml_path, csv_path, strict=False):
    xml_path = Path(xml_path)
    csv_path = Path(csv_path)
    if not xml_path.exists():
        print(f"Warning: JUnit XML report not found at {xml_path}. Skipping CSV export.")
        if strict:
            return 1
        return 0
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as e:
        print(f"Error parsing JUnit XML file {xml_path}: {e}")
        if strict:
            return 1
        return 0

    rows = []
    run_timestamp = datetime.now(timezone.utc).strftime("EXEC-%Y%m%d-%H%M%S")
    run_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    iso_timestamp = datetime.now(timezone.utc).isoformat()

    for case in root.iter("testcase"):
        classname = case.attrib.get("classname", "")
        name = case.attrib.get("name", "")
        duration = float(case.attrib.get("time", 0))
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")
        if failure is not None:
            status = "FAIL"
            remarks = failure.attrib.get("message", "Test failed")
        elif error is not None:
            status = "ERROR"
            remarks = error.attrib.get("message", "Test error")
        elif skipped is not None:
            status = classify_skipped_case(skipped)
            remarks = skipped.attrib.get("message", "Test skipped")
        else:
            status = "PASS"
            remarks = "Pytest completed successfully"
        rows.append({
            "Execution_ID": run_timestamp,
            "Test_ID": f"{classname}::{name}",
            "Test_Name": name,
            "Category": classname,
            "Module": classname,
            "Status": status,
            "Execution_Time_sec": round(duration, 4),
            "Expected_Result": "Test passes assertion checks without error",
            "Actual_Result": remarks,
            "Remarks": remarks,
            "Execution_Date": run_date_str,
            "Execution_Date_UTC": iso_timestamp,
        })
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "Execution_ID",
        "Test_ID",
        "Test_Name",
        "Category",
        "Module",
        "Status",
        "Execution_Time_sec",
        "Expected_Result",
        "Actual_Result",
        "Remarks",
        "Execution_Date",
        "Execution_Date_UTC",
    ]
    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} test records to {csv_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: python scripts/export_junit_csv.py input.xml output.csv [--strict]"
        )
    strict_flag = "--strict" in sys.argv
    ret = convert_junit_to_csv(sys.argv[1], sys.argv[2], strict=strict_flag)
    sys.exit(ret)
