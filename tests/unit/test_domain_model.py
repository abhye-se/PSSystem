import json

import pytest

from pssystem.model import (
    Bus,
    Generator,
    Line,
    Load,
    Network,
    PhaseConnection,
    Shunt,
    Switch,
    SwitchState,
    Transformer,
)


def test_bus_requires_positive_nominal_voltage() -> None:
    with pytest.raises(ValueError, match="nominal_kv"):
        Bus(id="B1", nominal_kv=0.0)


def test_line_requires_distinct_buses_and_nonzero_impedance() -> None:
    with pytest.raises(ValueError, match="different buses"):
        Line(id="L1", from_bus="B1", to_bus="B1", r_ohm=0.1, x_ohm=0.2)
    with pytest.raises(ValueError, match="cannot be zero"):
        Line(id="L1", from_bus="B1", to_bus="B2", r_ohm=0.0, x_ohm=0.0)


def test_transformer_validates_tap_and_rating() -> None:
    with pytest.raises(ValueError, match="rated_mva"):
        Transformer("T1", "B1", "B2", 0.0, 132.0, 33.0, 0.01, 0.1)
    with pytest.raises(ValueError, match="tap_ratio"):
        Transformer("T1", "B1", "B2", 100.0, 132.0, 33.0, 0.01, 0.1, tap_ratio=0.0)


def test_generator_enforces_limits() -> None:
    with pytest.raises(ValueError, match="below p_min"):
        Generator("G1", "B1", p_mw=5.0, p_min_mw=10.0, p_max_mw=100.0)
    with pytest.raises(ValueError, match="q_min_mvar must"):
        Generator("G1", "B1", p_mw=20.0, q_min_mvar=10.0, q_max_mvar=-10.0)


def test_load_sign_convention_rejects_negative_active_consumption() -> None:
    with pytest.raises(ValueError, match="p_mw"):
        Load("LD1", "B1", p_mw=-1.0)


def test_network_rejects_unknown_bus_reference() -> None:
    with pytest.raises(ValueError, match="unknown bus"):
        Network.from_iterables(
            buses=[Bus("B1", 11.0)],
            loads=[Load("LD1", "B2", 1.0)],
        )


def test_network_rejects_duplicate_equipment_ids_across_types() -> None:
    with pytest.raises(ValueError, match="duplicate equipment id"):
        Network.from_iterables(
            buses=[Bus("X", 11.0), Bus("B2", 11.0)],
            lines=[Line("X", "X", "B2", 0.1, 0.2)],
        )


def test_network_is_json_serializable_and_enum_values_are_strings() -> None:
    network = Network.from_iterables(
        buses=[Bus("B1", 132.0), Bus("B2", 132.0)],
        lines=[Line("L1", "B1", "B2", 0.1, 0.8, b_siemens=1e-4)],
        generators=[Generator("G1", "B1", 50.0, q_mvar=10.0)],
        loads=[Load("LD1", "B2", 45.0, q_mvar=15.0, connection=PhaseConnection.DELTA)],
        shunts=[Shunt("SH1", "B2", 5.0)],
        switches=[Switch("SW1", "B1", "B2", state=SwitchState.OPEN)],
    )

    payload = network.to_dict()
    json.dumps(payload)
    assert payload["loads"][0]["connection"] == "delta"
    assert payload["switches"][0]["state"] == "open"


def test_network_accepts_valid_two_voltage_level_system() -> None:
    network = Network.from_iterables(
        buses=[Bus("HV", 132.0), Bus("LV", 33.0)],
        transformers=[
            Transformer(
                "T1",
                "HV",
                "LV",
                rated_mva=90.0,
                from_nominal_kv=132.0,
                to_nominal_kv=33.0,
                r_pu=0.01,
                x_pu=0.12,
            )
        ],
        generators=[Generator("G1", "HV", 40.0)],
        loads=[Load("LD1", "LV", 35.0, 8.0)],
    )
    assert len(network.transformers) == 1
    assert network.loads[0].p_mw == 35.0
