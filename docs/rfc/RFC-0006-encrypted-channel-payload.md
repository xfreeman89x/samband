---
rfc: "0006"
title: Encrypted Channel Payload
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-02
target: Protocol v0.x
requires:
  - Agent 4 Security review
  - Agent 1 Protocol review
supersedes: []
superseded_by: null
---

# RFC-0006: Encrypted Channel Payload

## Summary

This RFC will define how authorized endpoints are intended to protect private
channel payloads so a reviewed future profile can prevent non-member relays
from recovering or undetectably modifying their content. It
separates payload protection from transport security, peer authentication, and
channel authorization. No cryptographic construction is selected here.

## Status and authority

Draft and non-normative. The project intends end-to-end confidentiality, but no
implementation may claim end-to-end encryption until Agent 4 has approved the
identity, membership, key, algorithm, nonce, authentication, and replay design.
Agent 4's Wave 0 review defines candidates and mandatory properties but does
not approve a construction or close SG-006.

## Motivation

The iconic Samband path crosses a foreign relay. Link encryption alone ends at
that relay and is insufficient. A protected payload must remain opaque across
multiple transports while binding the right channel context, sender/epoch state,
freshness, and relevant relay-envelope metadata without leaking unnecessary
information.

## Goals

- define a design target for channel payload confidentiality and integrity
  between authorized endpoints across foreign relays;
- use standard, reviewed cryptographic constructions;
- coordinate keys with channel membership changes and compromise assumptions;
- prevent nonce misuse, replay, cross-channel substitution, and downgrade;
- make failure behavior and metadata exposure explicit;
- support streaming/fresh media without persisting content.

## Non-goals

- invent cryptographic primitives;
- treat transport security as channel security;
- hide all traffic timing, size, or topology by unsubstantiated claim;
- solve membership authorization independently from RFC-0003;
- define audio codec/framing or PTT arbitration.

## Security-layer separation

The accepted specification must distinguish:

1. transport/link protection, if any;
2. node/session authentication;
3. channel membership and authorization;
4. end-to-end payload confidentiality/integrity;
5. replay protection and duplicate suppression;
6. optional metadata-protection techniques.

Success in one layer cannot be cited as success in another.

## Protocol-facing protected-payload boundary

RFC-0004 carries one `OPAQUE_ENDPOINT` payload whose relays preserve and do not
parse. For a locally eligible packet, the endpoint passes the opaque bytes plus
the exact Agent 4-approved associated semantic context to the channel-security
boundary. Relays never invoke this boundary and need no channel keys or
membership state.

The future boundary must provide, without exposing partial plaintext or
provisional context before all security gates accept:

| Result | Protocol consumer |
| --- | --- |
| open/authentication disposition | determines whether inner parsing is permitted |
| security-replay disposition | rejects replay independently from RFC-0004 duplicate state |
| channel context | selects the authorized endpoint channel state without making it relay-visible by default |
| authenticated principal/sender context | identifies the protected-record sender; distinct from payload-carried action subject, grant owner, or affected member |
| security epoch/context | binds subsequent inner state without defining its representation here |
| accepted inner bytes | parsed only after all required security checks accept |

Agent 4 may refine or combine these logical outputs when selecting a standard
construction. Authentication/open and replay are logically distinct verdicts,
not necessarily separate calls or a mandated internal cryptographic order. No
plaintext or context leaves the boundary until both accept; observable accept/
reject, replay state, and context-binding behavior remain testable across
implementations.

The security profile must receive an unambiguous representation of every outer
semantic and classify it as link-local, forwarding-immutable, hop-mutable, or
transport-local. The endpoint protection or a separate origin proof must bind every
immutable element whose substitution affects delivery, duplicates, scheduling,
interpretation, or authorization: the exact envelope/profile pair, outer
class/type, origin routing context, packet identity, routing directive/target,
traffic treatment, payload length/content relationship, and applicable
extension identifiers/criticality/lengths/values. EXP-002 must establish
canonicalization and unknown-extension preservation before exact coverage can
be frozen.

