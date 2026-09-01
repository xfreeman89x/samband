# Samband Security Documentation

Status: bootstrap review surface. No cryptographic architecture is accepted.

Agent 4 owns the security architecture and must complete the
[`threat-model.md`](threat-model.md) before Protocol v1 freeze. Active design
gates are listed in [`review-gates.md`](review-gates.md).

Required future documents include node identity, channel security, relay
security, discovery privacy, key lifecycle, implementation guidance, and review
records. They must use standard cryptographic constructions and distinguish:

- transport security;
- node/session authentication;
- channel authorization and membership;
- end-to-end payload confidentiality/integrity;
- replay protection versus mesh duplicate suppression;
- metadata privacy versus content encryption.

Draft security documents are not security guarantees. Vulnerability reporting
uses [`../../SECURITY.md`](../../SECURITY.md).

