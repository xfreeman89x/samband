# Android Reference App Skeleton

Status: no Android project has been created.

The initial physical objective will be generic direct Samband packet exchange
without Internet, followed only later by multi-hop relay. Kotlin and Jetpack
Compose are proposed for the native reference app. Transport, foreground/
background service, permission, battery, thermal, and device support require
measured experiments before architecture acceptance.

Android code may implement adapters and application policy but may not redefine
shared protocol contracts.
