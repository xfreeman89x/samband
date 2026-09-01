# Samband Threat Model

## Status

Placeholder requiring Agent 4 Security ownership and review. This file lists
the required structure only; it is not a completed threat model.

## Scope to define

- assets: identities, credentials, channel authorization, keys, payloads,
  membership, routing availability, device resources, and metadata;
- actors: honest nodes, malicious relays, malicious endpoints/members, passive
  observers, active nearby attackers, compromised devices, and optional future
  gateways;
- trust boundaries: discovery, one-hop transport, relay envelope, routing,
  channel security, app/core/FFI, device storage, and diagnostics;
- operating assumptions: offline use, partitions, clock quality, physical access,
  OS compromise boundaries, and denial-of-service limits;
- explicit non-goals and residual risks.

## Threats requiring analysis

- impersonation and unauthorized channel membership;
- replay, packet injection, and downgrade;
- route poisoning, blackhole/selective forwarding, wormhole, and Sybil behavior;
- malicious relay and malicious authorized channel member;
- discovery tracking, traffic analysis, membership correlation, and metadata
  leakage;
- parser, memory, CPU, bandwidth, battery, and storage exhaustion;
- key/device compromise, member removal, recovery, and rollback;
- PTT monopolization, forgery, stale ownership, and denial of service;
- diagnostic leakage and accidental audio persistence;
- supply-chain and unsafe/FFI implementation risk.

## Required outputs

Agent 4 must provide attacker capabilities, security goals, abuse cases, trust
assumptions, mitigations, residual risks, verification plan, and explicit release
blockers. Each security-sensitive RFC must link to the applicable analysis.

Protocol v1 cannot freeze while this document remains a placeholder.