Remaining hop limit is mutable and needs a separate reviewed admission/update
contract; it cannot simply be unchanged endpoint associated data. This RFC
does not add a signature, authentication tag, nonce, key identifier, algorithm
field, or origin hop-limit copy merely to make an envelope schema complete.

Forwarding duplicate suppression, cryptographic replay rejection, channel
operation idempotence, and media staleness are separate decisions. Rewrapping
the same protected operation under a new outer packet identity does not make it
fresh or authorized.

## Required construction properties

Agent 4 must define algorithm agility without downgrade, key identifiers or
epochs, sender/context binding, nonce strategy, authenticated associated data,
payload length limits, replay windows, rekey/rotation, member removal behavior,
compromise limits, secret storage, and erasure expectations.

Whether relays validate a separate outer origin proof before forwarding, and
the exact representation covering the required immutable fields, remain
EXP-002/018 and joint Agent 1/4 questions.

Agent 4 exclusively owns primitive/construction selection, key/nonce/tag sizes,
algorithm agility and downgrade behavior, sender/epoch domains, associated-data
coverage, replay windows, rekey/removal, forward/post-compromise claims,
padding/cover traffic, failure-oracle detail, secret storage, and erasure. No
real v0.x endpoint profile can claim protection or accept inner actions until
SG-001, SG-003, and SG-006 are satisfied for its scope.

## Agent 4 candidate design

MLS RFC 9420/9750 is the leading standardized EXP-006 candidate. It provides
authenticated group epochs, membership operations, encrypted application
messages, per-sender ratchets, and forward-secrecy/post-compromise mechanisms.
It does not automatically define Samband's credential trust, add/remove
authority, decentralized Delivery Service, concurrent-commit tie-break,
partition/reinitialization policy, recipient routing, metadata mitigation,
resource bounds, or PTT authorization. No MLS profile/suite is selected.

Pairwise HPKE fan-out is a cost/scale comparator and possible standard
bootstrap component. HPKE alone is not group membership, sender authorization,
replay, forward secrecy, post-compromise recovery, or epoch convergence. A
home-grown HPKE-plus-AEAD sender-key protocol is prohibited.

SFrame RFC 9605 is a later media-framing candidate only. It delegates key
management and receiver anti-replay, exposes its KID/counter header, and does
not authenticate one sender against other holders of the same symmetric key.
It cannot replace RFC-0003, this protected-record contract, or PTT action
authorization. Its header remains inside `OPAQUE_ENDPOINT` by default.

The complete security goals, trust assumptions, relay/member knowledge,
partition behavior, compromise consequences, revocation limits, lifecycle,
and unresolved questions are in
[`channel-security.md`](../security/channel-security.md).

## Security replay and authorization model

Every profile defines a non-wrapping, bounded replay domain scoped at least to
channel/group, epoch, authenticated sender/key context, and record generation.
It also defines window/retention, maximum forward gap/work, reordering, sequence
exhaustion, old-epoch handling, restart/rollback recovery, and erasure. Packet
identity never supplies security freshness.

The logical processing requirement is bounded header/key-context selection,
optional non-authoritative replay precheck, authentication into provisional
private storage, atomic authenticated replay check-and-commit, then plaintext/
context release. Authentication/open and replay can be combined internally but
both verdicts remain observable for conformance. Unauthenticated input never
advances replay state.

The proposed v0.x policy is consume-on-authenticated-record: once replay state
is atomically committed, later semantic decode, critical-extension,
authorization, or state-precondition failure does not roll it back. A semantic
retry uses a fresh protected record and preserves its separate operation ID.
This proposal requires joint Agent 1/Agent 4 review, SG-006, and vectors.

