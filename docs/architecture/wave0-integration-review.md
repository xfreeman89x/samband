# Wave 0 Integration Review

Date: 2026-09-02

Review authority: Agent 0 — Principal Architect / Maintainer, integrating the
first-pass Protocol, Routing, and Security bodies of work.

## WAVE 0 INTEGRATION STATUS

**Integrated for a bounded experimental simulation wave.** The architecture,
Protocol Draft, Routing research plan, and Security requirements now expose one
coherent experimental boundary. No RFC is Accepted, no security gate is closed,
no stable wire format exists, and no production implementation is authorized.

The explicitly versioned
[`wave1-sim-v0.1` profile](../../protocol/spec/v0x-simulation-profile.md)
authorizes only deterministic, non-production, non-security simulation and a
narrow experimental core. It exists to generate evidence for unresolved
decisions; it is not Protocol v1, a production route, or a cryptographic profile.

## GIT / WORKTREE STATUS

The pre-integration snapshot was inspected before editing and refreshed from
`origin`:

| Item | Observed state |
| --- | --- |
| current worktree | repository root on `main`, clean before integration |
| current commit | `3fe9704a87e3c78f999b66e4546e2ae2b97efebb` — `docs(protocol): define Samband experimental v0.x model` |
| upstream | `origin/main` at `01e72954be3e555cf316422747c5404ac1611f06` |
| divergence | local `main` ahead 1, behind 0 |
| Git operation | no merge, rebase, cherry-pick, revert, or bisect in progress |
| protocol worktree | `samband-agent-protocol`, clean at `01e7295`, tracking `origin/agent/protocol` |
| security worktree | `samband-agent-security`, clean at `01e7295`, tracking `origin/agent/security` |
| architect branch | `agent/architect` at `f25ed485f7c41f0911dbcbebd1d8717144a9c7db`, matching its remote |

The local commit contains the Protocol, Routing, and Security first-pass files
in one commit. Their logical provenance is retained in RFC decision records,
security review records, and research ownership. There was no uncommitted agent
output or divergent worktree state to recover, so no branch normalization,
pull, merge, rebase, stash, reset, or checkout was performed. This integration
review remains an uncommitted working-tree change until the user chooses a Git
action.

## CROSS-AGENT CONFLICTS FOUND

