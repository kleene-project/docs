---
title: Style guide
description: Naming, voice and markup conventions for Kleene's documentation
---

This page defines the naming, voice and markup conventions for Kleene's
documentation. The terminology table is normative; when a page disagrees with
it, the page is wrong. The general rules at the end of the page apply to every
hand-written page, including this one.

## Terminology

| Entity | Prose / headings | Code (backticks) | Avoid |
|---|---|---|---|
| Project / whole stack | **Kleene** | – | kleene, KLEENE |
| Client | **Klee** ("Klee sends the request to Kleened") | `klee`, `klee run`, `klee lsc` (the command) | "the klee tool", KLEE |
| Server / daemon | **Kleened** ("Kleened builds the image") | `kleened` (rc.d service name, `sysrc kleened_enable=yes`), `/usr/local/etc/kleened/` | "the Kleened daemon" (redundant) |
| Packages | – | `kleene-daemon`, `kleene-cli` | |
| Machine running Kleened | **Kleene host** (then just "the host") | – | `Kleened host`, `host machine` |
| Kleene objects | lowercase: container, image, network, volume, execution instance, build snapshot | `klee image ls` | Container/Image mid-sentence |
| Image names and tags | – | always code: `FreeBSD-15.1-RELEASE:latest`, `webapp` | |
| Base / parent image | base image, parent image | | `base-image` |
| Build file format | **Dockerfile** (proper noun) | `Dockerfile` (the file on disk) | `dockerfile` |
| Dockerfile instructions | "the `RUN` instruction" | `RUN`, `FROM`, `CMD` | "the RUN-instruction" |
| Network drivers | always code: "an `ipnet` network", "a `vnet` container", "the `host` driver" | `--driver vnet` | `IPNet`, `VNet`, `VNET`, `Ipnet`, `ipnet-container` |
| FreeBSD | FreeBSD, ZFS, PF (write "PF, the packet filter firewall" on first use per page), jail/jails (lowercase), nullfs (lowercase; rephrase to avoid starting a sentence with it), userland | `zfs list`, `pfctl`, `zroot/kleene`, `/etc/rc` | `zfs`/`pf` in prose, Jail mid-sentence, `Nullfs` |
| Man pages | `jail(8)`, `zfs-clone(8)`, `pf.conf(5)`; link the first occurrence per page to `https://man.freebsd.org/cgi/man.cgi?query=<name>&sektion=<n>` | | |
| Docker | Docker | `docker` (the command) | |
| Example FreeBSD version | FreeBSD 15.1-RELEASE | `FreeBSD-15.1-RELEASE:latest` | 13.x / 14.x in new examples |

Notes on the table:

- Network drivers are always written in code style, even in headings and
  titles ("`vnet` networking").
- The spelling `VNET` is reserved for FreeBSD's kernel feature, cited by its
  FreeBSD name: `options VIMAGE`, or `"VNET jails"` in FreeBSD's documents.
- The client is Klee, the server is Kleened and the whole stack is Kleene.
  When a sentence is about the client/server split, name the component; when
  it is about the stack, say Kleene.
- "The Kleened daemon" is redundant: Kleened *is* the daemon. Say Kleened.
- After the first mention, "the Kleene host" can be shortened to "the host".

## Voice

- **Tutorial:** second person, imperative numbered steps ("Run `klee build`
  …"). Every part ends with a short "what you learned / next steps" section.
- **Guides and reference:** second person or neutral, present tense. Active
  voice is preferred, and procedures are written as imperatives.
- No "we", except in project and community pages.
- Headings and titles use sentence case. Proper nouns keep their capitals:
  Kleene, Klee, Kleened, FreeBSD, ZFS, PF, Dockerfile, Docker.

## Markup

- **Admonitions** use `!!! note`, `!!! tip`, `!!! warning`, `!!! important`.
  Never `> **Note**` blockquotes.
- **Links** are relative links to `.md` files
  (`[volumes](../storage/volumes.md)`), never absolute site paths. The only
  exception is the `/assets/redoc/…` path on the Kleened API page. Use
  descriptive link text, never "here".
- **Commands** go in ```console blocks with a `$ ` prompt for commands run as
  a regular user and `# ` for root. Output follows the prompt line unprefixed
  and must come from a real run: never hand-edit or invent command output.
- **Icons** use Material emoji shortcodes (`:material-console:`), not
  Bootstrap classes or Font Awesome.
- The **first mention** of a Kleene object on a page links to its glossary
  entry (`[volume](../glossary.md#volume)`, with the relative depth
  adjusted).
- **No hyphenated compounds** of names: "MariaDB container", not
  "MariaDB-container"; "a `vnet` container", not "`vnet`-container".
- Wrap prose at about 80 characters, so review comments can target small
  chunks.
