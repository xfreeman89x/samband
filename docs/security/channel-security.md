# Samband Channel Security

## Status

Wave 0 candidate architecture for SG-003, SG-006, RFC-0003, and RFC-0006.
No channel credential, authority policy, group protocol, cipher suite, nonce,
signature, payload encoding, or replay window is selected. Real CHANNEL, PTT,
and AUDIO actions remain blocked; only explicitly synthetic non-security
dispositions may be used by current protocol vectors.

Messaging Layer Security (MLS) is the leading standardized group-security
candidate for EXP-006, not an accepted Samband profile. Pairwise HPKE fan-out
and SFrame are useful comparison/component candidates but do not independently
solve Samband membership, authorization, replay, partition, and recovery.

## Security goals

- through the protocol, only authorized clients in an accepted channel epoch
  can recover protected endpoint content under the construction's stated
  compromise assumptions; endpoint compromise or member exfiltration remains
  outside that guarantee;
- authenticate the sending channel principal and authorize each decoded action
  before state mutation or application delivery;
- ensure Samband neither provisions a foreign relay with channel key/plaintext
  material nor requires channel membership to forward valid opaque traffic;
- bind protected content to its exact channel, epoch, sender, profile, message
  context, and security replay domain;
- prevent cross-channel, cross-epoch, cross-profile, sender, action, and outer
  metadata substitution;
- define add, remove, leave, rotation, compromise, restart, partition, merge,
  and rejoin without claiming instant global revocation;
- hide channel/member/PTT/media security metadata from relays by default and
  document unavoidable timing/size leakage;
- use only standardized constructions with public vectors and maintained
  implementations; never compose a bespoke group protocol from primitives;
- bound candidate-key trials, cryptographic work, replay state, group history,
  and failures.

## Trust assumptions

- Membership admission begins from a verifier-approved credential or explicit
  invitation/bootstrap ceremony. A human label or shared radio name is not
  authorization.
- At least one current authorized principal is permitted by the selected
  channel policy to create each accepted membership transition.
- Honest members erase consumed/superseded secret state and protect current
  private keys within platform limits.
- Relays and the delivery/routing substrate can be malicious. They may drop,
  delay, reorder, duplicate, partition, or selectively deliver messages.
- Authorized members can read and record content for their epochs and can
  maliciously use whatever action authority they hold.
- The selected standardized group construction's authentication service,
  delivery service, credential validation, policy, and extension requirements
  must be concretely realized by Samband; naming the standard is insufficient.
- No trusted wall clock or continuously available authority is assumed.

## Channel security concepts

| Concept | Required meaning |
| --- | --- |
| channel context | collision-resistant internal group context; not a human label or relay routing target |
| channel credential | verifier-approved evidence binding a client/device key to a channel principal |
| membership policy | exact rule authorizing creation, add, remove, leave, update, reinit, and recovery |
| membership epoch | one accepted roster, policy, group state, and security-key domain |
| authenticated principal | sender/client identity returned by successful security processing |
| action subject | payload-carried member/owner affected by an authorized action; may differ from sender |
| operation identity | idempotence/conflict identity for a channel action; not packet ID or replay sequence |
| protected record | one authenticated endpoint container instance with its own replay/key-use state |
| security replay state | bounded authenticated record-consumption state; distinct from mesh duplicate and semantic idempotence |

The channel context should be random or generated according to the selected
standard's group-identifier rules and must be independent from human labels.
Its exact generation, size, collision handling, and representation remain
EXP-006/RFC-0003 decisions. It stays inside the endpoint security boundary by
default.

## Membership authority options

MLS and similar group protocols authenticate who sent a proposal or commit;
the application still decides whether that principal is allowed to perform the
operation. RFC-0003 must select an exact policy.

| Policy candidate | Benefits | Security/availability costs |
| --- | --- | --- |
| single creator/administrator | simple deterministic authority and conflict resolution | administrator compromise has broad power; unavailable administrator can block recovery/removal |
| explicit administrator set | distributes availability and can rotate administrators | concurrent changes and administrator-removal rules need exact ordering |
| multiple independent approvals over the same transition | reduces single-key abuse without inventing threshold cryptography | higher latency/traffic; partition can make threshold unavailable; exact signature set and duplicate rules required |
| any-member add/update with restricted removal | decentralized and available | malicious member can expand membership; policy may be unacceptable for private channels |

