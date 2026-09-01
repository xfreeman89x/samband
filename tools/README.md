# Contributor Tools

Tools in this directory must be public, deterministic where applicable, and
portable across Windows, macOS, and Linux. They must not require private
infrastructure or credentials.

## Repository validator

Run with Python 3.11 or newer:

```shell
python tools/validate_repository.py
```

The validator checks canonical structure, UTF-8/LF Markdown, internal Markdown
links, RFC/ADR metadata and indexes, required Draft/Accepted states, and the
Apache-2.0 license structure. It uses only the Python standard library.

Future generators and vector runners must document inputs, deterministic output,
versioning, and dependency licenses here.
