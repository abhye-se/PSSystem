# Roadmap

## M0 — Repository and tooling
Project structure, CI-ready test layout, coding standards, agent rules.

## M1 — Electrical network model
Buses, branches, lines, transformers, generators, loads, shunts, switches.

## M2 — Per-unit system
Base quantities and deterministic conversion rules.

## M3 — Y-bus
Sparse nodal-admittance construction with line charging and transformers.

## M4 — Newton-Raphson AC power flow
Slack/PV/PQ buses, mismatch equations, Jacobian, convergence reporting.

## M5 — Operating constraints
Generator reactive limits, PV/PQ switching, transformer taps, branch limits.

## M6 — Benchmark validation
IEEE benchmark networks and independently checked expected results.

## M7 — Reporting and I/O
Structured result model, serialization, tabular reporting, import/export.

## M8 — Single-line editor
Graphical network construction backed by the same domain model.

## M9 — IEC 60909 short-circuit
Standards-based short-circuit engine with dedicated validation suite.
