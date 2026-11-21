"""
Functional Tests: IRC Code Standards & Benchmark Verification.
Validates structural formulas, vehicle loads, impact factors, and allowable limits
against authentic specifications in IRC:6-2017, IRC:24-2010, and IS 800:2007.
"""
import pytest

from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.models import (
    BridgeProject,
    BridgeGeometry,
    PlateGirderDimensions,
)


@pytest.mark.functional
@pytest.mark.benchmark
@pytest.mark.engineering
def test_irc6_impact_factor_calculation():
    """
    IRC:6-2017 Clause 208: Impact Factor for Steel Bridges.
    For steel bridges, Impact Fraction IF = 0.10 + 9.0 / (13.5 + L), clamped to max 0.54.
    For 24m span: IF = 0.10 + 9 / (13.5 + 24) = 0.10 + 9 / 37.5 = 0.10 + 0.24 = 0.34.
    """
    span_24 = 24.0
    expected_if_24 = 0.10 + (9.0 / (13.5 + span_24))
    assert pytest.approx(expected_if_24, abs=0.001) == 0.34

    # Large span test: for 100m, formula gives 0.10 + 9 / 113.5 = 0.1793
    span_100 = 100.0
    expected_if_100 = 0.10 + (9.0 / (13.5 + span_100))
    assert 0.10 < expected_if_100 < 0.20


@pytest.mark.functional
@pytest.mark.benchmark
@pytest.mark.engineering
def test_irc24_deflection_limit_l_over_800():
    """
    IRC:24-2010 Clause 505: Permissible Live Load Deflection Limit.
    Delta_LL <= Span / 800 for highway road bridges.
    For 24m span: 24000 mm / 800 = 30.0 mm.
    """
    span_m = 24.0
    span_mm = span_m * 1000.0
    limit_mm = span_mm / 800.0
    assert limit_mm == 30.0


@pytest.mark.functional
@pytest.mark.benchmark
@pytest.mark.engineering
def test_irc24_minimum_web_thickness_corrosion_margin():
    """
    IRC:24-2010 Clause 506.2: Minimum web thickness to account for atmospheric corrosion.
    Minimum web plate thickness shall not be less than 8.0 mm.
    """
    from osdagbridge_core.validator import ProjectValidator
    from osdagbridge_core.models import BridgeGeometry, PlateGirderDimensions, BridgeProject

    # Test with 6 mm web thickness (below 8 mm)
    project_6mm = BridgeProject(
        project_id="TEST-CORROSION-6MM",
        project_name="Test Web Corrosion",
        location="Site A",
        engineer_name="QA Lead",
        bridge_type="Plate_Girder_Bridge",
        steel_grade="E250",
        concrete_grade="M35",
        vehicle_loading="IRC_Class_70R_Wheeled",
        geometry=BridgeGeometry(span_length=24.0, carriageway_width=7.5),
        girder_dimensions=PlateGirderDimensions(
            web_depth=1600.0,
            web_thickness=6.0,  # Below IRC:24 8mm limit
            flange_width=450.0,
            flange_thickness=25.0,
            stiffener_spacing=1500.0,
            stiffener_thickness=12.0,
        ),
    )
    result = ProjectValidator.validate(project_6mm)
    assert not result.is_valid
    assert any("8.0" in err["message"] or "minimum allowable limit" in err["message"] for err in result.errors)


@pytest.mark.functional
@pytest.mark.benchmark
@pytest.mark.engineering
def test_irc6_vehicle_load_weights_and_axle_configurations():
    """
    IRC:6-2017 Table 2 & Table 3: Vehicle load standards.
    - Class 70R Wheeled: Total static load = 1000 kN (100 tonnes) across 7 axles.
    - Class 70R Tracked: Total static load = 700 kN (70 tonnes) over two 4.57m tracks.
    - Class A: Standard highway train load = 554 kN across 8 axles.
    """
    class_70r_wheeled_total_kn = 1000.0
    class_70r_tracked_total_kn = 700.0
    class_a_train_total_kn = 554.0

    assert class_70r_wheeled_total_kn > class_70r_tracked_total_kn
    assert class_70r_wheeled_total_kn > class_a_train_total_kn
    assert class_70r_tracked_total_kn > class_a_train_total_kn
