# Samband Discovery Privacy

## Status

Wave 0 candidate architecture for SG-002, EXP-005, and EXP-007. No discovery
transport, alias format, rotation interval, private-discovery construction, or
wire field is selected. Rotating Samband identifiers are a required design
direction, not an anonymity or unlinkability claim.

## Security and privacy goals

- avoid broadcasting a stable node credential, human label, channel identity,
  membership proof, routing identity, or device inventory;
- limit passive correlation across encounters, locations, transports, restarts,
  and channels;
- bind the observed discovery encounter to the later authenticated session so
  substitution and stale-offer attacks are detected;
- keep discovery input non-authoritative until peer-session admission;
- bound advertisement parsing, active scans, handshake initiation, and response
  work;
- report lower-layer and traffic-analysis limits honestly.

## Trust assumptions

- Broadcast or multicast discovery is observable and forgeable by nearby
  parties.
- Transport identifiers, radio fingerprints, timing, device behavior, and
  platform APIs may remain outside Samband's control.
- Peers that have no prior relationship cannot obtain both strong identity
  authentication and passive identity hiding from an unauthenticated broadcast
  alone; trust is established in the later session or channel ceremony.
- A cryptographically secure random source is available for random handles in
  any profile that selects them.
- Discovery availability is best effort; an attacker can jam radio or flood
  advertisements.

## Discovery handle contract

A discovery handle is only a short-lived locator/correlation value for one
bounded encounter. It is not:

- a node credential or proof of possession;
- an origin routing context or routing target;
- a forwarding packet identity;
- a channel identifier or membership proof;
- permission to allocate unbounded session or routing state;
- evidence that two advertisements came from different physical devices.

The handle's syntax, entropy/collision target, maximum lifetime, rotation
events, overlap, equality scope, and restart behavior must be pinned by the
exact bootstrap profile after EXP-005. A receiver treats collisions as
ambiguous encounters and never merges identities or authority because handles
match.

## Candidate discovery designs

| Candidate | Benefits | Privacy/security limits | Evidence needed |
| --- | --- | --- | --- |
| random public ephemeral handle | supports discovery by unknown relays; no observer-computable stable-key derivation | timing, offer set, transport address, and active probing still correlate; rotation can interrupt setup | EXP-005 lifetime/collision/reconnect prototype |
| pairwise rotating handle for previously trusted peers | different observers/peers see different values; strong context separation when based on an established standard session/exported secret | cannot discover unknown community relays; desynchronization and recovery under partitions; must not invent a new PRF protocol | standard-construction review and loss/restart tests |
| channel-scoped rendezvous handle | can restrict discovery to channel contacts | risks revealing common membership and linking all members; group rotation/removal complexity; unusable for foreign relay discovery | EXP-005/006/007 analysis |
| stable or public-key-derived identifier | simple continuity | enables long-term passive tracking and cross-interface correlation | rejected for broadcast discovery |

The lead baseline for EXP-005 is a random public ephemeral handle used only to
bootstrap an authenticated session. Pairwise or channel-private discovery is a
possible optional profile after its standard construction and recovery behavior
are reviewed. Stable and deterministically public-key-derived broadcast IDs are
not acceptable for the base design.

## Advertisement data minimization

The current Draft requires enough bounded information to parse an offer and
select an exact `(envelope format, protocol profile)` pair. The bootstrap
profile must justify every additional item.

| Candidate visible item | Default decision | Risk |
| --- | --- | --- |
| discovery handle | visible, short-lived, non-authoritative | encounter correlation during its lifetime |
| bounded exact-pair offer | visible only as negotiation input | uncommon combinations fingerprint software/device deployments |
| session-exchange identity | visible only for the bounded exchange | links retries and simultaneous initiation |
| stable credential/fingerprint | hidden from discovery | direct long-term tracking and identity enumeration |
| human/device/channel label | prohibited | personal and membership disclosure |
| channel membership or proof | prohibited | membership correlation and active collection |
| raw capability snapshot | deferred until admitted session | platform/resource fingerprint and spoofed routing state |
| battery, thermal, OS, model, transport inventory | prohibited | unnecessary device fingerprinting |

EXP-007 must compare exact offer lists with coarser or padded offer classes. A
node cannot advertise an unsupported pair merely to blend in, because selecting
it would create downgrade, failure, and interoperability hazards. Any padding or
GREASE-like behavior must be defined by the bootstrap format and never treated
as support.

## Encounter-to-session binding

When a discovery handle and offer initiate a session, the selected standard
handshake profile must bind:

- the observed handle and session-exchange identity;
- the complete most-recent offered exact-pair set;
- the selected exact pair and responder echo;
- both roles and the specific transport adjacency or application context;
- fresh handshake contributions, credentials, methods, suites, and
  security-critical extensions.

