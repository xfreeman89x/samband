# Language Bindings

Status: no binding API or generator is accepted.

Bindings may expose a deliberately narrow portable-core interface to native
applications. They translate ownership, errors, cancellation, and callbacks
without becoming a second implementation of protocol semantics.

The Rust/shared-core experiment in
[`../docs/adr/ADR-0004-rust-shared-core.md`](../docs/adr/ADR-0004-rust-shared-core.md)
must justify an FFI boundary before binding code is added.

