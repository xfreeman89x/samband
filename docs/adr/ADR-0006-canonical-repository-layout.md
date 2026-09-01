---
adr: "0006"
title: Canonical Repository Layout
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

# ADR-0006: Canonical Repository Layout

## Context

The initial repository needs clear ownership before parallel work begins. The
protocol specification must remain independent from reference code, and
architecture, security, RFCs, ADRs, research, and agent guidance need durable
locations.

## Decision drivers

- visible authority and component ownership;
- clean separation of protocol, core, simulator, apps, and bindings;
- public contributor discoverability;
- room for canonical vectors and compatibility material;
- minimal empty skeletons without premature toolchains.

## Decision

Adopt the directory structure and ownership map in
[`../architecture/repository-layout.md`](../architecture/repository-layout.md).
Use README skeletons to track not-yet-implemented directories. A new top-level
product component, moved authority, or changed ownership boundary requires a new
ADR.

## Consequences

### Positive

- agents and contributors know where authoritative work belongs;
- implementation cannot easily masquerade as specification;
- empty future areas are documented without generating placeholder code.

### Negative

- several directories exist before implementation;
- maintainers must prevent duplicated documentation across indexes.

### Neutral or follow-up

- component package layouts are decided later by their accepted ADRs;
- generated artifacts require documented provenance and output policy.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| one application-first source tree | obscures protocol authority and future implementations |
| language-first monorepo root | prematurely makes one language the architecture |
| create directories only when code arrives | leaves ownership and review boundaries ambiguous during Wave 0 |

## Validation

The repository validator checks required directories/files and decision-record
indexes. New contributors should reach every authoritative area from README.

## Protocol impact

None. Layout cannot define protocol semantics.

## Security and privacy impact

Positive: dedicated threat-model and review area. The structure introduces no
credential or secret storage location.

## Revisit triggers

- ownership boundaries repeatedly conflict with actual accepted architecture;
- external implementations cannot locate specification and compatibility assets;
- build scale requires a documented repository split.
