# Samband Identity Domains

## Status and authority

This document defines the architectural separation and permitted relationships
among Samband identity domains. It does not select a credential, identifier
encoding, cryptographic algorithm, trust model, routing target construction, or
channel-security profile.

Concrete peer-visible representations remain Draft work in
[`RFC-0002`](../rfc/RFC-0002-node-identity.md),
[`RFC-0004`](../rfc/RFC-0004-relay-envelope.md), and
[`RFC-0005`](../rfc/RFC-0005-mesh-routing.md). Security mechanisms and claims
remain blocked by the applicable gates in
[`review-gates.md`](../security/review-gates.md).

## Architectural rule

Samband has no universal protocol `nodeId`. In this document, **Node Identity**
means only the credential-bearing security-principal role defined by a future
selected profile; it is not a generic peer, route, channel, packet, device, or
human identifier. Equality, authentication, or continuity in one domain does
not imply equality, authentication, authority, or continuity in another
domain.

In particular:

```text
credential identity
    != discovery handle
    != peer-session identity
    != routing origin or target
    != channel context
    != channel principal
    != action subject
    != packet identity
    != endpoint operation identity
    != PTT request or grant identity
    != media stream or sequence context
    != human-facing label
```

A selected security or routing profile may define an explicit binding between
two domains. The binding must state its scope, lifetime, disclosure, authority,
rotation, and failure behavior. Equal-looking bytes, a shared display label, a
transport address, or application convention never creates such a binding.

## Domain registry

