"""
Integration Tests: Official OsdagBridge Plate Girder Pipeline.
Evaluates official plate girder routines against structural engineering requirements,
and reports incomplete or placeholder functionality as explicitly blocked / xfailed (strict=True).
"""
import importlib.util
from pathlib import Path
import pytest


def _load_module_from_path(module_name: str, file_path: Path):
    """Loads a specific Python file directly, isolating it from missing parent package modules."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_official_core_import_blocked_by_missing_models(official_source, monkeypatch):
    """
    INT-PG-01 (OB-BUG-008): Verifies that importing official 'osdagbridge.core' fails.
    Upstream Defect: src/osdagbridge/core/__init__.py contains 'from .models import *',
    but models.py does not exist in the official repository checkout.
    Reported as an explicitly documented blocker, NOT silently skipped.
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        import osdagbridge.core  # noqa: F401
    assert "osdagbridge.core.models" in str(exc_info.value)


@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_official_plate_girder_pipeline_blocked_by_missing_models(official_source, monkeypatch):
    """
    INT-PG-02 (OB-BUG-008): Verifies that standard import of plate_girder fails due to
    parent package import failure.
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        from osdagbridge.core.bridge_types.plate_girder import dto  # noqa: F401
    assert "osdagbridge.core.models" in str(exc_info.value)


@pytest.mark.smoke
@pytest.mark.integration
def test_official_plate_girder_files_exist_on_disk(official_source):
    """
    INT-PG-03: Verifies that plate_girder modules exist physically in the source tree.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    assert (pg_dir / "dto.py").is_file()
    assert (pg_dir / "initial_sizing.py").is_file()
    assert (pg_dir / "designer.py").is_file()
    assert (pg_dir / "analyser.py").is_file()
    assert (pg_dir / "report_generator.py").is_file()
    assert (pg_dir / "cad_generator.py").is_file()


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream bug OB-BUG-003: preliminary_sizing returns DTO name string instead of calculated numeric depth in meters",
)
def test_preliminary_sizing_engineering_validity(official_source):
    """
    INT-PG-04 (OB-BUG-003): Engineering assertion on preliminary girder sizing.
    A valid engineering calculation for a bridge girder depth MUST return a positive
    numerical value in meters (typically Span/12 to Span/15), NOT a raw project name string.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto", pg_dir / "dto.py")
    sizing_mod = _load_module_from_path("official_pg_sizing", pg_dir / "initial_sizing.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    result = sizing_mod.preliminary_sizing(dto)

    assert "depth_m" in result, "Result dictionary must contain 'depth_m' key."
    depth = result["depth_m"]

    # Structural engineering assertion: depth must be a positive number (float or int)
    assert isinstance(depth, (int, float)), (
        f"Engineering assertion failed: girder depth must be a numerical value with unit [m], "
        f"got {type(depth).__name__}: {depth!r}"
    )
    assert depth > 0, f"Girder depth must be strictly positive, got {depth}"


@pytest.mark.regression
@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_preliminary_sizing_upstream_defect_reproduction_ob_bug_003(official_source):
    """
    INT-PG-05: Reproduces and verifies OB-BUG-003 with reproducible execution evidence.
    Confirms that the official preliminary_sizing routine returns the literal string
    dto.name instead of computing a structural girder depth.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_repro", pg_dir / "dto.py")
    sizing_mod = _load_module_from_path("official_pg_sizing_repro", pg_dir / "initial_sizing.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    result = sizing_mod.preliminary_sizing(dto)

    # Verifies the defect manifestation logged in issues.csv (OB-BUG-003)
    assert result.get("depth_m") == "24m_Highway_Bridge"
    assert isinstance(result.get("depth_m"), str)


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream blocker OB-BUG-002: Official designer returns placeholder stub {'design': 'ok'} lacking structural limit state calculations",
)
def test_plate_girder_designer_engineering_checks(official_source):
    """
    INT-PG-06: Verifies that the plate girder designer produces actionable structural calculations.
    Must evaluate limit states including moment capacity, shear capacity, and code compliance ratio.
    Reports functionality as blocked due to upstream placeholder stub implementation.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_des", pg_dir / "dto.py")
    des_mod = _load_module_from_path("official_pg_designer", pg_dir / "designer.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    result = des_mod.design(dto)

    # Must verify real engineering outputs, not mere presence of a placeholder dict key
    required_metrics = ["moment_capacity_kNm", "shear_capacity_kN", "code_compliance"]
    missing = [m for m in required_metrics if m not in result]
    assert not missing, (
        f"Structural Engineering Failure: Official designer returns placeholder stub without "
        f"IRC:24 structural verification checks. Missing outputs: {missing}; got: {result}"
    )


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream blocker OB-BUG-002: Official analyser returns placeholder stub {'result': 'ok'} lacking grillage analysis outputs",
)
def test_plate_girder_analyser_engineering_outputs(official_source):
    """
    INT-PG-07: Verifies that the plate girder analyser computes bending moments and shear force distributions.
    Reports functionality as blocked due to upstream placeholder stub implementation.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_ana", pg_dir / "dto.py")
    ana_mod = _load_module_from_path("official_pg_analyser", pg_dir / "analyser.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    result = ana_mod.analyse(dto)

    # Must verify real analysis outputs
    required_outputs = ["bending_moments", "shear_forces", "deflection_field"]
    missing = [f for f in required_outputs if f not in result]
    assert not missing, (
        f"Structural Engineering Failure: Official analyser returns placeholder stub without "
        f"grillage analysis outputs. Missing outputs: {missing}; got: {result}"
    )


@pytest.mark.smoke
@pytest.mark.integration
def test_plate_girder_cad_export_smoke(official_source, tmp_path):
    """
    INT-PG-08: Smoke test verifying official CAD step exporter generates an export file on disk.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_cad", pg_dir / "dto.py")
    cad_mod = _load_module_from_path("official_pg_cad", pg_dir / "cad_generator.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    export_path = tmp_path / "bridge_plate_girder.step"
    cad_mod.export_step(dto, str(export_path))

    assert export_path.is_file()
    assert export_path.stat().st_size > 0


@pytest.mark.defect_reproduction
@pytest.mark.integration
def test_repro_ob_bug_013_official_cad_export_is_placeholder_string(official_source, tmp_path):
    """
    Reproduces OB-BUG-013: Official export_step writes raw string 'STEP placeholder'
    instead of valid CAD geometry conforming to ISO 10303 STEP exchange structure.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_cad_repro", pg_dir / "dto.py")
    cad_mod = _load_module_from_path("official_pg_cad_repro", pg_dir / "cad_generator.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    export_path = tmp_path / "bridge_plate_girder_repro.step"
    cad_mod.export_step(dto, str(export_path))

    content = export_path.read_text(encoding="utf-8")
    assert content == "STEP placeholder"


@pytest.mark.functional
@pytest.mark.engineering
@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason="Upstream defect OB-BUG-013: Official CAD export generates plain text 'STEP placeholder' instead of valid ISO-10303-21 STEP structure",
)
def test_plate_girder_cad_export_iso_step_format(official_source, tmp_path):
    """
    Validates that exported CAD file adheres to ISO-10303-21 exchange file format standard.
    Must contain ISO header tokens (ISO-10303-21, HEADER, DATA).
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    dto_mod = _load_module_from_path("official_pg_dto_cad_val", pg_dir / "dto.py")
    cad_mod = _load_module_from_path("official_pg_cad_val", pg_dir / "cad_generator.py")

    dto = dto_mod.PlateGirderDTO(name="24m_Highway_Bridge")
    export_path = tmp_path / "bridge_plate_girder_val.step"
    cad_mod.export_step(dto, str(export_path))

    content = export_path.read_text(encoding="utf-8")
    assert "ISO-10303-21;" in content, "Exported file must contain ISO-10303-21 STEP header."
    assert "HEADER;" in content
    assert "DATA;" in content
