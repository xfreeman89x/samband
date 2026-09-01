#!/usr/bin/env python3
"""Validate the Samband architecture bootstrap without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRECTORIES = (
    "protocol/spec",
    "protocol/schemas",
    "protocol/test-vectors",
    "protocol/compatibility",
    "core/rust",
    "simulator",
    "apps/android",
    "apps/ios",
    "bindings/kotlin",
    "bindings/swift",
    "docs/architecture",
    "docs/adr",
    "docs/rfc",
    "docs/security",
    "docs/research",
    "docs/agents",
    "tools",
    ".github/ISSUE_TEMPLATE",
)

REQUIRED_FILES = (
    "LICENSE",
    "NOTICE",
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "CODE_OF_CONDUCT.md",
    "AGENTS.md",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "docs/architecture/system-overview.md",
    "docs/architecture/network-model.md",
    "docs/architecture/component-model.md",
    "docs/architecture/dependency-graph.md",
    "docs/architecture/repository-layout.md",
    "docs/architecture/glossary.md",
    "docs/architecture/shared-contracts.md",
    "docs/architecture/protocol-development-workflow.md",
    "docs/architecture/interoperability-strategy.md",
    "docs/architecture/simulator-first.md",
    "docs/architecture/milestone-acceptance.md",
    "docs/architecture/risk-register.md",
    "docs/rfc/RFC-TEMPLATE.md",
    "docs/adr/ADR-TEMPLATE.md",
    "docs/security/threat-model.md",
    "docs/security/review-gates.md",
    "docs/research/experiment-backlog.md",
    "docs/agents/PROMPTS.md",
    "docs/agents/HANDOFF-TEMPLATE.md",
)

RFC_REQUIRED = {"0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008"}
ADR_REQUIRED = {"0001", "0002", "0003", "0004", "0005", "0006"}

RFC_STATUSES = {"Draft", "Discussion", "Accepted", "Rejected", "Superseded"}
ADR_STATUSES = {"Proposed", "Accepted", "Rejected", "Deprecated", "Superseded"}

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".toml", ".py"}
TEXT_NAMES = {
    "LICENSE",
    "NOTICE",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")
TOP_LEVEL_FIELD = re.compile(r"^([a-z_]+):\s*(.*)$")


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    )


def read_utf8(path: Path, errors: list[str]) -> str | None:
    data = path.read_bytes()
    relative = path.relative_to(ROOT).as_posix()
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{relative}: UTF-8 BOM is not allowed")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{relative}: not valid UTF-8 ({exc})")
        return None


def validate_structure(errors: list[str]) -> None:
    for relative in REQUIRED_DIRECTORIES:
        if not (ROOT / relative).is_dir():
            errors.append(f"missing required directory: {relative}")
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def validate_text_files(files: list[Path], errors: list[str]) -> None:
    mojibake_markers = ("\ufffd", "\u00ef\u00bb\u00bf", "\u00e2\u20ac", "\u00c3\u00a2")
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        text = read_utf8(path, errors)
        if text is None:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if any(marker in text for marker in mojibake_markers):
            errors.append(f"{relative}: possible corrupted text encoding")
        if text and not text.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                errors.append(f"{relative}:{line_number}: trailing whitespace")


def exact_case_exists(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False

    current = ROOT
    for part in relative.parts:
        try:
            names = {child.name for child in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part
    return current.exists()


def markdown_without_fences(text: str) -> str:
    output: list[str] = []
    active_fence: str | None = None
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if active_fence is None:
                active_fence = marker
            elif marker == active_fence:
                active_fence = None
            output.append("")
        elif active_fence is None:
            output.append(line)
        else:
            output.append("")
    return "\n".join(output)


def split_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def validate_markdown_links(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = read_utf8(path, errors)
        if text is None:
            continue
        for match in MARKDOWN_LINK.finditer(markdown_without_fences(text)):
            target = unquote(split_link_target(match.group(1)))
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            candidate = (path.parent / file_part).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{path.relative_to(ROOT).as_posix()}: link escapes repository: {target}"
                )
                continue
            checked += 1
            if not candidate.exists():
                errors.append(
                    f"{path.relative_to(ROOT).as_posix()}: broken link: {target}"
                )
            elif not exact_case_exists(candidate):
                errors.append(
                    f"{path.relative_to(ROOT).as_posix()}: link has wrong path case: {target}"
                )
    return checked


def parse_front_matter(path: Path, errors: list[str]) -> dict[str, str]:
    text = read_utf8(path, errors)
    if text is None:
        return {}
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT).as_posix()}: missing front matter")
        return {}
    end = normalized.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT).as_posix()}: unterminated front matter")
        return {}
    fields: dict[str, str] = {}
    for line in normalized[4:end].splitlines():
        match = TOP_LEVEL_FIELD.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"')
    return fields


def validate_decision_records(errors: list[str]) -> tuple[int, int]:
    rfc_files = sorted((ROOT / "docs/rfc").glob("RFC-[0-9][0-9][0-9][0-9]-*.md"))
    adr_files = sorted((ROOT / "docs/adr").glob("ADR-[0-9][0-9][0-9][0-9]-*.md"))
    rfc_index = (ROOT / "docs/rfc/README.md").read_text(encoding="utf-8")
    adr_index = (ROOT / "docs/adr/README.md").read_text(encoding="utf-8")

    seen_rfc: dict[str, str] = {}
    for path in rfc_files:
        number = path.name[4:8]
        fields = parse_front_matter(path, errors)
        for required in ("rfc", "title", "status", "created", "updated", "target"):
            if not fields.get(required):
                errors.append(f"{path.relative_to(ROOT).as_posix()}: missing {required}")
        if fields.get("rfc") != number:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: RFC number mismatch")
        status = fields.get("status", "")
        if status not in RFC_STATUSES:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: invalid RFC status {status!r}")
        if number in seen_rfc:
            errors.append(f"duplicate RFC number: {number}")
        seen_rfc[number] = status
        if path.name not in rfc_index:
            errors.append(f"docs/rfc/README.md: missing RFC index entry for {path.name}")
        index_pattern = re.compile(
            rf"^\|\s*\[{number}\]\({re.escape(path.name)}\)\s*\|.*\|\s*"
            rf"{re.escape(status)}\s*\|",
            re.MULTILINE,
        )
        if status and not index_pattern.search(rfc_index):
            errors.append(
                f"docs/rfc/README.md: status mismatch for RFC {number} ({status})"
            )

    if set(seen_rfc) != RFC_REQUIRED:
        errors.append(
            "required RFC set mismatch: "
            f"expected {sorted(RFC_REQUIRED)!r}, found {sorted(seen_rfc)!r}"
        )

    seen_adr: dict[str, str] = {}
    for path in adr_files:
        number = path.name[4:8]
        fields = parse_front_matter(path, errors)
        for required in ("adr", "title", "status", "date"):
            if not fields.get(required):
                errors.append(f"{path.relative_to(ROOT).as_posix()}: missing {required}")
        if fields.get("adr") != number:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: ADR number mismatch")
        status = fields.get("status", "")
        if status not in ADR_STATUSES:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: invalid ADR status {status!r}")
        if number in seen_adr:
            errors.append(f"duplicate ADR number: {number}")
        seen_adr[number] = status
        if path.name not in adr_index:
            errors.append(f"docs/adr/README.md: missing ADR index entry for {path.name}")
        index_pattern = re.compile(
            rf"^\|\s*\[{number}\]\({re.escape(path.name)}\)\s*\|.*\|\s*"
            rf"{re.escape(status)}\s*\|",
            re.MULTILINE,
        )
        if status and not index_pattern.search(adr_index):
            errors.append(
                f"docs/adr/README.md: status mismatch for ADR {number} ({status})"
            )

    if set(seen_adr) != ADR_REQUIRED:
        errors.append(
            "required ADR set mismatch: "
            f"expected {sorted(ADR_REQUIRED)!r}, found {sorted(seen_adr)!r}"
        )

    return len(rfc_files), len(adr_files)


def validate_license(errors: list[str]) -> None:
    path = ROOT / "LICENSE"
    text = read_utf8(path, errors)
    if text is None:
        return
    normalized = text.replace("\r\n", "\n")
    required_phrases = (
        "Apache License\n                           Version 2.0, January 2004",
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
        "1. Definitions.",
        "2. Grant of Copyright License.",
        "3. Grant of Patent License.",
        "4. Redistribution.",
        "5. Submission of Contributions.",
        "6. Trademarks.",
        "7. Disclaimer of Warranty.",
        "8. Limitation of Liability.",
        "9. Accepting Warranty or Additional Liability.",
        "END OF TERMS AND CONDITIONS",
        "APPENDIX: How to apply the Apache License to your work.",
    )
    for phrase in required_phrases:
        if phrase not in normalized:
            errors.append(f"LICENSE: canonical Apache-2.0 section missing: {phrase!r}")


def validate_repository_hygiene(files: list[Path], errors: list[str]) -> None:
    secret_patterns = (
        re.compile(r"A[K]IA[0-9A-Z]{16}"),
        re.compile(r"A[S]IA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    )
    local_path_patterns = (
        re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
        re.compile(r"/(?:Users|home)/[^/\s]+/"),
    )
    for path in files:
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        text = read_utf8(path, errors)
        if text is None:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if any(pattern.search(text) for pattern in secret_patterns):
            errors.append(f"{relative}: possible credential or private key material")
        if path.name != "LICENSE" and any(
            pattern.search(text) for pattern in local_path_patterns
        ):
            errors.append(f"{relative}: environment-specific absolute user path")


def main() -> int:
    errors: list[str] = []
    files = repository_files()
    validate_structure(errors)
    validate_text_files(files, errors)
    links_checked = validate_markdown_links(files, errors)
    rfc_count, adr_count = validate_decision_records(errors)
    validate_license(errors)
    validate_repository_hygiene(files, errors)

    if errors:
        print(f"Samband repository validation failed with {len(errors)} error(s):")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    markdown_count = sum(path.suffix.lower() == ".md" for path in files)
    print("Samband repository validation passed.")
    print(f"- files inspected: {len(files)}")
    print(f"- Markdown files inspected: {markdown_count}")
    print(f"- internal Markdown links checked: {links_checked}")
    print(f"- RFC records checked: {rfc_count}")
    print(f"- ADR records checked: {adr_count}")
    print("- UTF-8/BOM, canonical structure, license, and hygiene checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
