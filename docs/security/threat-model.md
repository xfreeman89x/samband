# Samband Threat Model

## Status

Initial Wave 0 threat model, dated 2026-09-02. This document defines the
security problem and release blockers; it does not close SG-001, select a
cryptographic profile, authorize production implementation, or establish a
security claim. Independent security review and evidence from the referenced
experiments are still required.

The current protocol and RFCs are Draft designs under review. Terms such as
"protected payload", "authenticated", and "confidential" below describe
required properties of a future reviewed profile, not current behavior.

## Critical property

The security architecture must eventually justify this statement for a
specific reviewed profile:

> A node that does not belong to a private radio channel can relay Samband
> traffic for that channel without being able to recover or undetectably
> modify the protected channel payload.

Here, the relay-only guarantee means Samband does not provision channel keys or
plaintext to that relay and the selected endpoint protection resists the named
relay attacker. It cannot cover a compromised endpoint or an authorized member
that deliberately gives the relay plaintext or key material.

This property requires endpoint-to-endpoint channel protection. One-hop
transport encryption or peer authentication alone cannot provide it. It also
does not imply anonymity, hidden traffic patterns, trustworthy routing,
delivery, fair PTT arbitration, or protection after an endpoint is
compromised.

## System in scope

The model covers discovery, one-hop session establishment, the Samband outer
envelope, routing-visible control, opaque endpoint forwarding, channel
membership and key state, CHANNEL/PTT/AUDIO inner actions, local key storage,
diagnostics, and the future portable-core/platform boundary.

The operating environment includes disconnected use, changing one-hop links,
multi-hop community relays, packet loss/reordering/duplication, partitions and
merge, device restart, and no continuously reachable authority. Audio is live
and ephemeral; raw audio, encoded frames, conversations, transcripts, and
voice history are outside permitted persistence.

Production cryptographic code, production networking, routing algorithms,
mobile applications, codecs, and audio pipelines remain outside Wave 0.

## Assets

| Asset | Required protection |
| --- | --- |
| channel payload and live encoded media | confidentiality and integrity between authorized endpoints; no persistence |
| channel membership and authority state | authenticated changes, rollback/fork detection, bounded history |
| node, device, and channel credentials | confidentiality where appropriate, integrity, key separation, rotation, recovery |
| session, channel, epoch, and sender keys | secrecy, context separation, controlled lifetime, erasure |
| PTT grants and stream bindings | origin/action authorization, freshness, replay rejection |
| routing and capability state | admitted origin/context, freshness, bounded influence, safe degradation |
| replay and duplicate state | integrity, rollback handling, bounded memory, distinct semantics |
| relationship and presence metadata | minimization, context separation, limited linkability and retention |
| device resources | bounded parser, CPU, memory, radio, battery, queue, and storage work |
| protocol negotiation | exact selection, transcript binding, downgrade resistance |
| diagnostics and crash artifacts | no secrets, endpoint plaintext, audio, or unnecessary stable identifiers |

## Actors and attacker capabilities

**Honest endpoint.** Follows the selected profile, protects current secrets,
and applies local policy correctly until compromise.

**Honest relay.** Forwards only admitted traffic within bounded policy, but is
not assumed to be a channel member or to understand endpoint plaintext.

**Passive nearby observer.** Records discovery advertisements, radio/link
identifiers, packet timing, direction, size, cadence, and visible Samband
metadata. It can correlate observations over time and across locations.

**Active unauthenticated neighbor.** Advertises arbitrary capabilities and
profiles; injects, replays, truncates, delays, reorders, duplicates, and floods
frames; initiates many handshakes; and attempts downgrade and oracle attacks.

**Malicious admitted peer or community relay.** Holds valid state for its own
one-hop sessions. It can drop, selectively forward, delay, reorder, duplicate,
modify, replace, or originate outer traffic; lie about capabilities, routes,
metrics, and willingness; collude with other relays; and retain all metadata it
can observe. It has no private-channel entitlement merely because it relays.

**Malicious channel member.** Holds legitimate current channel secrets and can
decrypt traffic available to that membership epoch. It can record or disclose
plaintext outside Samband, inject authorized-looking traffic within its
permissions, monopolize PTT, withhold membership updates, and collude with
relays or removed members.

