"""
Functional, Smoke, and Defect-Reproduction Tests for Official OsdagBridge Application.
Evaluates official modules against structural engineering requirements, isolating
upstream defects and stubs with explicit markers and documentation.
"""
import importlib.util
from io import StringIO
from pathlib import Path
import subprocess
import sys
import pytest


def _load_module_from_path(module_name: str, file_path: Path):
    """Loads a specific Python file directly, isolating it from missing parent package modules."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Repository Structure & Smoke Tests
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.integration
def test_official_repository_and_source_structure(official_root, official_source):
    """Verifies official repository root and Python source tree structure."""
    assert official_root.is_dir()
    assert (official_source / "osdagbridge").is_dir()
    assert (official_source / "osdagbridge" / "cli").is_dir()
    assert (official_source / "osdagbridge" / "core").is_dir()
    assert (official_source / "osdagbridge" / "desktop").is_dir()


# ---------------------------------------------------------------------------
# CLI Tests (Smoke Stub vs. Functional Engineering Execution)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.integration
def test_official_cli_analyze_smoke_stub(official_source):
    """Verifies the official CLI analyze command entry point prints expected stub invocation text."""
    cli_mod = _load_module_from_path(
        "official_cli_cmds",
        official_source / "osdagbridge" / "cli" / "commands.py",
    )

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    try:
        cli_mod.analyze_cmd("sample_bridge_project.json")
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    assert "analyze" in output
    assert "sample_bridge_project.json" in output


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream limitation OB-BUG-009: CLI analyze_cmd is a placeholder stub that prints string instead of performing analysis",
)
def test_official_cli_analyze_produces_engineering_results(official_source):
    """
    Evaluates whether official CLI analyze command performs genuine bridge structural analysis.
    Fails because official analyze_cmd is a stub printing 'analyze <path>' without returning data.
    """
    cli_mod = _load_module_from_path(
        "official_cli_cmds_func",
        official_source / "osdagbridge" / "cli" / "commands.py",
    )
    result = cli_mod.analyze_cmd("sample_bridge_project.json")
    assert isinstance(result, dict), "CLI analyze command must return an analysis results dictionary."
    assert "bending_moment_kNm" in result
    assert "shear_force_kN" in result


# ---------------------------------------------------------------------------
# Unit Conversion Tests (Canonical SI vs. Metric Conversion)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.integration
def test_official_units_conversion_canonical_si(official_source):
    """Verifies official units conversion helper function returns unchanged values for canonical SI."""
    units_mod = _load_module_from_path(
        "official_units",
        official_source / "osdagbridge" / "core" / "utils" / "units.py",
    )

    assert units_mod.to_si(24.0, "m") == 24.0
    assert units_mod.to_si(500.0, "kN") == 500.0
    assert units_mod.to_si(0.0, "mm") == 0.0


@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_repro_ob_bug_011_official_units_fails_mm_to_m(official_source):
    """
    Reproduces OB-BUG-011: official to_si(val, unit) is a dummy function returning val unchanged,
    failing to convert millimeters to meters (1000 mm -> 1000.0 instead of 1.0 m).
    """
    units_mod = _load_module_from_path(
        "official_units_repro",
        official_source / "osdagbridge" / "core" / "utils" / "units.py",
    )
    # Defect assertion: 1000 mm is returned as 1000.0, not 1.0
    assert units_mod.to_si(1000.0, "mm") == 1000.0


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream defect OB-BUG-011: official to_si returns input value without metric unit conversion",
)
def test_official_units_conversion_metric(official_source):
    """
    Functional check: to_si must convert 1000 mm to 1.0 m and 50 kN to 50000 N.
    """
    units_mod = _load_module_from_path(
        "official_units_func",
        official_source / "osdagbridge" / "core" / "utils" / "units.py",
    )
    converted_length = units_mod.to_si(1000.0, "mm")
    assert converted_length == 1.0, f"Expected 1.0 m for 1000 mm, got {converted_length}"


# ---------------------------------------------------------------------------
# Input Validation Tests (Defect Reproduction vs. Rejection Requirement)
# ---------------------------------------------------------------------------
@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_repro_ob_bug_014_official_validation_accepts_negative_span(official_source):
    """
    Reproduces OB-BUG-014 (Upstream Defect): official validate_project utility is an unverified stub
    returning True even for invalid geometry payloads (negative span).
    """
    val_mod = _load_module_from_path(
        "official_val_stub",
        official_source / "osdagbridge" / "core" / "utils" / "validation.py",
    )
    # Documents upstream defect: official stub accepts negative span without error
    result = val_mod.validate_project({"span": -50.0})
    assert result is True


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream defect OB-BUG-014: official validate_project returns True for negative inputs without validation",
)
def test_official_input_validation_rejects_negative_span(official_source):
    """
    Functional assertion: input validation MUST reject negative span dimensions.
    """
    val_mod = _load_module_from_path(
        "official_val_func",
        official_source / "osdagbridge" / "core" / "utils" / "validation.py",
    )
    result = val_mod.validate_project({"span": -50.0})
    assert result is False, "Validation must return False or raise ValidationError for negative span."


# ---------------------------------------------------------------------------
# IRC:6 Vehicle Loads Tests
# ---------------------------------------------------------------------------
@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_repro_ob_bug_012_official_irc6_vehicle_loads_empty(official_source):
    """
    Reproduces OB-BUG-012: official get_vehicle_loads() returns an empty list []
    instead of IRC:6-2017 standard vehicle configurations.
    """
    irc6 = _load_module_from_path(
        "official_irc6_repro",
        official_source / "osdagbridge" / "core" / "utils" / "codes" / "irc6_2017.py",
    )
    assert hasattr(irc6, "get_vehicle_loads")
    assert irc6.get_vehicle_loads() == []


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream defect OB-BUG-012: official get_vehicle_loads returns empty list instead of IRC:6 vehicles",
)
def test_official_code_irc6_vehicle_loads_populated(official_source):
    """
    Functional assertion: get_vehicle_loads() must provide IRC:6 vehicle loading definitions.
    """
    irc6 = _load_module_from_path(
        "official_irc6_func",
        official_source / "osdagbridge" / "core" / "utils" / "codes" / "irc6_2017.py",
    )
    loads = irc6.get_vehicle_loads()
    assert len(loads) > 0, "IRC:6 code module must define at least Class 70R and Class A loading."


# ---------------------------------------------------------------------------
# Code Registry & Upstream Blocker OB-BUG-008
# ---------------------------------------------------------------------------
@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_official_code_registry_blocked_by_missing_models(official_source, monkeypatch):
    """
    Verifies that official code registry fails to import because its internal dynamic import
    of irc6_2017 triggers osdagbridge.core.__init__.py's missing models.py (OB-BUG-008).
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        _load_module_from_path(
            "official_registry",
            official_source / "osdagbridge" / "core" / "utils" / "codes" / "registry.py",
        )
    assert "osdagbridge" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------