The authenticated sending principal remains distinct from an action subject,
membership target, PTT grant owner, or stream owner. Authorization covers the
complete decoded action, operation identity, principal role, subject
references, and permission under the current epoch/policy, and is bound to the
exact referenced grant/stream identifiers and state revision. It does not
assert that later semantic PTT/grant/stream preconditions hold. Those are
checked next against the same revision; authorization plus precondition/state
transition is atomic or revision-guarded. A verdict cannot be reused after the
guarded state changes.

## Failure and resource bounds

Invalid tags, unknown algorithms/epochs, replay, truncated payloads, excessive
lengths, missing keys, and state rollback must fail safely and within bounded
work. Authentication failure must not expose partial plaintext or detailed
oracle behavior to untrusted peers.

The profile also bounds candidate channel/key/epoch trials per packet,
authentication operations, replay entries, retained epochs/forks, and failure
responses. Unknown profiles/suites/credentials/keys, ambiguous selectors,
authentication failures, and replay normally collapse to a profile-pinned
local `(channel-security, SECURITY_REJECTED)` when finer detail would create an
oracle. No automatic transit response is sent.

## Privacy and metadata considerations

Encryption does not hide packet size, timing, route, traffic treatment, origin/
target correlation, or activity cadence. Security profile, channel, epoch,
sender/key, replay, PTT, stream, codec, and inner-type data remain in the opaque
container by default. Padding, batching, aliasing, and cover traffic have
energy/latency/DoS costs and are not assumed. The initial field budget is in
[`relay-security.md`](../security/relay-security.md); EXP-007 must measure it.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| MLS RFC 9420/9750 application profile | standardized group state, sender ratchets, private application records, FS/PCS mechanisms | AS/DS realization, linear-epoch partition conflict, policy, metadata, and resource fit | EXP-006 bounded prototype |
| pairwise HPKE fan-out with separate standardized group state | recipient isolation and useful small-group baseline | linear bandwidth; HPKE lacks membership, replay, FS/PCS, and convergence | EXP-006 comparator only |
| sender-key/media construction supplied by a reviewed standard | efficient per-sender realtime protection | key distribution, replay, removal, sender auth, and PCS obligations | identify complete standard; EXP-006 |
| SFrame with reviewed external group key management | standardized transport-independent media framing | no built-in key management/receiver replay or per-sender auth against key holders; visible header if exposed | later EXP-006/007/013 comparison |
| static shared channel key | minimal overhead | broad compromise, sender impersonation, removal, and nonce-domain failures | insecure baseline only; not a general profile |

No alternative or primitive is selected.

## Wire and versioning impact

The protected payload may need version/algorithm context, epoch/sender context,
nonce or sequence information, ciphertext, and authentication data. Whether
these live inside or alongside the opaque relay payload, and which are visible,
requires joint Agent 1/Agent 4 design.

The default protocol boundary keeps security version/algorithm, channel,
epoch/sender, nonce/sequence, and authentication data inside the opaque endpoint
container unless Agent 4 demonstrates that pre-open recipient selection or
relay admission requires a bounded visible field. Any exposure requires
EXP-007. Unknown security-critical versions, algorithms, or extensions fail
closed and cannot be downgraded to an older profile.

This security boundary is distinct from optional semantic evolution inside a
known CHANNEL/PTT/AUDIO message. Agent 1 may define a bounded semantic element
as ignorable only when it cannot affect identity, context, authority,
authorization, replay/freshness, state preconditions, or emitted actions.
Agent 4 must nevertheless bind that element's presence and criticality under
future integrity coverage so it cannot be injected, stripped, or changed from
critical to optional. Protection-format versions, algorithms, epochs,
credentials/proofs, authentication, and replay fields always remain
`channel-security`-owned; failure-oracle behavior is part of Agent 4 review.

## Test-vector and interoperability plan

After construction selection, use published synthetic keys to cover valid
protection/opening, wrong channel/sender/epoch/context, nonce boundaries,
replay, tampering at every field, truncation, unknown algorithms, removal/rekey,
and deterministic standard vectors where safe. Randomized encryption vectors
must fix all randomness explicitly.

