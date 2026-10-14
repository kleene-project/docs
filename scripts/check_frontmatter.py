#!/usr/bin/env python3
"""Front-matter sanity check for the Kleene docs.

Every hand-written page must have:
- a non-empty `title`,
- a non-empty `description`,
- no `#` H1 in the body — Material injects the H1 from the title — unless the
  page hides the navigation (the front page, which uses its own headline
  markup).

Generated pages (reference/klee/*, glossary.md, SUMMARY.md, 404.md) are
exempt. Exits non-zero with a list of violations.
"""

import sys
from pathlib import Path

import yaml

DOCS = Path(__file__).resolve().parent.parent / "docs"

# Hand-written pages that may keep an H1 in the body.
H1_ALLOWED = {"index.md"}  # the front page hides toc+navigation


def page_excluded(path: Path) -> bool:
    rel = path.relative_to(DOCS)
    parts = rel.parts
    if rel.name == "SUMMARY.md":
        return True
    if str(rel) == "index.md":
        return False
    # Generated klee reference pages and the generated glossary.
    if parts[0] == "reference" and len(parts) > 1 and parts[1] == "klee":
        return rel.name not in ("cli.md", "configure-klee.md", "cheat-sheet.md")
    if str(rel) == "glossary.md":
        return True
    return False


def violations_for(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        problems.append(f"{path}: no front matter")
        return problems
    try:
        end = text.index("\n---", 3)
        front = yaml.safe_load(text[3:end])
        body = text[end + 4:]
    except (ValueError, yaml.YAMLError) as exc:
        problems.append(f"{path}: cannot parse front matter ({exc})")
        return problems
    if not isinstance(front, dict):
        problems.append(f"{path}: front matter is not a mapping")
        return problems

    for key in ("title", "description"):
        value = front.get(key)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"{path}: missing or empty '{key}'")

    hide = front.get("hide") or []
    hides_nav = "navigation" in hide
    if not hides_nav:
        in_fence = False
        for line in body.split("\n"):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith("# "):
                problems.append(
                    f"{path}: H1 in the body; Material injects it from the "
                    f"title. Demote to '##' or hide the navigation."
                )
                break
    return problems


def main() -> int:
    problems = []
    for path in sorted(DOCS.rglob("*.md")):
        if page_excluded(path):
            continue
        problems.extend(violations_for(path))
    for p in problems:
        print(p)
    print(f"{len(problems)} front-matter problem(s) found.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
