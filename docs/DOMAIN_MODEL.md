# Electrical Domain Model

The domain model is intentionally independent of any one solver.

## Sign conventions

- Generator `p_mw > 0`: active power injected into the network.
- Generator `q_mvar > 0`: reactive power injected into the network.
- Load `p_mw > 0`: active power consumed from the network.
- Load `q_mvar > 0`: reactive power consumed from the network.
- Shunt `q_mvar_at_1pu > 0`: capacitive reactive injection.
- Shunt `q_mvar_at_1pu < 0`: inductive reactive absorption.

## Voltage conventions

Bus nominal voltage is line-to-line RMS kV for balanced three-phase systems.

## Line model

Lines use total per-phase series resistance/reactance in ohms and total per-phase shunt susceptance in siemens. The network admittance builder will split total shunt susceptance equally between terminals.

## Transformer model

Two-winding transformer leakage impedance is stored in per-unit on the transformer's own rated MVA and winding rated voltages. Off-nominal tap ratio is applied at the from-side. Positive phase shift denotes a phase advance from from-side to to-side.

## Topology integrity

`Network` validates unique equipment IDs and verifies that all equipment bus references resolve to buses in the same network.

Solver concepts such as Slack/PV/PQ bus classification are intentionally not embedded in these core equipment objects; they belong to study/solver configuration.