**Malicious or compromised administrator.** Exercises every membership action
the selected authorization policy grants that administrator. Cryptography
cannot make an authorized but malicious decision benign.

**Compromised device.** Exposes keys and state available on that device and can
act with its current authorities until peers process a recovery or revocation
transition. A full OS compromise can also capture audio before protection or
after opening.

**Removed member.** Retains every credential, plaintext, ciphertext, and key it
obtained before removal and may remain connected to a stale partition.

**Implementation or supply-chain attacker.** Exploits parser, cryptographic
library, unsafe/FFI, dependency, update, logging, backup, or crash-reporting
weaknesses.

Attackers may collude. The model does not assume a unique physical device per
credential or prevent an attacker from creating many untrusted pseudonyms.

## Trust assumptions

- Standard constructions are secure only when used according to their
  specifications, with approved suites, correct libraries, and valid public
  test vectors.
- Honest endpoints have a cryptographically secure random source and a way to
  protect and erase key material within the limits of their platform.
- A user or deployment can perform at least one explicit trust-bootstrap
  ceremony for channel membership, such as comparing a fingerprint or scanning
  an invitation. The exact ceremony is not selected.
- No relay, transport, discovery mechanism, routing claim, wall clock, or
  continuously reachable server is globally trusted.
- Local monotonic time can order events while a process runs, but wall clocks
  may be absent, skewed, or attacker-influenced. Restart can lose volatile
  counters unless the profile defines rollback-safe recovery.
- Availability requires at least one usable path of cooperating nodes. No
  cryptographic mechanism can force a relay to forward.
- Channel members are trusted with plaintext for epochs in which they are
  authorized. They are not trusted to be fair, non-recording, or non-colluding.
- Platform radio identifiers and physical-layer fingerprints may remain
  observable even when Samband identifiers rotate.

## Trust boundaries

| Boundary | Untrusted input | Required decision before authority changes |
| --- | --- | --- |
| transport to parser | arbitrary frame bytes and rate | bounded framing/length admission |
| discovery to session | aliases, profile offers, link claims | authenticated key establishment and exact transcript binding |
| peer session to capability/routing | peer identity assurance, snapshots, control | profile-specific admission, freshness, limits, and policy |
| outer envelope to duplicate/routing | origin, target, packet ID, hop state, treatment | outer admission appropriate to the claimed assurance |
| relay to endpoint security | opaque bytes and visible outer context | protected-container authentication plus security replay acceptance |
| endpoint security to inner state | channel, authenticated principal, action subject, epoch, plaintext action | membership/action authorization and state preconditions |
| core to application/FFI | events and buffers | ownership, zeroization, non-persistence, bounded diagnostics |
| durable storage to live state | credentials, counters, epochs, replay state | integrity, rollback policy, freshness or mandatory rekey |

No result at one boundary substitutes for a later result. In particular,
forwarding duplicate suppression is not cryptographic replay protection, a
peer session is not channel membership, and payload confidentiality is not
metadata privacy.

## Security goals

1. Through the protocol, only endpoints authorized for a channel epoch can
   recover its protected payloads under the stated compromise assumptions;
   authorized-member exfiltration and endpoint compromise remain residuals.
2. A recipient detects modification, cross-channel substitution, sender/epoch
   substitution, and profile downgrade before releasing plaintext from the
   security boundary. It rejects unauthorized decoded actions before
   application delivery or state mutation; private bounded decode necessarily
   occurs before action authorization.
3. Each accepted channel, PTT, and media action is bound to an authenticated
   channel/authenticated-principal/security context and a replay domain.
4. Session negotiation binds both offered and selected exact compatibility
   pairs, roles, session-exchange identity, credentials, and the complete
   transcript before capability or routing state becomes authoritative.
5. Discovery, routing, and packet identifiers are separated from stable
   credentials and scoped to the smallest context and lifetime routing can
   support.
6. Relays learn only metadata justified by routing or bounded scheduling; they
   do not receive channel keys, membership proofs, authenticated principal,
   action subject, PTT subtype,
   codec, epoch, or endpoint plaintext by default.
7. Malformed, forged, replayed, duplicated, looping, or flooded input causes
   bounded CPU, memory, bandwidth, battery, storage, and response work.
