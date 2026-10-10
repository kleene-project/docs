#!/usr/bin/env python3
"""Check Kleene's documentation for terminology and style violations.

Implements the terminology rules of docs/contribute/style-guide.md.
Standard library only. Exit status is 1 if violations are found.

Usage:
    python3 scripts/check_terms.py [files...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

# Hand-written pages under reference/klee/ that are still scanned.
KLEE_HANDWRITTEN = {"reference/klee/cli.md", "reference/klee/configure-klee.md"}
SKIP_NAMES = {"SUMMARY.md"}
SKIP_DIRS = {"assets"}

# (pattern, replacement)
BANNED = [
    (r"\bIPNet\b|\bIpnet\b|\bipnet\b", "`ipnet`"),
    (r"\bVNet\b|\bVnet\b|\bVNET\b|\bvnet\b", "`vnet`"),
    (r"\b(?:ipnet|vnet|VNET|VNet)-container", "`vnet` container"),
    (r"\bKleened host\b", "Kleene host"),
    (r"\bbase-image\b", "base image"),
    (r"\bdockerfile\b", "Dockerfile"),
    (r"\bNullfs\b|\bNullFS\b", "nullfs"),
    (r"\bzfs\b", "ZFS"),
    (r"\bpf\b", "PF"),
    (r"FreeBSD[- ]1[34]\.\d", "FreeBSD 15.1-RELEASE"),
    (r"> \*\*(Note|Warning|Tip|Important)", "!!! note admonition"),
    (r"\{:", "attr_list syntax `{ ... }`"),
]

# Checked against the raw line (masked lines hide link URLs).
ABS_LINK = (r"\]\(/(?!assets/redoc/)", "a relative link")

FRONT_MATTER = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*\n", re.DOTALL)
FRONT_MATTER_TITLE = re.compile(r"^title:[ \t]*(.*)$", re.MULTILINE)
FRONT_MATTER_DESC = re.compile(r"^description:[ \t]*(.*)$", re.MULTILINE)
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK_URL = re.compile(r"\]\([^)\n]*\)")
BARE_URL = re.compile(r"(?:\w+://|www\.)\S+")
ATTR_LIST = re.compile(r"\{[^}\n]*\}")
HTML_TAG = re.compile(r"<[^>\n]*>")
IGNORE_HINT = re.compile(r"<!--\s*check-terms:\s*ignore\s*-->")


def blank(match):
    return " " * len(match.group(0))


def mask_line(line):
    """Blank out code spans, link URLs, bare URLs, attr lists and HTML so
    only prose is checked, preserving line length."""
    line = INLINE_CODE.sub(blank, line)
    line = LINK_URL.sub(blank, line)
    line = BARE_URL.sub(blank, line)
    line = ATTR_LIST.sub(blank, line)
    line = HTML_TAG.sub(blank, line)
    return line


def check_lines(raw_lines):
    """Yield (lineno, matched_text, replacement) for violations."""
    in_fence = False
    ignore_next = False
    for lineno, raw in enumerate(raw_lines, start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if IGNORE_HINT.search(raw):
            ignore_next = True
            continue
        if in_fence or ignore_next:
            ignore_next = False
            continue
        masked = mask_line(raw)
        for pattern, replacement in BANNED:
            for match in re.finditer(pattern, masked):
                yield lineno, match.group(0), replacement
        match = re.search(ABS_LINK[0], raw)
        if match:
            yield lineno, match.group(0), ABS_LINK[1]


def strip_front_matter(content):
    match = FRONT_MATTER.match(content)
    if not match:
        return content, ""
    return content[match.end():], match.group(0)


def front_matter_value(front, key_regex):
    match = key_regex.search(front)
    if not match:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    return value or None


def scan_file(path):
    """Return a list of violation strings for one markdown file."""
    content = path.read_text(encoding="utf-8")
    body, front = strip_front_matter(content)
    violations = []

    for key_regex, label in (
        (FRONT_MATTER_TITLE, "title"),
        (FRONT_MATTER_DESC, "description"),
    ):
        value = front_matter_value(front, key_regex)
        if value is None:
            continue
        masked = mask_line(value)
        for pattern, replacement in BANNED:
            match = re.search(pattern, masked)
            if match:
                violations.append(
                    f"{path}:front matter {label}: found "
                    f"'{match.group(0)}', use '{replacement}'"
                )

    body_offset = content.index(body)
    fm_lines = content.count("\n", 0, body_offset)
    for lineno, found, replacement in check_lines(body.split("\n")):
        violations.append(
            f"{path}:{lineno + fm_lines}: found '{found}', use '{replacement}'"
        )
    return violations


def scan_glossary(path):
    """Check the definitions in data/glossary.yaml."""
    import yaml

    with open(path, "r", encoding="utf-8") as f:
        terms = yaml.safe_load(f)
    violations = []
    for term, definition in terms.items():
        definition = definition or ""
        masked = mask_line(definition)
        for pattern, replacement in BANNED:
            match = re.search(pattern, masked)
            if match:
                violations.append(
                    f"{path} [{term}]: found '{match.group(0)}', "
                    f"use '{replacement}'"
                )
    return violations


def iter_doc_files(argv):
    if argv:
        for arg in argv:
            yield Path(arg)
        return
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if rel in SKIP_NAMES:
            continue
        if rel.startswith("reference/klee/") and rel not in KLEE_HANDWRITTEN:
            continue
        if SKIP_DIRS.intersection(path.parts):
            continue
        yield path


def main(argv):
    violations = []
    for path in iter_doc_files(argv):
        violations.extend(scan_file(path))

    glossary = REPO_ROOT / "data" / "glossary.yaml"
    if glossary.exists():
        violations.extend(scan_glossary(glossary))

    for violation in violations:
        print(violation)
    print(f"\n{len(violations)} violation(s) found.")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
