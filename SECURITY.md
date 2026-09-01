# Security Policy

## Current security posture

Samband is pre-implementation and pre-audit. It does not currently provide a
production-ready secure communication system. Draft documents that discuss
identity, encryption, membership, or privacy are design work, not security
claims.

Do not rely on Samband for emergency, safety-critical, regulated, or
confidential communication until a release explicitly states that its threat
model and cryptographic design have been reviewed.

## Supported versions

No released version is currently supported. Security work targets the latest
development branch until a release policy is adopted.

## Reporting a vulnerability

Prefer GitHub private vulnerability reporting for this repository when it is
available. If it is not available, do not publish exploit details. Open a
minimal public issue asking a maintainer to establish a private contact channel,
without including sensitive technical information.

Include, when possible:

- affected revision or release;
- attack preconditions and expected impact;
- a minimal reproduction that does not expose third-party data;
- suggested mitigations, if known;
- whether disclosure is time-sensitive.

Maintainers should acknowledge a private report promptly, establish a secure
communication path, assess severity, coordinate a fix and tests, and agree on a
disclosure timeline with the reporter. Exact service-level targets will be
adopted once a standing security team exists.

## Security review gates

Agent 4 or an equivalent qualified security reviewer must approve designs for:

- node identity and peer authentication;
- discovery privacy and rotating identifiers;
- channel authorization, membership changes, and key management;
- cryptographic envelope construction and replay protection;
- routing authentication and route-poisoning mitigations;
- relay metadata exposure and traffic-analysis mitigations;
- denial-of-service and resource-exhaustion bounds;
- any claim of end-to-end encryption.

The active gates are tracked in
[`docs/security/review-gates.md`](docs/security/review-gates.md). Protocol v1
cannot freeze before the threat model is complete and reviewed.

## Sensitive data rules

Never commit credentials, tokens, private keys, personal data, captured network
traffic containing private material, or private channel secrets. Never persist
raw or encoded audio, transcripts, conversations, or voice history. Diagnostic
fixtures must use synthetic identities and payloads.
