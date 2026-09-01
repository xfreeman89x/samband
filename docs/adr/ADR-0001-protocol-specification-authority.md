---
adr: "0001"
title: Protocol Specification Authority
status: Accepted
date: 2026-09-01
deciders:
  - Principal Architect / Maintainer
consulted:
  - Project charter
informed:
  - All component owners
supersedes: []
superseded_by: null
---

# ADR-0001: Protocol Specification Authority

## Context

Samband intends to support independent implementations. If official application
behavior defines the protocol implicitly, interoperability depends on reverse
engineering and implementation bugs can become accidental standards.

## Decision drivers

- third parties must implement Samband from public material;
- protocol changes need durable review and compatibility history;
- multiple platforms and future devices must share one contract;
- security review needs stable, inspectable semantics.

## Decision

Accepted protocol specification text, accepted RFCs, and canonical vectors are
authoritative over reference implementations. RFCs hold protocol rationale and
decisions; `protocol/spec` holds cohesive normative behavior after RFC acceptance.

When implementation, vector, and specification disagree, the discrepancy is
reported and resolved explicitly. Implementation behavior never silently
changes the protocol.

## Consequences

### Positive

- independent implementations have a public source of truth;
- interoperability and security review can precede code coupling;
- protocol evolution and objections remain traceable.

### Negative

- protocol work requires documentation and review before implementation;
- specification/vector defects need coordinated correction rather than a quick
  implementation-only fix.

### Neutral or follow-up

- Agent 1 must establish normative specification conventions and vector formats;
- pre-v1 experimental profiles must be marked explicitly.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| reference implementation as specification | blocks independent development and canonizes bugs |
| generated documentation only from core code | couples protocol authority to one language and cannot capture all semantics/rationale |
| informal consensus in issues | lacks stable versioned authority and review gates |

## Validation

Before v1.0, two independent implementations must pass the same mandatory
vectors and interoperate without undocumented behavior.

## Protocol impact

This ADR defines authority, not protocol semantics. Material semantics still
require an RFC.

## Security and privacy impact

Positive: security reviewers receive stable public inputs. No cryptographic
design is accepted by this ADR.

## Revisit triggers

- specification and vector governance cannot resolve repeated contradictions;
- independent implementers cannot build from the published material.

