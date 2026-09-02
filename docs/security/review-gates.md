# Security Review Gates

No checked item may be inferred from document existence. A reviewer records the
review, scope, revision, findings, and residual risk.

| Gate | Required artifact/review | Blocks |
| --- | --- | --- |
| SG-001 | complete threat model and trust assumptions | all security claims; Protocol v1 |
| SG-002 | node credential, discovery privacy, session binding, rotation, compromise, and recovery review | RFC-0002 acceptance |
| SG-003 | channel authorization, add/remove, epochs, partition behavior, and group-key construction review | RFC-0003 acceptance |
| SG-004 | relay-envelope metadata budget, parser bounds, authentication, replay, amplification, and downgrade review | RFC-0004 acceptance |
| SG-005 | route poisoning, metric trust, Sybil/resource abuse, topology metadata, and safe degradation review | RFC-0005 acceptance |
| SG-006 | standard payload construction, nonce, associated data, key lifecycle, failure oracles, and vectors review | RFC-0006 acceptance and E2EE claims |
| SG-007 | PTT authorization, replay, speaker privacy, monopolization, and partition conflict review | RFC-0007 acceptance |
| SG-008 | audio context binding, freshness/replay, diagnostics, crash artifacts, and non-persistence audit | RFC-0008 acceptance / M5 |
| SG-009 | dependency licenses, provenance, advisories, unsafe/FFI policy, and secret storage review | implementation releases |
| SG-010 | external review plus closure of release-blocking findings | Protocol v1.0 |

## Wave 0 Agent 4 review record

- **Date/revision:** 2026-09-02 working-tree security architecture review.
- **Reviewer:** Agent 4 — Security / Cryptography Engineer.
- **Scope:** the architecture corpus; RFC-0001 through RFC-0008, with detailed
  review of RFC-0002, RFC-0003, RFC-0004, and RFC-0006; the Draft v0.x
  specification/compatibility/vector model; and EXP-002 through EXP-008 plus
  EXP-015 through EXP-019.
- **Findings:** the Draft layering and synthetic security hooks are suitable for
  continued design, but no credential, peer-session construction, channel
  authority, group-security construction, protected-record profile, replay
  model, outer/control origin model, or metadata mitigation is selected.
- **Residual risk:** malicious relays and members, offline revocation, group
  forks, route poisoning, Sybil/resource abuse, mutable hop state, identifier
  correlation, traffic analysis, crash rollback, and implementation/supply-
  chain risks remain open.

Document creation does not close a gate. Current evidence state is:

| Gate | Wave 0 evidence | State |
| --- | --- | --- |
| SG-001 | initial scoped threat model, attacker capabilities, goals, residuals, verification, and blockers documented | open pending independent review and accepted scope |
| SG-002 | credential/discovery/session candidates and required contracts documented | open pending EXP-005/017, selection, vectors, and recovery review |
| SG-003 | authority, lifecycle, MLS/alternative, and partition candidates documented | open pending EXP-006 and selected policy/construction |
| SG-004 | field coverage, admission, duplicate, hop, metadata, and DoS requirements documented | open pending EXP-002/007/016/018 and selected construction |
| SG-005 | algorithm-independent poisoning, metric, Sybil, wormhole, and degradation requirements documented | open pending Agent 3 profile and adversarial evidence |
| SG-006 | protected-record, associated-context, replay, failure, and vector requirements documented | open pending standard profile, EXP-006/019, and public vectors |
| SG-007 | required principal/action/grant binding and malicious-member limits documented | open pending EXP-008 and arbitration profile |
| SG-008 | required channel/grant/stream/media binding and non-persistence boundary documented | open pending protected media/audio profile and artifact audit |
| SG-009 | implementation requirements only | blocked because production implementation is not authorized |
| SG-010 | no external review | open and blocks Protocol v1.0 |

## Claim policy

Until SG-001 through the relevant gate are complete, documentation and UI use
precise phrases such as "design target" or "designed for endpoint-only protected
payloads" and do not claim reviewed end-to-end encryption, anonymity,
unlinkability, forward secrecy, or post-compromise security. The
`wave1-sim-v0.1` `OpaqueEndpointPayload` is only unparsed fixture data and must
not be described as protected, encrypted, authenticated, or replay-safe.