This binding detects substitution, stale-offer replay, role confusion, and
downgrade at session completion. Before completion, all offers and errors are
untrusted. A new handle or reconnect never inherits old session admission,
capabilities, routes, duplicate state, or channel authority.

Rotation during an in-progress handshake must have a deterministic rule: the
exchange either remains bound to the exact handle/offer snapshot that started
it for a bounded period or restarts. It cannot silently bind to a newer
advertisement.

## Passive and active observers

Rotation primarily limits passive long-term correlation of the Samband handle.
An active observer can repeatedly initiate handshakes, correlate response
timing and credential disclosure, force radio wakeups, and compare supported
profiles. A malicious admitted peer can retain credentials it legitimately
sees and collude with other peers.

The profile therefore needs global and per-transport bounds on advertisements,
responses, concurrent handshakes, credential work, retry, and state lifetime.
Where a selected standard supports a stateless retry/cookie, EXP-017 should
measure it; no bespoke challenge is defined here. Silence or one bounded generic
failure is preferred to detailed unauthenticated errors that enable
enumeration or amplification.

## Cross-layer correlation controls

- Discovery handles must not be copied into origin routing contexts, packet
  identities, channel identifiers, logs, analytics IDs, or crash reports.
- Origin/target contexts must define their own scope and rotation. Equal-looking
  values across sessions are not correlated without an authenticated binding.
- Capability advertisements begin only after session admission and remain
  scoped to that session.
- UI labels remain local unless an authenticated endpoint protocol explicitly
  shares them with authorized members.
- Transport adapters report whether lower-layer addressing rotates and whether
  concurrent transports can expose a common stable identifier. They do not
  silently claim discovery privacy.

## What relays and observers learn

Nearby observers learn that some Samband-capable device is advertising, the
advertisement cadence/size, transport metadata, the ephemeral handle, and the
offered exact-pair fingerprint. A directly interacting relay additionally
learns handshake timing, success/failure, the selected pair, and any credential
the chosen handshake reveals to that verifier. These facts can remain
correlatable even after handle rotation.

Discovery does not need to expose a private channel, member, authenticated
principal, action subject, PTT state,
codec, or live-audio indicator. If a transport forces extra visibility, it must
be documented as a platform capability/privacy limitation.

## What channel members learn

Channel members may learn a channel-scoped credential or rendezvous value only
through the selected channel construction. That does not authorize them to
derive or publish another member's public discovery handle. Private discovery
mechanisms, if added, must rotate on member removal and avoid letting an old
member track future rendezvous values.

## Behavior during partitions

An established peer session is independent from subsequent discovery rotation.
A partition or transport loss ends or expires that session according to its
profile; later rediscovery uses a new encounter and new handshake. Pairwise or
channel-scoped discovery state can desynchronize during partitions, so any such
profile must define a bounded recovery window and fallback that does not reveal
a stable credential. Falling back to a stable public ID is prohibited.

## Compromise consequences

A compromised device reveals its current and retained discovery state and can
advertise arbitrary handles. If aliases are independently random and old
mappings are deleted, compromise need not reveal all past public handles;
actual forward privacy depends on implementation retention. Compromise of a
pairwise or channel discovery secret may link every alias derived from that
secret until rotation.

## Revocation limitations

There is no global mechanism to revoke an observed ephemeral handle; it expires.
Revoking a stable credential or channel member does not erase an observer's
historical radio observations. A removed member may retain current private
discovery material until remaining members establish a fresh epoch and stop
using the old material.

## Unresolved questions

- What handle entropy, rotation interval, overlap, and advertisement cadence
  meet collision, energy, and usability targets?
- Can profile offers be made less fingerprintable without advertising false
  compatibility or creating downgrade paths?
- Which transport identifiers rotate on Android/iOS and which remain observable
  outside Samband?
- Should unknown community relays ever receive a stable/continuity credential,
  or should generic relay sessions use a weaker explicitly named assurance?
- Can optional pairwise discovery use an existing reviewed construction and
  recover from state loss without a stable public fallback?
- What active-probing response policy balances usability, DoS, and credential
  enumeration?

## Required evidence

EXP-005 must record passive and active correlation across handle rotations,
restart, simultaneous transports, failed/completed handshakes, reconnect,
partition, and lower-layer address changes. EXP-007 must include offer-set,
cadence, response, capability, and transport metadata. EXP-017 must cover stale
offers, role collision, retransmission, state exhaustion, and credential
disclosure for each session candidate.

## Standards considered

- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973.html)
- [RFC 8386: Privacy Considerations for Broadcast/Multicast Protocols](https://www.rfc-editor.org/rfc/rfc8386.html)
- [RFC 9614: Partitioning as an Architecture for Privacy](https://www.rfc-editor.org/rfc/rfc9614.html)
- [RFC 9528: EDHOC](https://www.rfc-editor.org/rfc/rfc9528.html)