| Domain | Semantic role | Lifetime and scope | Who sees it | Stable? | Linkable? | Authentication | Carried across relays? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Credential Identity (the credential-bearing Node Identity role) | A device or other credential-bearing security principal evaluated against an explicit trust basis. It is not a human identity, route, peer session, or channel membership. | Longer-lived than one session; scoped by the selected credential and verifier policy; rotation, recovery, and revocation are explicit. | The holder and every verifier or observer to whom the selected construction exposes it; the architecture makes no confidentiality or anonymity claim. | Stable only for its credential lifetime; never globally permanent by architecture. | Linkable by anyone who learns the same credential; cross-context exposure must be minimized and measured. | Unresolved. Proof and assurance are defined only by a future selected security profile. | Not in the generic relay envelope or discovery broadcast by default. Any exception requires explicit review. |
| Discovery Handle | A minimal locator/correlation value for one bounded link-local discovery encounter. | Short-lived; scoped to one transport-visible encounter, including a defined rotation/overlap window. | Nearby observers and participants in that discovery mechanism. | No. | Intended to correlate only its bounded encounter, but timing, behavior, offers, or lower-layer identifiers may enable wider correlation; no anonymity or unlinkability claim. | The broadcast value is non-authoritative; a future session profile may bind the observed handle into its authenticated transcript. | No. |
| Session-Exchange Identity | Correlates the bounded messages of one peer-session establishment attempt and resolves retry or simultaneous initiation. | One link-local exchange; expires on success, rejection, timeout, or restart according to the selected bootstrap profile. | The two participants and nearby observers when the transport exposes it. | No. | Intended for its bounded exchange; observers may still correlate it with lower-layer or timing data. | It gains no authority itself; a future session profile may bind it into an authenticated transcript. | No. |
| Admitted Peer-Session Context | Names one admitted one-hop Samband session, its exact compatibility pair, roles, and admission or assurance result. | One admitted immediate-peer session; invalid after closure and never transferred to a reconnect or another ingress. | The two peers and local protocol, routing, and policy components. | No across sessions. | Locally linkable for the active session; any link to a credential follows a future selected security profile. | Real authentication awaits SG-002. The simulation profile supplies only a structured synthetic verdict containing `securityClaim: false`. | No; a session verdict is not transferable. |
| Origin Routing Context | May scope a forwarding origin, contribute to a profile-supplied duplicate scope, or scope some abuse accounting when an exact routing profile requires it. It is not a source route or credential. | No wider or longer than the selected routing profile requires; rotation, expiry, restart, and quota continuity must be explicit. | Relays within the forwarding/control scope that needs it. | Provisional and profile-specific. | Linkable within its visible scope; cross-session or cross-profile linking requires an explicit reviewed binding. | Origin or claim authentication is unresolved; immediate-peer authentication is insufficient. | Only when the exact routing profile requires it. Its universal necessity remains unresolved. |
| Routing Target Identifier | Lets a selected routing profile test local eligibility and choose bounded forwarding actions without making plaintext channel identity or membership generic relay metadata. It carries no privacy guarantee. | Target-kind-specific advertisement/discovery/use window with explicit rotation, overlap, expiry, takeover, and stale-partition rules. | Relays in the target's routing scope and the locally eligible endpoint. | Stable only for the minimum measured routing window. | Linkable for that scope; must not be a raw credential or plaintext channel identifier. | Ownership, claim issuer, and local-delivery admission are separate profile-defined results. | Only for target kinds that require it. |
| Packet Identity | Correlates relay copies of one forwarding instance for mesh duplicate suppression. It is not a principal, operation identity, acknowledgement, or replay value. | One profile-bounded duplicate-retention domain. | Relays processing that forwarding instance. | No beyond the profile's bounded duplicate scope. | Linkable while copies and retained duplicate state remain observable. | None by itself; it proves no origin, authenticity, authorization, ordering, or freshness. | Yes, unchanged across relay copies of the same forwarding instance. |
| Channel Context Identifier | Selects the channel/security state under which a future endpoint profile evaluates a record. It is not a member principal or action subject. | Profile-defined channel lifetime and accepted epoch or equivalent security-state interval. | Authorized endpoints and their local channel-security boundary; any peer-visible representation is unresolved. | Profile-specific. | Potentially linkable inside its exposed scope; relay-visible exposure requires explicit Metadata/Privacy review. | A future selected endpoint profile must bind it to the record and accepted security state. No construction is selected. | Not as generic relay-readable metadata. |
| Channel Principal | A channel-scoped member/client principal returned by a future reviewed endpoint security profile. It is distinct from a credential identity and from the subject of an action. | One channel credential and accepted membership epoch or other profile-defined channel-security context. | Authorized endpoints and the local channel-security boundary. | Stable only as required by the selected channel construction and epoch lifecycle. | Linkable inside the channel context; no cross-context unlinkability claim exists. | Established only when the future profile's record-authentication/open and security-replay gates accept. | Not as generic relay-readable metadata. Any endpoint carriage and protection await the selected profile. |
| Action Subject | The member, membership target, request owner, grant owner, stream owner, or other entity affected by a decoded action. | One endpoint operation and the bounded state to which its authorization verdict is revision-bound. | Authorized endpoints after the future endpoint security gates accept. | Operation/state-specific. | Profile- and application-specific inside the endpoint context. | Protecting the value is not enough: the complete action must be authorized for the authenticated channel principal and current state. | Not as generic relay-readable metadata. Any endpoint carriage and protection await the selected profile. |
| Endpoint Operation Identity | Correlates retries or conflict handling for one decoded channel operation. It is not a packet duplicate key or security-replay value. | Operation-specific, with profile-defined retention and restart behavior. | Authorized endpoints after endpoint security processing. | Only for the operation's bounded lifecycle. | Linkable within that operation lifecycle. | Its binding to the complete authorized action awaits a selected endpoint profile. | Not as generic relay-readable metadata. |
| PTT Request / Grant Identity | Distinguishes a PTT request from a decision/grant and its owner under a future PTT state machine. | One request or grant lifecycle, including explicit expiry and partition behavior. | Authorized endpoints participating in that channel operation. | No beyond the bounded PTT lifecycle. | Linkable within that lifecycle. | Authorization and principal/subject bindings remain Draft and security-blocked. | Not as generic relay-readable metadata. |
| Media Stream / Sequence Context | Scopes media ordering and freshness inside one future granted stream. It is not wall-clock time, hop state, packet identity, or security replay by itself. | One bounded stream and its non-wrapping sequence domain. | Authorized endpoints after the future media-security boundary accepts it. | No beyond the stream lifecycle. | Linkable within the stream; traffic analysis may correlate more broadly. | Sender/grant/stream/sequence bindings remain unresolved pending the endpoint media-security profile. | Not as generic relay-readable metadata. |
| Human-Facing Label | Local presentation data for a person, device, or channel. | Local application policy. | The local user unless an explicit endpoint action shares it. | Application-defined. | Application-defined; never a protocol trust signal. | None by default. | Not as generic relay-readable metadata; an explicit future endpoint action may carry it. |

