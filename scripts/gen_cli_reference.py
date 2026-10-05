"""Generate the klee CLI reference pages from data/klee-reference/*.yaml.

This is the MkDocs port of the old Jekyll ``_includes/cli.md`` include, which
was invoked 56 times and rendered the YAML files produced by klee's
``scripts/generate_yaml_docs.py`` (``make docs`` in the klee repo).

The data contract is unchanged: klee introspects its Click commands and dumps
one YAML file per command. Each stub page ``docs/reference/klee/<name>.md``
rendered the YAML file ``data/klee-reference/klee_<name>.yaml``; here those
pages are generated directly in the build environment instead, from the same
YAML files, so nothing is checked in twice.

Only the keys klee actually emits are handled. The old template also carried
machinery for fields klee never produced (``inherited_options``,
``default_value``, ``min_api_version``, ``details_url``) and links into
Docker's site (/engine/deprecated/, /engine/api/...), which are not ported.

Two YAML files exist without pages: ``klee_network_lsn.yaml`` and
``klee_volume_lsv.yaml`` (shortcut aliases that Jekyll never rendered either;
they are the "network ls" alias of "network lsn" and "volume ls" alias of
"volume lsv"). They are skipped here as well, by requiring that SUMMARY.md
lists the page. This also makes a new klee subcommand fail the build (strict
mode, missing nav entry) rather than appear silently.
"""

import re
from pathlib import Path

import mkdocs_gen_files
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "klee-reference"
OUTPUT_DIR = Path("reference") / "klee"
SUMMARY = REPO_ROOT / "docs" / "SUMMARY.md"

CALLOUT = re.compile(r"^\s*\{: ?\.(note|tip|warning|important|caution) ?\}\s*$")
ANY_ATTR_LIST = re.compile(r"^\s*\{:.*\}\s*$")


def _convert_callouts(text):
    """Convert kramdown blockquote callouts to Material admonitions.

    klee's authored prose (klee/docs/*.md) carries kramdown attribute-list
    callouts: a blockquote followed by ``{: .important }``. The attribute list
    attaches to the preceding block; only blockquote targets are converted,
    bare attribute lists are dropped.
    """
    if not text:
        return text
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        match = CALLOUT.match(lines[i])
        if match and out and any(l.lstrip().startswith(">") for l in out[-3:]):
            # Collect the contiguous blockquote block that ends at out[-1].
            j = len(out) - 1
            while j >= 0 and out[j].lstrip().startswith(">"):
                j -= 1
            quote = out[j + 1 :]
            out = out[: j + 1]
            body = [re.sub(r"^\s*>\s?", "", q) for q in quote]
            while body and not body[0].strip():
                body.pop(0)
            out.append(f"!!! {match.group(1)}")
            for qline in body:
                out.append(f"    {qline}" if qline.strip() else "")
            out.append("")
            i += 1
            continue
        if ANY_ATTR_LIST.match(lines[i]) and not CALLOUT.match(lines[i]):
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


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

    short = _convert_callouts(data.get("short", ""))
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

    long_help = _convert_callouts(data.get("long", ""))
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
        lines.append(_convert_callouts(data["examples"]))
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
    for yaml_path in sorted(DATA_DIR.glob("*.yaml")):
        name = yaml_path.stem.removeprefix("klee_")
        if name not in listed:
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


main()
