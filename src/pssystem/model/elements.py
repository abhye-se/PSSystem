from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from math import isfinite
from typing import Any


class PhaseConnection(str, Enum):
    """Common three-phase winding/load connection types."""

    WYE = "wye"
    DELTA = "delta"


class SwitchState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


def _require_identifier(value: str, field_name: str = "id") -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_finite(value: float, field_name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{field_name} must be finite")


def _require_positive(value: float, field_name: str) -> None:
    _require_finite(value, field_name)
    if value <= 0.0:
        raise ValueError(f"{field_name} must be > 0")


def _require_non_negative(value: float, field_name: str) -> None:
    _require_finite(value, field_name)
    if value < 0.0:
        raise ValueError(f"{field_name} must be >= 0")


class SerializableMixin:
    """Small JSON-ready representation for immutable domain objects."""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key, value in tuple(data.items()):
            if isinstance(value, Enum):
                data[key] = value.value
        return data


@dataclass(frozen=True, slots=True)
class Bus(SerializableMixin):
    """Electrical node.

    ``nominal_kv`` is line-to-line RMS voltage for a three-phase system.
    """

    id: str
    nominal_kv: float
    name: str | None = None
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_positive(self.nominal_kv, "nominal_kv")
        if self.name is not None and not self.name.strip():
            raise ValueError("name must be non-empty when provided")


@dataclass(frozen=True, slots=True)
class Line(SerializableMixin):
    """Balanced positive-sequence line model in physical units.

    ``r_ohm`` and ``x_ohm`` are total series impedance per phase.
    ``b_siemens`` is total shunt susceptance per phase and is split equally
    between the two terminals by the network model.
    """

    id: str
    from_bus: str
    to_bus: str
    r_ohm: float
    x_ohm: float
    b_siemens: float = 0.0
    rate_mva: float | None = None
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.from_bus, "from_bus")
        _require_identifier(self.to_bus, "to_bus")
        if self.from_bus == self.to_bus:
            raise ValueError("line terminals must reference different buses")
        _require_non_negative(self.r_ohm, "r_ohm")
        _require_finite(self.x_ohm, "x_ohm")
        _require_finite(self.b_siemens, "b_siemens")
        if self.r_ohm == 0.0 and self.x_ohm == 0.0:
            raise ValueError("line series impedance cannot be zero")
        if self.rate_mva is not None:
            _require_positive(self.rate_mva, "rate_mva")


@dataclass(frozen=True, slots=True)
class Transformer(SerializableMixin):
    """Two-winding transformer model.

    Impedance is stored in per-unit on ``rated_mva`` and the winding rated
    voltages. ``tap_ratio`` is the off-nominal ratio multiplier applied at
    the ``from_bus`` winding. ``phase_shift_deg`` is positive for a phase
    advance from the from-side to the to-side.
    """

    id: str
    from_bus: str
    to_bus: str
    rated_mva: float
    from_nominal_kv: float
    to_nominal_kv: float
    r_pu: float
    x_pu: float
    tap_ratio: float = 1.0
    phase_shift_deg: float = 0.0
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.from_bus, "from_bus")
        _require_identifier(self.to_bus, "to_bus")
        if self.from_bus == self.to_bus:
            raise ValueError("transformer terminals must reference different buses")
        _require_positive(self.rated_mva, "rated_mva")
        _require_positive(self.from_nominal_kv, "from_nominal_kv")
        _require_positive(self.to_nominal_kv, "to_nominal_kv")
        _require_non_negative(self.r_pu, "r_pu")
        _require_finite(self.x_pu, "x_pu")
        if self.r_pu == 0.0 and self.x_pu == 0.0:
            raise ValueError("transformer series impedance cannot be zero")
        _require_positive(self.tap_ratio, "tap_ratio")
        _require_finite(self.phase_shift_deg, "phase_shift_deg")


@dataclass(frozen=True, slots=True)
class Generator(SerializableMixin):
    """Controllable source.

    Positive ``p_mw`` and ``q_mvar`` mean injection into the network.
    Reactive-power and active-power limits are optional equipment limits.
    """

    id: str
    bus: str
    p_mw: float
    q_mvar: float = 0.0
    voltage_setpoint_pu: float = 1.0
    p_min_mw: float | None = None
    p_max_mw: float | None = None
    q_min_mvar: float | None = None
    q_max_mvar: float | None = None
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.bus, "bus")
        _require_finite(self.p_mw, "p_mw")
        _require_finite(self.q_mvar, "q_mvar")
        _require_positive(self.voltage_setpoint_pu, "voltage_setpoint_pu")
        for field_name in ("p_min_mw", "p_max_mw", "q_min_mvar", "q_max_mvar"):
            value = getattr(self, field_name)
            if value is not None:
                _require_finite(value, field_name)
        if self.p_min_mw is not None and self.p_max_mw is not None and self.p_min_mw > self.p_max_mw:
            raise ValueError("p_min_mw must be <= p_max_mw")
        if self.q_min_mvar is not None and self.q_max_mvar is not None and self.q_min_mvar > self.q_max_mvar:
            raise ValueError("q_min_mvar must be <= q_max_mvar")
        if self.p_min_mw is not None and self.p_mw < self.p_min_mw:
            raise ValueError("p_mw is below p_min_mw")
        if self.p_max_mw is not None and self.p_mw > self.p_max_mw:
            raise ValueError("p_mw is above p_max_mw")
        if self.q_min_mvar is not None and self.q_mvar < self.q_min_mvar:
            raise ValueError("q_mvar is below q_min_mvar")
        if self.q_max_mvar is not None and self.q_mvar > self.q_max_mvar:
            raise ValueError("q_mvar is above q_max_mvar")


@dataclass(frozen=True, slots=True)
class Load(SerializableMixin):
    """Constant-power load.

    Positive ``p_mw`` and ``q_mvar`` mean consumption from the network.
    """

    id: str
    bus: str
    p_mw: float
    q_mvar: float = 0.0
    connection: PhaseConnection = PhaseConnection.WYE
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.bus, "bus")
        _require_non_negative(self.p_mw, "p_mw")
        _require_finite(self.q_mvar, "q_mvar")


@dataclass(frozen=True, slots=True)
class Shunt(SerializableMixin):
    """Bus-connected shunt specified by reactive injection at 1.0 pu voltage.

    Positive ``q_mvar_at_1pu`` injects reactive power (capacitive); negative
    values absorb reactive power (inductive).
    """

    id: str
    bus: str
    q_mvar_at_1pu: float
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.bus, "bus")
        _require_finite(self.q_mvar_at_1pu, "q_mvar_at_1pu")


@dataclass(frozen=True, slots=True)
class Switch(SerializableMixin):
    """Ideal topological switch between two buses."""

    id: str
    from_bus: str
    to_bus: str
    state: SwitchState = SwitchState.CLOSED
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_identifier(self.id)
        _require_identifier(self.from_bus, "from_bus")
        _require_identifier(self.to_bus, "to_bus")
        if self.from_bus == self.to_bus:
            raise ValueError("switch terminals must reference different buses")
