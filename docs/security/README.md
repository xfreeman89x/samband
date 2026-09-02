# Samband Security Documentation

Status: Wave 0 candidate architecture. No cryptographic profile or security
claim is accepted.

Agent 4's initial review set is:

- [`threat-model.md`](threat-model.md) — scoped threats, trust assumptions,
  residual risks, verification, and ship blockers;
- [`node-identity.md`](node-identity.md) — credential, trust-bootstrap, and
  peer-session candidates;
- [`discovery-privacy.md`](discovery-privacy.md) — rotating-identifier and
  correlation requirements;
- [`channel-security.md`](channel-security.md) — channel authorization,
  standardized group-security candidates, protected records, and replay;
- [`relay-security.md`](relay-security.md) — outer/routing admission, malicious
  relay limits, metadata budget, and resource controls;
- [`review-gates.md`](review-gates.md) — active gates and review status.

The authoritative semantic separation of identity roles is in
[`../architecture/identity-domains.md`](../architecture/identity-domains.md).
The [`Wave 0 Integration Review`](../architecture/wave0-integration-review.md)
maps every open SG gate to the affected contracts and experiments; it closes no
gate and authorizes no production security behavior.

These documents make the security problem precise but deliberately do not
select credentials, primitives, suites, encodings, routing algorithms, group
policy, or production libraries. Key lifecycle is currently covered in the
identity and channel documents; implementation guidance and formal review
records follow only after experiments select a profile.

Security work must use standard cryptographic constructions and distinguish:

- transport security;
- node/session authentication;
- channel authorization and membership;
- end-to-end payload confidentiality/integrity;
- replay protection versus mesh duplicate suppression;
- metadata privacy versus content encryption.

Draft security documents are not security guarantees. The threat model must
receive independent review, all applicable gates must close, and the selected
standard profiles must pass public vectors before stronger claims are possible.
Vulnerability reporting uses [`../../SECURITY.md`](../../SECURITY.md).