Each security vector must pin the standard/profile/suite and source revision,
separate public and secret synthetic inputs, state every randomness input,
encode exact bytes, declare authenticated outer context and pre/post replay/
epoch state. Authentication/open or replay negatives assert that no plaintext
leaves the security boundary. Decode, critical-extension, authorization, and
state-precondition negatives may use private bounded decoded bytes but assert
no application plaintext/action delivery or inner state mutation; replay-state
consumption follows the profile's pinned consume-on-authenticated-record rule.
Standard published vectors are imported or traceably adapted rather than
silently rewritten. A profile-aware runner, not JSON Schema alone, validates
cryptographic/state semantics.

Before construction selection, protocol semantic vectors inject named
synthetic outcomes for outer admission, channel open, security replay, and
action authorization. They exercise processing order: open/replay rejection
causes no plaintext exposure, while later decode/authorization rejection causes
no application delivery or inner state mutation. They are explicitly non-
cryptographic/non-production and contain no placeholder crypto bytes.

## Migration and rollout

No protected-payload security profile exists to migrate today. A future change
to construction, algorithm, key/epoch/nonce/replay semantics, associated data,
metadata exposure, or failure behavior creates a new exact profile and reviewed
transition. Unknown security-critical profiles/algorithms fail closed. There is
no fallback to plaintext, transport-only security, an older construction, or a
synthetic simulator adapter. Relays do not decrypt/re-encrypt or translate
endpoint security profiles.

## Open questions

- Which standard construction meets offline group PTT requirements?
- What forward secrecy, post-compromise security, and removal guarantees are
  feasible without continuous connectivity?
- How are multi-sender nonce domains made misuse-resistant?
- Which relay-envelope fields are authenticated end to end?
- What channel/epoch metadata must be visible for recipient selection?
- How are lost key updates handled without storing missed audio?
- What padding or size-hiding policy is justified by measured costs?

## Review requirements

- [x] Agent 4 initial threat, standard-candidate, associated-context, replay,
  lifecycle, failure, and metadata requirements recorded in this revision.
- [ ] Agent 4 construction/suite selection and SG-006 closure after evidence.
- [x] Agent 1 opaque-payload interface, processing, replay separation,
  versioning, and synthetic-vector review recorded in this revision.
- [ ] RFC-0003 membership lifecycle reconciled.
- [ ] RFC-0004 associated metadata reconciled.
- [ ] Standard vectors and negative cases reviewed.

## Acceptance blockers

- the initial threat and candidate membership/key architecture exist, but
  SG-001/003/006 remain open;
- MLS is analyzed as a lead candidate but no standard profile/suite is selected;
- exact nonce/replay/epoch/rollback behavior is unresolved;
- the metadata/failure requirements are documented but unmeasured;
- EXP-002, EXP-006, EXP-007, EXP-018, and EXP-019 evidence does not exist.

## Decision record

- 2026-09-01: Agent 1 revision defined the opaque endpoint/security interface,
  kept channel/security context non-relay-visible by default, and separated
  forwarding duplicate, security replay, operation idempotence, and staleness.
  RFC remains Draft pending Agent 4 and EXP-006/EXP-007.
- 2026-09-02: Agent 4 documented MLS, HPKE, and SFrame boundaries; required
  complete immutable outer-context binding, principal/subject separation,
  bounded key selection, atomic consume-on-authenticated-record replay, failure
  behavior, and partition/compromise limits. No construction/suite was selected
  and no encryption claim is authorized.

## References

- [`RFC-0003`](RFC-0003-channel-identity-and-membership.md)
- [`RFC-0004`](RFC-0004-relay-envelope.md)
- [`review-gates.md`](../security/review-gates.md)
- [`channel-security.md`](../security/channel-security.md)
- [`relay-security.md`](../security/relay-security.md)
- [`threat-model.md`](../security/threat-model.md)
