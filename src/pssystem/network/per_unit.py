from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


def _positive(value: float, name: str) -> float:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return float(value)


def _finite(value: float, name: str) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)


@dataclass(frozen=True, slots=True)
class BaseValues:
    """Three-phase per-unit base quantities.

    ``power_mva`` is the three-phase apparent-power base.
    ``voltage_kv`` is line-to-line RMS voltage base.
    Derived current is line current and impedance is per-phase impedance.
    """

    power_mva: float
    voltage_kv: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "power_mva", _positive(self.power_mva, "power_mva"))
        object.__setattr__(self, "voltage_kv", _positive(self.voltage_kv, "voltage_kv"))

    @property
    def current_ka(self) -> float:
        return self.power_mva / (sqrt(3.0) * self.voltage_kv)

    @property
    def impedance_ohm(self) -> float:
        return self.voltage_kv**2 / self.power_mva

    @property
    def admittance_siemens(self) -> float:
        return 1.0 / self.impedance_ohm

    def power_to_pu(self, power_mw_or_mvar: float) -> float:
        return _finite(power_mw_or_mvar, "power_mw_or_mvar") / self.power_mva

    def power_from_pu(self, value_pu: float) -> float:
        return _finite(value_pu, "value_pu") * self.power_mva

    def voltage_to_pu(self, voltage_kv: float) -> float:
        return _finite(voltage_kv, "voltage_kv") / self.voltage_kv

    def voltage_from_pu(self, value_pu: float) -> float:
        return _finite(value_pu, "value_pu") * self.voltage_kv

    def current_to_pu(self, current_ka: float) -> float:
        return _finite(current_ka, "current_ka") / self.current_ka

    def current_from_pu(self, value_pu: float) -> float:
        return _finite(value_pu, "value_pu") * self.current_ka

    def impedance_to_pu(self, impedance_ohm: complex | float) -> complex:
        value = complex(impedance_ohm)
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("impedance_ohm must be finite")
        return value / self.impedance_ohm

    def impedance_from_pu(self, value_pu: complex | float) -> complex:
        value = complex(value_pu)
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("value_pu must be finite")
        return value * self.impedance_ohm

    def admittance_to_pu(self, admittance_siemens: complex | float) -> complex:
        value = complex(admittance_siemens)
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("admittance_siemens must be finite")
        return value / self.admittance_siemens

    def admittance_from_pu(self, value_pu: complex | float) -> complex:
        value = complex(value_pu)
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("value_pu must be finite")
        return value * self.admittance_siemens


def change_impedance_base(
    value_pu: complex | float,
    *,
    old_power_mva: float,
    old_voltage_kv: float,
    new_power_mva: float,
    new_voltage_kv: float,
) -> complex:
    """Convert per-unit impedance between bases.

    Zpu,new = Zpu,old * (Snew/Sold) * (Vold/Vnew)^2
    """

    value = complex(value_pu)
    if not (isfinite(value.real) and isfinite(value.imag)):
        raise ValueError("value_pu must be finite")
    old_s = _positive(old_power_mva, "old_power_mva")
    old_v = _positive(old_voltage_kv, "old_voltage_kv")
    new_s = _positive(new_power_mva, "new_power_mva")
    new_v = _positive(new_voltage_kv, "new_voltage_kv")
    return value * (new_s / old_s) * (old_v / new_v) ** 2


def change_admittance_base(
    value_pu: complex | float,
    *,
    old_power_mva: float,
    old_voltage_kv: float,
    new_power_mva: float,
    new_voltage_kv: float,
) -> complex:
    """Convert per-unit admittance between bases."""

    value = complex(value_pu)
    if not (isfinite(value.real) and isfinite(value.imag)):
        raise ValueError("value_pu must be finite")
    old_s = _positive(old_power_mva, "old_power_mva")
    old_v = _positive(old_voltage_kv, "old_voltage_kv")
    new_s = _positive(new_power_mva, "new_power_mva")
    new_v = _positive(new_voltage_kv, "new_voltage_kv")
    return value * (old_s / new_s) * (new_v / old_v) ** 2
