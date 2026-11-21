"""
Unit Tests: Comprehensive Unit Conversion Engine.
Tests conversions between supported civil and structural engineering units,
decimal values, negative values, unsupported units, and numerical rounding precision.
"""
import pytest


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Canonical QA reference unit conversion function."""
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()

    if from_unit == to_unit:
        return float(value)

    # Length conversions (base unit: meter)
    length_to_m = {
        "m": 1.0,
        "meter": 1.0,
        "meters": 1.0,
        "mm": 0.001,
        "millimeter": 0.001,
        "cm": 0.01,
        "centimeter": 0.01,
        "km": 1000.0,
    }
    # Force conversions (base unit: Newton)
    force_to_n = {
        "n": 1.0,
        "newton": 1.0,
        "kn": 1000.0,
        "kilonewton": 1000.0,
        "mn": 1000000.0,
    }
    # Moment conversions (base unit: Newton-meter)
    moment_to_nm = {
        "nm": 1.0,
        "knm": 1000.0,
        "nmm": 0.001,
    }

    if from_unit in length_to_m and to_unit in length_to_m:
        val_m = value * length_to_m[from_unit]
        return val_m / length_to_m[to_unit]
    elif from_unit in force_to_n and to_unit in force_to_n:
        val_n = value * force_to_n[from_unit]
        return val_n / force_to_n[to_unit]
    elif from_unit in moment_to_nm and to_unit in moment_to_nm:
        val_nm = value * moment_to_nm[from_unit]
        return val_nm / moment_to_nm[to_unit]
    else:
        raise ValueError(f"Incompatible or unsupported unit conversion from '{from_unit}' to '{to_unit}'")


@pytest.mark.unit
def test_length_conversions_metric():
    """Verify standard length conversions between meters, millimeters, and centimeters."""
    assert convert_units(24.0, "m", "mm") == 24000.0
    assert convert_units(1600.0, "mm", "m") == 1.6
    assert convert_units(45.0, "cm", "m") == 0.45
    assert convert_units(750.0, "mm", "cm") == 75.0


@pytest.mark.unit
def test_force_conversions_kn_and_n():
    """Verify force conversions between kN and N."""
    assert convert_units(500.0, "kN", "N") == 500000.0
    assert convert_units(125000.0, "N", "kN") == 125.0
    assert convert_units(1.0, "MN", "kN") == 1000.0


@pytest.mark.unit
def test_moment_conversions_knm_and_nmm():
    """Verify bending moment conversions between kNm, Nm, and Nmm."""
    # 1 kNm = 1,000 Nm = 1,000,000 Nmm (10^6 Nmm)
    assert convert_units(4250.0, "kNm", "Nmm") == 4250000000.0
    assert convert_units(1000000.0, "Nmm", "kNm") == 1.0
    assert convert_units(250.0, "kNm", "Nm") == 250000.0


@pytest.mark.unit
def test_decimal_values_precision():
    """Verify accurate precision retention on floating point decimal inputs."""
    assert pytest.approx(convert_units(0.125, "m", "mm"), abs=1e-6) == 125.0
    assert pytest.approx(convert_units(0.0075, "m", "mm"), abs=1e-6) == 7.5
    assert pytest.approx(convert_units(12.3456, "kN", "N"), abs=1e-3) == 12345.6


@pytest.mark.unit
def test_negative_values_conversion():
    """Verify negative values convert correctly where physical coordinates or camber offsets require sign."""
    assert convert_units(-2.5, "m", "mm") == -2500.0
    assert convert_units(-50.0, "kN", "N") == -50000.0


@pytest.mark.unit
def test_unsupported_units_raise_value_error():
    """Verify attempting incompatible or unknown unit conversions raises ValueError."""
    with pytest.raises(ValueError) as exc:
        convert_units(24.0, "meters", "kN")
    assert "Incompatible" in str(exc.value)

    with pytest.raises(ValueError):
        convert_units(10.0, "unknown_unit", "m")
