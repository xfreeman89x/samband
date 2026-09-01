# Agent Coordination

[`PROMPTS.md`](PROMPTS.md) defines roles, ownership, execution waves, and detailed
prompts. [`HANDOFF-TEMPLATE.md`](HANDOFF-TEMPLATE.md) defines the required
completion report.

## Ownership summary

| Agent | Primary ownership |
| --- | --- |
| 0 Architect | architecture, ADRs, RFC governance, integration, boundaries |
| 1 Protocol | specification, schemas, compatibility, canonical vectors |
| 2 Rust Core | portable core implementation |
| 3 Routing | routing, relay behavior, routing simulation model |
| 4 Security | threat model, identity, channel/relay/discovery security |
| 5 Simulator | deterministic simulation and reliability infrastructure |
| 6 Android | Android app, transports, lifecycle, diagnostics |
| 7 iOS | iOS app, transports, lifecycle, diagnostics |
| 8 Audio/PTT | codec pipeline, media lifecycle, latency |
| 9 Ecosystem | bindings, vector runners, independent implementation guidance |

Agents read `AGENTS.md`, architecture, and accepted decision records before
work. No agent independently changes a contract in the shared-contract registry.

## Execution discipline

Wave order is a dependency graph, not a request to start everyone. Wave 0
defines architecture/protocol/security; Wave 1 proves simulation; Wave 2 proves
Android relay; Wave 3 adds realtime audio; Wave 4 proves cross-platform behavior.
An agent may research an open question earlier, but cannot publish blocked
semantics as Samband protocol.

