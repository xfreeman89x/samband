# Project Risk Register

## Scale

- Likelihood: Low, Medium, High, or Unknown.
- Impact: Medium, High, or Critical.
- Gate: earliest milestone that needs evidence or a reviewed decision.

The domain owner maintains evidence; a maintainer owns cross-component closure.

| ID | Risk | Likelihood | Impact | Owner/review | Mitigation or evidence | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | community relay is unreliable or too costly under mobile lifecycle, battery, thermal, and data constraints | High | High | Android, iOS, Routing | physical capability/energy experiments; explicit dynamic relay policy | M3/M4 |
| R-002 | iOS cannot sustain discovery or background relay in required states | High | High | iOS | state-by-state device experiments; advertise actual availability; avoid protocol distortion | M3/M6 |
| R-003 | Android background and permission constraints prevent predictable relay | Medium | High | Android | foreground/background service experiments across supported OS versions | M3/M4 |
| R-004 | routing overhead or convergence fails under mobile churn and alternate paths | Unknown | High | Routing | compare bounded candidate algorithms in seeded simulator; measure churn and overhead | M1/M2 |
| R-005 | relay metadata leaks channel relationships, stable identity, or communication patterns | High | Critical | Security, Protocol | metadata inventory, unlinkability analysis, rotating discovery experiments | M1 |
| R-006 | decentralized group membership and removal cannot meet security/usability goals offline | Unknown | Critical | Security | threat model; compare standardized group-key approaches; prototype membership changes | M1/M4 |
| R-007 | duplicate, replay, or loop defenses permit resource exhaustion | Medium | Critical | Protocol, Routing, Security | bounded caches/windows, adversarial vectors, simulation and fuzzing | M1/M2 |
| R-008 | cross-platform discovery has no common viable transport path | Unknown | High | Android, iOS, Protocol | transport capability matrix and physical interoperability spikes | M3/M6 |
| R-009 | distributed PTT arbitration creates prolonged conflict or unfairness through partitions | Unknown | High | Protocol, Routing, Audio, Security | deterministic partition/concurrency models before audio | M1/M5 |
| R-010 | realtime audio exceeds latency, loss, or energy budgets over multi-hop paths | Unknown | High | Audio, Routing, Platforms | simulator freshness model then measured Opus/device pipeline | M5 |
| R-011 | portable Rust core and FFI cost outweigh shared-code benefit | Unknown | Medium | Core, Android, iOS | narrow prototype measuring build, binary, ownership, callbacks, errors, and debugging | M1/M3 |
| R-012 | serialization choice creates decoder risk, overhead, or poor independent implementability | Unknown | High | Protocol, Security, Core | compare candidates with corpus, size/latency measures, negative vectors, and fuzzability | M1 |
| R-013 | capability claims become stale and create unsafe relay/routing decisions | Medium | High | Protocol, Routing, Platforms | freshness/withdrawal semantics and dynamic transition scenarios | M1/M2 |
| R-014 | gateway work introduces central authority, generic proxying, or metadata expansion | Medium | High | Architect, Protocol, Security | keep gateway out of initial scope; require future RFC and threat-model update | after M4 |
| R-015 | reference implementations become de facto undocumented specification | Medium | Critical | Architect, Protocol, Ecosystem | spec authority, immutable vectors, independent implementation gate | all |
| R-016 | dependency licensing, maintenance, or supply-chain risk harms public adoption | Medium | High | Maintainers, Security | dependency review, minimal dependency surface, license and provenance checks | every implementation gate |
| R-017 | diagnostics retain stable identifiers, secrets, plaintext, or audio | Medium | Critical | Security and component owners | safe logging contract, redaction tests, artifact audits | M1 onward |
| R-018 | volunteer governance cannot resolve cross-domain protocol changes consistently | Medium | High | Maintainers | explicit RFC gates, decision records, ownership, objection logs | all |

## Review cadence

Review the register when an RFC enters Discussion, an ADR is accepted, a
milestone is proposed as complete, or new physical evidence invalidates an
assumption. Closing a risk requires a link to evidence or an accepted decision;
silence is not closure.
