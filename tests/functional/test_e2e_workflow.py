"""
Functional End-to-End Test: Complete Bridge Design Workflow.
Verifies the end-to-end pipeline: Input Specification -> Validation -> Structural Sizing
-> Analysis Demand Calculation -> Limit State Design Checks -> Report Generation & Export.
"""
from pathlib import Path
import pytest

from osdagbridge_core.models import (
    BridgeProject,
    BridgeGeometry,
    PlateGirderDimensions,
)
from osdagbridge_core.validator import ProjectValidator
from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.report_generator import ReportGenerator


@pytest.mark.functional
@pytest.mark.engineering
def test_complete_bridge_design_workflow_end_to_end(tmp_path):
    """
    E2E-01: Verifies the entire design cycle for a 24m IRC Highway Plate Girder Bridge:
    1. Define controlled input parameters conforming to IRC:6 and IRC:24 standards.
    2. Execute project validation and confirm zero validation errors.
    3. Run the structural analysis and limit state solver.
    4. Assert that all four mandatory safety checks (Moment, Shear, Deflection, Slenderness) pass.
    5. Generate engineering calculation reports in Markdown and HTML.
    6. Verify exported artifacts on disk for non-empty content and structural completeness.
    """
    # Step 1: Input Specification
    geometry = BridgeGeometry(
        span_length=24.0,
        carriageway_width=7.5,
        number_of_main_girders=3,
        girder_spacing=2.8,
        cross_girder_spacing=4.0,
        deck_slab_thickness=220.0,
        wearing_coat_thickness=75.0,
        footpath_width_left=1.0,
        footpath_width_right=1.0,
    )
    dimensions = PlateGirderDimensions(
        web_depth=1600.0,
        web_thickness=12.0,
        flange_width=450.0,
        flange_thickness=25.0,
        stiffener_spacing=1500.0,
        stiffener_thickness=12.0,
    )
    project = BridgeProject(
        project_id="OB-E2E-CONTROLLED-001",
        project_name="NH-48 Standard 24m Highway Bridge",
        location="Sector 14, Gurugram, Haryana",
        engineer_name="Senior Bridge QA Lead",
        bridge_type="Plate_Girder_Bridge",
        steel_grade="E250",
        concrete_grade="M35",
        vehicle_loading="IRC_Class_70R_Wheeled",
        geometry=geometry,
        girder_dimensions=dimensions,
        custom_notes="Controlled end-to-end verification project",
    )

    # Step 2: Input Validation
    val_result = ProjectValidator.validate(project)
    assert val_result.is_valid, f"Validation failed unexpectedly: {val_result.errors}"
    assert len(val_result.errors) == 0

    # Step 3: Analysis Demand & Capacity Solution
    summary = BridgeSolver.calculate_design(project)
    assert summary is not None
    assert summary.design_moment > 0
    assert summary.design_shear_force > 0
    assert summary.moment_capacity > summary.design_moment
    assert summary.shear_capacity > summary.design_shear_force

    # Step 4: Verification of Limit State Checks
    assert len(summary.checks) >= 4
    for check in summary.checks:
        assert check.status == "PASS", f"Check {check.check_name} failed: actual={check.actual_value}, limit={check.allowable_limit}"
        assert check.actual_value <= check.allowable_limit

    # Step 5: Report Generation
    md_content = ReportGenerator.generate_markdown_report(project, summary)
    html_content = ReportGenerator.generate_html_report(project, summary)

    assert "OB-E2E-CONTROLLED-001" in md_content
    assert "NH-48 Standard 24m Highway Bridge" in md_content
    assert "SAFE / ACCEPTABLE" in html_content
    assert "IRC:24" in html_content

    # Step 6: Export & Persistence Verification
    md_file = tmp_path / "design_report.md"
    html_file = tmp_path / "design_report.html"

    md_file.write_text(md_content, encoding="utf-8")
    html_file.write_text(html_content, encoding="utf-8")

    assert md_file.is_file() and md_file.stat().st_size > 1000
    assert html_file.is_file() and html_file.stat().st_size > 1500