A policy using multiple approvals should carry ordinary standard signatures or
standard group-authenticated proposals over one canonical transition. Samband
must not invent a new threshold signature scheme. Whatever policy is chosen
must define delegation, self-leave, last-administrator loss, compromised
administrator recovery, and subject/sender separation.

## Standard group-security candidates

### MLS as the primary experiment candidate

RFC 9420 provides authenticated group epochs, add/remove/update operations,
encrypted `PrivateMessage` application data, per-sender ratchets, forward
secrecy and post-compromise-security mechanisms, and HPKE-protected welcome
state. RFC 9750 describes authentication and delivery service responsibilities,
including eventually consistent peer-to-peer delivery.

Samband would still have to define:

- the credential and application Authentication Service rules;
- the channel authorization policy for proposals and commits;
- how the mesh realizes Delivery Service fanout, direct Welcome delivery, and
  KeyPackage availability without a central directory;
- cipher suite, required extensions, limits, padding, and private versus public
  handshake-message policy;
- deterministic resolution of concurrent commits and Welcome messages;
- state resynchronization, reinitialization, offline-member eviction, and
  bounded fork retention;
- mapping from an MLS authenticated client to Samband channel action authority;
- recipient-selection and routing metadata outside the MLS object;
- application anti-abuse, PTT, media freshness, and non-persistence.

MLS has a linear epoch history. A malicious or partitioning delivery substrate
can fork, stall, or selectively deliver group state; RFC 9750 requires the
application to resolve concurrent commits. EXP-006 must prove a specific
Samband realization rather than assuming MLS automatically merges partitions.

### Pairwise HPKE fan-out comparator

A sender can protect a separate recipient-specific operation ciphertext to each
member using RFC 9180 HPKE, avoiding one shared payload-decryption key at the
cost of linear ciphertext work. Alternatively, HPKE can wrap one common content
key independently to every recipient; that improves key delivery but all
recipients then share the payload key and its impersonation/compromise domain.
EXP-006 must measure and label these as distinct comparators.

HPKE alone does not define a roster, authority, canonical epoch, sender
signature policy, replay protection, forward secrecy after recipient-key
compromise, post-compromise recovery, concurrent change handling, or removal
convergence. Adding those from scratch would be a custom group protocol and is
not an acceptable production path. EXP-006 may use pairwise fan-out only with
an independently specified standardized authenticated group-state mechanism or
as a clearly incomplete cost baseline.

### Sender-key and static-group-key baselines

Per-sender epoch keys can make group media efficient, but their distribution,
rotation, sender authentication, nonce domains, replay, rollback, and
post-compromise behavior must come from a reviewed standard construction. A
home-grown "HPKE plus sender keys" design is prohibited.

A static shared channel secret is not a viable general Samband v0.x security
profile: any member can impersonate any other symmetric sender, removal cannot
exclude a member without complete redistribution, compromise is broad, and
multi-sender nonce coordination is hazardous. It may be measured only as an
explicitly insecure baseline, never shipped or described as end-to-end secure.

### SFrame as a later media-framing candidate

RFC 9605 provides transport-independent protected media framing and can use
keys derived from MLS. It explicitly leaves key management and receiver
anti-replay to the application, exposes its KID/counter header, and does not
provide per-sender authentication against another participant sharing the key.

SFrame therefore cannot replace the channel construction or PTT authorization.
If evaluated for AUDIO_MEDIA, its whole header should remain inside Samband's
opaque endpoint container unless EXP-007 justifies exposure, each encryption
key must be assigned to exactly one sender, full-size tags should be the
baseline under review, and Samband must add a reviewed anti-replay and
sender/action-authorization contract.

## Membership lifecycle requirements

### Create

Creation produces a fresh internal channel/group context, initial credential
set, membership policy, exact security profile, and epoch-zero state using the
selected standard. The creator's authority must be explicit; a UI label is
separate. All randomness is fixed in public vectors but unpredictable in real
operation.

### Invite and add

An invitation must be single-purpose, bounded, authenticated, expire or be
consumed according to exact rules, name the intended channel/profile and
candidate credential, and resist replay into another channel or epoch. The
joining credential is independently validated before an authorized principal
commits the add.

