# Samband RFC Index

RFCs record material Samband Protocol semantics. A merged Draft is not an
accepted contract. Normative implementation work follows only Accepted RFCs or
an explicitly authorized experimental profile.

## Status lifecycle

```text
Draft -> Discussion -> Accepted
                    -> Rejected
Accepted/Discussion -> Superseded
```

- **Draft**: incomplete, non-normative, and open to alternatives.
- **Discussion**: complete enough for formal domain review and objections.
- **Accepted**: approved protocol decision ready for specification integration.
- **Rejected**: considered and deliberately not adopted.
- **Superseded**: replaced by a linked later RFC.

Acceptance requires the workflow in
[`../architecture/protocol-development-workflow.md`](../architecture/protocol-development-workflow.md)
and the review rules in [`../../GOVERNANCE.md`](../../GOVERNANCE.md).

## Initial RFC set

| RFC | Title | Status | Primary required reviews |
| --- | --- | --- | --- |
| [0001](RFC-0001-samband-network-model.md) | Samband Network Model | Draft | Protocol, Routing, Security |
| [0002](RFC-0002-node-identity.md) | Node Identity | Draft | Protocol, Security, Routing |
| [0003](RFC-0003-channel-identity-and-membership.md) | Channel Identity and Membership | Draft | Protocol, Security, Routing |
| [0004](RFC-0004-relay-envelope.md) | Relay Envelope | Draft | Protocol, Routing, Security |
| [0005](RFC-0005-mesh-routing.md) | Mesh Routing | Draft | Routing, Protocol, Security |
| [0006](RFC-0006-encrypted-channel-payload.md) | Encrypted Channel Payload | Draft | Security, Protocol |
| [0007](RFC-0007-ptt-arbitration.md) | PTT Arbitration | Draft | Protocol, Routing, Security |
| [0008](RFC-0008-audio-transport.md) | Audio Transport | Draft | Protocol, Security, Routing, Audio |

There are currently no Accepted RFCs and no stable Samband wire format.

## Creating an RFC

Copy [`RFC-TEMPLATE.md`](RFC-TEMPLATE.md), obtain the next four-digit number,
and use `RFC-NNNN-short-kebab-title.md`. Do not reuse a number from a rejected
or superseded RFC. Keep rationale in the RFC and cohesive normative language in
`protocol/spec` after acceptance.
