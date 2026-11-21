"""
Run the QA test suite using the real Pytest runner with automated report generation.
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    # Ensure report directories exist
    (ROOT / "reports" / "test_results").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports" / "logs").mkdir(parents=True, exist_ok=True)

    junit_xml = ROOT / "reports" / "test_results" / "junit.xml"
    html_report = ROOT / "reports" / "test_results" / "test_report.html"

    # Forward any CLI arguments or use default test suite
    extra_args = sys.argv[1:] if len(sys.argv) > 1 else [str(ROOT / "tests")]

    command = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--tb=short",
        f"--junitxml={junit_xml}",
        f"--html={html_report}",
        "--self-contained-html",
    ] + extra_args

    result = subprocess.run(command, cwd=ROOT)

    # Automatically export JUnit XML to test_results.csv if XML was produced
    if junit_xml.is_file():
        export_script = ROOT / "scripts" / "export_junit_csv.py"
        csv_dest = ROOT / "test_results.csv"
        subprocess.run(
            [sys.executable, str(export_script), str(junit_xml), str(csv_dest)],
            cwd=ROOT,
            capture_output=True,
        )

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
