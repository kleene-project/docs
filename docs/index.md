---
description: Home page for Kleene's documentation
title: Kleene Documentation
hide:
  - toc
  - navigation
---

# ![](assets/images/kleene-logo.svg){ .title-logo } Kleene Documentation

Kleene is a container management tool for FreeBSD, similar to Docker but using
FreeBSD jails, ZFS and `pf`.

- **New to Kleene?** Start with the [Kleene overview](get-started/tutorial/index.md),
  then follow the [Get started](get-started/tutorial/index.md) guide.
- **Already familiar?** Jump into the reference documentation for
  [Klee, the command line tool](reference/klee/cli.md) and the
  [Kleened API](reference/kleened/kleened-v0.0.1.md).
- **Coming from Docker?** Kleene defines itself relative to Docker — see what
  is the same, what is different, and what Kleene deliberately leaves out in
  the [overview](get-started/tutorial/index.md) and the
  [Dockerfile reference](reference/dockerfile.md).

<div class="grid cards" markdown>

- :material-console:{ .lg .middle } __Get started__

    ---

    Containerize an application, persist its data, connect containers together —
    a step-by-step introduction to Kleene.

    [:octicons-arrow-right-24: Start the tutorial](get-started/tutorial/index.md)

- :material-book-open-variant:{ .lg .middle } __Reference__

    ---

    Every `klee` command, the Kleened REST API, and the Dockerfile syntax
    Kleene implements.

    [:octicons-arrow-right-24: Read the reference](reference/index.md)

- :material-cog:{ .lg .middle } __Operate Kleene__

    ---

    Networking, storage, jail parameters, resource limits and ZFS — running
    containers in production.

    [:octicons-arrow-right-24: Running containers](guides/run/index.md)

- :material-hand-heart:{ .lg .middle } __Contribute__

    ---

    Style guide, authoring conventions and how to build the docs locally.

    [:octicons-arrow-right-24: Contribute to the docs](project/contribute/index.md)

</div>
