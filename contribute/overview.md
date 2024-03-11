---
title: Contribute to Kleene's docs
toc_max: 1
redirect_from:
- /CONTRIBUTING/
---

Keeping documentation up to date, easy to understand and with lots of
insightful/helpful examples is a huge task - and there is *always* more that
could be done. If you want to help out that is greatly appreciated!

The documentation source repos is based on Docker's, which in turn is built on Jekyll,
and provides several helpful features to make it easy to contribute. For instance,
useful UI components, easy ways to make PR's etc.

## Style Guide

The style of writing documentation is taken directly from Docker's
[Style guide](https://docs.docker.com/contribute/style/grammar/) so please
consult these pages to learn how to contribute to Kleene's docs.

Note that there are a few modifications to Docker's style guide that is
applied to Kleene's docs:

- Kleene uses the *passive* form of writing to be more consistent with the style
  of other important sources of documentation, such as the FreeBSD handbook and
  man-pages. The only deviations from this rule is when referring directly to
  the reader (e.g., as in the first paragraph of this section), and in the
  'Getting Started' guide where the user should do what is described.

- Klee is used to refer directly to the Kleene client and Kleened is used when
  referring directly to the Kleene backend component. Use `klee` when referring
  to one of Klee's commands. For instance: 'Klee is designed to be an easy,
  effective and intuitive tools for humans to interact with Kleened.
  Use `klee <subcommand>` without any arguments to print the help page of the
  subcommand'

- Kleene is used to refer to the entire Kleene stack and project. E.g., 'Kleene
  is designed to make it easier for FreeBSD users to develop and maintain isolated
  runtime environments (jails) on the FreeBSD platform'.