The new member receives only state required for the new accepted epoch. It must
not receive past application message keys. Existing members accept the new
epoch only after validating the complete transition and application policy.
If multiple candidate commits or welcomes exist, the selected profile's
deterministic conflict rule decides; arrival order alone cannot be a hidden
implementation choice.

### Remove and leave

An authorized removal creates a fresh epoch whose key state excludes the
removed member. Self-leave is either a removal request requiring authorized
commit or another exact standardized operation; local deletion alone does not
change other members' state.

Removal becomes effective for an honest endpoint only when it accepts the
fresh epoch and stops sending under the old epoch. A removed member retains all
old keys and plaintext and can continue interacting with stale components. No
document or UI may claim instantaneous global removal while partitions exist.

### Rotate and update

Fresh key state is required after add, remove, compromise recovery, sequence or
key-use exhaustion, profile transition, and any cadence demanded by the
selected construction. Periodic updates can narrow compromise windows but
cost bandwidth and can fork during partitions. Exact triggers and limits are
EXP-006 decisions.

### Device loss, compromise, and rejoin

A replacement device uses fresh credentials and joins as a distinct client. A
compromised client is removed through the same authenticated epoch transition;
other uncompromised members then update key state as required for the selected
post-compromise property. Copying an old group database or private key is not a
safe default recovery method.

An endpoint that loses rollback-sensitive replay, ratchet, or send-counter
state must not resume encryption under the old context unless the selected
standard explicitly makes that safe. The conservative recovery is a new
epoch/rejoin with fresh key material.

## Partition and merge policy candidates

RFC-0003 must select one policy for the experimental profile:

| Policy | Availability | Removal/confidentiality consequence |
| --- | --- | --- |
| freeze membership change and protected sends until convergence | lowest during partition | strongest avoidance of known stale-epoch sends, but cannot distinguish attack from ordinary outage |
| continue on last accepted epoch | high | removed/compromised member in a stale component can continue reading/sending until update arrives |
| component-local advance then deterministic reconcile/reinitialize | medium/high | forks are explicit; losing branch state and traffic cannot be reinterpreted; bounded old-state retention affects forward secrecy |

MLS's eventually consistent architecture makes the third policy a credible
experiment, but Samband must define the tie-break, commit/welcome coupling,
rollback or reinitialization behavior, and user-visible state. Authentication
proves who authored competing commits; it does not choose the canonical branch.

No merge replays missed audio. Protected control needed to restore current
membership is distinct from media and remains bounded.

## Protected endpoint container requirements

Relays forward one `OPAQUE_ENDPOINT` value. A local endpoint supplies that
value and the exact approved outer context to the channel-security profile.
The construction must logically bind and return:

- exact security-profile/construction context with downgrade protection;
- channel/group context and membership epoch;
- authenticated sending principal/client and its authorized credential state;
- protected-record replay/generation context;
- accepted inner bytes only after authentication and replay acceptance;
- enough security state to authorize the exact decoded CHANNEL/PTT/AUDIO action.

The authenticated principal is not automatically the action subject, PTT grant
owner, or media stream owner. Authorization evaluates the complete decoded
action, operation identity, sender role, subject references, current channel
epoch/policy, and exact state revision plus referenced grant/stream identifiers.
It establishes permission, not whether every semantic state precondition holds.
The next stage validates those preconditions against the same revision;
authorization, precondition check, and guarded transition are revision-bound or
atomic so a stale verdict cannot be reused.

### Security-visible header and key selection

Security-profile, channel, epoch, sender/key, sequence/generation, nonce, and
algorithm information are security-critical. They stay inside the opaque
container by default. Unknown or unsupported values fail closed at
`channel-security`; none can be treated as an ignorable semantic extension.

Keeping selectors hidden means an endpoint may have to try candidate channel
contexts. Every profile must bound the number of candidate keys/epochs tried
per packet, define ambiguous matches and collisions, and expose only a generic
local rejection. A relay-visible recipient/key hint is permitted only after
EXP-007 proves it necessary and specifies unlinkability, integrity, collision,
rotation, and abuse behavior.

## Associated outer context

Every exact profile must classify each outer element as forwarding-immutable,
hop-mutable, or transport-local and state what authenticates it against which
attacker. The endpoint protection or a separate origin proof must bind every
immutable element whose substitution can affect delivery, duplicate state,
scheduling, interpretation, or authorization, including:

