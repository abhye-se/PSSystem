from math import isclose, sqrt

import pytest

from pssystem.network.per_unit import BaseValues, change_admittance_base, change_impedance_base


def test_base_values_three_phase_relationships() -> None:
    base = BaseValues(100.0, 10.0)
    assert isclose(base.impedance_ohm, 1.0)
    assert isclose(base.admittance_siemens, 1.0)
    assert isclose(base.current_ka, 100.0 / (sqrt(3.0) * 10.0))


def test_round_trip_scalar_quantities() -> None:
    base = BaseValues(100.0, 132.0)
    assert isclose(base.power_from_pu(base.power_to_pu(45.0)), 45.0)
    assert isclose(base.voltage_from_pu(base.voltage_to_pu(126.0)), 126.0)
    assert isclose(base.current_from_pu(base.current_to_pu(0.4)), 0.4)


def test_round_trip_complex_impedance_and_admittance() -> None:
    base = BaseValues(100.0, 132.0)
    z = 2.1 + 1.7j
    y = 0.02 - 0.1j
    assert abs(base.impedance_from_pu(base.impedance_to_pu(z)) - z) < 1e-12
    assert abs(base.admittance_from_pu(base.admittance_to_pu(y)) - y) < 1e-12


def test_impedance_base_change_matches_standard_formula() -> None:
    z_new = change_impedance_base(
        0.1j,
        old_power_mva=50.0,
        old_voltage_kv=11.0,
        new_power_mva=100.0,
        new_voltage_kv=11.0,
    )
    assert z_new == pytest.approx(0.2j)


def test_impedance_base_change_with_voltage_change() -> None:
    z_new = change_impedance_base(
        0.08j,
        old_power_mva=100.0,
        old_voltage_kv=10.0,
        new_power_mva=100.0,
        new_voltage_kv=20.0,
    )
    assert z_new == pytest.approx(0.02j)


def test_admittance_base_change_is_inverse_scaling() -> None:
    y_new = change_admittance_base(
        0.2j,
        old_power_mva=50.0,
        old_voltage_kv=10.0,
        new_power_mva=100.0,
        new_voltage_kv=20.0,
    )
    assert y_new == pytest.approx(0.4j)


def test_invalid_bases_are_rejected() -> None:
    with pytest.raises(ValueError, match="power_mva"):
        BaseValues(0.0, 11.0)
    with pytest.raises(ValueError, match="voltage_kv"):
        BaseValues(100.0, -11.0)
