---
title: Contribute to Klee and Kleened
description: Guidelines for contributing to Klee and Kleened
---

Do you want to hack on the Kleene project? Awesome!
Here are a few guidelines and useful information on how to get started.

This community is still in its infancy, so this is subject to change as
we gain experience. Also, remember that we are all busy people, so please
be patient with us

## Development guidelines

- As a rule of thumb, functional end-to-end tests are the primary way of testing in
  Kleene, and functional tests should be added to the Klee test-suite. Most of the
  functional tests in the Kleened repository are going to be migrated to Klee bit by bit.
- Unittests should be stored in their respective (Klee or Kleened) repositories.
- Make sure that tests runs fast, e.g., do not create a complicated `vnet` container that starts with `/bin/sh /etc/rc`
  if it can be avoided.
- Do not make pull requests for new flags, features etc. without discussing it with
  the maintainers first.
- All code for Klee should be formatted using `black`
- All code for Klee should pass `flake8` and `pylint` linters. For `flake8`, rules E501 and E701 can be ignored.
  In the rare case that it poses a problem, an inline pylint-exception can be made, i.e., `# pylint: disable=unused-argument`.
- All code for Kleened should be formatted using `mix format`.

## Creating a development environment

!!! note
    Kleene only runs on FreeBSD. Anything that drives jails, ZFS or a running
    Kleened must be executed on a FreeBSD host, e.g., inside a FreeBSD VM.

Development happens in the `klee` and `kleened` repositories; clone them and
follow their `README.md` files for how to build and run each project. The
documentation (this repository) can be built and served locally — from the
repository root, run:

```console
$ make serve
```

This creates the `.venv` if needed (see the Makefile) and starts the MkDocs
dev webserver at `http://127.0.0.1:8000/`.