@pytest.mark.functional
@pytest.mark.integration
def test_official_custom_exceptions_hierarchy(official_source):
    """Verifies official domain exceptions inherit correctly from Exception and carry messages."""
    exc_mod = _load_module_from_path(
        "official_exceptions",
        official_source / "osdagbridge" / "core" / "exceptions.py",
    )

    assert issubclass(exc_mod.OsdagError, Exception)
    err = exc_mod.OsdagError("Structural boundary violation: span cannot be negative")
    assert str(err) == "Structural boundary violation: span cannot be negative"
    with pytest.raises(exc_mod.OsdagError):
        raise err


# ---------------------------------------------------------------------------
# Desktop Bootstrap & GUI Tests
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.integration
def test_official_desktop_launch_message_stub(official_source):
    """
    Verifies official desktop entry point executes its console stub and prints launch message.
    """
    desk_mod = _load_module_from_path(
        "official_desktop_main",
        official_source / "osdagbridge" / "desktop" / "main.py",
    )

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    try:
        desk_mod.start()
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    assert "Starting desktop UI" in output


@pytest.mark.gui
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream limitation OB-BUG-010: desktop start() is a console print stub without QApplication / QMainWindow initialization",
)
def test_official_desktop_gui_window_instantiation(official_source):
    """
    Verifies whether the desktop module instantiates an actual graphical Qt window.
    Fails because official desktop/main.py only contains a print statement.
    """
    desk_mod = _load_module_from_path(
        "official_desktop_gui",
        official_source / "osdagbridge" / "desktop" / "main.py",
    )
    assert hasattr(desk_mod, "MainWindow") or hasattr(desk_mod, "app"), (
        "Desktop module must define a Qt application or MainWindow class."
    )


@pytest.mark.regression
@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_official_desktop_missing_main_module_execution(official_source):
    """
    Verifies OB-BUG-001: python -m osdagbridge.desktop fails with
    'No module named osdagbridge.desktop.__main__'.
    Reproducible execution evidence for bug OB-BUG-001.
    """
    res = subprocess.run(
        [sys.executable, "-m", "osdagbridge.desktop"],
        cwd=str(official_source),
        capture_output=True,
        text=True,
    )
    assert res.returncode != 0
    assert "No module named osdagbridge.desktop.__main__" in res.stderr