- exact envelope-format and protocol-profile pair;
- `OPAQUE_ENDPOINT` outer class/type;
- origin routing context and packet identity;
- routing directive/target and traffic treatment;
- payload length/content relationship;
- applicable extension identifiers, criticality, lengths, and values.

This proposed coverage requires Agent 1 review and EXP-002 canonicalization.
It means a retry under a new outer packet identity normally creates a new
protected record/replay generation while preserving its inner operation ID.
Relays still preserve the resulting opaque payload on each forwarding copy.

The remaining hop limit is mutable and cannot simply be included in unchanged
endpoint AEAD associated data. The outer/route security profile must define its
admission and update authority. Until then, Samband cannot claim that a
malicious relay cannot reset or manipulate hop lifetime.

An outer optional extension is safe only if its registry declares scope,
mutability, repeatability, preservation/canonicalization, integrity coverage,
and failure behavior. If it can affect behavior, its identifier, criticality,
length, and value must be protected at the relevant scope.

## Replay protection model

Replay has separate domains:

| Domain | Required scope/state |
| --- | --- |
| peer handshake/session | construction transcript, fresh exchange/session state, record replay if applicable |
| routing/capability control | authenticated issuer/session/profile plus generation/revision and validity |
| channel membership transition | channel/group plus source epoch, operation/commit identity, canonical next-state rule |
| endpoint protected record | channel, epoch, authenticated sender/key domain, non-wrapping generation/sequence |
| PTT operation | channel/epoch/sender plus request, grant/term, and bounded validity/idempotence |
| audio record | channel/epoch/sender plus grant, stream, frame sequence/security generation, and freshness |

For endpoint records, the selected construction must define the replay key,
window/retention, maximum forward gap/work, reordering behavior, sequence
exhaustion, epoch rollover, state deletion, and restart/rollback recovery.
Packet ID is never part of the security freshness guarantee.

The proposed processing contract is:

1. parse only a bounded security header and locate at most the profile maximum
   candidate contexts;
2. optionally make a non-authoritative replay precheck to avoid obvious work;
3. authenticate/decrypt into private provisional storage without releasing
   plaintext or security contexts;
4. atomically check and commit authenticated replay state under concurrency;
5. only after authentication and replay acceptance, release the authenticated
   principal/context and inner bytes to bounded semantic decoding;
6. authorize and apply the inner action against current state.

Authentication/open and replay are logically distinct verdicts but need not be
separate function calls or prescribe the standard construction's internal
order. Replay state cannot advance on unauthenticated input. The proposed v0.x
policy is consume-on-authenticated-record: once step 4 commits, a later decode,
critical-extension, authorization, or state-precondition failure does not roll
back replay consumption. A legitimate semantic retry uses a fresh protected
record with the same operation ID. Agent 1 and Agent 4 must jointly review and
vectorize this choice before SG-006 can close.

Nonce/key uniqueness must follow the selected standard. If crash-safe send
state cannot be preserved, a fresh epoch/key is mandatory before encryption.
Receiver replay state must be integrity-protected or conservatively invalidated
on rollback. EXP-019 must measure secure-storage writes versus rekey cost.

## Failure and oracle policy

- No partial or unauthenticated plaintext leaves the channel-security boundary.
- Unknown profile/suite/credential/epoch/key, invalid authentication, replay,
  ambiguity, missing state, and malformed protected headers map to exact
  profile-pinned local outcomes, normally a generic
  `(channel-security, SECURITY_REJECTED)` where detail would create an oracle.
- Failure causes no inner authorization or state mutation and no automatic
  transit error.
- Any endpoint response must be authenticated, rate/amplification bounded,
  non-recursive, and reviewed for membership/key enumeration.
- Diagnostics can retain bounded local categories and ephemeral handles, never
  keys, plaintext, protected audio bytes, full membership proofs, or stable
  cross-context identifiers.

## Relay-visible and relay-hidden metadata

Relays necessarily see the selected outer metadata documented in
[`relay-security.md`](relay-security.md), including sizes and timing. They do
not see by default:

- channel/group context or label;
- roster, member credential, invitation, or membership proof;
- authenticated channel principal or action subject;
- membership epoch or group-security profile/suite;
- CHANNEL/PTT/AUDIO family or subtype;
- PTT request/grant/owner/term;
- stream, codec, sender key, media sequence, or SFrame KID/counter;
- endpoint plaintext or encoded audio.

