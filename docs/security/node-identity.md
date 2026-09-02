# Samband Node Identity and Peer Sessions

## Status

Wave 0 candidate architecture for SG-002 and RFC-0002 review. No node
credential, signature scheme, trust store, authenticated key exchange, cipher
suite, or wire representation is selected. This document authorizes only
EXP-005 and EXP-017 design evidence, not production cryptography.

## Security goals

- prevent a peer from being accepted as an expected security principal without
  proof of possession of the credential required by local policy;
- bind the exact Samband compatibility negotiation and both session roles to
  one fresh peer session;
- keep stable identity material out of passive discovery and ordinary relay
  envelopes by default;
- separate device, discovery, session, routing, channel-member, and human
  identities so equality is never inferred across contexts;
- support offline trust bootstrap, credential rotation, device replacement,
  and compromise recovery with explicit limitations;
- provide forward-secret session keys when the selected standard construction
  and correctly erased ephemeral state justify that claim;
- bound handshake, credential-validation, and session state under active load.

## Trust assumptions

- A verifier needs an explicit local trust basis: prior fingerprint, invitation,
  channel state, deployment trust anchor, or deliberately accepted first-use
  continuity. Possession of an unknown self-issued key proves no real-world
  identity or authorization.
- Honest devices can generate random keys, protect private material, validate
  credentials, and erase superseded session secrets within platform limits.
- Discovery and transports are attacker-controlled until the selected session
  construction completes.
- No always-online certificate authority, directory, transparency service, or
  revocation service is assumed.
- One credential does not prove one physical device or prevent Sybil behavior.

## Required identity separation

Samband must not define one universal `nodeId` and reuse it at every layer. The
following values have different equality, disclosure, and lifetime rules:

| Context | Security meaning | Default exposure |
| --- | --- | --- |
| human label | local presentation only | local application |
| long-lived device credential | proof key plus verifier-defined identity assertion | only to a verifier under the selected handshake or channel construction |
| discovery handle | short-lived correlation for establishing one encounter | nearby observers |
| session-exchange identity | correlates bounded handshake messages | current one-hop exchange |
| admitted peer-session context | local handle for one completed session and assurance result | the two peers; never a global identifier |
| origin routing context | duplicate/routing scope | relays in its routing scope |
| channel member/client identity | authorization principal inside one channel security state | authorized channel members |
| channel member/action-subject/display identity | action subject and local presentation | channel/application policy |

An authenticated sender/principal is not automatically the subject of an
action. A membership administrator can remove another member; a PTT decision
issuer can grant the floor to another action subject. Future APIs and RFCs must keep
`authenticatedPrincipal`, `actionSubject`, `grantOwner`, and local display data
distinct.

## Credential architecture options

| Option | Security and trust model | Benefits | Limits and experiment questions |
| --- | --- | --- | --- |
| self-issued per-device credential with out-of-band fingerprint verification | each device has a distinct long-lived proof key; users verify a fingerprint/QR/invitation before granting continuity or channel authority | offline, decentralized, no directory required | first-contact MITM if not verified; recovery and revocation propagate only when peers reconnect; disclosure can correlate sessions |
| channel-scoped member credential | invitation/group state binds a device credential only within one channel; generic relays need not learn it | reduces cross-channel and relay correlation; aligns authority with membership | separate credential/state per channel; invitation and multi-device lifecycle complexity; cannot by itself authenticate generic routing peers |
| locally rooted device hierarchy | an offline user/deployment root authorizes separate device and scoped operational credentials using a standard certificate/container | enables device replacement and key separation without an online service | root compromise is broad; certificate format, path rules, rotation, and privacy remain unresolved |
| externally certified credential | an optional deployment validates a standard certificate chain and revocation policy | established enterprise lifecycle and accountable issuance | online provisioning/revocation assumptions, identity disclosure, tracking, and interoperability policy conflict with the base offline model |
| first-use continuity only | cache the first presented credential and detect later changes | usable for opportunistic relay continuity | first encounter is unauthenticated against active MITM; reset/reinstall ambiguity; must never grant channel membership by itself |

No option is selected. A base Samband profile must remain operable without an
online PKI. An externally certified profile can be optional only if its trust
and privacy semantics are exact and do not silently alter the base profile.

The preferred Wave 0 architectural direction for evaluation is distinct
per-device credentials, channel-scoped membership identity, and no stable
credential in discovery or the generic outer envelope. This is a privacy and
key-separation requirement, not a credential-format or primitive decision.

## Peer-session construction candidates

