from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .elements import Bus, Generator, Line, Load, Shunt, Switch, Transformer

Equipment = Bus | Line | Transformer | Generator | Load | Shunt | Switch


@dataclass(frozen=True, slots=True)
class Network:
    """Validated immutable collection of electrical equipment."""

    buses: tuple[Bus, ...] = field(default_factory=tuple)
    lines: tuple[Line, ...] = field(default_factory=tuple)
    transformers: tuple[Transformer, ...] = field(default_factory=tuple)
    generators: tuple[Generator, ...] = field(default_factory=tuple)
    loads: tuple[Load, ...] = field(default_factory=tuple)
    shunts: tuple[Shunt, ...] = field(default_factory=tuple)
    switches: tuple[Switch, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        collections: tuple[tuple[Equipment, ...], ...] = (
            self.buses,
            self.lines,
            self.transformers,
            self.generators,
            self.loads,
            self.shunts,
            self.switches,
        )
        seen: dict[str, str] = {}
        for collection in collections:
            for item in collection:
                type_name = type(item).__name__
                if item.id in seen:
                    raise ValueError(
                        f"duplicate equipment id {item.id!r}: {seen[item.id]} and {type_name}"
                    )
                seen[item.id] = type_name

        bus_ids = {bus.id for bus in self.buses}
        for item in self.lines + self.transformers + self.switches:
            self._require_bus(item.from_bus, item.id, bus_ids)
            self._require_bus(item.to_bus, item.id, bus_ids)
        for item in self.generators + self.loads + self.shunts:
            self._require_bus(item.bus, item.id, bus_ids)

    @staticmethod
    def _require_bus(bus_id: str, equipment_id: str, bus_ids: set[str]) -> None:
        if bus_id not in bus_ids:
            raise ValueError(f"equipment {equipment_id!r} references unknown bus {bus_id!r}")

    @classmethod
    def from_iterables(
        cls,
        *,
        buses: Iterable[Bus] = (),
        lines: Iterable[Line] = (),
        transformers: Iterable[Transformer] = (),
        generators: Iterable[Generator] = (),
        loads: Iterable[Load] = (),
        shunts: Iterable[Shunt] = (),
        switches: Iterable[Switch] = (),
    ) -> Network:
        return cls(
            buses=tuple(buses),
            lines=tuple(lines),
            transformers=tuple(transformers),
            generators=tuple(generators),
            loads=tuple(loads),
            shunts=tuple(shunts),
            switches=tuple(switches),
        )

    def to_dict(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "buses": [x.to_dict() for x in self.buses],
            "lines": [x.to_dict() for x in self.lines],
            "transformers": [x.to_dict() for x in self.transformers],
            "generators": [x.to_dict() for x in self.generators],
            "loads": [x.to_dict() for x in self.loads],
            "shunts": [x.to_dict() for x in self.shunts],
            "switches": [x.to_dict() for x in self.switches],
        }
