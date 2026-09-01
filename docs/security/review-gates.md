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

## Claim policy

Until SG-001 through the relevant gate are complete, documentation and UI use
precise phrases such as "design target" or "protected synthetic payload" and do
not claim reviewed end-to-end encryption, anonymity, unlinkability, forward
secrecy, or post-compromise security.

