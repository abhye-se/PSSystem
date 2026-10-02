# Validation Strategy

Validation is a first-class subsystem, not a final QA step.

Each analysis engine should include:

- unit tests for elemental equations
- analytical hand-checkable cases
- published benchmark cases
- IEEE test systems where appropriate
- cross-checks with an independent implementation
- regression tests
- conservation and consistency checks
- convergence and failure-mode tests
- documented numerical tolerances

A benchmark discrepancy must be investigated before expected values are changed.
