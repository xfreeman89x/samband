# Protocol Schemas

Status: no encoding or schema language selected.

The JSON Schema in [`../test-vectors/`](../test-vectors/README.md) validates the
public Draft test-vector carrier only. It is not a Samband packet schema and
does not select JSON or JSON Schema as a wire encoding.

Machine-readable schemas will be derived from accepted specification semantics.
They are interoperability artifacts, not an alternate source of protocol truth.
Any generator must be reproducible, versioned, publicly runnable on supported
host platforms, and covered by exact-byte plus malformed-input vectors.

Schema selection requires Agent 1 Protocol review, Agent 4 parser/security
review, cross-language feasibility evidence, license review, and an RFC when it
affects wire behavior.