| Candidate | Relevant established properties | Fit questions and exclusions |
| --- | --- | --- |
| EDHOC (RFC 9528) | compact authenticated ephemeral Diffie-Hellman, transcript hashes, credential references, exporter, key update, cipher-suite negotiation, standard traces in RFC 9529 | promising lead for EXP-017; CBOR/COSE coupling, identity method, exact application profile, message correlation, error behavior, and library maturity must be measured |
| TLS 1.3 / DTLS 1.3 (RFC 8446 / RFC 9147) | mature authenticated key exchange, transcript binding, key confirmation, established libraries and analyses | transport/record assumptions, certificate or raw-public-key profile, framing overhead, datagram/stream variance, resumption linkability, and mobile/library footprint must be measured |
| Noise Protocol Framework | compact established handshake patterns with transcript hash, identity-hiding options, forward-secret patterns, and multiple implementations | the framework is marked official/unstable and Samband would have to select and correctly profile a pattern, prologue, suite, negotiation, and error behavior; it is a comparator, not a selected design |

HPKE is not an interactive mutually authenticated peer-session protocol by
itself. MLS is group key establishment, not a replacement for the one-hop peer
session. A bespoke sequence of signatures, Diffie-Hellman operations, and AEAD
messages is prohibited.

EXP-017 must compare at least two candidates using the same credentials,
Samband transcript inputs, loss/retry/role-collision cases, code/library
constraints, and resource limits. Cryptographic suite selection follows that
evidence and external review.

The experiment compares complete peer-session profiles, not only handshakes.
TLS/DTLS and Noise candidates must pin their standard post-handshake record
mode. EDHOC establishes/export keying material but does not by itself define a
generic Samband record layer; pairing its exporter with an ad hoc nonce,
sequence, replay window, and AEAD framing would be custom cryptography and is
not permitted. An EDHOC candidate is viable only with a separately reviewed
established record-protection construction whose semantics fit Samband.

## Required peer-session contract

Whatever standard construction is selected, the Samband application profile
must define and authenticate as one transcript/context:

- the complete most-recent offered set of exact `(envelope format, protocol
  profile)` pairs;
- the selected exact pair and the responder's exact echo or rejection;
- the session-exchange identity and both initiator/responder roles;
- both presented credential references and proof-of-possession results;
- any security construction, method, suite, extension, and criticality choices;
- discovery handles when they are used to bind the observed encounter;
- a freshness/session-uniqueness contribution and explicit key-confirmation
  completion point;
- application context separating Samband from every other use of the same
  standard protocol or credential.

The complete session profile must also define post-handshake record framing,
direction and purpose key separation, nonce/sequence and replay rules, loss and
reordering behavior, record size, key update/exhaustion, closure/reconnect,
restart/rollback, and per-session resource bounds. These semantics must come
from the selected standard record construction or an established reviewed
companion protocol, never from a Samband-specific exporter-plus-AEAD design.

The session is authoritative only after the selected standard construction and
required key confirmation complete. Every later link-control packet must match
the admitted exact pair and session context before it can change capability,
routing, duplicate, or other authoritative state.

Credential validation returns a local assurance result and principal context.
It does not return channel membership, route truth, relay willingness, or
permission to perform every message action. Exact authorization remains at the
applicable routing or channel boundary.

Where the selected standard exposes exporters, session keys for different
directions and purposes use its standard labels/context and only as permitted
by the selected record profile. Signing, static key agreement, HPKE/decryption,
channel membership, and application encryption keys must be separate unless a
chosen standard explicitly specifies safe shared use and the review covers it.

## Admission assurance

A profile must state the verifier's trust basis. Local implementations may
classify results such as:

- **unverified encounter:** fresh key agreement or self-asserted credential
  without trusted continuity; provides no expected-node authentication;
- **continuity verified:** the presented credential matches locally retained
  first-use state; the first encounter and reset remain caveats;
- **explicitly verified:** the credential matches an out-of-band, channel, or
  configured trust assertion;
- **deployment certified:** a profile-specific external chain and revocation
  policy validates.

These are analysis categories, not assigned wire values. RFC-0002 and the
selected profile must state which category is sufficient for neighbor,
capability, route-control, or channel-bootstrap actions. An implementation must
not display "authenticated" without naming what was authenticated and against
which trust basis.

## Discovery and credential disclosure

The stable credential, certificate fingerprint, human label, channel list, and
channel membership proof remain absent from `DISCOVERY_ADVERTISEMENT` by
default. The handshake should protect credential disclosure to the extent the
selected standard permits, but a peer that completes the handshake may learn
and retain whatever credential it verifies.

