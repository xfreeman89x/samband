# Rust Core Candidate

Status: skeleton only. [`ADR-0004`](../../docs/adr/ADR-0004-rust-shared-core.md)
is Proposed, not Accepted.

Do not scaffold a broad Rust workspace until the narrow portability/FFI
experiment has measured Android, iOS, simulator, build, ownership, error,
debugging, fuzzing, binary-size, and dependency implications.

Any future code here must consume accepted protocol specification and canonical
vectors and keep transports, UI, platform lifecycle, and audio persistence out
of the portable core.
