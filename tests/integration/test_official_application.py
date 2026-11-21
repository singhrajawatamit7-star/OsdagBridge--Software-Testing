"""
Functional and Integration Tests for Official OsdagBridge Application.
Executes real functionality of available official modules and systematically
verifies application behavior, CLI commands, utility functions, code registries,
and documented entry points.
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


@pytest.mark.smoke
@pytest.mark.integration
def test_official_repository_and_source_structure(official_root, official_source):
    """Verifies official repository root and Python source tree structure."""
    assert official_root.is_dir()
    assert (official_source / "osdagbridge").is_dir()
    assert (official_source / "osdagbridge" / "cli").is_dir()
    assert (official_source / "osdagbridge" / "core").is_dir()
    assert (official_source / "osdagbridge" / "desktop").is_dir()


@pytest.mark.functional
@pytest.mark.integration
def test_official_cli_analyze_command_execution(official_source):
    """Executes the official CLI analyze command function and verifies output."""
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
@pytest.mark.integration
def test_official_units_conversion_canonical_si(official_source):
    """Executes official units conversion helper function."""
    units_mod = _load_module_from_path(
        "official_units",
        official_source / "osdagbridge" / "core" / "utils" / "units.py",
    )

    assert units_mod.to_si(24.0, "m") == 24.0
    assert units_mod.to_si(500.0, "kN") == 500.0
    assert units_mod.to_si(0.0, "mm") == 0.0


@pytest.mark.functional
@pytest.mark.integration
def test_official_input_validation_stub_permits_negative_inputs(official_source):
    """
    Documents that the official validate_project utility is currently an unverified
    stub returning True even for invalid geometry payloads (negative span).
    """
    val_mod = _load_module_from_path(
        "official_val_stub",
        official_source / "osdagbridge" / "core" / "utils" / "validation.py",
    )

    # Documents upstream limitation: official stub accepts negative span without error
    result = val_mod.validate_project({"span": -50.0})
    assert result is True


@pytest.mark.functional
@pytest.mark.integration
def test_official_code_irc6_vehicle_loads(official_source):
    """Verifies that official IRC:6 code rules module executes and provides vehicle loads."""
    irc6 = _load_module_from_path(
        "official_irc6",
        official_source / "osdagbridge" / "core" / "utils" / "codes" / "irc6_2017.py",
    )
    assert hasattr(irc6, "get_vehicle_loads")
    loads = irc6.get_vehicle_loads()
    assert isinstance(loads, list)


@pytest.mark.functional
@pytest.mark.integration
def test_official_code_registry_blocked_by_missing_models(official_source, monkeypatch):
    """
    Verifies that the official code registry module fails to import because its internal
    dynamic import of irc6_2017 triggers osdagbridge.core.__init__.py's missing models.py (OB-BUG-008).
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        _load_module_from_path(
            "official_registry",
            official_source / "osdagbridge" / "core" / "utils" / "codes" / "registry.py",
        )
    assert "osdagbridge" in str(exc_info.value)


@pytest.mark.functional
@pytest.mark.integration
def test_official_custom_exceptions_hierarchy(official_source):
    """Verifies official domain exceptions inherit correctly from Exception."""
    exc_mod = _load_module_from_path(
        "official_exceptions",
        official_source / "osdagbridge" / "core" / "exceptions.py",
    )

    assert issubclass(exc_mod.OsdagError, Exception)
    with pytest.raises(exc_mod.OsdagError):
        raise exc_mod.OsdagError("Test structural exception")


@pytest.mark.functional
@pytest.mark.integration
def test_official_desktop_main_start_stub(official_source):
    """
    Verifies official desktop entry point executes its console stub (OB-BUG-002)
    and does not instantiate a Qt application window.
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


@pytest.mark.regression
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