This protects against some passive observers; it does not stop a malicious
relay from completing sessions to collect credentials, peers from colluding,
or lower-layer/radio correlation. Channel-scoped or pairwise credentials can
reduce those risks but require their own bootstrap and routing analysis.

## Rotation, recovery, and revocation

- Session keys are fresh per admitted session and are never transferred to a
  reconnect merely because a discovery handle or transport address repeats.
- Credential rotation requires an authenticated transition from old to new,
  independent out-of-band verification, or a configured issuer policy. A bare
  replacement key is not self-authorizing.
- A lost or compromised device is represented as a distinct credential/member
  that must be removed or superseded. A replacement device joins with fresh
  keys; copying opaque old secret state is not an assumed recovery mechanism.
- Multi-device identity does not imply shared private keys. Each device should
  have independently revocable credentials and channel membership leaves.
- Resumption, tickets, cached aliases, and prekeys are disabled for a first
  experimental profile unless EXP-017 defines replay, expiry, single-use,
  storage, downgrade, and linkability behavior.
- Revocation is local and eventually propagated. A partitioned peer can
  continue accepting an old credential until its policy obtains and processes
  newer state; no instant global revocation is claimed.

## What a relay learns

A directly adjacent relay can learn that a Samband peer is present, the
selected exact pair, session timing, link behavior, and any credential exposed
by the chosen handshake to that verifier. It does not thereby learn channel
membership or receive channel keys. Non-adjacent relays should receive only
scoped routing identities, not the stable peer credential, unless a future
route-origin construction explicitly requires and justifies more exposure.

## What channel members learn

Authorized members learn the channel-scoped credentials and membership state
required by the selected group construction. Whether that maps to a stable
device or human identity is application policy. Members must not infer that a
channel credential is also a public discovery or routing identity.

## Behavior during partitions

Existing admitted one-hop sessions continue only while their local lifetime
and transport state remain valid. A reconnect creates a new handshake context.
Credential updates and revocations cannot be assumed globally visible during a
partition. Channel epoch rules, not peer-session continuity, decide whether a
member remains authorized to channel traffic.

## Compromise consequences

A stolen device credential permits impersonation wherever that credential is
trusted until rotation/revocation is processed. It must not automatically
expose old forward-secret peer-session keys, other devices' keys, or unrelated
channel epoch keys; those properties depend on key separation, construction,
erasure, and state actually present on the device. Full endpoint compromise can
capture current channel plaintext and act with every current local authority.

## Revocation limitations

Offline peers cannot check a live revocation source. TOFU state cannot
distinguish legitimate reset from attacker replacement without another trust
path. An externally signed revocation is useful only after it reaches a peer,
is fresh under the selected profile, and wins any conflict rule. These limits
must be visible to users and tests.

## Unresolved questions

- Which credential and trust-bootstrap option is mandatory for the base v0.x
  experiment?
- Which peer-session standard and exact authentication method best fits framed
  heterogeneous transports?
- Is generic community-relay admission allowed with only first-use continuity,
  and what authoritative routing state may it create?
- Can a stable credential remain encrypted from passive observers and still
  meet reconnect and route-origin requirements?
- How are multi-device roots, recovery, and compromised-device removal made
  usable without an online authority?
- Which secure-storage and rollback guarantees exist across target platforms?
- Which handshake errors can be sent without enabling enumeration,
  amplification, or credential oracles?

## Required evidence

- EXP-005 discovery/session binding and correlation analysis;
- EXP-017 complete handshake-plus-record construction, transcript, role,
  retry, replay, privacy, and resource comparison;
- EXP-019 restart, key-state loss, rollback, and recovery evidence;
- public standard traces and negative vectors for the chosen construction;
- independent review before SG-002 can close.

## Standards considered

- [RFC 9528: Ephemeral Diffie-Hellman Over COSE (EDHOC)](https://www.rfc-editor.org/rfc/rfc9528.html)
- [RFC 9529: Traces of EDHOC](https://www.rfc-editor.org/rfc/rfc9529.html)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 9147: DTLS 1.3](https://www.rfc-editor.org/rfc/rfc9147.html)
- [RFC 7250: Raw Public Keys in TLS/DTLS](https://www.rfc-editor.org/rfc/rfc7250.html)
- [RFC 5280: Internet X.509 PKI Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280.html)
- [Noise Protocol Framework, revision 34](https://noiseprotocol.org/noise.html)