| ID | Conflict | Evidence | Disposition |
| --- | --- | --- | --- |
| W0-C01 | The Draft specification prohibited every forwarding egress on the ingress transport attachment, while Routing models multiple peer links on one attachment and shared-medium emissions. | [`v0.x routing contract`](../../protocol/spec/v0x-experimental.md#routing-contract), [`RFC-0005 routing output`](../rfc/RFC-0005-mesh-routing.md#routing-output-contract), and the former attachment-only contract in [`FORMAT.md`](../../protocol/test-vectors/FORMAT.md#draft-semantic-outer-fixture-profile) | Resolved at the model level: suppress exact ingress peer-link unicast, not the whole attachment. |
| W0-C02 | RFC-0004/spec treated a distinct origin routing context as universally mandatory, while RFC-0005/EXP-007/016 kept its necessity open for different routing candidates. | [`RFC-0004 packet identity`](../rfc/RFC-0004-relay-envelope.md#packet-identity-and-duplicate-suppression), [`RFC-0005 open questions`](../rfc/RFC-0005-mesh-routing.md#open-questions), and [`routing metadata analysis`](../research/routing-candidate-evaluation.md#minimum-relay-metadata) | Reconciled as a profile-supplied duplicate scope. `wave1-sim-v0.1` pins a synthetic origin context without making it universal. |
| W0-C03 | RFC-0007 and RFC-0008 used unqualified “session loss/change” despite separate one-hop peer sessions and endpoint channel/security contexts. | [`RFC-0007 state machine`](../rfc/RFC-0007-ptt-arbitration.md#proposed-abstract-state-machine), [`RFC-0008 stream semantics`](../rfc/RFC-0008-audio-transport.md#proposed-stream-semantics), and [`identity domains`](identity-domains.md#domain-registry) | Resolved by naming the endpoint channel/arbitration/security context. One-hop session loss is a routing event unless the selected profile explicitly makes it terminal after bounded recovery. |
| W0-C04 | Routing freshness text required bounded high-water/tombstone state but appeared to promise permanent rejection after all recognition state was evicted. | [`RFC-0005 route freshness`](../rfc/RFC-0005-mesh-routing.md#route-freshness-and-restart) and [`routing freshness requirements`](../research/routing-candidate-evaluation.md#freshness-domains) | Resolved as an explicit profile choice: retain bounded issuer/incarnation admission state, require a fresh authenticated incarnation/session, or admit and measure stale resurrection. Forgotten state cannot provide permanent recognition. |

No other direct contradiction was found. The remaining differences are
deliberately open choices, evidence gaps, or security gates and are classified
below rather than silently decided.

## CONFLICTS RESOLVED

- Forwarding restrictions now apply to the exact ingress directional peer link,
  while a candidate may explicitly allow another peer on the same attachment or
  a shared-medium emission with bounded listener and cost accounting.
- Duplicate scoping is an exact-profile responsibility. The simulation profile
  uses a synthetic origin routing context; no universal wire field is frozen.
- PTT/audio teardown refers to the precise endpoint context, not arbitrary
  one-hop route churn.
- Bounded freshness state no longer implies impossible recognition after all
  recognition state is discarded.
- Routing identity versus privacy is reconciled semantically by separating
  credentials, discovery, peer sessions, routing origins/targets, channel
  principals, action subjects, and local abuse scopes. Concrete values remain
  evidence-blocked.

## CONFLICTS STILL OPEN

These are open design choices, not unresolved textual contradictions:

- whether a production routing profile carries a distinct origin routing
  context, derives duplicate scope from another admitted context, or uses a
  different bounded scope;
- the routing target model, candidate family, metrics, tie-breaks, no-route
  policy, numeric limits, and claim-freshness commit policy;
- peer-session, outer-envelope, route-claim, group membership, protected-record,
  and replay constructions;
- malicious-relay enforcement of mutable hop state;
- the measured relay-visible metadata budget and whether traffic treatment is
  worth its activity leakage;
- PTT authority/arbitration and all production audio/media choices.

## WAVE 0 INTEGRATION MATRIX

The classification describes the most restrictive unresolved part of each
contract. A row may still contain a smaller simulation-ready semantic subset.

| Shared contract | Classification | Integrated finding |
| --- | --- | --- |
| Samband layering | `CONSISTENT` | The shared transport mesh remains distinct from private channels; endpoint payloads stay opaque to relays. |
| Node identity domains | `CONSISTENT` | Domain separation is established architecturally; it selects no credential or identifier construction. |
| Discovery identity | `SECURITY BLOCKED` | The short-lived, non-authoritative handle role is clear; rotation, collision, binding, and privacy evidence remain open. |
| Routing identity | `EXPERIMENT BLOCKED` | Origin, target, issuer, and quota contexts are separate; their necessity, stability, binding, and linkability need EXP-005/007/016/018. |
| Session identity | `SECURITY BLOCKED` | One-hop scope and non-transferability are clear; credential assurance and handshake/record construction remain open. |
| Channel identity | `SECURITY BLOCKED` | Endpoint-only channel context is required, but its construction, selectors, and epoch binding are unselected. |
| Channel membership | `SECURITY BLOCKED` | Authority, add/remove/leave, partition conflict, rejoin, and standardized group-security profile remain open. |
| Relay envelope | `EXPERIMENT BLOCKED` | The logical simulation envelope is usable; wire encoding, exact fields, outer admission, and numeric limits are not selected. |
| Outer metadata | `EXPERIMENT BLOCKED` | A field-by-field inventory exists; visibility and mitigations await EXP-007 and candidate routing evidence. |
| Packet identity | `EXPERIMENT BLOCKED` | Its duplicate-only role and preservation are coherent; generation, collision, restart, linkability, and binding remain open. |
| Duplicate suppression | `EXPERIMENT BLOCKED` | The admitted first-effect rule is coherent; no-effect insertion, rushing, partial fanout, retention, and saturation await EXP-016. |
| Hop-limit semantics | `CONSISTENT` | Honest-node local-delivery/decrement behavior is simulatable; numeric values and malicious-relay protection remain security/experiment blocked. |
| Capabilities | `EXPERIMENT BLOCKED` | Full replacement lifecycle is a coherent baseline; registry, bounds, authentication, deltas, chatter, and route impact await EXP-015/017/018. |
| Routing claims | `SECURITY BLOCKED` | Issuer, subject/target, provenance, freshness, and truth are separated; no real admission construction exists. |
| Replay domains | `CONSISTENT` | Mesh duplicates, claim freshness/replay, protected-record replay, operation idempotence, and media staleness are explicitly different. Their mechanisms remain open. |
| Protected endpoint records | `SECURITY BLOCKED` | The open/replay/context/authorization interface is coherent, but no construction, suite, nonce, key, or rollback policy is selected. |
| PTT control | `EXPERIMENT BLOCKED` | Grant-gating and abstract state are usable for later synthetic tests; authority, arbitration, partitions, fairness, and timing remain open. |
| Audio control | `DEFERRED TO LATER PROFILE` | Stream start/end semantics depend on a selected channel/PTT/security profile and are outside Wave 1. |
| Audio media | `DEFERRED TO LATER PROFILE` | Codec, framing, freshness, jitter/FEC, protection, and physical evidence are unavailable. |
| Version negotiation | `PROTOCOL BLOCKED` | Exact-pair selection is coherent, but bootstrap bytes, retry/collision, transcript binding, and downgrade protection are unresolved. |
| Compatibility pair | `CONSISTENT` | Envelope format and protocol profile are exact, independent, opaque axes; no released identifiers exist. |
| Error/disposition model | `CONSISTENT` | Layered local outcomes are shared across Draft spec and vectors; selected profiles must still pin security failure coalescing and state consumption. |
| Resource bounds | `EXPERIMENT BLOCKED` | Finite work/state is invariant; exact maxima and deterministic overload behavior are candidate/profile evidence. |
| Ingress forwarding model | `CONSISTENT` | Attachment, immediate-peer session, and directional peer link are distinct; exact-link bounce is prohibited while same-attachment/shared-medium behavior is profile-defined. |

## IDENTITY DOMAIN MODEL

The authoritative architecture registry is
[`identity-domains.md`](identity-domains.md). Samband requires distinct semantic
domains for:

- Credential Identity (the credential-bearing Node Identity role);
- Discovery Handle;
- Session-Exchange Identity;
- Admitted Peer-Session Context;
- Origin Routing Context;
- Routing Target Identifier;
- Packet Identity;
- Channel Context Identifier;
- Channel Principal;
- Action Subject;
- Endpoint Operation Identity;
- PTT Request / Grant Identity;
- Media Stream / Sequence Context;
- local human labels.

Each registry row states lifetime, scope, audience, stability, linkability,
authentication, and relay visibility. Packet Identity remains a forwarding
duplicate-correlation token, never a principal. An authenticated principal and
action subject remain distinct because an authorized administrator or decision
issuer may act about another member or owner.

The simulator must use typed synthetic contexts. A generic
`SyntheticNodeIdentity` is permitted only as a local topology label and cannot
stand in for a credential, discovery handle, session, route, channel principal,
or action subject.

## RELAY METADATA MODEL

The labels below describe relay visibility in the current experimental design,
not approved production wire fields.

| Candidate relay-visible item | Budget decision | Reason and constraint |
| --- | --- | --- |
| exact envelope/profile compatibility identifiers | `REQUIRED` | Needed to select exact processing semantics; bind to the admitted context and never infer compatibility from ordering. |
| coarse outer class/type | `REQUIRED` | Needed for link/mesh/opaque dispatch; keep inner channel/PTT/audio family hidden. |
| packet identity | `REQUIRED` | Needed for bounded mesh duplicate suppression; never identity, authentication, or replay proof. |
| duplicate/origin routing scope | `PROVISIONAL` | The simulation pins a synthetic origin context; production necessity and correlation cost need EXP-007/016. |
| routing directive/target | `PROVISIONAL` | Candidate-dependent; never a raw credential, human label, membership proof, or plaintext channel ID. |
| remaining hop state | `REQUIRED` | Provides the current Draft safety bound; its adversarial protection remains unresolved. |
| traffic treatment | `AVOID IF POSSIBLE` | Retain only if EXP-003/007 proves a coarse scheduling/freshness hint materially necessary. |
| payload length | `REQUIRED` | Needed for bounded framing/allocation; padding or buckets require measured cost. |
| outer extension identifiers/shape | `AVOID IF POSSIBLE` | Keep the registry minimal; preserve and integrity-protect criticality/presence at the applicable scope. |
| direct capability information | `PROVISIONAL` | Only an admitted immediate peer receives a coarse session-scoped snapshot; no raw battery, OS, thermal, device, or channel inventory. |
| channel identity, roster, membership proof, epoch | `ENDPOINT ONLY` | No generic relay function needs them. |
| authenticated channel principal or action subject | `ENDPOINT ONLY` | Available only after endpoint security/replay admission. |
| PTT request, grant, owner, term, subtype | `ENDPOINT ONLY` | Relay scheduling cannot infer authorization or floor state. |
| stream, codec, sender/key ID, media sequence | `ENDPOINT ONLY` | Relays need no media internals; size/timing leakage remains measurable. |

The unavoidable observational surface also includes transport addresses, timing,
direction, cadence, retry patterns, and link behavior. Scoped identifiers do not
justify anonymity or unlinkability claims against those signals or colluding
observers.

## PROCESSING PIPELINE

The canonical logical pipeline is:

```text
transport ingress, byte/rate/buffer bounds
    -> bounded framing/prefix and declared-length validation
    -> exact compatibility and structural validation
    -> peer-session and outer-envelope security admission
    -> routing/capability claim authority and freshness admission, if applicable
    -> authoritative mesh duplicate lookup
    -> independent local-delivery and bounded forwarding decisions
    -> resource reservation
    -> atomic duplicate/claim/action commit required by the exact profile
    -> local opaque dispatch and/or peer-link-aware forwarding
    -> endpoint protected-record authentication/open, for local delivery only
    -> cryptographic replay admission and atomic replay commit
    -> release of principal/context/plaintext to bounded inner decode
    -> family/type/critical-extension validation
    -> complete action authorization with principal/subject separation
    -> semantic precondition check and atomic or revision-guarded state action
    -> permitted application event and bounded redacted observability
```

Cheap stateless rejection can occur before expensive work, but untrusted input
cannot mutate authoritative state. Outer security and applicable claim admission
precede the authoritative duplicate cache. Duplicate lookup through reserved
observable effects is atomic for one key. The exact claim-freshness consumption
point remains profile-specific and must never roll back after an observable
accepted effect.

At the endpoint, protected-record authentication/open and cryptographic replay
are logically distinct even if a standard construction combines their mechanics.
No provisional plaintext, principal, channel, or security context becomes
externally observable before both accept. Local endpoint rejection never undoes
an independently eligible relay action.

## MUTABLE HOP STATE AND INTEGRITY

Every exact profile classifies outer data as follows:

| Scope | Examples | Required property |
| --- | --- | --- |
| forwarding-immutable | exact pair, class/type, duplicate scope where carried, packet identity, routing directive/target, treatment, payload length/content, immutable extensions | Endpoint protection or a separate origin proof binds every semantic whose substitution affects delivery, duplicates, scheduling, interpretation, or authorization. |
| hop-mutable | remaining hop limit | The profile defines received-value admission, authorized decrement/re-protection, permitted transition, and failure. |
| session-local | immediate peer, session assurance, direct capability snapshot, link-level sequence/replay state | Valid only for one admitted session and never transferred across a relay or reconnect. |
| transport-local | attachment, directional peer link, next hop, transport framing and measurements | Never generic envelope fields or transferable authority. |

Current simulation can prove only that honest relays decrement once and enforce a
syntactic maximum. It cannot claim that a malicious relay cannot reset,
over-decrement, re-originate, or drop. EXP-018 compares reviewed admission
models; no signature chain, hash chain, path proof, or new construction is
invented here.

## CAPABILITY LIFECYCLE

The reconciled experimental baseline is a complete snapshot bound to one peer
session and exact pair:

1. first valid snapshot establishes a finite non-wrapping generation high-water
   mark;
2. a higher generation atomically replaces all capability entries;
3. identical canonical content at the current generation is idempotent and does
   not refresh receipt-relative expiry;
4. changed same-generation content conflicts; lower generation is stale;
5. expiry withdraws entries while retaining the generation high-water mark;
6. after expiry, only a higher generation can establish new state;
7. a higher snapshot omitting relay willingness withdraws it immediately;
8. heartbeat does not refresh or resurrect capabilities;
9. peer-session closure clears the session-scoped state.

Local safety policy stops accepting new transit work immediately. A direct peer
then applies admitted snapshot withdrawal/expiry. Any remote route consequence
is a distinct routing claim with separate issuer, freshness, and bounded
propagation; no instantaneous network-wide withdrawal is promised.

## ROUTING CLAIM AUTHORITY

The security/protocol boundary provides authenticated issuer, subject/target,
provenance, freshness, and exact context. Routing decides how admitted claims
influence routes. These statements remain false:

```text
authenticated assertion == truthful route
authenticated peer == target owner
authenticated metric == measured link quality
authenticated adjacency == symmetric reachability
authenticated willingness == successful forwarding
```

Only a local admitted transport/session event creates a one-hop adjacency. An
advertiser may replace only its own authorized claim slot and cannot withdraw a
target globally. Locally measured, immediate-peer self-asserted, transit-
aggregated, and separately origin-authenticated metrics retain distinct
provenance. Sybils, rushing, blackholes, selective forwarding, and wormholes
remain adversarial cases even after authentication.

## MEMBERSHIP AND FOREIGN RELAY

The Samband invariant survives integration:

```text
Alice, channel member -> Bob, relay only -> Carol, channel member
```

Bob may validate and forward an eligible outer packet without channel
membership, a channel credential, a channel key, membership proof, channel
identity, or endpoint plaintext. Failure to open the endpoint payload locally
is not a forwarding predicate. Real confidentiality/integrity against Bob is
only a future profile target; current simulation uses `OpaqueEndpointPayload`
and makes no encryption claim.

## SHARED CONTRACTS ESTABLISHED

The detailed classifications are in
[`shared-contracts.md`](shared-contracts.md). Established architecture is
limited to SC-001 through SC-004:

- transport mesh and private-channel separation;
- foreign relay independence from membership/plaintext;
- the abstract one-hop transport boundary, while its exact portable API remains
  unresolved; and
- identity-domain separation and non-transferability only, with no established
  representations, bindings, authentication, authority, or privacy property.

Other stable project rules still constrain all work, including specification
authority, ephemeral audio, prohibited audio/plaintext persistence, finite
work/state, and safe observability. This review does not promote their concrete
wire, security, routing, PTT, media, or observability mechanisms.

## SHARED CONTRACTS EXPERIMENTAL

`wave1-sim-v0.1` establishes only these simulation contracts:

- typed synthetic identity contexts and synthetic admissions with
  `securityClaim: false`;
- exact non-wire compatibility-pair labels;
- logical outer packets with opaque endpoint payloads;
- ingress attachment/session/directional-link separation and bounded
  peer-unicast/shared-medium actions;
- honest-node hop-limit behavior;
- profile-pinned duplicate scope and atomic processing, with unresolved
  no-effect policies exposed as experiment variants;
- the full-snapshot capability lifecycle;
- independent local-delivery/forwarding decisions;
- candidate-specific routing profiles behind one experimental interface;
- virtual time, named seeded randomness, layered outcomes, finite bounds, and
  deterministic safe traces.

Wire encoding, real identity/session admission, outer/claim security, channel
membership, payload protection, PTT, audio, gateways, physical transports, and
production numeric limits remain Draft or unresolved.

## RFC RECONCILIATION

No RFC advances to Discussion or Accepted merely because Wave 0 integration is
complete.

| RFC | Integrated status | Primary remaining blocker |
| --- | --- | --- |
| RFC-0001 | **Draft — coherent enough for experimentation** | real peer admission, metadata, capability bounds, and selected routing review |
| RFC-0002 | **Draft — blocked by security** | credential/session construction, discovery privacy, recovery, and routing-identity evidence |
| RFC-0003 | **Draft — blocked by security** | channel authority, membership/group construction, partition/removal, and rollback |
| RFC-0004 | **Draft — further design required** | encoding, duplicate-scope selection for real profiles, no-effect policy, outer/hop security, metadata, and bounds |
| RFC-0005 | **Draft — blocked by experiment** | operating envelope, target, algorithm, catalog, metrics, numeric policies, and adversarial evidence |
| RFC-0006 | **Draft — blocked by security** | standard protected-record profile, key/nonce/epoch/replay/rollback, metadata, and public vectors |
| RFC-0007 | **Draft — blocked by experiment** | authority/arbitration, propagation, partitions, fairness, timing, and abuse controls |
| RFC-0008 | **Draft — further design required** | deferred behind protected relay and PTT; codec/media/security/routing and physical evidence absent |

## RFCS READY FOR EXPERIMENTATION

- RFC-0001 layering, taxonomy, and full-snapshot capability semantics;
- RFC-0004 logical envelope, exact abstract pair, hop behavior, layered
  outcomes, processing order, and explicit duplicate-policy experiment surface;
- RFC-0005 routing interface, candidate families, target-model factorial,
  directed links, partitions, withdrawals, bounds, and scenario plan.

Only the subset pinned by `wave1-sim-v0.1` is implementable. Draft status and
all acceptance blockers remain.

## RFCS STILL BLOCKED

- RFC-0002, RFC-0003, and RFC-0006 are blocked by security construction and
  evidence.
- RFC-0004 remains blocked for a real wire/outer-security profile.
- RFC-0005 remains blocked for algorithm/target selection and SG-005.
- RFC-0007 remains blocked by PTT experiments and security/routing choices.
- RFC-0008 is deferred outside Wave 1 and blocked by channel/PTT/media evidence.

## SECURITY GATES STATUS

No gate closes in this review.

| Gate | Blocking RFC/contracts | Required experiment or review |
| --- | --- | --- |
| SG-001 | all security claims, all security-sensitive contracts, Protocol v1 | independent review and accepted threat-model scope/trust assumptions |
| SG-002 | RFC-0002; identity/session portions of SC-004, SC-007, SC-012 | EXP-005/017/019, selected credential and complete session/record profile, vectors, recovery and independent review |
| SG-003 | RFC-0003; SC-005 and prerequisites of SC-009/010/011 | EXP-006/007/019, selected authority/group construction, partition/removal policy and review |
| SG-004 | RFC-0004; SC-006/012 and related observability/vector contracts | EXP-002/007/016/017/018/019, selected outer/session/claim coverage, parser/amplification review |
| SG-005 | RFC-0005; SC-007/008 | Agent 3 exact candidate/profile, EXP-003/004/007/015/016/018 and adversarial review |
| SG-006 | RFC-0006 and any end-to-end-encryption claim; SC-009/security vectors | selected standard construction, EXP-002/006/007/018/019, public vectors and independent review |
| SG-007 | RFC-0007; SC-010 | EXP-008 and selected arbitration/security authority, replay/privacy/abuse review |
| SG-008 | RFC-0008/M5; SC-011 and non-persistence part of SC-014 | selected protected-media/audio profile, EXP-013, physical evidence and artifact audit |
| SG-009 | implementation releases, especially SC-015/016 | dependency/license/provenance/advisory, unsafe/FFI, storage and artifact review; not a blocker to isolated synthetic simulation |
| SG-010 | Protocol v1 and every v1-frozen contract | external review and closure of all release-blocking findings |

Until the relevant gates close, Samband uses phrases such as “design target,”
“designed for endpoint-only protected payloads,” or “synthetic admission with
`securityClaim: false`” only when precisely qualified. It never calls the
simulation payload protected or encrypted. It does not claim end-to-end
encryption, anonymity, unlinkability, forward secrecy, post-compromise
security, immediate revocation, or production security.

## EXPERIMENT DEPENDENCY GRAPH

The canonical question, evidence, owner, prerequisites, simulator role, and
decision unlocked for every EXP item are maintained together in
[`experiment-backlog.md`](../research/experiment-backlog.md). The integrated
dependency graph is:

```text
wave1-sim-v0.1
    +--> EXP-001 narrow Rust/core feasibility
    +--> EXP-004 operating envelope + preregistered traces/thresholds
    +--> EXP-005 identity rotation/binding --------+
    +--> EXP-007 metadata budget ------------------+
    +--> EXP-015 capability lifecycle -------------+--> exact candidate manifests
    +--> EXP-016 duplicate/no-effect policies -----+          |
                                                           EXP-003 routing comparison
                                                                    |
                                                                    +--> RFC-0005 selection evidence
                                                                    +--> EXP-008 PTT routing inputs
                                                                    +--> EXP-013 media routing inputs

EXP-002 encoding/canonicalization ----+--> RFC-0004 wire profile
EXP-017 peer session -----------------+--> SG-002/004 construction evidence
exact routing/admission candidates ---+--> EXP-018 malicious-relay admission evidence

EXP-006 group security ---------------+--> RFC-0003/0006 evidence --> EXP-008
EXP-006 + EXP-017 selected state -----+--> EXP-019 rollback/restart evidence

EXP-009 Android ----+
EXP-010 iOS --------+--> EXP-011 cross-platform direct transport
                    +--> EXP-012 physical relay cost
                    +--> EXP-014 physical MTU/fragmentation --> final EXP-002 bounds

EXP-003 + EXP-006 + EXP-008 + EXP-012 + EXP-014 --> EXP-013 audio profile evidence
```

The dependencies are gates, not a demand for sequential execution where work is
independent. In particular, EXP-005/007/015/016 can run in parallel with
EXP-004 preparation. EXP-003 result-bearing comparisons wait for the operating
envelope, thresholds, held-out traces, and exact candidate manifests to freeze.
EXP-018 runs only after exact synthetic claim/admission variants exist.

The RTE scenarios are shared test cases, not duplicate experiments:

- RTE-012 consumes EXP-016 duplicate-rushing policies;
- RTE-014 consumes EXP-018 malicious-claim/admission models;
- RTE-015 consumes EXP-015 withdrawal/flapping behavior;
- RTE-017 consumes EXP-005/007 identity and metadata evidence.

No EXP item was removed because each answers a distinct decision question.
Overlapping topology, resource, privacy, and adversarial measurements are
collected once through shared immutable traces and then referenced by the
applicable decision records.

## SAMBAND V0.X SIMULATION PROFILE STATUS

**AUTHORIZED: `wave1-sim-v0.1`, experimental simulation only.**

The profile authorizes:

- semantic objects rather than wire bytes;
- exact non-wire compatibility labels;
- preinstalled/synthetically admitted peer sessions;
- typed synthetic discovery/session/routing/channel contexts;
- `OpaqueEndpointPayload` with no protection claim;
- honest hop decrement and malicious-hop fault injection;
- profile-supplied duplicate scope, finite caches, and explicit no-effect policy
  variants;
- full replacement capability snapshots;
- separate attachment/session/directional-link ingress and peer-unicast/shared-
  medium egress actions;
- synthetic outer, claim, routing, channel-open, replay, and authorization
  verdicts with `securityClaim: false`;
- deterministic virtual time, named seeded randomness, explicit resource
  limits, and safe layered traces;
- multiple exact routing candidates without selecting a winner.

It excludes wire compatibility, real cryptography, credentials, production
routing, channel membership, positive security claims, PTT/audio, mobile
networking, gateways, and physical evidence.

## WAVE 1 AUTHORIZATION

Wave 1 may begin after the repository validators pass this integrated change.
The authorization is scoped to:

```text
narrow experimental Rust core
    + candidate routing modules
    + deterministic simulator and experiment harness
```

The work must identify `wave1-sim-v0.1` in its evidence. Discovering an
ambiguity pauses that behavior and returns it to RFC/experiment review; an
implementation cannot decide it silently. No Wave 1 result automatically
accepts an RFC, ADR, security gate, operating envelope, or routing winner.

## AGENTS UNBLOCKED

- **Agent 2 — Rust Core:** unblocked only for the narrow ADR-0004 experiment and
  profile-approved portable abstractions.
- **Agent 3 — Routing:** unblocked to implement and compare multiple exact
  candidate routing profiles behind the experimental interface.
- **Agent 5 — Simulator:** unblocked to build the deterministic directed-mesh,
  scenario, resource, and measurement harness.
- **Agent 4 — Security:** unblocked for synthetic-interface review and the
  scoped security/privacy experiments; not for production cryptography.
- **Agent 1 — Protocol:** unblocked to maintain Draft semantic vectors and
  review experiment-discovered ambiguity; not to freeze Protocol v1.

## AGENTS BLOCKED

- Agent 2 remains blocked from broad production crate/FFI scaffolding or an
  ADR-0004 acceptance claim.
- Agent 3 remains blocked from selecting or shipping a production routing
  algorithm.
- Agent 4 remains blocked from selecting/shipping cryptography without the
  required evidence and reviews.
- Agents 6 and 7 remain blocked from production Android/iOS mesh work; their
  later physical experiments do not alter Wave 1 semantics.
- Agent 8 remains blocked from realtime audio/PTT implementation.
- Agent 9 remains blocked from released compatibility/conformance claims,
  though later review of Draft vector tooling can proceed independently.

## EXACT NEXT MULTI-AGENT TASKS

### Agent 2 — Rust Core

1. Create only the smallest experimental crate structure needed by
   `wave1-sim-v0.1`; do not establish a production package graph.
2. Implement typed non-wire identity/context wrappers, logical envelope
   validation, hop behavior, profile-supplied duplicate scope, atomic duplicate
   reservation/commit hooks, capability snapshots, layered outcomes, injected
   monotonic time/randomness, and explicit finite configuration.
3. Expose candidate-policy interfaces for duplicate no-effect/partial-fanout and
   routing actions; do not choose those policies.
4. Consume the Draft semantic vectors and add malformed/boundary tests. No real
   key, signature, nonce, cipher, channel credential, or security claim enters
   the core.
5. Keep FFI to an isolated EXP-001 spike measuring ownership, callbacks,
   cancellation, errors, build, binary, portability, and fuzzing; do not publish
   a stable API.

### Agent 3 — Routing

1. Co-own EXP-004 preregistration with Agent 0: operating envelope, immutable
   traces, hard thresholds, seed/stopping/confidence rules, and supported versus
   stress ranges.
2. Publish exact candidate manifests for classic dissemination, reduced/gossip,
   distance-vector, link-state, and reactive profiles. Treat target model as a
   separate factorial dimension; evaluate a hybrid only after simpler candidates
   miss a named threshold.
3. Pin for each candidate its control catalog, issuer/subject/provenance model,
   target/local-delivery rule, freshness/restart, metrics/tie-break, queues,
   retries, fanout, duplicate commit matrix, loop behavior, numeric bounds, and
   safe observations.
4. Return only independent local-delivery and bounded peer-unicast/shared-medium
   actions. Never inspect channel payloads or platform types.
5. Co-own EXP-003/015/016/018 and report candidate results without selecting a
   winner before held-out evaluation and reviews.

### Agent 5 — Simulator

1. Implement a deterministic directed multigraph with multiple attachments,
   multiple sessions/links per attachment, virtual monotonic time, named seeded
   randomness, immutable event traces, and finite link/queue effects.
2. Model peer-unicast and shared-medium emissions, listener sets, correlated
   loss, bandwidth/accounting, churn, partitions, merge, and dynamic relay
   withdrawal without candidate-specific shortcuts.
3. Implement the common staged processing/resource ledger, including synthetic
   admissions, duplicate lookup/reservation/commit/action atomicity, and claim-
   state commit hooks.
4. Enforce every configured bound and generate `N`/`N+1` state/work/emission
   evidence. Emit safe deterministic semantic traces with ephemeral local
   handles only.
5. Build pilot scenarios while EXP-004 is prepared, but do not publish
   comparative conclusions before candidates, thresholds, and held-out traces
   are frozen.

### Agent 4 — Security

1. Review and freeze only the synthetic verdict interface: exact scope,
   non-transferability, ordering, principal/subject typing, and mandatory
   `securityClaim: false`.
2. Co-own EXP-005/007/015/016 and specify EXP-018 adversarial inputs for false
   claims, mutable hop state, rushing, Sybils, blackholes, selective forwarding,
   wormholes, and bounded verification work.
3. Review candidate manifests for claim/target admission, immutable/mutable
   coverage, freshness commit, metadata budget, and local quota continuity.
4. Audit Core/Simulator types and traces for universal-ID collapse, session-
   verdict transfer, payload/audio persistence, or accidental security claims.
5. Continue EXP-006 in parallel. Prepare EXP-017/019 only as isolated,
   hypothesis-pinned standards experiments; never use them as pseudo-
   cryptography in the simulation profile.

## Final decision

Wave 0 has produced enough shared semantic contract to begin evidence-generating
Wave 1 simulation without final production cryptography, wire encoding, routing,
PTT, or media. The authorization is deliberately narrow: it advances Samband by
making the unresolved questions executable while preserving every production
security, interoperability, routing-selection, and protocol-freeze gate.
