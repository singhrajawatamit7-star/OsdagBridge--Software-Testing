"""Convert Pytest JUnit XML into a normalized CSV execution report."""
import csv
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def _classify_case(case):
    """Return (status, remarks), preserving pytest's xfail/skip distinction."""
    failure = case.find("failure")
    error = case.find("error")
    skipped = case.find("skipped")
    if failure is not None:
        return "FAIL", failure.attrib.get("message", "Test failed")
    if error is not None:
        return "ERROR", error.attrib.get("message", "Test error")
    if skipped is not None:
        skip_type = skipped.attrib.get("type", "").lower()
        message = skipped.attrib.get("message", "Test skipped")
        if skip_type.endswith(".xfail") or skip_type == "xfail":
            return "XFAIL", message
        return "SKIPPED", message
    return "PASS", "Pytest completed successfully"


def convert_junit_to_csv(xml_path, csv_path, strict=False):
    xml_path, csv_path = Path(xml_path), Path(csv_path)
    if not xml_path.exists():
        print(f"Warning: JUnit XML report not found at {xml_path}.")
        return 1 if strict else 0
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:
        print(f"Error parsing JUnit XML file {xml_path}: {exc}")
        return 1 if strict else 0

    now = datetime.now(timezone.utc)
    execution_id = now.strftime("EXEC-%Y%m%d-%H%M%S")
    rows = []
    for case in root.iter("testcase"):
        classname = case.attrib.get("classname", "")
        name = case.attrib.get("name", "")
        try:
            duration = float(case.attrib.get("time", 0))
        except (TypeError, ValueError):
            duration = 0.0
        status, remarks = _classify_case(case)
        rows.append({
            "Execution_ID": execution_id,
            "Test_ID": f"{classname}::{name}",
            "Test_Name": name,
            "Category": classname,
            "Module": classname,
            "Status": status,
            "Execution_Time_sec": round(duration, 4),
            "Expected_Result": "Test outcome matches its declared expectation",
            "Actual_Result": remarks,
            "Remarks": remarks,
            "Execution_Date": now.strftime("%Y-%m-%d"),
            "Execution_Date_UTC": now.isoformat(),
        })

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "Execution_ID", "Test_ID", "Test_Name", "Category", "Module",
        "Status", "Execution_Time_sec", "Expected_Result", "Actual_Result",
        "Remarks", "Execution_Date", "Execution_Date_UTC",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} test records to {csv_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python scripts/export_junit_csv.py input.xml output.csv [--strict]")
    raise SystemExit(convert_junit_to_csv(
        sys.argv[1], sys.argv[2], strict="--strict" in sys.argv
    ))
