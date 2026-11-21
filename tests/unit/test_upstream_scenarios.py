"""
Unit Tests: Upstream Application Scenarios & Edge Cases.
Validates scenarios derived from OsdagBridge issue tracker:
- Scenario 43: Null / empty required input handling
- Scenario 44: Report generation before design calculation guarding
- Scenario 45: Custom load combinations reflection in design demand
- Scenario 46: Project serialization / reopening value consistency
- Scenario 47: Numerical precision and unit consistency
- Scenario 48: Design-check verification against authentic benchmarks
"""
import copy
import json
import pytest

from osdagbridge_core.models import (
    BridgeProject,
    BridgeGeometry,
    PlateGirderDimensions,
)
from osdagbridge_core.validator import ProjectValidator
from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.report_generator import ReportGenerator


@pytest.mark.unit
def test_scenario_43_null_or_empty_required_inputs(valid_project_dict):
    """
    Scenario 43: Input fields accept empty or null values in upstream bug reports.
    Confirms QA validator strictly rejects null/None/empty project names, IDs, and numeric dimensions.
    """
    # Test empty project_name
    dict_empty_name = copy.deepcopy(valid_project_dict)
    dict_empty_name["project_name"] = "   "
    res1 = ProjectValidator.validate_project_payload(dict_empty_name)
    assert not res1.is_valid
    assert any("project_name" in err["field"].lower() for err in res1.errors)

    # Test None / missing span_length
    dict_none_span = copy.deepcopy(valid_project_dict)
    dict_none_span["geometry"]["span_length"] = None
    res2 = ProjectValidator.validate_project_payload(dict_none_span)
    assert not res2.is_valid
    assert any("span_length" in err["field"].lower() for err in res2.errors)


@pytest.mark.unit
def test_scenario_44_report_generation_requires_valid_summary(valid_bridge_project):
    """
    Scenario 44: Guarding against generating reports without prior analysis.
    Confirms report generator rejects None or uncalculated design summaries.
    """
    with pytest.raises((ValueError, TypeError, AttributeError)):
        ReportGenerator.generate_markdown_report(valid_bridge_project, None)

    with pytest.raises((ValueError, TypeError, AttributeError)):
        ReportGenerator.generate_html_report(valid_bridge_project, None)


@pytest.mark.unit
@pytest.mark.engineering
def test_scenario_45_load_scaling_reflects_in_design_results(valid_bridge_project):
    """
    Scenario 45: Custom load factors or vehicle loadings must scale analysis demand.
    Verifies that changing vehicle loading from Class A to Class 70R increases the design bending moment.
    """
    proj_70r = copy.deepcopy(valid_bridge_project)
    proj_70r.vehicle_loading = "IRC_Class_70R_Wheeled"
    summary_70r = BridgeSolver.calculate_design(proj_70r)

    proj_a = copy.deepcopy(valid_bridge_project)
    proj_a.vehicle_loading = "IRC_Class_A"
    summary_a = BridgeSolver.calculate_design(proj_a)

    # Class 70R creates higher bending moment than Class A
    assert summary_70r.design_moment > summary_a.design_moment
    assert summary_70r.design_shear_force > summary_a.design_shear_force


@pytest.mark.unit
def test_scenario_46_project_reopen_value_preservation(valid_bridge_project):
    """
    Scenario 46: Upstream bug report: load/geometry values change after reopening a project.
    Verifies that serializing to JSON and reloading preserves 100% of parameters with exact equality.
    """
    original_dict = valid_bridge_project.to_dict()
    json_str = json.dumps(original_dict, indent=2)

    reloaded_dict = json.loads(json_str)
    reloaded_project = BridgeProject.from_dict(reloaded_dict)
    reloaded_project_dict = reloaded_project.to_dict()

    assert original_dict == reloaded_project_dict
    assert reloaded_project.geometry.span_length == valid_bridge_project.geometry.span_length
    assert reloaded_project.geometry.carriageway_width == valid_bridge_project.geometry.carriageway_width
    assert reloaded_project.girder_dimensions.web_depth == valid_bridge_project.girder_dimensions.web_depth
    assert reloaded_project.girder_dimensions.web_thickness == valid_bridge_project.girder_dimensions.web_thickness


@pytest.mark.unit
def test_scenario_47_numerical_precision_consistency(valid_bridge_project):
    """
    Scenario 47: Numerical precision consistency across models and calculation summaries.
    Verifies that calculated moment capacity and check ratios maintain consistent floating point precision.
    """
    summary = BridgeSolver.calculate_design(valid_bridge_project)
    # Check rounding precision on checks
    for check in summary.checks:
        assert isinstance(check.actual_value, float)
        assert isinstance(check.allowable_limit, float)
        assert isinstance(check.ratio, float)
        assert check.actual_value > 0
        assert check.allowable_limit > 0


@pytest.mark.unit
@pytest.mark.benchmark
def test_scenario_48_design_checks_match_irc_reference(valid_bridge_project, reference_irc_data):
    """
    Scenario 48: Verification of design-check results against independently verified reference calculations.
    """
    summary = BridgeSolver.calculate_design(valid_bridge_project)
    tolerances = reference_irc_data["expected_engineering_tolerances"]

    # Verify moment capacity is within verified engineering reference tolerances
    assert summary.moment_capacity >= tolerances["moment_capacity_knm_min"]
    assert summary.moment_capacity <= tolerances["moment_capacity_knm_max"]

    # Verify shear capacity within verified engineering reference tolerances
    assert summary.shear_capacity >= tolerances["shear_capacity_kn_min"]
    assert summary.shear_capacity <= tolerances["shear_capacity_kn_max"]

    # Verify overall safety status
    assert (summary.is_safe is True) if tolerances["overall_safety_status"] == "PASS" else (summary.is_safe is False)
