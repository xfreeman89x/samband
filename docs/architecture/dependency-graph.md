# Dependency Graph and Rules

## Permitted direction

```text
protocol specification and canonical vectors
                 |
                 v
      transport-independent contracts
        /          |             \
       v           v              v
 protocol codec  routing   reviewed security adapters
        \          |             /
         +---------+------------+
                   v
           node orchestration
             /           \
            v             v
    simulator harness   native app layer
                           |
                           v
                  platform transport/audio
```

Arrows mean "may depend on". Protocol artifacts are consumed by all
implementations but depend on none of them.

## Mandatory rules

1. `protocol/` never depends on `core/`, `simulator/`, `apps/`, or `bindings/`.
2. Protocol codecs do not depend on routing algorithms, transports, UI,
   persistence, or platform APIs.
3. Routing depends only on protocol-approved relay metadata, abstract time and
   randomness, capabilities, and abstract link metrics.
4. Routing never depends on channel plaintext, channel secrets, audio codecs,
   or mobile APIs.
5. Security components use reviewed standard primitives and explicit protocol
   inputs. They do not select routes or open physical links.
6. The portable core depends on transport interfaces, never concrete platform
   adapters.
7. Transport adapters depend inward on stable interfaces; core code never
   imports Wi-Fi, Bluetooth, Android, Apple, Internet, or simulator types.
8. Applications compose core, adapters, policy, UI, and audio devices. They may
   not implement alternate packet, routing, identity, channel, or PTT semantics.
9. The simulator consumes the same core contracts and canonical vectors as
   physical implementations. Test-only shortcuts cannot alter semantics.
10. Bindings translate a narrow approved API. Platform packages do not become
    dependencies of the portable core through FFI.
11. No component persists audio or channel plaintext. Diagnostics use synthetic
    or redacted payloads.
12. Cyclic dependencies across these boundaries are prohibited.

## Data ownership rules

- Byte ownership and lifetime must be explicit at FFI and transport boundaries.
- Secret material must remain in the smallest reviewed security boundary.
- Routing state is bounded and expires; it is not a permanent global database.
- Duplicate/replay caches have explicit size and time bounds.
- Platform capability snapshots are inputs, not inferred constants.
- Test-vector files are immutable once published for a released protocol
  version; corrections create a new vector/version with provenance.

## Extension rules

New transports implement the transport interface. New wire extensions follow
accepted version-negotiation rules. New routing metrics require routing and
protocol review when they alter peer-visible behavior. New channel-protection
features require security review. A dependency exception requires an ADR and,
if interoperability changes, an RFC.

## Enforcement plan

The bootstrap validator enforces documentation structure and decision-record
metadata. Later implementation waves should add package-graph checks, forbidden
import checks, dependency-license scanning, decoder fuzzing, and vector runners
without making one operating system mandatory.
