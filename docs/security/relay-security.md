# Samband Relay and Routing Security

## Status

Wave 0 security requirements for SG-004, SG-005, RFC-0004, and RFC-0005.
No route algorithm, target kind, trust model, outer signature/MAC, route proof,
Sybil defense, hop-limit construction, or wire representation is selected.

The outer envelope is currently a coherent Draft processing model, not an
authenticated envelope. `OPAQUE_ENDPOINT` means relays do not parse the inner
payload; it does not by itself provide confidentiality, integrity, anonymity,
or traffic-analysis resistance.

## Security goals

- ensure the protocol gives non-member relays no channel key, membership proof,
  or plaintext, while acknowledging endpoint compromise or authorized-member
  exfiltration can defeat that relay-only boundary;
- prevent unauthenticated input from mutating authoritative session,
  capability, routing, duplicate, or forwarding state;
- distinguish immediate-peer authentication from multi-hop packet/control
  origin authentication and from truth of a routing claim;
- bind every security verdict to one exact compatibility pair, context, content,
  ingress, and declared mutable-field policy;
- limit route poisoning, capability spoofing, cache poisoning, control
  amplification, loops, and resource exhaustion even from admitted peers;
- minimize stable routing identifiers and relay-visible channel/activity
  metadata;
- preserve safe bounded operation under loss, malicious relays, partitions, and
  stale state without promising delivery or global convergence.

## Trust assumptions

- Any relay, admitted peer, route/control origin, or set of colluding relays may
  be malicious.
- Authentication can prove possession/origin and message integrity under a
  selected trust basis; it cannot prove that a route, metric, capability, or
  willingness claim is truthful.
- At least one cooperating path is required for availability. Loss, malicious
  dropping, suspension, and partition can be observationally indistinguishable.
- No global identity registry, scarce-identity issuer, trusted clock, trusted
  location, distance bound, or path-attestation infrastructure is assumed.
- Routing sees only approved outer metadata and never channel plaintext or
  keys.

## Security disposition boundary

The protocol requires logically distinct decisions, even if a selected
standard profile combines calls internally:

1. **peer-session admission** — under a future selected profile, establishes a
   one-hop security context, trust assurance, exact compatibility pair, and
   any session keys produced by that standard construction;
2. **outer-envelope admission** — validates the packet's required hop-by-hop
   and/or origin integrity/context coverage;
3. **routing/capability claim admission** — validates who is authorized to make
   the exact route, metric, revision, withdrawal, or capability assertion and
   whether its security freshness/replay state is acceptable;
4. **endpoint protected-record authentication/open** — performed only at a
   locally eligible endpoint, never by a foreign relay;
5. **endpoint security replay** — atomically admits an authenticated record in
   its bounded replay domain, never by outer packet identity;
6. **decoded action authorization** — evaluates channel/PTT/audio authority,
   keeping authenticated principal distinct from action subject.

RFC-0004 records all six logical dispositions. A selected implementation may
group them behind fewer component calls, but the required security distinctions
cannot be omitted: authenticating the immediate peer does not authorize it to
assert arbitrary third-party routes or capabilities, and opening a protected
record does not substitute for replay or action authorization.

A verdict is usable only for the exact pair, admitted session, ingress context,
packet/control bytes or canonical semantics, issuer scope, and mutable-field
classification supplied to security. It is not transferable to another packet,
session, route claim, or post-mutation envelope.

## Outer admission model candidates

| Candidate | What it can establish | Important residuals |
| --- | --- | --- |
| hop-by-hop session integrity only | current neighbor sent the admitted bytes on this session; protects link against outsiders | malicious relay can modify/re-originate immutable traffic and arbitrary packet IDs; no multi-hop origin authenticity |
| origin-authenticated immutable envelope plus hop-by-hop session protection | verified scoped origin bound immutable fields/payload; each link binds current neighbor and mutable transmission state | origin credential distribution/revocation, signature/verification DoS, linkability, and mutable hop state remain |
| trust-domain/network-wide origin credentials | stronger accountable route-control origin within a configured community | central or pre-provisioned trust, privacy loss, Sybil/account lifecycle, and offline revocation complexity |

No model is selected. A future experimental profile must name its attacker and
claim scope. If it uses only hop-by-hop integrity, it must explicitly state that
a malicious relay can alter or re-originate outer traffic; endpoint content
integrity must still survive through the channel-security construction.

## Required outer field classification

For every field and extension, the exact profile must publish:

