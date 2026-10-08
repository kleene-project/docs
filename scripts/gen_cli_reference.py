"""Generate the klee CLI reference pages from data/klee-reference/*.yaml.

The YAML files are produced by klee's ``scripts/generate_yaml_docs.py``
(``make docs`` in the klee repo), one per command: klee introspects its
Click commands and dumps ``command``/``short``/``long``/``usage``/
``options``/``examples`` plus parent/child links. Each nav entry
``docs/reference/klee/<name>.md`` is generated here in the build
environment from ``data/klee-reference/klee_<name>.yaml``, so nothing is
checked in twice.

Every YAML file must correspond to a nav entry: generation is keyed on
SUMMARY.md, so a new klee subcommand without a nav entry fails the build
(strict mode) rather than appearing silently - and, conversely, a stale
YAML file with no page is not silently ignored either.
"""

from pathlib import Path

import mkdocs_gen_files
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "klee-reference"
OUTPUT_DIR = Path("reference") / "klee"
SUMMARY = REPO_ROOT / "docs" / "SUMMARY.md"

def render_command_page(data):
    """Render one command's YAML data as Markdown, mirroring _includes/cli.md."""
    lines = []

    if data.get("shortcut"):
        target = data["shortcut"].replace(" ", "_")
        lines.append(
            f"> This command is a shortcut to "
            f"[`klee {data['shortcut']}`](/reference/klee/{target}/)."
        )
        lines.append("")

    short = data.get("short", "")
    if short:
        lines.append(short)
        lines.append("")

    if data.get("usage"):
        lines.append("## Usage")
        lines.append("")
        usage = data["usage"].replace("\t", "")
        if data.get("cname"):
            usage = f"{usage} COMMAND"
        lines.append("```console")
        lines.append(f"$ {usage.strip()}")
        lines.append("```")
        lines.append("")

    long_help = data.get("long", "")
    if long_help and long_help.strip() != (data.get("short") or "").strip():
        if data.get("options"):
            lines.append(
                "Refer to the [options section](#options) for an overview of "
                "available `OPTIONS` for this command."
            )
            lines.append("")
        lines.append("## Description")
        lines.append("")
        lines.append(long_help)
        lines.append("")

    if data.get("examples"):
        lines.append(
            "For example uses of this command, refer to the "
            "[examples section](#examples) below."
        )
        lines.append("")

    options = data.get("options") or []
    if options:
        lines.append("## Options")
        lines.append("")
        lines.append("| Name, shorthand | Description |")
        lines.append("|:----------------|:------------|")
        for opt in options:
            name = f"`--{opt['option']}`"
            if opt.get("shorthand"):
                name = f"{name}, `-{opt['shorthand']}`"
            desc = " ".join((opt.get("description") or "").split())
            desc = desc.replace("|", "\\|")
            lines.append(f"| {name} | {desc} |")
        lines.append("")

    if data.get("examples"):
        lines.append("## Examples")
        lines.append("")
        lines.append(data["examples"])
        lines.append("")

    if data.get("pname") and data["pname"] != "klee":
        parent_page = data["pname"].replace("klee ", "").replace(" ", "_")
        lines.append("## Parent command")
        lines.append("")
        lines.append("| Command | Description |")
        lines.append("|:--------|:-------------|")
        lines.append(f"| [`{data['pname']}`](/reference/klee/{parent_page}/) | |")
        lines.append("")

    if data.get("cname"):
        lines.append("## Child commands")
        lines.append("")
        lines.append("| Command | Description |")
        lines.append("|:--------|:-------------|")
        for cname in data["cname"]:
            datafile = cname.replace("klee ", "").replace(" ", "_")
            lines.append(f"| [`{cname}`](/reference/klee/{datafile}/) | |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def nav_pages():
    """Pages listed under reference/klee/ in docs/SUMMARY.md, in nav order."""
    pages = []
    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- [") and "](reference/klee/" in line:
            target = line.split("](", 1)[1].rstrip(")")
            if target.endswith(".md"):
                pages.append(target.removeprefix("reference/klee/").removesuffix(".md"))
    return pages


def main():
    if not DATA_DIR.is_dir():
        raise SystemExit(
            f"gen_cli_reference: {DATA_DIR} not found - run 'make docs' in the klee repo first"
        )

    listed = nav_pages()
    unlisted = []
    for yaml_path in sorted(DATA_DIR.glob("*.yaml")):
        name = yaml_path.stem.removeprefix("klee_")
        if name not in listed:
            unlisted.append(yaml_path.name)
            continue
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        page = OUTPUT_DIR / f"{name}.md"
        content = render_command_page(data)
        with mkdocs_gen_files.open(page, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: {data.get('command', name)}\n---\n\n")
            f.write(content)
        mkdocs_gen_files.set_edit_path(page, None)

    if unlisted:
        # A YAML file with no nav entry is either a new klee command that needs
        # a SUMMARY.md entry, or a stale file that should be deleted. Both are
        # drift between klee and the docs; fail the build rather than guess.
        raise SystemExit(
            "gen_cli_reference: YAML files without a nav entry in docs/SUMMARY.md "
            "(add them or delete the stale files): " + ", ".join(unlisted)
        )


main()
