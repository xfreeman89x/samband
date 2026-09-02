# Samband Research and Experiments

This area records questions whose answer depends on measurements, prototypes,
standards analysis, or physical platform evidence. An experiment does not create
protocol authority; its result informs an RFC or ADR.

Every experiment should define:

- decision/question and competing alternatives;
- hypothesis and success/failure thresholds;
- reproducible setup, versions, topology/device matrix, and inputs;
- collected metrics and known sources of bias;
- security/privacy constraints and artifact handling;
- result, raw non-sensitive evidence, and impact on RFC/ADR status.

The canonical queue and integrated EXP-001 through EXP-019 dependency graph are
in [`experiment-backlog.md`](experiment-backlog.md). The
[`Wave 0 Integration Review`](../architecture/wave0-integration-review.md)
records which evidence-generating work is authorized by the non-production
[`wave1-sim-v0.1`](../../protocol/spec/v0x-simulation-profile.md) contract.

## Integrated experiment plans

- [`Routing requirements and candidate evaluation`](routing-candidate-evaluation.md)
  refines EXP-003 and EXP-004 into reproducible simulator scenarios, candidate
  metadata requirements, metrics, and security/privacy questions. It records no
  routing-family selection and no experimental result.
