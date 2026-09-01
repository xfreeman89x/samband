---
adr: "0004"
title: Rust Shared Core
status: Proposed
date: 2026-09-01
deciders:
  - Principal Architect / Maintainer
consulted: []
informed:
  - Core, Android, iOS, Simulator, and Ecosystem owners
supersedes: []
superseded_by: null
---

# ADR-0004: Rust Shared Core

## Context

Portable packet validation, bounded mesh state, routing primitives, and state
machines could benefit from one memory-safe implementation shared by simulator,
mobile apps, Linux, and future devices. Rust is the preferred direction in the
project charter, but FFI, build, binary, debugging, and lifecycle cost are not
yet measured.

## Decision drivers

- memory-safe handling of untrusted packets;
- deterministic tests and fuzzing;
- portability to mobile, desktop, and embedded Linux;
- reduction of duplicated protocol behavior;
- maintainable narrow bindings rather than exposing an entire runtime.

## Proposed decision

Evaluate Rust as the portable shared-core language through a small, deliberately
narrow prototype. Do not create a broad production crate graph or FFI API until
the experiment passes.

The prototype should exercise bounded packet decode of an experimental fixture,
an injected clock/randomness interface, one state transition, error mapping,
byte ownership, callback/concurrency behavior, Kotlin and Swift build/link steps,
binary size, sanitizer/fuzz workflow, and contributor setup on Windows, macOS,
and Linux where applicable.

## Consequences if accepted

### Positive

- one reviewed core can serve several reference platforms;
- Rust tooling supports strong types, fuzzing, and controlled memory ownership;
- simulator and physical nodes can share logic.

### Negative

- mobile FFI and cross-compilation increase build and debugging complexity;
- Swift/Kotlin async, cancellation, and ownership mismatches need careful APIs;
- contributor toolchain requirements increase.

### Neutral or follow-up

- native audio and transport APIs remain outside Rust unless a later ADR proves
  a better boundary;
- bindings expose only stable use cases, not every internal type.

## Alternatives considered

| Alternative | Why not selected yet |
| --- | --- |
| duplicate native Kotlin and Swift cores | simpler platform tooling but high semantic drift and duplicated security review |
| C/C++ portable core | broad portability but weaker default memory safety and a larger unsafe surface |
| Kotlin Multiplatform | promising mobile sharing but future-device, Swift integration, and low-level codec/routing fit need comparison |
| specification plus independent native implementations only | strongest independence but high initial implementation and consistency cost |

No alternative is rejected until the experiment reports evidence.

## Validation required for acceptance

- reproducible build and test path on supported contributor hosts;
- Android and iOS integration spike with documented lifecycle/error boundaries;
- measured binary size, build time, call overhead, and debugging workflow;
- packet decoder fuzzing and unsafe-code policy proposal;
- Apache-compatible dependency/license review;
- clear public API boundary and ownership model.

## Protocol impact

None. Rust cannot define protocol semantics; it consumes accepted specification
and vectors.

## Security and privacy impact

Potential memory-safety benefit, offset by FFI/unsafe and supply-chain surfaces.
Agent 4 should review the eventual unsafe/secret-handling policy.

## Revisit triggers

- mobile prototype cost exceeds measured shared-core benefit;
- supported future hardware cannot use the produced core;
- FFI prevents required performance, lifecycle, or auditability.