8. Add, remove, rotate, compromise, restart, partition, and merge behavior is
   explicit, deterministic where required, and honest about delayed revocation.
9. Security-critical versions and extensions fail closed without fallback to
   plaintext, transport-only protection, or an older profile.
10. Secrets, plaintext, and audio do not enter prohibited logs, backups, crash
    artifacts, or test fixtures.

## Explicit non-goals and unavoidable limits

- guaranteed delivery, globally consistent routing, or resistance to a relay
  that simply drops traffic;
- one global PTT speaker across disconnected partitions;
- anonymity or unlinkability against a global observer, colluding relays, or
  radio/platform fingerprints;
- hiding all packet size, timing, direction, path length, or activity cadence
  without measured padding/batching/cover-traffic costs;
- preventing an authorized member from recording or redistributing content;
- retroactively protecting plaintext or keys exposed before compromise or
  removal;
- instantaneous revocation across disconnected components;
- making a signed route, metric, capability, or PTT request truthful merely
  because its origin is authenticated;
- protecting microphone/speaker plaintext on a fully compromised endpoint;
- safety-critical or emergency-service guarantees.

## Threat register

`Required` means the future profile must implement and verify the control.
`Open` means the construction or evidence is not yet selected.

| ID | Threat and attack path | Required controls | Residual risk and status |
| --- | --- | --- | --- |
| TM-01 | node impersonation through substituted discovery/session credentials | explicit identity-assurance level; proof of possession; transcript-bound exact profile; verified bootstrap for trusted continuity | first-contact/TOFU impersonation and recovery remain open; SG-002 |
| TM-02 | unauthorized channel membership or forged invitation/update | authenticated member credential; explicit add/remove authority; canonical group/epoch state; action authorization | malicious authorized inviter/admin remains powerful; SG-003 |
| TM-03 | non-member relay reads or changes endpoint payload | channel-only endpoint protection spanning every relay; context-bound integrity; no relay key distribution | timing/size/route metadata remains; SG-006 |
| TM-04 | malicious member impersonates another member, leaks content, or sends prohibited actions | per-sender origin authentication, least-authority action policy, audit-safe local events, bounded abuse policy | member can record/share plaintext and may DoS within its permissions; SG-003/007 |
| TM-05 | packet injection by unauthenticated neighbor or admitted malicious peer | staged cheap validation, peer/outer admission, origin/context binding where claimed, rate/state quotas | admitted origins and Sybils can still flood within limits; SG-004/005 |
| TM-06 | replay of a valid protected action, including rewrapping under a new packet ID | authenticated per-channel/epoch/sender replay domain; atomic check/commit; operation idempotence; bounded reordering | crash rollback and long partition windows are open; SG-006 |
| TM-07 | exact-profile or cryptographic downgrade and cross-protocol confusion | bind complete offer, selected pair, roles, credentials, profile/suite, and security-critical extensions into one transcript/context | bootstrap grammar and resumption remain open; EXP-002/017 |
| TM-08 | forged packet IDs poison duplicate caches or collisions suppress valid traffic | do not commit authoritative cache before required admission; bind ID/origin/immutable content where claimed; per-origin quotas; conflict detection | authenticated malicious origin can deliberately collide/flood; EXP-016 |
| TM-09 | route poisoning, false withdrawal, metric or capability spoofing | authenticated control origin/context and freshness; bounded claim influence; prefer local observations; explicit expiry/withdrawal | authentication cannot prove a route or metric truthful; SG-005 |
| TM-10 | blackhole, selective forwarding, wormhole, looping, or colluding relays | alternate-path evidence, hop/duplicate/resource bounds, anomaly-safe local policy, convergence tests | perfect wormholes and intentional dropping can be undetectable; availability not guaranteed |
| TM-11 | Sybil peers consume route, session, duplicate, or crypto state | pre-auth and per-peer/global quotas, rate limits, stateless challenge where selected, finite admission/state | no global identity or scarce-resource authority is selected; Sybil prevention remains a blocker for strong claims |
| TM-12 | discovery tracking through stable identifiers or distinctive offers | rotating random discovery handles; no stable credential/channel/label in broadcast; minimized/padded offer sets where viable | lower-layer addresses, RF fingerprints, timing, and rare profiles remain correlatable; EXP-005/007 |
| TM-13 | stable-identifier correlation across sessions, channels, transports, or relays | distinct identity domains; scoped pseudonyms; encrypted credential disclosure where construction permits; retention limits | peers that legitimately learn the same credential can collude; SG-002/004 |
| TM-14 | channel/member/speaker inference from origin, target, treatment, size, cadence, and control patterns | field-by-field metadata budget; hide inner family/context; scoped routing values; evaluate padding/batching | realtime traffic analysis remains substantial without costly cover traffic; EXP-007 |
| TM-15 | parser, allocation, decompression, or cryptographic CPU exhaustion | maximum frame/field/extension sizes; no attacker-controlled unbounded allocation; cheap checks before crypto; bounded failed-handshake work | high-rate physical jamming and distributed floods remain |
| TM-16 | queue, bandwidth, battery, duplicate/replay table, membership-history, or storage exhaustion | per-class/per-peer/global caps; finite retention/fanout/retry; no recursive errors; load shedding without state growth | availability can be sacrificed under saturation; EXP-003/012/016 |
| TM-17 | compromised device exposes identity/channel keys and live plaintext | key separation, secure storage, minimal retention, rekey/rejoin, credential revocation, explicit compromise UX | compromise window lasts until honest members process fresh state; past/current exposure depends on construction |
| TM-18 | removed member reads future traffic from a stale partition or replays old authority | removal creates a fresh epoch excluding it; old epoch never authorizes new epoch; explicit partition policy and bounded stale-state retention | immediate global revocation is impossible offline; SG-003/EXP-006 |
| TM-19 | rollback after crash restores used nonce/counter, accepted replay window, or stale membership state | persist next-use state before encryption or require a fresh key/epoch; authenticated durable state; reject ambiguous rollback | platform rollback resistance and write cost are open; EXP-019 |
| TM-20 | concurrent membership changes fork group state during partition/merge | standard group-state rules; deterministic conflict/tie-break policy; bounded fork retention; explicit reinitialization/rejoin | availability, forward secrecy, and convergence trade off; EXP-006 |
| TM-21 | forged/stale PTT grant, release, or media binding; malicious member monopolizes floor | channel/principal/subject/term/grant/stream binding; replay and expiry; bounded requests; authorization before state mutation | cryptography cannot enforce fairness or prevent RF/audio jamming; SG-007/EXP-008 |
| TM-22 | diagnostic, backup, crash, test, or telemetry leakage; accidental audio persistence | allowlisted safe observations; synthetic fixtures; artifact scans; no payload/audio logging; key redaction/zeroization | platform crash reporters and third-party SDKs need later audit; SG-008/009 |
| TM-23 | dependency, cryptographic API, unsafe/FFI, or supply-chain failure | maintained reviewed libraries, pinned provenance, minimal unsafe boundary, fuzzing, advisory/license process | implementation work and dependency selection are not authorized yet; SG-009 |