Keeping these fields opaque prevents direct inspection but not inference from
origin/target values, traffic treatment, packet size, cadence, or colluding
observations. No anonymity or speaker-unlinkability claim follows.

## What other channel members learn

Members learn the authenticated roster/credentials, policy, epoch/group state,
and sender/action information required by the selected construction and PTT
semantics. They can read content authorized for their epochs and can retain or
redistribute it outside the protocol. Padding cannot hide sender activity from
recipients that must render the stream. Member-visible human identities and
contact data remain an application policy, not a cryptographic default.

## Compromise consequences

- Compromise of a current endpoint exposes plaintext and every current key and
  authority available to that endpoint.
- Forward secrecy protects prior content only to the exact extent the selected
  standard provides and all members deleted the needed old secrets.
- Post-compromise security begins only after an uncompromised update/commit is
  processed by the relevant honest members; rotation in name only is
  insufficient.
- A shared group key broadens sender impersonation and compromise. Per-sender
  authentication/key domains reduce that risk but do not stop malicious
  authorized content.
- Backups, cloned devices, rollback, and retained fork states can defeat
  deletion assumptions and need explicit platform evidence.

## Revocation limitations

Removal does not erase past messages or keys, force a device to delete them, or
prevent out-of-band recordings. During a partition, a removed member may keep
using an old epoch with peers that have not received the removal. Even after a
new epoch, a malicious remaining member can re-share plaintext or keys.

The strongest accurate statement for a future profile is scoped: after an
honest endpoint accepts a correctly authorized fresh epoch excluding the
removed client and erases obsolete send state, messages it sends under that
fresh epoch are intended to be inaccessible to the removed client's old keys,
subject to the selected construction and uncompromised remaining members.

## Unresolved questions

- Can MLS's Authentication and Delivery Service roles be realized without a
  central service and within Samband's routing/privacy boundaries?
- Which deterministic concurrent-commit and partition/reinitialization policy
  preserves acceptable availability and forward-secrecy state deletion?
- Which membership authority policy and bootstrap ceremony are usable offline?
- What group sizes, state, bandwidth, and update latency define the v0.x target?
- Is MLS `PrivateMessage` sufficient for control and realtime frames, or is an
  MLS-derived SFrame profile worth its extra replay/sender-auth obligations?
- Can all channel/key selectors remain hidden while keeping candidate trials
  bounded under many memberships?
- Which immutable outer fields receive endpoint binding, and what separate
  origin proof is needed for relay verification?
- How much old epoch and out-of-order state can be retained without violating
  audio non-persistence or weakening forward secrecy unacceptably?
- What secure-storage/rollback guarantees can target devices actually provide?

## Required evidence and vectors

EXP-006 must compare MLS with at least one clearly scoped alternative using
identical create/add/remove/update, concurrent-commit, partition, stale-member,
rejoin, malicious-member, state-loss, bandwidth, and memory cases. EXP-007 must
measure every proposed visible selector. EXP-019 must force crash and rollback
at each counter/epoch transition.

After construction selection, public vectors must pin the standard/profile and
suite, all public synthetic credentials/keys, every randomness input, initial
state, exact bytes, authenticated context, expected intermediate/final state,
and no-plaintext/state effects for tamper/replay/wrong-context negatives. Draft
vectors must continue using named `securityClaim: false` dispositions until
then.

## Standards considered

- [RFC 9420: The Messaging Layer Security Protocol](https://www.rfc-editor.org/rfc/rfc9420.html)
- [RFC 9750: The Messaging Layer Security Architecture](https://www.rfc-editor.org/rfc/rfc9750.html)
- [RFC 9180: Hybrid Public Key Encryption](https://www.rfc-editor.org/rfc/rfc9180.html)
- [RFC 9605: Secure Frame](https://www.rfc-editor.org/rfc/rfc9605.html)
- [RFC 5116: Authenticated Encryption Interface and Algorithms](https://www.rfc-editor.org/rfc/rfc5116.html)
- [RFC 8613: OSCORE](https://www.rfc-editor.org/rfc/rfc8613.html), as reference
  material for replay windows and state-loss handling, not as a Samband profile