- scope: link-local, forwarding-immutable, hop-mutable, or transport-local;
- source/issuer and authorization rule;
- equality and canonical/preserved representation;
- security coverage and the attacker against which it applies;
- permitted mutation and re-protection rule;
- privacy audience, stability, and rotation/expiry;
- failure outcome and whether any state is consumed.

At minimum this covers envelope format, protocol profile, class/type, origin
routing context, packet identity, routing directive/target, hop limit, traffic
treatment, payload length/content, and every extension identifier, criticality,
length, and value. Unknown optional bytes cannot be stripped or changed at a
scope where their presence affects behavior. Security-critical unknowns fail
closed.

## Hop-limit security boundary

The Draft hop rule is deterministic for honest relays but is not yet enforced
against a malicious relay. A profile must state:

- how the received remaining hop value is authenticated/admitted;
- which immutable origin context or initial bound, if any, is authenticated;
- how an outgoing decrement is authorized and re-protected for the next peer;
- which exact fields may change without invalidating origin/content integrity;
- the behavior for increase, reset, invalid transition, and re-identification.

Candidate protections for EXP-018 are:

| Candidate | Benefit | Limit |
| --- | --- | --- |
| one-hop session protection of current value | next peer detects outsider/link tampering and knows its neighbor sent the value | malicious neighbor can reset or choose any in-range value |
| immutable authenticated origin budget plus hop-protected remaining value | prevents exceeding an origin-selected cap when receivers enforce `remaining <= origin` | does not prove every malicious hop decremented; adds a field/metadata and requires Agent 1 review |
| reviewed path/hop attestation construction | could provide stronger transition evidence | no suitable construction or trust model is selected; path proofs can expose topology and cost bytes/CPU |

Samband must not invent a hash chain, signature chain, distance proof, or trusted
hardware scheme merely to close the schema. Until EXP-018 and RFC review select
a construction, the accurate guarantee is that honest relays decrement and all
receivers enforce the profile maximum; a malicious relay can drop, over-
decrement, reset within allowed syntax, or re-originate traffic.

## Packet identity and duplicate-cache security

Packet identity remains only the tuple component defined by RFC-0004. To avoid
turning duplicate state into a suppression attack:

- all outer and applicable routing-claim admission must complete before
  authoritative duplicate lookup or insertion;
- an unauthenticated negative cache, if used for abuse control, is separate,
  strictly bounded, and cannot suppress an admitted packet;
- the authenticated immutable comparison context excludes only fields the
  profile explicitly marks mutable;
- conflicting authenticated immutable content under one key is dropped and may
  produce only a local, redacted `PACKET_ID_CONFLICT` observation;
- global and appropriate per-attachment, session, scoped-origin, and target
  quotas bound unique-ID floods from admitted malicious peers;
- rotating origin contexts cannot silently reset all resource quotas;
- packet duplicate retention never becomes channel, routing-control, PTT, or
  cryptographic replay freshness.

An authenticated malicious origin can deliberately issue colliding IDs or many
fresh IDs. Authentication enables attribution/quota scope; it does not remove
the need for finite state and deterministic overload behavior.

## Routing-control and capability requirements

Every selected control type must state whether an assertion is authorized from
the immediate peer, a separately authenticated control origin, a locally
derived state transition, or an explicit combination.

- A direct peer cannot replace or withdraw another origin's route merely
  because its one-hop session is authenticated.
- Forwarding an unchanged control instance and originating a derived update use
  distinct authority, revision, and packet-identity rules.
- Target/scope, issuer, generation/revision, validity, metrics, capability
  claims, unknown optional content, and criticality are bound by the claim's
  integrity context.
- Claim freshness and cryptographic replay are checked before route/capability
  mutation. Delayed authenticated state cannot resurrect withdrawn or
  superseded state unless the routing profile's explicit conflict rule allows
  it.
- Session-scoped capability snapshots bind the exact session/pair, generation,
  validity, and complete canonical content. They are never reinterpreted as
  authenticated multi-hop reachability.
- Session close, admitted withdrawal, or expiry removes direct capability
  eligibility. A propagated routing consequence is a new control assertion.

If claim freshness/replay admission is stateful, the exact profile must define
its key/window, provisional-check point, authoritative commit point, and atomic
relationship to duplicate insertion and route/capability transition. It must
also pin whether authenticated claim state is consumed for every later no-
effect result, resource failure, semantic stale/conflict result, and partial
forwarding outcome. Unauthenticated input never advances it; state cannot roll
back after an observable accepted effect. This architecture does not yet choose
a consume-on-authentication or consume-on-application policy for routing claims.