## Partition, removal, and compromise model

A partition creates multiple local views; it cannot create a globally current
membership or PTT state. A future channel profile must choose and test one of
these availability policies rather than leaving behavior implementation-defined:

- freeze security-sensitive membership changes or protected transmission until
  a canonical next epoch is available;
- allow partition-local continuation on the last accepted epoch and explicitly
  accept that a removed member in another component may continue to receive or
  transmit stale-epoch traffic;
- advance a component-local epoch and later perform a reviewed deterministic
  merge/reinitialization, never reinterpreting stale-epoch data as current.

No policy gives instantaneous offline revocation. Removal protects future
traffic only after an honest endpoint has accepted a fresh epoch that excludes
the removed member and has erased obsolete send keys. Previously obtained
plaintext and keys cannot be revoked. Post-compromise recovery similarly begins
only after uncompromised members process a fresh update under a construction
that provides that property.

Missed audio is never retained or replayed to repair a partition. Old security
state retained for bounded control reordering must not become a voice-history
store.

## Denial-of-service and resource model

Processing must remain layered:

1. enforce transport byte/rate/buffer bounds;
2. parse only a fixed or bounded prefix and validate declared lengths;
3. reject unsupported format/profile/criticality before expensive work;
4. apply bounded pre-authentication rate and handshake-state limits;
5. perform session, outer, and applicable routing/capability-claim admission
   required by the exact profile;
