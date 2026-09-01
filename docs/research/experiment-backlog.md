# Technical Experiment Backlog

These questions must be answered with evidence rather than architectural
assumptions. IDs are stable; an experiment report should link its governing RFC
or ADR and preserve failed results.

| ID | Question | Minimum evidence | Owner/review | Decision gate |
| --- | --- | --- | --- | --- |
| EXP-001 | Can a narrow Rust core integrate cleanly with Android, iOS, and simulator? | build/link prototype; ownership, async/callback, error, cancellation, binary size, build time, debug, fuzz, and host portability results | Core + Android + iOS; Security for unsafe/FFI | ADR-0004 |
| EXP-002 | Which envelope encoding is compact, evolvable, safe, and independently implementable? | at least two candidate codecs; exact-byte corpus; size/CPU/allocation; unknown-field/version behavior; fuzzing; license/tooling matrix | Protocol + Core + Security | RFC-0004 |
| EXP-003 | Which routing family fits expected Samband size and churn? | identical seeded scenarios across simple candidates; convergence, overhead, delivery, duplicate, churn, state bounds, relay withdrawal | Routing + Simulator + Security | RFC-0005 |
| EXP-004 | What operating envelope should Protocol v0 target? | documented node count/density, churn, loss, latency, path length, and traffic assumptions with scenario sensitivity | Architect + Routing | RFC-0005/M2 |
| EXP-005 | Can discovery identifiers rotate without breaking authenticated sessions and routing? | passive-correlation analysis plus prototype of alias/session binding under reconnect and partition | Security + Protocol + Routing | RFC-0002 |
| EXP-006 | Which standard group security approach fits offline PTT membership? | standards comparison and bounded prototype for add/remove, concurrent partition changes, epochs, compromise, bandwidth/state | Security + Protocol | RFC-0003/0006 |
| EXP-007 | What metadata is strictly necessary at a relay? | field-by-field budget for routing candidates; correlation/traffic-analysis assessment; mitigation cost | Security + Routing + Protocol | RFC-0004/0005/0006 |
| EXP-008 | Which distributed PTT model meets latency and conflict requirements? | seeded concurrency/loss/skew/partition/merge comparison; acquisition latency, fairness, stale-owner recovery, control overhead | Protocol + Routing + Security | RFC-0007 |
| EXP-009 | Which Android transports and lifecycle states support direct/relay operation? | reproducible physical device/OS matrix for discovery, link, background, foreground service, permissions, battery, thermal, and no-Internet behavior | Android | ADR-0005/M3 |
| EXP-010 | Which iOS states support discovery, direct links, background reception, and relay? | reproducible physical device/OS matrix including suspension and capability transitions | iOS | ADR-0005/M6 |
| EXP-011 | Is a cross-platform direct transport path viable? | Android-iOS physical exchange using the same bounded experimental frame and documented setup, without protocol shortcuts | Android + iOS + Protocol | M6 planning |
| EXP-012 | What is the community relay energy/bandwidth cost and safe policy? | multi-hour physical measurements across charging/battery/thermal/data states; withdrawal behavior; abuse load | Platforms + Routing + Security | M4/M7 |
| EXP-013 | Which Opus profile and media policy meet latency/loss/energy goals? | simulator freshness tests followed by physical capture-to-playback stage measurements over multi-hop paths | Audio + Platforms + Routing | RFC-0008/M5 |
| EXP-014 | What maximum Samband frame sizes avoid harmful fragmentation across candidate transports? | transport MTU/fragment behavior, loss amplification, memory/backpressure, and envelope overhead | Platforms + Protocol + Core | RFC-0004 |
| EXP-015 | Which capability freshness/withdrawal semantics avoid chatter and stale routes? | seeded rapid state-change scenarios plus physical lifecycle transition traces | Routing + Protocol + Platforms | RFC-0001/0005 |

## Priority order

Wave 0 should begin with EXP-002 through EXP-008 as scoped design evidence and
planning, while implementation agents remain blocked. EXP-001 and simulator
implementation follow only when required shared contracts authorize an
experimental profile. Mobile and audio experiments follow the roadmap gates.
