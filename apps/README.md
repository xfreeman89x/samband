# Native Reference Applications

Reference applications prove Samband on physical platforms; they do not define
the protocol. No application implementation exists.

- [`android/`](android/README.md) is reserved for the Android reference app and
  official-API transport adapters.
- [`ios/`](ios/README.md) is reserved for the iOS reference app and transport
  adapters.

[`ADR-0005`](../docs/adr/ADR-0005-native-mobile-reference-apps.md) remains
Proposed pending platform experiments. Apps must advertise actual runtime
capabilities and must not simulate unsupported relay/background behavior.