6. commit authoritative duplicate, route, capability, or replay state only
   after the admission that protects that state;
7. reserve finite work before observable forwarding or endpoint effects;
8. emit no unauthenticated recursive or amplifying error traffic;
9. record only bounded, privacy-safe local outcomes.

Authentication does not make work free. Every profile must publish limits for
concurrent handshakes, credential chains, signature/tag checks, peers,
capabilities, route origins, duplicate and replay entries, channel members,
epochs/forks, pending operations, queues, fanout, retries, and responses.

## Privacy analysis boundary

Content protection and metadata privacy are separate. The current outer model
can expose envelope/profile, outer class/type, origin and target contexts,
packet identity, remaining hop limit, traffic treatment, length, extension
shape, timing, direction, and capability/control patterns. Discovery can expose
presence and supported-profile fingerprints. Transports can expose radio
addresses and physical characteristics.

The future metadata budget must identify, for every observer and relay, why
each visible item is necessary, its scope and lifetime, correlation potential,
integrity requirement, and mitigation cost. A field cannot be made visible
merely because it simplifies routing. In particular, plaintext channel IDs,
member/sender identity, membership proofs, PTT request/grant data, stream IDs,
codec, and key epoch remain inside the opaque endpoint boundary by default.

Rotating Samband identifiers cannot justify an anonymity or unlinkability claim
while timing, packet sizes, lower-layer identifiers, route targets, or colluding
peers remain linkable. Padding, batching, and cover traffic are candidates for
EXP-007, not assumed controls.

## Verification plan

- EXP-002/017: exact-pair and cryptographic-suite transcript binding, role
  collision, stale offer, retry, resumption, and downgrade corpus.
- EXP-005: passive and active correlation of discovery aliases across restart,
  reconnect, transport changes, and partitions.
- EXP-006: standardized group-security comparison and bounded prototype for
  add/remove, concurrent commits, stale components, merge/reinit, state, and
  bandwidth.
- EXP-007: observer-by-observer metadata inventory plus padding/batching cost.
- EXP-008: unauthorized/replayed PTT actions, malicious-member monopolization,
  and partition conflict.
- EXP-015/016: authenticated capability freshness and duplicate-cache poisoning
  with strict state/work high-water assertions.
- EXP-018: outer and route-control authentication alternatives, mutable hop
  state, forged origins, and malicious-relay behavior.
- EXP-019: forced restart/rollback, nonce uniqueness, replay-state recovery,
  epoch rollover, and secure-storage write cost.
- Later implementation evidence: standard known-answer/negative vectors,
  parser and state-machine fuzzing, differential interoperability, dependency
  review, secret/audio artifact scans, and external cryptographic review.

## Ship blockers

- SG-001 is not closed until this model receives independent review and the
  accepted scope/trust assumptions are recorded.
- No node credential, trust-bootstrap, peer-session, recovery, or discovery
  privacy profile is selected.
- No channel authority, membership conflict policy, or standardized group-key
  construction is selected and proven under partitions.
- No protected-payload construction, suite, associated-data coverage, nonce,
  replay, rollback, key-erasure, or failure-oracle policy is selected.
- No outer/route-control origin-admission model or malicious-relay guarantee is
  selected; mutable hop-limit integrity remains unresolved.
- EXP-002, EXP-005 through EXP-008, and EXP-015 through EXP-019 lack evidence.
- No external security review has closed release-blocking findings.

Until those blockers close, Samband must not claim end-to-end encryption,
anonymity, unlinkability, forward secrecy, post-compromise security, immediate
revocation, or production security.

## Related documents and standards considered

- [`node-identity.md`](node-identity.md)
- [`channel-security.md`](channel-security.md)
- [`relay-security.md`](relay-security.md)
- [`discovery-privacy.md`](discovery-privacy.md)
- [`review-gates.md`](review-gates.md)
- [RFC 3552: Guidelines for Writing RFC Text on Security Considerations](https://www.rfc-editor.org/rfc/rfc3552.html)
- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973.html)
- [RFC 8386: Privacy Considerations for Protocols Relying on IP Broadcast or Multicast](https://www.rfc-editor.org/rfc/rfc8386.html)
- [RFC 7416: A Security Threat Analysis for RPL](https://www.rfc-editor.org/rfc/rfc7416.html)
