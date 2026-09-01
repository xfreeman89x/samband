# Contributing to Samband

Samband welcomes protocol analysis, documentation, simulation, implementation,
security review, tests, and reproducible platform research.

## Before starting

1. Read the [project overview](README.md) and
   [architecture index](docs/architecture/README.md).
2. Read accepted RFCs and ADRs that govern the area. Draft RFCs are not
   implementation authority.
3. Check the [shared-contract registry](docs/architecture/shared-contracts.md)
   before changing identity, channels, capabilities, envelopes, routing, PTT,
   audio, versioning, or test-vector semantics.
4. For substantial work, open an issue or draft RFC/ADR before investing in an
   implementation that may conflict with the protocol.

## Choose the right decision record

- Use an RFC for observable protocol semantics or interoperability contracts.
- Use an ADR for repository or implementation architecture that does not alter
  protocol semantics.
- Use a research note or experiment plan when evidence is needed before a
  decision can be made.

The full workflow is in
[`docs/architecture/protocol-development-workflow.md`](docs/architecture/protocol-development-workflow.md).

## Development rules

- Keep the protocol independent of transports and platforms.
- Preserve the separation between the transport mesh and private channels.
- Never require a relay to join a channel merely to forward its opaque traffic.
- Never persist microphone audio, encoded audio frames, conversations,
  transcripts, or voice history.
- Never invent cryptographic algorithms or claim end-to-end encryption before
  review.
- Keep malformed-input work bounded and test failure behavior.
- Avoid unrelated refactors in focused changes.
- Add no dependency without documenting its purpose, maintenance health,
  license, portability, and security implications.
- Keep tooling usable on Windows, macOS, and Linux.

## Validation

Run the repository-level checks from the repository root:

```shell
python tools/validate_repository.py
git diff --check
```

Component-specific commands will be added to the component README after a
toolchain ADR is accepted. A change is not complete until its relevant build,
tests, documentation, malformed-input cases, security impact, and
interoperability impact have been checked.

## Pull requests

Use a focused title, preferably following Conventional Commits, for example:

```text
docs: clarify RFC acceptance gate
feat: add deterministic duplicate-cache scenario
fix: reject zero-hop relay envelopes
```

A pull request should state:

- the problem and intended outcome;
- files and contracts affected;
- protocol, public API, security, and interoperability impact;
- tests and validation performed;
- assumptions, limitations, and follow-up work;
- the RFC or ADR that authorizes a material shared-contract change.

Do not combine protocol-semantic changes with broad implementation cleanup.

Maintainers should label bounded, dependency-safe documentation and test tasks
as `good first issue` only when their governing contracts are clear enough that
a new contributor will not unknowingly decide protocol semantics.

## Contributions and licensing

The repository is licensed under Apache License 2.0. Under section 5 of that
license, intentionally submitted contributions are provided under the same
terms unless explicitly stated otherwise. Do not submit material you do not
have the right to contribute.

Third-party code or assets must have a license compatible with Apache-2.0 and
must retain all required notices. Add required attributions to `NOTICE` and
document the dependency review in the pull request.

## Security reports

Do not disclose exploitable vulnerabilities in a public issue. Follow
[`SECURITY.md`](SECURITY.md).

## Conduct

Participation is governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