## Packet identity is not an identity principal

The relay-envelope packet identity is an opaque duplicate-correlation token for
one forwarding instance. The current Draft duplicate key also includes the
exact compatibility pair and the duplicate scope supplied by the exact
profile. A profile may derive that scope from an origin routing context, but a
distinct origin field is not universal. Packet identity is preserved across
relay copies but proves no origin, authenticity, authorization, ordering,
acknowledgement, channel operation identity, or security freshness.

Whether an origin routing context remains a mandatory common key component for
every future routing candidate is unresolved. An experimental simulation
profile may pin one synthetic scope so duplicate experiments are executable;
that fixture does not settle the general protocol decision.

## Routing claim roles

Every routing or capability claim keeps these concepts distinct:

```text
immediate peer principal
claim issuer
claimed subject or target
origin routing context
locally eligible delivery subject
local-only abuse quota scope
```

An authenticated peer may replace only the claim slot that the selected profile
authorizes it to own. Authentication establishes who made a bounded assertion;
it does not prove proximity, link symmetry, link quality, forwarding, metric
truth, resource state, target ownership, or route availability.

## Endpoint action roles

Endpoint processing keeps the authenticated channel principal separate from an
action subject, membership target, PTT decision issuer, request subject, grant
owner, stream owner, and media sender. A selected profile must define the exact
authorization relationship. Authorization is bound to the complete decoded
action, current channel/security epoch, referenced identifiers, and state
revision; it cannot be reused after that state changes.

## Simulation-only representations

The Wave 1 simulation profile uses distinct typed fixture values such as:

- `SyntheticCredentialIdentity` only when a credential-bearing test role is
  required;
- `SyntheticDiscoveryHandle`;
- `SyntheticSessionExchangeIdentity`;
- `SyntheticPeerSessionContext`;
- `SyntheticOriginRoutingContext`, `SyntheticRoutingTarget`, and
  `SyntheticPacketIdentity`;
- `SyntheticChannelContext`, `SyntheticChannelPrincipalContext`, and
  `SyntheticActionSubject`.

A generic `SyntheticNodeIdentity` may be used only as a local simulator host
label. It must not cross a protocol boundary or stand in for several identity
domains. Every synthetic action or verdict is a structured fixture that
contains `securityClaim: false`; a bare Boolean or an omitted flag is invalid.
This applies to peer-session admission, outer admission, routing-claim
admission, routing disposition, channel-open, security-replay, inner-decode,
and action-authorization fixtures. An opaque simulator endpoint payload is an
unparsed fixture, not a protected or encrypted payload. None of these fixtures
supports authentication, privacy, channel-security, replay-protection, or
end-to-end-encryption claims.

## Review and change rule

Changing the separation, audience, equality, or authority of a peer-visible
domain requires the governing RFC and Protocol/Security/Routing reviews. A
concrete representation cannot be promoted from the simulation profile until
its privacy lifetime, authentication or admission rule, restart behavior,
resource bounds, and vectors are complete.
