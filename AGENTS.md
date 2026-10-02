# PSSystem Agent Instructions

## Mission

Develop PSSystem into a professional, transparent, validated power-system analysis platform.

The long-term objective is to provide engineering capabilities comparable to major commercial power-system analysis platforms while emphasizing numerical transparency, reproducibility, automation, scripting, and independent validation.

## Engineering priorities

1. Electrical engineering correctness
2. Numerical robustness
3. Validation and reproducibility
4. Maintainable architecture
5. Performance
6. User-interface convenience

Never sacrifice engineering correctness merely to make a test pass.

## Autonomous development rules

- Work only on approved GitHub Issues or explicitly assigned tasks.
- Never push directly to `main`.
- Use an `agent/*` development branch.
- Never merge your own pull request.
- Keep changes small and reviewable.
- Run all relevant tests before opening a pull request.
- Do not weaken or delete valid tests merely to obtain passing results.
- Do not modify engineering equations simply to match another software package.
- Investigate discrepancies mathematically.
- Clearly document assumptions and unresolved questions.
- Leave the repository in a buildable state.

## Engineering traceability

Every major analytical method must document governing equations, assumptions, units, sign conventions, per-unit conventions, numerical tolerances, applicable IEEE/IEC references, benchmark cases, and known limitations.

## Validation

Every solver must be independently validated using appropriate analytical examples, published benchmark systems, IEEE test systems, comparison with trusted independent implementations, regression tests, conservation checks, and numerical sensitivity testing.

Differences against third-party software must not automatically be treated as errors in PSSystem.

## Initial development sequence

1. Core project architecture
2. Electrical network data model
3. Per-unit system
4. Y-bus construction
5. Newton-Raphson AC power flow
6. PV/PQ bus handling
7. Generator reactive limits
8. Transformer taps and phase shifting
9. Branch flows and losses
10. IEEE benchmark validation
11. Reporting and import/export
12. Graphical single-line diagram
13. IEC 60909 short-circuit analysis

Do not proceed to advanced modules until the shared network model and load-flow foundation are sufficiently validated.
