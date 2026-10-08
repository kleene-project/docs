"""Generate the glossary page from data/glossary.yaml.

The YAML file is the single source of truth for terms; this script renders
it as Markdown during the build.

Terms are rendered as `##` headings so the definitions can cross-reference
each other with plain #anchor links, which is what the YAML data already does
(e.g. "[zfs](#zfs)").
"""

import re
from pathlib import Path

import mkdocs_gen_files
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = REPO_ROOT / "data" / "glossary.yaml"


def _slug(text):
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


def main():
    with open(GLOSSARY, "r", encoding="utf-8") as f:
        terms = yaml.safe_load(f)

    lines = [
        "---",
        'title: "Glossary"',
        'description: "Glossary of terms used around Kleene"',
        "hide:",
        "  - toc",
        "---",
        "",
    ]
    for term, definition in terms.items():
        lines.append(f"## {term}")
        lines.append("")
        lines.append(definition.strip())
        lines.append("")

    with mkdocs_gen_files.open("glossary.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


main()
