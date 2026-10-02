# Architecture

PSSystem is organized around a shared electrical network model consumed by independent analysis engines.

## Layers

1. Domain model
2. Network topology and per-unit normalization
3. Numerical analysis engines
4. Validation and benchmark framework
5. Import/export and reporting
6. API and future graphical interface

## Initial packages

- `pssystem.model`: equipment and network-domain objects
- `pssystem.network`: topology, per-unit conversion, Y-bus construction
- `pssystem.loadflow`: AC load-flow algorithms
- `pssystem.shortcircuit`: short-circuit analysis
- `pssystem.protection`: protection models and coordination
- `pssystem.dynamics`: dynamic simulation
- `pssystem.io`: import/export and serialization

Analysis engines must depend on the common model rather than duplicating equipment representations.
