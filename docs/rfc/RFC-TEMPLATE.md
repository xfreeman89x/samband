---
rfc: "NNNN"
title: Short descriptive title
status: Draft
authors:
  - Samband contributor name or handle
created: YYYY-MM-DD
updated: YYYY-MM-DD
target: Protocol v0.x
requires:
  - Agent 1 Protocol review when wire-visible
  - Agent 4 Security review when security-sensitive
  - Agent 3 Routing review when routing-sensitive
supersedes: []
superseded_by: null
---

# RFC-NNNN: Short Descriptive Title

## Summary

State the proposal and why it is needed in a few paragraphs.

## Status and authority

Explain whether any text is inherited project constraint, proposed protocol
semantics, or unresolved research. A Draft is non-normative.

## Motivation

Describe the interoperability problem, affected parties, and failure of the
status quo.

## Goals

- Goal one.

## Non-goals

- Explicitly excluded work.

## Terminology

Use the canonical glossary and define only RFC-specific terms.

## Proposed semantics

Specify states, inputs, processing order, outputs, and peer-visible behavior.
Separate conceptual fields from an exact encoding decision.

## Failure and resource bounds

Define malformed input, unsupported state/version, duplicate/replay behavior,
timeouts, allocation limits, and safe failure.

## Privacy and security considerations

Describe trust boundaries, metadata, authentication, authorization, replay,
abuse, and denial-of-service implications. Mark required Agent 4 review.

## Routing considerations

Describe reachability, relay, loop, metric, partition, or convergence impact.
Mark required Agent 3 review.

## Wire and versioning impact

Describe message families, fields, extensibility, negotiation, downgrade, and
compatibility. Mark required Agent 1 review.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| A | | | |

## Test-vector and interoperability plan

List positive, negative, state-machine, and cross-implementation evidence.

## Migration and rollout

Explain pre-v1 changes, coexistence, feature negotiation, and rollback where
applicable.

## Open questions

- Unresolved question with an owner or experiment.

## Review requirements

- [ ] Agent 1 Protocol review or not applicable with rationale.
- [ ] Agent 3 Routing review or not applicable with rationale.
- [ ] Agent 4 Security review or not applicable with rationale.
- [ ] Test-vector plan reviewed.
- [ ] Compatibility impact reviewed.

## Acceptance blockers

- List every issue that prevents moving to Accepted.

## Decision record

Record Discussion entry, significant objections, approvals, acceptance or
rejection date, and rationale. Do not fill this section by implication.

## References

- Link related architecture, RFCs, ADRs, experiments, and external standards.