Locally observed link measurements remain distinguishable from peer-advertised
and transit-derived metrics. Remote input cannot masquerade as a local
measurement. Every metric is range-checked with bounded arithmetic. The
authenticated issuer/provenance context given to routing is opaque and bounded.

## Route-poisoning and malicious-relay model

The selected routing profile must handle, within finite state/work:

- false reachability, withdrawal, generation, metric, or relay-willingness
  claims;
- blackhole and selective forwarding;
- sinkhole attraction through attractive but false metrics;
- routing loops, oscillation, count-to-infinity, and control storms;
- Sybil origins or rapid credential/origin rotation;
- colluding wormholes or tunneled adjacencies;
- replayed state after expiry, reconnect, partition, or merge;
- suppression through duplicate-cache or queue saturation.

Only a real admitted local transport/session event can create a one-hop
adjacency. A remote route assertion cannot manufacture one. Hop limit counts
Samband forwarding events, not geographic or radio distance. Authenticated
colluding peers can still tunnel valid traffic and distort apparent topology;
without separate distance/location/path trust, a clean wormhole may be
indistinguishable from a useful low-latency link.

Security supplies verified issuer/context/freshness facts. Routing alone owns
target kinds, propagation, next-hop selection, metric formula, tie-break,
fanout, queues, retries, and convergence. Neither layer may silently absorb the
other's decision.

## Sybil and abuse boundary

Proof of possession establishes control of a key, not uniqueness, reputation,
physical-device count, honest behavior, or scarce identity. In the base offline
model, strong Sybil resistance has no selected trust source.

Profiles must therefore remain safe with many untrusted credentials through
finite global/per-scope budgets, admission policy, local observations, and
bounded claim influence. Optional deployment-certified identities can support
different policy only in an exact profile with explicit centralization,
revocation, and privacy costs.

## Relay-visible metadata budget

This is the initial EXP-007 review matrix. `Required?` remains a routing/protocol
decision; visibility is not approved merely by appearing in the Draft.

| Observable item | Current proposed audience/purpose | Privacy/security risk | Required review direction |
| --- | --- | --- | --- |
| transport/radio address and attachment | direct peers; one-hop delivery | device/location correlation, cross-transport fingerprint | report platform behavior; do not copy into Samband identities |
| discovery handle and offer set | nearby observers; session bootstrap | presence, implementation fingerprint, retry correlation | rotate handle; minimize offers; bind later transcript |
| exact envelope/profile pair | every processing relay | software/profile fingerprint and downgrade target | bind to session and protected/origin context; no numeric inference |
| outer class/type | every relay; control versus endpoint dispatch | distinguishes mesh/link/endpoint activity | keep taxonomy coarse; inner family stays hidden |
| origin routing context | routing/duplicate scope | source and path correlation, quota evasion | no raw credential; minimum scope/lifetime; authenticated binding if claimed |
| routing target/directive | routing relays | recipient/contact/topology inference | no channel ID/credential; scoped opaque target; EXP-003/007 |
| packet identity | relays; duplicate suppression | packet/path correlation and sender sequencing | bounded scope; collision/restart rules; never identity proof |
| remaining hop limit | relays; forwarding bound | path/position inference and malicious mutation | compare necessity and protection in EXP-018 |
| traffic treatment | relays; queue/freshness hint | likely control/media and speaker-activity signal | retain only if EXP-003/007 proves operational need |
| payload length | relays; framing/allocation | message/codec/activity fingerprint | evaluate buckets/padding cost; always bound |
| extension identifiers/shape | relays where outer | implementation/capability fingerprint | minimal registry; authenticate criticality/presence |
| capability snapshots | admitted direct peer | relay role, lifecycle, resource/platform fingerprint | coarse session-scoped full snapshot only; no raw device state |
| timing, direction, cadence, retries | observers and relays | speaker activity, relationship, route and partition inference | measure batching/padding/cover alternatives; no hidden claim |
| route control and local telemetry | participating relays/local operator | topology, origin, behavior correlation | minimum control catalog; scoped/redacted observations |

Relays do not need channel context, member identity, membership proof,
authenticated principal, action subject,
PTT subtype, grant, stream, codec, key epoch, sender key ID, or media sequence.
Those remain inside the opaque endpoint protection by default.

Padding buckets, batching, and cover traffic may reduce some correlations but
increase latency, bandwidth, battery, and DoS surface. They remain EXP-007
alternatives. No cover traffic is assumed.

## Resource and denial-of-service requirements

Every exact profile needs finite global and appropriate per-attachment,
peer-session, asserted-origin, target, and control-class budgets for:

- framing, parsing, extension, and credential bytes;
- concurrent handshakes and authentication attempts;
- pending origin/control verification and cryptographic operations;
- peers, capability snapshots, route origins/entries/revisions, and metrics;
- duplicate/security-replay entries and retention;
- packet/control rate, fanout, queues, retries, and emitted responses;
- diagnostics and failure counters.

Invalid or over-quota claims cannot evict unrelated admitted state except under
an explicit deterministic profile rule. Resource saturation may sacrifice
availability but cannot create unbounded work, recursive errors, or a detailed
failure oracle. Authentication and signature verification costs must be part of
the bounds, including attacks by admitted peers.

## Observability and failure claims

Useful local events include session/claim admission result, route disposition,
selected local egress, enqueue/send outcome, expiry, withdrawal, no-route, and
resource rejection. They use aggregates or local scoped handles and omit
endpoint plaintext, channel identity, secrets, audio, and unnecessary stable
origin/target identifiers.

Local enqueue or transport success does not prove downstream forwarding or
delivery. Absence of delivery does not prove malicious behavior. Invalid
transit traffic gets no automatic network error; any future response requires
authentication, rate/amplification bound, non-recursion, and oracle review.

## What relays learn

Relays learn the visible metadata above for packets/control in their local
view. Direct peers may additionally learn session credentials and assurance.
Colluding relays can combine timing, packet IDs, origin/target contexts, hop
values, and path observations. Endpoint encryption prevents payload recovery
only after a real reviewed channel profile exists; it does not prevent this
correlation.

## What channel members learn

Channel members learn endpoint security and action context after successful
protected-record processing. Routing must not pass relay metadata off as
authenticated member identity. Whether endpoints expose path/relay information
to members is a separate privacy-sensitive protocol decision.

## Behavior during partitions

Old-session admission never transfers automatically to a new session. Expiry,
generation/revision, semantic staleness, packet duplicate, and cryptographic
replay remain distinct. Delayed control from a prior component or session can
be authentic yet stale. Concurrent authenticated claims require the selected
routing profile's deterministic replacement/conflict rule; security does not
create global order.

Fresh media is dropped rather than retained across partition/reconnection.
Control retention is bounded and message-specific. Revocation or relay
withdrawal affects only nodes that have received and admitted it; no immediate
network-wide effect exists.

## Compromise and revocation limitations

Compromise of a peer/session key permits link traffic forgery for that session.
Compromise of a route-origin credential permits authorized-looking false claims
within its scope until update/revocation reaches peers. It should not expose
channel payload keys if key separation holds.

Revoking a credential cannot force a malicious relay to delete metadata or
stop transmitting previously captured packets. A route or capability signature
cannot make its content truthful. Blackhole, selective forwarding, perfect
wormhole, radio jamming, and collusion remain availability/privacy risks.

## Unresolved questions

- Which outer admission model does the first experimental routing profile need?
- Which fields require multi-hop origin authentication versus one-hop session
  integrity, and how are credentials distributed without stable tracking?
- Can the single mutable `hopLimit` meet the claimed adversarial bound, or does
  RFC-0004 need a separately authenticated origin limit?
- What origin/target scope and rotation preserve routing across reconnect and
  partitions without becoming stable identifiers?
- Is visible traffic treatment operationally necessary enough to justify its
  media/activity leakage?
- Which admitted-peer/Sybil quotas preserve legitimate dense/churning meshes?
- Which route-control claims can be validated from local observations and how
  much influence may remote metrics have?
- What telemetry can help detect selective forwarding without creating a
  topology or identity database?

## Required evidence

- EXP-002 for exact authenticated canonical/preserved field coverage;
- EXP-003/004 for adversarial routing candidates and safe operating bounds;
- EXP-005/007 for origin/target and cross-hop correlation;
- EXP-012 for physical relay abuse cost;
- EXP-015/016 for capability and duplicate-cache attacks;
- EXP-017 for session assurance and credential cost;
- EXP-018 for outer/control origin admission and mutable hop state;
- independent SG-004/005 review before RFC acceptance.

## Standards and analyses considered

- [RFC 3552: Security Considerations Guidelines](https://www.rfc-editor.org/rfc/rfc3552.html)
- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973.html)
- [RFC 7416: A Security Threat Analysis for RPL](https://www.rfc-editor.org/rfc/rfc7416.html)
- [RFC 8386: Privacy Considerations for Broadcast/Multicast Protocols](https://www.rfc-editor.org/rfc/rfc8386.html)
